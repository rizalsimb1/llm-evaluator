"""OpenAI provider implementation."""
from typing import Generator, Optional
import os
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None
from ..models import CompletionResponse


class OpenAIProvider:
    DEFAULT_MODEL = "gpt-4o-mini"

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or self.DEFAULT_MODEL
        if OpenAI:
            self.client = OpenAI(api_key=self.api_key)

    def complete(self, prompt: str, **kwargs) -> CompletionResponse:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        )
        return CompletionResponse(
            text=response.choices[0].message.content,
            model=self.model,
            provider="openai",
            input_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens,
        )

    def stream(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            **kwargs,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    def estimate_cost(self, prompt: str) -> dict:
        # Rough estimate: 1 token ≈ 4 chars
        input_tokens = len(prompt) // 4
        return {
            "model": self.model,
            "estimated_input_tokens": input_tokens,
            "estimated_cost_usd": input_tokens * 0.00000015,
        }
