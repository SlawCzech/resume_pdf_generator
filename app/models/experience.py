import datetime as dt
from pydantic import BaseModel, ConfigDict


class Experience(BaseModel):
    job_title: str
    company: str
    location: str | None = None
    start_date: dt.date
    end_date: dt.date | None = None
    description: str
    challenge: str | None = None

    model_config = ConfigDict(extra="ignore")
