"""Anthropic Claude provider implementation."""
from typing import Generator, Optional
import os
try:
    import anthropic
except ImportError:
    anthropic = None
from ..models import CompletionResponse


class AnthropicProvider:
    DEFAULT_MODEL = "claude-3-5-sonnet-20241022"

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model or self.DEFAULT_MODEL
        if anthropic:
            self.client = anthropic.Anthropic(api_key=self.api_key)

    def complete(self, prompt: str, **kwargs) -> CompletionResponse:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        )
        return CompletionResponse(
            text=response.content[0].text,
            model=self.model,
            provider="anthropic",
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
        )

    def stream(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        with self.client.messages.stream(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            for text in stream.text_stream:
                yield text

    def estimate_cost(self, prompt: str) -> dict:
        input_tokens = len(prompt) // 4
        return {
            "model": self.model,
            "estimated_input_tokens": input_tokens,
            "estimated_cost_usd": input_tokens * 0.000003,
        }
