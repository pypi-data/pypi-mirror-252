from collections import defaultdict

from ..pipeline import SDPipeline, IPAdapterPipeline, enhance_factory
from .scheme import PipelineResource, UpscalerResource, Scheme, ResourceCacheNotLoaded, ResourceCacheNotFound


class ResourceCache:
    pipelines = defaultdict(PipelineResource)
    upscalers = defaultdict(UpscalerResource)

    @classmethod
    def get_pipeline(cls, scheme: Scheme):
        name = cls._pipeline_name(scheme)
        if name not in cls.pipelines:
            raise ResourceCacheNotFound(name)
        r = cls.pipelines.get(name)
        if r.pipeline is None:
            raise ResourceCacheNotLoaded
        return r.pipeline

    @classmethod
    def get_upscaler(cls, scheme: Scheme):
        name = cls._upscaler_name(scheme)
        if name not in cls.upscalers:
            raise ResourceCacheNotFound(name)
        r = cls.upscalers.get(name)
        if r.enhance_method is None:
            raise ResourceCacheNotLoaded
        return r.enhance_method

    @classmethod
    def add_schemes(cls, *schemes):
        for scheme in schemes:
            cls._add_pipeline(scheme)
            cls._add_upscaler(scheme)

    @classmethod
    def load(cls):
        cls._load_pipeline()
        cls._load_upscaler()

    @staticmethod
    def _pipeline_name(scheme: Scheme) -> tuple:
        return scheme.base_model, scheme.vae, scheme.clip_skip, scheme.adapt_model

    @staticmethod
    def _upscaler_name(scheme: Scheme) -> tuple:
        return scheme.upscaler_method, scheme.restorer_method

    @classmethod
    def _add_pipeline(cls, scheme: Scheme):
        uniq_id = cls._pipeline_name(scheme)
        for lora, weight in scheme.lora_specs:
            if weight > 0:
                cls.pipelines[uniq_id].loras.add(lora)
        for embedding in scheme.embedding_specs:
            cls.pipelines[uniq_id].embeddings.add(embedding)

    @classmethod
    def _add_upscaler(cls, scheme: Scheme):
        uniq_id = cls._upscaler_name(scheme)
        _ = cls.upscalers[uniq_id]

    @classmethod
    def _load_pipeline(cls):
        for name, r in cls.pipelines.items():
            print(name, r)
            base_model, vae, clip_skip, adapt_model = name

            if adapt_model == "None":
                p = SDPipeline(memory_efficient=True)
                p.init(base_model, vae, clip_skip,
                       lora_adapters=list(r.loras),
                       embedding_adapters=list(r.embeddings))
                r.pipe = p
            else:
                p = IPAdapterPipeline(memory_efficient=True)
                p.init(base_model, vae, clip_skip,
                       adapt_model=adapt_model,
                       lora_adapters=list(r.loras),
                       embedding_adapters=list(r.embeddings))
                r.pipe = p

    @classmethod
    def _load_upscaler(cls):
        for name, r in cls.upscalers.items():
            upscaler_method, restorer_method = name
            enhance_method, enhance_type = enhance_factory(
                {"method": upscaler_method, "model_id": upscaler_method},
                {"method": restorer_method, "model_id": restorer_method},
            )
            r.enhance_method, r.enhance_type = enhance_method, enhance_type


def load(*schemes):
    ResourceCache.add_schemes(schemes)
    ResourceCache.load()
