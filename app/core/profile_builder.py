import asyncio

from openai import AsyncOpenAI

from app.ai.messaging import (
    generate_tailored_exp_edu,
    generate_tailored_skill_proj_cert,
    generate_tailored_summary,
)
from app.models import ResumePayload
from app.models.job_posting import JobPosting
from app.models.tailored_profile import TailoredProfile


async def build_profile(job: JobPosting, resume: ResumePayload, ai_client: AsyncOpenAI) -> TailoredProfile:
    part_one = asyncio.create_task(
        generate_tailored_exp_edu(job=job, resume=resume, ai_client=ai_client)
    )
    part_two = asyncio.create_task(
        generate_tailored_skill_proj_cert(job=job, resume=resume, ai_client=ai_client)
    )
    summary = asyncio.create_task(
        generate_tailored_summary(job=job, resume=resume, ai_client=ai_client)
    )
    a, b, c = await asyncio.gather(part_one, part_two, summary)

    return TailoredProfile(
        fullname=resume.fullname,
        professional_title=resume.professional_title,
        location=resume.location,
        phone=resume.phone,
        summary=c.summary,
        experience=a.experience,
        education=a.education,
        skills=b.skills,
        projects=b.projects,
        certificates=b.certificates,
        social_links=resume.social_links,
        languages=resume.languages,
    )