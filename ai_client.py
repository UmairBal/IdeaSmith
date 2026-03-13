"""
ai_client.py — Provider-agnostic AI completion client.
Supports: Anthropic, OpenAI, Google Gemini, Mistral, Groq, Cohere.
All providers normalised to a single call: complete(messages, system) -> str
"""

from __future__ import annotations
import json

# ── Provider registry ────────────────────────────────────────────────────────

PROVIDERS = {
    "anthropic": {
        "label": "Anthropic",
        "models": [
            "claude-opus-4-5-20251101",
            "claude-sonnet-4-5-20251101",
            "claude-haiku-4-5-20251001",
            "claude-opus-4-20250514",
            "claude-sonnet-4-20250514",
        ],
        "key_hint": "sk-ant-...",
        "docs": "https://docs.anthropic.com",
    },
    "openai": {
        "label": "OpenAI",
        "models": [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
            "gpt-4",
            "gpt-3.5-turbo",
            "o1",
            "o1-mini",
            "o3-mini",
        ],
        "key_hint": "sk-...",
        "docs": "https://platform.openai.com/docs",
    },
    "gemini": {
        "label": "Google Gemini",
        "models": [
            "gemini-2.0-flash",
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-1.0-pro",
        ],
        "key_hint": "AIza...",
        "docs": "https://ai.google.dev",
    },
    "mistral": {
        "label": "Mistral AI",
        "models": [
            "mistral-large-latest",
            "mistral-medium-latest",
            "mistral-small-latest",
            "codestral-latest",
        ],
        "key_hint": "...",
        "docs": "https://docs.mistral.ai",
    },
    "groq": {
        "label": "Groq",
        "models": [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
            "gemma2-9b-it",
        ],
        "key_hint": "gsk_...",
        "docs": "https://console.groq.com/docs",
    },
    "cohere": {
        "label": "Cohere",
        "models": [
            "command-r-plus",
            "command-r",
            "command",
            "command-light",
        ],
        "key_hint": "...",
        "docs": "https://docs.cohere.com",
    },
}


class AIClient:
    """Unified completion client."""

    def __init__(self, provider: str, api_key: str, model: str):
        self.provider = provider.lower()
        self.api_key = api_key
        self.model = model

        if self.provider not in PROVIDERS:
            raise ValueError(f"Unknown provider: {provider}. Choose from: {list(PROVIDERS.keys())}")

    # ── Public API ────────────────────────────────────────────────────────────

    def complete(self, user_prompt: str, system_prompt: str = "") -> str:
        """Run a completion and return the text response."""
        method = getattr(self, f"_complete_{self.provider}", None)
        if method is None:
            raise NotImplementedError(f"Provider {self.provider} not yet implemented.")
        return method(user_prompt, system_prompt)

    # ── Anthropic ─────────────────────────────────────────────────────────────

    def _complete_anthropic(self, user_prompt: str, system_prompt: str) -> str:
        import anthropic
        client = anthropic.Anthropic(api_key=self.api_key)
        kwargs = dict(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": user_prompt}],
        )
        if system_prompt:
            kwargs["system"] = system_prompt
        response = client.messages.create(**kwargs)
        return response.content[0].text.strip()

    # ── OpenAI ────────────────────────────────────────────────────────────────

    def _complete_openai(self, user_prompt: str, system_prompt: str) -> str:
        import openai
        client = openai.OpenAI(api_key=self.api_key)
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=2000,
        )
        return response.choices[0].message.content.strip()

    # ── Google Gemini ─────────────────────────────────────────────────────────

    def _complete_gemini(self, user_prompt: str, system_prompt: str) -> str:
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        full_prompt = f"{system_prompt}\n\n{user_prompt}" if system_prompt else user_prompt
        model = genai.GenerativeModel(self.model)
        response = model.generate_content(full_prompt)
        return response.text.strip()

    # ── Mistral ───────────────────────────────────────────────────────────────

    def _complete_mistral(self, user_prompt: str, system_prompt: str) -> str:
        from mistralai import Mistral
        client = Mistral(api_key=self.api_key)
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})
        response = client.chat.complete(model=self.model, messages=messages)
        return response.choices[0].message.content.strip()

    # ── Groq ──────────────────────────────────────────────────────────────────

    def _complete_groq(self, user_prompt: str, system_prompt: str) -> str:
        from groq import Groq
        client = Groq(api_key=self.api_key)
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})
        response = client.chat.completions.create(model=self.model, messages=messages, max_tokens=2000)
        return response.choices[0].message.content.strip()

    # ── Cohere ────────────────────────────────────────────────────────────────

    def _complete_cohere(self, user_prompt: str, system_prompt: str) -> str:
        import cohere
        client = cohere.Client(api_key=self.api_key)
        preamble = system_prompt or None
        response = client.chat(
            model=self.model,
            message=user_prompt,
            preamble=preamble,
        )
        return response.text.strip()
