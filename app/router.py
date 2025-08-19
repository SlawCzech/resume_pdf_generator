import io
import json
from enum import Enum
from io import BytesIO
from pathlib import Path
from typing import Annotated
from fastapi import APIRouter, Body, HTTPException, Query, Depends
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI

from app.ai.dependencies import get_openai_client
from app.core.profile_builder import build_profile
from app.models import ResumePayload
from app.models.job_posting import JobPosting
from app.core.pdf_generator import generate_pdf_bytes

router = APIRouter(prefix="", tags=["Resume PDF Generator"])


class Level(str, Enum):
    senior = "senior"
    mid = "mid"
    junior = "junior"


class Style(str, Enum):
    simple = "simple"
    vibrant = "vibrant"
    elegant = "elegant"


@router.get(
    "/example-resume",
    response_class=StreamingResponse,
    summary="Render example resume PDF",
)
async def generate_example_resume(
    style: Annotated[Style, Query(description="Choose style")] = Style.simple,
    level: Annotated[Level, Query(description="Choose level")] = Level.junior,
) -> StreamingResponse:
    package_dir = Path(__file__).resolve().parent
    fixtures_dir = package_dir / "fixtures"
    json_path = fixtures_dir / f"resume_{level.value}.json"

    if not json_path.exists():
        raise HTTPException(status_code=500, detail=f"Fixture not found: {json_path}")

    try:
        with json_path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to load fixture JSON")

    payload = ResumePayload(**raw)

    pdf_bytes = generate_pdf_bytes(
        data=payload,
        template_key=style,
    )

    buffer = BytesIO(pdf_bytes)
    headers = {
        "Content-Disposition": f'attachment; filename="resume_{level.value}_{style.value}.pdf"',
        "Content-Length": str(len(pdf_bytes)),
    }
    return StreamingResponse(buffer, media_type="application/pdf", headers=headers)


@router.post(
    "/tailored_profile",
    response_class=StreamingResponse,
    summary="Generate ai-tailored resume",
)
async def render_resume(
    ai_client: Annotated[AsyncOpenAI, Depends(get_openai_client)],
    job: Annotated[JobPosting, Body()],
    resume: Annotated[ResumePayload, Body()],
    style: Annotated[Style | None, Query(description="Choose style")] = Style.simple,
    filename: Annotated[
        str | None, Query(description="Optional output filename")
    ] = None,
) -> StreamingResponse:
    data = await build_profile(job=job, resume=resume, ai_client=ai_client)

    try:
        pdf_bytes = generate_pdf_bytes(data=data, template_key=style)
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Failed to render PDF. Reason: {err}") from err

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename or "_".join(resume.fullname.split() + ["resume"])}.pdf"',
            "Cache-Control": "no-store",
        },
    )
