"""Main LLM client with provider abstraction."""
from __future__ import annotations
import time
import random
from typing import Generator, Optional
from .providers import get_provider
from .cache import ResponseCache
from .models import CompletionResponse


class LLMClient:
    """Unified LLM client supporting multiple providers."""

    def __init__(
        self,
        provider: str = "openai",
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        cache: bool = False,
        max_retries: int = 3,
        timeout: int = 60,
    ):
        self.provider_name = provider
        self.model = model
        self.max_retries = max_retries
        self.timeout = timeout
        self._provider = get_provider(provider, api_key=api_key, model=model)
        self._cache = ResponseCache() if cache else None

    def complete(self, prompt: str, **kwargs) -> CompletionResponse:
        """Send a completion request with automatic retry."""
        cache_key = f"{self.provider_name}:{self.model}:{prompt}"
        if self._cache and (cached := self._cache.get(cache_key)):
            return cached

        for attempt in range(self.max_retries):
            try:
                response = self._provider.complete(prompt, **kwargs)
                if self._cache:
                    self._cache.set(cache_key, response)
                return response
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                wait = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait)

    def stream(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        """Stream completion tokens as they arrive."""
        yield from self._provider.stream(prompt, **kwargs)

    def estimate_cost(self, prompt: str) -> dict:
        """Estimate token count and cost for a prompt."""
        return self._provider.estimate_cost(prompt)
