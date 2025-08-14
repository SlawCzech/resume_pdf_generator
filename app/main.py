from fastapi import FastAPI
from reportlab.pdfbase import pdfmetrics

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)