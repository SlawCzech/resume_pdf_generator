import io
import os
import json
from enum import Enum
from io import BytesIO
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Query, Response
from fastapi.responses import StreamingResponse

from app.models import ResumePayload
from app.pdf_generator import generate_pdf_bytes

router = APIRouter(prefix="/pdf-generator", tags=["Resume PDF Generator"])

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
    responses={
        200: {
            "content": {
                "application/pdf": {
                    "schema": {"type": "string", "format": "binary"}
                }
            },
            "description": "Generated resume as PDF",
        }
    },
    summary="Render example resume PDF"
)
async def generate_example_resume(
        style: Annotated[Style, Query(description="Choose style")] = Style.simple,
        level: Annotated[Level, Query(description="Choose level")] = Level.junior
) -> Response:

    package_dir = Path(__file__).resolve().parent
    fixtures_dir = package_dir / "fixtures"
    json_path = fixtures_dir / f"resume_{level.value}.json"

    if not json_path.exists():
        raise HTTPException(
            status_code=500,
            detail=f"Fixture not found: {json_path}"
        )

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


@router.post("/resume", response_class=StreamingResponse, summary="Render resume PDF")
def render_resume(
    payload: Annotated[ResumePayload, Body(embed=False)],
    style: Annotated[Style | None, Query(description="Choose style")] = Style.simple,
    filename: Annotated[str | None, Query(description="Optional output filename")] = None,
) -> Response:

    try:
        pdf_bytes = generate_pdf_bytes(data=payload, template_key=style)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to render PDF")

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename or "_".join(payload.fullname.split() + ['resume'])}.pdf"',
            "Cache-Control": "no-store",
        },
    )
