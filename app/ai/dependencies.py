from functools import cache

from openai import AsyncOpenAI

from app.ai.config import OpenAISettings


@cache
def get_openai_settings() -> OpenAISettings:
    return OpenAISettings()


@cache
def get_openai_client() -> AsyncOpenAI:
    cfg = get_openai_settings()
    return AsyncOpenAI(
        api_key=cfg.openai_api_key,
        base_url=str(cfg.openai_base_url) if cfg.openai_base_url else None,
    )
