from __future__ import annotations

import gc
import os
import PIL
import time
import torch
import random
import datetime
import traceback
import threading

from typing import Type, Union, Any, Optional, List, Tuple, Dict, Callable, Literal, Set, BinaryIO, TYPE_CHECKING
from hashlib import md5

from math import ceil
from pibble.api.configuration import APIConfiguration
from pibble.api.exceptions import ConfigurationError, BadRequestError
from pibble.util.files import dump_json, load_json
from pibble.util.numeric import human_size

from enfugue.diffusion.constants import *
from enfugue.diffusion.util import get_vram_info
from enfugue.util import (
    logger,
    check_download,
    human_duration,
    check_make_directory,
    find_file_in_directory,
    get_file_name_from_url,
    get_domain_from_url,
    redact_for_log,
    check_make_directory_by_names,
)

__all__ = ["DiffusionPipelineManager"]

DEFAULT_MODEL_FILE = os.path.basename(DEFAULT_MODEL)
DEFAULT_INPAINTING_MODEL_FILE = os.path.basename(DEFAULT_INPAINTING_MODEL)
DEFAULT_SDXL_MODEL_FILE = os.path.basename(DEFAULT_SDXL_MODEL)
DEFAULT_SDXL_INPAINTING_MODEL_FILE = os.path.basename(DEFAULT_SDXL_INPAINTING_MODEL)
DEFAULT_SDXL_REFINER_FILE = os.path.basename(DEFAULT_SDXL_REFINER)

if TYPE_CHECKING:
    from diffusers.pipelines.stable_diffusion import StableDiffusionPipelineOutput
    from diffusers.pipelines.stable_video_diffusion import StableVideoDiffusionPipeline
    from diffusers.models import (
        ControlNetModel,
        AutoencoderKL,
        AutoencoderTiny,
        ConsistencyDecoderVAE
    )
    from diffusers.schedulers.scheduling_utils import KarrasDiffusionSchedulers
    from enfugue.diffusion.pipeline import EnfugueStableDiffusionPipeline
    from enfugue.diffusion.animate.pipeline import EnfugueAnimateStableDiffusionPipeline
    from enfugue.diffusion.util import ModelMetadata
    from enfugue.diffusion.support import (
        ControlImageProcessor,
        Upscaler,
        IPAdapter,
        BackgroundRemover,
        Interpolator,
        Conversation,
        DragAnimatorPipeline,
        Unimatch
    )
    from torch import Tensor

def noop(*args: Any) -> None:
    """
    The default callback, does nothing.
    """

class KeepaliveThread(threading.Thread):
    """
    Calls the keepalive function every <n> seconds.
    """

    INTERVAL = 0.5
    KEEPALIVE_INTERVAL = 15

    def __init__(self, manager: DiffusionPipelineManager) -> None:
        super(KeepaliveThread, self).__init__()
        self.manager = manager
        self.stop_event = threading.Event()

    @property
    def stopped(self) -> bool:
        """
        Returns true IFF the stop event is set.
        """
        return self.stop_event.is_set()

    def stop(self) -> None:
        """
        Stops the thread.
        """
        self.stop_event.set()

    def run(self) -> None:
        """
        The threading run loop.
        """
        last_keepalive = datetime.datetime.now()
        while not self.stopped:
            time.sleep(self.INTERVAL)
            now = datetime.datetime.now()
            if (now - last_keepalive).total_seconds() > self.KEEPALIVE_INTERVAL:
                callback = self.manager.keepalive_callback
                logger.debug(f"Pipeline still initializing. Please wait.")
                callback()
                last_keepalive = now


class DiffusionPipelineManager:
    TENSORRT_STAGES = ["unet"]  # TODO: Get others to work with multidiff (clip works but isnt worth it right now)
    TENSORRT_ALWAYS_USE_CONTROLLED_UNET = False  # TODO: Figure out if this is possible
    LOADABLE_EXTENSIONS = [".safetensors", ".ckpt", ".pt", ".pth", ".pb", ".caffemodel", ".bin"] # AI models

    DEFAULT_CHUNK = 64
    DEFAULT_SIZE = 512
    DEFAULT_TEMPORAL_CHUNK = 4
    DEFAULT_TEMPORAL_SIZE = 16

    is_default_inpainter: bool = False
    is_default_animator: bool = False

    _keepalive_thread: KeepaliveThread
    _keepalive_callback: Callable[[], None]
    _scheduler: KarrasDiffusionSchedulers
    _pipeline: EnfugueStableDiffusionPipeline
    _refiner_pipeline: EnfugueStableDiffusionPipeline
    _inpainter_pipeline: EnfugueStableDiffusionPipeline
    _animator_pipeline: EnfugueAnimateStableDiffusionPipeline
    _task_callback: Optional[Callable[[str], None]] = None
    _ip_adapter_model: Optional[IP_ADAPTER_LITERAL] = None

    def __init__(
        self,
        configuration: Optional[Union[Dict[str, Any], APIConfiguration]] = None,
        optimize: bool = True
    ) -> None:
        self.configuration = APIConfiguration()
        if configuration is not None:
            if isinstance(configuration, APIConfiguration):
                self.configuration = configuration
            else:
                self.configuration = APIConfiguration(**configuration)
        if optimize:
            self.optimize_configuration()
        self.apply_patches()

    def optimize_configuration(self) -> None:
        """
        Gets information about the execution environment and changes configuration.
        """
        vram_free, vram_total = get_vram_info()
        if self.device.type == "cpu" or vram_total < 16 * 10 ** 9:
            self.configuration["enfugue.pipeline.cache"] = None
            self.configuration["enfugue.pipeline.switch"] = "unload"
            if vram_total < 12 * 10 ** 9:
                # Maximum optimization
                self.configuration["enfugue.pipeline.sequential"] = True

    def task_callback(self, message: str) -> None:
        """
        Calls the passed task callback if set.
        """
        if getattr(self, "_task_callback", None) is not None:
            self._task_callback(message) # type: ignore[misc]
        else:
            logger.debug(message)

    def set_task_callback(self, callback: Callable[[str], None]) -> None:
        """
        Sets the task callback.
        """
        self._task_callback = callback

    def clear_task_callback(self) -> None:
        """
        Clears the task callback.
        """
        try:
            delattr(self, "_task_callback")
        except AttributeError:
            pass

    def apply_patches(self) -> None:
        """
        Injects various modifications of global packages.
        """
        self.patch_freeu()
        self.patch_downloads()

    def patch_freeu(self) -> None:
        """
        Steals `apply_freeu`
        """
        from enfugue.diffusion.util.torch_util.inference_util import apply_freeu
        import diffusers.utils.torch_utils

        diffusers.utils.torch_utils.apply_freeu = apply_freeu # type: ignore[assignment]

    def get_download_callback(self, file_label: str) -> Callable[[int, int], None]:
        """
        Gets the callback that applies during downloads.
        """
        last_callback = datetime.datetime.now()
        last_callback_amount: int = 0
        bytes_per_second_history = []

        def progress_callback(written_bytes: int, total_bytes: int) -> None:
            nonlocal last_callback
            nonlocal last_callback_amount
            this_callback = datetime.datetime.now()
            this_callback_offset = (this_callback-last_callback).total_seconds()
            if this_callback_offset > 1:
                difference = written_bytes - last_callback_amount

                bytes_per_second = difference / this_callback_offset
                bytes_per_second_history.append(bytes_per_second)
                bytes_per_second_average = sum(bytes_per_second_history[-10:]) / len(bytes_per_second_history[-10:])

                estimated_seconds_remaining = (total_bytes - written_bytes) / bytes_per_second_average
                estimated_duration = human_duration(int(estimated_seconds_remaining), compact=True)
                percentage = (written_bytes / total_bytes) * 100.0
                self.task_callback(f"Downloading {file_label}: {percentage:0.1f}% ({human_size(written_bytes)}/{human_size(total_bytes)}), {human_size(bytes_per_second)}/s, {estimated_duration} remaining")
                last_callback = this_callback
                last_callback_amount = written_bytes

        return progress_callback

    def patch_downloads(self) -> None:
        """
        Steals huggingface hub HTTP GET to report back to the UI.
        """
        import huggingface_hub
        import huggingface_hub.file_download

        huggingface_http_get = huggingface_hub.file_download.http_get

        def http_get(url: str, out: BinaryIO, *args: Any, **kwargs: Any) -> Any:
            """
            Call the task callback then execute the standard function
            """
            file_label = "{0} from {1}".format(
                get_file_name_from_url(url),
                get_domain_from_url(url)
            )
            if self.offline:
                raise ValueError(f"Offline mode enabled, but need to download {file_label}. Exiting.")

            self.task_callback(f"Downloading {file_label}")

            return check_download(
                url,
                out,
                resume_size=kwargs.pop("resume_size", 0),
                text_callback=self.task_callback
            )

        huggingface_hub.file_download.http_get = http_get

    def check_download_model(self, local_dir: str, remote_url: str) -> str:
        """
        Downloads a model directly to the model folder if enabled.
        """
        if not remote_url.startswith("http"):
            return remote_url
        output_file = get_file_name_from_url(remote_url)
        output_path = os.path.join(local_dir, output_file)
        found_path = find_file_in_directory(
            self.engine_root,
            os.path.splitext(output_file)[0],
            extensions = [".ckpt", ".bin", ".pt", ".pth", ".safetensors"]
        )

        if found_path:
            return found_path

        if self.offline:
            raise ValueError(f"File {output_file} does not exist in {local_dir} and offline mode is enabled, refusing to download from {remote_url}")

        file_label = "{0} from {1}".format(
            output_file,
            get_domain_from_url(remote_url)
        )
        self.task_callback(f"Downloading {file_label}")

        check_download(
            remote_url,
            output_path,
            text_callback=self.task_callback
        )

        return output_path

    def start_keepalive(self) -> None:
        """
        Starts a thread which will call the keepalive callback every <n> seconds.
        """
        if not hasattr(self, "_keepalive_thread") or not self._keepalive_thread.is_alive():
            keepalive_callback = self.keepalive_callback
            self._keepalive_thread = KeepaliveThread(self)
            self._keepalive_thread.start()

    def stop_keepalive(self) -> None:
        """
        Stops the thread which calls the keepalive.
        """
        if hasattr(self, "_keepalive_thread"):
            if self._keepalive_thread.is_alive():
                self._keepalive_thread.stop()
                self._keepalive_thread.join()
            del self._keepalive_thread

    def clear_memory(self) -> None:
        """
        Clears cached data
        """
        if self.device.type == "cuda":
            import torch
            import torch.cuda
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
        elif self.device.type == "mps":
            import torch
            import torch.mps
            torch.mps.empty_cache()
            torch.mps.synchronize()
        gc.collect()

    @classmethod
    def is_loadable_model_file(cls, path: str) -> bool:
        """
        Returns if the path is a known format for loadable models.
        """
        _, ext = os.path.splitext(path)
        return ext in cls.LOADABLE_EXTENSIONS

    # Overall properties

    @property
    def offline(self) -> bool:
        """
        True if this should be running in offline (local files only) mode.
        """
        return getattr(self, "_offline", self.configuration.get("enfugue.offline", False))

    @offline.setter
    def offline(self, new_offline: bool) -> None:
        """
        Enables/disables offline mode.
        """
        self._offline = new_offline

    @property
    def safe(self) -> bool:
        """
        Returns true if safety checking should be enabled.
        """
        if not hasattr(self, "_safe"):
            self._safe = self.configuration.get("enfugue.safe", True)
        return self._safe

    @safe.setter
    def safe(self, val: bool) -> None:
        """
        Sets a new value for safety checking. Destroys the pipeline.
        """
        if val != getattr(self, "_safe", None):
            self._safe = val
            if hasattr(self, "_pipeline"):
                if self._pipeline.safety_checker is None and val:
                    self.unload_pipeline("safety checking enabled")
                else:
                    self._pipeline.safety_checking_disabled = not val
            if hasattr(self, "_inpainter_pipeline"):
                if self._inpainter_pipeline.safety_checker is None and val:
                    self.unload_inpainter("safety checking enabled")
                else:
                    self._inpainter_pipeline.safety_checking_disabled = not val
            if hasattr(self, "_animator_pipeline"):
                if self._animator_pipeline.safety_checker is None and val:
                    self.unload_animator("safety checking enabled")
                else:
                    self._animator_pipeline.safety_checking_disabled = not val

    @property
    def device(self) -> torch.device:
        """
        Gets the device that will be executed on
        """
        if not hasattr(self, "_device"):
            from enfugue.diffusion.util import get_optimal_device

            self._device = get_optimal_device(self.configuration.get("enfugue.gpu.index", None))
        return self._device

    @device.setter
    def device(self, new_device: Optional[DEVICE_LITERAL]) -> None:
        """
        Changes the device.
        """
        if new_device is None:
            from enfugue.diffusion.util import get_optimal_device

            device = get_optimal_device()
        elif new_device == "dml":
            import torch_directml

            device = torch_directml.device()
        else:
            import torch

            device = torch.device(new_device)
        self._device = device

    @property
    def seed(self) -> int:
        """
        Gets the seed. If there is None, creates a random one once.
        """
        if not hasattr(self, "_seed"):
            self._seed = self.configuration.get("enfugue.seed", random.randint(0, 2**32-1))
        return self._seed

    @seed.setter
    def seed(self, new_seed: int) -> None:
        """
        Re-seeds the pipeline. This deletes the generator so it gets re-initialized.
        """
        self._seed = new_seed
        del self.generator
        del self.noise_generator

    @property
    def keepalive_callback(self) -> Callable[[], None]:
        """
        A callback function to call during long operations.
        """
        if not hasattr(self, "_keepalive_callback"):
            return lambda: None
        return self._keepalive_callback

    @keepalive_callback.setter
    def keepalive_callback(self, new_callback: Callable[[], None]) -> None:
        """
        Sets the callback
        """
        if hasattr(self, "_keepalive_callback") and self._keepalive_callback is not new_callback:
            logger.debug(f"Setting keepalive callback to {new_callback}")
        self._keepalive_callback = new_callback

    @keepalive_callback.deleter
    def keepalive_callback(self) -> None:
        """
        Removes the callback.
        """
        if hasattr(self, "_keepalive_callback"):
            del self._keepalive_callback

    @property
    def generator(self) -> torch.Generator:
        """
        Creates the generator once, otherwise returns it.
        """
        if not hasattr(self, "_generator"):
            try:
                self._generator = torch.Generator(device=self.device)
            except RuntimeError:
                # Unsupported device, go to CPU
                self._generator = torch.Generator()
            self._generator.manual_seed(self.seed)
        return self._generator

    @generator.deleter
    def generator(self) -> None:
        """
        Removes an existing generator.
        """
        if hasattr(self, "_generator"):
            delattr(self, "_generator")

    @property
    def noise_generator(self) -> torch.Generator:
        """
        Creates the noise generator once, otherwise returns it.
        This is kept on the CPU as it creates better noise.
        """
        if not hasattr(self, "_noise_generator"):
            self._noise_generator = torch.Generator()
            self._noise_generator.manual_seed(self.seed)
        return self._noise_generator

    @noise_generator.deleter
    def noise_generator(self) -> None:
        """
        Removes an existing noise generator.
        """
        if hasattr(self, "_noise_generator"):
            delattr(self, "_noise_generator")

    # Diffusion properties

    @property
    def scheduler_config(self) -> Dict[str, Any]:
        """
        Gets the kwargs for the scheduler class.
        """
        return getattr(self, "_scheduler_config", {})

    @scheduler_config.setter
    def scheduler_config(self, scheduler_config: Dict[str, Any]) -> None:
        """
        Gets the kwargs for the scheduler class.
        """
        self._scheduler_config = scheduler_config

    @property
    def static_scheduler_config(self) -> Dict[str, Any]:
        """
        Gets the static kwargs for the scheduler class.
        """
        return getattr(self, "_static_scheduler_config", {})

    @static_scheduler_config.setter
    def static_scheduler_config(self, scheduler_config: Dict[str, Any]) -> None:
        """
        Gets the kwargs for the scheduler class.
        """
        self._static_scheduler_config = scheduler_config

    @property
    def scheduler(self) -> Optional[KarrasDiffusionSchedulers]:
        """
        Gets the scheduler class to instantiate.
        """
        return getattr(self, "_scheduler", None)

    @scheduler.setter
    def scheduler(
        self,
        new_scheduler: Optional[SCHEDULER_LITERAL],
    ) -> None:
        """
        Sets the scheduler class
        """
        if not new_scheduler:
            if hasattr(self, "_scheduler"):
                delattr(self, "_scheduler")
                if hasattr(self, "_pipeline"):
                    logger.debug("Reverting pipeline scheduler to default.")
                    self._pipeline.revert_scheduler()
                if hasattr(self, "_inpainter_pipeline"):
                    logger.debug("Reverting inpainter pipeline scheduler to default.")
                    self._inpainter_pipeline.revert_scheduler()
                if hasattr(self, "_refiner_pipeline"):
                    logger.debug("Reverting refiner pipeline scheduler to default.")
                    self._refiner_pipeline.revert_scheduler()
                if hasattr(self, "_animator_pipeline"):
                    logger.debug("Reverting animator pipeline scheduler to default.")
                    self._animator_pipeline.revert_scheduler()
            return

        scheduler_class = self.get_scheduler_class(new_scheduler)
        scheduler_config: Dict[str, Any] = {}

        if isinstance(scheduler_class, tuple):
            scheduler_class, scheduler_config = scheduler_class

        logger.debug(f"Changing to scheduler {scheduler_class.__name__} ({new_scheduler})") # type: ignore[union-attr]
        self._scheduler = scheduler_class # type: ignore[assignment]
        self._static_scheduler_config = scheduler_config

        if hasattr(self, "_pipeline"):
            logger.debug(f"Hot-swapping pipeline scheduler.")
            self._pipeline.scheduler = self.scheduler.from_config({ # type: ignore
                **self._pipeline.scheduler_config,
                **self.scheduler_config,
                **self.static_scheduler_config
            })
        if hasattr(self, "_inpainter_pipeline"):
            logger.debug(f"Hot-swapping inpainter pipeline scheduler.")
            self._inpainter_pipeline.scheduler = self.scheduler.from_config({ # type: ignore
                **self._inpainter_pipeline.scheduler_config,
                **self.scheduler_config,
                **self.static_scheduler_config
            })
        if hasattr(self, "_refiner_pipeline"):
            logger.debug(f"Hot-swapping refiner pipeline scheduler.")
            self._refiner_pipeline.scheduler = self.scheduler.from_config({ # type: ignore
                **self._refiner_pipeline.scheduler_config,
                **self.scheduler_config,
                **self.static_scheduler_config
            })
        if hasattr(self, "_animator_pipeline"):
            logger.debug(f"Hot-swapping animator pipeline scheduler.")
            self._animator_pipeline.scheduler = self.scheduler.from_config({ # type: ignore
                **self._animator_pipeline.scheduler_config,
                **self.scheduler_config,
                **self.static_scheduler_config
            })

    @property
    def vae(self) -> Optional[Union[AutoencoderKL, ConsistencyDecoderVAE]]:
        """
        Gets the configured VAE (or None.)
        """
        if not hasattr(self, "_vae"):
            self._vae = self.get_vae(self.vae_name)
        return self._vae

    @vae.setter
    def vae(
        self,
        new_vae: Optional[str],
    ) -> None:
        """
        Sets a new vae.
        """
        existing_vae = getattr(self, "_vae", None)

        if (
            (not existing_vae and new_vae)
            or (existing_vae and not new_vae)
            or (existing_vae and new_vae and self.vae_name != new_vae)
        ):
            if not new_vae:
                self._vae_name = None  # type: ignore
                self._vae = None
                self.unload_pipeline("VAE resetting to default")
            else:
                vae_path = self.check_download_model(self.engine_vae_dir, new_vae)

                self._vae_name = os.path.basename(vae_path)
                self._vae = self.get_vae(vae_path)

                if self.tensorrt_is_ready and "vae" in self.TENSORRT_STAGES:
                    self.unload_pipeline("VAE changing")
                elif hasattr(self, "_pipeline"):
                    logger.debug(f"Hot-swapping pipeline VAE to {new_vae}")
                    self._pipeline.vae = self._vae # type: ignore[assignment]
                    if self.is_sdxl:
                        self._pipeline.register_to_config( # type: ignore[attr-defined]
                            force_full_precision_vae = "xl" in new_vae and "16" not in new_vae
                        )

    @property
    def vae_name(self) -> Optional[str]:
        """
        Gets the name of the VAE, if one was set.
        """
        if not hasattr(self, "_vae_name"):
            self._vae_name = self.configuration.get("enfugue.vae.base", None)
        return self._vae_name
    
    @property
    def refiner_vae(self) -> Optional[Union[AutoencoderKL, ConsistencyDecoderVAE]]:
        """
        Gets the configured refiner VAE (or None.)
        """
        if not hasattr(self, "_refiner_vae"):
            self._refiner_vae = self.get_vae(self.refiner_vae_name)
        return self._refiner_vae

    @refiner_vae.setter
    def refiner_vae(
        self,
        new_vae: Optional[str],
    ) -> None:
        """
        Sets a new refiner vae.
        """
        existing_vae = getattr(self, "_refiner_vae", None)

        if (
            (not existing_vae and new_vae)
            or (existing_vae and not new_vae)
            or (existing_vae and new_vae and self.refiner_vae_name != new_vae)
        ):
            if not new_vae:
                self._refiner_vae_name = None  # type: ignore
                self._refiner_vae = None
                self.unload_refiner("VAE resetting to default")
            else:
                vae_path = self.check_download_model(self.engine_vae_dir, new_vae)
                self._refiner_vae_name = new_vae
                self._refiner_vae = self.get_vae(vae_path)
                if self.refiner_tensorrt_is_ready and "vae" in self.TENSORRT_STAGES:
                    self.unload_refiner("VAE changing")
                elif hasattr(self, "_refiner_pipeline"):
                    logger.debug(f"Hot-swapping refiner pipeline VAE to {new_vae}")
                    self._refiner_pipeline.vae = self._refiner_vae # type: ignore[assignment]
                    if self.refiner_is_sdxl:
                        self._refiner_pipeline.register_to_config( # type: ignore[attr-defined]
                            force_full_precision_vae = "xl" in new_vae and "16" not in new_vae
                        )

    @property
    def refiner_vae_name(self) -> Optional[str]:
        """
        Gets the name of the VAE, if one was set.
        """
        if not hasattr(self, "_refiner_vae_name"):
            self._refiner_vae_name = self.configuration.get("enfugue.vae.refiner", None)
        return self._refiner_vae_name
    
    @property
    def inpainter_vae(self) -> Optional[Union[AutoencoderKL, ConsistencyDecoderVAE]]:
        """
        Gets the configured inpainter VAE (or None.)
        """
        if not hasattr(self, "_inpainter_vae"):
            self._inpainter_vae = self.get_vae(self.inpainter_vae_name)
        return self._inpainter_vae

    @inpainter_vae.setter
    def inpainter_vae(
        self,
        new_vae: Optional[str],
    ) -> None:
        """
        Sets a new inpainter vae.
        """
        existing_vae = getattr(self, "_inpainter_vae", None)

        if (
            (not existing_vae and new_vae)
            or (existing_vae and not new_vae)
            or (existing_vae and new_vae and self.inpainter_vae_name != new_vae)
        ):
            if not new_vae:
                self._inpainter_vae_name = None  # type: ignore
                self._inpainter_vae = None
                self.unload_inpainter("VAE resetting to default")
            else:
                vae_path = self.check_download_model(self.engine_vae_dir, new_vae)
                self._inpainter_vae_name = new_vae
                self._inpainter_vae = self.get_vae(vae_path)
                if self.inpainter_tensorrt_is_ready and "vae" in self.TENSORRT_STAGES:
                    self.unload_inpainter("VAE changing")
                elif hasattr(self, "_inpainter_pipeline"):
                    logger.debug(f"Hot-swapping inpainter pipeline VAE to {new_vae}")
                    self._inpainter_pipeline.vae = self._inpainter_vae # type: ignore[assignment]
                    if self.inpainter_is_sdxl:
                        self._inpainter_pipeline.register_to_config( # type: ignore[attr-defined]
                            force_full_precision_vae = "xl" in new_vae and "16" not in new_vae
                        )

    @property
    def inpainter_vae_name(self) -> Optional[str]:
        """
        Gets the name of the VAE, if one was set.
        """
        if not hasattr(self, "_inpainter_vae_name"):
            self._inpainter_vae_name = self.configuration.get("enfugue.vae.inpainter", None)
        return self._inpainter_vae_name

    @property
    def animator_vae(self) -> Optional[Union[AutoencoderKL, ConsistencyDecoderVAE]]:
        """
        Gets the configured animator VAE (or None.)
        """
        if not hasattr(self, "_animator_vae"):
            self._animator_vae = self.get_vae(self.animator_vae_name)
        return self._animator_vae

    @animator_vae.setter
    def animator_vae(
        self,
        new_vae: Optional[str],
    ) -> None:
        """
        Sets a new animator vae.
        """
        existing_vae = getattr(self, "_animator_vae", None)

        if (
            (not existing_vae and new_vae)
            or (existing_vae and not new_vae)
            or (existing_vae and new_vae and self.animator_vae_name != new_vae)
        ):
            if not new_vae:
                self._animator_vae_name = None  # type: ignore
                self._animator_vae = None
                self.unload_animator("VAE resetting to default")
            else:
                vae_path = self.check_download_model(self.engine_vae_dir, new_vae)
                self._animator_vae_name = new_vae
                self._animator_vae = self.get_vae(vae_path)
                if self.animator_tensorrt_is_ready and "vae" in self.TENSORRT_STAGES:
                    self.unload_animator("VAE changing")
                elif hasattr(self, "_animator_pipeline"):
                    logger.debug(f"Hot-swapping animator pipeline VAE to {new_vae}")
                    self._animator_pipeline.vae = self._animator_vae # type: ignore [assignment]
                    if self.animator_is_sdxl:
                        self._animator_pipeline.register_to_config( # type: ignore[attr-defined]
                            force_full_precision_vae = "xl" in new_vae and "16" not in new_vae
                        )

    @property
    def animator_vae_name(self) -> Optional[str]:
        """
        Gets the name of the VAE, if one was set.
        """
        if not hasattr(self, "_animator_vae_name"):
            self._animator_vae_name = self.configuration.get("enfugue.vae.animator", None)
        return self._animator_vae_name

    @property
    def size(self) -> int:
        """
        Gets the trained size of the model
        """
        if not hasattr(self, "_size"):
            return 1024 if self.is_sdxl else 512
        return self._size

    @property
    def refiner_size(self) -> int:
        """
        Gets the trained size of the refiner
        """
        if not hasattr(self, "_refiner_size"):
            return 1024 if self.refiner_is_sdxl else 512
        return self._refiner_size

    @property
    def inpainter_size(self) -> int:
        """
        Gets the trained size of the inpainter
        """
        if not hasattr(self, "_inpainter_size"):
            if self.inpainter:
                return 1024 if self.inpainter_is_sdxl else 512
            return self.size
        return self._inpainter_size

    @property
    def animator_size(self) -> int:
        """
        Gets the trained size of the animator
        """
        if not hasattr(self, "_animator_size"):
            if self.animator:
                return 1024 if self.animator_is_sdxl else 512
            return self.size
        return self._animator_size

    @property
    def tiling_size(self) -> Optional[int]:
        """
        Gets the tiling size in pixels.
        """
        if not hasattr(self, "_tiling_size"):
            self._tiling_size = self.configuration.get("enfugue.tile.size", None)
        return self._tiling_size

    @tiling_size.setter
    def tiling_size(self, new_tiling_size: Optional[int]) -> None:
        """
        Sets the new tiling size. This will require a restart if pipelines are loaded and using tensorrt.
        """
        if (
            (self.tiling_size is None and new_tiling_size is not None) or
            (self.tiling_size is not None and new_tiling_size is None) or
            (self.tiling_size is not None and new_tiling_size is not None and self.tiling_size != new_tiling_size)
        ):
            if hasattr(self, "_pipeline") and self.tensorrt_is_ready:
                self.unload_pipeline("engine tiling size changing")
            if hasattr(self, "_inpainter_pipeline") and self.inpainter_tensorrt_is_ready:
                self.unload_inpainter("engine tiling size changing")
            if hasattr(self, "_refiner_pipeline") and self.refiner_tensorrt_is_ready:
                self.unload_refiner("engine tiling size changing")
            if hasattr(self, "_animator_pipeline") and self.animator_tensorrt_is_ready:
                self.unload_animator("engine tiling size changing")

    @property
    def tiling_stride(self) -> int:
        """
        Gets the chunking size in pixels.
        """
        if not hasattr(self, "_tiling_stride"):
            self._tiling_stride = int(
                self.configuration.get("enfugue.tile.stride", self.size // 4)
            )
        return self._tiling_stride

    @tiling_stride.setter
    def tiling_stride(self, new_tiling_stride: int) -> None:
        """
        Sets the new tiling stride. This doesn't require a restart.
        """
        self._tiling_stride = new_tiling_stride

    @property
    def tensorrt_size(self) -> int:
        """
        Gets the size of an active tensorrt engine.
        """
        if self.tiling_size is not None:
            return self.tiling_size
        return self.size

    @property
    def inpainter_tensorrt_size(self) -> int:
        """
        Gets the size of an active inpainter tensorrt engine.
        """
        if self.tiling_size is not None:
            return self.tiling_size
        return self.inpainter_size

    @property
    def refiner_tensorrt_size(self) -> int:
        """
        Gets the size of an active refiner tensorrt engine.
        """
        if self.tiling_size is not None:
            return self.tiling_size
        return self.refiner_size

    @property
    def animator_tensorrt_size(self) -> int:
        """
        Gets the size of an active animator tensorrt engine.
        """
        if self.tiling_size is not None:
            return self.tiling_size
        return self.animator_size

    @property
    def frame_window_size(self) -> int:
        """
        Gets the animator frame window engine size in frames when chunking (default always.)
        """
        if not hasattr(self, "_frame_window_size"):
            self._frame_window_size = self.configuration.get("enfugue.frames", DiffusionPipelineManager.DEFAULT_TEMPORAL_SIZE)
        return self._frame_window_size

    @frame_window_size.setter
    def frame_window_size(self, new_frame_window_size: Optional[int]) -> None:
        """
        Sets the animator engine size in pixels.
        """
        if new_frame_window_size is None:
            if hasattr(self, "_frame_window_size"):
                if self._frame_window_size != self.frame_window_size and self.tensorrt_is_ready:
                    self.unload_animator("engine frame window size changing")
                elif hasattr(self, "_animator_pipeline"):
                    logger.debug("Setting animator engine size in-place.")
                    self._animator_pipeline.frame_window_size = new_frame_window_size # type: ignore[assignment]
                delattr(self, "_frame_window_size")
        elif hasattr(self, "_frame_window_size") and self._frame_window_size != new_frame_window_size:
            if self.tensorrt_is_ready:
                self.unload_animator("engine size changing")
            elif hasattr(self, "_animator_pipeline"):
                logger.debug("Setting animator frame window engine size in-place.")
                self._animator_pipeline.frame_window_size = new_frame_window_size
        if new_frame_window_size is not None:
            self._frame_window_size = new_frame_window_size

    @property
    def frame_window_stride(self) -> Optional[int]:
        """
        Gets the chunking size in pixels.
        """
        if not hasattr(self, "_frame_window_stride"):
            self._frame_window_stride = int(
                self.configuration.get("enfugue.temporal.size", DiffusionPipelineManager.DEFAULT_TEMPORAL_CHUNK)
            )
        return self._frame_window_stride

    @frame_window_stride.setter
    def frame_window_stride(self, new_frame_window_stride: Optional[int]) -> None:
        """
        Sets the new chunking size. This doesn't require a restart.
        """
        self._frame_window_stride = new_frame_window_stride # type: ignore[assignment]
        if hasattr(self, "_animator_pipeline"):
            self._animator_pipeline.frame_window_stride = new_frame_window_stride # type: ignore[assignment]

    @property
    def engine_root(self) -> str:
        """
        Gets the root of the engine.
        """
        path = self.configuration.get("enfugue.engine.root", "~/.cache/enfugue")
        if path.startswith("~"):
            path = os.path.expanduser(path)
        path = os.path.realpath(path)
        check_make_directory(path)
        return path

    @property
    def engine_cache_dir(self) -> str:
        """
        Gets the cache for diffusers-downloaded configuration files, base models, etc.
        """
        path = self.configuration.get("enfugue.engine.cache", None)
        if path is not None:
            if path.startswith("~"):
                path = os.path.expanduser(path)
            path = os.path.realpath(path)
            check_make_directory(path)
            return path
        else:
            return check_make_directory_by_names(self.engine_root, "cache")

    @property
    def engine_checkpoints_dir(self) -> str:
        """
        Gets where checkpoints are downloaded in.
        """
        path = self.configuration.get("enfugue.engine.checkpoint", None)
        if path is not None:
            if path.startswith("~"):
                path = os.path.expanduser(path)
            path = os.path.realpath(path)
            check_make_directory(path)
            return path
        else:
            return check_make_directory_by_names(self.engine_root, "checkpoint", "Stable-diffusion")

    @property
    def engine_other_dir(self) -> str:
        """
        Gets where any other weights are download in
        """
        path = self.configuration.get("enfugue.engine.other", None)
        if path is not None:
            if path.startswith("~"):
                path = os.path.expanduser(path)
            path = os.path.realpath(path)
            check_make_directory(path)
            return path
        else:
            return check_make_directory_by_names(self.engine_root, "other")

    @property
    def engine_lora_dir(self) -> str:
        """
        Gets where lora are downloaded in.
        """
        path = self.configuration.get("enfugue.engine.lora", None)
        if path is not None:
            if path.startswith("~"):
                path = os.path.expanduser(path)
            path = os.path.realpath(path)
            check_make_directory(path)
            return path
        else:
            return check_make_directory_by_names(self.engine_root, "lora")

    @property
    def engine_lycoris_dir(self) -> str:
        """
        Gets where lycoris are downloaded in.
        """
        path = self.configuration.get("enfugue.engine.lycoris", None)
        if path is not None:
            if path.startswith("~"):
                path = os.path.expanduser(path)
            path = os.path.realpath(path)
            check_make_directory(path)
            return path
        else:
            return check_make_directory_by_names(self.engine_root, "lycoris", "locon")

    @property
    def engine_inversion_dir(self) -> str:
        """
        Gets where inversion are downloaded to.
        """
        path = self.configuration.get("enfugue.engine.inversion", None)
        if path is not None:
            if path.startswith("~"):
                path = os.path.expanduser(path)
            path = os.path.realpath(path)
            check_make_directory(path)
            return path
        else:
            return check_make_directory_by_names(self.engine_root, "inversion", "embedding", "ti")

    @property
    def engine_tensorrt_dir(self) -> str:
        """
        Gets where TensorRT engines are built.
        """
        path = self.configuration.get("enfugue.engine.tensorrt", None)
        if path is not None:
            if path.startswith("~"):
                path = os.path.expanduser(path)
            path = os.path.realpath(path)
            check_make_directory(path)
            return path
        else:
            return check_make_directory_by_names(self.engine_root, "tensorrt", "tensor_rt")

    @property
    def engine_motion_dir(self) -> str:
        """
        Gets where motion modules are saved.
        """
        path = self.configuration.get("enfugue.engine.motion", None)
        if path is not None:
            if path.startswith("~"):
                path = os.path.expanduser(path)
            path = os.path.realpath(path)
            check_make_directory(path)
            return path
        else:
            return check_make_directory_by_names(self.engine_root, "motion", "motion_module")

    @property
    def engine_controlnet_dir(self) -> str:
        """
        Gets where controlnet models are saved.
        """
        path = self.configuration.get("enfugue.engine.controlnet", None)
        if path is not None:
            if path.startswith("~"):
                path = os.path.expanduser(path)
            path = os.path.realpath(path)
            check_make_directory(path)
            return path
        else:
            return check_make_directory_by_names(self.engine_root, "controlnet", "control_net")

    @property
    def engine_vae_dir(self) -> str:
        """
        Gets where vae models are saved.
        """
        path = self.configuration.get("enfugue.engine.vae", None)
        if path is not None:
            if path.startswith("~"):
                path = os.path.expanduser(path)
            path = os.path.realpath(path)
            check_make_directory(path)
            return path
        else:
            return check_make_directory_by_names(self.engine_root, "vae")

    @property
    def engine_vae_approx_dir(self) -> str:
        """
        Gets where approximate vae models are saved.
        """
        path = self.configuration.get("enfugue.engine.vae_approx", None)
        if path is not None:
            if path.startswith("~"):
                path = os.path.expanduser(path)
            path = os.path.realpath(path)
            check_make_directory(path)
            return path
        else:
            return check_make_directory_by_names(self.engine_root, "vae_approx", "vae_taesd")

    @property
    def engine_clip_dir(self) -> str:
        """
        Gets where clip models are saved.
        """
        path = self.configuration.get("enfugue.engine.clip", None)
        if path is not None:
            if path.startswith("~"):
                path = os.path.expanduser(path)
            path = os.path.realpath(path)
            check_make_directory(path)
            return path
        else:
            return check_make_directory_by_names(self.engine_root, "clip")

    @property
    def engine_clip_vision_dir(self) -> str:
        """
        Gets where clip vision models are saved.
        """
        path = self.configuration.get("enfugue.engine.clip_vision", None)
        if path is not None:
            if path.startswith("~"):
                path = os.path.expanduser(path)
            path = os.path.realpath(path)
            check_make_directory(path)
            return path
        else:
            return check_make_directory_by_names(self.engine_root, "clip_vision")

    @property
    def engine_ip_adapter_dir(self) -> str:
        """
        Gets where IP adapter models are saved.
        """
        path = self.configuration.get("enfugue.engine.ip_adapter", None)
        if path is not None:
            if path.startswith("~"):
                path = os.path.expanduser(path)
            path = os.path.realpath(path)
            check_make_directory(path)
            return path
        else:
            return check_make_directory_by_names(self.engine_root, "ip_adapter")

    @property
    def engine_upscale_dir(self) -> str:
        """
        Gets where IP adapter models are saved.
        """
        path = self.configuration.get("enfugue.engine.upscale", None)
        if path is not None:
            if path.startswith("~"):
                path = os.path.expanduser(path)
            path = os.path.realpath(path)
            check_make_directory(path)
            return path
        else:
            return check_make_directory_by_names(self.engine_root, "upscale", "upscale_models")

    @property
    def engine_language_dir(self) -> str:
        """
        Gets where language modules are saved.
        """
        path = self.configuration.get("enfugue.engine.language", None)
        if path is not None:
            if path.startswith("~"):
                path = os.path.expanduser(path)
            path = os.path.realpath(path)
            check_make_directory(path)
            return path
        else:
            return check_make_directory_by_names(self.engine_root, "language")

    @property
    def engine_detection_dir(self) -> str:
        """
        Gets where detection modules are saved.
        """
        path = self.configuration.get("enfugue.engine.detection", None)
        if path is not None:
            if path.startswith("~"):
                path = os.path.expanduser(path)
            path = os.path.realpath(path)
            check_make_directory(path)
            return path
        else:
            return check_make_directory_by_names(self.engine_root, "detection", "mmdet")

    @property
    def engine_interpolation_dir(self) -> str:
        """
        Gets where interpolation modules are saved.
        """
        path = self.configuration.get("enfugue.engine.interpolation", None)
        if path is not None:
            if path.startswith("~"):
                path = os.path.expanduser(path)
            path = os.path.realpath(path)
            check_make_directory(path)
            return path
        else:
            return check_make_directory_by_names(self.engine_root, "interpolation")

    @property
    def model_tensorrt_dir(self) -> str:
        """
        Gets where tensorrt engines will be built per model.
        """
        path = os.path.join(self.engine_tensorrt_dir, self.model_name)
        check_make_directory(path)
        return path

    @property
    def refiner_tensorrt_dir(self) -> str:
        """
        Gets where tensorrt engines will be built per refiner.
        """
        if not self.refiner_name:
            raise ValueError("No refiner set")
        path = os.path.join(self.engine_tensorrt_dir, self.refiner_name)
        check_make_directory(path)
        return path

    @property
    def inpainter_tensorrt_dir(self) -> str:
        """
        Gets where tensorrt engines will be built per inpainter.
        """
        if not self.inpainter_name:
            raise ValueError("No inpainter set")
        path = os.path.join(self.engine_tensorrt_dir, self.inpainter_name)
        check_make_directory(path)
        return path

    @property
    def animator_tensorrt_dir(self) -> str:
        """
        Gets where tensorrt engines will be built per animator.
        """
        if not self.animator_name:
            raise ValueError("No animator set")
        path = os.path.join(self.engine_tensorrt_dir, self.animator_name)
        check_make_directory(path)
        return path

    @property
    def engine_diffusers_dir(self) -> str:
        """
        Gets where diffusers caches are saved.
        """
        path = self.configuration.get("enfugue.engine.diffusers", "~/.cache/enfugue/diffusers")
        if path.startswith("~"):
            path = os.path.expanduser(path)
        path = os.path.realpath(path)
        check_make_directory(path)
        return path

    @property
    def model_diffusers_dir(self) -> str:
        """
        Gets where the diffusers cache will be for the current model.
        """
        path = os.path.join(self.engine_diffusers_dir, self.model_name)
        check_make_directory(path)
        return path

    @property
    def refiner_diffusers_dir(self) -> str:
        """
        Gets where the diffusers cache will be for the current refiner.
        """
        if not self.refiner_name:
            raise ValueError("No refiner set")
        path = os.path.join(self.engine_diffusers_dir, self.refiner_name)
        check_make_directory(path)
        return path

    @property
    def inpainter_diffusers_dir(self) -> str:
        """
        Gets where the diffusers cache will be for the current inpainter.
        """
        if not self.inpainter_name:
            raise ValueError("No inpainter set")
        path = os.path.join(self.engine_diffusers_dir, self.inpainter_name)
        check_make_directory(path)
        return path

    @property
    def animator_diffusers_dir(self) -> str:
        """
        Gets where the diffusers cache will be for the current animator.
        """
        if not self.animator_name:
            raise ValueError("No animator set")
        path = os.path.join(self.engine_diffusers_dir, f"{self.animator_name}-animator")
        check_make_directory(path)
        return path

    @property
    def engine_onnx_dir(self) -> str:
        """
        Gets where ONNX models are built (when using DirectML)
        """
        path = self.configuration.get("enfugue.engine.onnx", "~/.cache/enfugue/onnx")
        if path.startswith("~"):
            path = os.path.expanduser(path)
        path = os.path.realpath(path)
        check_make_directory(path)
        return path

    @property
    def model_onnx_dir(self) -> str:
        """
        Gets where the onnx cache will be for the current model.
        """
        path = os.path.join(self.engine_onnx_dir, self.model_name)
        check_make_directory(path)
        return path

    @property
    def refiner_onnx_dir(self) -> str:
        """
        Gets where the onnx cache will be for the current refiner.
        """
        if not self.refiner_name:
            raise ValueError("No refiner set")
        path = os.path.join(self.engine_onnx_dir, self.refiner_name)
        check_make_directory(path)
        return path

    @property
    def inpainter_onnx_dir(self) -> str:
        """
        Gets where the onnx cache will be for the current inpainter.
        """
        if not self.inpainter_name:
            raise ValueError("No inpainter set")
        path = os.path.join(self.engine_onnx_dir, self.inpainter_name)
        check_make_directory(path)
        return path

    @property
    def animator_onnx_dir(self) -> str:
        """
        Gets where the onnx cache will be for the current animator.
        """
        if not self.animator_name:
            raise ValueError("No animator set")
        path = os.path.join(self.engine_onnx_dir, self.animator_name)
        check_make_directory(path)
        return path

    @staticmethod
    def get_clip_key(
        size: int, lora: List[Tuple[str, float]], lycoris: List[Tuple[str, float]], inversion: List[str], **kwargs: Any
    ) -> str:
        """
        Uses hashlib to generate the unique key for the CLIP engine.
        CLIP must be rebuilt for each:
            1. Model
            2. Dimension
            3. LoRA
            4. LyCORIS
            5. Textual Inversion
        """
        return md5(
            "-".join(
                [
                    str(size),
                    ":".join(
                        "=".join([str(part) for part in lora_weight])
                        for lora_weight in sorted(lora, key=lambda lora_part: lora_part[0])
                    ),
                    ":".join(
                        "=".join([str(part) for part in lycoris_weight])
                        for lycoris_weight in sorted(lycoris, key=lambda lycoris_part: lycoris_part[0])
                    ),
                    ":".join(sorted(inversion)),
                ]
            ).encode("utf-8")
        ).hexdigest()

    @property
    def model_clip_key(self) -> str:
        """
        Gets the CLIP key for the current configuration.
        """
        return DiffusionPipelineManager.get_clip_key(
            size=self.size,
            lora=self.lora_names_weights,
            lycoris=self.lycoris_names_weights,
            inversion=self.inversion_names,
        )

    @property
    def model_tensorrt_clip_dir(self) -> str:
        """
        Gets where the tensorrt CLIP engine will be stored.
        """
        path = os.path.join(self.model_tensorrt_dir, "clip", self.model_clip_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def model_onnx_clip_dir(self) -> str:
        """
        Gets where the onnx CLIP engine will be stored.
        """
        path = os.path.join(self.model_onnx_dir, "clip", self.model_clip_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def refiner_clip_key(self) -> str:
        """
        Gets the CLIP key for the current configuration.
        """
        return DiffusionPipelineManager.get_clip_key(
            size=self.refiner_size,
            lora=[],
            lycoris=[],
            inversion=[]
        )

    @property
    def refiner_tensorrt_clip_dir(self) -> str:
        """
        Gets where the tensorrt CLIP engine will be stored.
        """
        path = os.path.join(self.refiner_tensorrt_dir, "clip", self.refiner_clip_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def refiner_onnx_clip_dir(self) -> str:
        """
        Gets where the onnx CLIP engine will be stored.
        """
        path = os.path.join(self.refiner_onnx_dir, "clip", self.refiner_clip_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def inpainter_clip_key(self) -> str:
        """
        Gets the CLIP key for the current configuration.
        """
        return DiffusionPipelineManager.get_clip_key(
            size=self.inpainter_size,
            lora=[],
            lycoris=[],
            inversion=[]
        )

    @property
    def inpainter_tensorrt_clip_dir(self) -> str:
        """
        Gets where the tensorrt CLIP engine will be stored.
        """
        path = os.path.join(self.inpainter_tensorrt_dir, "clip", self.inpainter_clip_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def inpainter_onnx_clip_dir(self) -> str:
        """
        Gets where the onnx CLIP engine will be stored.
        """
        path = os.path.join(self.inpainter_onnx_dir, "clip", self.inpainter_clip_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def animator_clip_key(self) -> str:
        """
        Gets the CLIP key for the current configuration.
        """
        return DiffusionPipelineManager.get_clip_key(
            size=self.animator_size,
            lora=[],
            lycoris=[],
            inversion=[]
        )

    @property
    def animator_tensorrt_clip_dir(self) -> str:
        """
        Gets where the tensorrt CLIP engine will be stored.
        """
        path = os.path.join(self.animator_tensorrt_dir, "clip", self.animator_clip_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def animator_onnx_clip_dir(self) -> str:
        """
        Gets where the onnx CLIP engine will be stored.
        """
        path = os.path.join(self.animator_onnx_dir, "clip", self.animator_clip_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @staticmethod
    def get_unet_key(
        size: int,
        lora: List[Tuple[str, float]],
        lycoris: List[Tuple[str, float]],
        inversion: List[str],
        **kwargs: Any,
    ) -> str:
        """
        Uses hashlib to generate the unique key for the UNET engine.
        UNET must be rebuilt for each:
            1. Model
            2. Dimension
            3. LoRA
            4. LyCORIS
            5. Textual Inversion
        """
        return md5(
            "-".join(
                [
                    str(size),
                    ":".join(
                        "=".join([str(part) for part in lora_weight])
                        for lora_weight in sorted(lora, key=lambda lora_part: lora_part[0])
                    ),
                    ":".join(
                        "=".join([str(part) for part in lycoris_weight])
                        for lycoris_weight in sorted(lycoris, key=lambda lycoris_part: lycoris_part[0])
                    ),
                    ":".join(sorted(inversion)),
                ]
            ).encode("utf-8")
        ).hexdigest()

    @property
    def model_unet_key(self) -> str:
        """
        Gets the UNET key for the current configuration.
        """
        return DiffusionPipelineManager.get_unet_key(
            size=self.tensorrt_size,
            lora=self.lora_names_weights,
            lycoris=self.lycoris_names_weights,
            inversion=self.inversion_names,
        )

    @property
    def model_tensorrt_unet_dir(self) -> str:
        """
        Gets where the tensorrt UNET engine will be stored.
        """
        path = os.path.join(self.model_tensorrt_dir, "unet", self.model_unet_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def model_onnx_unet_dir(self) -> str:
        """
        Gets where the onnx UNET engine will be stored.
        """
        path = os.path.join(self.model_onnx_dir, "unet", self.model_unet_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def refiner_unet_key(self) -> str:
        """
        Gets the UNET key for the current configuration.
        """
        return DiffusionPipelineManager.get_unet_key(
            size=self.refiner_tensorrt_size,
            lora=[],
            lycoris=[],
            inversion=[]
        )

    @property
    def refiner_tensorrt_unet_dir(self) -> str:
        """
        Gets where the tensorrt UNET engine will be stored for the refiner.
        """
        path = os.path.join(self.refiner_tensorrt_dir, "unet", self.refiner_unet_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def refiner_onnx_unet_dir(self) -> str:
        """
        Gets where the onnx UNET engine will be stored for the refiner.
        """
        path = os.path.join(self.refiner_onnx_dir, "unet", self.refiner_unet_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def inpainter_unet_key(self) -> str:
        """
        Gets the UNET key for the current configuration.
        """
        return DiffusionPipelineManager.get_unet_key(
            size=self.inpainter_tensorrt_size,
            lora=[],
            lycoris=[],
            inversion=[]
        )

    @property
    def inpainter_tensorrt_unet_dir(self) -> str:
        """
        Gets where the tensorrt UNET engine will be stored for the inpainter.
        """
        path = os.path.join(self.inpainter_tensorrt_dir, "unet", self.inpainter_unet_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def inpainter_onnx_unet_dir(self) -> str:
        """
        Gets where the onnx UNET engine will be stored for the inpainter.
        """
        path = os.path.join(self.inpainter_onnx_dir, "unet", self.inpainter_unet_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def animator_unet_key(self) -> str:
        """
        Gets the UNET key for the current configuration.
        """
        return DiffusionPipelineManager.get_unet_key(
            size=self.animator_tensorrt_size,
            lora=[],
            lycoris=[],
            inversion=[]
        )

    @property
    def animator_tensorrt_unet_dir(self) -> str:
        """
        Gets where the tensorrt UNET engine will be stored for the animator.
        """
        path = os.path.join(self.animator_tensorrt_dir, "unet", self.animator_unet_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def animator_onnx_unet_dir(self) -> str:
        """
        Gets where the onnx UNET engine will be stored for the animator.
        """
        path = os.path.join(self.animator_onnx_dir, "unet", self.animator_unet_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @staticmethod
    def get_controlled_unet_key(
        size: int,
        lora: List[Tuple[str, float]],
        lycoris: List[Tuple[str, float]],
        inversion: List[str],
        **kwargs: Any,
    ) -> str:
        """
        Uses hashlib to generate the unique key for the UNET engine with controlnet blocks.
        ControlledUNET must be rebuilt for each:
            1. Model
            2. Dimension
            3. LoRA
            4. LyCORIS
            5. Textual Inversion
        """
        return md5(
            "-".join(
                [
                    str(size),
                    ":".join(
                        "=".join([str(part) for part in lora_weight])
                        for lora_weight in sorted(lora, key=lambda lora_part: lora_part[0])
                    ),
                    ":".join(
                        "=".join([str(part) for part in lycoris_weight])
                        for lycoris_weight in sorted(lycoris, key=lambda lycoris_part: lycoris_part[0])
                    ),
                    ":".join(sorted(inversion)),
                ]
            ).encode("utf-8")
        ).hexdigest()

    @property
    def model_controlled_unet_key(self) -> str:
        """
        Gets the UNET key for the current configuration.
        """
        return DiffusionPipelineManager.get_controlled_unet_key(
            size=self.size,
            lora=self.lora_names_weights,
            lycoris=self.lycoris_names_weights,
            inversion=self.inversion_names,
        )

    @property
    def model_tensorrt_controlled_unet_dir(self) -> str:
        """
        Gets where the tensorrt Controlled UNet engine will be stored.
        """
        path = os.path.join(self.model_tensorrt_dir, "controlledunet", self.model_controlled_unet_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def model_onnx_controlled_unet_dir(self) -> str:
        """
        Gets where the onnx Controlled UNet engine will be stored.
        """
        path = os.path.join(self.model_onnx_dir, "controlledunet", self.model_controlled_unet_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def refiner_controlled_unet_key(self) -> str:
        """
        Gets the UNET key for the current configuration.
        """
        return DiffusionPipelineManager.get_controlled_unet_key(
            size=self.refiner_size,
            lora=[],
            lycoris=[],
            inversion=[]
        )

    @property
    def refiner_tensorrt_controlled_unet_dir(self) -> str:
        """
        Gets where the tensorrt Controlled UNet engine will be stored for the refiner.
        TODO: determine if this should exist.
        """
        path = os.path.join(self.refiner_tensorrt_dir, "controlledunet", self.refiner_controlled_unet_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def refiner_onnx_controlled_unet_dir(self) -> str:
        """
        Gets where the onnx Controlled UNet engine will be stored for the refiner.
        TODO: determine if this should exist.
        """
        path = os.path.join(self.refiner_onnx_dir, "controlledunet", self.refiner_controlled_unet_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def inpainter_controlled_unet_key(self) -> str:
        """
        Gets the UNET key for the current configuration.
        """
        return DiffusionPipelineManager.get_controlled_unet_key(
            size=self.inpainter_tensorrt_size,
            lora=[],
            lycoris=[],
            inversion=[]
        )

    @property
    def inpainter_tensorrt_controlled_unet_dir(self) -> str:
        """
        Gets where the tensorrt Controlled UNet engine will be stored for the inpainter.
        TODO: determine if this should exist.
        """
        path = os.path.join(self.inpainter_tensorrt_dir, "controlledunet", self.inpainter_controlled_unet_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def inpainter_onnx_controlled_unet_dir(self) -> str:
        """
        Gets where the onnx Controlled UNet engine will be stored for the inpainter.
        TODO: determine if this should exist.
        """
        path = os.path.join(self.inpainter_onnx_dir, "controlledunet", self.inpainter_controlled_unet_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def animator_controlled_unet_key(self) -> str:
        """
        Gets the UNET key for the current configuration.
        """
        return DiffusionPipelineManager.get_controlled_unet_key(
            size=self.animator_tensorrt_size,
            lora=[],
            lycoris=[],
            inversion=[]
        )

    @property
    def animator_tensorrt_controlled_unet_dir(self) -> str:
        """
        Gets where the tensorrt Controlled UNet engine will be stored for the animator.
        TODO: determine if this should exist.
        """
        path = os.path.join(self.animator_tensorrt_dir, "controlledunet", self.animator_controlled_unet_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def animator_onnx_controlled_unet_dir(self) -> str:
        """
        Gets where the onnx Controlled UNet engine will be stored for the animator.
        TODO: determine if this should exist.
        """
        path = os.path.join(self.animator_onnx_dir, "controlledunet", self.animator_controlled_unet_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @staticmethod
    def get_vae_key(size: int, **kwargs: Any) -> str:
        """
        Uses hashlib to generate the unique key for the VAE engine.
        VAE must be rebuilt for each:
            1. Model
            2. Dimension
        """
        return md5(str(size).encode("utf-8")).hexdigest()

    @property
    def model_vae_key(self) -> str:
        """
        Gets the UNET key for the current configuration.
        """
        return DiffusionPipelineManager.get_vae_key(size=self.size)

    @property
    def model_tensorrt_vae_dir(self) -> str:
        """
        Gets where the tensorrt VAE engine will be stored.
        """
        path = os.path.join(self.model_tensorrt_dir, "vae", self.model_vae_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def model_onnx_vae_dir(self) -> str:
        """
        Gets where the onnx VAE engine will be stored.
        """
        path = os.path.join(self.model_onnx_dir, "vae", self.model_vae_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def refiner_vae_key(self) -> str:
        """
        Gets the UNET key for the current configuration.
        """
        return DiffusionPipelineManager.get_vae_key(size=self.refiner_size)

    @property
    def refiner_tensorrt_vae_dir(self) -> str:
        """
        Gets where the tensorrt VAE engine will be stored for the refiner.
        """
        path = os.path.join(self.refiner_tensorrt_dir, "vae", self.refiner_vae_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def refiner_onnx_vae_dir(self) -> str:
        """
        Gets where the onnx VAE engine will be stored for the refiner.
        """
        path = os.path.join(self.refiner_onnx_dir, "vae", self.refiner_vae_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def inpainter_vae_key(self) -> str:
        """
        Gets the UNET key for the current configuration.
        """
        return DiffusionPipelineManager.get_vae_key(size=self.inpainter_size)

    @property
    def inpainter_tensorrt_vae_dir(self) -> str:
        """
        Gets where the tensorrt VAE engine will be stored for the inpainter.
        """
        path = os.path.join(self.inpainter_tensorrt_dir, "vae", self.inpainter_vae_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def inpainter_onnx_vae_dir(self) -> str:
        """
        Gets where the onnx VAE engine will be stored for the inpainter.
        """
        path = os.path.join(self.inpainter_onnx_dir, "vae", self.inpainter_vae_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def animator_vae_key(self) -> str:
        """
        Gets the UNET key for the current configuration.
        """
        return DiffusionPipelineManager.get_vae_key(size=self.animator_size)

    @property
    def animator_tensorrt_vae_dir(self) -> str:
        """
        Gets where the tensorrt VAE engine will be stored for the animator.
        """
        path = os.path.join(self.animator_tensorrt_dir, "vae", self.animator_vae_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def animator_onnx_vae_dir(self) -> str:
        """
        Gets where the onnx VAE engine will be stored for the animator.
        """
        path = os.path.join(self.animator_onnx_dir, "vae", self.animator_vae_key)
        check_make_directory(path)
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            self.write_model_metadata(metadata_path)
        return path

    @property
    def tensorrt_is_supported(self) -> bool:
        """
        Tries to import tensorrt to see if it's supported.
        """
        if not hasattr(self, "_tensorrt_is_supported"):
            from enfugue.diffusion.util import tensorrt_available
            self._tensorrt_is_supported = tensorrt_available()
        return self._tensorrt_is_supported

    @property
    def tensorrt_is_enabled(self) -> bool:
        """
        By default this is always enabled. This is independent from supported/ready.
        """
        if not hasattr(self, "_tensorrt_enabled"):
            self._tensorrt_enabled = True
        return self._tensorrt_enabled

    @tensorrt_is_enabled.setter
    def tensorrt_is_enabled(self, new_enabled: bool) -> None:
        """
        Disables or enables TensorRT.
        """
        if new_enabled != self.tensorrt_is_enabled and self.tensorrt_is_ready:
            self.unload_pipeline("TensorRT enabled or disabled")
        if new_enabled != self.tensorrt_is_enabled and self.inpainter_tensorrt_is_ready:
            self.unload_inpainter("TensorRT enabled or disabled")
        if new_enabled != self.tensorrt_is_enabled and self.animator_tensorrt_is_ready:
            self.unload_animator("TensorRT enabled or disabled")
        if new_enabled != self.tensorrt_is_enabled and self.refiner_tensorrt_is_ready:
            self.unload_refiner("TensorRT enabled or disabled")
        self._tensorrt_enabled = new_enabled

    @property
    def tensorrt_is_ready(self) -> bool:
        """
        Checks to determine if Tensor RT is ready based on the existence of engines.
        """
        if not self.tensorrt_is_supported:
            return False
        from enfugue.diffusion.rt.engine import Engine

        trt_ready = True
        if "vae" in self.TENSORRT_STAGES:
            trt_ready = trt_ready and os.path.exists(Engine.get_engine_path(self.model_tensorrt_vae_dir))
        if "clip" in self.TENSORRT_STAGES:
            trt_ready = trt_ready and os.path.exists(Engine.get_engine_path(self.model_tensorrt_clip_dir))
        if self.controlnets or self.TENSORRT_ALWAYS_USE_CONTROLLED_UNET:
            if "unet" in self.TENSORRT_STAGES:
                trt_ready = trt_ready and os.path.exists(
                    Engine.get_engine_path(self.model_tensorrt_controlled_unet_dir)
                )
        elif "unet" in self.TENSORRT_STAGES:
            trt_ready = trt_ready and os.path.exists(Engine.get_engine_path(self.model_tensorrt_unet_dir))
        return trt_ready

    @property
    def refiner_tensorrt_is_ready(self) -> bool:
        """
        Checks to determine if Tensor RT is ready based on the existence of engines for the refiner
        """
        if not self.tensorrt_is_supported:
            return False
        if self.refiner is None:
            return False
        from enfugue.diffusion.rt.engine import Engine

        trt_ready = True
        if "vae" in self.TENSORRT_STAGES:
            trt_ready = trt_ready and os.path.exists(Engine.get_engine_path(self.refiner_tensorrt_vae_dir))
        if "clip" in self.TENSORRT_STAGES:
            trt_ready = trt_ready and os.path.exists(Engine.get_engine_path(self.refiner_tensorrt_clip_dir))
        if self.refiner_controlnets or self.TENSORRT_ALWAYS_USE_CONTROLLED_UNET:
            if "unet" in self.TENSORRT_STAGES:
                trt_ready = trt_ready and os.path.exists(
                    Engine.get_engine_path(self.refiner_tensorrt_controlled_unet_dir)
                )
        elif "unet" in self.TENSORRT_STAGES:
            trt_ready = trt_ready and os.path.exists(Engine.get_engine_path(self.refiner_tensorrt_unet_dir))
        return trt_ready

    @property
    def inpainter_tensorrt_is_ready(self) -> bool:
        """
        Checks to determine if Tensor RT is ready based on the existence of engines for the inpainter
        """
        if not self.tensorrt_is_supported:
            return False
        if self.inpainter is None:
            return False
        from enfugue.diffusion.rt.engine import Engine

        trt_ready = True
        if "vae" in self.TENSORRT_STAGES:
            trt_ready = trt_ready and os.path.exists(Engine.get_engine_path(self.inpainter_tensorrt_vae_dir))
        if "clip" in self.TENSORRT_STAGES:
            trt_ready = trt_ready and os.path.exists(Engine.get_engine_path(self.inpainter_tensorrt_clip_dir))
        if self.inpainter_controlnets or self.TENSORRT_ALWAYS_USE_CONTROLLED_UNET:
            if "unet" in self.TENSORRT_STAGES:
                trt_ready = trt_ready and os.path.exists(
                    Engine.get_engine_path(self.inpainter_tensorrt_controlled_unet_dir)
                )
        elif "unet" in self.TENSORRT_STAGES:
            trt_ready = trt_ready and os.path.exists(Engine.get_engine_path(self.inpainter_tensorrt_unet_dir))
        return trt_ready

    @property
    def animator_tensorrt_is_ready(self) -> bool:
        """
        Checks to determine if Tensor RT is ready based on the existence of engines for the animator
        """
        if not self.tensorrt_is_supported:
            return False
        if self.animator is None:
            return False
        from enfugue.diffusion.rt.engine import Engine

        trt_ready = True
        if "vae" in self.TENSORRT_STAGES:
            trt_ready = trt_ready and os.path.exists(Engine.get_engine_path(self.animator_tensorrt_vae_dir))
        if "clip" in self.TENSORRT_STAGES:
            trt_ready = trt_ready and os.path.exists(Engine.get_engine_path(self.animator_tensorrt_clip_dir))
        if self.animator_controlnets or self.TENSORRT_ALWAYS_USE_CONTROLLED_UNET:
            if "unet" in self.TENSORRT_STAGES:
                trt_ready = trt_ready and os.path.exists(
                    Engine.get_engine_path(self.animator_tensorrt_controlled_unet_dir)
                )
        elif "unet" in self.TENSORRT_STAGES:
            trt_ready = trt_ready and os.path.exists(Engine.get_engine_path(self.animator_tensorrt_unet_dir))
        return trt_ready

    @property
    def build_tensorrt(self) -> bool:
        """
        Checks to see if TensorRT should be built based on configuration.
        """
        if not hasattr(self, "_build_tensorrt"):
            if not self.tensorrt_is_supported:
                self._build_tensorrt = False
            else:
                self._build_tensorrt = self.configuration.get("enfugue.tensorrt", False)
        return self._build_tensorrt

    @build_tensorrt.setter
    def build_tensorrt(self, new_build: bool) -> None:
        """
        Changes whether or not TensorRT engines should be built when absent
        """
        self._build_tensorrt = new_build
        if not self.tensorrt_is_ready and self.tensorrt_is_supported:
            self.unload_pipeline("preparing for TensorRT build")
        if not self.inpainter_tensorrt_is_ready and self.tensorrt_is_supported:
            self.unload_inpainter("preparing for TensorRT build")
        if not self.animator_tensorrt_is_ready and self.tensorrt_is_supported:
            self.unload_animator("preparing for TensorRT build")
        if not self.refiner_tensorrt_is_ready and self.tensorrt_is_supported:
            self.unload_refiner("preparing for TensorRT build")

    @property
    def use_tensorrt(self) -> bool:
        """
        Gets the ultimate decision on whether the tensorrt pipeline should be used.
        """
        return (self.tensorrt_is_ready or self.build_tensorrt) and self.tensorrt_is_enabled

    @property
    def refiner_use_tensorrt(self) -> bool:
        """
        Gets the ultimate decision on whether the tensorrt pipeline should be used for the refiner.
        """
        return (self.refiner_tensorrt_is_ready or self.build_tensorrt) and self.tensorrt_is_enabled

    @property
    def inpainter_use_tensorrt(self) -> bool:
        """
        Gets the ultimate decision on whether the tensorrt pipeline should be used for the inpainter.
        """
        return (self.inpainter_tensorrt_is_ready or self.build_tensorrt) and self.tensorrt_is_enabled

    @property
    def animator_use_tensorrt(self) -> bool:
        """
        Gets the ultimate decision on whether the tensorrt pipeline should be used for the animator.
        """
        return False
        # return (self.animator_tensorrt_is_ready or self.build_tensorrt) and self.tensorrt_is_enabled

    @property
    def use_directml(self) -> bool:
        """
        Determine if directml should be used
        """
        import torch
        from enfugue.diffusion.util import directml_available

        return not torch.cuda.is_available() and directml_available()

    @property
    def pipeline_switch_mode(self) -> Optional[PIPELINE_SWITCH_MODE_LITERAL]:
        """
        Defines how to switch to pipelines.
        """
        if not hasattr(self, "_pipeline_switch_mode"):
            self._pipeline_switch_mode = self.configuration.get("enfugue.pipeline.switch", "offload")
        return self._pipeline_switch_mode

    @pipeline_switch_mode.setter
    def pipeline_switch_mode(self, mode: Optional[PIPELINE_SWITCH_MODE_LITERAL]) -> None:
        """
        Changes how pipelines get switched.
        """
        self._pipeline_switch_mode = mode

    @property
    def pipeline_sequential_onload(self) -> bool:
        """
        Defines how pipelines are loaded into memory.
        """
        if not hasattr(self, "_pipeline_sequential_onload"):
            self._pipeline_sequential_onload = self.configuration.get("enfugue.pipeline.sequential", False) in [1, True, "1"]
        return self._pipeline_sequential_onload

    @pipeline_sequential_onload.setter
    def pipeline_sequential_onload(self, new_onload: bool) -> None:
        """
        Defines how pipelines are loaded into memory.
        """
        self._pipeline_sequential_onload = new_onload

    @property
    def create_inpainter(self) -> bool:
        """
        Defines how to switch to inpainting.
        """
        configured = self.configuration.get("enfugue.pipeline.inpainter", True)
        if type(configured) is bool:
            return configured
        if configured == "sd":
            return not self.is_sdxl
        elif configured == "xl":
            return self.is_sdxl
        logger.warning(f"Unknown configuration for inpainting '{configured}', defaulting to True")
        return True

    @property
    def create_animator(self) -> bool:
        """
        Defines how to switch to inpainting.
        """
        configured = self.configuration.get("enfugue.pipeline.animator", None)
        if configured is None:
            return not self.is_sdxl
        return configured

    @property
    def refiner_strength(self) -> float:
        """
        Gets the denoising strength of the refiner
        """
        if not hasattr(self, "_refiner_strength"):
            self._refiner_strength = self.configuration.get("enfugue.refiner.strength", 0.3)
        return self._refiner_strength

    @refiner_strength.setter
    def refiner_strength(self, new_strength: float) -> None:
        """
        Sets the denoising strength of the refiner
        """
        self._refiner_strength = new_strength

    @property
    def refiner_start(self) -> float:
        """
        Gets where in the denoising phase we should switch to refining.
        """
        if not hasattr(self, "_refiner_strength"):
            self._refiner_start = self.configuration.get("enfugue.refiner.start", 0.85)
        return self._refiner_start

    @refiner_start.setter
    def refiner_start(self, new_refiner_start: float) -> None:
        """
        Sets where in the denoising phase we should switch to refining.
        """
        self._refiner_start = max(min(new_refiner_start, 1.0), 0.0)

    @property
    def refiner_guidance_scale(self) -> float:
        """
        Gets the guidance_ cale of the refiner
        """
        if not hasattr(self, "_refiner_guidance_scale"):
            self._refiner_guidance_scale = self.configuration.get("enfugue.refiner.guidance_scale", 5.0)
        return self._refiner_guidance_scale

    @refiner_guidance_scale.setter
    def refiner_guidance_scale(self, new_guidance_scale: float) -> None:
        """
        Sets the guidance scale of the refiner
        """
        self._refiner_guidance_scale = new_guidance_scale

    @property
    def refiner_aesthetic_score(self) -> float:
        """
        Gets the refiner_aesthetic score for the refiner
        """
        if not hasattr(self, "_refiner_aesthetic_score"):
            self._refiner_aesthetic_score = self.configuration.get("enfugue.refiner.refiner_aesthetic_score", 6.0)
        return self._refiner_aesthetic_score

    @refiner_aesthetic_score.setter
    def refiner_aesthetic_score(self, new_refiner_aesthetic_score: float) -> None:
        """
        Sets the refiner_aesthetic score for the refiner
        """
        self._refiner_aesthetic_score = new_refiner_aesthetic_score

    @property
    def refiner_negative_aesthetic_score(self) -> float:
        """
        Gets the negative refiner_aesthetic score for the refiner
        """
        if not hasattr(self, "_refiner_negative_aesthetic_score"):
            self._refiner_negative_aesthetic_score = self.configuration.get(
                "enfugue.refiner.refiner_negative_aesthetic_score", 2.5
            )
        return self._refiner_negative_aesthetic_score

    @refiner_negative_aesthetic_score.setter
    def refiner_negative_aesthetic_score(self, new_refiner_negative_aesthetic_score: float) -> None:
        """
        Sets the negative refiner_aesthetic score for the refiner
        """
        self._refiner_negative_aesthetic_score = new_refiner_negative_aesthetic_score

    @property
    def pipeline_class(self) -> Type:
        """
        Gets the pipeline class to use.
        """
        if self.use_tensorrt:
            from enfugue.diffusion.rt.pipeline import EnfugueTensorRTStableDiffusionPipeline

            return EnfugueTensorRTStableDiffusionPipeline
        else:
            from enfugue.diffusion.pipeline import EnfugueStableDiffusionPipeline

            return EnfugueStableDiffusionPipeline

    @property
    def refiner_pipeline_class(self) -> Type:
        """
        Gets the pipeline class to use.
        """
        if self.refiner_use_tensorrt:
            from enfugue.diffusion.rt.pipeline import EnfugueTensorRTStableDiffusionPipeline

            return EnfugueTensorRTStableDiffusionPipeline
        else:
            from enfugue.diffusion.pipeline import EnfugueStableDiffusionPipeline

            return EnfugueStableDiffusionPipeline

    @property
    def inpainter_pipeline_class(self) -> Type:
        """
        Gets the pipeline class to use.
        """
        if self.inpainter_use_tensorrt:
            from enfugue.diffusion.rt.pipeline import EnfugueTensorRTStableDiffusionPipeline

            return EnfugueTensorRTStableDiffusionPipeline
        else:
            from enfugue.diffusion.pipeline import EnfugueStableDiffusionPipeline

            return EnfugueStableDiffusionPipeline

    @property
    def animator_pipeline_class(self) -> Type:
        """
        Gets the pipeline class to use.
        """
        if self.animator_use_tensorrt:
            raise RuntimeError("No TensorRT animation pipeline exists yet.")
        else:
            from enfugue.diffusion.animate.pipeline import EnfugueAnimateStableDiffusionPipeline
            return EnfugueAnimateStableDiffusionPipeline

    @property
    def model(self) -> str:
        """
        Gets the configured model.
        """
        if not hasattr(self, "_model"):
            self._model = self.configuration.get("enfugue.model", DEFAULT_MODEL)
        return self._model

    @model.setter
    def model(self, new_model: Optional[str]) -> None:
        """
        Sets a new model. Destroys the pipeline.
        """
        if new_model is None:
            model = self.configuration.get("enfugue.model", DEFAULT_MODEL)
        else:
            model = new_model
        model = self.check_get_default_model(model)
        model = self.check_download_model(self.engine_checkpoints_dir, model)
        if not model:
            raise ValueError(f"Cannot find model {new_model}")

        model_name, _ = os.path.splitext(os.path.basename(model))
        if self.model_name != model_name:
            self.unload_pipeline("model changing")
            if self.is_default_animator and getattr(self, "_animator_pipeline", None) is not None:
                self.unload_animator("base model changing")
                self.is_default_animator = False
            if self.is_default_inpainter and getattr(self, "_inpainter_pipeline", None) is not None:
                self.unload_inpainter("base model changing")
                self.is_default_inpainter = False
        self._model = model
        if hasattr(self, "_model_metadata"):
            delattr(self, "_model_metadata")

    @property
    def model_name(self) -> str:
        """
        Gets just the basename of the model
        """
        return os.path.splitext(os.path.basename(self.model))[0]

    @property
    def model_metadata(self) -> ModelMetadata:
        """
        Gets metadata from the model
        """
        if not hasattr(self, "_model_metadata"):
            from enfugue.diffusion.util import ModelMetadata
            self._model_metadata = ModelMetadata.from_file(self.model)
        return self._model_metadata

    @property
    def has_refiner(self) -> bool:
        """
        Returns true if the refiner is set.
        """
        return self.refiner is not None

    @property
    def refiner(self) -> Optional[str]:
        """
        Gets the configured refiner.
        """
        if not hasattr(self, "_refiner"):
            self._refiner = self.configuration.get("enfugue.refiner", None)
        return self._refiner

    @refiner.setter
    def refiner(self, new_refiner: Optional[str]) -> None:
        """
        Sets a new refiner. Destroys the refiner pipelline.
        """
        if new_refiner is None:
            self._refiner = None
            return
        refiner = self.check_get_default_model(new_refiner)
        refiner = self.check_download_model(self.engine_checkpoints_dir, refiner)
        if not refiner:
            raise ValueError(f"Cannot find refiner {new_refiner}")
        refiner_name, _ = os.path.splitext(os.path.basename(refiner))
        if self.refiner_name != refiner_name:
            self.unload_refiner("model changing")
        self._refiner = refiner
        if hasattr(self, "_refiner_metadata"):
            delattr(self, "_refiner_metadata")

    @property
    def refiner_name(self) -> Optional[str]:
        """
        Gets just the basename of the refiner
        """
        if self.refiner is None:
            return None
        return os.path.splitext(os.path.basename(self.refiner))[0]

    @property
    def refiner_metadata(self) -> ModelMetadata:
        """
        Gets metadata from the refiner
        """
        if not hasattr(self, "_refiner_metadata"):
            from enfugue.diffusion.util import ModelMetadata
            self._refiner_metadata = ModelMetadata.from_file(self.refiner) # type: ignore[arg-type]
        return self._refiner_metadata

    @property
    def has_inpainter(self) -> bool:
        """
        Returns true if the inpainter is set.
        """
        return self.inpainter is not None or (
            os.path.exists(self.default_inpainter_path) or (
                self.default_inpainter_path.startswith("http") and not self.offline
            )
        )

    @property
    def inpainter(self) -> Optional[str]:
        """
        Gets the configured inpainter.
        """
        if not hasattr(self, "_inpainter"):
            self._inpainter = self.configuration.get("enfugue.inpainter", None)
        return self._inpainter

    @inpainter.setter
    def inpainter(self, new_inpainter: Optional[str]) -> None:
        """
        Sets a new inpainter. Destroys the inpainter pipelline.
        """
        if new_inpainter is None:
            self._inpainter = None
            return
        inpainter = self.check_get_default_model(new_inpainter)
        inpainter = self.check_download_model(self.engine_checkpoints_dir, inpainter)
        if not inpainter:
            raise ValueError(f"Cannot find inpainter {new_inpainter}")
        inpainter_name, _ = os.path.splitext(os.path.basename(inpainter))
        if self.inpainter_name != inpainter_name:
            self.unload_inpainter("model changing")
        self._inpainter = inpainter
        if hasattr(self, "_inpainter_metadata"):
            delattr(self, "_inpainter_metadata")

    @property
    def inpainter_name(self) -> Optional[str]:
        """
        Gets just the basename of the inpainter
        """
        if self.inpainter is None:
            return None
        return os.path.splitext(os.path.basename(self.inpainter))[0]

    @property
    def inpainter_metadata(self) -> ModelMetadata:
        """
        Gets metadata from the inpainter
        """
        if not hasattr(self, "_inpainter_metadata"):
            from enfugue.diffusion.util import ModelMetadata
            self._inpainter_metadata = ModelMetadata.from_file(self.inpainter) # type: ignore[arg-type]
        return self._inpainter_metadata

    @property
    def animator(self) -> Optional[str]:
        """
        Gets the configured animator.
        """
        if not hasattr(self, "_animator"):
            self._animator = self.configuration.get("enfugue.animator", None)
        return self._animator

    @animator.setter
    def animator(self, new_animator: Optional[str]) -> None:
        """
        Sets a new animator. Destroys the animator pipelline.
        """
        if new_animator is None:
            self._animator = None
            return
        animator = self.check_get_default_model(new_animator)
        animator = self.check_download_model(self.engine_checkpoints_dir, animator)
        if not animator:
            raise ValueError(f"Cannot find animator {new_animator}")

        animator_name, _ = os.path.splitext(os.path.basename(animator))
        if self.animator_name != animator_name:
            self.unload_animator("model changing")
        self._animator = animator
        if hasattr(self, "_animator_metadata"):
            delattr(self, "_animator_metadata")

    @property
    def animator_name(self) -> Optional[str]:
        """
        Gets just the basename of the animator
        """
        if self.animator is None:
            return None
        return os.path.splitext(os.path.basename(self.animator))[0]

    @property
    def animator_metadata(self) -> ModelMetadata:
        """
        Gets metadata from the animator
        """
        if not hasattr(self, "_animator_metadata"):
            from enfugue.diffusion.util import ModelMetadata
            self._animator_metadata = ModelMetadata.from_file(self.animator) # type: ignore[arg-type]
        return self._animator_metadata

    @property
    def has_animator(self) -> bool:
        """
        Returns true if the animator is set.
        """
        return self.animator is not None

    @property
    def dtype(self) -> torch.dtype:
        """
        Gets the default or configured torch data type
        """
        if not hasattr(self, "_torch_dtype"):
            import torch

            device_type = self.device.type

            if device_type == "cpu":
                logger.debug("Inferencing on cpu, must use dtype bfloat16")
                self._torch_dtype = torch.bfloat16
            elif device_type == "cuda" and torch.version.hip:
                logger.debug("Inferencing on rocm, must use dtype float32")  # type: ignore[unreachable]
                self._torch_dtype = torch.float
            else:
                configuration_dtype = self.configuration.get("enfugue.dtype", None)
                if configuration_dtype is None:
                    logger.debug(f"Inferencing on {device_type}, defaulting to dtype float16")
                    self._torch_dtype = torch.half
                else:
                    logger.debug(f"Inferencing on {device_type}, using configured dtype {configuration_dtype}")
                    if configuration_dtype == "float16" or configuration_dtype == "half":
                        self._torch_dtype = torch.half
                    elif (
                        configuration_dtype == "float32"
                        or configuration_dtype == "float"
                        or configuration_dtype == "full"
                    ):
                        self._torch_dtype = torch.float
                    else:
                        raise ConfigurationError(
                            f"dtype incorrectly configured, use 'float16/half' or 'float32/float/full', got '{configuration_dtype}'"
                        )
        return self._torch_dtype

    @dtype.setter
    def dtype(self, new_dtype: Union[str, torch.dtype]) -> None:
        """
        Sets the torch dtype.
        Deletes the pipeline if it's different from the previous one.
        """
        if self.device.type == "cpu":
            raise ValueError("CPU-based diffusion can only use bfloat")
        if new_dtype == "float16" or new_dtype == "half":
            new_dtype = torch.half
        elif new_dtype == "float32" or new_dtype == "float":
            new_dtype = torch.float
        else:
            raise ConfigurationError("dtype incorrectly configured, use 'float16/half' or 'float32/float'")

        if getattr(self, "_torch_dtype", new_dtype) != new_dtype:
            self.unload_pipeline("data type changing")
            self.unload_refiner("data type changing")
            self.unload_inpainter("data type changing")
            self.unload_animator("data type changing")

        self._torch_dtype = new_dtype

    @property
    def half(self) -> bool:
        """
        Returns true if the dtype is half-precision.
        """
        import torch
        return self.dtype is torch.float16

    @property
    def lora(self) -> List[Tuple[str, float]]:
        """
        Get LoRA added to the text encoder and UNet.
        """
        return getattr(self, "_lora", [])

    @lora.setter
    def lora(self, new_lora: Optional[Union[str, List[str], Tuple[str, float], List[Tuple[str, float]]]]) -> None:
        """
        Sets new LoRA. Destroys the pipeline.
        """
        if new_lora is None:
            if hasattr(self, "_lora") and len(self._lora) > 0:
                self.unload_pipeline("LoRA changing")
                self.unload_inpainter("LoRA changing")
                self.unload_animator("LoRA changing")
            self._lora: List[Tuple[str, float]] = []
            return

        lora: List[Tuple[str, float]] = []
        if isinstance(new_lora, list):
            for this_lora in new_lora:
                if isinstance(this_lora, list):
                    lora.append(tuple(this_lora))  # type: ignore[unreachable]
                elif isinstance(this_lora, tuple):
                    lora.append(this_lora)
                else:
                    lora.append((this_lora, 1))
        elif isinstance(new_lora, tuple):
            lora = [new_lora]
        else:
            lora = [(new_lora, 1)]

        for i, (model, weight) in enumerate(lora):
            find_model = self.check_download_model(self.engine_lora_dir, model)
            if not find_model:
                raise ValueError(f"Cannot find LoRA model {model}")
            lora[i] = (find_model, weight)

        if getattr(self, "_lora", []) != lora:
            self.unload_pipeline("LoRA changing")
            self.unload_inpainter("LoRA changing")
            self.unload_animator("LoRA changing")
            self._lora = lora

    @property
    def lora_names_weights(self) -> List[Tuple[str, float]]:
        """
        Gets the basenames of any LoRA present.
        """
        return [(os.path.splitext(os.path.basename(lora))[0], weight) for lora, weight in self.lora]

    @property
    def lycoris(self) -> List[Tuple[str, float]]:
        """
        Get lycoris added to the text encoder and UNet.
        """
        return getattr(self, "_lycoris", [])

    @lycoris.setter
    def lycoris(self, new_lycoris: Optional[Union[str, List[str], Tuple[str, float], List[Tuple[str, float]]]]) -> None:
        """
        Sets new lycoris. Destroys the pipeline.
        """
        if new_lycoris is None:
            if hasattr(self, "_lycoris") and len(self._lycoris) > 0:
                self.unload_pipeline("LyCORIS changing")
                self.unload_inpainter("LyCORIS changing")
                self.unload_animator("LyCORIS changing")
            self._lycoris: List[Tuple[str, float]] = []
            return

        lycoris: List[Tuple[str, float]] = []
        if isinstance(new_lycoris, list):
            for this_lycoris in new_lycoris:
                if isinstance(this_lycoris, list):
                    lycoris.append(tuple(this_lycoris))  # type: ignore[unreachable]
                elif isinstance(this_lycoris, tuple):
                    lycoris.append(this_lycoris)
                else:
                    lycoris.append((this_lycoris, 1))
        elif isinstance(new_lycoris, tuple):
            lycoris = [new_lycoris]
        else:
            lycoris = [(new_lycoris, 1)]

        for i, (model, weight) in enumerate(lycoris):
            model = self.check_download_model(self.engine_lycoris_dir, model)
            if not model:
                raise ValueError(f"Cannot find LyCORIS model {model}")
            lycoris[i] = (model, weight)

        if getattr(self, "_lycoris", []) != lycoris:
            self.unload_pipeline("LyCORIS changing")
            self.unload_inpainter("LyCORIS changing")
            self.unload_animator("LyCORIS changing")
            self._lycoris = lycoris

    @property
    def lycoris_names_weights(self) -> List[Tuple[str, float]]:
        """
        Gets the basenames of any lycoris present.
        """
        return [(os.path.splitext(os.path.basename(lycoris))[0], weight) for lycoris, weight in self.lycoris]

    @property
    def inversion(self) -> List[str]:
        """
        Get textual inversion added to the text encoder.
        """
        return getattr(self, "_inversion", [])

    @inversion.setter
    def inversion(self, new_inversion: Optional[Union[str, List[str]]]) -> None:
        """
        Sets new textual inversion. Destroys the pipeline.
        """
        if new_inversion is None:
            if hasattr(self, "_inversion") and len(self._inversion) > 0:
                self.unload_pipeline("Textual Inversions changing")
                self.unload_inpainter("Textual Inversions changing")
                self.unload_animator("Textual Inversions changing")
            self._inversion: List[str] = []
            return

        if not isinstance(new_inversion, list):
            new_inversion = [new_inversion]
        for i, model in enumerate(new_inversion):
            model = self.check_download_model(self.engine_inversion_dir, model)
            if not model:
                raise ValueError(f"Cannot find inversion model {model}")
            new_inversion[i] = model
        if getattr(self, "_inversion", []) != new_inversion:
            self.unload_pipeline("Textual Inversions changing")
            self.unload_inpainter("Textual Inversions changing")
            self.unload_animator("Textual Inversions changing")
            self._inversion = new_inversion

    @property
    def inversion_names(self) -> List[str]:
        """
        Gets the basenames of any textual inversions present.
        """
        return [os.path.splitext(os.path.basename(inversion))[0] for inversion in self.inversion]

    @property
    def reload_motion_module(self) -> bool:
        """
        Returns true if the motion module should be reloaded.
        """
        return getattr(self, "_reload_motion_module", False)

    @reload_motion_module.setter
    def reload_motion_module(self, reload: bool) -> None:
        """
        Sets if the motion module should be reloaded.
        """
        self._reload_motion_module = reload

    @property
    def motion_module(self) -> Optional[str]:
        """
        Gets optional configured non-default motion module.
        """
        return getattr(self, "_motion_module", None)

    @motion_module.setter
    def motion_module(self, new_module: Optional[str]) -> None:
        """
        Sets a new motion module or reverts to default.
        """
        if (
            self.motion_module is None and new_module is not None or
            self.motion_module is not None and new_module is None or
            (
                self.motion_module is not None and
                new_module is not None and
                self.motion_module != new_module
            )
        ):
            self.reload_motion_module = True
        if new_module is not None:
            self._motion_module = self.check_download_model(self.engine_motion_dir, new_module)
        else:
            self._motion_module = None # type: ignore[assignment]

    @property
    def position_encoding_truncate_length(self) -> Optional[int]:
        """
        An optional length (frames) to truncate position encoder tensors to
        """
        return getattr(self, "_position_encoding_truncate_length", None)

    @position_encoding_truncate_length.setter
    def position_encoding_truncate_length(self, new_length: Optional[int]) -> None:
        """
        Sets position encoder truncate length.
        """
        if (
            self.position_encoding_truncate_length is None and new_length is not None or
            self.position_encoding_truncate_length is not None and new_length is None or
            (
                self.position_encoding_truncate_length is not None and 
                new_length is not None and
                self.position_encoding_truncate_length != new_length
            )
        ):
            self.reload_motion_module = True
        self._position_encoding_truncate_length = new_length

    @property
    def position_encoding_scale_length(self) -> Optional[int]:
        """
        An optional length (frames) to scale position encoder tensors to
        """
        return getattr(self, "_position_encoding_scale_length", None)

    @position_encoding_scale_length.setter
    def position_encoding_scale_length(self, new_length: Optional[int]) -> None:
        """
        Sets position encoder scale length.
        """
        if (
            self.position_encoding_scale_length is None and new_length is not None or
            self.position_encoding_scale_length is not None and new_length is None or
            (
                self.position_encoding_scale_length is not None and 
                new_length is not None and
                self.position_encoding_scale_length != new_length
            )
        ):
            self.reload_motion_module = True
        self._position_encoding_scale_length = new_length

    @property
    def model_diffusers_cache_dir(self) -> Optional[str]:
        """
        Gets where the diffusers cache directory is saved for this model, if there is any.
        """
        if os.path.exists(os.path.join(self.model_diffusers_dir, "model_index.json")):
            return self.model_diffusers_dir
        elif os.path.exists(os.path.join(self.model_tensorrt_dir, "model_index.json")):
            return self.model_tensorrt_dir
        return None

    @property
    def engine_cache_exists(self) -> bool:
        """
        Gets whether or not the diffusers cache exists.
        """
        return self.model_diffusers_cache_dir is not None and os.path.exists(
            os.path.join(self.model_diffusers_cache_dir, "model_index.json")
        )

    @property
    def refiner_diffusers_cache_dir(self) -> Optional[str]:
        """
        Ggets where the diffusers cache directory is saved for this refiner, if there is any.
        """
        if os.path.exists(os.path.join(self.refiner_diffusers_dir, "model_index.json")):
            return self.refiner_diffusers_dir
        elif os.path.exists(os.path.join(self.refiner_tensorrt_dir, "model_index.json")):
            return self.refiner_tensorrt_dir
        return None

    @property
    def refiner_engine_cache_exists(self) -> bool:
        """
        Gets whether or not the diffusers cache exists.
        """
        return self.refiner_diffusers_cache_dir is not None and os.path.exists(
            os.path.join(self.refiner_diffusers_cache_dir, "model_index.json")
        )

    @property
    def inpainter_diffusers_cache_dir(self) -> Optional[str]:
        """
        Ggets where the diffusers cache directory is saved for this inpainter, if there is any.
        """
        if os.path.exists(os.path.join(self.inpainter_diffusers_dir, "model_index.json")):
            return self.inpainter_diffusers_dir
        elif os.path.exists(os.path.join(self.inpainter_tensorrt_dir, "model_index.json")):
            return self.inpainter_tensorrt_dir
        return None

    @property
    def inpainter_engine_cache_exists(self) -> bool:
        """
        Gets whether or not the diffusers cache exists.
        """
        return self.inpainter_diffusers_cache_dir is not None and os.path.exists(
            os.path.join(self.inpainter_diffusers_cache_dir, "model_index.json")
        )

    @property
    def animator_diffusers_cache_dir(self) -> Optional[str]:
        """
        Ggets where the diffusers cache directory is saved for this animator, if there is any.
        """
        if os.path.exists(os.path.join(self.animator_diffusers_dir, "model_index.json")):
            return self.animator_diffusers_dir
        elif os.path.exists(os.path.join(self.animator_tensorrt_dir, "model_index.json")):
            return self.animator_tensorrt_dir
        return None

    @property
    def animator_engine_cache_exists(self) -> bool:
        """
        Gets whether or not the diffusers cache exists.
        """
        return self.animator_diffusers_cache_dir is not None and os.path.exists(
            os.path.join(self.animator_diffusers_cache_dir, "model_index.json")
        )

    @property
    def should_cache(self) -> bool:
        """
        Returns true if the model should always be cached.
        """
        configured = self.configuration.get("enfugue.pipeline.cache", None)
        if configured == "xl":
            return self.is_sdxl
        return configured in ["always", True]

    @property
    def should_cache_inpainter(self) -> bool:
        """
        Returns true if the inpainter model should always be cached.
        """
        configured = self.configuration.get("enfugue.pipeline.cache", None)
        if configured == "xl":
            return self.inpainter_is_sdxl
        return configured in ["always", True]

    @property
    def should_cache_animator(self) -> bool:
        """
        Returns true if the animator model should always be cached.
        """
        configured = self.configuration.get("enfugue.pipeline.cache", None)
        if configured == "xl":
            return self.animator_is_sdxl
        return configured in ["always", True]

    @property
    def should_cache_refiner(self) -> bool:
        """
        Returns true if the refiner model should always be cached.
        """
        configured = self.configuration.get("enfugue.pipeline.cache", None)
        if configured == "xl":
            return self.refiner_is_sdxl
        return configured in ["always", True]

    @property
    def is_sdxl(self) -> bool:
        """
        If the model is cached, we can know for sure by checking for sdxl-exclusive models.
        Otherwise, we guess by file name.
        """
        if getattr(self, "_pipeline", None) is not None:
            return self._pipeline.is_sdxl
        if self.engine_cache_exists:
            return os.path.exists(os.path.join(self.model_diffusers_cache_dir, "text_encoder_2"))  # type: ignore[arg-type]
        if ".safetensor" in self.model:
            return self.model_metadata.is_sdxl
        return "xl" in self.model_name.lower()

    @property
    def refiner_is_sdxl(self) -> bool:
        """
        If the refiner model is cached, we can know for sure by checking for sdxl-exclusive models.
        Otherwise, we guess by file name.
        """
        if not self.refiner_name:
            return False
        if getattr(self, "_refiner_pipeline", None) is not None:
            return self._refiner_pipeline.is_sdxl
        if self.refiner_engine_cache_exists:
            return os.path.exists(os.path.join(self.refiner_diffusers_cache_dir, "text_encoder_2"))  # type: ignore[arg-type]
        if ".safetensor" in self.refiner: # type: ignore[operator]
            return self.refiner_metadata.is_sdxl
        return "xl" in self.refiner_name.lower()

    @property
    def refiner_requires_aesthetic_score(self) -> bool:
        """
        If the refiner model is cached, check the model_index.json file for the requirement of an aesthetic score.
        Otherwise, we guess by file name.
        """
        if not self.refiner_name:
            return False
        if self.refiner_engine_cache_exists:
            return load_json(os.path.join(self.refiner_diffusers_cache_dir, "model_index.json")).get("requires_aesthetic_score", False) # type: ignore[arg-type]
        if ".safetensor" in self.refiner: # type: ignore[operator]
            return self.refiner_metadata.model_type == "SDXL-Refiner"
        return "xl" in self.refiner_name.lower() and "refine" in self.refiner_name.lower()

    @property
    def inpainter_is_sdxl(self) -> bool:
        """
        If the inpainter model is cached, we can know for sure by checking for sdxl-exclusive models.
        Otherwise, we guess by file name.
        """
        if not self.inpainter_name:
            return self.is_sdxl
        if getattr(self, "_inpainter_pipeline", None) is not None:
            return self._inpainter_pipeline.is_sdxl
        if self.inpainter_engine_cache_exists:
            return os.path.exists(os.path.join(self.inpainter_diffusers_cache_dir, "text_encoder_2"))  # type: ignore[arg-type]
        if ".safetensor" in self.inpainter: # type: ignore[operator]
            return self.inpainter_metadata.is_sdxl
        return "xl" in self.inpainter_name.lower()

    @property
    def animator_is_sdxl(self) -> bool:
        """
        If the animator model is cached, we can know for sure by checking for sdxl-exclusive models.
        Otherwise, we guess by file name.
        """
        if not self.animator_name:
            return False
        if getattr(self, "_animator_pipeline", None) is not None:
            return self._animator_pipeline.is_sdxl
        if self.animator_engine_cache_exists:
            return os.path.exists(os.path.join(self.animator_diffusers_cache_dir, "text_encoder_2"))  # type: ignore[arg-type]
        if ".safetensor" in self.animator: # type: ignore[operator]
            return self.animator_metadata.is_sdxl
        return "xl" in self.animator_name.lower()

    @property
    def svd_xt(self) -> bool:
        """
        Returns true if the SVD pipeline should use XT.
        """
        return getattr(self, "_svd_xt", False)

    @svd_xt.setter
    def svd_xt(self, value: bool) -> None:
        """
        Sets the pipeline XT, unloads the pipeline if set
        """
        if self.svd_xt != value:
            del self.svd_pipeline
        self._svd_xt = value

    def check_get_default_model(self, model: str) -> str:
        """
        Checks if a model is a default model, in which case the remote URL is returned
        to check if the resources has changed or needs to be downloaded
        """
        model_file = os.path.basename(model)
        if model_file == DEFAULT_MODEL_FILE:
            return DEFAULT_MODEL
        elif model_file == DEFAULT_INPAINTING_MODEL_FILE:
            return DEFAULT_INPAINTING_MODEL
        elif model_file == DEFAULT_SDXL_MODEL_FILE:
            return DEFAULT_SDXL_MODEL
        elif model_file == DEFAULT_SDXL_INPAINTING_MODEL_FILE:
            return DEFAULT_SDXL_INPAINTING_MODEL
        elif model_file == DEFAULT_SDXL_REFINER_FILE:
            return DEFAULT_SDXL_REFINER
        return model

    def check_create_engine_cache(self) -> None:
        """
        Converts a .ckpt file to the directory structure from diffusers
        """
        if not self.engine_cache_exists:
            from diffusers.pipelines.stable_diffusion.convert_from_ckpt import (
                download_from_original_stable_diffusion_ckpt,
            )

            _, ext = os.path.splitext(self.model)
            pipe = download_from_original_stable_diffusion_ckpt(
                self.model,
                from_safetensors=ext == ".safetensors",
            ).to(torch_dtype=self.dtype)
            pipe.save_pretrained(self.model_diffusers_dir)
            del pipe
            self.clear_memory()

    def check_create_refiner_engine_cache(self) -> None:
        """
        Converts a .safetensor file to diffusers cache
        """
        if not self.refiner_engine_cache_exists and self.refiner:
            from diffusers.pipelines.stable_diffusion.convert_from_ckpt import (
                download_from_original_stable_diffusion_ckpt,
            )

            _, ext = os.path.splitext(self.refiner)
            pipe = download_from_original_stable_diffusion_ckpt(
                self.refiner,
                from_safetensors=ext == ".safetensors",
            ).to(torch_dtype=self.dtype)
            pipe.save_pretrained(self.refiner_diffusers_dir)
            del pipe
            self.clear_memory()

    def check_create_inpainter_engine_cache(self) -> None:
        """
        Converts a .safetensor file to diffusers cache
        """
        if not self.inpainter_engine_cache_exists and self.inpainter:
            from diffusers.pipelines.stable_diffusion.convert_from_ckpt import (
                download_from_original_stable_diffusion_ckpt,
            )

            _, ext = os.path.splitext(self.inpainter)
            pipe = download_from_original_stable_diffusion_ckpt(
                self.inpainter,
                num_in_channels=9 if "inpaint" in self.inpainter.lower() else 4,
                from_safetensors=ext == ".safetensors"
            ).to(torch_dtype=self.dtype)
            pipe.save_pretrained(self.inpainter_diffusers_dir)
            del pipe
            self.clear_memory()

    def check_create_animator_engine_cache(self) -> None:
        """
        Converts a .safetensor file to diffusers cache
        """
        if not self.animator_engine_cache_exists and self.animator:
            from diffusers.pipelines.stable_diffusion.convert_from_ckpt import (
                download_from_original_stable_diffusion_ckpt,
            )

            _, ext = os.path.splitext(self.animator)
            pipe = download_from_original_stable_diffusion_ckpt(
                self.animator,
                num_in_channels=9 if "inpaint" in self.animator.lower() else 4,
                from_safetensors=ext == ".safetensors"
            ).to(torch_dtype=self.dtype)
            pipe.save_pretrained(self.animator_diffusers_dir)
            del pipe
            self.clear_memory()

    def swap_pipelines(self, to_gpu: EnfugueStableDiffusionPipeline, to_cpu: EnfugueStableDiffusionPipeline) -> None:
        """
        Swaps pipelines in and out of GPU.
        """
        modules_to_gpu = to_gpu.get_modules()
        modules_to_cpu = to_cpu.get_modules()
        modules = max(len(modules_to_gpu), len(modules_to_cpu))
        for i in range(modules):
            if i < len(modules_to_gpu):
                modules_to_gpu[i].to(self.device, dtype=self.dtype)
            if i < len(modules_to_cpu):
                modules_to_cpu[i].to(torch.device("cpu"))
            self.clear_memory()

    @property
    def pipeline(self) -> EnfugueStableDiffusionPipeline:
        """
        Instantiates the pipeline.
        """
        if not hasattr(self, "_pipeline"):
            self.model = self.check_download_model(self.engine_checkpoints_dir, self.model)

            kwargs = {
                "cache_dir": self.engine_cache_dir,
                "engine_size": self.tensorrt_size,
                "tiling_stride": self.tiling_stride,
                "requires_safety_checker": self.safe,
                "torch_dtype": self.dtype,
                "force_full_precision_vae": self.is_sdxl and "fp16_vae" not in self.model and (self.vae_name is None or "16" not in self.vae_name),
                "controlnets": self.controlnets,
                "ip_adapter": self.ip_adapter,
                "task_callback": getattr(self, "_task_callback", None),
                "vae": self.vae,
                "vae_preview": self.get_vae_preview(self.is_sdxl)
            }
            
            if self.use_tensorrt:
                if self.is_sdxl:
                    raise ValueError(f"Sorry, TensorRT is not yet supported for SDXL.")
                if "unet" in self.TENSORRT_STAGES:
                    if not self.controlnets and not self.TENSORRT_ALWAYS_USE_CONTROLLED_UNET:
                        kwargs["unet_engine_dir"] = self.model_tensorrt_unet_dir
                    else:
                        kwargs["controlled_unet_engine_dir"] = self.model_tensorrt_controlled_unet_dir
                if "vae" in self.TENSORRT_STAGES:
                    kwargs["vae_engine_dir"] = self.model_tensorrt_vae_dir

                if "clip" in self.TENSORRT_STAGES:
                    kwargs["clip_engine_dir"] = self.model_tensorrt_clip_dir
                if not self.safe:
                    kwargs["safety_checker"] = None

                self.check_create_engine_cache()

                if self.model_diffusers_cache_dir is None:
                    raise IOError("Couldn't create engine cache, check logs.")

                if not self.is_sdxl:
                    kwargs["tokenizer_2"] = None
                    kwargs["text_encoder_2"] = None

                if "16" in str(self.dtype):
                    kwargs["build_half"] = True
                    kwargs["variant"] = "fp16"

                if kwargs["vae"] is None:
                    kwargs.pop("vae")

                logger.debug(
                    f"Initializing TensorRT pipeline from diffusers cache directory at {self.model_diffusers_cache_dir}. Arguments are {redact_for_log(kwargs)}"
                )

                pipeline = self.pipeline_class.from_pretrained(
                    self.model_diffusers_cache_dir,
                    local_files_only=self.offline,
                    **kwargs
                )
            elif self.model_diffusers_cache_dir is not None:
                if not self.safe:
                    kwargs["safety_checker"] = None
                if not self.is_sdxl:
                    kwargs["tokenizer_2"] = None
                    kwargs["text_encoder_2"] = None

                if "16" in str(self.dtype):
                    kwargs["variant"] = "fp16"

                if kwargs["vae"] is None:
                    kwargs.pop("vae")

                logger.debug(
                    f"Initializing pipeline from diffusers cache directory at {self.model_diffusers_cache_dir}. Arguments are {redact_for_log(kwargs)}"
                )

                pipeline = self.pipeline_class.from_pretrained(
                    self.model_diffusers_cache_dir,
                    local_files_only=self.offline,
                    **kwargs
                )
            else:
                kwargs["offload_models"] = self.pipeline_sequential_onload
                kwargs["load_safety_checker"] = self.safe

                logger.debug(f"Initializing pipeline from checkpoint at {self.model}. Arguments are {redact_for_log(kwargs)}")

                pipeline = self.pipeline_class.from_ckpt(self.model, **kwargs)
                if pipeline.is_sdxl and "16" not in self.model and (self.vae_name is None or "16" not in self.vae_name):
                    # We may have made an incorrect guess earlier if 'xl' wasn't in the filename.
                    # We can fix that here, though, by forcing full precision VAE
                    pipeline.register_to_config(force_full_precision_vae=True)
                if self.should_cache:
                    self.task_callback("Saving pipeline to pretrained cache")
                    pipeline.save_pretrained(self.model_diffusers_dir)
            # Load post-initialization controlnets
            for controlnet_name in self.controlnet_names:
                if controlnet_name.startswith("sparse"):
                    pipeline.controlnets[controlnet_name] = pipeline.get_sparse_controlnet(
                        controlnet_name,
                        cache_dir=self.engine_controlnet_dir,
                        task_callback=self.task_callback
                    ).to(self.dtype)
            if not self.tensorrt_is_ready:
                if self._ip_adapter_model is not None:
                    self.ip_adapter.check_download(
                        is_sdxl=self.is_sdxl,
                        model=self._ip_adapter_model,
                        task_callback=self.task_callback,
                    )
                    pipeline.load_ip_adapter(
                        device=self.device,
                        model=self._ip_adapter_model,
                    )
                for lora, weight in self.lora:
                    self.task_callback(f"Adding LoRA {os.path.basename(lora)} to pipeline with weight {weight}")
                    pipeline.load_lora_weights(lora, multiplier=weight)
                for lycoris, weight in self.lycoris:
                    self.task_callback(f"Adding lycoris {os.path.basename(lycoris)} to pipeline")
                    pipeline.load_lycoris_weights(lycoris, multiplier=weight)
                for inversion in self.inversion:
                    self.task_callback(f"Adding textual inversion {os.path.basename(inversion)} to pipeline")
                    pipeline.load_textual_inversion(inversion)
            # load scheduler
            if self.scheduler is not None:
                logger.debug(f"Setting scheduler to {self.scheduler.__name__}") # type: ignore[attr-defined]
                pipeline.scheduler = self.scheduler.from_config({**pipeline.scheduler_config, **self.scheduler_config}) # type: ignore[attr-defined]
            # Check for adapter LoRA
            if any([name.startswith("sparse") for name in self.controlnet_names]):
                adapter_lora_loaded = os.path.basename(SPARSE_CONTROLNET_ADAPTER_LORA) in [
                    os.path.basename(lora) for lora, weight in self.lora
                ]
                if not adapter_lora_loaded and not self.tensorrt_is_ready:
                    logger.debug("Sparse ControlNet detected, loading adapter LoRA.")
                    pipeline.load_lora_weights(
                        self.check_download_model(
                            self.engine_lora_dir,
                            SPARSE_CONTROLNET_ADAPTER_LORA
                        )
                    )
            self._pipeline = pipeline
        return self._pipeline

    @pipeline.deleter
    def pipeline(self) -> None:
        """
        Eliminates any instantiated pipeline.
        """
        if hasattr(self, "_pipeline"):
            logger.debug("Deleting pipeline.")
            del self._pipeline
            self.clear_memory()
        else:
            logger.debug("Pipeline delete called, but no pipeline present. This is not an error.")

    @property
    def refiner_pipeline(self) -> EnfugueStableDiffusionPipeline:
        """
        Instantiates the refiner pipeline.
        """
        if not self.refiner:
            raise ValueError("No refiner set")
        if not hasattr(self, "_refiner_pipeline"):
            self.refiner = self.check_download_model(self.engine_checkpoints_dir, self.refiner)

            kwargs = {
                "cache_dir": self.engine_cache_dir,
                "engine_size": self.refiner_tensorrt_size,
                "tiling_stride": self.tiling_stride,
                "torch_dtype": self.dtype,
                "requires_safety_checker": False,
                "force_full_precision_vae": self.refiner_is_sdxl and "fp16_vae" not in self.refiner and (
                    self.refiner_vae_name is None or "16" not in self.refiner_vae_name
                ),
                "controlnets": self.refiner_controlnets,
                "ip_adapter": self.ip_adapter,
                "task_callback": getattr(self, "_task_callback", None),
                "vae_preview": self.get_vae_preview(self.refiner_is_sdxl),
                "vae": self.refiner_vae
            }

            if self.refiner_use_tensorrt:
                if self.refiner_is_sdxl:
                    raise ValueError("Sorry, TensorRT is not yet supported for SDXL.")
                if "unet" in self.TENSORRT_STAGES:
                    if not self.refiner_controlnets and not self.TENSORRT_ALWAYS_USE_CONTROLLED_UNET:
                        kwargs["unet_engine_dir"] = self.refiner_tensorrt_unet_dir
                    else:
                        kwargs["controlled_unet_engine_dir"] = self.refiner_tensorrt_controlled_unet_dir

                if "vae" in self.TENSORRT_STAGES:
                    kwargs["vae_engine_dir"] = self.refiner_tensorrt_vae_dir

                if "clip" in self.TENSORRT_STAGES:
                    kwargs["clip_engine_dir"] = self.refiner_tensorrt_clip_dir

                self.check_create_refiner_engine_cache()

                if self.refiner_is_sdxl and self.refiner_requires_aesthetic_score: # type: ignore[unreachable]
                    kwargs["text_encoder"] = None # type: ignore[unreachable]
                    kwargs["tokenizer"] = None
                    kwargs["requires_aesthetic_score"] = True
                else:
                    kwargs["text_encoder_2"] = None
                    kwargs["tokenizer_2"] = None

                if "16" in str(self.dtype):
                    kwargs["build_half"] = True
                    kwargs["variant"] = "fp16"

                if kwargs["vae"] is None:
                    kwargs.pop("vae")

                logger.debug(
                    f"Initializing refiner TensorRT pipeline from diffusers cache directory at {self.refiner_diffusers_cache_dir}. Arguments are {redact_for_log(kwargs)}"
                )

                refiner_pipeline = self.refiner_pipeline_class.from_pretrained(
                    self.refiner_diffusers_cache_dir,
                    safety_checker=None,
                    local_files_only=self.offline,
                    **kwargs,
                )
            elif self.refiner_engine_cache_exists:
                if self.refiner_is_sdxl:
                    if self.refiner_requires_aesthetic_score:
                        kwargs["text_encoder"] = None
                        kwargs["tokenizer"] = None
                        kwargs["requires_aesthetic_score"] = True
                else:
                    kwargs["text_encoder_2"] = None
                    kwargs["tokenizer_2"] = None

                if "16" in str(self.dtype):
                    kwargs["variant"] = "fp16"

                if kwargs["vae"] is None:
                    kwargs.pop("vae")

                logger.debug(
                    f"Initializing refiner pipeline from diffusers cache directory at {self.refiner_diffusers_cache_dir}. Arguments are {redact_for_log(kwargs)}"
                )

                refiner_pipeline = self.refiner_pipeline_class.from_pretrained(
                    self.refiner_diffusers_cache_dir,
                    safety_checker=None,
                    local_files_only=self.offline,
                    **kwargs,
                )
            else:
                kwargs["offload_models"] = self.pipeline_sequential_onload

                logger.debug(f"Initializing refiner pipeline from checkpoint at {self.refiner}. Arguments are {redact_for_log(kwargs)}")

                refiner_pipeline = self.refiner_pipeline_class.from_ckpt(
                    self.refiner,
                    load_safety_checker=False,
                    **kwargs,
                )

                if refiner_pipeline.is_sdxl and "fp16_vae" not in self.refiner and (self.refiner_vae_name is None or "16" not in self.refiner_vae_name):
                    refiner_pipeline.register_to_config(force_full_precision_vae=True)
                if self.should_cache_refiner:
                    self.task_callback("Saving pipeline to pretrained.")
                    refiner_pipeline.save_pretrained(self.refiner_diffusers_dir)
            # load scheduler
            if self.scheduler is not None:
                logger.debug(f"Setting refiner scheduler to {self.scheduler.__name__}") # type: ignore[attr-defined]
                refiner_pipeline.scheduler = self.scheduler.from_config({**refiner_pipeline.scheduler_config, **self.scheduler_config}) # type: ignore[attr-defined]
            # Load post-initialization controlnets
            for controlnet_name in self.refiner_controlnet_names:
                adapter_lora_loaded = os.path.basename(SPARSE_CONTROLNET_ADAPTER_LORA) in [
                    os.path.basename(lora) for lora, weight in self.lora
                ]
                if controlnet_name.startswith("sparse"):
                    if not adapter_lora_loaded and not self.refiner_tensorrt_is_ready:
                        logger.debug("Sparse ControlNet detected, loading adapter LoRA.")
                        refiner_pipeline.load_lora_weights(
                            self.check_download_model(
                                self.engine_lora_dir,
                                SPARSE_CONTROLNET_ADAPTER_LORA
                            )
                        )
                        adapter_lora_loaded = True
                    refiner_pipeline.controlnets[controlnet_name] = refiner_pipeline.get_sparse_controlnet(
                        controlnet_name,
                        cache_dir=self.engine_cache_dir,
                        task_callback=self.task_callback
                    ).to(self.dtype)
            self._refiner_pipeline = refiner_pipeline
        return self._refiner_pipeline

    @refiner_pipeline.deleter
    def refiner_pipeline(self) -> None:
        """
        Unloads the refiner pipeline if present.
        """
        if hasattr(self, "_refiner_pipeline"):
            logger.debug("Deleting refiner pipeline.")
            del self._refiner_pipeline
            self.clear_memory()
        else:
            logger.debug("Refiner pipeline delete called, but no refiner pipeline present. This is not an error.")

    @property
    def default_inpainter_path(self) -> str:
        """
        Gets the default path for an auto-created inpainter
        """
        current_checkpoint_path = self.model
        default_checkpoint_name, _ = os.path.splitext(os.path.basename(DEFAULT_MODEL))
        default_xl_checkpoint_name, _ = os.path.splitext(os.path.basename(DEFAULT_SDXL_MODEL))
        checkpoint_name, ext = os.path.splitext(os.path.basename(current_checkpoint_path))

        if default_checkpoint_name == checkpoint_name:
            return DEFAULT_INPAINTING_MODEL
        elif default_xl_checkpoint_name == checkpoint_name:
            return DEFAULT_SDXL_INPAINTING_MODEL
        else:
            target_checkpoint_name = f"{checkpoint_name}-inpainting"
            return os.path.join(self.engine_checkpoints_dir, f"{target_checkpoint_name}{ext}")

    @property
    def inpainter_pipeline(self) -> EnfugueStableDiffusionPipeline:
        """
        Instantiates the inpainter pipeline.
        """
        if not hasattr(self, "_inpainter_pipeline"):
            if not self.inpainter:
                target_checkpoint_path = self.default_inpainter_path
                logger.debug(f"No inpainter explicitly set, will look for inpainter from {target_checkpoint_path}")
                target_checkpoint_path = self.check_download_model(self.engine_checkpoints_dir, target_checkpoint_path)
                if not os.path.exists(target_checkpoint_path):
                    if self.create_inpainter:
                        logger.info(f"Creating inpainting checkpoint from {self.model}")
                        self.create_inpainting_checkpoint(
                            self.model,
                            target_checkpoint_path,
                            self.is_sdxl
                        )
                    else:
                        raise ConfigurationError(f"No target inpainter, creation is disabled, and default inpainter does not exist at {target_checkpoint_path}")
                self.inpainter = target_checkpoint_path
                self.is_default_inpainter = True
            else:
                self.is_default_inpainter = False

            self.inpainter = self.check_download_model(self.engine_checkpoints_dir, self.inpainter)

            kwargs = {
                "cache_dir": self.engine_cache_dir,
                "engine_size": self.inpainter_tensorrt_size,
                "tiling_stride": self.tiling_stride,
                "torch_dtype": self.dtype,
                "requires_safety_checker": self.safe,
                "requires_aesthetic_score": False,
                "controlnets": self.inpainter_controlnets,
                "force_full_precision_vae": self.inpainter_is_sdxl and "fp16_vae" not in self.inpainter and (
                    self.inpainter_vae_name is None or "16" not in self.inpainter_vae_name
                ),
                "ip_adapter": self.ip_adapter,
                "task_callback": getattr(self, "_task_callback", None),
                "is_inpainter": True,
                "vae_preview": self.get_vae_preview(self.inpainter_is_sdxl),
                "vae": self.inpainter_vae
            }

            if self.inpainter_use_tensorrt:
                if self.inpainter_is_sdxl: # Not possible yet
                    raise ValueError(f"Sorry, TensorRT is not yet supported for SDXL.")

                if "unet" in self.TENSORRT_STAGES:
                    if not self.inpainter_controlnets and not self.TENSORRT_ALWAYS_USE_CONTROLLED_UNET:
                        kwargs["unet_engine_dir"] = self.inpainter_tensorrt_unet_dir
                    else:
                        kwargs["controlled_unet_engine_dir"] = self.inpainter_tensorrt_controlled_unet_dir

                if "vae" in self.TENSORRT_STAGES:
                    kwargs["vae_engine_dir"] = self.inpainter_tensorrt_vae_dir

                if "clip" in self.TENSORRT_STAGES:
                    kwargs["clip_engine_dir"] = self.inpainter_tensorrt_clip_dir

                self.check_create_inpainter_engine_cache()

                if not self.safe:
                    kwargs["safety_checker"] = None
                if not self.inpainter_is_sdxl:
                    kwargs["text_encoder_2"] = None
                    kwargs["tokenizer_2"] = None

                if "16" in str(self.dtype):
                    kwargs["variant"] = "fp16"
                    kwargs["build_half"] = True

                if kwargs["vae"] is None:
                    kwargs.pop("vae")

                logger.debug(
                    f"Initializing inpainter TensorRT pipeline from diffusers cache directory at {self.inpainter_diffusers_cache_dir}. Arguments are {redact_for_log(kwargs)}"
                )

                inpainter_pipeline = self.inpainter_pipeline_class.from_pretrained(
                    self.inpainter_diffusers_cache_dir,
                    local_files_only=self.offline,
                    **kwargs
                )
            elif self.inpainter_engine_cache_exists:
                if not self.safe:
                    kwargs["safety_checker"] = None
                if not self.inpainter_is_sdxl:
                    kwargs["text_encoder_2"] = None
                    kwargs["tokenizer_2"] = None
                    kwargs["text_encoder_2"] = None
                    kwargs["tokenizer_2"] = None
                if "16" in str(self.dtype):
                    kwargs["variant"] = "fp16"

                if kwargs["vae"] is None:
                    kwargs.pop("vae")
                
                logger.debug(
                    f"Initializing inpainter pipeline from diffusers cache directory at {self.inpainter_diffusers_cache_dir}. Arguments are {redact_for_log(kwargs)}"
                )

                inpainter_pipeline = self.inpainter_pipeline_class.from_pretrained(
                    self.inpainter_diffusers_cache_dir,
                    local_files_only=self.offline,
                    **kwargs
                )
            else:
                kwargs["offload_models"] = self.pipeline_sequential_onload
                logger.debug(
                    f"Initializing inpainter pipeline from checkpoint at {self.inpainter}. Arguments are {redact_for_log(kwargs)}"
                )

                inpainter_pipeline = self.inpainter_pipeline_class.from_ckpt(
                    self.inpainter, load_safety_checker=self.safe, **kwargs
                )
                if inpainter_pipeline.is_sdxl and "16" not in self.inpainter and (self.inpainter_vae_name is None or "16" not in self.inpainter_vae_name):
                    inpainter_pipeline.register_to_config(force_full_precision_vae=True)
                if self.should_cache_inpainter:
                    self.task_callback("Saving inpainter pipeline to pretrained cache")
                    inpainter_pipeline.save_pretrained(self.inpainter_diffusers_dir)
            # Load post-initialization controlnets
            for controlnet_name in self.inpainter_controlnet_names:
                if controlnet_name.startswith("sparse"):
                    inpainter_pipeline.controlnets[controlnet_name] = inpainter_pipeline.get_sparse_controlnet(
                        controlnet_name,
                        cache_dir=self.engine_controlnet_dir,
                        task_callback=self.task_callback
                    ).to(self.dtype)
            if not self.inpainter_tensorrt_is_ready:
                if self._ip_adapter_model is not None:
                    self.ip_adapter.check_download(
                        is_sdxl=self.inpainter_is_sdxl,
                        model=self._ip_adapter_model,
                        task_callback=self.task_callback,
                    )
                    inpainter_pipeline.load_ip_adapter(
                        device=self.device,
                        model=self._ip_adapter_model,
                    )
                for lora, weight in self.lora:
                    self.task_callback(f"Adding LoRA {os.path.basename(lora)} to inpainter pipeline with weight {weight}")
                    inpainter_pipeline.load_lora_weights(lora, multiplier=weight)
                for lycoris, weight in self.lycoris:
                    self.task_callback(f"Adding lycoris {os.path.basename(lycoris)} to inpainter pipeline")
                    inpainter_pipeline.load_lycoris_weights(lycoris, multiplier=weight)
                for inversion in self.inversion:
                    self.task_callback(f"Adding textual inversion {os.path.basename(inversion)} to inpainter pipeline")
                    inpainter_pipeline.load_textual_inversion(inversion)
            # load scheduler
            if self.scheduler is not None:
                logger.debug(f"Setting inpainter scheduler to {self.scheduler.__name__}") # type: ignore[attr-defined]
                inpainter_pipeline.scheduler = self.scheduler.from_config({**inpainter_pipeline.scheduler_config, **self.scheduler_config}) # type: ignore[attr-defined]
            # Check for adapter LoRA
            if any([name.startswith("sparse") for name in self.controlnet_names]):
                adapter_lora_loaded = os.path.basename(SPARSE_CONTROLNET_ADAPTER_LORA) in [
                    os.path.basename(lora) for lora, weight in self.lora
                ]
                if not adapter_lora_loaded and not self.inpainter_tensorrt_is_ready:
                    logger.debug("Sparse ControlNet detected, loading adapter LoRA.")
                    inpainter_pipeline.load_lora_weights(
                        self.check_download_model(
                            self.engine_lora_dir,
                            SPARSE_CONTROLNET_ADAPTER_LORA
                        )
                    )
            self._inpainter_pipeline = inpainter_pipeline
        return self._inpainter_pipeline

    @inpainter_pipeline.deleter
    def inpainter_pipeline(self) -> None:
        """
        Unloads the inpainter pipeline if present.
        """
        if hasattr(self, "_inpainter_pipeline"):
            logger.debug("Deleting inpainter pipeline.")
            del self._inpainter_pipeline
            self.clear_memory()
    
    @property
    def animator_pipeline(self) -> EnfugueAnimateStableDiffusionPipeline:
        """
        Instantiates the animator pipeline.
        """
        if not hasattr(self, "_animator_pipeline"):
            if self.animator is None:
                logger.info("No animator explicitly set, using base model for animator.")
                self.animator = self.model
                self.is_default_animator = True
            else:
                self.is_default_animator = False

            self.animator = self.check_download_model(self.engine_checkpoints_dir, self.animator)

            motion_module = self.motion_module
            if motion_module is None:
                if self.animator_is_sdxl:
                    motion_module = self.animator_pipeline_class.MOTION_MODULE_HOTSHOT
                else:
                    motion_module = self.animator_pipeline_class.MOTION_MODULE_V3

            motion_module = self.check_download_model(self.engine_motion_dir, motion_module)

            # Disable reloading if it was set
            self.reload_motion_module = False

            kwargs = {
                "cache_dir": self.engine_cache_dir,
                "engine_size": self.animator_tensorrt_size,
                "tiling_stride": self.tiling_stride,
                "frame_window_size": self.frame_window_size,
                "frame_window_stride": self.frame_window_stride,
                "torch_dtype": self.dtype,
                "requires_safety_checker": self.safe,
                "requires_aesthetic_score": False,
                "controlnets": self.animator_controlnets,
                "force_full_precision_vae": self.animator_is_sdxl and self.animator_vae_name not in ["xl16", VAE_XL16],
                "ip_adapter": self.ip_adapter,
                "task_callback": getattr(self, "_task_callback", None),
                "motion_module": motion_module,
                "position_encoding_truncate_length": self.position_encoding_truncate_length,
                "position_encoding_scale_length": self.position_encoding_scale_length,
                "vae_preview": self.get_vae_preview(self.animator_is_sdxl),
                "vae": self.inpainter_vae
            }

            if self.animator_use_tensorrt:
                if self.animator_is_sdxl: # Not possible yet
                    raise ValueError(f"Sorry, TensorRT is not yet supported for SDXL.")

                if "unet" in self.TENSORRT_STAGES:
                    if not self.animator_controlnets and not self.TENSORRT_ALWAYS_USE_CONTROLLED_UNET:
                        kwargs["unet_engine_dir"] = self.animator_tensorrt_unet_dir
                    else:
                        kwargs["controlled_unet_engine_dir"] = self.animator_tensorrt_controlled_unet_dir

                if "vae" in self.TENSORRT_STAGES:
                    kwargs["vae_engine_dir"] = self.animator_tensorrt_vae_dir

                if "clip" in self.TENSORRT_STAGES:
                    kwargs["clip_engine_dir"] = self.animator_tensorrt_clip_dir

                self.check_create_animator_engine_cache()

                if not self.safe:
                    kwargs["safety_checker"] = None
                if not self.animator_is_sdxl:
                    kwargs["text_encoder_2"] = None
                    kwargs["tokenizer_2"] = None
                if "16" in str(self.dtype):
                    kwargs["variant"] = "fp16"
                    kwargs["build_half"] = True

                if kwargs["vae"] is None:
                    kwargs.pop("vae")

                logger.debug(
                    f"Initializing animator TensorRT pipeline from diffusers cache directory at {self.animator_diffusers_cache_dir}. Arguments are {redact_for_log(kwargs)}"
                )

                animator_pipeline = self.animator_pipeline_class.from_pretrained(
                    self.animator_diffusers_cache_dir,
                    **kwargs
                )
            elif self.animator_engine_cache_exists:
                if not self.safe:
                    kwargs["safety_checker"] = None
                if not self.animator_is_sdxl:
                    kwargs["text_encoder_2"] = None
                    kwargs["tokenizer_2"] = None
                    kwargs["text_encoder_2"] = None
                    kwargs["tokenizer_2"] = None
                if "16" in str(self.dtype):
                    kwargs["variant"] = "fp16"

                if kwargs["vae"] is None:
                    kwargs.pop("vae")
                
                logger.debug(
                    f"Initializing animator pipeline from diffusers cache directory at {self.animator_diffusers_cache_dir}. Arguments are {redact_for_log(kwargs)}"
                )

                animator_pipeline = self.animator_pipeline_class.from_pretrained(
                    self.animator_diffusers_cache_dir,
                    **kwargs
                )
            else:
                logger.debug(
                    f"Initializing animator pipeline from checkpoint at {self.animator}. Arguments are {redact_for_log(kwargs)}"
                )

                animator_pipeline = self.animator_pipeline_class.from_ckpt(
                    self.animator, load_safety_checker=self.safe, **kwargs
                )
                if animator_pipeline.is_sdxl and self.animator_vae_name not in ["xl16", VAE_XL16]:
                    animator_pipeline.register_to_config(force_full_precision_vae=True)
                if self.should_cache_animator:
                    self.task_callback("Saving animator pipeline to pretrained cache")
                    animator_pipeline.save_pretrained(self.animator_diffusers_dir)
            # Load post-initialization controlnets
            for controlnet_name in self.animator_controlnet_names:
                if controlnet_name.startswith("sparse"):
                    animator_pipeline.controlnets[controlnet_name] = animator_pipeline.get_sparse_controlnet(
                        controlnet_name,
                        cache_dir=self.engine_controlnet_dir,
                        task_callback=self.task_callback
                    ).to(self.dtype)
            if not self.animator_tensorrt_is_ready:
                if self._ip_adapter_model is not None:
                    self.ip_adapter.check_download(
                        is_sdxl=self.animator_is_sdxl,
                        model=self._ip_adapter_model,
                        task_callback=self.task_callback,
                    )
                    animator_pipeline.load_ip_adapter(
                        device=self.device,
                        model=self._ip_adapter_model,
                    )
                for lora, weight in self.lora:
                    self.task_callback(f"Adding LoRA {os.path.basename(lora)} to animator pipeline with weight {weight}")
                    animator_pipeline.load_lora_weights(lora, multiplier=weight)
                for lycoris, weight in self.lycoris:
                    self.task_callback(f"Adding lycoris {os.path.basename(lycoris)} to animator pipeline")
                    animator_pipeline.load_lycoris_weights(lycoris, multiplier=weight)
                for inversion in self.inversion:
                    self.task_callback(f"Adding textual inversion {os.path.basename(inversion)} to animator pipeline")
                    animator_pipeline.load_textual_inversion(inversion)
            # load scheduler
            if self.scheduler is not None:
                logger.debug(f"Setting animator scheduler to {self.scheduler.__name__}") # type: ignore [attr-defined]
                animator_pipeline.scheduler = self.scheduler.from_config({**animator_pipeline.scheduler_config, **self.scheduler_config}) # type: ignore[attr-defined]
            # Check for adapter LoRA
            if any([name.startswith("sparse") for name in self.controlnet_names]):
                adapter_lora_loaded = os.path.basename(SPARSE_CONTROLNET_ADAPTER_LORA) in [
                    os.path.basename(lora) for lora, weight in self.lora
                ]
                if not adapter_lora_loaded and not self.animator_tensorrt_is_ready:
                    logger.debug("Sparse ControlNet detected, loading adapter LoRA.")
                    animator_pipeline.load_lora_weights(
                        self.check_download_model(
                            self.engine_lora_dir,
                            SPARSE_CONTROLNET_ADAPTER_LORA
                        )
                    )
            self._animator_pipeline = animator_pipeline.to(self.device)
        return self._animator_pipeline

    @animator_pipeline.deleter
    def animator_pipeline(self) -> None:
        """
        Unloads the animator pipeline if present.
        """
        if hasattr(self, "_animator_pipeline"):
            logger.debug("Deleting animator pipeline.")
            del self._animator_pipeline
            self.clear_memory()
            self.reload_motion_module = False

    # Special pipelines

    @property
    def drag_pipeline(self) -> DragAnimatorPipeline:
        """
        Gets the drag animator pipeline.
        """
        if not hasattr(self, "_drag_pipeline"):
            from enfugue.diffusion.support import DragAnimator
            from enfugue.diffusion.util import get_vram_info
            drag_pipeline = DragAnimator(
                self.engine_root,
                self.engine_motion_dir,
                device=self.device,
                dtype=self.dtype,
                offline=self.offline
            )
            drag_pipeline.task_callback = self.task_callback
            self.task_callback("Preparing DragNUWA Pipeline")
            vram_free, vram_total = get_vram_info()
            self._drag_pipeline = drag_pipeline.nuwa()
        return self._drag_pipeline

    @drag_pipeline.deleter
    def drag_pipeline(self) -> None:
        """
        Deletes the drag animator pipeline.
        """
        if hasattr(self, "_drag_pipeline"):
            logger.debug("Unloading DragNUWA pipeline.")
            del self._drag_pipeline
            self.clear_memory()

    @property
    def svd_pipeline(self, use_xt: bool = True) -> StableVideoDiffusionPipeline:
        """
        Gets the SVD pipeline
        """
        if not hasattr(self, "_svd_pipeline"):
            self._svd_pipeline = self.get_svd_pipeline(self.svd_xt)
        return self._svd_pipeline

    @svd_pipeline.deleter
    def svd_pipeline(self) -> None:
        """
        Deletes the SVD pipeline
        """
        if hasattr(self, "_svd_pipeline"):
            logger.debug("Unloading SVD pipeline.")
            del self._svd_pipeline
            self.clear_memory()

    # Functional pipeline loaders/unloaders

    def unload_pipeline(self, reason: str = "None", reset_controlnets: bool = True) -> None:
        """
        Calls the pipeline deleter.
        """
        if hasattr(self, "_pipeline"):
            logger.debug(f'Unloading pipeline for reason "{reason}"')
            del self.pipeline
            if reset_controlnets:
                self.controlnets = None # type: ignore[assignment]

    def offload_pipeline(self, intention: Optional[Literal["inpainting", "refining"]] = None) -> None:
        """
        Offloads the pipeline to CPU if present.
        """
        if hasattr(self, "_pipeline"):
            if self.pipeline_switch_mode == "unload":
                logger.debug("Offloading is disabled, unloading pipeline.")
                self.unload_pipeline("switching modes" if not intention else f"switching to {intention}")
            elif self.pipeline_switch_mode is None:
                logger.debug("Offloading is disabled, keeping pipeline in memory.")
            elif intention == "inpainting" and hasattr(self, "_inpainter_pipeline"):
                logger.debug("Swapping inpainter out of CPU and pipeline into CPU")
                self.swap_pipelines(self._inpainter_pipeline, self._pipeline)
            elif intention == "refining" and hasattr(self, "_refiner_pipeline"):
                logger.debug("Swapping refiner out of CPU and pipeline into CPU")
                self.swap_pipelines(self._refiner_pipeline, self._pipeline)
            else:
                import torch
                logger.debug("Offloading pipeline to CPU.")
                self._pipeline = self._pipeline.to("cpu") # type: ignore[attr-defined]
            self.clear_memory()

    def unload_refiner(self, reason: str = "None", reset_controlnets: bool = True) -> None:
        """
        Calls the refiner deleter.
        """
        if hasattr(self, "_refiner_pipeline"):
            logger.debug(f'Unloading refiner pipeline for reason "{reason}"')
            del self.refiner_pipeline
            if reset_controlnets:
                self.refiner_controlnets = None # type: ignore[assignment]

    def offload_refiner(self, intention: Optional[Literal["inpainting", "inference"]] = None) -> None:
        """
        Offloads the pipeline to CPU if present.
        """
        if hasattr(self, "_refiner_pipeline"):
            if self.pipeline_switch_mode == "unload":
                logger.debug("Offloading is disabled, unloading refiner pipeline.")
                self.unload_refiner("switching modes" if not intention else f"switching to {intention}")
            elif self.pipeline_switch_mode is None:
                logger.debug("Offloading is disabled, keeping refiner pipeline in memory.")
            elif intention == "inference" and hasattr(self, "_pipeline"):
                logger.debug("Swapping pipeline out of CPU and refiner into CPU")
                self.swap_pipelines(self._pipeline, self._refiner_pipeline)
            elif intention == "inpainting" and hasattr(self, "_inpainter_pipeline"):
                logger.debug("Swapping inpainter out of CPU and refiner into CPU")
                self.swap_pipelines(self._inpainter_pipeline, self._refiner_pipeline)
            else:
                import torch
                logger.debug("Offloading refiner to CPU")
                self._refiner_pipeline = self._refiner_pipeline.to("cpu") # type: ignore[attr-defined]
            self.clear_memory()

    def unload_inpainter(self, reason: str = "None", reset_controlnets: bool = True) -> None:
        """
        Calls the inpainter deleter.
        """
        if hasattr(self, "_inpainter_pipeline"):
            logger.debug(f'Unloading inpainter pipeline for reason "{reason}"')
            del self.inpainter_pipeline
            if reset_controlnets:
                self.inpainter_controlnets = None # type: ignore[assignment]

    def offload_inpainter(self, intention: Optional[Literal["inference", "refining"]] = None) -> None:
        """
        Offloads the pipeline to CPU if present.
        """
        if hasattr(self, "_inpainter_pipeline"):
            import torch
            
            if self.pipeline_switch_mode == "unload":
                logger.debug("Offloading is disabled, unloading inpainter pipeline.")
                self.unload_inpainter("switching modes" if not intention else f"switching to {intention}")
            elif self.pipeline_switch_mode is None:
                logger.debug("Offloading is disabled, keeping inpainter pipeline in memory.")
            elif intention == "inference" and hasattr(self, "_pipeline"):
                logger.debug("Swapping pipeline out of CPU and inpainter into CPU")
                self.swap_pipelines(self._pipeline, self._inpainter_pipeline)
            elif intention == "refining" and hasattr(self, "_refiner_pipeline"):
                logger.debug("Swapping refiner out of CPU and inpainter into CPU")
                self.swap_pipelines(self._refiner_pipeline, self._inpainter_pipeline)
            else:
                import torch
                logger.debug("Offloading inpainter to CPU")
                self._inpainter_pipeline = self._inpainter_pipeline.to("cpu") # type: ignore[attr-defined]
            self.clear_memory()

    def unload_animator(self, reason: str = "None", reset_controlnets: bool = True) -> None:
        """
        Calls the animator deleter.
        """
        if hasattr(self, "_animator_pipeline"):
            logger.debug(f'Unloading animator pipeline for reason "{reason}"')
            del self.animator_pipeline
            if reset_controlnets:
                self.animator_controlnets = None # type: ignore[assignment]

    def offload_animator(self, intention: Optional[Literal["inference", "inpainting", "refining"]] = None) -> None:
        """
        Offloads the pipeline to CPU if present.
        """
        if hasattr(self, "_animator_pipeline"):
            import torch
            
            if self.pipeline_switch_mode == "unload":
                logger.debug("Offloading is disabled, unloading animator pipeline.")
                self.unload_animator("switching modes" if not intention else f"switching to {intention}")
            elif self.pipeline_switch_mode is None:
                logger.debug("Offloading is disabled, keeping animator pipeline in memory.")
            elif intention == "inference" and hasattr(self, "_pipeline"):
                logger.debug("Swapping pipeline out of CPU and animator into CPU")
                self.swap_pipelines(self._pipeline, self._animator_pipeline)
            elif intention == "inpainting" and hasattr(self, "_inpainter_pipeline"):
                logger.debug("Swapping inpainter out of CPU and animator into CPU")
                self.swap_pipelines(self._inpainter_pipeline, self._animator_pipeline)
            elif intention == "refining" and hasattr(self, "_refiner_pipeline"):
                logger.debug("Swapping refiner out of CPU and animator into CPU")
                self.swap_pipelines(self._refiner_pipeline, self._animator_pipeline)
            else:
                import torch
                logger.debug("Offloading animator to CPU")
                self._animator_pipeline = self._animator_pipeline.to("cpu") # type: ignore[attr-defined]
            self.clear_memory()

    def offload_all(self) -> None:
        """
        Offloads pipelines that are present.
        """
        self.offload_pipeline()
        self.offload_refiner()
        self.offload_inpainter()
        self.offload_animator()

    @property
    def upscaler(self) -> Upscaler:
        """
        Gets the GAN upscaler
        """
        if not hasattr(self, "_upscaler"):
            from enfugue.diffusion.support.upscale import Upscaler
            self._upscaler = Upscaler(
                self.engine_root,
                self.engine_upscale_dir,
                device=self.device,
                dtype=self.dtype,
                offline=self.offline
            )
            self._upscaler.task_callback = self.task_callback
        return self._upscaler

    @property
    def control_image_processor(self) -> ControlImageProcessor:
        """
        Gets the processor for control images
        """
        if not hasattr(self, "_control_image_processor"):
            from enfugue.diffusion.support import ControlImageProcessor
            self._control_image_processor = ControlImageProcessor(
                self.engine_root,
                self.engine_detection_dir,
                device=self.device,
                dtype=self.dtype,
                offline=self.offline
            )
            self._control_image_processor.task_callback = self.task_callback
        return self._control_image_processor

    @property
    def background_remover(self) -> BackgroundRemover:
        """
        Gets the processor for removing backgrounds
        """
        if not hasattr(self, "_background_remover"):
            from enfugue.diffusion.support import BackgroundRemover
            self._background_remover = BackgroundRemover(
                self.engine_root,
                self.engine_detection_dir,
                device=self.device,
                dtype=self.dtype,
                offline=self.offline
            )
            self._background_remover.task_callback = self.task_callback
        return self._background_remover

    @property
    def ip_adapter(self) -> IPAdapter:
        """
        Gets the IP adapter.
        """
        if not hasattr(self, "_ip_adapter"):
            from enfugue.diffusion.support import IPAdapter
            self._ip_adapter = IPAdapter(
                self.engine_root,
                self.engine_ip_adapter_dir,
                device=self.device,
                dtype=self.dtype,
                offline=self.offline,
                clip_vision_dir=self.engine_clip_vision_dir,
            )
            self._ip_adapter.task_callback = self.task_callback
        return self._ip_adapter

    @property
    def conversation(self) -> Conversation:
        """
        Gets an LLM conversation.
        """
        if not hasattr(self, "_conversation"):
            from enfugue.diffusion.support import Conversation
            self._conversation = Conversation(
                self.engine_root,
                self.engine_language_dir,
                device=self.device,
                dtype=self.dtype,
                offline=self.offline
            )
            self._conversation.task_callback = self.task_callback
        return self._conversation

    @property
    def interpolator(self) -> Interpolator:
        """
        Gets the interpolator.
        """
        if not hasattr(self, "_interpolator"):
            from enfugue.diffusion.support import Interpolator
            self._interpolator = Interpolator(
                self.engine_root,
                self.engine_interpolation_dir,
                device=self.device,
                dtype=self.dtype,
                offline=self.offline
            )
            self._interpolator.task_callback = self.task_callback
        return self._interpolator

    @property
    def unimatch(self) -> Unimatch:
        """
        Gets the unimatch.
        """
        if not hasattr(self, "_unimatch"):
            from enfugue.diffusion.support import Unimatch
            self._unimatch = Unimatch(
                self.engine_root,
                self.engine_detection_dir,
                device=self.device,
                dtype=self.dtype,
                offline=self.offline
            )
            self._unimatch.task_callback = self.task_callback
        return self._unimatch

    # Diffusers model getters

    def get_vae_path(self, vae: Optional[str] = None) -> Optional[str]:
        """
        Gets the path to the VAE repository based on the passed path or key
        """
        if vae == "ema":
            return VAE_EMA
        elif vae == "mse":
            return VAE_MSE
        elif vae == "xl":
            return VAE_XL
        elif vae == "xl16":
            return VAE_XL16
        elif vae == "consistency":
            return VAE_CONSISTENCY
        return vae

    def check_default_vae(self, vae: str) -> str:
        """
        Gets a default VAE URL
        """
        basename = os.path.basename(vae)
        for default in [VAE_MSE, VAE_EMA, VAE_XL, VAE_XL16, VAE_CONSISTENCY]:
            if get_file_name_from_url(default) == basename:
                return default
        return vae

    def get_xl_vae(self, vae: str) -> AutoencoderKL:
        """
        Loads an XL VAE from file or dies trying
        """
        from diffusers.models import AutoencoderKL
        from enfugue.diffusion.util.torch_util import load_state_dict

        vae_config = os.path.join(self.engine_cache_dir, "sdxl-vae-config.json")
        check_download(
            "https://huggingface.co/stabilityai/sdxl-vae/raw/main/config.json",
            vae_config
        )
        vae_model = AutoencoderKL.from_config(
            AutoencoderKL._dict_from_json_file(vae_config)
        )
        vae_model.load_state_dict(load_state_dict(vae), strict=False)
        return vae_model.to(self.device)

    def get_vae(
        self,
        vae: Optional[str] = None
    ) -> Optional[Union[AutoencoderKL, ConsistencyDecoderVAE]]:
        """
        Loads the VAE
        """
        if vae is None:
            return None

        if "consisten" in vae.lower():
            from diffusers.models import ConsistencyDecoderVAE
            vae_model = ConsistencyDecoderVAE
        else:
            from diffusers.models import AutoencoderKL
            vae_model = AutoencoderKL

        try:
            result = vae_model.from_single_file(
                vae,
                torch_dtype=self.dtype,
                cache_dir=self.engine_cache_dir,
                from_safetensors="safetensors" in vae
            )
        except KeyError as ex:
            logger.debug(f"Received KeyError on '{ex}' when instantiating VAE from single file, trying to use XL VAE loader fix.")
            result = self.get_xl_vae(vae)

        return result

    def get_vae_preview(self, use_xl: bool) -> AutoencoderTiny:
        """
        Gets a previewer VAE (tiny)
        """
        from diffusers.models import AutoencoderTiny
        from enfugue.diffusion.util.torch_util import load_state_dict
        url = VAE_PREVIEW_XL if use_xl else VAE_PREVIEW
        path = self.check_download_model(self.engine_vae_approx_dir, url)
        vae_config = os.path.join(self.engine_cache_dir, "taesd-config.json")
        check_download(
            "https://huggingface.co/madebyollin/taesd/raw/main/config.json",
            vae_config
        )
        vae_model = AutoencoderTiny.from_config(
            AutoencoderTiny._dict_from_json_file(vae_config)
        )
        vae_model.load_state_dict(load_state_dict(path), strict=False)
        return vae_model.to(device=self.device, dtype=self.dtype)

    def get_scheduler_class(
        self,
        scheduler: Optional[SCHEDULER_LITERAL]
    ) -> Optional[
        Union[
            Type,
            Tuple[Type, Dict[str, Any]]
        ]
    ]:
        """
        Sets the scheduler class
        """
        kwargs: Dict[str, Any] = {}
        if not scheduler:
            return None
        elif scheduler in ["dpmsm", "dpmsms", "dpmsmk", "dpmsmka"]:
            from diffusers.schedulers import DPMSolverMultistepScheduler
            if scheduler in ["dpmsms", "dpmsmka"]:
                kwargs["algorithm_type"] = "sde-dpmsolver++"
            if scheduler in ["dpmsmk", "dpmsmka"]:
                kwargs["use_karras_sigmas"] = True
            return (DPMSolverMultistepScheduler, kwargs)
        elif scheduler in ["dpmss", "dpmssk"]:
            from diffusers.schedulers import DPMSolverSinglestepScheduler
            if scheduler == "dpmssk":
                kwargs["use_karras_sigmas"] = True
            return (DPMSolverSinglestepScheduler, kwargs)
        elif scheduler == "heun":
            from diffusers.schedulers import HeunDiscreteScheduler
            return HeunDiscreteScheduler
        elif scheduler in ["dpmd", "dpmdk"]:
            from diffusers.schedulers import KDPM2DiscreteScheduler
            if scheduler == "dpmdk":
                kwargs["use_karras_sigmas"] = True
            return (KDPM2DiscreteScheduler, kwargs)
        elif scheduler in ["adpmd", "adpmdk"]:
            from diffusers.schedulers import KDPM2AncestralDiscreteScheduler
            if scheduler == "adpmdk":
                kwargs["use_karras_sigmas"] = True
            return (KDPM2AncestralDiscreteScheduler, kwargs)
        elif scheduler in ["lmsd", "lmsdk"]:
            from diffusers.schedulers import LMSDiscreteScheduler
            if scheduler == "lmsdk":
                kwargs["use_karras_sigmas"] = True
            return (LMSDiscreteScheduler, kwargs)
        elif scheduler == "ddim":
            from diffusers.schedulers import DDIMScheduler
            return DDIMScheduler
        elif scheduler == "ddpm":
            from diffusers.schedulers import DDPMScheduler
            return DDPMScheduler
        elif scheduler == "deis":
            from diffusers.schedulers import DEISMultistepScheduler
            return DEISMultistepScheduler
        elif scheduler == "dpmsde":
            from diffusers.schedulers import DPMSolverSDEScheduler
            return DPMSolverSDEScheduler
        elif scheduler == "unipc":
            from diffusers.schedulers import UniPCMultistepScheduler
            return UniPCMultistepScheduler
        elif scheduler == "pndm":
            from diffusers.schedulers import PNDMScheduler
            return PNDMScheduler
        elif scheduler in ["eds", "edsk"]:
            from diffusers.schedulers import EulerDiscreteScheduler
            if scheduler == "edsk":
                kwargs["use_karras_sigmas"] = True
            return (EulerDiscreteScheduler, kwargs)
        elif scheduler == "eads":
            from diffusers.schedulers import EulerAncestralDiscreteScheduler
            return EulerAncestralDiscreteScheduler
        elif scheduler == "lcm":
            from diffusers.schedulers import LCMScheduler
            return LCMScheduler
        raise ValueError(f"Unknown scheduler {scheduler}")

    def get_svd_pipeline(self, use_xt: bool = True) -> StableVideoDiffusionPipeline:
        """
        Gets an SVD pipeline. This should eventually not be separate.
        """
        from diffusers import StableVideoDiffusionPipeline
        path = "stabilityai/stable-video-diffusion-img2vid-xt" if use_xt else "stabilityai/stable-video-diffusion-img2vid"
        self.task_callback(f"Initializing SVD pipeline from {path}")
        pipe = StableVideoDiffusionPipeline.from_pretrained(
            path,
            torch_dtype=self.dtype,
            cache_dir=self.engine_cache_dir,
            variant="fp16"
        )
        pipe.enable_model_cpu_offload()
        return pipe.to(self.device)

    def get_xl_controlnet(self, controlnet: str) -> ControlNetModel:
        """
        Loads an XL ControlNet from file or dies trying
        """
        from diffusers.models import ControlNetModel
        from enfugue.diffusion.util.torch_util import load_state_dict

        controlnet_config = os.path.join(self.engine_cache_dir, "controlnet-xl-config.json")
        check_download(
            "https://huggingface.co/diffusers/controlnet-canny-sdxl-1.0/raw/main/config.json",
            controlnet_config
        )
        controlnet_model = ControlNetModel.from_config(
            ControlNetModel._dict_from_json_file(controlnet_config)
        )
        state_dict = load_state_dict(controlnet)
        controlnet_model.load_state_dict(state_dict, strict=False)
        del state_dict
        return controlnet_model.to(self.device, self.dtype)

    def get_controlnet(self, controlnet: Optional[str] = None) -> Optional[ControlNetModel]:
        """
        Loads a controlnet
        """
        if controlnet is None:
            return None

        from diffusers.models import ControlNetModel
        from enfugue.diffusion.util.torch_util import load_state_dict

        find_controlnet = self.check_download_model(self.engine_controlnet_dir, controlnet)
        if not find_controlnet:
            raise ValueError(f"ControlNet path {controlnet} is not a file that can be accessed, a URL that can be downloaded or a repository that can be cloned.")
        try:
            self.task_callback(f"Loading ControlNet from file {find_controlnet}")
            controlnet_config = os.path.join(self.engine_cache_dir, "controlnet-config.json")
            check_download(
                "https://huggingface.co/lllyasviel/control_v11p_sd15_canny/raw/main/config.json",
                controlnet_config
            )
            controlnet_model = ControlNetModel.from_config(
                ControlNetModel._dict_from_json_file(controlnet_config)
            )
            state_dict = load_state_dict(find_controlnet)
            controlnet_model.load_state_dict(state_dict, strict=False)
            del state_dict
            return controlnet_model.to(self.device, self.dtype)
        except (RuntimeError, KeyError):
            return self.get_xl_controlnet(find_controlnet)
    
    def get_default_controlnet_path_by_name(
        self,
        name: CONTROLNET_LITERAL,
        is_sdxl: bool
    ) -> str:
        """
        Gets the default controlnet path based on pipeline type
        """
        if is_sdxl:
            if name == "canny":
                return CONTROLNET_CANNY_XL
            elif name == "depth":
                return CONTROLNET_DEPTH_XL
            elif name == "pidi":
                return CONTROLNET_PIDI_XL
            elif name == "pose":
                return CONTROLNET_POSE_XL
            elif name == "qr":
                return CONTROLNET_QR_XL
            else:
                raise ValueError(f"Sorry, ControlNet “{name}” is not yet supported by SDXL. Check back soon!")
        else:
            if name == "canny":
                return CONTROLNET_CANNY
            elif name == "mlsd":
                return CONTROLNET_MLSD
            elif name == "hed":
                return CONTROLNET_HED
            elif name == "tile":
                return CONTROLNET_TILE
            elif name == "scribble":
                return CONTROLNET_SCRIBBLE
            elif name == "inpaint":
                return CONTROLNET_INPAINT
            elif name == "depth":
                return CONTROLNET_DEPTH
            elif name == "normal":
                return CONTROLNET_NORMAL
            elif name == "pose":
                return CONTROLNET_POSE
            elif name == "line":
                return CONTROLNET_LINE
            elif name == "anime":
                return CONTROLNET_ANIME
            elif name == "pidi":
                return CONTROLNET_PIDI
            elif name == "temporal":
                return CONTROLNET_TEMPORAL
            elif name == "qr":
                return CONTROLNET_QR
        raise ValueError(f"Unknown or unsupported ControlNet {name}")

    def get_controlnet_path_by_name(self, name: CONTROLNET_LITERAL, is_sdxl: bool) -> str:
        """
        Gets a Controlnet path by name, based on current config.
        """
        key_parts = ["enfugue", "controlnet"]
        if is_sdxl:
            key_parts += ["xl"]
        key_parts += [name]
        configured_path = self.configuration.get(".".join(key_parts), None)
        if not configured_path:
            return self.get_default_controlnet_path_by_name(name, is_sdxl)
        return configured_path

    @property
    def controlnets(self) -> Dict[str, ControlNetModel]:
        """
        Gets the configured controlnets for the main pipeline
        """
        if not hasattr(self, "_controlnets"):
            self._controlnets = {}

            for controlnet_name in self.controlnet_names:
                if controlnet_name.startswith("sparse"):
                    continue
                self._controlnets[controlnet_name] = self.get_controlnet(
                    self.get_controlnet_path_by_name(controlnet_name, self.is_sdxl)
                )
        return self._controlnets # type: ignore[return-value]

    @controlnets.deleter
    def controlnets(self) -> None:
        """
        Removes current controlnets and clears memory
        """
        if hasattr(self, "_controlnets"):
            del self._controlnets
            self.clear_memory()

    @controlnets.setter
    def controlnets(
        self,
        *new_controlnets: Optional[Union[CONTROLNET_LITERAL, List[CONTROLNET_LITERAL], Set[CONTROLNET_LITERAL]]],
    ) -> None:
        """
        Sets a new list of controlnets (optional)
        """
        controlnet_names: Set[CONTROLNET_LITERAL] = set()

        for arg in new_controlnets:
            if arg is None:
                break
            if isinstance(arg, str):
                controlnet_names.add(arg)
            else:
                controlnet_names = controlnet_names.union(arg) # type: ignore[arg-type]

        existing_controlnet_names = self.controlnet_names
        if controlnet_names == existing_controlnet_names:
            return # No changes

        logger.debug(f"Setting main pipeline ControlNet(s) to {controlnet_names} from {existing_controlnet_names}")
        self._controlnet_names = controlnet_names

        if not hasattr(self, "_controlnets"):
            self._controlnets = {}

        if getattr(self, "_pipeline", None) is not None and any([name.startswith("sparse") for name in (controlnet_names - existing_controlnet_names)]):
            self.unload_pipeline("Adding sparse ControlNet", False)

        for controlnet_name in controlnet_names.union(existing_controlnet_names):
            if controlnet_name not in controlnet_names:
                old_cnet = self._controlnets.pop(controlnet_name, None)
                del old_cnet # Help the garbage collector
            elif controlnet_name not in self._controlnets:
                if controlnet_name.startswith("sparse"):
                    continue
                self._controlnets[controlnet_name] = self.get_controlnet(
                    self.get_controlnet_path_by_name(controlnet_name, self.is_sdxl)
                )

        self.clear_memory()
        if getattr(self, "_pipeline", None) is not None:
            self._pipeline.controlnets = self.controlnets

    @property
    def inpainter_controlnets(self) -> Dict[str, ControlNetModel]:
        """
        Gets the configured controlnets for the inpainter
        """
        if not hasattr(self, "_inpainter_controlnets"):
            self._inpainter_controlnets = {}

            for controlnet_name in self.inpainter_controlnet_names:
                if controlnet_name.startswith("sparse"):
                    continue
                self._inpainter_controlnets[controlnet_name] = self.get_controlnet(
                    self.get_controlnet_path_by_name(controlnet_name, self.inpainter_is_sdxl)
                )
        return self._inpainter_controlnets # type: ignore[return-value]

    @inpainter_controlnets.deleter
    def inpainter_controlnets(self) -> None:
        """
        Removes current inpainter controlnets and clears memory
        """
        if hasattr(self, "_inpainter_controlnets"):
            del self._inpainter_controlnets
            self.clear_memory()

    @inpainter_controlnets.setter
    def inpainter_controlnets(
        self,
        *new_inpainter_controlnets: Optional[Union[CONTROLNET_LITERAL, List[CONTROLNET_LITERAL], Set[CONTROLNET_LITERAL]]],
    ) -> None:
        """
        Sets a new list of inpainter controlnets (optional)
        """
        controlnet_names: Set[CONTROLNET_LITERAL] = set()

        for arg in new_inpainter_controlnets:
            if arg is None:
                break
            if isinstance(arg, str):
                controlnet_names.add(arg)
            else:
                controlnet_names = controlnet_names.union(arg) # type: ignore[arg-type]

        existing_controlnet_names = self.inpainter_controlnet_names

        if controlnet_names == existing_controlnet_names:
            return # No changes

        logger.debug(f"Setting inpainter pipeline ControlNet(s) to {controlnet_names} from {existing_controlnet_names}")
        self._inpainter_controlnet_names = controlnet_names

        if not hasattr(self, "_inpainter_controlnets"):
            self._inpainter_controlnets = {}

        if getattr(self, "_inpainter_pipeline", None) is not None and any([name.startswith("sparse") for name in (controlnet_names - existing_controlnet_names)]):
            self.unload_inpainter("Adding sparse ControlNet", False)

        for controlnet_name in controlnet_names.union(existing_controlnet_names):
            if controlnet_name not in controlnet_names:
                old_cnet = self._inpainter_controlnets.pop(controlnet_name, None)
                del old_cnet
            elif controlnet_name not in self._inpainter_controlnets:
                if controlnet_name.startswith("sparse"):
                    continue
                self._inpainter_controlnets[controlnet_name] = self.get_controlnet(
                    self.get_controlnet_path_by_name(controlnet_name, self.inpainter_is_sdxl)
                )

        self.clear_memory()
        if getattr(self, "_inpainter_pipeline", None) is not None:
            self._inpainter_pipeline.controlnets = self.inpainter_controlnets

    @property
    def animator_controlnets(self) -> Dict[str, ControlNetModel]:
        """
        Gets the configured controlnets for the animator
        """
        if not hasattr(self, "_animator_controlnets"):
            self._animator_controlnets = {}

            for controlnet_name in self.animator_controlnet_names:
                if controlnet_name.startswith("sparse"):
                    continue
                self._animator_controlnets[controlnet_name] = self.get_controlnet(
                    self.get_controlnet_path_by_name(controlnet_name, self.animator_is_sdxl)
                )
        return self._animator_controlnets # type: ignore[return-value]

    @animator_controlnets.deleter
    def animator_controlnets(self) -> None:
        """
        Removes current animator controlnets and clears memory
        """
        if hasattr(self, "_animator_controlnets"):
            del self._animator_controlnets
            self.clear_memory()

    @animator_controlnets.setter
    def animator_controlnets(
        self,
        *new_animator_controlnets: Optional[Union[CONTROLNET_LITERAL, List[CONTROLNET_LITERAL], Set[CONTROLNET_LITERAL]]],
    ) -> None:
        """
        Sets a new list of animator controlnets (optional)
        """
        controlnet_names: Set[CONTROLNET_LITERAL] = set()

        for arg in new_animator_controlnets:
            if arg is None:
                break
            if isinstance(arg, str):
                controlnet_names.add(arg)
            else:
                controlnet_names = controlnet_names.union(arg) # type: ignore[arg-type]

        existing_controlnet_names = self.animator_controlnet_names

        if controlnet_names == existing_controlnet_names:
            return # No changes

        logger.debug(f"Setting animator pipeline ControlNet(s) to {controlnet_names} from {existing_controlnet_names}")
        self._animator_controlnet_names = controlnet_names

        if not hasattr(self, "_animator_controlnets"):
            self._animator_controlnets = {}

        if getattr(self, "_animator_pipeline", None) is not None and any([name.startswith("sparse") for name in (controlnet_names - existing_controlnet_names)]):
            self.unload_animator("Adding sparse ControlNet", False)

        for controlnet_name in controlnet_names.union(existing_controlnet_names):
            if controlnet_name not in controlnet_names:
                old_cnet = self._animator_controlnets.pop(controlnet_name, None)
                del old_cnet
            elif controlnet_name not in self._animator_controlnets:
                if controlnet_name.startswith("sparse"):
                    continue
                self._animator_controlnets[controlnet_name] = self.get_controlnet(
                    self.get_controlnet_path_by_name(controlnet_name, self.animator_is_sdxl)
                )

        self.clear_memory()
        if getattr(self, "_animator_pipeline", None) is not None:
            self._animator_pipeline.controlnets = self.animator_controlnets

    @property
    def refiner_controlnets(self) -> Dict[str, ControlNetModel]:
        """
        Gets the configured controlnets for the refiner
        """
        if not hasattr(self, "_refiner_controlnets"):
            self._refiner_controlnets = {}

            for controlnet_name in self.refiner_controlnet_names:
                self._refiner_controlnets[controlnet_name] = self.get_controlnet(
                    self.get_controlnet_path_by_name(controlnet_name, self.refiner_is_sdxl)
                )
        return self._refiner_controlnets # type: ignore[return-value]

    @refiner_controlnets.deleter
    def refiner_controlnets(self) -> None:
        """
        Removes current refiner controlnets and clears memory
        """
        if hasattr(self, "_refiner_controlnets"):
            del self._refiner_controlnets
            self.clear_memory()

    @refiner_controlnets.setter
    def refiner_controlnets(
        self,
        *new_refiner_controlnets: Optional[Union[CONTROLNET_LITERAL, List[CONTROLNET_LITERAL], Set[CONTROLNET_LITERAL]]],
    ) -> None:
        """
        Sets a new list of refiner controlnets (optional)
        """
        controlnet_names: Set[CONTROLNET_LITERAL] = set()

        for arg in new_refiner_controlnets:
            if arg is None:
                break
            if isinstance(arg, str):
                controlnet_names.add(arg)
            else:
                controlnet_names = controlnet_names.union(arg) # type: ignore[arg-type]

        existing_controlnet_names = self.refiner_controlnet_names

        if controlnet_names == existing_controlnet_names:
            return # No changes

        logger.debug(f"Setting refiner pipeline ControlNet(s) to {controlnet_names} from {existing_controlnet_names}")
        self._refiner_controlnet_names = controlnet_names

        if not hasattr(self, "_refiner_controlnets"):
            self._refiner_controlnets = {}

        if getattr(self, "_refiner_pipeline", None) is not None and any([name.startswith("sparse") for name in (controlnet_names - existing_controlnet_names)]):
            self.unload_refiner("Adding sparse ControlNet", False)

        for controlnet_name in controlnet_names.union(existing_controlnet_names):
            if controlnet_name not in controlnet_names:
                old_cnet = self._refiner_controlnets.pop(controlnet_name, None)
                del old_cnet
            elif controlnet_name not in self._refiner_controlnets:
                if controlnet_name.startswith("sparse"):
                    continue
                self._refiner_controlnets[controlnet_name] = self.get_controlnet(
                    self.get_controlnet_path_by_name(controlnet_name, self.refiner_is_sdxl)
                )

        self.clear_memory()
        if getattr(self, "_refiner_pipeline", None) is not None:
            self._refiner_pipeline.controlnets = self.refiner_controlnets

    @property
    def controlnet_names(self) -> Set[CONTROLNET_LITERAL]:
        """
        Gets the name of the control net, if one was set.
        """
        return getattr(self, "_controlnet_names", set())

    @property
    def inpainter_controlnet_names(self) -> Set[CONTROLNET_LITERAL]:
        """
        Gets the name of the control net, if one was set.
        """
        return getattr(self, "_inpainter_controlnet_names", set())

    @property
    def animator_controlnet_names(self) -> Set[CONTROLNET_LITERAL]:
        """
        Gets the name of the control net, if one was set.
        """
        return getattr(self, "_animator_controlnet_names", set())

    @property
    def refiner_controlnet_names(self) -> Set[CONTROLNET_LITERAL]:
        """
        Gets the name of the control net, if one was set.
        """
        return getattr(self, "_refiner_controlnet_names", set())

    def dragnuwa_img2vid(
        self,
        image: Union[str, PIL.Image.Image],
        motion_vectors: List[List[MotionVectorPointDict]],
        optical_flow: Dict[OPTICAL_FLOW_METHOD_LITERAL, List[List[PIL.Image.Image]]]={},
        motion_vector_repeat_window: bool=False,
        decode_chunk_size: Optional[int]=1,
        num_frames: int=14,
        frame_window_size: int=14,
        num_inference_steps: int=25,
        min_guidance_scale: float=1.0,
        max_guidance_scale: float=3.0,
        fps: int=4,
        motion_bucket_id: int=27,
        noise_aug_strength: float=0.02,
        gaussian_sigma: int=20,
        task_callback: Optional[Callable[[str], None]]=None,
        progress_callback: Optional[Callable[[int, int, float], None]]=None,
        image_callback: Optional[Callable[[List[PIL.Image.Image]], None]]=None,
        image_callback_steps: Optional[int]=None,
        **kwargs: Any
    ) -> List[PIL.Image.Image]:
        """
        Gets a Stable Video Diffusion (SVD) pipeline and executes it.
        """
        if task_callback is None:
            task_callback = lambda arg: None

        self.set_task_callback(task_callback)
        self.offload_all() # Send any active diffusion pipelines to CPU
        del self.svd_pipeline # Also unload this
        self.start_keepalive()

        try:
            if isinstance(image, str):
                from enfugue.util import image_from_uri
                image = image_from_uri(image)

            latent_callback: Optional[Callable[[Tensor, int], None]] = None
            num_iterations = ceil(num_frames / frame_window_size)
            last_iteration = 0
            num_returned_images = num_frames - num_iterations + 1
            animation_preview_images: List[PIL.Image.Image] = [
                image.copy()
                for i in range(num_returned_images)
            ]

            if image_callback is not None:
                # Build decoding callback
                from diffusers.image_processor import VaeImageProcessor
                vae_preview = self.get_vae_preview(False).to(device=self.device)
                image_processor = VaeImageProcessor()

                def decode_svd_latents(latents, iteration):
                    nonlocal last_iteration
                    import numpy as np
                    from einops import rearrange
                    from torchvision import utils
                    cond, uncond = latents.chunk(2)
                    cond = cond.unsqueeze(0)
                    preview_decoded = torch.cat([
                        vae_preview.decode(
                            cond[:, i, :, :, :],
                            return_dict=False
                        )[0].to(self.device).unsqueeze(1)
                        for i in range(cond.shape[1])
                    ], dim=1)
                    preview_decoded = (preview_decoded / 2 + 0.5).clamp(0, 0.98)
                    preview_decoded = rearrange(preview_decoded, "b f c h w -> f b c h w")
                    images = []
                    image_count = 0
                    for frame in preview_decoded:
                        frame = utils.make_grid(frame, nrow=8)
                        frame = frame.transpose(0, 1).transpose(1, 2).squeeze(-1)
                        frame = (255 - (frame * 255)).cpu().numpy().astype(np.uint8)
                        images.extend(image_processor.numpy_to_pil(frame))
                        image_count += 1

                    start_index = (frame_window_size * iteration) - iteration
                    for i in range(start_index, num_returned_images):
                        image_index = i - start_index
                        if image_index >= image_count:
                            image_index = image_count - 1
                        animation_preview_images[i] = images[image_index]

                    image_callback(animation_preview_images)
                    last_iteration = iteration

                latent_callback = decode_svd_latents

            width, height = image.size
            pipeline = self.drag_pipeline
            self.stop_keepalive()
            task_callback("Executing Inference")

            return pipeline(
                image,
                width=width,
                height=height,
                fps=fps,
                seed=self.seed,
                num_frames=num_frames,
                motion_vectors=motion_vectors,
                motion_vector_repeat_window=motion_vector_repeat_window,
                motion_bucket_id=motion_bucket_id,
                gaussian_sigma=gaussian_sigma,
                noise_aug_strength=noise_aug_strength,
                num_inference_steps=num_inference_steps,
                min_guidance_scale=min_guidance_scale,
                max_guidance_scale=max_guidance_scale,
                optical_flow=optical_flow,
                progress_callback=progress_callback,
                latent_callback=latent_callback,
                latent_callback_steps=image_callback_steps
            )[0]
        finally:
            self.clear_task_callback()
            self.stop_keepalive()

    def svd_img2vid(
        self,
        image: Union[str, PIL.Image.Image],
        use_xt: bool = False,
        num_frames: int=14,
        frame_window_size: int=14,
        decode_chunk_size: Optional[int] = 1,
        num_inference_steps: int = 25,
        min_guidance_scale: float = 1.0,
        max_guidance_scale: float = 3.0,
        fps: int = 7,
        motion_bucket_id: int = 127,
        noise_aug_strength: float = 0.02,
        task_callback: Optional[Callable[[str], None]] = None,
        progress_callback: Optional[Callable[[int, int, float], None]] = None,
        image_callback: Optional[Callable[[List[PIL.Image.Image]], None]] = None,
        image_callback_steps: Optional[int] = None,
        **kwargs: Any
    ) -> List[PIL.Image.Image]:
        """
        Gets a Stable Video Diffusion (SVD) pipeline and executes it.
        """
        if task_callback is None:
            task_callback = lambda arg: None

        self.set_task_callback(task_callback)
        self.offload_all() # Send any active diffusion pipelines to CPU
        del self.drag_pipeline # Unload this
        self.start_keepalive()
        try:
            if isinstance(image, str):
                from enfugue.util import image_from_uri
                image = image_from_uri(image)

            width, height = image.size
            self.svd_xt = use_xt

            pipe = self.svd_pipeline
            vae_preview = None
            if image_callback is not None and image_callback_steps is not None:
                vae_preview = self.get_vae_preview(False).to(device=self.device)

            self.stop_keepalive()
            task_callback("Executing Inference")

            frame_window_size = 21 if self.svd_xt else 14
            num_iterations = ceil(num_frames / frame_window_size)
            iteration = 0
            total_steps = num_iterations * num_inference_steps
            total_step = 0
            total_images = [
                image.copy()
                for i in range(num_frames)
            ]
            step_start: datetime.datetime = datetime.datetime.now()
            step_times: List[float] = []

            def step_callback(
                pipe: StableVideoDiffusionPipeline,
                step: int,
                timestep: Tensor,
                callback_kwargs: Dict[str, Any]
            ) -> Dict[str, Any]:
                """
                The SVD pipeline uses one callback function, so we invoke our split ones here
                """
                import numpy as np
                from einops import rearrange
                from torchvision import utils
                nonlocal total_step, step_start

                total_step += 1
                iteration_start = iteration * frame_window_size

                now = datetime.datetime.now()
                step_times.append((now-step_start).total_seconds())
                step_start = now

                if progress_callback is not None:
                    time_slice = step_times[-5:]
                    step_rate = 1.0 / (sum(time_slice)/len(time_slice))
                    progress_callback(total_step, total_steps, step_rate)

                if (
                    step > 0 and
                    vae_preview is not None and
                    image_callback is not None and
                    image_callback_steps is not None and
                    step % image_callback_steps == 0 and
                    "latents" in callback_kwargs
                ):
                    latents = callback_kwargs["latents"]
                    preview_decoded = torch.cat([
                        vae_preview.decode(
                            latents[:, i, :, :, :],
                            return_dict=False
                        )[0].to(self.device).unsqueeze(1)
                        for i in range(latents.shape[1])
                    ], dim=1)
                    preview_decoded = (preview_decoded / 2 + 0.5).clamp(0, 0.98)
                    preview_decoded = rearrange(preview_decoded, "b f c h w -> f b c h w")
                    images = []
                    for frame in preview_decoded:
                        frame = utils.make_grid(frame, nrow=8)
                        frame = frame.transpose(0, 1).transpose(1, 2).squeeze(-1)
                        frame = (255 - (frame * 255)).cpu().numpy().astype(np.uint8)
                        images.extend(pipe.image_processor.numpy_to_pil(frame)) # type: ignore[attr-defined]
                    step_images = len(images)
                    for i in range(iteration_start, num_frames):
                        image_index = i - iteration_start
                        if image_index >= step_images:
                            image_index = step_images - 1
                        total_images[i] = images[image_index].copy()
                    image_callback(total_images)
                return callback_kwargs

            for iteration in range(num_iterations):
                frames = pipe( # type: ignore[operator]
                    image=image.convert("RGB"),
                    height=height,
                    width=width,
                    num_frames=frame_window_size,
                    decode_chunk_size=decode_chunk_size,
                    num_inference_steps=num_inference_steps,
                    min_guidance_scale=min_guidance_scale,
                    max_guidance_scale=max_guidance_scale,
                    fps=fps,
                    motion_bucket_id=motion_bucket_id,
                    noise_aug_strength=noise_aug_strength,
                    generator=self.noise_generator,
                    callback_on_step_end=step_callback,
                    callback_on_step_end_tensor_inputs=["latents"] if image_callback is not None else [],
                ).frames[0]
                iteration_start = iteration * frame_window_size
                for i, frame in enumerate(frames):
                    total_images[iteration_start+i] = frame
                image = frames[-1].convert("RGB")
            del pipe
            del vae_preview
            self.clear_memory()
            return total_images
        finally:
            self.clear_task_callback()
            self.stop_keepalive()

    def __call__(
        self,
        refiner_start: Optional[float] = None,
        refiner_strength: Optional[float] = None,
        refiner_guidance_scale: Optional[float] = None,
        refiner_aesthetic_score: Optional[float] = None,
        refiner_negative_aesthetic_score: Optional[float] = None,
        refiner_prompt: Optional[str] = None,
        refiner_prompt_2: Optional[str] = None,
        refiner_negative_prompt: Optional[str] = None,
        refiner_negative_prompt_2: Optional[str] = None,
        scale_to_refiner_size: bool = True,
        task_callback: Optional[Callable[[str], None]] = None,
        next_intention: Optional[Literal["inpainting", "animation", "inference", "refining", "upscaling"]] = None,
        scheduler: Optional[SCHEDULER_LITERAL] = None,
        **kwargs: Any,
    ) -> StableDiffusionPipelineOutput:
        """
        Passes an invocation down to the pipeline, doing whatever it needs to do to initialize it.
        Will switch between inpainting and non-inpainting models
        """
        if task_callback is None:
            task_callback = lambda arg: None

        self.set_task_callback(task_callback)

        if kwargs.get("ip_adapter_images", None) is not None:
            requested_ip_adapter = kwargs.get("ip_adapter_model", "default")
            if requested_ip_adapter is None:
                requested_ip_adapter = "default"
            self._ip_adapter_model = requested_ip_adapter
        else:
            self._ip_adapter_model = None

        latent_callback = noop
        will_refine = (refiner_strength != 0 or (refiner_start != 0 and refiner_start != 1)) and self.refiner is not None
        callback_images: List[PIL.Image.Image] = []

        if kwargs.get("latent_callback", None) is not None and kwargs.get("latent_callback_type", "pil") == "pil":
            latent_callback = kwargs["latent_callback"]
            if will_refine:
                # Memoize last latent callbacks because we aren't returning an image from the first execution
                previous_callback = latent_callback
                def memoize_callback(images: List[PIL.Image.Image]) -> None:
                    nonlocal callback_images
                    callback_images = images
                    previous_callback(images)
                latent_callback = memoize_callback # type: ignore[assignment]
                kwargs["latent_callback"] = memoize_callback

        self.start_keepalive()

        try:
            animating = bool(kwargs.get("animation_frames", None))
            inpainting = kwargs.get("mask", None) is not None
            refining = (
                kwargs.get("image", None) is not None and
                kwargs.get("strength", 0) in [0, None] and
                kwargs.get("ip_adapter_scale", None) is None and
                refiner_strength != 0 and
                refiner_start != 1 and
                self.refiner is not None
            )

            if animating:
                intention = "animation"
            elif inpainting:
                intention = "inpainting"
            elif refining:
                intention = "refining"
            else:
                intention = "inference"

            task_callback(f"Preparing {intention.title()} Pipeline")
            # Unload any remaining specialty pipelines
            del self.svd_pipeline
            del self.drag_pipeline

            if animating and self.has_animator:
                size = self.animator_size
            elif inpainting and (self.has_inpainter or self.create_inpainter):
                size = self.inpainter_size
            elif refining:
                size = self.refiner_size
            else:
                size = self.size

            if scheduler is not None:
                # Allow overriding scheduler
                self.scheduler = scheduler # type: ignore[assignment]

            if refining:
                # Set result here to passed image
                from diffusers.pipelines.stable_diffusion import StableDiffusionPipelineOutput
                samples = kwargs.get("samples", 1)
                result = StableDiffusionPipelineOutput(
                    images=[kwargs["image"]] * samples,
                    nsfw_content_detected=[False] * samples
                )
                self.offload_animator(intention) # type: ignore
                self.offload_pipeline(intention) # type: ignore
                self.offload_inpainter(intention) # type: ignore
            else:
                called_width = kwargs.get("width", size)
                called_height = kwargs.get("height", size)
                tiling_stride = kwargs.get("tiling_stride", self.tiling_stride)

                # Check sizes
                if called_width < size:
                    self.tensorrt_is_enabled = False
                    logger.info(f"Width ({called_width}) less than configured width ({size}), disabling TensorRT")
                elif called_height < size:
                    self.tensorrt_is_enabled = False
                    logger.info(f"height ({called_height}) less than configured height ({size}), disabling TensorRT")
                elif (called_width != size or called_height != size) and not tiling_stride:
                    logger.info(f"Dimensions do not match size of engine and chunking is disabled, disabling TensorRT")
                    self.tensorrt_is_enabled = False
                else:
                    self.tenssort_is_enabled = True
                
                # Check IP adapter for TensorRT
                if self._ip_adapter_model is not None:
                    logger.info(f"IP adapter requested, TensorRT is not compatible, disabling.")
                    self.tensorrt_is_enabled = False

                if animating:
                    if not self.has_animator:
                        logger.debug(f"Animation requested but no animator set, setting animator to the same as the base model")
                        self.animator = self.model

                    self.offload_pipeline(intention) # type: ignore
                    self.offload_refiner(intention) # type: ignore
                    self.offload_inpainter(intention) # type: ignore

                    # Check IP adapter load/unload
                    if hasattr(self, "_animator_pipeline"):
                        if self._ip_adapter_model is None:
                            if self._animator_pipeline.ip_adapter_loaded:
                                self.unload_animator("disabling IP adapter")
                        else:
                            if not self._animator_pipeline.ip_adapter_loaded:
                                self.unload_animator("enabling IP adapter")
                            elif self.ip_adapter.model != self._ip_adapter_model:
                                self.unload_animator("changing IP adapter model")

                    pipe = self.animator_pipeline
                    if self.reload_motion_module and self.motion_module is not None:
                        if task_callback is not None:
                            task_callback("Reloading motion module")
                        try:
                            pipe.load_motion_module_weights(
                                motion_module=self.motion_module,
                                task_callback=task_callback,
                                position_encoding_truncate_length=self.position_encoding_truncate_length,
                                position_encoding_scale_length=self.position_encoding_scale_length,
                            )
                        except Exception as ex:
                            logger.warning(f"Received Exception {ex} when loading motion module weights, will try to reload the entire pipeline.")
                            del pipe
                            self.reload_motion_module = False
                            self.unload_animator("Re-initializing Pipeline")
                            pipe = self.animator_pipeline # Will raise

                elif inpainting and (self.has_inpainter or self.create_inpainter):
                    self.offload_pipeline(intention) # type: ignore
                    self.offload_refiner(intention) # type: ignore
                    self.offload_animator(intention) # type: ignore
                    # Check IP adapter load/unload
                    if hasattr(self, "_inpainter_pipeline"):
                        if self._ip_adapter_model is None:
                            if self._inpainter_pipeline.ip_adapter_loaded:
                                self.unload_inpainter("disabling IP adapter")
                        else:
                            if not self._inpainter_pipeline.ip_adapter_loaded:
                                self.unload_inpainter("enabling IP adapter")
                            elif self.ip_adapter.model != self._ip_adapter_model:
                                self.unload_inpainter("changing IP adapter model")
                    pipe = self.inpainter_pipeline # type: ignore
                else:
                    if inpainting:
                        logger.info(f"No inpainter set and creation is disabled; using base pipeline for inpainting.")
                    self.offload_refiner(intention) # type: ignore
                    self.offload_inpainter(intention) # type: ignore
                    self.offload_animator(intention) # type: ignore
                    # Check IP adapter load/unload
                    if hasattr(self, "_pipeline"):
                        if self._ip_adapter_model is None:
                            if self._pipeline.ip_adapter_loaded:
                                self.unload_pipeline("disabling IP adapter", False)
                        else:
                            if not self._pipeline.ip_adapter_loaded:
                                self.unload_pipeline("enabling IP adapter", False)
                            elif self.ip_adapter.model != self._ip_adapter_model:
                                self.unload_pipeline("changing IP adapter model", False)

                    pipe = self.pipeline # type: ignore

                # Check refining settings
                if self.refiner is not None and refiner_strength != 0:
                    refiner_start = self.refiner_start if refiner_start is None else refiner_start
                    if refiner_start > 0 and refiner_start < 1:
                        kwargs["denoising_end"] = refiner_start
                        kwargs["output_type"] = "latent"

                self.stop_keepalive()
                task_callback("Executing Inference")
                logger.debug(f"Calling pipeline with arguments {redact_for_log(kwargs)}")
                try:
                    result = pipe( # type: ignore[assignment]
                        generator=self.generator,
                        device=self.device,
                        offload_models=self.pipeline_sequential_onload,
                        noise_generator=self.noise_generator,
                        **kwargs
                    )
                except BadRequestError:
                    raise
                except:
                    if inpainting and (self.has_inpainter or self.create_inpainter):
                        self.unload_inpainter("invocation error")
                    elif animating:
                        self.unload_animator("invocation error")
                    else:
                        self.unload_pipeline("invocation error")
                    raise
            if will_refine:
                self.start_keepalive()

                # Loading both SDXL checkpoints into memory at once requires a LOT of VRAM - more than 24GB, at least.
                # If the refiner is not cached, it takes even more; possibly too much.
                # Add a catch here to unload the main pipeline if loading the refiner pipeline and it's not cached.

                task_callback("Preparing Refining Pipeline")

                if self.refiner_is_sdxl and not self.refiner_engine_cache_exists:
                    # Force unload
                    if inpainting:
                        self.unload_inpainter("switching to refining")
                    else:
                        self.unload_pipeline("switching to refining")
                elif inpainting:
                    self.offload_inpainter("refining")
                else:
                    self.offload_pipeline("refining")

                kwargs.pop("image", None)  # Remove any previous image
                kwargs.pop("mask", None)  # Remove any previous mask
                kwargs.pop("control_images", None) # Remove previous ControlNet images
                kwargs.pop("ip_adapter_images", None) # IP adapter seems to absolutely explode with refiner
                kwargs["latent_callback"] = latent_callback # Revert to original callback, we'll wrap later if needed
                kwargs["output_type"] = "pil"
                kwargs["latent_callback_type"] = "pil"
                kwargs["strength"] = refiner_strength if refiner_strength else self.refiner_strength
                kwargs["denoising_start"] = kwargs.pop("denoising_end", None)
                kwargs["guidance_scale"] = (
                    refiner_guidance_scale if refiner_guidance_scale else self.refiner_guidance_scale
                )
                kwargs["aesthetic_score"] = (
                    refiner_aesthetic_score if refiner_aesthetic_score else self.refiner_aesthetic_score
                )
                kwargs["negative_aesthetic_score"] = (
                    refiner_negative_aesthetic_score
                    if refiner_negative_aesthetic_score
                    else self.refiner_negative_aesthetic_score
                )

                # check if we have a different prompt
                if refiner_prompt:
                    kwargs["prompt"] = refiner_prompt
                    if "prompt_2" in kwargs and not refiner_prompt_2:
                        # if giving a refining prompt but not a second refining prompt,
                        # and the primary prompt has a secondary prompt, then remove
                        # the non-refining secondary prompt as it overrides too much
                        # of the refining prompt if it gets merged
                        kwargs.pop("prompt_2")
                if refiner_prompt_2:
                    kwargs["prompt_2"] = refiner_prompt_2
                if refiner_negative_prompt:
                    kwargs["negative_prompt"] = refiner_negative_prompt
                    if "negative_prompt_2" in kwargs and not refiner_negative_prompt_2:
                        kwargs.pop("negative_prompt_2")
                if refiner_negative_prompt_2:
                    kwargs["negative_prompt_2"] = refiner_negative_prompt_2

                logger.debug(f"Refining results with arguments {redact_for_log(kwargs)}")
                pipe = self.refiner_pipeline # type: ignore 
                self.stop_keepalive()  # This checks, we can call it all we want
                task_callback(f"Refining")

                refiner_result = pipe(  # type: ignore
                    generator=self.generator,
                    device=self.device,
                    offload_models=self.pipeline_sequential_onload,
                    noise_generator=self.noise_generator,
                    image=result["images"],
                    **kwargs
                )

                # Callback with the result
                result = refiner_result # type: ignore[assignment]
                if next_intention == "refining":
                    logger.debug("Next intention is refining, leaving refiner in memory")
                elif next_intention == "upscaling":
                    logger.debug("Next intention is upscaling, unloading pipeline and sending refiner to CPU")
                    self.unload_pipeline("unloading for upscaling")
                self.offload_refiner(intention if next_intention is None else next_intention) # type: ignore
            return result
        finally:
            self.clear_task_callback()
            self.stop_keepalive()
            self.tensorrt_is_enabled = True

    def write_model_metadata(self, path: str) -> None:
        """
        Writes metadata for TensorRT to a json file
        """
        if "controlnet" in path:
            dump_json(path, {"size": self.tensorrt_size, "controlnets": self.controlnet_names})
        else:
            dump_json(
                path,
                {
                    "size": self.tensorrt_size,
                    "lora": self.lora_names_weights,
                    "lycoris": self.lycoris_names_weights,
                    "inversion": self.inversion_names,
                },
            )

    @staticmethod
    def get_status(
        engine_root: str,
        model: str,
        size: Optional[int] = None,
        lora: Optional[Union[str, Tuple[str, float], List[Union[str, Tuple[str, float]]]]] = None,
        lycoris: Optional[Union[str, Tuple[str, float], List[Union[str, Tuple[str, float]]]]] = None,
        inversion: Optional[Union[str, List[str]]] = None,
        controlnet: Optional[Union[str, List[str]]] = None,
    ) -> Dict[str, bool]:
        """
        Gets the TensorRT status for an individual model.
        """
        tensorrt_is_supported = False

        try:
            import tensorrt

            tensorrt.__version__  # quiet importchecker
            tensorrt_is_supported = True
        except Exception as ex:
            logger.info("TensorRT is disabled.")
            logger.debug("{0}: {1}".format(type(ex).__name__, ex))
            pass

        if model.endswith(".ckpt") or model.endswith(".safetensors"):
            model, _ = os.path.splitext(os.path.basename(model))
        else:
            model = os.path.basename(model)

        model_dir = os.path.join(engine_root, "tensorrt", model)
        model_cache_dir = os.path.join(engine_root, "diffusers", model)
        model_index: Optional[str] = os.path.join(model_dir, "model_index.json")
        if not os.path.exists(model_index):  # type: ignore
            model_index = os.path.join(model_cache_dir, "model_index.json")
            if not os.path.exists(model_index):
                model_index = None

        if model_index is not None:
            # Cached model, get details
            model_is_sdxl = os.path.exists(os.path.join(os.path.dirname(model_index), "tokenizer_2"))
        else:
            model_is_sdxl = "xl" in model.lower()

        if not tensorrt_is_supported or model_is_sdxl:
            return {"supported": False, "xl": model_is_sdxl, "ready": False}

        if size is None:
            size = DiffusionPipelineManager.DEFAULT_SIZE

        if inversion is None:
            inversion = []
        elif not isinstance(inversion, list):
            inversion = [inversion]

        inversion_key = []
        for inversion_part in inversion:
            inversion_name, ext = os.path.splitext(os.path.basename(inversion_part))
            inversion_key.append(inversion_name)

        if lora is None:
            lora = []
        elif not isinstance(lora, list):
            lora = [lora]

        lora_key = []
        for lora_part in lora:
            if isinstance(lora_part, tuple):
                lora_path, lora_weight = lora_part
            else:
                lora_path, lora_weight = lora_part, 1.0
            lora_name, ext = os.path.splitext(os.path.basename(lora_path))
            lora_key.append((lora_name, lora_weight))

        if lycoris is None:
            lycoris = []
        elif not isinstance(lycoris, list):
            lycoris = [lycoris]

        lycoris_key = []
        for lycoris_part in lycoris:
            if isinstance(lycoris_part, tuple):
                lycoris_path, lycoris_weight = lycoris_part
            else:
                lycoris_path, lycoris_weight = lycoris_part, 1.0
            lycoris_name, ext = os.path.splitext(os.path.basename(lycoris_path))
            lycoris_key.append((lycoris_name, lycoris_weight))

        clip_ready = "clip" not in DiffusionPipelineManager.TENSORRT_STAGES
        vae_ready = "vae" not in DiffusionPipelineManager.TENSORRT_STAGES
        unet_ready = "unet" not in DiffusionPipelineManager.TENSORRT_STAGES
        controlled_unet_ready = unet_ready

        if not clip_ready:
            clip_key = DiffusionPipelineManager.get_clip_key(
                size, lora=lora_key, lycoris=lycoris_key, inversion=inversion_key
            )
            clip_plan = os.path.join(model_dir, "clip", clip_key, "engine.plan")
            clip_ready = os.path.exists(clip_plan)

        if not vae_ready:
            vae_key = DiffusionPipelineManager.get_vae_key(
                size, lora=lora_key, lycoris=lycoris_key, inversion=inversion_key
            )
            vae_plan = os.path.join(model_dir, "vae", vae_key, "engine.plan")
            vae_ready = os.path.exists(vae_plan)

        if not unet_ready:
            unet_key = DiffusionPipelineManager.get_unet_key(
                size, lora=lora_key, lycoris=lycoris_key, inversion=inversion_key
            )
            unet_plan = os.path.join(model_dir, "unet", unet_key, "engine.plan")
            unet_ready = os.path.exists(unet_plan)

            controlled_unet_key = DiffusionPipelineManager.get_controlled_unet_key(
                size, lora=lora_key, lycoris=lycoris_key, inversion=inversion_key
            )
            controlled_unet_plan = os.path.join(model_dir, "controlledunet", controlled_unet_key, "engine.plan")
            controlled_unet_ready = os.path.exists(controlled_unet_plan)

        ready = clip_ready and vae_ready
        if controlnet is not None or DiffusionPipelineManager.TENSORRT_ALWAYS_USE_CONTROLLED_UNET:
            ready = ready and controlled_unet_ready
        else:
            ready = ready and unet_ready

        return {
            "supported": tensorrt_is_supported,
            "xl": model_is_sdxl,
            "unet_ready": unet_ready,
            "controlled_unet_ready": controlled_unet_ready,
            "vae_ready": vae_ready,
            "clip_ready": clip_ready,
            "ready": ready,
        }

    def create_inpainting_checkpoint(
        self,
        source_checkpoint_path: str,
        target_checkpoint_path: str,
        is_sdxl: bool = False
    ) -> None:
        """
        Creates an inpainting model by merging in the SD 1.5 inpainting model with a non inpainting model.
        """
        from enfugue.diffusion.util import ModelMerger

        primary_model = DEFAULT_SDXL_INPAINTING_MODEL if is_sdxl else DEFAULT_INPAINTING_MODEL
        tertiary_model = DEFAULT_SDXL_MODEL if is_sdxl else DEFAULT_MODEL

        try:
            merger = ModelMerger(
                self.check_download_model(self.engine_checkpoints_dir, primary_model),
                source_checkpoint_path,
                self.check_download_model(self.engine_checkpoints_dir, tertiary_model),
                interpolation="add-difference",
            )
            merger.save(target_checkpoint_path)
        except Exception as ex:
            logger.error(
                f"Couldn't save merged checkpoint made from {source_checkpoint_path} to {target_checkpoint_path}: {ex}"
            )
            logger.error(traceback.format_exc())
            raise
        else:
            logger.info(f"Saved merged inpainting checkpoint at {target_checkpoint_path}")
