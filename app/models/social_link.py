from pydantic import BaseModel, Field, HttpUrl, ConfigDict, field_validator

class SocialLink(BaseModel):
    url: str
    platform: str
    description: str = ""

    model_config = ConfigDict(extra="ignore")
