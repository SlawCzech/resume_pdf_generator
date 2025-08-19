from pathlib import Path

from pydantic import Field, AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

MODEL = "gpt-5-mini"


class OpenAISettings(BaseSettings):
    openai_api_key: str = Field(..., validation_alias="OPENAI_API_KEY")
    openai_base_url: AnyUrl = Field(default="https://api.openai.com/v1")

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).with_name(".env")),
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
