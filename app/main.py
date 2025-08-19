from typing import Annotated

from fastapi import FastAPI, Depends
from openai import AsyncOpenAI

from app.ai.dependencies import get_openai_client
from app.fonts import register_fonts
from app.router import router

app = FastAPI(
    title="Resume PDF Generator",
    version="0.1.0",
)

register_fonts()

app.include_router(router)


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ai/ping")
async def ai_ping(ai_client: Annotated[AsyncOpenAI, Depends(get_openai_client)]):
    resp = await ai_client.responses.create(
        model="gpt-4.1-mini",
        input="This is health check. Reply with 'pong'",
    )
    reply = resp.output[0].content[0].text if resp.output else None
    return {"status": "ok", "reply": reply}
