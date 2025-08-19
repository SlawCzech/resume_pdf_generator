import datetime as dt
from pydantic import BaseModel, ConfigDict


class Certificate(BaseModel):
    issuer: str
    name: str
    date_issued: dt.date
    description: str | None = None
    link: str | None = None

    model_config = ConfigDict(extra="ignore")
