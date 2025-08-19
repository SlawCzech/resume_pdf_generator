from pydantic import BaseModel, ConfigDict


class Project(BaseModel):
    name: str
    description: str | None = None
    link: str | None = None
    tech_stack: list[str] | None = None

    model_config = ConfigDict(extra="ignore")
