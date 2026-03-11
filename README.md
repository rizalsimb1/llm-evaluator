# llm-evaluator

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Stars](https://img.shields.io/github/stars/rizalsimb1/llm-evaluator?style=social)
![Issues](https://img.shields.io/github/issues/rizalsimb1/llm-evaluator)

> A production-ready Python SDK for interacting with multiple LLM providers (OpenAI, Anthropic, Gemini) with built-in caching, retry logic, and streaming support.

## ✨ Features

- ✅ Unified interface for OpenAI, Anthropic Claude, and Google Gemini
- ✅ Automatic retry with exponential backoff on rate limits
- ✅ Response caching with Redis or in-memory store
- ✅ Streaming response support out of the box
- ✅ Token counting and cost estimation per request
- ✅ Async-first design with asyncio support
- ✅ Structured output with Pydantic validation

## 🛠️ Tech Stack

`Python 3.11+` • `OpenAI SDK` • `Anthropic SDK` • `Redis` • `Pydantic` • `asyncio`

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/rizalsimb1/llm-evaluator.git
cd llm-evaluator

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Quick Start

```python
from llm_wrapper import LLMClient

client = LLMClient(provider="openai", model="gpt-4o")

# Simple completion
response = client.complete("Explain transformers in simple terms")
print(response.text)

# Streaming
for chunk in client.stream("Write a poem about AI"):
    print(chunk, end="", flush=True)

# With caching
client_cached = LLMClient(provider="anthropic", model="claude-3-5-sonnet", cache=True)
response = client_cached.complete("What is RAG?")  # cached on repeat calls

```

## 📁 Project Structure

```
llm-evaluator/
├── src/
│   └── main files
├── tests/
│   └── test files
├── requirements.txt
├── README.md
└── LICENSE
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<p align="center">Made with ❤️ by <a href="https://github.com/rizalsimb1">rizalsimb1</a></p>

