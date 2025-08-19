from pydantic import BaseModel, ConfigDict


class JobPosting(BaseModel):
    description: str
    requirements: str
    responsibilities: str
    tech_tags: list[str]

    model_config = ConfigDict(extra="ignore")
