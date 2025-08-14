from pydantic import BaseModel, ConfigDict

class Language(BaseModel):
    name: str
    level: str | None = None

    model_config = ConfigDict(extra="ignore")
