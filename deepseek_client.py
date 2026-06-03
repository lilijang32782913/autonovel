from __future__ import annotations

import os

import httpx


def _api_key() -> str:
    return os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("ANTHROPIC_API_KEY", "")


def _base_url() -> str:
    base_url = os.environ.get("AUTONOVEL_API_BASE_URL", "https://api.deepseek.com").rstrip("/")
    if base_url.endswith("/v1"):
        base_url = base_url[:-3]
    return base_url


def chat_completion(*, model: str, prompt: str, system: str | None = None, max_tokens: int = 4000,
                    temperature: float = 0.7, timeout: int = 300) -> str:
    api_key = _api_key()
    if not api_key:
        raise RuntimeError("DeepSeek API key is not set. Define DEEPSEEK_API_KEY in .env.")

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    resp = httpx.post(
        f"{_base_url()}/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=timeout,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]