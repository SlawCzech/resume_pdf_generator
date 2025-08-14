import datetime as dt
from pydantic import BaseModel, Field, ConfigDict

from .experience import Experience
from .education import Education
from .skill import Skill
from .project import Project
from .social_link import SocialLink
from .certificate import Certificate
from .language import Language


class ResumePayload(BaseModel):
    user_id: int | None = None
    fullname: str
    professional_title: str | None = None
    summary: str | None = None
    location: str
    phone: str
    image_url: str | None = None

    experiences: list[Experience] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    skills: list[Skill] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    social_links: list[SocialLink] = Field(default_factory=list)
    certificates: list[Certificate] = Field(default_factory=list)
    languages: list[Language] = Field(default_factory=list)

    created_at: dt.datetime
    updated_at: dt.datetime | None = None

    model_config = ConfigDict(extra="ignore")
