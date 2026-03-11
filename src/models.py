"""Pydantic models for request/response types."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class CompletionResponse:
    text: str
    model: str
    provider: str
    input_tokens: int = 0
    output_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    def __repr__(self) -> str:
        return f"CompletionResponse(provider={self.provider!r}, model={self.model!r}, tokens={self.total_tokens})"
