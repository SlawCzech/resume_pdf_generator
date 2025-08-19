from openai import AsyncOpenAI

from app.ai.config import MODEL
from app.ai.prompts.system import (
    SYSTEM_PROMPT_EXP_EDU,
    SYSTEM_PROMPT_SKILL_PROJ_CERT,
    SYSTEM_SUMMARY,
)
from app.ai.prompts.guidelines import (
    GUIDELINES_SUMMARY,
    GUIDELINES_SKL_PROJ_CERT,
    GUIDELINES_EXP_EDU,
)
from app.models import ResumePayload
from app.models.job_posting import JobPosting
from app.models.tailored_profile import (
    TailoredExperienceEducation,
    TailoredSkillProjectCertificate,
    TailoredSummary,
)


def build_message(
    job: JobPosting, resume: ResumePayload, system: str, instructions: str
) -> list[dict]:
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": instructions},
        {
            "role": "user",
            "content": "JOB_POSTING:\n"
            + job.model_dump_json(indent=2, exclude_none=True),
        },
        {
            "role": "user",
            "content": "USER_PROFILE:\n"
            + resume.model_dump_json(indent=2, exclude_none=True),
        },
    ]


async def generate_tailored_exp_edu(
    job: JobPosting, resume: ResumePayload, ai_client: AsyncOpenAI
):
    messages = build_message(
        job=job,
        resume=resume,
        system=SYSTEM_PROMPT_EXP_EDU,
        instructions=GUIDELINES_EXP_EDU,
    )
    response = await ai_client.responses.parse(
        model=MODEL,
        input=messages,
        text_format=TailoredExperienceEducation,
    )
    return response.output_parsed


async def generate_tailored_skill_proj_cert(
    job: JobPosting, resume: ResumePayload, ai_client: AsyncOpenAI
):
    messages = build_message(
        job=job,
        resume=resume,
        system=SYSTEM_PROMPT_SKILL_PROJ_CERT,
        instructions=GUIDELINES_SKL_PROJ_CERT,
    )
    response = await ai_client.responses.parse(
        model=MODEL,
        input=messages,
        text_format=TailoredSkillProjectCertificate,
    )
    return response.output_parsed


async def generate_tailored_summary(
    job: JobPosting, resume: ResumePayload, ai_client: AsyncOpenAI
):
    messages = build_message(
        job=job, resume=resume, system=SYSTEM_SUMMARY, instructions=GUIDELINES_SUMMARY
    )
    response = await ai_client.responses.parse(
        model=MODEL, input=messages, text_format=TailoredSummary
    )
    return response.output_parsed
