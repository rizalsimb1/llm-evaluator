"""Tests for the LLM client."""
import pytest
from unittest.mock import MagicMock, patch
from src.client import LLMClient
from src.models import CompletionResponse


def make_mock_response(text="Test response"):
    return CompletionResponse(
        text=text, model="gpt-4o-mini",
        provider="openai", input_tokens=10, output_tokens=20
    )


def test_client_init():
    with patch("src.providers.openai_provider.OpenAI"):
        client = LLMClient(provider="openai")
        assert client.provider_name == "openai"


def test_cache_stores_response():
    with patch("src.providers.openai_provider.OpenAI"):
        client = LLMClient(provider="openai", cache=True)
        client._provider.complete = MagicMock(return_value=make_mock_response())
        client.complete("Hello")
        client.complete("Hello")
        # Should only call provider once (second is cached)
        assert client._provider.complete.call_count == 1


def test_max_retries_on_failure():
    with patch("src.providers.openai_provider.OpenAI"):
        client = LLMClient(provider="openai", max_retries=2)
        client._provider.complete = MagicMock(side_effect=Exception("API Error"))
        with pytest.raises(Exception):
            client.complete("Hello")
        assert client._provider.complete.call_count == 2
