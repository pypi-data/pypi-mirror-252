# Inspired by https://github.com/guoyww/AnimateDiff/blob/main/animatediff/pipelines/pipeline_animation.py
from __future__ import annotations

import os
import torch
import torch.nn.functional as F

from typing import Optional, Dict, Any, Union, Callable, List, TYPE_CHECKING

from pibble.util.files import load_json

from diffusers.utils import WEIGHTS_NAME
from diffusers.models.modeling_utils import ModelMixin
from diffusers.schedulers import EulerDiscreteScheduler

from einops import rearrange

from enfugue.util import logger

from enfugue.diffusion.constants import *
from enfugue.diffusion.pipeline import EnfugueStableDiffusionPipeline
from enfugue.diffusion.util.torch_util import load_state_dict

from enfugue.diffusion.animate.diff.unet import UNet3DConditionModel as AnimateDiffUNet # type: ignore[attr-defined]
from enfugue.diffusion.animate.diffxl.unet import UNet3DConditionModel as AnimateDiffXLUNet # type: ignore[attr-defined]
from enfugue.diffusion.animate.hotshot.unet import UNet3DConditionModel as HotshotUNet # type: ignore[attr-defined]

if TYPE_CHECKING:
    from transformers import (
        CLIPTokenizer,
        CLIPTextModel,
        CLIPImageProcessor,
        CLIPTextModelWithProjection,
        CLIPVisionModelWithProjection
    )
    from diffusers.models import (
        AutoencoderKL,
        AutoencoderTiny,
        ControlNetModel,
        UNet2DConditionModel,
        ConsistencyDecoderVAE,
    )
    from diffusers.pipelines.stable_diffusion import (
        StableDiffusionSafetyChecker
    )
    from diffusers.schedulers import KarrasDiffusionSchedulers
    from enfugue.diffusion.support.ip import IPAdapter
    from enfugue.diffusion.util import Chunker, MaskWeightBuilder
    from enfugue.diffusion.constants import MASK_TYPE_LITERAL

class EnfugueAnimateStableDiffusionPipeline(EnfugueStableDiffusionPipeline):
    unet_3d: Optional[Union[AnimateDiffUNet, HotshotUNet]]
    vae: AutoencoderKL

    STATIC_SCHEDULER_KWARGS = {
        "num_train_timesteps": 1000,
        "beta_start": 0.00085,
        "beta_end": 0.012,
        "beta_schedule": "linear",
        "steps_offset": 1
    }

    MOTION_MODULE_HOTSHOT = "https://huggingface.co/hotshotco/Hotshot-XL/resolve/main/hsxl_temporal_layers.safetensors"
    MOTION_MODULE_HOTSHOT_FP16 = "https://huggingface.co/hotshotco/Hotshot-XL/resolve/main/hsxl_temporal_layers.f16.safetensors"

    MOTION_MODULE = "https://huggingface.co/guoyww/animatediff/resolve/main/mm_sd_v15.ckpt"
    MOTION_MODULE_V2 = "https://huggingface.co/guoyww/animatediff/resolve/main/mm_sd_v15_v2.ckpt"
    MOTION_MODULE_V3 = "https://huggingface.co/guoyww/animatediff/resolve/main/v3_sd15_mm.ckpt"
    MOTION_MODULE_PE_KEY = "down_blocks.0.motion_modules.0.temporal_transformer.transformer_blocks.0.attention_blocks.0.pos_encoder.pe"
    MOTION_MODULE_MID_KEY = "mid_block.motion_modules.0.temporal_transformer.norm.weight"
    MOTION_MODULE_XL = "https://huggingface.co/guoyww/animatediff/resolve/main/mm_sdxl_v10_beta.ckpt"

    def __init__(
        self,
        vae: Union[AutoencoderKL, ConsistencyDecoderVAE],
        vae_preview: AutoencoderTiny,
        text_encoder: Optional[CLIPTextModel],
        text_encoder_2: Optional[CLIPTextModelWithProjection],
        tokenizer: Optional[CLIPTokenizer],
        tokenizer_2: Optional[CLIPTokenizer],
        unet: UNet2DConditionModel,
        scheduler: KarrasDiffusionSchedulers,
        safety_checker: StableDiffusionSafetyChecker,
        feature_extractor: CLIPImageProcessor,
        image_encoder: Optional[CLIPVisionModelWithProjection] = None,
        requires_safety_checker: bool = True,
        force_zeros_for_empty_prompt: bool = True,
        requires_aesthetic_score: bool = False,
        force_full_precision_vae: bool = False,
        controlnets: Optional[Dict[str, ControlNetModel]] = None,
        ip_adapter: Optional[IPAdapter] = None,
        engine_size: int = 512,  # Recommended even for machines that can handle more
        tiling_size: Optional[int] = None,
        tiling_stride: Optional[int] = 32,
        tiling_mask_type: MASK_TYPE_LITERAL = "bilinear",
        tiling_mask_kwargs: Dict[str, Any] = {},
        frame_window_size: Optional[int] = 16,
        frame_window_stride: Optional[int] = 4,
        override_scheduler_config: bool = True,
    ) -> None:
        super(EnfugueAnimateStableDiffusionPipeline, self).__init__(
            vae=vae,
            vae_preview=vae_preview,
            text_encoder=text_encoder,
            text_encoder_2=text_encoder_2,
            tokenizer=tokenizer,
            tokenizer_2=tokenizer_2,
            unet=unet,
            scheduler=scheduler,
            safety_checker=safety_checker,
            feature_extractor=feature_extractor,
            image_encoder=image_encoder,
            requires_safety_checker=requires_safety_checker,
            force_zeros_for_empty_prompt=force_zeros_for_empty_prompt,
            force_full_precision_vae=force_full_precision_vae,
            requires_aesthetic_score=requires_aesthetic_score,
            controlnets=controlnets,
            ip_adapter=ip_adapter,
            engine_size=engine_size,
            tiling_stride=tiling_stride,
            tiling_size=tiling_size,
            tiling_mask_type=tiling_mask_type,
            tiling_mask_kwargs=tiling_mask_kwargs,
            frame_window_size=frame_window_size,
            frame_window_stride=frame_window_stride
        )

        if override_scheduler_config:
            self.scheduler_config = {
                **self.scheduler_config,
                **EnfugueAnimateStableDiffusionPipeline.STATIC_SCHEDULER_KWARGS
            }
            self.scheduler.register_to_config( # type: ignore[attr-defined]
                **EnfugueAnimateStableDiffusionPipeline.STATIC_SCHEDULER_KWARGS
            )

        if not self.is_sdxl and not isinstance(self.scheduler, EulerDiscreteScheduler):
            logger.debug(f"Animation pipeline changing default scheduler from {type(self.scheduler).__name__} to Euler Discrete")
            self.scheduler = EulerDiscreteScheduler.from_config(self.scheduler_config)

    @classmethod
    def from_pretrained(
        cls,
        pretrained_model_name_or_path: Optional[Union[str, os.PathLike]],
        vae_preview: AutoencoderTiny,
        motion_module: str,
        cache_dir: str,
        position_encoding_truncate_length: Optional[int]=None,
        position_encoding_scale_length: Optional[int]=None,
        task_callback: Optional[Callable[[str], None]]=None,
        **kwargs: Any
    ) -> EnfugueAnimateStableDiffusionPipeline:
        """
        Override from_pretrained to reload the unet as a 3D condition model instead.
        """
        pipe = super(EnfugueAnimateStableDiffusionPipeline, cls).from_pretrained(
            pretrained_model_name_or_path,
            vae_preview=vae_preview,
            **kwargs
        )
        unet_dir = os.path.join(pretrained_model_name_or_path, "unet") # type: ignore[arg-type]
        unet_config = os.path.join(unet_dir, "config.json")
        unet_weights = os.path.join(unet_dir, WEIGHTS_NAME)

        is_sdxl = os.path.exists(os.path.join(pretrained_model_name_or_path, "text_encoder_2")) # type: ignore[arg-type]

        if not os.path.exists(unet_config):
            raise IOError(f"Couldn't find UNet config at {unet_config}")
        if not os.path.exists(unet_weights):
            # Check for safetensors version
            safetensors_weights = os.path.join(unet_dir, "diffusion_pytorch_model.safetensors")
            if os.path.exists(safetensors_weights):
                unet_weights = safetensors_weights
            else:
                raise IOError(f"Couldn't find UNet weights at {unet_weights} or {safetensors_weights}")

        unet = cls.create_unet(
            load_json(unet_config),
            cache_dir,
            is_sdxl=is_sdxl,
            is_inpainter=False,
            motion_module=motion_module,
            position_encoding_truncate_length=position_encoding_truncate_length,
            position_encoding_scale_length=position_encoding_scale_length,
            task_callback=task_callback,
        )

        state_dict = load_state_dict(unet_weights)

        for key in list(state_dict.keys()):
            if "motion" in key or "temporal" in key:
                state_dict.pop(key)

        unet.load_state_dict(state_dict, strict=False)

        if "torch_dtype" in kwargs:
            unet = unet.to(kwargs["torch_dtype"])

        pipe.unet = unet

        return pipe

    @classmethod
    def create_unet(
        cls,
        config: Dict[str, Any],
        cache_dir: str,
        is_sdxl: bool,
        is_inpainter: bool,
        task_callback: Optional[Callable[[str], None]]=None,
        **unet_additional_kwargs: Any
    ) -> ModelMixin:
        """
        Creates the 3D Unet
        """
        motion_module: Optional[str] = unet_additional_kwargs.pop("motion_module", None)
        if motion_module is None:
            raise RuntimeError("Did not receive a motion module.")

        animate_diff_mm_version: bool = unet_additional_kwargs.pop("animate_diff_mm_version", 3)
        use_hotshot: bool = unet_additional_kwargs.pop("use_hotshot", True)
        position_encoding_truncate_length: Optional[int] = unet_additional_kwargs.pop("position_encoding_truncate_length", None)
        position_encoding_scale_length: Optional[int] = unet_additional_kwargs.pop("position_encoding_scale_length", None)

        if is_sdxl:
            if use_hotshot:
                return cls.create_hotshot_unet(
                    config=config,
                    motion_module=motion_module,
                    task_callback=task_callback,
                    position_encoding_truncate_length=position_encoding_truncate_length,
                    position_encoding_scale_length=position_encoding_scale_length,
                    **unet_additional_kwargs
                )
            return cls.create_diff_xl_unet(
                config=config,
                motion_module=motion_module,
                task_callback=task_callback,
                position_encoding_truncate_length=position_encoding_truncate_length,
                position_encoding_scale_length=position_encoding_scale_length,
                **unet_additional_kwargs
            )
        return cls.create_diff_unet(
            config=config,
            motion_module=motion_module,
            animate_diff_mm_version=animate_diff_mm_version,
            task_callback=task_callback,
            position_encoding_truncate_length=position_encoding_truncate_length,
            position_encoding_scale_length=position_encoding_scale_length,
            **unet_additional_kwargs
        )

    @classmethod
    def create_hotshot_unet(
        cls,
        config: Dict[str, Any],
        motion_module: str,
        motion_dir: Optional[str]=None,
        task_callback: Optional[Callable[[str], None]]=None,
        position_encoding_truncate_length: Optional[int]=None,
        position_encoding_scale_length: Optional[int]=None,
        **unet_additional_kwargs: Any
    ) -> ModelMixin:
        """
        Creates a UNet3DConditionModel then loads hotshot into it
        """
        config["_class_name"] = "UNet3DConditionModel"
        config["down_block_types"] = [
            "DownBlock3D",
            "CrossAttnDownBlock3D",
            "CrossAttnDownBlock3D",
        ]
        config["up_block_types"] = [
            "CrossAttnUpBlock3D",
            "CrossAttnUpBlock3D",
            "UpBlock3D"
        ]
        if position_encoding_scale_length:
            config["positional_encoding_max_length"] = position_encoding_scale_length

        # Instantiate from 2D model config
        model = HotshotUNet.from_config(config)

        # Load motion weights into it
        cls.load_hotshot_state_dict(
            unet=model,
            motion_module=motion_module,
            task_callback=task_callback,
            position_encoding_truncate_length=position_encoding_truncate_length,
            position_encoding_scale_length=position_encoding_scale_length,
        )
        return model

    @classmethod
    def load_hotshot_state_dict(
        cls,
        unet: HotshotUNet,
        motion_module: str,
        task_callback: Optional[Callable[[str], None]]=None,
        position_encoding_truncate_length: Optional[int]=None,
        position_encoding_scale_length: Optional[int]=None,
    ) -> None:
        """
        Loads pretrained hotshot weights into the UNet
        """
        message = f"Loading HotShot XL motion module {os.path.basename(motion_module)}"
        if task_callback is not None:
            task_callback(message)
        logger.debug(f"{message} with truncate length '{position_encoding_truncate_length}' and scale length '{position_encoding_scale_length}'")
        hotshot_state_dict = load_state_dict(motion_module)
        for key in list(hotshot_state_dict.keys()):
            if "temporal" not in key:
                hotshot_state_dict.pop(key)
            elif key.endswith(".positional_encoding"): # type: ignore
                if position_encoding_truncate_length is not None:
                    hotshot_state_dict[key] = hotshot_state_dict[key][:, :position_encoding_truncate_length] # type: ignore[index]
                if position_encoding_scale_length is not None:
                    tensor_shape = hotshot_state_dict[key].shape # type: ignore[union-attr]
                    tensor = rearrange(hotshot_state_dict[key], "(t b) f d -> t b f d", t=1)
                    tensor = F.interpolate(tensor, size=(position_encoding_scale_length, tensor_shape[-1]), mode="bilinear")
                    hotshot_state_dict[key] = rearrange(tensor, "t b f d -> (t b) f d") # type: ignore[assignment]
                    del tensor

        num_motion_keys = len(hotshot_state_dict.keys())
        logger.debug(f"Loading {num_motion_keys} keys into UNet state dict (non-strict)")
        unet.load_state_dict(hotshot_state_dict, strict=False)
        del hotshot_state_dict

    @classmethod
    def create_diff_unet(
        cls,
        config: Dict[str, Any],
        motion_module: str,
        animate_diff_mm_version:int=3,
        task_callback: Optional[Callable[[str], None]]=None,
        position_encoding_truncate_length: Optional[int]=None,
        position_encoding_scale_length: Optional[int]=None,
        **unet_additional_kwargs: Any
    ) -> ModelMixin:
        """
        Creates a UNet3DConditionModel then loads MM into it
        """
        config["_class_name"] = "UNet3DConditionModel"
        config["down_block_types"] = [
            "CrossAttnDownBlock3D",
            "CrossAttnDownBlock3D",
            "CrossAttnDownBlock3D",
            "DownBlock3D"
        ]
        config["up_block_types"] = [
            "UpBlock3D",
            "CrossAttnUpBlock3D",
            "CrossAttnUpBlock3D",
            "CrossAttnUpBlock3D"
        ]

        # Detect MM version
        logger.debug(f"Loading motion module {motion_module} to detect MMV1/2/3")
        state_dict = load_state_dict(motion_module)

        if cls.MOTION_MODULE_PE_KEY in state_dict:
            position_tensor: torch.Tensor = state_dict[cls.MOTION_MODULE_PE_KEY] # type: ignore[assignment]
            if position_tensor.shape[1] == 24:
                animate_diff_mm_version = 1
                logger.debug("Detected MMV1")
            elif position_tensor.shape[1] == 32:
                if cls.MOTION_MODULE_MID_KEY in state_dict:
                    animate_diff_mm_version = 2
                    logger.debug("Detected MMV2")
                else:
                    animate_diff_mm_version = 3
                    logger.debug("Detected MMV3")
            else:
                if position_tensor.shape[1] > 32:
                    # Long AnimateDiff
                    if position_encoding_scale_length:
                        position_encoding_scale_length = min(position_encoding_scale_length, position_tensor.shape[1])
                    else:
                        position_encoding_scale_length = position_tensor.shape[1]
                else:
                    raise ValueError(f"Position encoder tensor has unsupported length {position_tensor.shape[1]}")
        else:
            raise ValueError(f"Couldn't detect motion module version from {motion_module}. It may be an unsupported format.")

        motion_module = state_dict # type: ignore[assignment]

        config["mid_block_type"] = "UNetMidBlock3DCrossAttn"
        default_position_encoding_len = 32 if animate_diff_mm_version >= 2 else 24
        position_encoding_len = default_position_encoding_len
        if position_encoding_scale_length:
            position_encoding_len = position_encoding_scale_length

        unet_additional_kwargs["use_inflated_groupnorm"] = animate_diff_mm_version >= 2
        unet_additional_kwargs["unet_use_cross_frame_attention"] = False
        unet_additional_kwargs["unet_use_temporal_attention"] = False
        unet_additional_kwargs["use_motion_module"] = True
        unet_additional_kwargs["motion_module_resolutions"] = [1, 2, 4, 8]
        unet_additional_kwargs["motion_module_mid_block"] = animate_diff_mm_version == 2
        unet_additional_kwargs["motion_module_decoder_only"] = False
        unet_additional_kwargs["motion_module_type"] = "Vanilla"
        unet_additional_kwargs["motion_module_kwargs"] = {
            "num_attention_heads": 8,
            "num_transformer_block": 1,
            "attention_block_types": [
                "Temporal_Self",
                "Temporal_Self"
            ],
            "temporal_position_encoding": True,
            "temporal_position_encoding_max_len": position_encoding_len,
            "temporal_attention_dim_div": 1
        }

        model = AnimateDiffUNet.from_config(config, **unet_additional_kwargs)
        model.position_encoding_truncate_length = position_encoding_truncate_length
        model.position_encoding_scale_length = position_encoding_scale_length

        cls.load_diff_state_dict(
            unet=model,
            motion_module=motion_module,
            animate_diff_mm_version=animate_diff_mm_version,
            task_callback=task_callback,
            position_encoding_truncate_length=position_encoding_truncate_length,
            position_encoding_scale_length=position_encoding_scale_length,
        )
        return model

    @classmethod
    def load_diff_state_dict(
        cls,
        unet: AnimateDiffUNet,
        motion_module: Union[str, Dict[str, torch.Tensor]],
        animate_diff_mm_version: int=3,
        task_callback: Optional[Callable[[str], None]]=None,
        position_encoding_truncate_length: Optional[int]=None,
        position_encoding_scale_length: Optional[int]=None,
    ) -> None:
        """
        Loads animate diff state dict into an animate diff unet
        """
        if isinstance(motion_module, dict):
            logger.debug(f"Loading AnimateDiff motion module with truncate length '{position_encoding_truncate_length}' and scale length '{position_encoding_scale_length}'")

            state_dict = motion_module
        else:
            logger.debug(f"Loading AnimateDiff motion module {motion_module} with truncate length '{position_encoding_truncate_length}' and scale length '{position_encoding_scale_length}'")

            state_dict = load_state_dict(motion_module) # type: ignore[assignment]

        state_dict.pop("animatediff_config", "")
        if position_encoding_truncate_length is not None or position_encoding_scale_length is not None:
            for key in state_dict:
                if key.endswith(".pe"):
                    if position_encoding_truncate_length is not None:
                        state_dict[key] = state_dict[key][:, :position_encoding_truncate_length] # type: ignore[index]
                    if position_encoding_scale_length is not None:
                        tensor_shape = state_dict[key].shape # type: ignore[union-attr]
                        tensor = rearrange(state_dict[key], "(t b) f d -> t b f d", t=1)
                        tensor = F.interpolate(tensor, size=(position_encoding_scale_length, tensor_shape[-1]), mode="bilinear")
                        state_dict[key] = rearrange(tensor, "t b f d -> (t b) f d") # type: ignore[assignment]
                        del tensor

        num_motion_keys = len(list(state_dict.keys()))
        logger.debug(f"Loading {num_motion_keys} keys into AnimateDiff UNet v{animate_diff_mm_version} state dict (non-strict)")
        unet.load_state_dict(state_dict, strict=False)
        del state_dict

    @classmethod
    def load_diff_xl_state_dict(
        cls,
        unet: AnimateDiffXLUNet,
        motion_module: Union[str, Dict[str, torch.Tensor]],
        task_callback: Optional[Callable[[str], None]]=None,
        position_encoding_truncate_length: Optional[int]=None,
        position_encoding_scale_length: Optional[int]=None,
    ) -> None:
        """
        Loads animate diff state dict into an animate diff unet
        """
        if isinstance(motion_module, dict):
            logger.debug(f"Loading AnimateDiffXL motion module with truncate length '{position_encoding_truncate_length}' and scale length '{position_encoding_scale_length}'")

            state_dict = motion_module
        else:
            logger.debug(f"Loading AnimateDiffXL motion module {motion_module} with truncate length '{position_encoding_truncate_length}' and scale length '{position_encoding_scale_length}'")

            state_dict = load_state_dict(motion_module) # type: ignore[assignment]

        state_dict.pop("animatediff_config", "")
        if position_encoding_truncate_length is not None or position_encoding_scale_length is not None:
            for key in state_dict:
                if key.endswith(".pe"):
                    if position_encoding_truncate_length is not None:
                        state_dict[key] = state_dict[key][:, :position_encoding_truncate_length] # type: ignore[index]
                    if position_encoding_scale_length is not None:
                        tensor_shape = state_dict[key].shape # type: ignore[union-attr]
                        tensor = rearrange(state_dict[key], "(t b) f d -> t b f d", t=1)
                        tensor = F.interpolate(tensor, size=(position_encoding_scale_length, tensor_shape[-1]), mode="bilinear")
                        state_dict[key] = rearrange(tensor, "t b f d -> (t b) f d") # type: ignore[assignment]
                        del tensor

        num_motion_keys = len(list(state_dict.keys()))
        logger.debug(f"Loading {num_motion_keys} keys into AnimateDiff XL UNet state dict (non-strict)")
        unet.load_state_dict(state_dict, strict=False)
        del state_dict

    @classmethod
    def create_diff_xl_unet(
        cls,
        config: Dict[str, Any],
        motion_module: str,
        task_callback: Optional[Callable[[str], None]]=None,
        position_encoding_truncate_length: Optional[int]=None,
        position_encoding_scale_length: Optional[int]=None,
        **unet_additional_kwargs: Any
    ) -> ModelMixin:
        """
        Creates a UNet3DConditionModel then loads MMXL into it
        """
        config["_class_name"] = "UNet3DConditionModel"
        config["down_block_types"] = [
            "DownBlock3D",
            "CrossAttnDownBlock3D",
            "CrossAttnDownBlock3D",
        ]
        config["up_block_types"] = [
            "CrossAttnUpBlock3D",
            "CrossAttnUpBlock3D",
            "UpBlock3D"
        ]
        config["mid_block_type"] = "UNetMidBlock3DCrossAttn"
        default_position_encoding_len = 32
        position_encoding_len = default_position_encoding_len
        if position_encoding_scale_length:
            position_encoding_len = position_encoding_scale_length

        unet_additional_kwargs["use_motion_module"] = True
        unet_additional_kwargs["motion_module_resolutions"] = [1, 2, 4, 8]
        unet_additional_kwargs["motion_module_mid_block"] = False
        unet_additional_kwargs["motion_module_type"] = "Vanilla"
        unet_additional_kwargs["motion_module_kwargs"] = {
            "num_attention_heads": 8,
            "num_transformer_block": 1,
            "attention_block_types": [
                "Temporal_Self",
                "Temporal_Self"
            ],
            "temporal_position_encoding": True,
            "temporal_position_encoding_max_len": position_encoding_len,
            "temporal_attention_dim_div": 1
        }

        model = AnimateDiffXLUNet.from_config(config, **unet_additional_kwargs)
        cls.load_diff_xl_state_dict(
            unet=model,
            motion_module=motion_module,
            task_callback=task_callback,
            position_encoding_truncate_length=position_encoding_truncate_length,
            position_encoding_scale_length=position_encoding_scale_length,
        )
        return model

    def get_sparse_controlnet_config(self, use_simplified_embedding: bool) -> Dict[str, Any]:
        """
        Gets configuration for the sparse controlnet.
        """
        config = super(EnfugueAnimateStableDiffusionPipeline, self).get_sparse_controlnet_config(use_simplified_embedding)
        encoding_length = getattr(self.unet, "position_encoding_scale_length", None)
        if encoding_length is None:
            encoding_length = 32
        return {
            **config,
            **{
                "use_motion_module": True,
                "motion_module_resolutions": [1,2,4,8],
                "motion_module_mid_block": False,
                "motion_module_type": "Vanilla",
                "motion_module_kwargs": {
                    "num_attention_heads": 8,
                    "num_transformer_block": 1,
                    "attention_block_types": ["Temporal_Self"],
                    "temporal_position_encoding": True,
                    "temporal_position_encoding_max_len": encoding_length,
                    "temporal_attention_dim_div": 1
                }
            }
        }

    def load_motion_module_weights(
        self,
        motion_module: str,
        task_callback: Optional[Callable[[str], None]]=None,
        position_encoding_truncate_length: Optional[int]=None,
        position_encoding_scale_length: Optional[int]=None,
        animate_diff_mm_version: int=3,
    ) -> None:
        """
        Loads motion module weights after-the-fact
        """
        self.unet.position_encoding_truncate_length = position_encoding_truncate_length # type: ignore[assignment]
        self.unet.position_encoding_scale_length = position_encoding_scale_length # type: ignore[assignment]
        if self.is_sdxl:
            self.load_hotshot_state_dict(
                unet=self.unet,
                motion_module=motion_module,
                task_callback=task_callback,
                position_encoding_truncate_length=position_encoding_truncate_length,
                position_encoding_scale_length=position_encoding_scale_length
            )
        else:
            self.load_diff_state_dict(
                unet=self.unet,
                motion_module=motion_module,
                task_callback=task_callback,
                animate_diff_mm_version=animate_diff_mm_version,
                position_encoding_truncate_length=position_encoding_truncate_length,
                position_encoding_scale_length=position_encoding_scale_length
            )

    def load_motion_lora_weights(
        self,
        state_dict: Dict[str, torch.Tensor],
        multiplier: float = 1.0,
        dtype: torch.dtype = torch.float32
    ) -> None:
        """
        Loads motion LoRA checkpoint into the unet
        """
        for key in state_dict:
            if "up." in key:
                continue
            up_key = key.replace(".down.", ".up.")
            model_key = key.replace("processor.", "").replace("_lora", "").replace("down.", "").replace("up.", "")
            model_key = model_key.replace("to_out.", "to_out.0.")
            layer_infos = model_key.split(".")[:-1]

            curr_layer = self.unet
            while len(layer_infos) > 0:
                temp_name = layer_infos.pop(0)
                curr_layer = getattr(curr_layer, temp_name, None) # type: ignore[assignment]
                if curr_layer is None:
                    break # type: ignore[unreachable]

            if curr_layer is None:
                logger.warning(f"Couldn't find layer to load LoRA state key {key}, skipping.") # type: ignore[unreachable]
                continue

            weight_down = state_dict[key].to(dtype)
            weight_up   = state_dict[up_key].to(dtype)
            curr_layer.weight.data += multiplier * torch.mm(weight_up, weight_down).to(curr_layer.weight.data.device)

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
        Decodes each video frame individually.
        """
        from math import ceil
        animation_frames = latents.shape[2]

        if scale_latents:
            latents = latents / self.vae.config.scaling_factor # type: ignore[attr-defined]

        latents = rearrange(latents, "b c f h w -> (b f) c h w")
        dtype = latents.dtype
        # Force full precision VAE
        #self.vae = self.vae.to(torch.float32)
        #latents = latents.to(torch.float32)
        video: List[torch.Tensor] = []
        total_batch_size = latents.shape[0]
        decode_chunk_size = 1 if not frame_decode_chunk_size else frame_decode_chunk_size
        decode_chunks = ceil(total_batch_size / decode_chunk_size)
        for i in range(decode_chunks):
            start_index = (i * decode_chunk_size)
            video.append(
                super(EnfugueAnimateStableDiffusionPipeline, self).decode_latents(
                    latents=latents[start_index:start_index+decode_chunk_size],
                    device=device,
                    weight_builder=weight_builder,
                    chunker=chunker,
                    progress_callback=progress_callback,
                    scale_latents=False,
                    tiling=tiling
                )
            )
        video = torch.cat(video) # type: ignore
        video = rearrange(video, "(b f) c h w -> b c f h w", f = animation_frames) # type: ignore
        video = (video / 2 + 0.5).clamp(0, 1.0) # type: ignore
        video = video.cpu().float() # type: ignore
        #self.vae.to(dtype)
        return video # type: ignore
