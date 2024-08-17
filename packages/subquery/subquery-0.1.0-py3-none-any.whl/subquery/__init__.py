from .core import SubqueryResult, SubqueryGenerator


def TransformersSubqueryGenerator():
    from .transformers_model import TransformersSubqueryGenerator as TSG
    return TSG()


def OllamaSubqueryGenerator():
    from .ollama_model import OllamaSubqueryGenerator as OSG
    return OSG()


__all__ = ['SubqueryResult', 'SubqueryGenerator', 'TransformersSubqueryGenerator', 'OllamaSubqueryGenerator']