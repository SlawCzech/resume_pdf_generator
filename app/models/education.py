import datetime as dt
from pydantic import BaseModel, ConfigDict


class Education(BaseModel):
    degree: str | None = None
    school: str
    field_of_study: str | None = None
    location: str | None = None
    start_date: dt.date
    end_date: dt.date | None = None
    description: str | None = None

    model_config = ConfigDict(extra="ignore")
