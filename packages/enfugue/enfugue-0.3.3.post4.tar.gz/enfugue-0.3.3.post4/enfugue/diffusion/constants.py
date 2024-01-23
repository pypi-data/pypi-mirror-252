from __future__ import annotations

import os

from typing import (
    Optional,
    Union,
    Tuple,
    Literal,
    List,
    TYPE_CHECKING
)
from typing_extensions import (
    TypedDict,
    NotRequired
)
from enfugue.util import (
    IMAGE_FIT_LITERAL,
    IMAGE_ANCHOR_LITERAL
)

if TYPE_CHECKING:
    from PIL.Image import Image

__all__ = [
    "UpscaleStepDict",
    "ImageDict",
    "IPAdapterImageDict",
    "ControlImageDict",
    "PromptDict",
    "MotionVectorPointDict",
    "DEFAULT_MODEL",
    "DEFAULT_INPAINTING_MODEL",
    "DEFAULT_SDXL_MODEL",
    "DEFAULT_SDXL_REFINER",
    "DEFAULT_SDXL_INPAINTING_MODEL",
    "SDXL_TURBO_MODEL",
    "PLAYGROUND_V2_MODEL",
    "SEGMIND_VEGA_MODEL",
    "OPEN_DALLE_MODEL",
    "ANIMAGINE_MODEL",
    "VAE_EMA",
    "VAE_MSE",
    "VAE_XL",
    "VAE_XL16",
    "VAE_CONSISTENCY",
    "VAE_PREVIEW",
    "VAE_PREVIEW_XL",
    "CONTROLNET_SPARSE_RGB",
    "CONTROLNET_SPARSE_SCRIBBLE",
    "CONTROLNET_CANNY",
    "CONTROLNET_CANNY_XL",
    "CONTROLNET_MLSD",
    "CONTROLNET_HED",
    "CONTROLNET_SCRIBBLE",
    "CONTROLNET_TILE",
    "CONTROLNET_INPAINT",
    "CONTROLNET_DEPTH",
    "CONTROLNET_DEPTH_XL",
    "CONTROLNET_NORMAL",
    "CONTROLNET_POSE",
    "CONTROLNET_POSE_XL",
    "CONTROLNET_PIDI",
    "CONTROLNET_PIDI_XL",
    "CONTROLNET_LINE",
    "CONTROLNET_ANIME",
    "CONTROLNET_TEMPORAL",
    "CONTROLNET_QR",
    "CONTROLNET_QR_XL",
    "CONTROLNET_LITERAL",
    "MOTION_LORA_ZOOM_IN",
    "MOTION_LORA_ZOOM_OUT",
    "MOTION_LORA_PAN_LEFT",
    "MOTION_LORA_PAN_RIGHT",
    "MOTION_LORA_ROLL_CLOCKWISE",
    "MOTION_LORA_ROLL_ANTI_CLOCKWISE",
    "MOTION_LORA_TILT_UP",
    "MOTION_LORA_TILT_DOWN",
    "MOTION_LORA_LITERAL",
    "LCM_LORA_DEFAULT",
    "LCM_LORA_XL",
    "LCM_LORA_VEGA",
    "SPARSE_CONTROLNET_ADAPTER_LORA",
    "DPO_OFFSET_XL",
    "DPO_OFFSET",
    "DPO_LORA_XL",
    "DPO_LORA",
    "OFFSET_LORA_XL",
    "SCHEDULER_LITERAL",
    "DEVICE_LITERAL",
    "PIPELINE_SWITCH_MODE_LITERAL",
    "UPSCALE_LITERAL",
    "MASK_TYPE_LITERAL",
    "LOOP_TYPE_LITERAL",
    "DEFAULT_CHECKPOINT_DIR",
    "DEFAULT_INVERSION_DIR",
    "DEFAULT_LORA_DIR",
    "DEFAULT_LYCORIS_DIR",
    "DEFAULT_TENSORRT_DIR",
    "DEFAULT_CACHE_DIR",
    "DEFAULT_OTHER_DIR",
    "DEFAULT_DIFFUSERS_DIR",
    "DEFAULT_SIZE",
    "DEFAULT_SDXL_SIZE",
    "DEFAULT_TEMPORAL_SIZE",
    "DEFAULT_TILING_SIZE",
    "DEFAULT_TILING_STRIDE",
    "DEFAULT_TEMPORAL_TILING_SIZE",
    "DEFAULT_IMAGE_CALLBACK_STEPS",
    "DEFAULT_CONDITIONING_SCALE",
    "DEFAULT_IMG2IMG_STRENGTH",
    "DEFAULT_INFERENCE_STEPS",
    "DEFAULT_GUIDANCE_SCALE",
    "DEFAULT_UPSCALE_PROMPT",
    "DEFAULT_UPSCALE_INFERENCE_STEPS",
    "DEFAULT_UPSCALE_GUIDANCE_SCALE",
    "DEFAULT_UPSCALE_TILING_SIZE",
    "DEFAULT_UPSCALE_TILING_STRIDE",
    "DEFAULT_REFINER_START",
    "DEFAULT_REFINER_STRENGTH",
    "DEFAULT_REFINER_GUIDANCE_SCALE",
    "DEFAULT_AESTHETIC_SCORE",
    "DEFAULT_NEGATIVE_AESTHETIC_SCORE",
    "MODEL_PROMPT_WEIGHT",
    "GLOBAL_PROMPT_UPSCALE_WEIGHT",
    "MAX_IMAGE_SCALE",
    "LATENT_BLEND_METHOD_LITERAL",
    "NOISE_METHOD_LITERAL",
    "IP_ADAPTER_LITERAL",
    "ANIMATION_ENGINE_LITERAL",
    "OPTICAL_FLOW_METHOD_LITERAL"
]

DEFAULT_MODEL = "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.ckpt"
DEFAULT_INPAINTING_MODEL = "https://huggingface.co/runwayml/stable-diffusion-inpainting/resolve/main/sd-v1-5-inpainting.ckpt"
DEFAULT_SDXL_MODEL = "https://huggingface.co/benjamin-paine/sd-xl-alternative-bases/resolve/main/sd_xl_base_1.0_fp16_vae.safetensors"
DEFAULT_SDXL_REFINER = "https://huggingface.co/stabilityai/stable-diffusion-xl-refiner-1.0/resolve/main/sd_xl_refiner_1.0.safetensors"
DEFAULT_SDXL_INPAINTING_MODEL = "https://huggingface.co/benjamin-paine/sd-xl-alternative-bases/resolve/main/sd_xl_base_1.0_inpainting_0.1.safetensors"

# Other Featured Open-Source Models
OPEN_DALLE_MODEL = "https://huggingface.co/dataautogpt3/OpenDalleV1.1/resolve/main/OpenDalleV1.1.safetensors"
PLAYGROUND_V2_MODEL = "https://huggingface.co/playgroundai/playground-v2-1024px-aesthetic/resolve/main/playground-v2.fp16.safetensors"
SEGMIND_VEGA_MODEL = "https://huggingface.co/segmind/Segmind-Vega/resolve/main/segmind-vega.safetensors"
SDXL_TURBO_MODEL = "https://huggingface.co/stabilityai/sdxl-turbo/resolve/main/sd_xl_turbo_1.0_fp16.safetensors"
ANIMAGINE_MODEL = "https://huggingface.co/cagliostrolab/animagine-xl-3.0/resolve/main/animagine-xl-3.0.safetensors"

DEFAULT_CHECKPOINT_DIR = os.path.expanduser("~/.cache/enfugue/checkpoint")
DEFAULT_INVERSION_DIR = os.path.expanduser("~/.cache/enfugue/inversion")
DEFAULT_TENSORRT_DIR = os.path.expanduser("~/.cache/enfugue/tensorrt")
DEFAULT_LORA_DIR = os.path.expanduser("~/.cache/enfugue/lora")
DEFAULT_LYCORIS_DIR = os.path.expanduser("~/.cache/enfugue/lycoris")
DEFAULT_CACHE_DIR = os.path.expanduser("~/.cache/enfugue/cache")
DEFAULT_DIFFUSERS_DIR = os.path.expanduser("~/.cache/enfugue/diffusers")
DEFAULT_OTHER_DIR = os.path.expanduser("~/.cache/enfugue/other")

DEFAULT_SIZE = 512
DEFAULT_TILING_SIZE = 512
DEFAULT_TILING_STRIDE = 32
DEFAULT_TILING_MASK = "bilinear"
DEFAULT_TEMPORAL_SIZE = 16
DEFAULT_TEMPORAL_TILING_SIZE = 12
DEFAULT_SDXL_SIZE = 1024
DEFAULT_IMAGE_CALLBACK_STEPS = 10
DEFAULT_CONDITIONING_SCALE = 1.0
DEFAULT_IMG2IMG_STRENGTH = 0.8
DEFAULT_INFERENCE_STEPS = 40
DEFAULT_GUIDANCE_SCALE = 7.5
DEFAULT_UPSCALE_PROMPT = "highly detailed, ultra-detailed, intricate detail, high definition, HD, 4k, 8k UHD"
DEFAULT_UPSCALE_INFERENCE_STEPS = 100
DEFAULT_UPSCALE_GUIDANCE_SCALE = 12
DEFAULT_UPSCALE_TILING_STRIDE = 128
DEFAULT_UPSCALE_TILING_SIZE = DEFAULT_TILING_SIZE

DEFAULT_REFINER_START = 0.85
DEFAULT_REFINER_STRENGTH = 0.3
DEFAULT_REFINER_GUIDANCE_SCALE = 5.0
DEFAULT_AESTHETIC_SCORE = 6.0
DEFAULT_NEGATIVE_AESTHETIC_SCORE = 2.5

MODEL_PROMPT_WEIGHT = 0.5
GLOBAL_PROMPT_UPSCALE_WEIGHT = 0.8
MAX_IMAGE_SCALE = 3.0

CACHE_MODE_LITERAL = ["always", "xl", "tensorrt"]
VAE_LITERAL = Literal["ema", "mse", "xl", "xl16", "consistency"]
DEVICE_LITERAL = Literal["cpu", "cuda", "dml", "mps"]
PIPELINE_SWITCH_MODE_LITERAL = Literal["offload", "unload"]
SCHEDULER_LITERAL = Literal[
    "ddim", "ddpm", "deis",
    "dpmsm", "dpmsms", "dpmsmk", "dpmsmka",
    "dpmss", "dpmssk", "heun",
    "dpmd", "dpmdk", "adpmd",
    "adpmdk", "dpmsde", "unipc",
    "lmsd", "lmsdk", "pndm",
    "eds", "edsk", "eads", "lcm"
]
UPSCALE_LITERAL = Literal[
    "esrgan", "esrganime", "gfpgan",
    "lanczos", "bilinear", "bicubic",
    "nearest"
]
CONTROLNET_LITERAL = Literal[
    "canny", "mlsd", "hed",
    "scribble", "tile", "inpaint",
    "depth", "normal", "pose",
    "pidi", "line", "anime",
    "temporal", "qr", "sparse-rgb",
    "sparse-scribble"
]
MOTION_LORA_LITERAL = [
    "pan-left", "pan-right",
    "roll-clockwise", "roll-anti-clockwise",
    "tilt-up", "tilt-down",
    "zoom-in", "zoom-out"
]
LOOP_TYPE_LITERAL = Literal[
    "loop", "reflect"
]
MASK_TYPE_LITERAL = Literal[
    "constant", "bilinear", "gaussian"
]
LATENT_BLEND_METHOD_LITERAL = Literal[
    "add", "bislerp", "cosine", "cubic",
    "difference", "inject", "lerp", "slerp",
    "exclusion", "subtract", "multiply", "overlay",
    "screen", "color_dodge", "linear_dodge", "glow",
    "pin_light", "hard_light", "linear_light", "vivid_light"
]
NOISE_METHOD_LITERAL = Literal[
    "default", "crosshatch", "simplex",
    "perlin", "brownian_fractal", "white",
    "grey", "pink", "blue", "green",
    "velvet", "violet", "random_mix"
]
IP_ADAPTER_LITERAL = Literal[
    "default", "plus", "plus-face", "full-face"
]
ANIMATION_ENGINE_LITERAL = Literal[
    "ad_hsxl", "svd"
]
OPTICAL_FLOW_METHOD_LITERAL = Literal[
    "lucas-kanade", "dense-lucas-kanade", "farneback", "rlof", "unimatch"
]

# VAE repos/files
VAE_EMA = "https://huggingface.co/stabilityai/sd-vae-ft-ema/resolve/main/diffusion_pytorch_model.safetensors?filename=sd-vae-ft-ema.safetensors"
VAE_MSE = "https://huggingface.co/stabilityai/sd-vae-ft-mse/resolve/main/diffusion_pytorch_model.safetensors?filename=sd-vae-ft-mse.safetensors"
VAE_XL = "https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors"
VAE_XL16 = "https://huggingface.co/madebyollin/sdxl-vae-fp16-fix/resolve/main/diffusion_pytorch_model.safetensors?filename=sdxl-vae-fp16-fix.safetensors"
VAE_CONSISTENCY = "https://huggingface.co/openai/consistency-decoder/resolve/main/diffusion_pytorch_model.safetensors?filename=consistency-decoder-vae.safetensors"
VAE_PREVIEW = "https://huggingface.co/madebyollin/taesd/resolve/main/diffusion_pytorch_model.safetensors?filename=taesd.safetensors"
VAE_PREVIEW_XL = "https://huggingface.co/madebyollin/taesdxl/resolve/main/diffusion_pytorch_model.safetensors?filename=taesdxl.safetensors"

# ControlNet repos/files
CONTROLNET_CANNY = "https://huggingface.co/lllyasviel/control_v11p_sd15_canny/resolve/main/diffusion_pytorch_model.safetensors?filename=control_v11p_sd15_canny.safetensors"
CONTROLNET_MLSD = "https://huggingface.co/lllyasviel/control_v11p_sd15_mlsd/resolve/main/diffusion_pytorch_model.safetensors?filename=control_v11p_sd15_mlsd.safetensors"
CONTROLNET_HED = "https://huggingface.co/lllyasviel/sd-controlnet-hed/resolve/main/diffusion_pytorch_model.safetensors?filename=sd-controlnet-hed.safetensors"
CONTROLNET_SCRIBBLE = "https://huggingface.co/lllyasviel/control_v11p_sd15_scribble/resolve/main/diffusion_pytorch_model.safetensors?filename=control_v11p_sd15_scribble.safetensors"
CONTROLNET_TILE = "https://huggingface.co/lllyasviel/control_v11f1e_sd15_tile/resolve/main/diffusion_pytorch_model.bin?filename=control_v11f1e_sd15_tile.bin"
CONTROLNET_INPAINT = "https://huggingface.co/lllyasviel/control_v11p_sd15_inpaint/resolve/main/diffusion_pytorch_model.safetensors?filename=control_v11p_sd15_inpaint.safetensors"
CONTROLNET_DEPTH = "https://huggingface.co/lllyasviel/control_v11f1p_sd15_depth/resolve/main/diffusion_pytorch_model.safetensors?filename=control_v11f1p_sd15_depth.safetensors"
CONTROLNET_NORMAL = "https://huggingface.co/lllyasviel/control_v11p_sd15_normalbae/resolve/main/diffusion_pytorch_model.safetensors?filename=control_v11p_sd15_normalbae.safetensors"
CONTROLNET_POSE = "https://huggingface.co/lllyasviel/control_v11p_sd15_openpose/resolve/main/diffusion_pytorch_model.safetensors?filename=control_v11p_sd15_openpose.safetensors"
CONTROLNET_PIDI = "https://huggingface.co/lllyasviel/control_v11p_sd15_softedge/resolve/main/diffusion_pytorch_model.safetensors?filename=control_v11p_sd15_softedge.safetensors"
CONTROLNET_LINE = "https://huggingface.co/lllyasviel/control_v11p_sd15_lineart/resolve/main/diffusion_pytorch_model.safetensors?filename=control_v11p_sd15_lineart.safetensors"
CONTROLNET_ANIME = "https://huggingface.co/lllyasviel/control_v11p_sd15s2_lineart_anime/resolve/main/diffusion_pytorch_model.safetensors?filename=control_v11p_sd15s2_lineart_anime.safetensors"

CONTROLNET_TEMPORAL = "https://huggingface.co/CiaraRowles/TemporalNet/resolve/main/diffusion_pytorch_model.safetensors?filename=temporalnet.safetensors"
CONTROLNET_QR = "https://huggingface.co/monster-labs/control_v1p_sd15_qrcode_monster/resolve/main/v2/control_v1p_sd15_qrcode_monster_v2.safetensors"

CONTROLNET_PIDI_XL = "https://huggingface.co/SargeZT/controlnet-sd-xl-1.0-softedge-dexined/resolve/main/controlnet-sd-xl-1.0-softedge-dexined.safetensors"
CONTROLNET_QR_XL = "https://huggingface.co/monster-labs/control_v1p_sdxl_qrcode_monster/resolve/main/diffusion_pytorch_model.safetensors?filename=control_v1p_sdxl_qrcode_monster.safetensors"

CONTROLNET_CANNY_XL = "https://huggingface.co/diffusers/controlnet-canny-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors?filename=controlnet-canny-sdxl-1.0.safetensors"
CONTROLNET_DEPTH_XL = "https://huggingface.co/diffusers/controlnet-depth-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors?filename=controlnet-depth-sdxl-1.0.safetensors"
CONTROLNET_POSE_XL = "https://huggingface.co/thibaud/controlnet-openpose-sdxl-1.0/resolve/main/OpenPoseXL2.safetensors"

CONTROLNET_SPARSE_RGB = "https://huggingface.co/guoyww/animatediff/resolve/main/v3_sd15_sparsectrl_rgb.ckpt"
CONTROLNET_SPARSE_SCRIBBLE = "https://huggingface.co/guoyww/animatediff/resolve/main/v3_sd15_sparsectrl_scribble.ckpt"

MOTION_LORA_PAN_LEFT = "https://huggingface.co/guoyww/animatediff/resolve/main/v2_lora_PanLeft.ckpt"
MOTION_LORA_PAN_RIGHT = "https://huggingface.co/guoyww/animatediff/resolve/main/v2_lora_PanRight.ckpt"
MOTION_LORA_ROLL_CLOCKWISE = "https://huggingface.co/guoyww/animatediff/resolve/main/v2_lora_RollingClockwise.ckpt"
MOTION_LORA_ROLL_ANTI_CLOCKWISE = "https://huggingface.co/guoyww/animatediff/resolve/main/v2_lora_RollingAnticlockwise.ckpt"
MOTION_LORA_TILT_UP = "https://huggingface.co/guoyww/animatediff/resolve/main/v2_lora_TiltUp.ckpt"
MOTION_LORA_TILT_DOWN = "https://huggingface.co/guoyww/animatediff/resolve/main/v2_lora_TiltDown.ckpt"
MOTION_LORA_ZOOM_IN = "https://huggingface.co/guoyww/animatediff/resolve/main/v2_lora_ZoomIn.ckpt"
MOTION_LORA_ZOOM_OUT = "https://huggingface.co/guoyww/animatediff/resolve/main/v2_lora_ZoomOut.ckpt"

LCM_LORA_VEGA = "https://huggingface.co/segmind/Segmind-VegaRT/resolve/main/pytorch_lora_weights.safetensors?filename=lcm-lora-segmind-vega-rt.safetensors"
LCM_LORA_DEFAULT = "https://huggingface.co/latent-consistency/lcm-lora-sdv1-5/resolve/main/pytorch_lora_weights.safetensors?filename=lcm-lora-sdv1-5.safetensors"
LCM_LORA_XL = "https://huggingface.co/latent-consistency/lcm-lora-sdxl/resolve/main/pytorch_lora_weights.safetensors?filename=lcm-lora-sdxl.safetensors"
SPARSE_CONTROLNET_ADAPTER_LORA = "https://huggingface.co/guoyww/animatediff/resolve/main/v3_sd15_adapter.ckpt"

DPO_LORA = "https://huggingface.co/benjamin-paine/sd-dpo-offsets/resolve/main/sd_v15_dpo_lora_v1.safetensors"
DPO_LORA_XL = "https://huggingface.co/benjamin-paine/sd-dpo-offsets/resolve/main/sd_xl_dpo_lora_v1.safetensors"
DPO_OFFSET = "https://huggingface.co/benjamin-paine/sd-dpo-offsets/resolve/main/sd_v15_unet_dpo_offset_v1.safetensors"
DPO_OFFSET_XL = "https://huggingface.co/benjamin-paine/sd-dpo-offsets/resolve/main/sd_xl_unet_dpo_offset_v1.safetensors"

OFFSET_LORA_XL = "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_offset_example-lora_1.0.safetensors"

MultiModelType = Union[str, List[str]]
WeightedMultiModelType = Union[
    str, Tuple[str, float],
    List[Union[str, Tuple[str, float]]]
]

class ImageDict(TypedDict):
    """
    An image or video with optional fitting details
    """
    image: Union[str, Image, List[Image]]
    skip_frames: NotRequired[Optional[int]]
    divide_frames: NotRequired[Optional[int]]
    start_frame: NotRequired[Optional[int]]
    end_frame: NotRequired[Optional[int]]
    fit: NotRequired[Optional[IMAGE_FIT_LITERAL]]
    anchor: NotRequired[Optional[IMAGE_ANCHOR_LITERAL]]
    invert: NotRequired[bool]
    low_frequency: NotRequired[int]
    high_frequency: NotRequired[int]
    audio_channel: NotRequired[int]

class ControlImageDict(ImageDict):
    """
    Extends the image dict additionally with controlnet details
    """
    controlnet: CONTROLNET_LITERAL
    scale: NotRequired[float]
    start: NotRequired[Optional[float]]
    end: NotRequired[Optional[float]]
    process: NotRequired[bool]

class IPAdapterImageDict(ImageDict):
    """
    Extends the image dict additionally with IP adapter scale
    """
    scale: NotRequired[float]

class UpscaleStepDict(TypedDict):
    """
    All the options for each upscale step
    """
    method: UPSCALE_LITERAL
    amount: Union[int, float]
    strength: NotRequired[float]
    num_inference_steps: NotRequired[int]
    scheduler: NotRequired[SCHEDULER_LITERAL]
    guidance_scale: NotRequired[float]
    controlnet: NotRequired[Optional[CONTROLNET_LITERAL]]
    controlnet_scale: NotRequired[float]
    prompt: NotRequired[str]
    prompt_2: NotRequired[str]
    negative_prompt: NotRequired[str]
    negative_prompt_2: NotRequired[str]
    tiling_stride: NotRequired[Optional[int]]
    tiling_mask: NotRequired[MASK_TYPE_LITERAL]
    frame_window_size: NotRequired[Optional[int]]
    frame_window_stride: NotRequired[Optional[int]]

class PromptDict(TypedDict):
    """
    A prompt step, optionally with frame details
    """
    positive: str
    negative: NotRequired[Optional[str]]
    positive_2: NotRequired[Optional[str]]
    negative_2: NotRequired[Optional[str]]
    weight: NotRequired[Optional[float]]
    start: NotRequired[Optional[int]]
    end: NotRequired[Optional[int]]
    low_frequency: NotRequired[int]
    high_frequency: NotRequired[int]
    audio_channel: NotRequired[int]

class MotionVectorPointDict(TypedDict):
    """
    A point along a motion vector
    """
    anchor: Tuple[int, int]
    control_1: NotRequired[Tuple[int, int]]
    control_2: NotRequired[Tuple[int, int]]
