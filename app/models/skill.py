from pydantic import BaseModel, ConfigDict

class Skill(BaseModel):
    name: str
    level: str | None = None

    model_config = ConfigDict(extra="ignore")