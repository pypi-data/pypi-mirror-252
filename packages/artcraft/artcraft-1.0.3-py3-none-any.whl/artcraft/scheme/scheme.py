from dataclasses import dataclass, field
from typing import Callable

from ..pipeline import SDPipeline, IPAdapterPipeline


@dataclass
class Scheme:
    name: str
    tags: list[str]

    # model
    network_type: str
    base_model: str
    vae: str = "Auto"
    clip_skip: int = 0
    adapt_model: str = "None"
    lora_specs: list[tuple[str, float]] = field(default_factory=list)
    embedding_specs: list[str] = field(default_factory=list)
    # restore
    upscaler_method: str = "None"
    restorer_method: str = "None"
    enhance_scale: float = 1.6
    enhance_strength: float = 0.15
    # run args
    prompt_template: str = ""
    neg_prompt_template: str = ""
    cfg: float = 7.0
    scheduler: str = "Auto"
    sampling_steps: int = 35
    # adapt
    adapt_scale = 0.5


@dataclass
class PipelineResource:
    loras: set[str] = field(default_factory=set)
    embeddings: set[str] = field(default_factory=set)
    pipeline: SDPipeline | IPAdapterPipeline = None


@dataclass
class UpscalerResource:
    enhance_method: Callable = None
    enhance_type: str = " pil"


class ResourceCacheNotFound(Exception):
    def __init__(self, message):
        self.message = message


class ResourceCacheNotLoaded(Exception):
    def __init__(self):
        super(ResourceCacheNotLoaded, self).__init__()
