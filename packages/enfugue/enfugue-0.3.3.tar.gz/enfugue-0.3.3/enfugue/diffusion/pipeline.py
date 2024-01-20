from __future__ import annotations

from typing import (
    Any,
    List,
    Callable,
    Dict,
    List,
    Optional,
    Union,
    Tuple,
    Iterator,
    Literal,
    Mapping,
    TypedDict,
    cast,
    TYPE_CHECKING
)
from typing_extensions import NotRequired

import os
import PIL
import PIL.Image
import copy
import math
import torch
import inspect
import datetime
import torchvision
import numpy as np
import safetensors.torch

from contextlib import contextmanager
from omegaconf import OmegaConf
from compel import ReturnedEmbeddingsType
from einops import rearrange, repeat
from math import floor, ceil

from transformers import (
    AutoFeatureExtractor,
    CLIPImageProcessor,
    CLIPTextModel,
    CLIPTextModelWithProjection,
    CLIPTokenizer,
    CLIPVisionModelWithProjection,
)
from diffusers.schedulers import (
    KarrasDiffusionSchedulers,
    DDIMScheduler,
    DPMSolverMultistepScheduler,
    EulerAncestralDiscreteScheduler,
    EulerDiscreteScheduler,
    HeunDiscreteScheduler,
    LMSDiscreteScheduler,
    PNDMScheduler,
)
from diffusers.models.modeling_utils import ModelMixin
from diffusers.models import (
    AutoencoderKL,
    AutoencoderTiny,
    ConsistencyDecoderVAE,
    UNet2DConditionModel,
    ControlNetModel,
)
from diffusers.loaders import LoraLoaderMixin
from diffusers.models.attention_processor import (
    AttnProcessor2_0,
    LoRAAttnProcessor2_0,
    LoRAXFormersAttnProcessor,
    XFormersAttnProcessor,
)
from diffusers.pipelines.stable_diffusion import (
    StableDiffusionPipeline,
    StableDiffusionPipelineOutput,
    StableDiffusionSafetyChecker,
)
from diffusers.pipelines.stable_diffusion.convert_from_ckpt import (
    create_unet_diffusers_config,
    create_vae_diffusers_config,
    convert_ldm_unet_checkpoint,
    convert_ldm_vae_checkpoint,
    convert_ldm_clip_checkpoint,
    convert_open_clip_checkpoint,
)

from diffusers.utils import PIL_INTERPOLATION
from diffusers.utils.torch_utils import randn_tensor
from diffusers.image_processor import VaeImageProcessor

from pibble.util.files import load_json

from enfugue.diffusion.animate.diff.sparse_controlnet import SparseControlNetModel # type: ignore[attr-defined]
from enfugue.diffusion.constants import *
from enfugue.util import (
    logger,
    check_download_to_dir,
    merge_tokens,
)

from enfugue.diffusion.util import (
    iterate_state_dict,
    load_state_dict,
    empty_cache,
    make_noise,
    blend_latents,
    freq_mix_3d,
    get_freq_filter,
    LatentScaler,
    MaskWeightBuilder,
    PromptEncoder,
    Prompt,
    Chunker,
    EncodedPrompt,
    EncodedPrompts,
    Video,
)

if TYPE_CHECKING:
    from enfugue.diffusers.support.ip import IPAdapter

# This is ~64k×64k. Absurd, but I don't judge
PIL.Image.MAX_IMAGE_PIXELS = 2**32

# Image arg accepted arguments
ImageArgType = Union[str, PIL.Image.Image, List[PIL.Image.Image]]

# IP image accepted arguments
class ImagePromptArgDict(TypedDict):
    image: ImageArgType
    scale: NotRequired[float]

ImagePromptType = Union[
    ImageArgType, # Image
    Tuple[ImageArgType, float], # Image, Scale
    ImagePromptArgDict,
]

ImagePromptArgType = Optional[Union[ImagePromptType, List[ImagePromptType]]]

# Control image accepted arguments
class ControlImageArgDict(TypedDict):
    image: ImageArgType
    scale: NotRequired[Optional[Union[float, List[float]]]]
    start: NotRequired[Optional[float]]
    end: NotRequired[Optional[float]]
    frame: NotRequired[Optional[Union[int, List[int]]]]
    frequency: NotRequired[Optional[Union[int, Tuple[int]]]]
    standalone: NotRequired[bool]
    channel: NotRequired[Optional[Tuple[int, ...]]]

ControlImageType = Union[
    ImageArgType, # Image
    Tuple[ImageArgType, float], # Image, Scale
    ControlImageArgDict
]

ControlImageArgType = Optional[Dict[str, Union[ControlImageType, List[ControlImageType]]]]
PreparedControlImageType = Tuple[torch.Tensor, Union[float, torch.Tensor], Optional[float], Optional[float], Optional[torch.Tensor]]
PreparedControlImageArgType = Optional[Dict[str, List[PreparedControlImageType]]]

class EnfugueStableDiffusionPipeline(StableDiffusionPipeline):
    """
    This pipeline merges all of the following, for all versions of SD:
    1. txt2img
    2. img2img
    3. inpainting/outpainting
    4. controlnet/multicontrolnet
    5. ip adapter
    6. animatediff
    """
    controlnets: Optional[Dict[str, ControlNetModel]]
    unet: UNet2DConditionModel
    scheduler: KarrasDiffusionSchedulers
    vae: AutoencoderKL
    vae_preview: AutoencoderTiny
    tokenizer: Optional[CLIPTokenizer]
    tokenizer_2: Optional[CLIPTokenizer]
    text_encoder: Optional[CLIPTextModel]
    text_encoder_2: Optional[CLIPTextModelWithProjection]
    vae_scale_factor: int
    safety_checker: Optional[StableDiffusionSafetyChecker]
    config: OmegaConf
    safety_checking_disabled: bool = False

    frame_window_size: Optional[int]
    frame_window_stride: Optional[int]
    tiling_stride: Optional[int]
    tiling_mask_type: MASK_TYPE_LITERAL
    frequencies_filter_type: Literal["gaussian", "ideal", "box", "butterworth"] = "butterworth"
    frequencies_filter_order = 4
    frequencies_filter_stop_spatial = 0.25
    frequencies_filter_stop_temporal = 0.25

    def __init__(
        self,
        vae: Union[AutoencoderKL, ConsistencyDecoderVAE],
        vae_preview: Optional[AutoencoderTiny],
        text_encoder: Optional[CLIPTextModel],
        text_encoder_2: Optional[CLIPTextModelWithProjection],
        tokenizer: Optional[CLIPTokenizer],
        tokenizer_2: Optional[CLIPTokenizer],
        unet: UNet2DConditionModel,
        scheduler: KarrasDiffusionSchedulers,
        safety_checker: Optional[StableDiffusionSafetyChecker],
        feature_extractor: Optional[CLIPImageProcessor],
        image_encoder: Optional[CLIPVisionModelWithProjection]=None,
        controlnets: Optional[Dict[str, ControlNetModel]]=None,
        requires_safety_checker: bool=True,
        force_zeros_for_empty_prompt: bool=True,
        requires_aesthetic_score: bool=False,
        force_full_precision_vae: bool=False,
        ip_adapter: Optional[IPAdapter]=None,
        engine_size: int=512,
        tiling_size: Optional[int]=None,
        tiling_stride: Optional[int]=64,
        tiling_mask_type: MASK_TYPE_LITERAL="bilinear",
        tiling_mask_kwargs: Dict[str, Any]={},
        frame_window_size: Optional[int]=16,
        frame_window_stride: Optional[int]=4
    ) -> None:
        super(EnfugueStableDiffusionPipeline, self).__init__(
            vae=vae,
            text_encoder=text_encoder,
            tokenizer=tokenizer,
            unet=unet,
            scheduler=scheduler,
            safety_checker=safety_checker,
            feature_extractor=feature_extractor,
            requires_safety_checker=requires_safety_checker,
            image_encoder=image_encoder,
        )
        # Save scheduler config for hotswapping
        self.scheduler_class = type(scheduler)
        self.scheduler_config = {**dict(scheduler.config)} # type: ignore[attr-defined]

        # Enfugue engine settings
        self.engine_size = engine_size
        self.tiling_size = tiling_size
        self.tiling_stride = tiling_stride
        self.tiling_mask_type = tiling_mask_type
        self.tiling_mask_kwargs = tiling_mask_kwargs
        self.frame_window_size = frame_window_size
        self.frame_window_stride = frame_window_stride

        # Hide tqdm
        self.set_progress_bar_config(disable=True) # type: ignore[attr-defined]

        # Add config for xl
        self.register_to_config( # type: ignore[attr-defined]
            force_full_precision_vae=force_full_precision_vae,
            requires_aesthetic_score=requires_aesthetic_score,
            force_zeros_for_empty_prompt=force_zeros_for_empty_prompt
        )

        # Add an image processor for later
        self.image_processor = VaeImageProcessor(vae_scale_factor=self.vae_scale_factor)

        # Register other networks
        self.register_modules( # type: ignore[attr-defined]
            text_encoder_2=text_encoder_2,
            tokenizer_2=tokenizer_2,
            vae_preview=vae_preview
        )

        # Add ControlNet map
        self.controlnets = controlnets

        # Add IP Adapter
        self.ip_adapter = ip_adapter
        self.ip_adapter_loaded = False

        # Create helpers
        self.latent_scaler = LatentScaler(
            upscale_mode="bicubic",
            downscale_mode="bicubic"
        )

    @classmethod
    def open_image(cls, path: str) -> List[PIL.Image.Image]:
        """
        Opens an image or video and standardizes to a list of images
        """
        ext = os.path.splitext(path)[1]
        if ext in [".gif", ".webp", ".mp4", ".mkv", ".mp4", ".avi", ".mov", ".apng"]:
            return list(Video.file_to_frames(path))
        else:
            return [PIL.Image.open(path)]

    @classmethod
    def get_config_from_url(cls, cache_dir: str, url: str) -> Dict[str, Any]:
        """
        Downloads remote config and loads it
        """
        config_path = check_download_to_dir(url, cache_dir, check_size=False)
        return load_json(config_path)

    @classmethod
    def create_unet(
        cls,
        config: Dict[str, Any],
        cache_dir: str,
        is_sdxl: bool,
        is_inpainter: bool,
        task_callback: Optional[Callable[[str], None]]=None,
        **kwargs: Any
    ) -> ModelMixin:
        """
        Instantiates the UNet from config
        """
        from diffusers.models.attention_processor import AttnProcessor2_0
        if is_sdxl and is_inpainter and config["in_channels"] == 9:
            config = cls.get_config_from_url(
                cache_dir,
                "https://huggingface.co/diffusers/stable-diffusion-xl-1.0-inpainting-0.1/raw/main/unet/config.json?filename=stable-diffusion-xl-1.0-inpainting-0.1-unet-config.json"
            )
        unet = UNet2DConditionModel.from_config(config)
        unet.set_attn_processor(AttnProcessor2_0())
        return unet

    @classmethod
    def from_ckpt(
        cls,
        checkpoint_path: str,
        cache_dir: str,
        prediction_type: Optional[str]=None,
        image_size: int=512,
        scheduler_type: Literal["pndm", "lms", "heun", "euler", "euler-ancestral", "dpm", "ddim"]="ddim",
        vae: Optional[Union[AutoencoderKL, ConsistencyDecoderVAE]]=None,
        vae_preview: Optional[AutoencoderTiny]=None,
        load_safety_checker: bool=True,
        torch_dtype: Optional[torch.dtype]=None,
        upcast_attention: Optional[bool]=None,
        extract_ema: Optional[bool]=None,
        motion_dir: Optional[str]=None,
        motion_module: Optional[str]=None,
        unet_kwargs: Dict[str, Any]={},
        offload_models: bool=False,
        is_inpainter=False,
        task_callback: Optional[Callable[[str], None]]=None,
        position_encoding_truncate_length: Optional[int]=None,
        position_encoding_scale_length: Optional[int]=None,
        **kwargs: Any,
    ) -> EnfugueStableDiffusionPipeline:
        """
        Loads a checkpoint into this pipeline.
        Diffusers' `from_pretrained` lets us pass arbitrary kwargs in, but `from_ckpt` does not.
        That's why we override it for this method - most of this is copied from
        https://github.com/huggingface/diffusers/blob/49949f321d9b034440b52e54937fd2df3027bf0a/src/diffusers/pipelines/stable_diffusion/convert_from_ckpt.py
        """
        if task_callback is None:
            task_callback = lambda msg: logger.debug(msg)

        task_callback(f"Loading checkpoint file {os.path.basename(checkpoint_path)}")
        checkpoint = load_state_dict(checkpoint_path)

        # Sometimes models don't have the global_step item
        if "global_step" in checkpoint:
            global_step = checkpoint["global_step"]
        else:
            global_step = None

        # NOTE: this while loop isn't great but this controlnet checkpoint has one additional
        # "state_dict" key https://huggingface.co/thibaud/controlnet-canny-sd21
        while "state_dict" in checkpoint:
            checkpoint = checkpoint["state_dict"] # type: ignore[assignment]

        checkpoint = cast(Mapping[str, torch.Tensor], checkpoint) # type: ignore[assignment]

        # Check for config in same directory as checkpoint
        ckpt_dir = os.path.dirname(os.path.abspath(checkpoint_path))
        ckpt_name, _ = os.path.splitext(os.path.basename(checkpoint_path))

        original_config_file: Optional[str] = os.path.join(ckpt_dir, f"{ckpt_name}.yaml")
        if os.path.exists(original_config_file): # type: ignore[arg-type]
            logger.info(f"Found configuration file alongside checkpoint, using {ckpt_name}.yaml")
        else:
            original_config_file = os.path.join(ckpt_dir, f"{ckpt_name}.json")
            if os.path.exists(original_config_file):
                logger.info(f"Found configuration file alongside checkpoint, using {ckpt_name}.json")
            else:
                original_config_file = None

        if original_config_file is None:
            key_name_2_1 = "model.diffusion_model.input_blocks.2.1.transformer_blocks.0.attn2.to_k.weight"
            key_name_xl_base = "conditioner.embedders.1.model.transformer.resblocks.9.mlp.c_proj.bias"
            key_name_xl_refiner = "conditioner.embedders.0.model.transformer.resblocks.9.mlp.c_proj.bias"

            # SD v1 default
            config_url = (
                "https://raw.githubusercontent.com/CompVis/stable-diffusion/main/configs/stable-diffusion/v1-inference.yaml"
            )

            if key_name_2_1 in checkpoint and checkpoint[key_name_2_1].shape[-1] == 1024: # type: ignore[union-attr]
                # SD v2.1
                config_url = "https://raw.githubusercontent.com/Stability-AI/stablediffusion/main/configs/stable-diffusion/v2-inference-v.yaml"
                logger.info(f"No configuration file found for checkpoint {ckpt_name}, using Stable Diffusion V2.1")

                if global_step == 110000:
                    # v2.1 needs to upcast attention
                    upcast_attention = True
            elif key_name_xl_base in checkpoint:
                # SDXL Base
                logger.info(f"No configuration file found for checkpoint {ckpt_name}, using Stable Diffusion XL Base")
                config_url = "https://raw.githubusercontent.com/Stability-AI/generative-models/main/configs/inference/sd_xl_base.yaml"
            elif key_name_xl_refiner in checkpoint:
                # SDXL Refiner
                logger.info(f"No configuration file found for checkpoint {ckpt_name}, using Stable Diffusion XL Refiner")
                config_url = "https://raw.githubusercontent.com/Stability-AI/generative-models/main/configs/inference/sd_xl_refiner.yaml"
            else:
                # SD v1
                logger.info(f"No configuration file found for checkpoint {ckpt_name}, using Stable Diffusion 1.5")
            original_config_file = check_download_to_dir(config_url, cache_dir, check_size=False)

        original_config = OmegaConf.load(original_config_file) # type: ignore

        if "model.diffusion_model.input_blocks.0.0.weight" in checkpoint:
            num_in_channels = checkpoint["model.diffusion_model.input_blocks.0.0.weight"].shape[1] # type: ignore[union-attr]
            logger.info(f"Checkpoint has {num_in_channels} input channels")
        else:
            num_in_channels = 9 if is_inpainter else 4
            logger.info(f"Could not automatically determine input channels, forcing {num_in_channels} input channels")

        if "conditioner.embedders.1.model.text_projection.weight" in checkpoint:
            # Fix for playgroundv2, segmind
            checkpoint["conditioner.embedders.1.model.text_projection"] = checkpoint.pop("conditioner.embedders.1.model.text_projection.weight")

        if "unet_config" in original_config["model"]["params"]:  # type: ignore
            # SD 1 or 2
            original_config["model"]["params"]["unet_config"]["params"]["in_channels"] = num_in_channels  # type: ignore
        elif "network_config" in original_config["model"]["params"]:  # type: ignore
            # SDXL
            original_config["model"]["params"]["network_config"]["params"]["in_channels"] = num_in_channels  # type: ignore
        else:
            raise IOError("Cannot determine UNet type from configuration.")

        if (
            "parameterization" in original_config["model"]["params"]  # type: ignore
            and original_config["model"]["params"]["parameterization"] == "v"  # type: ignore
        ):
            if prediction_type is None:
                # NOTE: For stable diffusion 2 base it is recommended to pass `prediction_type=="epsilon"`
                # as it relies on a brittle global step parameter here
                prediction_type = "epsilon" if global_step == 875000 else "v_prediction"
            if image_size is None:
                # NOTE: For stable diffusion 2 base one has to pass `image_size==512`
                # as it relies on a brittle global step parameter here
                image_size = 512 if global_step == 875000 else 768  # type: ignore[unreachable]
        else:
            if prediction_type is None:
                prediction_type = "epsilon"
            if image_size is None:
                image_size = 512  # type: ignore[unreachable]

        model_type = None
        if (
            "cond_stage_config" in original_config.model.params
            and original_config.model.params.cond_stage_config is not None
        ):
            model_type = original_config.model.params.cond_stage_config.target.split(".")[-1]
        elif original_config.model.params.network_config is not None:
            if original_config.model.params.network_config.params.context_dim == 2048:
                model_type = "SDXL"
            else:
                model_type = "SDXL-Refiner"

        is_sdxl = isinstance(model_type, str) and model_type.startswith("SDXL")
        is_sdxl_turbo = is_sdxl and "denoiser.sigmas" in checkpoint
        is_segmind = model_type == "SDXL" and "model.diffusion_model.output_blocks.0.1.transformer_blocks.2.attn1.to_k.weight" not in checkpoint

        num_train_timesteps = 1000  # Default is SDXL
        if "timesteps" in original_config.model.params:
            # SD 1 or 2
            num_train_timesteps = original_config.model.params.timesteps

        if is_sdxl:
            image_size = 1024
            scheduler_dict = {
                "beta_schedule": "scaled_linear",
                "beta_start": 0.00085,
                "beta_end": 0.012,
                "interpolation_type": "linear",
                "num_train_timesteps": num_train_timesteps,
                "prediction_type": "epsilon",
                "sample_max_value": 1.0,
                "set_alpha_to_one": False,
                "skip_prk_steps": True,
                "steps_offset": 1,
                "timestep_spacing": "trailing" if is_sdxl_turbo else "leading",
            }
            scheduler = EulerDiscreteScheduler.from_config(scheduler_dict)
            scheduler_type = "euler"
        else:
            beta_start = original_config.model.params.linear_start
            beta_end = original_config.model.params.linear_end
            scheduler = DDIMScheduler(
                beta_end=beta_end,
                beta_schedule="scaled_linear",
                beta_start=beta_start,
                num_train_timesteps=num_train_timesteps,
                steps_offset=1,
                clip_sample=False,
                set_alpha_to_one=False,
                prediction_type=prediction_type,
            )

        # make sure scheduler works correctly with DDIM
        scheduler.register_to_config(clip_sample=False)

        if scheduler_type == "pndm":
            config = dict(scheduler.config)
            config["skip_prk_steps"] = True
            scheduler = PNDMScheduler.from_config(config)
        elif scheduler_type == "lms":
            scheduler = LMSDiscreteScheduler.from_config(scheduler.config)
        elif scheduler_type == "heun":
            scheduler = HeunDiscreteScheduler.from_config(scheduler.config)
        elif scheduler_type == "euler":
            scheduler = EulerDiscreteScheduler.from_config(scheduler.config)
        elif scheduler_type == "euler-ancestral":
            scheduler = EulerAncestralDiscreteScheduler.from_config(scheduler.config)
        elif scheduler_type == "dpm":
            scheduler = DPMSolverMultistepScheduler.from_config(scheduler.config)
        elif scheduler_type == "ddim":
            scheduler = scheduler
        else:
            raise ValueError(f"Scheduler of type {scheduler_type} doesn't exist!")

        task_callback("Loading UNet")
        if is_segmind:
            logger.debug("Detected segmind distilled model.")
            unet_config = cls.get_config_from_url(
                cache_dir,
                "https://huggingface.co/segmind/Segmind-Vega/raw/main/unet/config.json?filename=segmind-vega-unet-config.json"
            )
        else:
            unet_config = create_unet_diffusers_config(original_config, image_size=image_size)

        unet_config["upcast_attention"] = upcast_attention
        if is_sdxl_turbo:
            logger.debug("Lowering sample size for turbo.")
            unet_config["sample_size"] = 64

        unet = cls.create_unet(
            unet_config,
            cache_dir=cache_dir,
            motion_dir=motion_dir,
            motion_module=motion_module,
            is_sdxl=is_sdxl,
            is_inpainter=is_inpainter,
            task_callback=task_callback,
            position_encoding_truncate_length=position_encoding_truncate_length,
            position_encoding_scale_length=position_encoding_scale_length,
            **unet_kwargs
    	)

        if is_segmind:
            # Add middle blocks back in temporarily
            checkpoint["model.diffusion_model.middle_block.1.temporary"] = torch.ones((2, 2), dtype=torch.float16)
            checkpoint["model.diffusion_model.middle_block.2.temporary"] = torch.ones((2, 2), dtype=torch.float16)

        converted_unet_checkpoint = convert_ldm_unet_checkpoint(
            checkpoint,
            unet_config,
            path=checkpoint_path,
            extract_ema=extract_ema
        )

        if is_segmind:
            # Remove temporarily added middle blocks
            for key in list(converted_unet_checkpoint.keys()):
                if "mid_block.resnets.1" in key or "mid_block.attentions.0" in key:
                    converted_unet_checkpoint.pop(key)

        unet_keys = len(list(converted_unet_checkpoint.keys()))
        logger.debug(f"Loading {unet_keys} keys into UNet state dict (non-strict)")

        unet.load_state_dict(converted_unet_checkpoint, strict=False)

        # Convert the VAE model.
        if vae is None:
            task_callback("Loading Default VAE")
            vae_config = create_vae_diffusers_config(original_config, image_size=image_size)
            converted_vae_checkpoint = convert_ldm_vae_checkpoint(checkpoint, vae_config)

            if (
                "model" in original_config
                and "params" in original_config.model
                and "scale_factor" in original_config.model.params
            ):
                vae_scale_factor = original_config.model.params.scale_factor
            else:
                vae_scale_factor = 0.18215  # default SD scaling factor

            vae_config["scaling_factor"] = vae_scale_factor

            vae = AutoencoderKL(**vae_config)
            vae_keys = len(list(converted_vae_checkpoint.keys()))
            logger.debug(f"Loading {vae_keys} keys into Autoencoder state dict (strict). Autoencoder scale is {vae_config['scaling_factor']}")
            vae.load_state_dict(converted_vae_checkpoint)

        if offload_models:
            logger.debug("Offloading enabled; sending VAE to CPU")
            vae.to("cpu")
            empty_cache()

        if load_safety_checker:
            safety_checker_path = "CompVis/stable-diffusion-safety-checker"
            task_callback(f"Loading safety checker {safety_checker_path}")
            safety_checker = StableDiffusionSafetyChecker.from_pretrained(
                safety_checker_path,
                cache_dir=cache_dir
            )
            if offload_models:
                logger.debug("Offloading enabled; sending safety checker to CPU")
                safety_checker.to("cpu")
                empty_cache()
            task_callback(f"Initializing feature extractor from repository {safety_checker_path}")
            feature_extractor = AutoFeatureExtractor.from_pretrained(
                safety_checker_path,
                cache_dir=cache_dir
            )
        else:
            safety_checker = None
            feature_extractor = None

        # Convert the text model and instantiate.
        if model_type == "FrozenOpenCLIPEmbedder":
            # SD V2
            tokenizer_path = "stabilityai/stable-diffusion-2"

            task_callback(f"Loading tokenizer {tokenizer_path}")

            tokenizer = CLIPTokenizer.from_pretrained(
                tokenizer_path,
                subfolder="tokenizer",
                cache_dir=cache_dir
            )

            text_model = convert_open_clip_checkpoint(
                checkpoint,
                tokenizer_path,
                subfolder="text_encoder"
            )
            if offload_models:
                logger.debug("Offloading enabled; sending text encoder to CPU")
                text_model.to("cpu")
                empty_cache()

            kwargs["text_encoder_2"] = None
            kwargs["tokenizer_2"] = None

            pipe = cls(
                vae=vae,
                text_encoder=text_model,
                tokenizer=tokenizer,
                unet=unet, # type: ignore[arg-type]
                scheduler=scheduler,
                safety_checker=safety_checker,
                feature_extractor=feature_extractor,
                **kwargs
            )
        elif model_type == "FrozenCLIPEmbedder":
            # SD V1
            tokenizer_path = "openai/clip-vit-large-patch14"

            task_callback(f"Loading tokenizer {tokenizer_path}")

            tokenizer = CLIPTokenizer.from_pretrained(
                tokenizer_path,
                cache_dir=cache_dir
            )

            text_model = convert_ldm_clip_checkpoint(checkpoint)
            if offload_models:
                logger.debug("Offloading enabled; sending text encoder to CPU")
                text_model.to("cpu")
                empty_cache()

            kwargs["text_encoder_2"] = None
            kwargs["tokenizer_2"] = None
            pipe = cls(
                vae=vae,
                vae_preview=vae_preview,
                text_encoder=text_model,
                tokenizer=tokenizer,
                unet=unet, # type: ignore[arg-type]
                scheduler=scheduler,
                safety_checker=safety_checker,
                feature_extractor=feature_extractor,
                **kwargs,
            )
        elif model_type == "SDXL":
            clip_vit_l_path = "openai/clip-vit-large-patch14"
            openclip_vit_g_path = "laion/CLIP-ViT-bigG-14-laion2B-39B-b160k"
            playground_v2_path = "playgroundai/playground-v2-1024px-aesthetic"
            segmind_vega_path = "segmind/Segmind-Vega"

            is_playground_v2 = "conditioner.embedders.0.transformer.text_model.embeddings.position_ids" not in checkpoint and not is_segmind

            if is_segmind:
                tokenizer_path = segmind_vega_path
                subfolder = "tokenizer"
            elif is_playground_v2:
                tokenizer_path = playground_v2_path
                subfolder = "tokenizer"
            else:
                tokenizer_path = clip_vit_l_path
                subfolder = None

            task_callback(f"Loading tokenizer 1 {tokenizer_path}")
            tokenizer = CLIPTokenizer.from_pretrained(
                tokenizer_path,
                cache_dir=cache_dir,
                subfolder=subfolder,
            )

            text_encoder = convert_ldm_clip_checkpoint(checkpoint)

            if is_segmind:
                tokenizer_2_path = segmind_vega_path
                subfolder_2 = "tokenizer_2"
            elif is_playground_v2:
                tokenizer_2_path = playground_v2_path
                subfolder_2 = "tokenizer_2"
            else:
                tokenizer_2_path = openclip_vit_g_path
                subfolder_2 = None
                
            task_callback(f"Loading tokenizer 2 {tokenizer_2_path}")

            tokenizer_2 = CLIPTokenizer.from_pretrained(
                tokenizer_2_path,
                cache_dir=cache_dir,
                subfolder=subfolder_2,
                pad_token="!"
            )
            text_encoder_2 = convert_open_clip_checkpoint(
                checkpoint,
                openclip_vit_g_path,
                prefix="conditioner.embedders.1.model.",
                has_projection=True,
                projection_dim=1280,
            )

            if offload_models:
                logger.debug("Offloading enabled; sending text encoder 1 and 2 to CPU")
                text_encoder.to("cpu")
                text_encoder_2.to("cpu")
                empty_cache()

            pipe = cls(
                vae=vae,
                vae_preview=vae_preview,
                text_encoder=text_encoder,
                text_encoder_2=text_encoder_2,
                tokenizer=tokenizer,
                tokenizer_2=tokenizer_2,
                unet=unet, # type: ignore[arg-type]
                scheduler=scheduler,
                safety_checker=safety_checker,
                feature_extractor=feature_extractor,
                force_zeros_for_empty_prompt=True,
                **kwargs,
            )
        elif model_type == "SDXL-Refiner":
            tokenizer_2_path = "laion/CLIP-ViT-bigG-14-laion2B-39B-b160k"
            task_callback(f"Loading tokenizer {tokenizer_2_path}")
            tokenizer_2 = CLIPTokenizer.from_pretrained(
                tokenizer_2_path,
                cache_dir=cache_dir,
                pad_token="!"
            )
            text_encoder_2 = convert_open_clip_checkpoint(
                checkpoint,
                tokenizer_2_path,
                prefix="conditioner.embedders.0.model.",
                has_projection=True,
                projection_dim=1280,
            )

            if offload_models:
                logger.debug("Offloading enabled; sending text encoder 2 to CPU")
                text_encoder_2.to("cpu")
                empty_cache()

            pipe = cls(
                vae=vae,
                vae_preview=vae_preview,
                text_encoder=None,
                text_encoder_2=text_encoder_2,
                tokenizer=None,
                tokenizer_2=tokenizer_2,
                unet=unet, # type: ignore[arg-type]
                scheduler=scheduler,
                safety_checker=safety_checker,
                feature_extractor=feature_extractor,
                force_zeros_for_empty_prompt=False,
                requires_aesthetic_score=True,
                **kwargs,
            )
        else:
            raise ValueError(f"Unsupported model type {model_type}")
        if torch_dtype is not None:
            return pipe.to(torch_dtype=torch_dtype) # type: ignore[attr-defined]
        return pipe

    @property
    def is_sdxl(self) -> bool:
        """
        Returns true if this is using SDXL (base or refiner)
        """
        return self.tokenizer_2 is not None and self.text_encoder_2 is not None
    
    @property
    def is_sdxl_refiner(self) -> bool:
        """
        Returns true if this is using SDXL refiner
        """
        return self.is_sdxl and self.tokenizer is None and self.text_encoder is None
    
    @property
    def is_sdxl_base(self) -> bool:
        """
        Returns true if this is using SDXL base
        """
        return self.is_sdxl and self.tokenizer is not None and self.text_encoder is not None

    @property
    def module_size(self) -> int:
        """
        Returns the size of the pipeline models in bytes.
        """
        size = 0
        for module in self.get_modules():
            module_size = 0
            for param in module.parameters():
                size += param.nelement() * param.element_size()
            for buffer in module.buffers():
                size += buffer.nelement() * buffer.element_size()
        return size

    @property
    def is_inpainting_unet(self) -> bool:
        """
        Returns true if this is an inpainting UNet (9-channel)
        """
        return self.unet.config.in_channels == 9 # type: ignore[attr-defined]

    def get_sparse_controlnet_config(self, use_simplified_condition_embedding: bool) -> Dict[str, Any]:
        """
        Gets configuration for the sparse controlnet.
        """
        return {
            "set_noisy_sample_input_to_zero": True,
            "use_simplified_condition_embedding": use_simplified_condition_embedding,
            "conditioning_channels": 4 if use_simplified_condition_embedding else 3,
            "use_motion_module": False,
        }

    def get_sparse_controlnet(
        self,
        controlnet: Literal["sparse-rgb", "sparse-scribble"],
        cache_dir: str,
        task_callback: Optional[Callable[[str], None]]=None,
    ) -> SparseControlNetModel:
        """
        Loads a sparse controlnet from the UNet
        """
        if controlnet == "sparse-rgb":
            controlnet_path = CONTROLNET_SPARSE_RGB
        elif controlnet == "sparse-scribble":
            controlnet_path = CONTROLNET_SPARSE_SCRIBBLE
        else:
            raise ValueError(f"Unknown ControlNet {controlnet}")

        use_simplified_condition_embedding = controlnet == "sparse-rgb"
        sparse_controlnet_config = self.get_sparse_controlnet_config(use_simplified_condition_embedding)

        # Prepare UNet
        self.unet.config.num_attention_heads = 8 # type: ignore[attr-defined]
        self.unet.config.projection_class_embeddings_input_dim = None # type: ignore[attr-defined]

        # Create model
        controlnet_model = SparseControlNetModel.from_unet(
            self.unet,
            controlnet_additional_kwargs=sparse_controlnet_config
        )

        if task_callback is not None and not os.path.exists(os.path.join(cache_dir, os.path.basename(controlnet_path))):
            task_callback(f"Downloading {controlnet_path}")

        controlnet_module = check_download_to_dir(
            controlnet_path,
            cache_dir,
            text_callback=task_callback
        )
        controlnet_state_dict = load_state_dict(controlnet_module)
        if "controlnet" in controlnet_state_dict:
            controlnet_state_dict = controlnet_state_dict["controlnet"] # type: ignore[assignment]
        controlnet_state_dict.pop("animatediff_config", "")
        if not sparse_controlnet_config.get("use_motion_module", False):
            for key in list (controlnet_state_dict.keys()):
                if "motion" in key or "temporal" in key:
                    controlnet_state_dict.pop(key)
        else:
            # Check if we need to adjust PE tensors
            scale_length = getattr(self.unet, "position_encoding_scale_length")
            truncate_length = getattr(self.unet, "position_encoding_truncate_length")

            if scale_length or truncate_length:
                logger.info(f"Adjusting ControlNet position encoder tensors, will truncate to length '{truncate_length}' and/or scale to length '{scale_length}'")
                for key in controlnet_state_dict:
                    if key.endswith(".pe"):
                        if truncate_length:
                            controlnet_state_dict[key] = controlnet_state_dict[key][:, :truncate_length] # type: ignore[index]
                        if scale_length:
                            shape = controlnet_state_dict[key].shape # type: ignore[union-attr]
                            tensor = rearrange(controlnet_state_dict[key], "(t b) f d -> t b f d", t=1)
                            tensor = torch.nn.functional.interpolate(tensor, size=(scale_length, shape[-1]), mode="bilinear")
                            controlnet_state_dict[key] = rearrange(tensor, "t b f d -> (t b) f d") # type: ignore[assignment]
                            del tensor

        controlnet_model.load_state_dict(controlnet_state_dict)
        return controlnet_model

    def revert_scheduler(self) -> None:
        """
        Reverts the scheduler back to whatever the original was.
        """
        self.scheduler = self.scheduler_class.from_config(self.scheduler_config) # type: ignore[attr-defined]

    def get_size_from_module(self, module: torch.nn.Module) -> int:
        """
        Gets the size of a module in bytes
        """
        size = 0
        for param in module.parameters():
            size += param.nelement() * param.element_size()
        for buffer in module.buffers():
            size += buffer.nelement() * buffer.element_size()
        return size

    def get_modules(self) -> List[torch.nn.Module]:
        """
        Gets modules in this pipeline ordered in decreasing size.
        """
        modules = []
        module_names, _ = self._get_signature_keys(self) # type: ignore[attr-defined]
        for name in module_names:
            module = getattr(self, name, None)
            if isinstance(module, torch.nn.Module):
                modules.append(module)
        modules.sort(key = lambda item: self.get_size_from_module(item), reverse=True)
        return modules

    def align_unet(
        self,
        device: torch.device,
        dtype: torch.dtype,
        animation_frames: Optional[int] = None,
        motion_scale: Optional[float] = None,
        freeu_factors: Optional[Tuple[float, float, float, float]] = None,
        offload_models: bool = False
    ) -> None:
        """
        Makes sure the unet is on the device and text encoders are off.
        """
        if offload_models:
            if self.text_encoder:
                self.text_encoder.to("cpu")
            if self.text_encoder_2:
                self.text_encoder_2.to("cpu")
            empty_cache()
        if freeu_factors is None:
            if getattr(self, "_freeu_enabled", False): # Make sure we've enabled this at least once
                self.unet.disable_freeu()
        else:
            s1, s2, b1, b2 = freeu_factors
            logger.debug(f"Enabling FreeU with factors {s1=} {s2=} {b1=} {b2=}")
            self.unet.enable_freeu(s1=s1, s2=s2, b1=b1, b2=b2)
            self._freeu_enabled = True
        if animation_frames: 
            try:
                if motion_scale:
                    logger.debug(f"Setting motion attention scale to {motion_scale}")
                    self.unet.set_motion_attention_scale(motion_scale)
                else:
                    self.unet.reset_motion_attention_scale()
            except AttributeError:
                raise RuntimeError("Couldn't set motion attention scale - was this pipeline initialized with the right UNet?")
        self.unet.to(device=device, dtype=dtype)

    def run_safety_checker(
        self,
        output: np.ndarray,
        device: torch.device,
        dtype: torch.dtype
    ) -> Tuple[np.ndarray, List[bool]]:
        """
        Override parent run_safety_checker to make sure safety checker is aligned
        """
        if self.safety_checking_disabled:
            return (output, [False] * len(output)) # Disabled after being enabled (likely temporary)
        if self.safety_checker is not None:
            self.safety_checker.to(device)
        return super(EnfugueStableDiffusionPipeline, self).run_safety_checker(output, device, dtype) # type: ignore[misc]

    def load_ip_adapter(
        self,
        device: Union[str, torch.device],
        scale: float = 1.0,
        model: Optional[IP_ADAPTER_LITERAL]=None,
    ) -> None:
        """
        Loads the IP Adapter
        """
        if getattr(self, "ip_adapter", None) is None:
            raise RuntimeError("Pipeline does not have an IP adapter")

        if not self.ip_adapter_loaded:
            logger.debug("Loading IP adapter")
            self.ip_adapter.load( # type: ignore[union-attr]
                self.unet,
                scale=scale,
                model=model,
                is_sdxl=self.is_sdxl,
                controlnets=self.controlnets
            )
            self.ip_adapter_loaded = True

    def get_image_embeds(
        self,
        image: PIL.Image.Image,
        num_results_per_prompt: int
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Uses the IP adapter to get prompt embeddings from the image
        """
        if getattr(self, "ip_adapter", None) is None:
            raise RuntimeError("Pipeline does not have an IP adapter")
        image_prompt_embeds, image_uncond_prompt_embeds = self.ip_adapter.probe(image) # type: ignore[union-attr]
        bs_embed, seq_len, _ = image_prompt_embeds.shape
        image_prompt_embeds = image_prompt_embeds.repeat(1, num_results_per_prompt, 1)
        image_prompt_embeds = image_prompt_embeds.view(bs_embed * num_results_per_prompt, seq_len, -1)
        image_uncond_prompt_embeds = image_uncond_prompt_embeds.repeat(1, num_results_per_prompt, 1)
        image_uncond_prompt_embeds = image_uncond_prompt_embeds.view(bs_embed * num_results_per_prompt, seq_len, -1)
        return image_prompt_embeds, image_uncond_prompt_embeds

    def encode_prompt(
        self,
        prompt: Optional[str],
        device: torch.device,
        num_results_per_prompt: int = 1,
        do_classifier_free_guidance: bool = False,
        negative_prompt: Optional[str] = None,
        prompt_embeds: Optional[torch.Tensor] = None,
        negative_prompt_embeds: Optional[torch.Tensor] = None,
        lora_scale: Optional[float] = None,
        prompt_2: Optional[str] = None,
        negative_prompt_2: Optional[str] = None,
        clip_skip: Optional[int] = None,
    ) -> Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]]:
        """
        Encodes the prompt into text encoder hidden states.
        See https://github.com/huggingface/diffusers/blob/main/src/diffusers/pipelines/stable_diffusion_xl/pipeline_stable_diffusion_xl.py
        """
        # set lora scale so that monkey patched LoRA
        # function of text encoder can correctly access it
        if lora_scale is not None and isinstance(self, LoraLoaderMixin): # type: ignore[unreachable]
            self._lora_scale = lora_scale # type: ignore[unreachable]

        if self.is_sdxl_base:
            prompts = [
                prompt if prompt else prompt_2,
                prompt_2 if prompt_2 else prompt
            ]
            negative_prompts = [
                negative_prompt if negative_prompt else negative_prompt_2,
                negative_prompt_2 if negative_prompt_2 else negative_prompt
            ]
        else:
            if prompt and prompt_2:
                logger.debug("Merging prompt and prompt_2")
                prompt = merge_tokens(prompt, prompt_2)
            elif not prompt and prompt_2:
                logger.debug("Using prompt_2 for empty primary prompt")
                prompt = prompt_2
            
            if negative_prompt and negative_prompt_2:
                logger.debug("Merging negative_prompt and negative_prompt_2")
                negative_prompt = merge_tokens(negative_prompt, negative_prompt_2)
            elif not negative_prompt and negative_prompt_2:
                logger.debug("Using negative_prompt_2 for empty primary negative_prompt")
                negative_prompt = negative_prompt_2

            prompts = [prompt, prompt]
            negative_prompts = [negative_prompt, negative_prompt]

        # Align device
        dtype = torch.float32 if device.type == "cpu" else torch.float16
        if self.text_encoder:
            self.text_encoder = self.text_encoder.to(device, dtype=dtype)
        if self.text_encoder_2:
            self.text_encoder_2 = self.text_encoder_2.to(device, dtype=dtype)

        tokenizers = [self.tokenizer, self.tokenizer_2]
        text_encoders = [self.text_encoder, self.text_encoder_2]

        if prompt_embeds is None:
            prompt_embeds_list = []
            for tokenizer, text_encoder, prompt in zip(tokenizers, text_encoders, prompts):
                if tokenizer is None or text_encoder is None:
                    continue

                if self.is_sdxl:
                    return_type = ReturnedEmbeddingsType.PENULTIMATE_HIDDEN_STATES_NON_NORMALIZED
                elif clip_skip:
                    return_type = ReturnedEmbeddingsType.PENULTIMATE_HIDDEN_STATES_NORMALIZED
                else:
                    return_type = ReturnedEmbeddingsType.LAST_HIDDEN_STATES_NORMALIZED

                compel = PromptEncoder(
                    text_encoder=text_encoder,
                    tokenizer=tokenizer,
                    returned_embeddings_type=return_type,
                    requires_pooled=self.is_sdxl
                )
                compel.clip_skip = 0 if not clip_skip else clip_skip

                if self.is_sdxl:
                    prompt_embeds, pooled_prompt_embeds = compel([prompt])
                else:
                    prompt_embeds = compel([prompt])

                bs_embed, seq_len, _ = prompt_embeds.shape  # type: ignore
                # duplicate text embeddings for each generation per prompt, using mps friendly method
                prompt_embeds = prompt_embeds.repeat(1, num_results_per_prompt, 1)  # type: ignore
                prompt_embeds = prompt_embeds.view(bs_embed * num_results_per_prompt, seq_len, -1)

                if self.is_sdxl:
                    prompt_embeds_list.append(prompt_embeds)

            if self.is_sdxl:
                prompt_embeds = torch.concat(prompt_embeds_list, dim=-1)

        # get unconditional embeddings for classifier free guidance
        zero_out_negative_prompt = negative_prompt is None and self.config.force_zeros_for_empty_prompt # type: ignore[attr-defined]
        negative_pooled_prompt_embeds: Optional[torch.Tensor] = None
        if self.is_sdxl and do_classifier_free_guidance and negative_prompt_embeds is None and zero_out_negative_prompt:
            negative_prompt_embeds = torch.zeros_like(prompt_embeds)  # type: ignore
            negative_pooled_prompt_embeds = torch.zeros_like(pooled_prompt_embeds)
        elif do_classifier_free_guidance and negative_prompt_embeds is None:
            negative_prompt_embeds_list = []

            for tokenizer, text_encoder, negative_prompt in zip(tokenizers, text_encoders, negative_prompts):
                if tokenizer is None or text_encoder is None:
                    continue

                compel = PromptEncoder(
                    text_encoder=text_encoder,
                    tokenizer=tokenizer,
                    returned_embeddings_type=return_type,
                    requires_pooled=self.is_sdxl
                )
                compel.clip_skip = 0 if not clip_skip else clip_skip

                if self.is_sdxl:
                    negative_prompt_embeds, negative_pooled_prompt_embeds = compel([negative_prompt or ""])
                else:
                    negative_prompt_embeds = compel([negative_prompt or ""])

                if do_classifier_free_guidance:
                    # duplicate unconditional embeddings for each generation per prompt, using mps friendly method
                    seq_len = negative_prompt_embeds.shape[1]  # type: ignore

                    negative_prompt_embeds = negative_prompt_embeds.to(dtype=text_encoder.dtype, device=device)  # type: ignore

                    negative_prompt_embeds = negative_prompt_embeds.repeat(1, num_results_per_prompt, 1)
                    negative_prompt_embeds = negative_prompt_embeds.view(num_results_per_prompt, seq_len, -1)

                    # For classifier free guidance, we need to do two forward passes.
                    # Here we concatenate the unconditional and text embeddings into a single batch
                    # to avoid doing two forward passes
                    if not self.is_sdxl:
                        prompt_embeds = torch.cat([negative_prompt_embeds, prompt_embeds])  # type: ignore
                if self.is_sdxl:
                    negative_prompt_embeds_list.append(negative_prompt_embeds)
            if self.is_sdxl:
                negative_prompt_embeds = torch.concat(negative_prompt_embeds_list, dim=-1)

        if self.is_sdxl:
            pooled_prompt_embeds = pooled_prompt_embeds.repeat(1, num_results_per_prompt).view(
                bs_embed * num_results_per_prompt, -1
            )
            if do_classifier_free_guidance and negative_pooled_prompt_embeds is not None:
                negative_pooled_prompt_embeds = negative_pooled_prompt_embeds.repeat(1, num_results_per_prompt).view(
                    bs_embed * num_results_per_prompt, -1
                )
            return prompt_embeds, negative_prompt_embeds, pooled_prompt_embeds, negative_pooled_prompt_embeds  # type: ignore
        return prompt_embeds  # type: ignore

    @contextmanager
    def get_runtime_context(
        self,
        batch_size: int,
        animation_frames: Optional[int],
        device: Union[str, torch.device],
        ip_adapter_scale: Optional[Union[List[float], float]] = None,
        step_complete: Optional[Callable[[bool], None]] = None
    ) -> Iterator[None]:
        """
        Builds the runtime context, which ensures everything is on the right devices
        """
        if isinstance(device, str):
            device = torch.device(device)
        if ip_adapter_scale is not None:
            self.ip_adapter.set_scale( # type: ignore[union-attr]
                unet=self.unet,
                scale=ip_adapter_scale
            )
        if self.text_encoder is not None:
            self.text_encoder.to(device)
        if self.text_encoder_2 is not None:
            self.text_encoder_2.to(device)

        if device.type == "cpu":
            with torch.autocast("cpu"):
                yield
        elif ip_adapter_scale is not None:
            with self.ip_adapter.context(): # type: ignore[union-attr]
                yield
        else:
            yield

    def load_lycoris_weights(
        self,
        weights_path: str,
        multiplier: float = 1.0,
        dtype: torch.dtype = torch.float32,
        **kwargs: Any,
    ) -> None:
        """
        Loads lycoris weights using the official package
        """
        name, ext = os.path.splitext(os.path.basename(weights_path))
        if ext == ".safetensors":
            state_dict = safetensors.torch.load_file(weights_path, device="cpu")
        else:
            state_dict = torch.load(weights_path, map_location="cpu")

        while "state_dict" in state_dict:
            state_dict = state_dict["state_dict"] # type: ignore[assignment]

        from lycoris.utils import merge

        merge((self.text_encoder, self.vae, self.unet), state_dict, multiplier, device="cpu")

    def load_lora_weights(
        self,
        pretrained_model_name_or_path_or_dict: Union[str, Dict[str, torch.Tensor]],
        multiplier: float = 1.0,
        dtype: torch.dtype = torch.float32,
        **kwargs: Any,
    ) -> None:
        """
        Call the appropriate adapted fix based on pipeline class
        """
        try:
            return self.load_flexible_lora_weights(
                pretrained_model_name_or_path_or_dict,
                multiplier=multiplier,
                dtype=dtype,
                **kwargs
            )
        except (AttributeError, KeyError) as ex:
            if self.is_sdxl:
                message = "Are you trying to use a Stable Diffusion 1.5 LoRA with this Stable Diffusion XL pipeline?"
            else:
                message = "Are you trying to use a Stable Diffusion XL LoRA with this Stable Diffusion 1.5 pipeline?"
            raise IOError(f"Received {type(ex).__name__} loading LoRA. {message}")

    def load_sdxl_lora_weights(
        self, 
        pretrained_model_name_or_path_or_dict: Union[str, Dict[str, torch.Tensor]],
        multiplier: float = 1.0,
        **kwargs: Any
    ) -> None:
        """
        Fix adapted from https://github.com/huggingface/diffusers/blob/4a4cdd6b07a36bbf58643e96c9a16d3851ca5bc5/src/diffusers/pipelines/stable_diffusion_xl/pipeline_stable_diffusion_xl.py
        """
        state_dict, network_alphas = self.lora_state_dict( # type: ignore[attr-defined]
            pretrained_model_name_or_path_or_dict,
            unet_config=self.unet.config,
            **kwargs,
        )
        self.load_lora_into_unet( # type: ignore[attr-defined]
            state_dict,
            network_alphas=network_alphas,
            unet=self.unet,
            _pipeline=self,
        )

        text_encoder_state_dict = dict([
            (k, v)
            for k, v in state_dict.items()
            if "text_encoder." in k
        ])
        text_encoder_keys = len(text_encoder_state_dict)

        if text_encoder_keys > 0:
            logger.debug(f"Loading {text_encoder_keys} keys into primary text encoder with multiplier {multiplier}")
            self.load_lora_into_text_encoder( # type: ignore[attr-defined]
                text_encoder_state_dict,
                network_alphas=network_alphas,
                text_encoder=self.text_encoder,
                prefix="text_encoder",
                lora_scale=multiplier,
                _pipeline=self,
            )

        text_encoder_2_state_dict = dict([
            (k, v)
            for k, v in state_dict.items()
            if "text_encoder_2." in k
        ])
        text_encoder_2_keys = len(text_encoder_2_state_dict)

        if text_encoder_2_keys > 0:
            logger.debug(f"Loading {text_encoder_2_keys} keys into secondary text encoder with multiplier {multiplier}")
            self.load_lora_into_text_encoder( # type: ignore[attr-defined]
                text_encoder_2_state_dict,
                network_alphas=network_alphas,
                text_encoder=self.text_encoder_2,
                prefix="text_encoder_2",
                lora_scale=multiplier,
                _pipeline=self,
            )

    def load_motion_lora_weights(
        self,
        state_dict: Dict[str, torch.Tensor],
        multiplier: float = 1.0,
        dtype: torch.dtype = torch.float32
    ) -> None:
        """
        Don't do anything in base pipeline
        """
        logger.warning("Ignoring motion LoRA for non-animation pipeline")

    def load_flexible_lora_weights(
        self,
        pretrained_model_name_or_path_or_dict: Union[str, Dict[str, torch.Tensor]],
        multiplier: float = 1.0,
        dtype: torch.dtype = torch.float32,
        **kwargs: Any,
    ) -> None:
        """
        Fix adapted from here: https://github.com/huggingface/diffusers/issues/3064#issuecomment-1545013909
        """
        LORA_PREFIX_UNET = "lora_unet"
        LORA_PREFIX_TEXT_ENCODER = "lora_te"

        state_dict = load_state_dict(pretrained_model_name_or_path_or_dict) # type: ignore[arg-type]
        while "state_dict" in state_dict:
            state_dict = state_dict["state_dict"] # type: ignore[assignment]
        state_dict.pop("animatediff_config", "")
        if any(["motion_module" in key for key in state_dict.keys()]):
            return self.load_motion_lora_weights(
                state_dict, # type: ignore[arg-type]
                multiplier=multiplier,
                dtype=dtype
            )
        if self.is_sdxl:
            return self.load_sdxl_lora_weights(
                state_dict, # type: ignore[arg-type]
                multiplier=multiplier,
                dtype=dtype
            )
        return super(EnfugueStableDiffusionPipeline, self).load_lora_weights( # type: ignore[misc]
            state_dict,
            multiplier=multiplier,
            dtype=dtype
        )

    def load_textual_inversion(self, inversion_path: str, **kwargs: Any) -> None:
        """
        Loads textual inversion
        Temporary implementation from https://github.com/huggingface/diffusers/issues/4405
        """
        try:
            if not self.is_sdxl:
                return super(EnfugueStableDiffusionPipeline, self).load_textual_inversion(inversion_path, **kwargs) # type: ignore[misc]

            logger.debug(f"Using SDXL adaptation for textual inversion - Loading {inversion_path}")
            if inversion_path.endswith("safetensors"):
                from safetensors import safe_open

                inversion = {}
                with safe_open(inversion_path, framework="pt", device="cpu") as f: # type: ignore[attr-defined]
                    for key in f.keys():
                        inversion[key] = f.get_tensor(key)
            else:
                inversion = torch.load(inversion_path, map_location="cpu")

            for i, (embedding_1, embedding_2) in enumerate(zip(inversion["clip_l"], inversion["clip_g"])):
                token = f"sksd{chr(i+65)}"
                if self.tokenizer is not None:
                    self.tokenizer.add_tokens(token)
                if self.tokenizer_2 is not None:
                    self.tokenizer_2.add_tokens(token)
                if self.text_encoder is not None and self.tokenizer is not None:
                    token_id = self.tokenizer.convert_tokens_to_ids(token)
                    self.text_encoder.resize_token_embeddings(len(self.tokenizer))
                    self.text_encoder.get_input_embeddings().weight.data[token_id] = embedding_1
                if self.text_encoder_2 is not None:
                    if self.tokenizer_2 is not None:
                        token_id_2 = self.tokenizer_2.convert_tokens_to_ids(token)
                    elif self.tokenizer is not None:
                        token_id_2 = self.tokenizer.convert_tokens_to_ids(token)
                    else:
                        raise ValueError("No tokenizer, cannot add inversion to encoder")
                    self.text_encoder_2.resize_token_embeddings(len(self.tokenizer))
                    self.text_encoder_2.get_input_embeddings().weight.data[token_id_2] = embedding_2
        except (AttributeError, KeyError) as ex:
            if self.is_sdxl:
                message = "Are you trying to use a Stable Diffusion 1.5 textual inversion with this Stable Diffusion XL pipeline?"
            else:
                message = "Are you trying to use a Stable Diffusion XL textual inversion with this Stable Diffusion 1.5 pipeline?"
            raise IOError(f"Received {type(ex).__name__} loading textual inversion. {message}")

    def inject_unet(self, checkpoint_path: str, strict: bool=False) -> None:
        """
        Injects weights into the UNet.
        """
        for key, tensor in iterate_state_dict(checkpoint_path):
            key_parts = key.split(".")
            current_layer = self.unet
            for key_part in key_parts[:-1]:
                current_layer = getattr(current_layer, key_part, None) # type: ignore[assignment]
                if current_layer is None:
                    break # type: ignore[unreachable]
            if current_layer is None:
                if strict: # type: ignore[unreachable]
                    raise IOError(f"Couldn't find a layer to inject key {key} in.")
                continue
            layer_param = getattr(current_layer, key_parts[-1], None)
            if layer_param is None:
                if strict:
                    raise IOError(f"Couldn't get current weight for {key}")
                continue
            layer_param.data += tensor

    def denormalize_latents(self, latents: torch.Tensor) -> torch.Tensor:
        """
        Denomalizes image data from [-1, 1] to [0, 1]
        """
        return (latents / 2 + 0.5).clamp(0, 1)

    def prepare_mask_and_image(
        self,
        mask: Union[np.ndarray, PIL.Image.Image, torch.Tensor],
        image: Union[np.ndarray, PIL.Image.Image, torch.Tensor],
        return_image: bool = False
    ) -> Union[
        Tuple[torch.Tensor, torch.Tensor],
        Tuple[torch.Tensor, torch.Tensor, torch.Tensor]
    ]:
        """
        Prepares a mask and image for inpainting.
        """
        if isinstance(image, torch.Tensor):
            if not isinstance(mask, torch.Tensor):
                raise TypeError(f"`image` is a torch.Tensor but `mask` (type: {type(mask)} is not")

            # Batch single image
            if image.ndim == 3:
                assert image.shape[0] == 3, "Image outside a batch should be of shape (3, H, W)"
                image = image.unsqueeze(0)

            # Batch and add channel dim for single mask
            if mask.ndim == 2:
                mask = mask.unsqueeze(0).unsqueeze(0)

            # Batch single mask or add channel dim
            if mask.ndim == 3:
                # Single batched mask, no channel dim or single mask not batched but channel dim
                if mask.shape[0] == 1:
                    mask = mask.unsqueeze(0)

                # Batched masks no channel dim
                else:
                    mask = mask.unsqueeze(1)

            assert image.ndim == 4 and mask.ndim == 4, "Image and Mask must have 4 dimensions"
            assert image.shape[-2:] == mask.shape[-2:], "Image and Mask must have the same spatial dimensions"
            assert image.shape[0] == mask.shape[0], "Image and Mask must have the same batch size"

            # Check image is in [-1, 1]
            if image.min() < -1 or image.max() > 1:
                raise ValueError("Image should be in [-1, 1] range")

            # Check mask is in [0, 1]
            if mask.min() < 0 or mask.max() > 1:
                raise ValueError("Mask should be in [0, 1] range")

            # Binarize mask
            mask[mask < 0.5] = 0
            mask[mask >= 0.5] = 1

            # Image as float32
            image = image.to(dtype=torch.float32)
        elif isinstance(mask, torch.Tensor):
            raise TypeError(f"`mask` is a torch.Tensor but `image` (type: {type(image)} is not")
        else:
            # preprocess image
            if isinstance(image, (PIL.Image.Image, np.ndarray)):
                image = [image]

            if isinstance(image, list) and isinstance(image[0], PIL.Image.Image):
                image = [np.array(i.convert("RGB"))[None, :] for i in image] # type: ignore[index]
                image = np.concatenate(image, axis=0)
            elif isinstance(image, list) and isinstance(image[0], np.ndarray):
                image = np.concatenate([i[None, :] for i in image], axis=0)

            image = image.transpose(0, 3, 1, 2) # type: ignore[attr-defined]
            image = torch.from_numpy(image).to(dtype=torch.float32) / 127.5 - 1.0

            # preprocess mask
            if isinstance(mask, (PIL.Image.Image, np.ndarray)):
                mask = [mask]

            if isinstance(mask, list) and isinstance(mask[0], PIL.Image.Image):
                mask = np.concatenate([np.array(m.convert("L"))[None, None, :] for m in mask], axis=0) # type: ignore[index]
                mask = mask.astype(np.float32) / 255.0
            elif isinstance(mask, list) and isinstance(mask[0], np.ndarray):
                mask = np.concatenate([m[None, None, :] for m in mask], axis=0)

            # binarize mask
            mask[mask < 0.5] = 0
            mask[mask >= 0.5] = 1
            mask = torch.from_numpy(mask)

        masked_image = image * (mask < 0.5)
        if return_image:
            return mask, masked_image, image
        return mask, masked_image

    def create_latents(
        self,
        batch_size: int,
        num_channels_latents: int,
        height: int,
        width: int,
        dtype: torch.dtype,
        device: Union[str, torch.device],
        generator: Optional[torch.Generator] = None,
        animation_frames: Optional[int] = None,
    ) -> torch.Tensor:
        """
        Creates random latents of a particular shape and type.
        """
        if not animation_frames:
            shape = (
                batch_size,
                num_channels_latents,
                height // self.vae_scale_factor,
                width // self.vae_scale_factor,
            )
        else:
            shape = ( # type: ignore[assignment]
                batch_size,
                num_channels_latents,
                animation_frames,
                height // self.vae_scale_factor,
                width // self.vae_scale_factor,
            )
        
        random_latents = randn_tensor(
            shape,
            generator=generator,
            device=torch.device(device) if isinstance(device, str) else device,
            dtype=dtype
        )

        return random_latents * self.scheduler.init_noise_sigma # type: ignore[attr-defined]

    def encode_image_unchunked(
        self,
        image: torch.Tensor,
        dtype: torch.dtype,
        generator: Optional[torch.Generator] = None
    ) -> torch.Tensor:
        """
        Encodes an image without chunking using the VAE.
        """
        if self.config.force_full_precision_vae: # type: ignore[attr-defined]
            self.vae.to(dtype=torch.float32)
            image = image.float()
        else:
            image = image.to(dtype=self.vae.dtype)
        latents = self.vae.encode(image).latent_dist.sample(generator) * self.vae.config.scaling_factor # type: ignore[attr-defined]
        if self.config.force_full_precision_vae: # type: ignore[attr-defined]
            self.vae.to(dtype=dtype)
        return latents.to(dtype=dtype)

    def encode_image(
        self,
        image: torch.Tensor,
        device: Union[str, torch.device],
        dtype: torch.dtype,
        chunker: Chunker,
        weight_builder: MaskWeightBuilder,
        generator: Optional[torch.Generator] = None,
        progress_callback: Optional[Callable[[bool], None]] = None,
        tiling: bool = False
    ) -> torch.Tensor:
        """
        Encodes an image in chunks using the VAE.
        """
        _, _, height, width = image.shape

        # Disable tiling during encoding
        tile = chunker.tile
        chunker.tile = False

        total_steps = chunker.num_chunks

        # Align device
        self.vae.to(device)

        if total_steps == 1 or not tiling:
            result = self.encode_image_unchunked(image, dtype, generator)
            if progress_callback is not None:
                progress_callback(True)
            # Re-enable tiling if asked for
            chunker.tile = tile
            return result

        chunks = chunker.chunks

        latent_height = height // self.vae_scale_factor
        latent_width = width // self.vae_scale_factor

        engine_latent_size = self.engine_size // self.vae_scale_factor
        num_channels = self.vae.config.latent_channels # type: ignore[attr-defined]

        count = torch.zeros((1, num_channels, latent_height, latent_width)).to(device=device)
        value = torch.zeros_like(count)

        if self.config.force_full_precision_vae: # type: ignore[attr-defined]
            self.vae.to(dtype=torch.float32)
            weight_builder.dtype = torch.float32
            image = image.float()
        else:
            self.vae.to(dtype=image.dtype)

        with weight_builder:
            for i, ((top, bottom), (left, right)) in enumerate(chunker.chunks):
                top_px = top * self.vae_scale_factor
                bottom_px = bottom * self.vae_scale_factor
                left_px = left * self.vae_scale_factor
                right_px = right * self.vae_scale_factor

                image_view = image[:, :, top_px:bottom_px, left_px:right_px]

                encoded_image = self.vae.encode(image_view).latent_dist.sample(generator).to(device)

                # Build weights
                multiplier = weight_builder(
                    mask_type=self.tiling_mask_type,
                    batch=1,
                    dim=num_channels,
                    width=right-left,
                    height=bottom-top,
                    unfeather_left=left==0,
                    unfeather_top=top==0,
                    unfeather_right=right==latent_width,
                    unfeather_bottom=bottom==latent_height,
                    **self.tiling_mask_kwargs
                )

                value[:, :, top:bottom, left:right] += encoded_image * multiplier
                count[:, :, top:bottom, left:right] += multiplier

                if progress_callback is not None:
                    progress_callback(True)

        # Re-enable tiling if asked for
        chunker.tile = tile
        if self.config.force_full_precision_vae: # type: ignore[attr-defined]
            self.vae.to(dtype=dtype)
            weight_builder.dtype = dtype
        return (torch.where(count > 0, value / count, value) * self.vae.config.scaling_factor).to(dtype=dtype) # type: ignore[attr-defined]

    def prepare_image_latents(
        self,
        image: torch.Tensor,
        timestep: torch.Tensor,
        batch_size: int,
        dtype: torch.dtype,
        device: Union[str, torch.device],
        chunker: Chunker,
        weight_builder: MaskWeightBuilder,
        generator: Optional[torch.Generator] = None,
        progress_callback: Optional[Callable[[bool], None]] = None,
        add_noise: bool = True,
        tiling: bool = False,
        animation_frames: Optional[int] = None
    ) -> torch.Tensor:
        """
        Prepares latents from an image, adding initial noise for img2img inference
        """
        def encoded() -> Iterator[torch.Tensor]:
            for i in image:
                if i.shape[1] == 4:
                    yield i
                else:
                    yield self.encode_image(
                        image=i.to(dtype=dtype, device=device),
                        device=device,
                        generator=generator,
                        dtype=dtype,
                        chunker=chunker,
                        weight_builder=weight_builder,
                        progress_callback=progress_callback,
                        tiling=tiling
                    )

        # these should all be [1, 4, h, w], collapse along batch dim
        latents = torch.cat(list(encoded()), dim=0).to(dtype) # type: ignore[assignment]

        if animation_frames:
            # Change from collapsing on batch dim to temporal dim
            latents = rearrange(latents, 't c h w -> c t h w').unsqueeze(0)
        
        if batch_size > latents.shape[0] and batch_size % latents.shape[0] == 0:
            # duplicate images to match batch size
            additional_image_per_prompt = batch_size // latents.shape[0]
            latents = torch.cat([latents] * additional_image_per_prompt, dim=0)
        elif batch_size > latents.shape[0] and batch_size % latents.shape[0] != 0:
            raise ValueError(
                f"Cannot duplicate `image` of batch size {latents.shape[0]} to {batch_size} text prompts."
            )

        if animation_frames and animation_frames > latents.shape[2]:
            # duplicate last image to match animation length
            latents = torch.cat([
                latents,
                latents.repeat(1, 1, animation_frames - latents.shape[2], 1, 1)
            ], dim=2)

        # add noise in accordance with timesteps
        if add_noise:
            shape = latents.shape
            noise = randn_tensor(
                shape,
                generator=generator,
                device=torch.device(device) if isinstance(device, str) else device,
                dtype=dtype
            )
            return self.scheduler.add_noise(latents, noise, timestep) # type: ignore[attr-defined]
        else:
            return latents

    def prepare_mask_latents(
        self,
        mask: torch.Tensor,
        image: torch.Tensor,
        batch_size: int,
        height: int,
        width: int,
        dtype: torch.dtype,
        device: Union[str, torch.device],
        chunker: Chunker,
        weight_builder: MaskWeightBuilder,
        generator: Optional[torch.Generator] = None,
        do_classifier_free_guidance: bool = False,
        progress_callback: Optional[Callable[[bool], None]] = None,
        animation_frames: Optional[int] = None,
        tiling: bool = False,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Prepares both mask and image latents for inpainting
        """
        tensor_height = height // self.vae_scale_factor
        tensor_width = width // self.vae_scale_factor
        tensor_size = (tensor_height, tensor_width)

        mask_latents = torch.Tensor().to(device)
        latents = torch.Tensor().to(device)

        if mask.shape[0] != image.shape[0]:
            # Should have been fixed by now, raise value error
            raise ValueError("Mask and image should be the same length.")

        for m, i in zip(mask, image):
            m = torch.nn.functional.interpolate(m, size=tensor_size)
            m = m.to(device=device, dtype=dtype)
            mask_latents = torch.cat([mask_latents, m.unsqueeze(0)])

            latents = torch.cat([
                latents,
                self.encode_image(
                    i,
                    device=device,
                    generator=generator,
                    dtype=dtype,
                    chunker=chunker,
                    weight_builder=weight_builder,
                    progress_callback=progress_callback,
                    tiling=tiling,
                ).unsqueeze(0).to(device=device, dtype=dtype)
            ])

        if animation_frames:
            latents = rearrange(latents, "t b c h w -> b c t h w")
            mask_latents = rearrange(mask_latents, "t b c h w -> b c t h w")

        # duplicate mask and latents for each generation per prompt, using mps friendly method
        if mask_latents.shape[0] < batch_size:
            if not batch_size % mask_latents.shape[0] == 0:
                raise ValueError(
                    "The passed mask_latents and the required batch size don't match. mask_latentss are supposed to be duplicated to"
                    f" a total batch size of {batch_size}, but {mask_latents.shape[0]} mask_latentss were passed. Make sure the number"
                    " of mask_latentss that you pass is divisible by the total requested batch size."
                )
            repeat_axes = [1 for i in range(len(mask_latents.shape)-1)]
            mask_latents = mask_latents.repeat(batch_size // mask_latents.shape[0], *repeat_axes)
        if latents.shape[0] < batch_size:
            if not batch_size % latents.shape[0] == 0:
                raise ValueError(
                    "The passed images and the required batch size don't match. Images are supposed to be duplicated"
                    f" to a total batch size of {batch_size}, but {latents.shape[0]} images were passed."
                    " Make sure the number of images that you pass is divisible by the total requested batch size."
                )
            repeat_axes = [1 for i in range(len(latents.shape)-1)]
            latents = latents.repeat(batch_size // latents.shape[0], *repeat_axes)

        # Duplicate mask and latents to match animation length, using mps friendly method:
        if animation_frames and mask_latents.shape[2] < animation_frames:
            mask_latents = mask_latents.repeat(1, 1, animation_frames - mask_latents.shape[2], 1, 1)
        if animation_frames and latents.shape[2] < animation_frames:
            latents = latents.repeat(1, 1, animation_frames - latents.shape[2], 1, 1)

        mask_latents = torch.cat([mask_latents] * 2) if do_classifier_free_guidance else mask_latents
        latents = torch.cat([latents] * 2) if do_classifier_free_guidance else latents

        # aligning device to prevent device errors when concating it with the latent model input
        mask_latents = mask_latents.to(device=device, dtype=dtype)
        latents = latents.to(device=device, dtype=dtype)

        return mask_latents, latents

    def get_timesteps(
        self,
        num_inference_steps: int,
        strength: Optional[float],
        denoising_start: Optional[float] = None
    ) -> Tuple[torch.Tensor, int]:
        """
        Gets the original timesteps from the scheduler based on strength when doing img2img
        """
        if denoising_start is None:
            if strength is None:
                raise ValueError("You must include at least one of 'denoising_start' or 'strength'")
            init_timestep = min(int(num_inference_steps * strength), num_inference_steps)
            t_start = max(num_inference_steps - init_timestep, 0)
        else:
            t_start = 0

        timesteps = self.scheduler.timesteps[t_start * self.scheduler.order :] # type: ignore[attr-defined]

        if denoising_start is not None:
            discrete_timestep_cutoff = int(
                round(
                    self.scheduler.config.num_train_timesteps # type: ignore[attr-defined]
                    - (denoising_start * self.scheduler.config.num_train_timesteps) # type: ignore[attr-defined]
                )
            )
            timesteps = list(filter(lambda ts: ts < discrete_timestep_cutoff, timesteps))
            return torch.tensor(timesteps), len(timesteps)
        return timesteps, num_inference_steps - t_start

    def get_add_time_ids(
        self,
        original_size: Tuple[int, int],
        crops_coords_top_left: Tuple[int, int],
        target_size: Tuple[int, int],
        dtype: torch.dtype,
        aesthetic_score: Optional[float] = None,
        negative_aesthetic_score: Optional[float] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Gets added time embedding vectors for SDXL
        """
        if not self.text_encoder_2:
            raise ValueError("Missing text encoder 2, incorrect call of `get_add_time_ids` on non-SDXL pipeline.")
        if (
            aesthetic_score is not None
            and negative_aesthetic_score is not None
            and self.config.requires_aesthetic_score # type: ignore[attr-defined]
        ):
            add_time_ids = list(original_size + crops_coords_top_left + (aesthetic_score,))
            add_neg_time_ids = list(original_size + crops_coords_top_left + (negative_aesthetic_score,))
        else:
            add_time_ids = list(original_size + crops_coords_top_left + target_size)
            add_neg_time_ids = None

        passed_add_embed_dim = (
            self.unet.config.addition_time_embed_dim * len(add_time_ids) + self.text_encoder_2.config.projection_dim # type: ignore[attr-defined]
        )
        expected_add_embed_dim = self.unet.add_embedding.linear_1.in_features # type: ignore[union-attr]

        if (
            expected_add_embed_dim > passed_add_embed_dim
            and (expected_add_embed_dim - passed_add_embed_dim) == self.unet.config.addition_time_embed_dim # type: ignore[attr-defined]
        ):
            raise ValueError(
                f"Model expects an added time embedding vector of length {expected_add_embed_dim}, but a vector of {passed_add_embed_dim} was created. Please make sure to enable `requires_aesthetic_score` with `pipe.register_to_config(requires_aesthetic_score=True)` to make sure `aesthetic_score` {aesthetic_score} and `negative_aesthetic_score` {negative_aesthetic_score} is correctly used by the model."
            )
        elif (
            expected_add_embed_dim < passed_add_embed_dim
            and (passed_add_embed_dim - expected_add_embed_dim) == self.unet.config.addition_time_embed_dim # type: ignore[attr-defined]
        ):
            raise ValueError(
                f"Model expects an added time embedding vector of length {expected_add_embed_dim}, but a vector of {passed_add_embed_dim} was created. Please make sure to disable `requires_aesthetic_score` with `pipe.register_to_config(requires_aesthetic_score=False)` to make sure `target_size` {target_size} is correctly used by the model."
            )
        elif expected_add_embed_dim != passed_add_embed_dim:
            raise ValueError(
                f"Model expects an added time embedding vector of length {expected_add_embed_dim}, but a vector of {passed_add_embed_dim} was created. The model has an incorrect config. Please check `unet.config.time_embedding_type` and `text_encoder_2.config.projection_dim`."
            )

        add_time_ids = torch.tensor([add_time_ids], dtype=dtype)  # type: ignore
        if add_neg_time_ids is not None:
            add_neg_time_ids = torch.tensor([add_neg_time_ids], dtype=dtype)  # type: ignore

        return add_time_ids, add_neg_time_ids  # type: ignore

    def predict_noise_residual(
        self,
        latents: torch.Tensor,
        timestep: torch.Tensor,
        embeddings: torch.Tensor,
        timestep_cond: Optional[torch.Tensor] = None,
        cross_attention_kwargs: Optional[Dict[str, Any]] = None,
        added_cond_kwargs: Optional[Dict[str, Any]] = None,
        down_block_additional_residuals: Optional[List[torch.Tensor]] = None,
        mid_block_additional_residual: Optional[torch.Tensor] = None,
        motion_attention_mask: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Runs the UNet to predict noise residual.
        """
        kwargs: Dict[str, Any] = {}
        if added_cond_kwargs is not None:
            kwargs["added_cond_kwargs"] = added_cond_kwargs
        if motion_attention_mask is not None:
            kwargs["motion_attention_mask"] = motion_attention_mask
        return self.unet(
            latents,
            timestep,
            encoder_hidden_states=embeddings,
            timestep_cond=timestep_cond,
            cross_attention_kwargs=cross_attention_kwargs,
            down_block_additional_residuals=down_block_additional_residuals,
            mid_block_additional_residual=mid_block_additional_residual,
            return_dict=False,
            **kwargs,
        )[0]

    def prepare_control_image(
        self,
        image: Union[torch.Tensor, PIL.Image.Image, List[PIL.Image.Image]],
        width: int,
        height: int,
        batch_size: int,
        num_results_per_prompt: int,
        device: Union[str, torch.device],
        dtype: torch.dtype,
        do_classifier_free_guidance=False,
        animation_frames: Optional[int] = None,
        conditioning_frame: Optional[Union[int, List[int]]] = None,
    ) -> Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
        """
        Prepares an image for controlnet conditioning.
        """
        mask: Optional[torch.Tensor] = None
        if not isinstance(image, torch.Tensor):
            if isinstance(image, PIL.Image.Image):
                image = [image]

            if isinstance(image[0], PIL.Image.Image):
                images = []

                for i in image:
                    i = i.convert("RGB")
                    i = i.resize((width, height), resample=PIL_INTERPOLATION["lanczos"])
                    i = np.array(i)
                    i = i[None, :]
                    images.append(i)

                image = images

                image = np.concatenate(image, axis=0)
                image = np.array(image).astype(np.float32) / 255.0 # type: ignore[attr-defined]
                image = image.transpose(0, 3, 1, 2)
                image = torch.from_numpy(image)
            elif isinstance(image[0], torch.Tensor):
                image = torch.cat(image, dim=0)

        if animation_frames:
            # Move what is normally batch (0) to time (2), then insert batch dim back in
            image = rearrange(image, 't c h w -> c t h w').unsqueeze(0) # now b c t h w
            if conditioning_frame is not None:
                # Get condition length
                image_length = image.shape[2]

                # Start from zeros
                condition_shape = list(image.shape)
                condition_shape[2] = animation_frames
                condition = torch.zeros(condition_shape).to(device=device, dtype=dtype)
                mask_shape = list(condition.shape)
                mask_shape[1] = 1
                mask = torch.zeros(mask_shape).to(device=device, dtype=dtype)

                # Set condition(s)
                if not isinstance(conditioning_frame, list):
                    conditioning_frame = [conditioning_frame]

                for cond_frame in conditioning_frame:
                    # Set image and mask for cond frames
                    condition[:,:,cond_frame:cond_frame+image_length] = image
                    mask[:,:,cond_frame:cond_frame+image_length] = 1
                # image now becomes the combined condition
                image = condition

        image_batch_size = image.shape[0]

        if image_batch_size == 1:
            repeat_by = batch_size
        else:
            # image batch size is the same as prompt batch size
            repeat_by = num_results_per_prompt

        image = image.repeat_interleave(repeat_by, dim=0)
        if do_classifier_free_guidance and conditioning_frame is None:
            image = torch.cat([image] * 2)

        image = image.to(device=device, dtype=dtype)
        if mask is None:
            return image
        return (image, mask)

    def prepare_controlnet_inpaint_control_image(
        self,
        image: PIL.Image.Image,
        mask: PIL.Image.Image,
        device: Union[str, torch.device],
        dtype: torch.dtype,
    ) -> torch.Tensor:
        """
        Combines the image and mask into a condition for controlnet inpainting.
        """
        image = np.array(image.convert("RGB")).astype(np.float32) / 255.0 # type: ignore[attr-defined]
        mask = np.array(mask.convert("L")).astype(np.float32) / 255.0 # type: ignore[attr-defined]

        assert image.shape[0:1] == mask.shape[0:1], "image and image_mask must have the same image size"
        image[mask > 0.5] = -1.0  # set as masked pixel

        image = np.expand_dims(image, 0).transpose(0, 3, 1, 2) # type: ignore[attr-defined]
        image = torch.from_numpy(image)

        return image.to(device=device, dtype=dtype)

    def get_controlnet_conditioning_blocks(
        self,
        device: Union[str, torch.device],
        latents: torch.Tensor,
        timestep: torch.Tensor,
        encoder_hidden_states: torch.Tensor,
        controlnet_conds: Optional[Dict[str, List[Tuple[torch.Tensor, Union[float, torch.Tensor], Optional[torch.Tensor]]]]],
        added_cond_kwargs: Optional[Dict[str, Any]],
    ) -> Tuple[Optional[List[torch.Tensor]], Optional[torch.Tensor]]:
        """
        Executes the controlnet
        """
        if not controlnet_conds or not self.controlnets:
            return None, None

        is_animation = len(latents.shape) == 5
        if is_animation:
            batch, channels, frames, height, width = latents.shape
            # Compress frames to batch. First the latent input...
            latent_input = rearrange(latents, "b c f h w -> (b f) c h w")
            # Then hidden states...
            hidden_state_input = rearrange(encoder_hidden_states, "b f t d -> (b f) t d")
#            hidden_state_input = encoder_hidden_states.repeat_interleave(frames, dim=0)
            # Then additional conditioning arguments, if passed (XL)
            if added_cond_kwargs:
                added_cond_input = {}
                if "text_embeds" in added_cond_kwargs:
                    added_cond_input["text_embeds"] = rearrange(added_cond_kwargs["text_embeds"][:, :, 0, :], "b f d -> (b f) d")
                if "time_ids" in added_cond_kwargs:
                    added_cond_input["time_ids"] = added_cond_kwargs["time_ids"].repeat_interleave(frames, dim=0)
            else:
                added_cond_input = {}
        else:
            batch, channels, height, width = latents.shape
            frames = None
            latent_input = latents
            hidden_state_input = encoder_hidden_states
            added_cond_input = added_cond_kwargs if added_cond_kwargs is not None else {}

        down_blocks, mid_block = None, None
        for name in controlnet_conds:
            if self.controlnets.get(name, None) is None:
                raise RuntimeError(f"Conditioning image requested ControlNet {name}, but it's not loaded.")
            for i, (controlnet_cond, conditioning_scale, conditioning_mask) in enumerate(controlnet_conds[name]):
                if conditioning_mask is not None:
                    if is_animation:
                        sparse_latent_input = latents
                        hidden_state_input = torch.sum(encoder_hidden_states, dim=1) / encoder_hidden_states.shape[1]
                    else:
                        sparse_latent_input = rearrange(latents.unsqueeze(0), "f b c h w -> b c f h w")
                    # Sparse
                    down_samples, mid_sample = self.controlnets[name](
                        sparse_latent_input,
                        timestep,
                        encoder_hidden_states=hidden_state_input,
                        controlnet_cond=controlnet_cond,
                        conditioning_mask=conditioning_mask,
                        conditioning_scale=1.0 if isinstance(conditioning_scale, torch.Tensor) else conditioning_scale,
                        added_cond_kwargs=added_cond_input,
                        return_dict=False,
                        guess_mode=False
                    )
                    if isinstance(conditioning_scale, torch.Tensor):
                        for i, sample in enumerate(down_samples):
                            _, C, _, H, W = sample.shape
                            down_samples[i] *= repeat(conditioning_scale, "f -> b c f h w", b=batch, c=C, h=H, w=W)
                        _, C, _, H, W = mid_sample.shape
                        mid_sample *= repeat(conditioning_scale, "f -> b c f h w", b=batch, c=C, h=H, w=W)

                    if not is_animation:
                        for i, sample in enumerate(down_samples):
                            down_samples[i] = rearrange(sample, "b c f h w -> (b f) c h w")
                        mid_sample = rearrange(mid_sample, "b c f h w -> (b f) c h w")

                else:
                    if is_animation:
                        controlnet_cond = rearrange(controlnet_cond, "b c f h w -> (b f) c h w")

                    down_samples, mid_sample = self.controlnets[name](
                        latent_input,
                        timestep,
                        encoder_hidden_states=hidden_state_input,
                        controlnet_cond=controlnet_cond,
                        conditioning_scale=1.0 if isinstance(conditioning_scale, torch.Tensor) else conditioning_scale,
                        added_cond_kwargs=added_cond_input,
                        return_dict=False,
                    )

                    if is_animation:
                        for i, sample in enumerate(down_samples):
                            down_samples[i] = rearrange(sample, "(b f) c h w -> b c f h w", b=batch, f=frames)
                            if isinstance(conditioning_scale, torch.Tensor):
                                _, C, H, W = sample.shape
                                down_samples[i] *= repeat(conditioning_scale, "f -> b c f h w", b=batch, c=C, h=H, w=W)
                        mid_sample = rearrange(mid_sample, f"(b f) c h w -> b c f h w", b=batch, f=frames)
                        if isinstance(conditioning_scale, torch.Tensor):
                            _, C, _, H, W = mid_sample.shape
                            mid_sample *= repeat(conditioning_scale, "f -> b c f h w", b=batch, c=C, h=H, w=W)

                if down_blocks is None or mid_block is None: # type: ignore[unreachable]
                    down_blocks, mid_block = down_samples, mid_sample
                else:
                    down_blocks = [ # type: ignore[unreachable]
                        previous_block + current_block
                        for previous_block, current_block in zip(down_blocks, down_samples)
                    ]
                    mid_block += mid_sample

        return down_blocks, mid_block

    def denoise_unchunked(
        self,
        height: int,
        width: int,
        device: Union[str, torch.device],
        num_inference_steps: int,
        timesteps: torch.Tensor,
        latents: torch.Tensor,
        encoded_prompts: EncodedPrompts,
        weight_builder: MaskWeightBuilder,
        guidance_scale: float,
        do_classifier_free_guidance: bool = False,
        timestep_cond: Optional[torch.Tensor] = None,
        mask: Optional[torch.Tensor] = None,
        mask_image: Optional[torch.Tensor] = None,
        image: Optional[torch.Tensor] = None,
        control_images: PreparedControlImageArgType = None,
        progress_callback: Optional[Callable[[bool], None]] = None,
        latent_callback: Optional[Callable[[Union[torch.Tensor, np.ndarray, List[PIL.Image.Image]]], None]] = None,
        latent_callback_steps: Optional[int] = None,
        latent_callback_type: Literal["latent", "pt", "np", "pil"] = "latent",
        extra_step_kwargs: Optional[Dict[str, Any]] = None,
        cross_attention_kwargs: Optional[Dict[str, Any]] = None,
        added_cond_kwargs: Optional[Dict[str, Any]] = None,
        frequencies: Optional[torch.Tensor] = None,
        amplitudes: Optional[torch.Tensor] = None,
        motion_attention_frequency: Optional[Union[int, Tuple[int, int]]] = (0, 22050),
        motion_attention_channel: Optional[Union[int, Tuple[int, ...]]] = None,
        motion_attention_min: float=0.85,
        motion_attention_max: float=1.30,
    ) -> torch.Tensor:
        """
        Executes the denoising loop without chunking.
        """
        if extra_step_kwargs is None:
            extra_step_kwargs = {}

        num_steps = len(timesteps)
        num_warmup_steps = num_steps - num_inference_steps * self.scheduler.order # type: ignore[attr-defined]

        if len(latents.shape) == 5:
            samples, num_channels, num_frames, latent_height, latent_width = latents.shape
        else:
            samples, num_channels, latent_height, latent_width = latents.shape
            num_frames = None

        embedding_frames = None if num_frames is None else list(range(num_frames))

        noise = None
        if mask is not None and mask_image is not None and not self.is_inpainting_unet:
            noise = latents.detach().clone() / self.scheduler.init_noise_sigma # type: ignore[attr-defined]
            noise = noise.to(device=device)

        logger.debug(f"Denoising image in {num_steps} steps on {device} (unchunked)")

        # Calculate motion attention
        if motion_attention_frequency is not None and frequencies is not None and amplitudes is not None and num_frames is not None:
            motion_attention_audio_mask = weight_builder.audio(
                frames=list(range(num_frames)),
                frequencies=frequencies,
                amplitudes=amplitudes,
                frequency=motion_attention_frequency,
                channel=motion_attention_channel
            )
            motion_attention_mask = torch.ones_like(motion_attention_audio_mask) * motion_attention_min
            motion_attention_mask += motion_attention_audio_mask * (motion_attention_max - motion_attention_min)
        else:
            motion_attention_mask = None

        steps_since_last_callback = 0
        for i, t in enumerate(timesteps):
            # store ratio for later
            denoising_ratio = i / num_steps

            # expand the latents if we are doing classifier free guidance
            latent_model_input = torch.cat([latents] * 2) if do_classifier_free_guidance else latents
            latent_model_input = self.scheduler.scale_model_input(latent_model_input, t) # type: ignore[attr-defined]

            # Get embeds
            embeds = encoded_prompts.get_embeds(
                frames=embedding_frames,
                frequencies=frequencies,
                amplitudes=amplitudes
            )
            if embeds is None:
                logger.warning("No text embeds, using zeros")
                if self.text_encoder:
                    embeds = torch.zeros(samples, 77, self.text_encoder.config.hidden_size).to(device)
                elif self.text_encoder_2:
                    embeds = torch.zeros(samples, 77, self.text_encoder_2.config.hidden_size).to(device)
                else:
                    raise IOError("No embeds and no text encoder.")

            embeds = embeds.to(device=device)

            # Get added embeds
            add_text_embeds = encoded_prompts.get_add_text_embeds(
                frames=embedding_frames,
                frequencies=frequencies,
                amplitudes=amplitudes
            )
            if add_text_embeds is not None:
                if not added_cond_kwargs:
                    raise ValueError(f"Added condition arguments is empty, but received add text embeds. There should be time IDs prior to this point.")
                added_cond_kwargs["text_embeds"] = add_text_embeds.to(device=device, dtype=embeds.dtype)

            # Get controlnet input(s) if configured
            if control_images is not None:
                # Find which control image(s) to use
                controlnet_conds: Dict[str, List[Tuple[torch.Tensor, Union[float, torch.Tensor], Optional[torch.Tensor]]]] = {}
                for controlnet_name in control_images:
                    for (
                        control_image,
                        conditioning_scale,
                        conditioning_start,
                        conditioning_end,
                        conditioning_mask,
                    ) in control_images[controlnet_name]:
                        if (
                            (conditioning_start is None or conditioning_start <= denoising_ratio) and
                            (conditioning_end is None or denoising_ratio <= conditioning_end)
                        ):
                            if controlnet_name not in controlnet_conds:
                                controlnet_conds[controlnet_name] = []

                            controlnet_conds[controlnet_name].append((control_image, conditioning_scale, conditioning_mask))

                if not controlnet_conds:
                    down_block, mid_block = None, None
                else:
                    down_block, mid_block = self.get_controlnet_conditioning_blocks(
                        device=device,
                        latents=latent_model_input,
                        timestep=t,
                        encoder_hidden_states=embeds,
                        controlnet_conds=controlnet_conds,
                        added_cond_kwargs=added_cond_kwargs,
                    )
            else:
                down_block, mid_block = None, None

            # add other dimensions to unet input if set
            if mask is not None and mask_image is not None and self.is_inpainting_unet:
                latent_model_input = torch.cat(
                    [latent_model_input, mask, mask_image],
                    dim=1,
                )

            # predict the noise residual
            noise_pred = self.predict_noise_residual(
                latents=latent_model_input,
                timestep=t,
                embeddings=embeds,
                timestep_cond=timestep_cond,
                cross_attention_kwargs=cross_attention_kwargs,
                added_cond_kwargs=added_cond_kwargs,
                down_block_additional_residuals=down_block,
                mid_block_additional_residual=mid_block,
                motion_attention_mask=motion_attention_mask,
            )

            # perform guidance
            if do_classifier_free_guidance:
                noise_pred_uncond, noise_pred_text = noise_pred.chunk(2)
                noise_pred = noise_pred_uncond + guidance_scale * (noise_pred_text - noise_pred_uncond)

            # Compute previous noisy sample
            latents = self.scheduler.step( # type: ignore[attr-defined]
                noise_pred,
                t,
                latents,
                **extra_step_kwargs,
            ).prev_sample.to(dtype=embeds.dtype)

            # If using mask and not using fine-tuned inpainting, then we calculate
            # the same denoising on the image without unet and cross with the
            # calculated unet input * mask
            if mask is not None and image is not None and not self.is_inpainting_unet:
                init_latents = image[:1]
                init_mask = mask[:1]

                if i < len(timesteps) - 1:
                    noise_timestep = timesteps[i + 1]
                    init_latents = self.scheduler.add_noise( # type: ignore[attr-defined]
                        init_latents,
                        noise,
                        torch.tensor([noise_timestep])
                    )

                latents = (1 - init_mask) * init_latents + init_mask * latents

            if progress_callback is not None:
                progress_callback(True)

            # call the callback, if provided
            steps_since_last_callback += 1
            if (
                latent_callback is not None
                and latent_callback_steps is not None
                and steps_since_last_callback >= latent_callback_steps
                and (i == num_steps - 1 or ((i + 1) > num_warmup_steps and (i + 1) % self.scheduler.order == 0)) # type: ignore[attr-defined]
            ):
                if i > num_steps * 0.75 and not self.safety_checking_disabled and self.safety_checker is not None:
                    # Don't call the callback in the final 25% of the image if safety checking is enabled
                    continue

                steps_since_last_callback = 0
                latent_callback_value = latents

                if latent_callback_type != "latent":
                    latent_callback_value = self.decode_latent_preview(
                        latent_callback_value,
                        weight_builder=weight_builder,
                        device=device,
                    )
                    latent_callback_value = self.denormalize_latents(latent_callback_value)
                    if num_frames is not None:
                        output = [] # type: ignore[assignment]
                        for frame in self.decode_animation_frames(latent_callback_value):
                            output.extend(self.image_processor.numpy_to_pil(frame)) # type: ignore[attr-defined]
                        latent_callback_value = output # type: ignore[assignment]
                    else:
                        if latent_callback_type != "pt":
                            latent_callback_value = self.image_processor.pt_to_numpy(latent_callback_value)
                            if latent_callback_type == "pil":
                                latent_callback_value = self.image_processor.numpy_to_pil(latent_callback_value)

                latent_callback(latent_callback_value)

        return latents

    def get_scheduler_state(self) -> Dict[str, Any]:
        """
        Gets the state dictionary from the current scheduler.
        Copies it in a safe way.
        """
        data: Dict[str, Any] = {}
        scheduler_data = self.scheduler.__dict__
        for key in scheduler_data:
            try:
                data[key] = copy.deepcopy(scheduler_data[key])
            except:
                pass
        return data

    def denoise(
        self,
        height: int,
        width: int,
        device: Union[str, torch.device],
        num_inference_steps: int,
        chunker: Chunker,
        timesteps: torch.Tensor,
        latents: torch.Tensor,
        encoded_prompts: EncodedPrompts,
        weight_builder: MaskWeightBuilder,
        guidance_scale: float,
        do_classifier_free_guidance: bool = False,
        timestep_cond: Optional[torch.Tensor] = None,
        mask: Optional[torch.Tensor] = None,
        mask_image: Optional[torch.Tensor] = None,
        image: Optional[torch.Tensor] = None,
        control_images: PreparedControlImageArgType = None,
        progress_callback: Optional[Callable[[bool], None]] = None,
        latent_callback: Optional[Callable[[Union[torch.Tensor, np.ndarray, List[PIL.Image.Image]]], None]] = None,
        latent_callback_steps: Optional[int] = None,
        latent_callback_type: Literal["latent", "pt", "np", "pil"] = "latent",
        extra_step_kwargs: Optional[Dict[str, Any]] = None,
        cross_attention_kwargs: Optional[Dict[str, Any]] = None,
        added_cond_kwargs: Optional[Dict[str, Any]] = None,
        tiling: bool = False,
        frequencies: Optional[torch.Tensor] = None,
        amplitudes: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Executes the denoising loop.
        """
        if extra_step_kwargs is None:
            extra_step_kwargs = {}

        if len(latents.shape) == 5:
            samples, num_channels, num_frames, latent_height, latent_width = latents.shape
        else:
            samples, num_channels, latent_height, latent_width = latents.shape
            num_frames = None
        
        num_chunks = chunker.num_chunks
        num_temporal_chunks = chunker.num_frame_chunks

        if num_temporal_chunks <= 1 and (num_chunks <= 1 or not tiling):
            return self.denoise_unchunked(
                height=height,
                width=width,
                device=device,
                num_inference_steps=num_inference_steps,
                timesteps=timesteps,
                latents=latents,
                encoded_prompts=encoded_prompts,
                weight_builder=weight_builder,
                guidance_scale=guidance_scale,
                do_classifier_free_guidance=do_classifier_free_guidance,
                timestep_cond=timestep_cond,
                mask=mask,
                mask_image=mask_image,
                image=image,
                control_images=control_images,
                progress_callback=progress_callback,
                latent_callback=latent_callback,
                latent_callback_steps=latent_callback_steps,
                latent_callback_type=latent_callback_type,
                extra_step_kwargs=extra_step_kwargs,
                cross_attention_kwargs=cross_attention_kwargs,
                added_cond_kwargs=added_cond_kwargs,
                frequencies=frequencies,
                amplitudes=amplitudes,
            )

        revert_chunker_size: Any = None
        if num_chunks > 1 and not tiling:
            # Disable spatial tiling
            revert_chunker_size = chunker.size
            chunker.size = None
            num_chunks = 1

        chunk_scheduler_status = []
        for i in range(num_chunks * num_temporal_chunks):
            chunk_scheduler_status.append(self.get_scheduler_state())

        num_steps = len(timesteps)
        num_warmup_steps = num_steps - num_inference_steps * self.scheduler.order # type: ignore[attr-defined]

        latent_width = width // self.vae_scale_factor
        latent_height = height // self.vae_scale_factor
        engine_latent_size = self.engine_size // self.vae_scale_factor

        count = torch.zeros_like(latents)
        value = torch.zeros_like(latents)

        total_num_steps = num_steps * num_chunks * num_temporal_chunks
        logger.debug(
            f"Denoising image in {total_num_steps} steps on {device} ({num_inference_steps} inference steps * {num_chunks} chunks * {num_temporal_chunks} temporal chunks)"
        )

        noise = None
        if mask is not None and mask_image is not None and not self.is_inpainting_unet:
            noise = latents.detach().clone() / self.scheduler.init_noise_sigma # type: ignore[attr-defined]
            noise = noise.to(device=device)

        steps_since_last_callback = 0
        for i, t in enumerate(timesteps):
            # Calculate ratio for later
            denoising_ratio = i / num_steps

            # zero view latents
            count.zero_()
            value.zero_()

            # Check if we should store generator state
            generator_state: Optional[torch.Tensor] = None
            if "generator" in extra_step_kwargs:
                generator_state = extra_step_kwargs["generator"].get_state()

            # iterate over chunks
            for j, ((top, bottom), (left, right), (start, end)) in enumerate(chunker):
                # Memoize wrap for later
                wrap_x = right <= left
                wrap_y = bottom <= top
                wrap_t = start is not None and end is not None and end <= start

                mask_width = (latent_width - left) + right if wrap_x else right - left
                mask_height = (latent_height - top) + bottom if wrap_y else bottom - top
                if num_frames is None or start is None or end is None:
                    mask_frames = None
                else:
                    mask_frames = (num_frames - start) + end if wrap_t else end - start

                # Define some helpers for chunked denoising
                def slice_for_view(tensor: torch.Tensor, scale_factor: int = 1) -> torch.Tensor:
                    """
                    Copies and slices input tensors
                    """
                    left_idx = left * scale_factor
                    right_idx = right * scale_factor
                    top_idx = top * scale_factor
                    bottom_idx = bottom * scale_factor
                    height_idx = latent_height * scale_factor
                    width_idx = latent_width * scale_factor

                    if wrap_x:
                        horizontal = (left_idx, width_idx, right_idx)
                    else:
                        horizontal = (left_idx, right_idx) # type: ignore[assignment]

                    if wrap_y:
                        vertical = (top_idx, height_idx, bottom_idx)
                    else:
                        vertical = (top_idx, bottom_idx) # type: ignore[assignment]

                    if wrap_t:
                        temporal = (start, num_frames, end)
                    else:
                        temporal = (start, end) # type: ignore[assignment]

                    if num_frames is not None:
                        if len(horizontal) == 3:
                            if len(vertical) == 3:
                                if len(temporal) == 3:
                                    return torch.cat([
                                        torch.cat([
                                            torch.cat([
                                                tensor[:, :, temporal[0]:temporal[1], vertical[0]:vertical[1], horizontal[0]:horizontal[1]],
                                                tensor[:, :,            :temporal[2], vertical[0]:vertical[1], horizontal[0]:horizontal[1]],
                                            ], dim=2),
                                            torch.cat([
                                                tensor[:, :, temporal[0]:temporal[1],            :vertical[2], horizontal[0]:horizontal[1]],
                                                tensor[:, :,            :temporal[2],            :vertical[2], horizontal[0]:horizontal[1]],
                                            ], dim=2),
                                        ], dim=3),
                                        torch.cat([
                                            torch.cat([
                                                tensor[:, :, temporal[0]:temporal[1], vertical[0]:vertical[1],              :horizontal[2]],
                                                tensor[:, :,            :temporal[2], vertical[0]:vertical[1],              :horizontal[2]],
                                            ], dim=2),
                                            torch.cat([
                                                tensor[:, :, temporal[0]:temporal[1],            :vertical[2],              :horizontal[2]],
                                                tensor[:, :,            :temporal[2],            :vertical[2],              :horizontal[2]],
                                            ], dim=2),
                                        ], dim=3)
                                    ], dim=4)
                                else:
                                    return torch.cat([
                                        torch.cat([
                                            tensor[:, :, temporal[0]:temporal[1], vertical[0]:vertical[1], horizontal[0]:horizontal[1]],
                                            tensor[:, :, temporal[0]:temporal[1],            :vertical[2], horizontal[0]:horizontal[1]],
                                        ], dim=3),
                                        torch.cat([
                                            tensor[:, :, temporal[0]:temporal[1], vertical[0]:vertical[1],              :horizontal[2]],
                                            tensor[:, :, temporal[0]:temporal[1],            :vertical[2],              :horizontal[2]],
                                        ], dim=3)
                                    ], dim=4)
                            else:
                                if len(temporal) == 3:
                                    return torch.cat([
                                        torch.cat([
                                            tensor[:, :, temporal[0]:temporal[1], vertical[0]:vertical[1], horizontal[0]:horizontal[1]],
                                            tensor[:, :,            :temporal[2], vertical[0]:vertical[1], horizontal[0]:horizontal[1]],
                                        ], dim=2),
                                        torch.cat([
                                            tensor[:, :, temporal[0]:temporal[1], vertical[0]:vertical[1],              :horizontal[2]],
                                            tensor[:, :,            :temporal[2], vertical[0]:vertical[1],              :horizontal[2]],
                                        ], dim=2),
                                    ], dim=4)
                                else:
                                    return torch.cat([
                                        tensor[:, :, temporal[0]:temporal[1], vertical[0]:vertical[1], horizontal[0]:horizontal[1]],
                                        tensor[:, :, temporal[0]:temporal[1], vertical[0]:vertical[1],              :horizontal[2]],
                                    ], dim=4)
                        else:
                            if len(vertical) == 3:
                                if len(temporal) == 3:
                                    return torch.cat([
                                        torch.cat([
                                            tensor[:, :, temporal[0]:temporal[1], vertical[0]:vertical[1], horizontal[0]:horizontal[1]],
                                            tensor[:, :,            :temporal[2], vertical[0]:vertical[1], horizontal[0]:horizontal[1]],
                                        ], dim=2),
                                        torch.cat([
                                            tensor[:, :, temporal[0]:temporal[1],            :vertical[2], horizontal[0]:horizontal[1]],
                                            tensor[:, :,            :temporal[2],            :vertical[2], horizontal[0]:horizontal[1]],
                                        ], dim=2),
                                    ], dim=3)
                                else:
                                    return torch.cat([
                                        tensor[:, :, temporal[0]:temporal[1], vertical[0]:vertical[1], horizontal[0]:horizontal[1]],
                                        tensor[:, :, temporal[0]:temporal[1],            :vertical[2], horizontal[0]:horizontal[1]],
                                    ], dim=3)
                            else:
                                if len(temporal) == 3:
                                    return torch.cat([
                                        tensor[:, :, temporal[0]:temporal[1], vertical[0]:vertical[1], horizontal[0]:horizontal[1]],
                                        tensor[:, :,            :temporal[2], vertical[0]:vertical[1], horizontal[0]:horizontal[1]],
                                    ], dim=2)
                                else:
                                    return tensor[:, :, temporal[0]:temporal[1], vertical[0]:vertical[1], horizontal[0]:horizontal[1]]
                    else:
                        if len(horizontal) == 3:
                            if len(vertical) == 3:
                                return torch.cat([
                                    torch.cat([
                                        tensor[:, :, vertical[0]:vertical[1], horizontal[0]:horizontal[1]],
                                        tensor[:, :,            :vertical[2], horizontal[0]:horizontal[1]],
                                    ], dim=2),
                                    torch.cat([
                                        tensor[:, :, vertical[0]:vertical[1],              :horizontal[2]],
                                        tensor[:, :,            :vertical[2],              :horizontal[2]],
                                    ], dim=2),
                                ], dim=3)
                            else:
                                return torch.cat([
                                    tensor[:, :, vertical[0]:vertical[1], horizontal[0]:horizontal[1]],
                                    tensor[:, :, vertical[0]:vertical[1],              :horizontal[2]],
                                ], dim=3)
                        else:
                            if len(vertical) == 3:
                                return torch.cat([
                                    tensor[:, :, vertical[0]:vertical[1], horizontal[0]:horizontal[1]],
                                    tensor[:, :,            :vertical[2], horizontal[0]:horizontal[1]],
                                ], dim=2)
                            else:
                                return tensor[:, :, vertical[0]:vertical[1], horizontal[0]:horizontal[1]]

                    raise RuntimeError("This should not be possible, a case has been missed in programming. Please raise this issue to the developer.")

                def fill_value(tensor: torch.Tensor, multiplier: torch.Tensor) -> None:
                    """
                    Fills the value and count tensors
                    """
                    nonlocal value, count
                    start_x = left
                    end_x = latent_width if wrap_x else right
                    initial_x = end_x - start_x
                    start_y = top
                    end_y = latent_height if wrap_y else bottom
                    initial_y = end_y - start_y
                    start_t = start
                    end_t = num_frames if wrap_t else end
                    initial_t = None if end_t is None or start_t is None else end_t - start_t

                    if num_frames is None:
                        value[:, :, start_y:end_y, start_x:end_x] += tensor[:, :, :initial_y, :initial_x]
                        count[:, :, start_y:end_y, start_x:end_x] += multiplier[:, :, :initial_y, :initial_x]
                        if wrap_x:
                            value[:, :, start_y:end_y, :right] += tensor[:, :, :initial_y, initial_x:]
                            count[:, :, start_y:end_y, :right] += multiplier[:, :, :initial_y, initial_x:]
                            if wrap_y:
                                value[:, :, :bottom, :right] += tensor[:, :, initial_y:, initial_x:]
                                count[:, :, :bottom, :right] += multiplier[:, :, initial_y:, initial_x:]
                        if wrap_y:
                            value[:, :, :bottom, start_x:end_x] += tensor[:, :, initial_y:, :initial_x]
                            count[:, :, :bottom, start_x:end_x] += multiplier[:, :, initial_y:, :initial_x]
                    else:
                        value[:, :, start_t:end_t, start_y:end_y, start_x:end_x] += tensor[:, :, :initial_t, :initial_y, :initial_x]
                        count[:, :, start_t:end_t, start_y:end_y, start_x:end_x] += multiplier[:, :, :initial_t, :initial_y, :initial_x]
                        if wrap_x:
                            value[:, :, start_t:end_t, start_y:end_y, :right] += tensor[:, :, :initial_t, :initial_y, initial_x:]
                            count[:, :, start_t:end_t, start_y:end_y, :right] += multiplier[:, :, :initial_t, :initial_y, initial_x:]
                            if wrap_y:
                                value[:, :, start_t:end_t, :bottom, :right] += tensor[:, :, :initial_t, initial_y:, initial_x:]
                                count[:, :, start_t:end_t, :bottom, :right] += multiplier[:, :, :initial_t, initial_y:, initial_x:]
                                if wrap_t:
                                    value[:, :, :end, :bottom, :right] += tensor[:, :, initial_t:, initial_y:, initial_x:]
                                    count[:, :, :end, :bottom, :right] += multiplier[:, :, initial_t:, initial_y:, initial_x:]
                        if wrap_y:
                            value[:, :, start_t:end_t, :bottom, start_x:end_x] += tensor[:, :, :initial_t, initial_y:, :initial_x]
                            count[:, :, start_t:end_t, :bottom, start_x:end_x] += multiplier[:, :, :initial_t, initial_y:, :initial_x]
                            if wrap_t:
                                value[:, :, :end, :bottom, start_x:end_x] += tensor[:, :, initial_t:, initial_y:, :initial_x]
                                count[:, :, :end, :bottom, start_x:end_x] += multiplier[:, :, initial_t:, initial_y:, :initial_x]
                        if wrap_t:
                            value[:, :, :end, start_y:end_y, start_x:end_x] += tensor[:, :, initial_t:, :initial_y, :initial_x]
                            count[:, :, :end, start_y:end_y, start_x:end_x] += multiplier[:, :, initial_t:, :initial_y, :initial_x]

                # Wrap IndexError to give a nice error about MultiDiff w/ some schedulers
                try:
                    # Slice latents
                    latents_for_view = slice_for_view(latents)

                    # expand the latents if we are doing classifier free guidance
                    latent_model_input = (
                        torch.cat([latents_for_view] * 2) if do_classifier_free_guidance else latents_for_view
                    )

                    # Re-match chunk scheduler status
                    self.scheduler.__dict__.update(chunk_scheduler_status[j])

                    # Re-match generator state
                    if "generator" in extra_step_kwargs and generator_state is not None:
                        extra_step_kwargs["generator"].set_state(generator_state)

                    # Scale model input
                    latent_model_input = self.scheduler.scale_model_input(latent_model_input, t) # type: ignore[attr-defined]

                    # Get embeds
                    if wrap_t and start is not None and num_frames is not None and end is not None:
                        frame_indexes = list(range(start,num_frames)) + list(range(end))
                    elif num_frames is not None and start is not None and end is not None:
                        frame_indexes = list(range(start,end))
                    else:
                        frame_indexes = None

                    embeds = encoded_prompts.get_embeds(
                        frames=frame_indexes,
                        frequencies=frequencies,
                        amplitudes=amplitudes
                     )

                    if embeds is None:
                        logger.warning(f"Warning: no prompts found for frame window {frame_indexes}")
                        if self.text_encoder:
                            embeds = torch.zeros(samples, 77, self.text_encoder.config.hidden_size).to(device)
                        elif self.text_encoder_2:
                            embeds = torch.zeros(samples, 77, self.text_encoder_2.config.hidden_size).to(device)
                        else:
                            raise IOError("No embeds and no text encoder.")

                    # Get added embeds
                    add_text_embeds = encoded_prompts.get_add_text_embeds(
                        frames=frame_indexes,
                        frequencies=frequencies,
                        amplitudes=amplitudes
                    )
                    if add_text_embeds is not None:
                        if not added_cond_kwargs:
                            raise ValueError(f"Added condition arguments is empty, but received add text embeds. There should be time IDs prior to this point.")
                        added_cond_kwargs["text_embeds"] = add_text_embeds.to(device=device, dtype=embeds.dtype)

                    # Get controlnet input(s) if configured
                    if control_images is not None:
                        # Find which control image(s) to use
                        controlnet_conds: Dict[str, List[Tuple[torch.Tensor, Union[float, torch.Tensor], Optional[torch.Tensor]]]] = {}
                        for controlnet_name in control_images:
                            for (
                                control_image,
                                conditioning_scale,
                                conditioning_start,
                                conditioning_end,
                                conditioning_mask
                            ) in control_images[controlnet_name]:
                                if (
                                    (conditioning_start is None or conditioning_start <= denoising_ratio) and
                                    (conditioning_end is None or denoising_ratio <= conditioning_end)
                                ):
                                    if controlnet_name not in controlnet_conds:
                                        controlnet_conds[controlnet_name] = []

                                    if isinstance(conditioning_scale, torch.Tensor):
                                        if start > end: # type: ignore[operator]
                                            # Wraparound
                                            this_scale = torch.cat([
                                                conditioning_scale[start:num_frames],
                                                conditioning_scale[:end]
                                            ])
                                        else:
                                            this_scale = conditioning_scale[start:end]
                                    else:
                                        this_scale = conditioning_scale # type: ignore[assignment]

                                    controlnet_conds[controlnet_name].append((
                                        slice_for_view(control_image, self.vae_scale_factor),
                                        this_scale,
                                        None if conditioning_mask is None else slice_for_view(
                                            conditioning_mask,
                                            1 if self.controlnets[controlnet_name].use_simplified_condition_embedding else self.vae_scale_factor # type: ignore[index]
                                        )
                                    ))

                        if not controlnet_conds:
                            down_block, mid_block = None, None
                        else:
                            down_block, mid_block = self.get_controlnet_conditioning_blocks(
                                device=device,
                                latents=latent_model_input,
                                timestep=t,
                                encoder_hidden_states=embeds,
                                controlnet_conds=controlnet_conds,
                                added_cond_kwargs=added_cond_kwargs,
                            )
                    else:
                        down_block, mid_block = None, None

                    # add other dimensions to unet input if set
                    if mask is not None and mask_image is not None and self.is_inpainting_unet:
                        latent_model_input = torch.cat(
                            [
                                latent_model_input,
                                slice_for_view(mask),
                                slice_for_view(mask_image),
                            ],
                            dim=1,
                        )

                    # predict the noise residual
                    noise_pred = self.predict_noise_residual(
                        latents=latent_model_input,
                        timestep=t,
                        embeddings=embeds,
                        timestep_cond=timestep_cond,
                        cross_attention_kwargs=cross_attention_kwargs,
                        added_cond_kwargs=added_cond_kwargs,
                        down_block_additional_residuals=down_block,
                        mid_block_additional_residual=mid_block,
                    )

                    # perform guidance
                    if do_classifier_free_guidance:
                        noise_pred_uncond, noise_pred_text = noise_pred.chunk(2)
                        noise_pred = noise_pred_uncond + guidance_scale * (noise_pred_text - noise_pred_uncond)

                    # compute the previous noisy sample x_t -> x_t-1
                    denoised_latents = self.scheduler.step( #type: ignore[attr-defined]
                        noise_pred,
                        t,
                        latents_for_view,
                        **extra_step_kwargs,
                    ).prev_sample

                except IndexError:
                    raise RuntimeError(f"Received IndexError during denoising. It is likely that the scheduler you are using ({type(self.scheduler).__name__}) does not work with Multi-Diffusion, and you should avoid using this when chunking is enabled.")

                # Save chunk scheduler status after sample
                chunk_scheduler_status[j] = self.get_scheduler_state()

                # If using mask and not using fine-tuned inpainting, then we calculate
                # the same denoising on the image without unet and cross with the
                # calculated unet input * mask
                if mask is not None and image is not None and noise is not None and not self.is_inpainting_unet:
                    init_latents = (slice_for_view(image))[:1]
                    init_mask = (slice_for_view(mask))[:1]

                    if i < len(timesteps) - 1:
                        noise_timestep = timesteps[i + 1]
                        init_latents = self.scheduler.add_noise( # type: ignore[attr-defined]
                            init_latents,
                            slice_for_view(noise),
                            torch.tensor([noise_timestep])
                        )

                    denoised_latents = (1 - init_mask) * init_latents + init_mask * denoised_latents

                # Build weights
                multiplier = weight_builder(
                    mask_type=self.tiling_mask_type,
                    batch=samples,
                    dim=num_channels,
                    frames=mask_frames,
                    width=mask_width,
                    height=mask_height,
                    unfeather_left=left==0,
                    unfeather_top=top==0,
                    unfeather_right=right==latent_width,
                    unfeather_bottom=bottom==latent_height,
                    unfeather_start=False if num_frames is None else (start==0 and not chunker.loop),
                    unfeather_end=False if num_frames is None else (end==num_frames and not chunker.loop),
                    **self.tiling_mask_kwargs
                )

                fill_value(denoised_latents * multiplier, multiplier)

                if progress_callback is not None:
                    progress_callback(True)

            # multidiffusion
            latents = torch.where(count > 0, value / count, value)

            # Call the latent callback, if provided
            steps_since_last_callback += 1
            if (
                latent_callback is not None
                and latent_callback_steps is not None
                and steps_since_last_callback >= latent_callback_steps
                and (i == num_steps - 1 or ((i + 1) > num_warmup_steps and (i + 1) % self.scheduler.order == 0)) # type: ignore[attr-defined]
            ):
                if i > num_steps * 0.75 and not self.safety_checking_disabled and self.safety_checker is not None:
                    # Don't call the callback in the final 25% of the image if safety checking is enabled
                    continue

                latent_callback_value = latents

                if latent_callback_type != "latent":
                    latent_callback_value = self.decode_latent_preview(
                        latent_callback_value,
                        weight_builder=weight_builder,
                        device=device,
                    )
                    latent_callback_value = self.denormalize_latents(latent_callback_value)
                    if num_frames is not None:
                        output = [] # type: ignore[assignment]
                        for frame in self.decode_animation_frames(latent_callback_value):
                            output.extend(self.image_processor.numpy_to_pil(frame)) # type: ignore[attr-defined]
                        latent_callback_value = output # type: ignore[assignment]
                    else:
                        if latent_callback_type != "pt":
                            latent_callback_value = self.image_processor.pt_to_numpy(latent_callback_value)
                            if latent_callback_type == "pil":
                                latent_callback_value = self.image_processor.numpy_to_pil(latent_callback_value)

                latent_callback(latent_callback_value)
        if revert_chunker_size is not None:
            chunker.size = revert_chunker_size
        return latents

    def decode_latent_preview(
        self,
        latents: torch.Tensor,
        weight_builder: MaskWeightBuilder,
        device: Union[str, torch.device],
    ) -> torch.Tensor:
        """
        Issues the command to decode latents with the tiny VAE.
        Batches anything > 1024px (128 latent)
        """
        from math import ceil

        shape = latents.shape
        if len(shape) == 5:
            batch, channels, frames, height, width = shape
        else:
            batch, channels, height, width = shape
            frames = None

        height_px = height * self.vae_scale_factor
        width_px = width * self.vae_scale_factor

        max_size = 128
        overlap = 16
        max_size_px = max_size * self.vae_scale_factor

        # Define function to decode a single frame
        def decode_preview(tensor: torch.Tensor) -> torch.Tensor:
            """
            Decodes a single frame
            """
            if height > max_size or width > max_size:
                # Do some chunking to avoid sharp lines, but don't follow global chunk
                width_chunks = ceil(width / (max_size - overlap))
                height_chunks = ceil(height / (max_size - overlap))
                decoded_preview = torch.zeros(
                    (batch, 3, height*self.vae_scale_factor, width*self.vae_scale_factor),
                    dtype=tensor.dtype,
                    device=device
                )
                multiplier = torch.zeros_like(decoded_preview)
                for i in range(height_chunks):
                    start_h = max(0, i * (max_size - overlap))
                    end_h = start_h + max_size
                    if end_h > height:
                        diff = end_h - height
                        end_h -= diff
                        start_h = max(0, start_h-diff)
                    start_h_px = start_h * self.vae_scale_factor
                    end_h_px = end_h * self.vae_scale_factor
                    for j in range(width_chunks):
                        start_w = max(0, j * (max_size - overlap))
                        end_w = start_w + max_size
                        if end_w > width:
                            diff = end_w - width
                            end_w -= diff
                            start_w = max(0, start_w-diff)
                        start_w_px = start_w * self.vae_scale_factor
                        end_w_px = end_w * self.vae_scale_factor
                        mask = weight_builder(
                            mask_type="bilinear",
                            batch=batch,
                            dim=3,
                            width=min(width_px, max_size_px),
                            height=min(height_px, max_size_px),
                            unfeather_left=start_w==0,
                            unfeather_top=start_h==0,
                            unfeather_right=end_w==width,
                            unfeather_bottom=end_h==height,
                        )
                        decoded_view = self.vae_preview.decode(
                            tensor[:, :, start_h:end_h, start_w:end_w],
                            return_dict=False
                        )[0].to(device)
                        decoded_preview[:, :, start_h_px:end_h_px, start_w_px:end_w_px] += decoded_view * mask
                        multiplier[:, :, start_h_px:end_h_px, start_w_px:end_w_px] += mask
                return decoded_preview / multiplier
            else:
                return self.vae_preview.decode(tensor, return_dict=False)[0].to(device)

        # If there are frames, decode them one at a time
        if frames is not None:
            decoded_frames = [
                decode_preview(latents[:, :, i, :, :]).unsqueeze(2)
                for i in range(frames)
            ]
            return torch.cat(decoded_frames, dim=2)
        else:
            return decode_preview(latents)

    def decode_latent_view(self, latents: torch.Tensor) -> torch.Tensor:
        """
        Issues the command to decode a chunk of latents with the VAE.
        """
        return self.vae.decode(latents, return_dict=False)[0]

    def decode_latents_unchunked(
        self,
        latents: torch.Tensor,
        device: Union[str, torch.device]
    ) -> torch.Tensor:
        """
        Decodes the latents using the VAE without chunking.
        """
        return self.decode_latent_view(latents).to(device=device)

    def decode_latents(
        self,
        latents: torch.Tensor,
        device: Union[str, torch.device],
        chunker: Chunker,
        weight_builder: MaskWeightBuilder,
        progress_callback: Optional[Callable[[bool], None]]=None,
        scale_latents: bool=True,
        tiling: bool=False,
        frame_decode_chunk_size: Optional[int]=None,
    ) -> torch.Tensor:
        """
        Decodes the latents in chunks as necessary.
        """
        if len(latents.shape) == 5:
            samples, num_channels, num_frames, height, width = latents.shape
        else:
            samples, num_channels, height, width = latents.shape
            num_frames = None

        height *= self.vae_scale_factor
        width *= self.vae_scale_factor

        if scale_latents:
            latents = 1 / self.vae.config.scaling_factor * latents # type: ignore[attr-defined]

        total_steps = chunker.num_chunks
        revert_dtype = None

        if self.config.force_full_precision_vae: # type: ignore[attr-defined]
            # Resist overflow
            revert_dtype = latents.dtype
            self.vae.to(dtype=torch.float32)
            latents = latents.to(dtype=torch.float32)
            weight_builder.dtype = torch.float32

        if total_steps <= 1 or not tiling:
            result = self.decode_latents_unchunked(latents, device)
            if progress_callback is not None:
                progress_callback(True)
            if self.config.force_full_precision_vae: # type: ignore[attr-defined]
                self.vae.to(dtype=latents.dtype)
            return result

        latent_width = width // self.vae_scale_factor
        latent_height = height // self.vae_scale_factor
        engine_latent_size = self.engine_size // self.vae_scale_factor

        if num_frames is None:
            count = torch.zeros((samples, 3, height, width)).to(device=device, dtype=latents.dtype)
        else:
            count = torch.zeros((samples, 3, num_frames, height, width)).to(device=device, dtype=latents.dtype)

        value = torch.zeros_like(count)

        for j, ((top, bottom), (left, right)) in enumerate(chunker.chunks):
            # Memoize wrap for later
            wrap_x = right <= left
            wrap_y = bottom <= top

            mask_width = ((latent_width - left) + right if wrap_x else right - left) * self.vae_scale_factor
            mask_height = ((latent_height - top) + bottom if wrap_y else bottom - top) * self.vae_scale_factor

            # Define some helpers for chunked denoising
            def slice_for_view(tensor: torch.Tensor, scale_factor: int = 1) -> torch.Tensor:
                """
                Copies and slices input tensors
                """
                left_idx = left * scale_factor
                right_idx = right * scale_factor
                top_idx = top * scale_factor
                bottom_idx = bottom * scale_factor
                height_idx = latent_height * scale_factor
                width_idx = latent_width * scale_factor
                tensor_for_view = torch.clone(tensor)

                if wrap_x:
                    tensor_for_view = torch.cat([tensor_for_view[:, :, :, left_idx:width_idx], tensor_for_view[:, :, :, :right_idx]], dim=3)
                else:
                    tensor_for_view = tensor_for_view[:, :, :, left_idx:right_idx]

                if wrap_y:
                    tensor_for_view = torch.cat([tensor_for_view[:, :, top_idx:height_idx, :], tensor_for_view[:, :, :bottom_idx, :]], dim=2)
                else:
                    tensor_for_view = tensor_for_view[:, :, top_idx:bottom_idx, :]

                return tensor_for_view

            def fill_value(tensor: torch.Tensor, multiplier: torch.Tensor) -> None:
                """
                Fills the value and count tensors
                """
                nonlocal value, count
                start_x = left
                end_x = latent_width if wrap_x else right
                start_x *= self.vae_scale_factor
                end_x *= self.vae_scale_factor
                initial_x = end_x - start_x
                right_px = right * self.vae_scale_factor

                start_y = top
                end_y = latent_height if wrap_y else bottom
                start_y *= self.vae_scale_factor
                end_y *= self.vae_scale_factor
                initial_y = end_y - start_y
                bottom_px = bottom * self.vae_scale_factor

                value[:, :, start_y:end_y, start_x:end_x] += tensor[:, :, :initial_y, :initial_x]
                count[:, :, start_y:end_y, start_x:end_x] += multiplier[:, :, :initial_y, :initial_x]
                if wrap_x:
                    value[:, :, start_y:end_y, :right_px] += tensor[:, :, :initial_y, initial_x:]
                    count[:, :, start_y:end_y, :right_px] += multiplier[:, :, :initial_y, initial_x:]
                    if wrap_y:
                        value[:, :, :bottom_px, :right_px] += tensor[:, :, initial_y:, initial_x:]
                        count[:, :, :bottom_px, :right_px] += multiplier[:, :, initial_y:, initial_x:]
                if wrap_y:
                    value[:, :, :bottom_px, start_x:end_x] += tensor[:, :, initial_y:, :initial_x]
                    count[:, :, :bottom_px, start_x:end_x] += multiplier[:, :, initial_y:, :initial_x]

            # Slice latents
            latents_for_view = slice_for_view(latents)

            # Decode latents
            decoded_latents = self.decode_latent_view(latents_for_view).to(device=device)

            # Build weights
            multiplier = weight_builder(
                mask_type=self.tiling_mask_type,
                batch=samples,
                dim=3,
                frames=None,
                width=mask_width,
                height=mask_height,
                unfeather_left=left==0,
                unfeather_top=top==0,
                unfeather_right=right==latent_width,
                unfeather_bottom=bottom==latent_height,
                **self.tiling_mask_kwargs
            )

            fill_value(decoded_latents * multiplier, multiplier)

            if progress_callback is not None:
                progress_callback(True)

        # re-average pixels
        latents = torch.where(count > 0, value / count, value)
        if revert_dtype is not None:
            latents = latents.to(dtype=revert_dtype)
            self.vae.to(dtype=revert_dtype)

        return latents

    def decode_animation_frames(
        self,
        videos: torch.Tensor,
        n_rows: int = 8,
        rescale: bool = False
    ) -> List[np.ndarray]:
        """
        Decode an animation
        """
        videos = rearrange(videos, "b c t h w -> t b c h w")
        outputs = []
        for x in videos:
            x = torchvision.utils.make_grid(x, nrow=n_rows)
            x = x.transpose(0, 1).transpose(1, 2).squeeze(-1)
            if rescale:
                x = ((x + 1.0) / 2.0).clamp(0.0, 0.98)  # -1,1 -> 0,1
            else:
                x = x.clamp(0.0, 0.98)
            x = (255 - (x * 255)).cpu().numpy().astype(np.uint8)
            outputs.append(x)
        return outputs

    def prepare_extra_step_kwargs(
        self,
        generator: Optional[torch.Generator],
        eta: float
    ) -> Dict[str, Any]:
        """
        Prepares arguments to add during denoising
        """
        accepts_eta = "eta" in set(inspect.signature(self.scheduler.step).parameters.keys()) # type: ignore[attr-defined]
        extra_step_kwargs: Dict[str, Any] = {}
        if accepts_eta:
            extra_step_kwargs["eta"] = eta

        # check if the scheduler accepts generator
        accepts_generator = "generator" in set(inspect.signature(self.scheduler.step).parameters.keys()) # type: ignore[attr-defined]
        if accepts_generator:
            extra_step_kwargs["generator"] = generator
        return extra_step_kwargs

    def get_guidance_scale_embedding(
        self,
        timesteps: torch.Tensor,
        embedding_dim: int=512,
        dtype: torch.dtype=torch.float32
    ) -> torch.Tensor:
        """
        Gets the embeddings of guidance scale for LCM
        """
        assert len(timesteps.shape) == 1
        timesteps = timesteps * 1000.0

        half_dim = embedding_dim // 2
        emb = torch.log(torch.tensor(10000.0)) / (half_dim - 1)
        emb = torch.exp(torch.arange(half_dim, dtype=dtype) * -emb)
        emb = timesteps.to(dtype)[:, None] * emb[None, :]
        emb = torch.cat([torch.sin(emb), torch.cos(emb)], dim=1)
        if embedding_dim % 2 == 1:  # zero pad
            emb = torch.nn.functional.pad(emb, (0, 1))
        assert emb.shape == (timesteps.shape[0], embedding_dim)
        return emb

    def get_step_complete_callback(
        self,
        overall_steps: int,
        progress_callback: Optional[Callable[[int, int, float], None]] = None,
        log_interval: int = 5,
        log_sampling_duration: Union[int, float] = 2,
    ) -> Callable[[bool], None]:
        """
        Creates a scoped callback to trigger during iterations
        """
        overall_step, window_start_step, its = 0, 0, 0.0
        window_start = datetime.datetime.now()
        digits = math.ceil(math.log10(overall_steps))

        def step_complete(increment_step: bool = True) -> None:
            nonlocal overall_step, window_start, window_start_step, its
            if increment_step:
                overall_step += 1
            if overall_step != 0 and overall_step % log_interval == 0 or overall_step == overall_steps:
                seconds_in_window = (datetime.datetime.now() - window_start).total_seconds()
                its = (overall_step - window_start_step) / seconds_in_window
                unit = "s/it" if its < 1 else "it/s"
                its_display = 0 if its == 0 else 1 / its if its < 1 else its
                logger.debug(
                    f"{{0:0{digits}d}}/{{1:0{digits}d}}: {{2:0.2f}} {{3:s}}".format(
                        overall_step, overall_steps, its_display, unit
                    )
                )

                if seconds_in_window > log_sampling_duration:
                    window_start_step = overall_step
                    window_start = datetime.datetime.now()

            if progress_callback is not None:
                progress_callback(overall_step, overall_steps, its)

        return step_complete

    def standardize_image(
        self,
        image: Optional[Union[ImageArgType, torch.Tensor]]=None,
        animation_frames: Optional[int]=None,
    ) -> Optional[Union[torch.Tensor, List[PIL.Image.Image]]]:
        """
        Standardizes image args to list
        """
        if image is None or isinstance(image, torch.Tensor):
            return image
        if not isinstance(image, list):
            image = [image]

        images = []
        for img in image:
            if isinstance(img, str):
                img = self.open_image(img)
            if isinstance(img, list):
                images.extend(img)
            else:
                images.append(img)

        if animation_frames:
            image_len = len(images)
            if image_len < animation_frames:
                images += [
                    images[image_len-1]
                    for i in range(animation_frames - image_len)
                ]
        else:
            images = images[:1]

        return images

    def standardize_ip_adapter_images(
        self,
        images: ImagePromptArgType=None,
        animation_frames: Optional[int]=None,
    ) -> Optional[List[Tuple[List[PIL.Image.Image], float]]]:
        """
        Standardizes IP adapter args to list
        """
        if not images:
            return None

        if not isinstance(images, list):
            images = [images]

        ip_adapter_tuples = []

        for image in images:
            if isinstance(image, tuple):
                img, scale = image
            elif isinstance(image, dict):
                img = image["image"]
                scale = float(image["scale"])
            elif isinstance(image, str):
                img = self.open_image(img)
                scale = 1.0
            else:
                img = image
                scale = 1.0

            if not isinstance(img, list):
                img = [img]

            if animation_frames:
                img = img[:animation_frames]
            else:
                img = img[:1]

            ip_adapter_tuples.append((img, scale))

        return ip_adapter_tuples

    def standardize_control_images(
        self,
        control_images: ControlImageArgType=None,
        animation_frames: Optional[int]=None,
    ) -> Optional[Dict[str, List[ControlImageArgDict]]]:
        """
        Standardizes control images to dict of list of dicts
        """
        if control_images is None:
            return None

        standardized: Dict[str, List[ControlImageArgDict]] = {}

        for name in control_images:
            if name not in self.controlnets: # type: ignore[operator]
                raise RuntimeError(f"Control image mapped to ControlNet {name}, but it is not loaded.")
            standardized[name] = []

            image_list = control_images[name]
            if not isinstance(image_list, list):
                image_list = [image_list]

            is_sparse = isinstance(self.controlnets[name], SparseControlNetModel) # type: ignore[index]

            for controlnet_image in image_list:
                conditioning_scale = 1.0
                conditioning_standalone = False
                conditioning_frame, conditioning_start, conditioning_end = None, None, None
                conditioning_frequency, conditioning_channel = None, None

                if isinstance(controlnet_image, tuple):
                    controlnet_image, conditioning_scale = controlnet_image[:2]
                elif isinstance(controlnet_image, dict):
                    conditioning_scale = controlnet_image.get("scale", conditioning_scale) # type: ignore[assignment]
                    conditioning_start = controlnet_image.get("start", None)
                    conditioning_end = controlnet_image.get("end", None)
                    conditioning_frame = controlnet_image.get("frame", None)
                    conditioning_frequency = controlnet_image.get("frequency", None)
                    conditioning_channel = controlnet_image.get("channel", None)
                    conditioning_standalone = controlnet_image.get("standalone", False)
                    controlnet_image = controlnet_image["image"]

                if isinstance(controlnet_image, str):
                    controlnet_image = self.open_image(controlnet_image)

                if not isinstance(controlnet_image, PIL.Image.Image) and not isinstance(controlnet_image, list):
                    raise IOError(f"Unhandled control image type {type(controlnet_image)}")

                if not isinstance(controlnet_image, list):
                    controlnet_image = [controlnet_image]

                if animation_frames:
                    if is_sparse:
                        if conditioning_frame is None:
                            conditioning_frame = 0
                    else:
                        image_len = len(controlnet_image)
                        if image_len < animation_frames:
                            controlnet_image += [
                                controlnet_image[image_len-1]
                                for i in range(animation_frames - image_len)
                            ]
                else:
                    conditioning_frame = None

                standardized[name].append({
                    "image": controlnet_image,
                    "scale": conditioning_scale,
                    "start": conditioning_start,
                    "end": conditioning_end,
                    "frame": conditioning_frame,
                    "frequency": conditioning_frequency,
                    "channel": conditioning_channel,
                    "standalone": conditioning_standalone
                })

        return standardized

    def standardize_audio(
        self,
        audio: Optional[Tuple[List[int], List[Union[float, Tuple[float, ...]]]]]=None,
        animation_frames: Optional[int]=None,
    ) -> Optional[Tuple[List[int], List[Tuple[float, ...]]]]:
        """
        Standardizes audio to tuples (mono/stereo fix) and slices
        """
        if not audio or not animation_frames:
            return None

        frequencies, amplitudes = audio
        return (
            [int(f) for f in frequencies],
            [tuple(a) for a in amplitudes[:animation_frames]] # type: ignore[arg-type]
        )

    def encode_audio(
        self,
        frequencies: List[int],
        amplitudes: List[Tuple[float, ...]],
        device: torch.device,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Encodes the audio into frequencies and amplitude tensors
        """
        f_tensor = torch.tensor(frequencies).to(device=device, dtype=torch.int32)
        a_tensor = torch.tensor(amplitudes).to(device=device, dtype=torch.float32)
        return (f_tensor, a_tensor)

    @torch.no_grad()
    def __call__(
        self,
        device: Optional[Union[str, torch.device]]=None,
        offload_models: bool=False,
        prompt: Optional[str]=None,
        prompt_2: Optional[str]=None,
        negative_prompt: Optional[str]=None,
        negative_prompt_2: Optional[str]=None,
        prompts: Optional[List[Prompt]]=None,
        audio: Optional[Tuple[List[int], List[Union[float, Tuple[float]]]]]=None,
        image: Optional[Union[ImageArgType, torch.Tensor]]=None,
        mask: Optional[Union[ImageArgType, torch.Tensor]]=None,
        clip_skip: Optional[int]=None,
        freeu_factors: Optional[Tuple[float, float, float, float]]=None,
        control_images: ControlImageArgType=None,
        ip_adapter_images: ImagePromptArgType=None,
        ip_adapter_model: Optional[IP_ADAPTER_LITERAL]=None,
        height: Optional[int]=None,
        width: Optional[int]=None,
        tiling_unet: bool=False,
        tiling_vae: bool=False,
        tiling_size: Optional[int]=None,
        tiling_stride: Optional[int]=None,
        frame_window_size: Optional[int]=None,
        frame_window_stride: Optional[int]=None,
        frame_decode_chunk_size: Optional[int]=None,
        denoising_start: Optional[float]=None,
        denoising_end: Optional[float]=None,
        strength: Optional[float]=0.8,
        num_inference_steps: int=20,
        guidance_scale: float=7.5,
        num_results_per_prompt: int=1,
        animation_frames: Optional[int]=None,
        motion_scale: Optional[float]=None,
        loop: bool=False,
        tile: Union[bool, Tuple[bool, bool]]=False,
        eta: float=0.0,
        generator: Optional[torch.Generator]=None,
        noise_generator: Optional[torch.Generator]=None,
        latents: Optional[torch.Tensor]=None,
        prompt_embeds: Optional[torch.Tensor]=None,
        negative_prompt_embeds: Optional[torch.Tensor]=None,
        output_type: Literal["latent", "pt", "np", "pil"]="pil",
        return_dict: bool=True,
        progress_callback: Optional[Callable[[int, int, float], None]]=None,
        latent_callback: Optional[Callable[[Union[torch.Tensor, np.ndarray, List[PIL.Image.Image]]], None]]=None,
        latent_callback_steps: Optional[int]=None,
        latent_callback_type: Literal["latent", "pt", "np", "pil"]="latent",
        cross_attention_kwargs: Optional[Dict[str, Any]]=None,
        original_size: Optional[Tuple[int, int]]=None,
        crops_coords_top_left: Tuple[int, int]=(0, 0),
        target_size: Optional[Tuple[int, int]]=None,
        aesthetic_score: float=6.0,
        negative_aesthetic_score: float=2.5,
        tiling_mask_type: Optional[MASK_TYPE_LITERAL]=None,
        tiling_mask_kwargs: Optional[Dict[str, Any]]=None,
        noise_offset: Optional[float]=None,
        noise_method: NOISE_METHOD_LITERAL="perlin",
        noise_blend_method: LATENT_BLEND_METHOD_LITERAL="inject",
        num_denoising_iterations: Optional[int]=None,
    ) -> Union[
        StableDiffusionPipelineOutput,
        Tuple[Union[torch.Tensor, np.ndarray, List[PIL.Image.Image]], Optional[List[bool]]],
    ]:
        """
        Invokes the pipeline.
        """
        # 0. Standardize arguments
        image = self.standardize_image(
            image,
            animation_frames=animation_frames
        )
        mask = self.standardize_image(
            mask,
            animation_frames=animation_frames
        )
        control_images = self.standardize_control_images( # type: ignore[assignment]
            control_images,
            animation_frames=animation_frames
        )

        if ip_adapter_images is not None:
            ip_adapter_images = self.standardize_ip_adapter_images(
                ip_adapter_images,
                animation_frames=animation_frames
            )
            ip_adapter_scale = max([scale for _, scale in ip_adapter_images]) # type: ignore[union-attr]
        else:
            ip_adapter_scale = None

        if audio is not None:
            audio = self.standardize_audio( # type: ignore[assignment]
                audio, # type: ignore[arg-type]
                animation_frames=animation_frames
            )
        if audio is not None:
            frequencies, amplitudes = audio
        else:
            frequencies, amplitudes = None, None

        # 1. Default height and width to image or unet config
        if not height:
            if isinstance(image, list):
                _, height = image[0].size
            elif isinstance(image, torch.Tensor):
                height = image.shape[-2] * self.vae_scale_factor
            else:
                height = self.unet.config.sample_size * self.vae_scale_factor # type: ignore[attr-defined]

        if not width:
            if isinstance(image, list):
                width, _ = image[0].size
            elif isinstance(image, torch.Tensor):
                width = image.shape[-1] * self.vae_scale_factor
            else:
                width = self.unet.config.sample_size * self.vae_scale_factor # type: ignore[attr-defined]

        height = cast(int, height)
        width = cast(int, width)

        # Training details
        original_size = original_size or (height, width)
        target_size = target_size or (height, width)

        # Allow overridding tiling variables
        if tiling_size:
            self.tiling_size = tiling_size
        if tiling_stride is not None:
            self.tiling_stride = tiling_stride
        if tiling_mask_type is not None:
            self.tiling_mask_type = tiling_mask_type
        if tiling_mask_kwargs is not None:
            self.tiling_mask_kwargs = tiling_mask_kwargs
        if frame_window_size is not None:
            self.frame_window_size = frame_window_size
        if frame_window_stride is not None:
            self.frame_window_stride = frame_window_stride

        # Check 0/None
        if latent_callback_steps == 0:
            latent_callback_steps = None
        if animation_frames == 0:
            animation_frames = None

        # Check denoising iterations
        if num_denoising_iterations is None or not animation_frames:
            num_denoising_iterations = 1

        # Convenient bool for later
        decode_intermediates = latent_callback_steps is not None and latent_callback is not None

        # Define outputs here to process later
        prepared_latents: Optional[torch.Tensor] = None
        output_nsfw: Optional[List[bool]] = None

        # Define call parameters
        if prompt_embeds:
            batch_size = prompt_embeds.shape[0]
        else:
            batch_size = 1
            if prompt is None and prompts is None:
                prompt = "high-quality, best quality, aesthetically pleasing" # Good luck!

        if self.is_inpainting_unet:
            if image is None:
                logger.warning("No image present, but using inpainting model. Adding blank image.")
                image = [PIL.Image.new("RGB", (width, height))]
            if mask is None:
                logger.warning("No mask present, but using inpainting model. Adding blank mask.")
                mask = [PIL.Image.new("RGB", (width, height), (255, 255, 255))]
            if self.is_sdxl and strength == 1.0:
                logger.debug("Adjusting strength from 1.0 to 0.99 for SDXL inpainting fix.")
                strength = 0.99

        if device is None:
            device = torch.device("cpu")
        elif isinstance(device, str):
            device = torch.device(device)

        try:
            has_time_cond_proj = self.unet.config.time_cond_proj_dim is not None # type: ignore[attr-defined]
        except AttributeError:
            has_time_cond_proj = False

        do_classifier_free_guidance = guidance_scale > 1.0 and not has_time_cond_proj

        # Calculate chunks
        chunker = Chunker(
            height=height,
            width=width,
            size=self.tiling_size if self.tiling_size else 1024 if self.is_sdxl else 512,
            stride=self.tiling_stride,
            frames=animation_frames,
            frame_size=self.frame_window_size,
            frame_stride=self.frame_window_stride,
            loop=loop,
            tile=tile,
        )

        num_chunks = chunker.num_chunks 
        num_temporal_chunks = chunker.num_frame_chunks

        if strength is not None and image is not None and floor(num_inference_steps * strength) == 0:
            required_steps = ceil(1.0 / strength)
            logger.warning(f"Strength and steps combination will result in no inference steps, changing `num_inference_steps` to {required_steps}")
            num_inference_steps = required_steps

        self.scheduler.set_timesteps(num_inference_steps, device=device) # type: ignore[attr-defined]

        if image is not None and (strength is not None or denoising_start is not None):
            # Scale timesteps by strength
            timesteps, num_inference_steps = self.get_timesteps(
                num_inference_steps,
                strength,
                denoising_start=denoising_start
            )
        else:
            timesteps = self.scheduler.timesteps # type: ignore[attr-defined]

        batch_size *= num_results_per_prompt
        num_scheduled_inference_steps = len(timesteps)

        # Calculate end of steps if we aren't going all the way
        if denoising_end is not None and type(denoising_end) == float and denoising_end > 0 and denoising_end < 1:
            discrete_timestep_cutoff = int(
                round(
                    self.scheduler.config.num_train_timesteps # type: ignore[attr-defined]
                    - (denoising_end * self.scheduler.config.num_train_timesteps) # type: ignore[attr-defined]
                )
            )
            num_scheduled_inference_steps = len(list(filter(lambda ts: ts >= discrete_timestep_cutoff, timesteps)))
            timesteps = timesteps[:num_scheduled_inference_steps]

        # Calculate total steps including all unet and vae calls
        encoding_steps = 0
        decoding_steps = 1

        # Open images if they're files
        if isinstance(image, str):
            image = self.open_image(image) # type: ignore[unreachable]
        if isinstance(mask, str):
            mask = self.open_image(mask) # type: ignore[unreachable]

        if image is not None and type(image) is not torch.Tensor:
            if isinstance(image, list):
                encoding_steps += len(image)
            else:
                encoding_steps += 1
        if mask is not None and type(mask) is not torch.Tensor:
            if isinstance(mask, list):
                encoding_steps += len(mask)
            else:
                encoding_steps += 1
            if not self.is_inpainting_unet:
                if isinstance(image, list):
                    encoding_steps += len(image)
                else:
                    encoding_steps += 1
        if ip_adapter_images is not None:
            image_prompt_probes = sum([
                len(images) for images, scale in ip_adapter_images
            ])
        else:
            image_prompt_probes = 0
        if control_images:
            for controlnet_name in control_images:
                if getattr(self.controlnets[controlnet_name], "use_simplified_condition_embedding", False): # type: ignore[index]
                    for control_image_dict in control_images[controlnet_name]:
                        control_image = control_image_dict["image"] # type: ignore
                        if isinstance(control_image, list):
                            encoding_steps += len(control_image)
                        else:
                            encoding_steps += 1

        num_frames = 1 if not animation_frames else animation_frames
        unet_spatial_chunks = (1 if not tiling_unet else num_chunks)
        unet_steps = unet_spatial_chunks * num_temporal_chunks * num_scheduled_inference_steps * num_denoising_iterations

        vae_chunks = (1 if not tiling_vae else num_chunks)
        decode_chunk_size = 1 if not frame_decode_chunk_size else frame_decode_chunk_size
        frame_decode_steps = ceil(num_frames / decode_chunk_size)
        vae_steps = vae_chunks * (encoding_steps + (decoding_steps * frame_decode_steps))
        if prompts is not None:
            clip_steps = len(prompts)
        else:
            clip_steps = 1

        overall_num_steps = image_prompt_probes + unet_steps + vae_steps + clip_steps

        logger.debug(
            " ".join([
                f"Calculated overall steps to be {overall_num_steps}.",
                f"{image_prompt_probes} image prompt embedding probe(s) +",
                f"{clip_steps} prompt encoding step(s) +",
                f"{unet_steps} UNet step(s) ({unet_spatial_chunks} spatial chunk(s) * {num_temporal_chunks} temporal chunk(s) * {num_scheduled_inference_steps} inference step(s) * {num_denoising_iterations} denoising iteration(s)) +",
                f"{vae_steps} VAE step(s) ({vae_chunks} chunk(s) * ({encoding_steps} encoding step(s) + ({decoding_steps} decoding step(s) * ({num_frames} frame(s) / {decode_chunk_size} frame(s) per decode))))"
            ])
        )

        # Create a callback which gets passed to stepped functions
        step_complete = self.get_step_complete_callback(overall_num_steps, progress_callback)

        if self.config.force_full_precision_vae: # type: ignore[attr-defined]
            logger.debug(f"Configuration indicates VAE must be used in full precision")
            # make sure the VAE is in float32 mode, as it overflows in float16
            self.vae.to(dtype=torch.float32)
        elif self.is_sdxl:
            logger.debug(f"Configuration indicates VAE may operate in half precision")
            self.vae.to(dtype=torch.float16)

        with self.get_runtime_context(
            batch_size=batch_size,
            animation_frames=animation_frames,
            device=device,
            ip_adapter_scale=ip_adapter_scale,
            step_complete=step_complete
        ):
            # First standardize to list of prompts
            if prompts is None:
                prompts = [
                    Prompt(
                        positive=prompt,
                        positive_2=prompt_2,
                        negative=negative_prompt,
                        negative_2=negative_prompt_2,
                        start=None,
                        end=None,
                        weight=None,
                        frequency=None,
                        channel=None,
                    )
                ]

            encoded_prompt_list = []
            # Iterate over given prompts and encode
            for given_prompt in prompts:
                if self.is_sdxl:
                    # XL uses more inputs for prompts than 1.5
                    (
                        these_prompt_embeds,
                        these_negative_prompt_embeds,
                        these_pooled_prompt_embeds,
                        these_negative_pooled_prompt_embeds,
                    ) = self.encode_prompt(
                        given_prompt.positive,
                        device,
                        num_results_per_prompt,
                        do_classifier_free_guidance,
                        given_prompt.negative,
                        prompt_embeds=prompt_embeds,
                        negative_prompt_embeds=negative_prompt_embeds,
                        prompt_2=given_prompt.positive_2,
                        negative_prompt_2=given_prompt.negative_2,
                        clip_skip=clip_skip
                    )
                else:
                    these_prompt_embeds = self.encode_prompt(
                        given_prompt.positive,
                        device,
                        num_results_per_prompt,
                        do_classifier_free_guidance,
                        given_prompt.negative,
                        prompt_embeds=prompt_embeds,
                        negative_prompt_embeds=negative_prompt_embeds,
                        prompt_2=given_prompt.positive_2,
                        negative_prompt_2=given_prompt.negative_2,
                        clip_skip=clip_skip
                    )  # type: ignore
                    these_pooled_prompt_embeds = None
                    these_negative_prompt_embeds = None
                    these_negative_pooled_prompt_embeds = None

                step_complete(True)

                encoded_prompt_list.append(
                    EncodedPrompt(
                        prompt=given_prompt,
                        embeds=these_prompt_embeds, # type: ignore[arg-type]
                        negative_embeds=these_negative_prompt_embeds,
                        pooled_embeds=these_pooled_prompt_embeds,
                        negative_pooled_embeds=these_negative_pooled_prompt_embeds
                    )
                )

            encoded_prompts = EncodedPrompts(
                prompts=encoded_prompt_list,
                is_sdxl=self.is_sdxl,
                do_classifier_free_guidance=do_classifier_free_guidance,
                image_prompt_embeds=None, # Will be set later
                image_uncond_prompt_embeds=None # Will be set later
            )

            # Encode audio if present
            if frequencies and amplitudes:
                frequencies, amplitudes = self.encode_audio( # type: ignore[assignment]
                    frequencies=frequencies,
                    amplitudes=amplitudes, # type: ignore[arg-type]
                    device=device
                )

            # Remove any alpha mask on image, convert mask to grayscale, align tensors
            if image is not None:
                if isinstance(image, torch.Tensor):
                    image = image.to(device=device, dtype=encoded_prompts.dtype)
                else:
                    image = [img.convert("RGB") for img in image]
            if mask is not None:
                if isinstance(mask, torch.Tensor):
                    mask = mask.to(device=device, dtype=encoded_prompts.dtype)
                else:
                    mask = [img.convert("L") for img in mask]

            # Repeat images as necessary to get the same size
            image_length = max([
                0 if image is None else len(image),
                0 if mask is None else len(mask),
            ])

            if image is not None and not isinstance(image, torch.Tensor):
                l = len(image)
                for i in range(image_length - l):
                    image.append(image[-1])
            if mask is not None and not isinstance(mask, torch.Tensor):
                l = len(mask)
                for i in range(image_length - l):
                    mask.append(mask[-1])

            # Process image and mask or image
            prepared_image: Optional[torch.Tensor] = None
            prepared_mask: Optional[torch.Tensor] = None
            init_image: Optional[torch.Tensor] = None

            if image is not None and mask is not None:
                prepared_image = torch.Tensor()
                prepared_mask = torch.Tensor()
                init_image = torch.Tensor()

                for m, i in zip(mask, image):
                    p_m, p_i, i_i = self.prepare_mask_and_image(m, i, True) # type: ignore
                    prepared_mask = torch.cat([prepared_mask, p_m.unsqueeze(0)])
                    prepared_image = torch.cat([prepared_image, p_i.unsqueeze(0)])
                    init_image = torch.cat([init_image, i_i.unsqueeze(0)])

            elif image is not None and mask is None:
                if isinstance(image, torch.Tensor):
                    prepared_image = image.unsqueeze(0)
                else:
                    prepared_image = torch.Tensor()
                    for i in image:
                        prepared_image = torch.cat([
                            prepared_image,
                            self.image_processor.preprocess(i).unsqueeze(0)
                        ])

            # Build the weight builder
            weight_builder = MaskWeightBuilder(
                device=device,
                dtype=encoded_prompts.dtype
            )

            with weight_builder:
                if prepared_image is not None and prepared_mask is not None:
                    # Inpainting
                    num_channels_latents = self.vae.config.latent_channels # type: ignore[attr-defined]

                    if latents:
                        prepared_latents = latents.to(device) * self.schedule.init_noise_sigma # type: ignore[attr-defined]
                    else:
                        if strength is not None and strength < 1.0:
                            prepared_latents = self.prepare_image_latents(
                                image=init_image.to(device=device), # type: ignore[union-attr]
                                timestep=timesteps[:1].repeat(batch_size),
                                batch_size=batch_size,
                                dtype=encoded_prompts.dtype,
                                device=device,
                                chunker=chunker,
                                weight_builder=weight_builder,
                                generator=generator,
                                progress_callback=step_complete,
                                add_noise=denoising_start is None,
                                animation_frames=animation_frames,
                                tiling=tiling_vae
                            )
                        else:
                            prepared_latents = self.create_latents(
                                batch_size,
                                num_channels_latents,
                                height,
                                width,
                                encoded_prompts.dtype,
                                device,
                                generator,
                                animation_frames=animation_frames
                            )

                    prepared_mask, prepared_image_latents = self.prepare_mask_latents(
                        mask=prepared_mask.to(device=device),
                        image=prepared_image.to(device=device),
                        batch_size=batch_size,
                        height=height,
                        width=width,
                        dtype=encoded_prompts.dtype,
                        device=device,
                        chunker=chunker,
                        generator=generator,
                        weight_builder=weight_builder,
                        do_classifier_free_guidance=do_classifier_free_guidance,
                        progress_callback=step_complete,
                        animation_frames=animation_frames,
                        tiling=tiling_vae,
                    )

                    if init_image is not None:
                        init_image = self.prepare_image_latents(
                            image=init_image.to(device=device),
                            timestep=timesteps[:1].repeat(batch_size),
                            batch_size=batch_size,
                            dtype=encoded_prompts.dtype,
                            device=device,
                            chunker=chunker,
                            weight_builder=weight_builder,
                            generator=generator,
                            progress_callback=step_complete,
                            add_noise=False,
                            animation_frames=animation_frames,
                            tiling=tiling_vae,
                        )
                    # prepared_latents = noise or init latents + noise
                    # prepared_mask = only mask
                    # prepared_image_latents = masked image
                    # init_image = only image when not using inpainting unet
                elif prepared_image is not None and strength is not None:
                    # img2img
                    prepared_latents = self.prepare_image_latents(
                        image=prepared_image.to(device=device),
                        timestep=timesteps[:1].repeat(batch_size),
                        batch_size=batch_size,
                        dtype=encoded_prompts.dtype,
                        device=device,
                        chunker=chunker,
                        weight_builder=weight_builder,
                        generator=generator,
                        progress_callback=step_complete,
                        add_noise=denoising_start is None,
                        animation_frames=animation_frames,
                        tiling=tiling_vae,
                    )
                    prepared_image_latents = None # Don't need to store these separately
                    # prepared_latents = img + noise
                elif latents:
                    prepared_latents = latents.to(device) * self.scheduler.init_noise_sigma # type: ignore[attr-defined]
                    # prepared_latents = passed latents + noise
                else:
                    # txt2img
                    prepared_image_latents = None
                    prepared_latents = self.create_latents(
                        batch_size=batch_size,
                        num_channels_latents=self.unet.config.in_channels, # type: ignore[attr-defined]
                        height=height,
                        width=width,
                        dtype=encoded_prompts.dtype,
                        device=device,
                        generator=generator,
                        animation_frames=animation_frames
                    )
                    # prepared_latents = noise

                # Look for controlnet and conditioning image, prepare
                prepared_control_images: PreparedControlImageArgType = {}
                if control_images is not None:
                    if not self.controlnets:
                        logger.warning("Control image passed, but no controlnet present. Ignoring.")
                        prepared_control_images = None
                    else:
                        for name in control_images:
                            is_sparse = type(self.controlnets[name]) is SparseControlNetModel

                            prepared_control_images[name] = [] # type: ignore[index]

                            sparse_condition_scale = 0.0
                            sparse_conditioning_start: Optional[float] = None
                            sparse_conditioning_end: Optional[float] = None
                            sparse_conditions: List[torch.Tensor] = []
                            sparse_masks: List[torch.Tensor] = []

                            for controlnet_image_dict in control_images[name]:
                                # Gather variables
                                controlnet_image_dict = cast(ControlImageArgDict, controlnet_image_dict)
                                controlnet_image = controlnet_image_dict["image"]
                                conditioning_scale = controlnet_image_dict.get("scale", 1.0)
                                conditioning_start = controlnet_image_dict.get("start", 0.0)
                                conditioning_end = controlnet_image_dict.get("end", 0.0)
                                conditioning_frame = controlnet_image_dict.get("frame", None)
                                conditioning_standalone = controlnet_image_dict.get("standalone", False)
                                conditioning_frequency = controlnet_image_dict.get("frequency", None)
                                conditioning_channel = controlnet_image_dict.get("channel", None)

                                if is_sparse:
                                    if self.controlnets[name].use_simplified_condition_embedding:
                                        controlnet_image = self.image_processor.preprocess([
                                            i.convert("RGB") for i in controlnet_image # type: ignore
                                        ]).to(dtype=encoded_prompts.dtype, device=device)
                                        controlnet_image = self.encode_image(
                                            image=controlnet_image,
                                            device=device,
                                            generator=generator,
                                            dtype=encoded_prompts.dtype,
                                            chunker=chunker,
                                            weight_builder=weight_builder,
                                            progress_callback=step_complete,
                                            tiling=tiling_vae
                                        )

                                    prepared_controlnet_image, prepared_controlnet_mask = self.prepare_control_image(
                                        image=controlnet_image,
                                        height=height,
                                        width=width,
                                        batch_size=batch_size,
                                        num_results_per_prompt=num_results_per_prompt,
                                        device=device,
                                        dtype=encoded_prompts.dtype,
                                        do_classifier_free_guidance=do_classifier_free_guidance,
                                        animation_frames=1 if not animation_frames else animation_frames,
                                        conditioning_frame=0 if not conditioning_frame else conditioning_frame
                                    )

                                    if conditioning_standalone:
                                        # Sparse on its own (blending sparse controls)
                                        if conditioning_frequency is not None and frequencies is not None and amplitudes is not None and animation_frames:
                                            audio_mask = weight_builder.audio(
                                                frames=list(range(animation_frames)),
                                                frequencies=frequencies, # type: ignore[arg-type]
                                                amplitudes=amplitudes, # type: ignore[arg-type]
                                                frequency=conditioning_frequency, # type: ignore[arg-type]
                                                channel=conditioning_channel
                                            )
                                            conditioning_scale = audio_mask * conditioning_scale # type: ignore[assignment]

                                        prepared_control_images[name].append( # type: ignore[index]
                                            (prepared_controlnet_image, conditioning_scale, conditioning_start, conditioning_end, prepared_controlnet_mask) # type: ignore[arg-type]
                                        )
                                        
                                    else:
                                        sparse_conditions.append(prepared_controlnet_image)
                                        sparse_masks.append(prepared_controlnet_mask)
                                        sparse_condition_scale = max(sparse_condition_scale, conditioning_scale) # type: ignore

                                        if conditioning_start is not None:
                                            if sparse_conditioning_start is None:
                                                sparse_conditioning_start = conditioning_start
                                            else:
                                                sparse_conditioning_start = min(sparse_conditioning_start, conditioning_start)
                                        if conditioning_end is not None:
                                            if sparse_conditioning_end is None:
                                                sparse_conditioning_end = conditioning_end
                                            else:
                                                sparse_conditioning_end = min(sparse_conditioning_end, conditioning_end)
                                else:
                                    prepared_controlnet_image = self.prepare_control_image(
                                        image=controlnet_image,
                                        height=height,
                                        width=width,
                                        batch_size=batch_size,
                                        num_results_per_prompt=num_results_per_prompt,
                                        device=device,
                                        dtype=encoded_prompts.dtype,
                                        do_classifier_free_guidance=do_classifier_free_guidance,
                                        animation_frames=animation_frames,
                                        conditioning_frame=None
                                    )

                                    if conditioning_frequency is not None and frequencies is not None and amplitudes is not None and animation_frames:
                                        audio_mask = weight_builder.audio(
                                            frames=list(range(animation_frames)),
                                            frequencies=frequencies, # type: ignore[arg-type]
                                            amplitudes=amplitudes, # type: ignore[arg-type]
                                            frequency=conditioning_frequency, # type: ignore[arg-type]
                                            channel=conditioning_channel
                                        )
                                        conditioning_scale = audio_mask * conditioning_scale # type: ignore[assignment]

                                    prepared_control_images[name].append( # type: ignore[index]
                                        (prepared_controlnet_image, conditioning_scale, conditioning_start, conditioning_end, None) # type: ignore[arg-type]
                                    )

                            if is_sparse and len(sparse_conditions) > 0:
                                # Create single condition
                                sparse_condition = torch.zeros_like(sparse_conditions[0])
                                sparse_mask = torch.zeros_like(sparse_masks[0])
                                for condition, mask in zip(sparse_conditions, sparse_masks):
                                    sparse_condition += condition
                                    sparse_mask += mask

                                prepared_control_images[name].append( # type: ignore[index]
                                    (sparse_condition, sparse_condition_scale, sparse_conditioning_start, sparse_conditioning_end, sparse_mask)
                                )

                # Should no longer be None
                prepared_latents = cast(torch.Tensor, prepared_latents)

                # Check if we need to cut multi-images
                if not animation_frames:
                    if prepared_mask is not None:
                        prepared_mask = prepared_mask[:, 0]
                    if prepared_image_latents is not None:
                        prepared_image_latents = prepared_image_latents[:, 0]

                # Prepare extra step kwargs
                extra_step_kwargs = self.prepare_extra_step_kwargs(generator, eta)

                # Get prompt embeds here if using IP adapter
                if ip_adapter_images is not None:
                    logger.debug(f"Performing {image_prompt_probes} image prompt probe(s)")
                    ip_adapter_image_embeds = torch.Tensor().to(
                        device=device,
                        dtype=encoded_prompts.dtype
                    )
                    ip_adapter_image_uncond_embeds = torch.Tensor().to(
                        device=device,
                        dtype=encoded_prompts.dtype
                    )
                    for images, scale in ip_adapter_images:
                        image_prompt_embeds = torch.Tensor().to(
                            device=device,
                            dtype=encoded_prompts.dtype
                        )
                        image_uncond_prompt_embeds = torch.Tensor().to(
                            device=device,
                            dtype=encoded_prompts.dtype
                        )
                        for img in images:
                            image_embeds, uncond_embeds = self.get_image_embeds(
                                img,
                                num_results_per_prompt
                            )
                            step_complete(True)
                            image_prompt_embeds = torch.cat([
                                image_prompt_embeds,
                                image_embeds.unsqueeze(0)
                            ], dim=0)
                            image_uncond_prompt_embeds = torch.cat([
                                image_uncond_prompt_embeds,
                                uncond_embeds.unsqueeze(0)
                            ], dim=0)

                        # Repeat last image embed as needed to match frames
                        if animation_frames:
                            embed_frames = image_prompt_embeds.shape[0]
                            if embed_frames < animation_frames:
                                image_prompt_embeds = torch.cat([
                                    image_prompt_embeds,
                                    image_prompt_embeds[-1].unsqueeze(0).repeat(animation_frames - embed_frames + 1, 1, 1, 1)
                                ], dim=0)
                                image_uncond_prompt_embeds = torch.cat([
                                    image_uncond_prompt_embeds,
                                    image_uncond_prompt_embeds[-1].unsqueeze(0).repeat(animation_frames - embed_frames + 1, 1, 1, 1)
                                ], dim=0)
                            

                        image_prompt_embeds *= scale / ip_adapter_scale # type: ignore[operator]
                        image_uncond_prompt_embeds *= scale / ip_adapter_scale # type: ignore[operator]

                        ip_adapter_image_embeds = torch.cat([
                            ip_adapter_image_embeds,
                            image_prompt_embeds.unsqueeze(0)
                        ], dim=0)
                        ip_adapter_image_uncond_embeds = torch.cat([
                            ip_adapter_image_uncond_embeds,
                            image_uncond_prompt_embeds.unsqueeze(0)
                        ], dim=0)

                    # Assign to helper data class
                    encoded_prompts.image_prompt_embeds = ip_adapter_image_embeds
                    encoded_prompts.image_uncond_prompt_embeds = ip_adapter_image_uncond_embeds

                # Prepared added time IDs (SDXL)
                added_cond_kwargs: Optional[Dict[str, Any]] = None
                if self.is_sdxl:
                    added_cond_kwargs = {}
                    if self.config.requires_aesthetic_score: # type: ignore[attr-defined]
                        add_time_ids, add_neg_time_ids = self.get_add_time_ids(
                            original_size=original_size,
                            crops_coords_top_left=crops_coords_top_left,
                            target_size=target_size,
                            dtype=encoded_prompts.dtype,
                            aesthetic_score=aesthetic_score,
                            negative_aesthetic_score=negative_aesthetic_score,
                        )
                        if do_classifier_free_guidance:
                            add_time_ids = torch.cat([add_neg_time_ids, add_time_ids], dim=0)
                    else:
                        add_time_ids, _ = self.get_add_time_ids(
                            original_size=original_size,
                            crops_coords_top_left=crops_coords_top_left,
                            target_size=target_size,
                            dtype=encoded_prompts.dtype,
                        )
                        if do_classifier_free_guidance:
                            add_time_ids = torch.cat([add_time_ids, add_time_ids], dim=0)
                    add_time_ids = add_time_ids.to(device).repeat(batch_size, 1)
                    added_cond_kwargs["time_ids"] = add_time_ids
            
                # Set guidance scale embedding (LCM)
                timestep_cond: Optional[torch.Tensor] = None
                if "time_cond_proj_dim" in self.unet.config and self.unet.config.time_cond_proj_dim is not None: # type: ignore[attr-defined]
                    guidance_scale_tensor = torch.tensor(guidance_scale - 1).repeat(batch_size)
                    timestep_cond = self.get_guidance_scale_embedding(
                        guidance_scale_tensor,
                        embedding_dim=self.unet.config.time_cond_proj_dim, # type: ignore[attr-defined]
                        dtype=encoded_prompts.dtype
                    ).to(device=device)

                # Make sure controlnet on device
                if self.controlnets is not None:
                    for name in self.controlnets:
                        self.controlnets[name].to(device=device)

                # Unload VAE, and maybe preview VAE
                self.vae.to("cpu")
                if decode_intermediates:
                    self.vae_preview.to(device, dtype=encoded_prompts.dtype)

                empty_cache()

                # Inject noise
                if noise_offset is not None and noise_offset > 0 and denoising_start is None:
                    noise_timestep = timesteps[:1].repeat(batch_size).to("cpu", dtype=torch.int)
                    schedule_factor = (1 - self.scheduler.alphas_cumprod[noise_timestep]) ** 0.5 # type: ignore
                    schedule_factor = schedule_factor.flatten()[0] # type: ignore
                    logger.debug(f"Adding {noise_method} noise by method {noise_blend_method} and factor {schedule_factor*noise_offset:.4f} - offset is {noise_offset:.2f}, scheduled alpha cumulative product is {schedule_factor:.4f}")
                    noise_latents = make_noise(
                        batch_size=prepared_latents.shape[0],
                        channels=prepared_latents.shape[1],
                        animation_frames=animation_frames,
                        height=height // self.vae_scale_factor,
                        width=width // self.vae_scale_factor,
                        generator=noise_generator,
                        device=device,
                        dtype=prepared_latents.dtype,
                        method=noise_method,
                    )
                    prepared_latents = blend_latents(
                        left=prepared_latents,
                        right=noise_latents,
                        time=noise_offset,
                        method=noise_blend_method
                    )

                # Make sure unet is on device
                self.align_unet(
                    device=device,
                    dtype=encoded_prompts.dtype,
                    freeu_factors=freeu_factors,
                    animation_frames=animation_frames,
                    motion_scale=motion_scale,
                    offload_models=offload_models
                ) # May be overridden by RT

                initial_noisy_latents = None
                freq_filter = None
                for i in range(num_denoising_iterations):
                    if i == 0 and num_denoising_iterations > 1:
                        initial_noisy_latents = prepared_latents.detach().clone()
                        freq_filter = get_freq_filter(
                            prepared_latents.shape,
                            device=device,
                            filter_type=self.frequencies_filter_type,
                            n=self.frequencies_filter_order,
                            d_s=self.frequencies_filter_stop_spatial,
                            d_t=self.frequencies_filter_stop_temporal,
                        )
                    elif i > 0:
                        # Invoke callback if requested
                        if latent_callback is not None and (self.safety_checking_disabled or self.safety_checker is None):
                            latent_callback_value = prepared_latents

                            if latent_callback_type != "latent":
                                latent_callback_value = self.decode_latent_preview(
                                    latent_callback_value,
                                    weight_builder=weight_builder,
                                    device=device,
                                )
                                latent_callback_value = self.denormalize_latents(latent_callback_value)
                                if animation_frames:
                                    output = [] # type: ignore[assignment]
                                    for frame in self.decode_animation_frames(latent_callback_value):
                                        output.extend(self.image_processor.numpy_to_pil(frame)) # type: ignore[attr-defined]
                                    latent_callback_value = output # type: ignore[assignment]
                                else:
                                    if latent_callback_type != "pt":
                                        latent_callback_value = self.image_processor.pt_to_numpy(latent_callback_value)
                                        if latent_callback_type == "pil":
                                            latent_callback_value = self.image_processor.numpy_to_pil(latent_callback_value)

                            latent_callback(latent_callback_value)

                        # 1. DDPM Forward with initial noise
                        current_diffuse_timestep = self.scheduler.config.num_train_timesteps - 1 # type: ignore[attr-defined]
                        diffuse_timesteps = torch.full((1,), int(current_diffuse_timestep))
                        diffuse_timesteps = diffuse_timesteps.long()
                        z_T = self.scheduler.add_noise( # type: ignore[attr-defined]
                            original_samples=prepared_latents,
                            noise=initial_noisy_latents.to(device), # type: ignore[union-attr]
                            timesteps=diffuse_timesteps
                        )

                        # 2. create random noise z_rand for high-frequencies
                        z_rand = randn_tensor(
                            prepared_latents.shape,
                            generator=generator,
                            device=device,
                            dtype=torch.float32
                        )

                        # 3. Noise Reinitialization
                        prepared_latents = freq_mix_3d(
                            z_T.to(dtype=torch.float32),
                            z_rand,
                            low_pass_filter=freq_filter, # type: ignore[arg-type]
                        )
                        prepared_latents = prepared_latents.to(initial_noisy_latents.dtype) # type: ignore[union-attr]

                    # Denoising loop
                    prepared_latents = self.denoise(
                        height=height,
                        width=width,
                        device=device,
                        num_inference_steps=num_scheduled_inference_steps,
                        chunker=chunker,
                        weight_builder=weight_builder,
                        timesteps=timesteps,
                        latents=prepared_latents,
                        encoded_prompts=encoded_prompts,
                        guidance_scale=guidance_scale,
                        timestep_cond=timestep_cond,
                        do_classifier_free_guidance=do_classifier_free_guidance,
                        mask=prepared_mask,
                        mask_image=prepared_image_latents,
                        image=init_image,
                        control_images=prepared_control_images,
                        progress_callback=step_complete,
                        latent_callback=latent_callback,
                        latent_callback_steps=latent_callback_steps,
                        latent_callback_type=latent_callback_type,
                        extra_step_kwargs=extra_step_kwargs,
                        cross_attention_kwargs=cross_attention_kwargs,
                        added_cond_kwargs=added_cond_kwargs,
                        tiling=tiling_unet,
                        frequencies=frequencies, # type: ignore[arg-type]
                        amplitudes=amplitudes, # type: ignore[arg-type]
                    )

                # Clear no longer needed tensors
                del prepared_mask
                del prepared_image_latents

                # Unload controlnets to free memory
                if self.controlnets is not None:
                    for name in self.controlnets:
                        self.controlnets[name].to("cpu")
                    del prepared_control_images

                # Unload UNet to free memory
                if offload_models:
                    self.unet.to("cpu")
                    empty_cache()

                # Load VAE if decoding
                if output_type != "latent":
                    self.vae.to(
                        dtype=torch.float32 if self.config.force_full_precision_vae else prepared_latents.dtype, # type: ignore[attr-defined]
                        device=device
                    )
                    if self.is_sdxl:
                        use_torch_2_0_or_xformers = self.vae.decoder.mid_block.attentions[0].processor in [ # type: ignore[union-attr]
                            AttnProcessor2_0,
                            XFormersAttnProcessor,
                            LoRAXFormersAttnProcessor,
                            LoRAAttnProcessor2_0,
                        ]
                        # if xformers or torch_2_0 is used attention block does not need
                        # to be in float32 which can save lots of memory
                        if not use_torch_2_0_or_xformers:
                            self.vae.post_quant_conv.to(prepared_latents.dtype)
                            self.vae.decoder.conv_in.to(prepared_latents.dtype)
                            self.vae.decoder.mid_block.to(prepared_latents.dtype) # type: ignore
                        else:
                            prepared_latents = prepared_latents.float()

                if output_type == "latent":
                    output = prepared_latents # type: ignore[assignment]
                else:
                    prepared_latents = self.decode_latents(
                        prepared_latents,
                        device=device,
                        chunker=chunker,
                        progress_callback=step_complete,
                        weight_builder=weight_builder,
                        tiling=tiling_vae,
                        frame_decode_chunk_size=frame_decode_chunk_size,
                    )
                    if not animation_frames:
                        output = self.denormalize_latents(prepared_latents) # type: ignore[assignment]
                        if output_type != "pt":
                            output = self.image_processor.pt_to_numpy(output)
                            output_nsfw = self.run_safety_checker(output, device, encoded_prompts.dtype)[1] # type: ignore[arg-type]
                            if output_type == "pil":
                                output = self.image_processor.numpy_to_pil(output)
                    else:
                        output = [] # type: ignore[assignment]
                        for frame in self.decode_animation_frames(prepared_latents):
                            output.extend(self.image_processor.numpy_to_pil(frame)) # type: ignore[attr-defined]

                if offload_models:
                    # Offload VAE again
                    self.vae.to("cpu")
                    self.vae_preview.to("cpu")
                elif self.config.force_full_precision_vae: #type: ignore[attr-defined]
                    self.vae.to(dtype=prepared_latents.dtype)

            if hasattr(self, "final_offload_hook") and self.final_offload_hook is not None:
                self.final_offload_hook.offload()

            empty_cache()

            if not return_dict:
                return (output, output_nsfw)

            return StableDiffusionPipelineOutput(images=output, nsfw_content_detected=output_nsfw) # type: ignore[arg-type]
