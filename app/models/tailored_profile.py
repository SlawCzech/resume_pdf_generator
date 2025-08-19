from pydantic import BaseModel, Field, ConfigDict

from .experience import Experience
from .education import Education
from .language import Language
from .skill import Skill
from .project import Project
from .certificate import Certificate
from .social_link import SocialLink


class TailoredExperienceEducation(BaseModel):
    experience: list[Experience] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)

    model_config = ConfigDict(extra="ignore")


class TailoredSkillProjectCertificate(BaseModel):
    skills: list[Skill] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    certificates: list[Certificate] = Field(default_factory=list)

    model_config = ConfigDict(extra="ignore")


class TailoredSummary(BaseModel):
    summary: str


class TailoredProfile(
    TailoredExperienceEducation, TailoredSkillProjectCertificate, TailoredSummary
):
    fullname: str
    professional_title: str | None = None
    location: str
    phone: str
    image_url: str | None = None
    social_links: list[SocialLink] | None = None
    languages: list[Language]
