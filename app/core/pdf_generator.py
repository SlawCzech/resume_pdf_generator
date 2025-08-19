from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, BaseDocTemplate
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

from app.models import ResumePayload
from app.models.tailored_profile import TailoredProfile
from app.templates import TEMPLATES
from app.fonts import register_fonts

register_fonts()


class TemplateNotFound(ValueError):
    pass


def list_templates() -> list[str]:
    return list(TEMPLATES.keys())


def generate_pdf_bytes(
    data: TailoredProfile | ResumePayload,
    template_key: str = "simple",
    pagesize=A4,
    margins: tuple[float, float, float, float] = (14 * mm, 16 * mm, 14 * mm, 14 * mm),
) -> bytes:
    if template_key not in TEMPLATES:
        raise TemplateNotFound(
            f"Unknown template '{template_key}'. Available: {list_templates()}"
        )

    tpl = TEMPLATES[template_key]
    story = tpl.build_story(data)

    buf = BytesIO()

    has_custom_pages = hasattr(tpl, "get_page_templates") and callable(
        getattr(tpl, "get_page_templates")
    )

    if has_custom_pages:
        doc = BaseDocTemplate(
            buf,
            pagesize=pagesize,
            leftMargin=0,
            rightMargin=0,
            topMargin=0,
            bottomMargin=0,
            title=getattr(data, "fullname", None) or "Resume",
            author=getattr(data, "fullname", None),
        )
        for pt in tpl.get_page_templates():
            doc.addPageTemplates(pt)
        doc.build(story)
    else:
        left, top, right, bottom = margins
        doc = SimpleDocTemplate(
            buf,
            pagesize=pagesize,
            leftMargin=left,
            rightMargin=right,
            topMargin=top,
            bottomMargin=bottom,
            title=getattr(data, "fullname", None) or "Resume",
            author=getattr(data, "fullname", None),
        )
        doc.build(story)

    buf.seek(0)
    return buf.read()
