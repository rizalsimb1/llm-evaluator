"""Provider factory."""
from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider


def get_provider(name: str, **kwargs):
    providers = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
    }
    if name not in providers:
        raise ValueError(f"Unknown provider: {name}. Choose from: {list(providers.keys())}")
    return providers[name](**kwargs)
