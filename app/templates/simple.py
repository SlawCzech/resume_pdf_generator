from reportlab.platypus import (
    Paragraph, Spacer, HRFlowable, Frame, PageTemplate
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors

from app.templates.helpers.date_helpers import fmt_range, fmt_mmyyyy


class SimpleTemplate:
    key = "simple"
    label = "Simple"

    PAGE_W, PAGE_H = A4
    ML, MR, MT, MB = 18 * mm, 18 * mm, 20 * mm, 18 * mm
    GAP_Y = 6

    def __init__(self):
        base = getSampleStyleSheet()

        self.colors = {
            "ink": colors.HexColor("#111827"),
            "muted": colors.HexColor("#6B7280"),
            "accent": colors.HexColor("#374151"),
            "rule": colors.HexColor("#E5E7EB"),
        }
        self.h_name = ParagraphStyle(
            "h_name", parent=base["Heading1"],
            fontName="Roboto-Bold", fontSize=22, leading=24,
            textColor=self.colors["ink"], spaceAfter=2
        )
        self.h_title = ParagraphStyle(
            "h_title", parent=base["BodyText"],
            fontName="SourceSans", fontSize=10.5, leading=14,
            textColor=self.colors["muted"], spaceAfter=8
        )
        self.h_meta = ParagraphStyle(
            "h_meta", parent=base["BodyText"],
            fontName="SourceSans", fontSize=9.2, leading=12,
            textColor=self.colors["muted"], spaceAfter=8
        )
        self.body = ParagraphStyle(
            "body", parent=base["BodyText"],
            fontName="SourceSans", fontSize=10, leading=14,
            textColor=self.colors["ink"]
        )
        self.meta = ParagraphStyle(
            "meta", parent=self.body,
            fontName="SourceSans", fontSize=9.2, leading=12,
            textColor=self.colors["muted"]
        )
        self.h_sec = ParagraphStyle(
            "h_sec",
            parent=base["Heading2"],
            fontName="Roboto-Bold",
            fontSize=10.5,
            leading=14,
            textColor=self.colors["accent"],
            spaceBefore=10,
            spaceAfter=4,
            leftIndent=4 * mm,
            backColor=colors.HexColor("#F9FAFB"),
        )

    def _rule(self, thickness=0.6, space_before=2, space_after=6):
        return HRFlowable(width="100%", color=self.colors["rule"],
                          thickness=thickness, spaceBefore=space_before, spaceAfter=space_after)

    def _section_title(self, text: str) -> list:
        from reportlab.platypus import Table, TableStyle

        cell = Paragraph(text.upper(), self.h_sec)
        table = Table([[cell]], colWidths=[None])
        table.setStyle(
            TableStyle(
                [
                    (
                        "LINEBEFORE",
                        (0, 0),
                        (0, 0),
                        1.5,
                        self.colors["accent"],
                    ),
                    ("LEFTPADDING", (0, 0), (-1, -1), 3),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 2),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F9FAFB")),
                ]
            )
        )
        return [table]

    def _header(self, data) -> list:
        s: list = []
        fullname = getattr(data, "fullname", None)
        s.append(Paragraph(fullname or "RESUME", self.h_name))
        if getattr(data, "professional_title", None):
            s.append(Paragraph(data.professional_title, self.h_title))
        meta_bits = [getattr(data, "location", None), getattr(data, "phone", None)]
        meta_line = " · ".join([b for b in meta_bits if b])
        if meta_line:
            s.append(Paragraph(meta_line, self.h_meta))
        s.append(HRFlowable(width="100%", color=self.colors["ink"], thickness=0.7, spaceBefore=2, spaceAfter=8))
        return s

    def _profile(self, data) -> list:
        s: list = []
        s += self._section_title("Profile")
        s.append(Paragraph(getattr(data, "summary", ""), self.body))
        s.append(Spacer(1, self.GAP_Y))
        return s

    def _experience(self, data) -> list:
        s: list = []
        s += self._section_title("Experience")
        for exp in getattr(data, "experiences", []):
            left = f"{exp.company}" + (f", {exp.location}" if exp.location else "")
            s.append(Paragraph(f"{left} — <b>{exp.job_title}</b>", self.body))
            rng = fmt_range(exp.start_date, exp.end_date)
            if rng:
                s.append(Paragraph(rng.upper(), self.meta))
            if exp.description:
                s.append(Paragraph(exp.description, self.body))
            if exp.challenge:
                s.append(Paragraph(f"<i>Challenge:</i> {exp.challenge}", self.meta))
            s.append(Spacer(1, self.GAP_Y))
        return s

    def _education(self, data) -> list:
        s: list = []
        s += self._section_title("Education")
        for ed in getattr(data, "education", []):
            left = f"{ed.school}" + (f", {ed.location}" if ed.location else "")
            title = f"{left} — <b>{ed.degree}</b>" if ed.degree else left
            s.append(Paragraph(title, self.body))
            rng = fmt_range(ed.start_date, ed.end_date)
            if rng:
                s.append(Paragraph(rng.upper(), self.meta))
            if ed.field_of_study:
                s.append(Paragraph(ed.field_of_study, self.meta))
            if ed.description:
                s.append(Paragraph(ed.description, self.body))
            s.append(Spacer(1, self.GAP_Y))
        return s

    def _projects(self, data) -> list:
        s: list = []
        s += self._section_title("Projects")
        for p in getattr(data, "projects", []):
            title = p.name or "Project"
            if getattr(p, "link", None):
                title = f"<link href='{p.link}'><font color='#6B7280'>{title}</font></link>"
            s.append(Paragraph(title, self.body))
            if getattr(p, "tech_stack", None):
                s.append(Paragraph(", ".join(p.tech_stack), self.meta))
            if getattr(p, "description", None):
                s.append(Paragraph(p.description, self.body))
            s.append(Spacer(1, self.GAP_Y))
        return s

    def _skills(self, data) -> list:
        s: list = []
        s += self._section_title("Skills")
        skills = ", ".join([f"{x.name}{f' ({x.level})' if getattr(x, 'level', None) else ''}" for x in getattr(data, "skills", [])])
        s.append(Paragraph(skills, self.body))
        s.append(Spacer(1, self.GAP_Y))
        return s

    def _certificates(self, data) -> list:
        s: list = []
        s += self._section_title("Certificates")
        LINK_COLOR = "#6B7280"
        for c in getattr(data, "certificates", []):
            name = c.name or ""
            issuer = c.issuer or ""
            date_txt = fmt_mmyyyy(c.date_issued) if getattr(c, "date_issued", None) else ""
            if issuer and getattr(c, "link", None):
                issuer_html = f"<link href='{c.link}'><font color='{LINK_COLOR}'>{issuer}</font></link>"
            else:
                issuer_html = issuer
            bits = [x for x in [name, issuer_html, date_txt] if x]
            s.append(Paragraph(" — ".join(bits), self.body))
            s.append(Spacer(1, self.GAP_Y - 2))
        return s

    def _languages(self, data) -> list:
        s: list = []
        s += self._section_title("Languages")
        langs = ", ".join([f"{l.name}{f' ({l.level})' if getattr(l, 'level', None) else ''}" for l in getattr(data, "languages", [])])
        s.append(Paragraph(langs, self.body))
        s.append(Spacer(1, self.GAP_Y))
        return s

    def _social(self, data) -> list:
        s: list = []
        s += self._section_title("Social")
        for sl in getattr(data, "social_links", []):
            label = sl.platform or "Profile"
            if getattr(sl, "url", None):
                label = f"<link href='{sl.url}'><font color='#6B7280'>{label}</font></link>"
            text = label
            if getattr(sl, "description", None):
                text += f" — {sl.description}"
            s.append(Paragraph(text, self.body))
        s.append(Spacer(1, self.GAP_Y))
        return s

    def build_story(self, data) -> list:
        story: list = []
        story += self._header(data)

        if getattr(data, "summary", None):         story += self._profile(data)
        if getattr(data, "experiences", None):     story += self._experience(data)
        if getattr(data, "education", None):       story += self._education(data)
        if getattr(data, "projects", None):        story += self._projects(data)
        if getattr(data, "skills", None):          story += self._skills(data)
        if getattr(data, "certificates", None):    story += self._certificates(data)
        if getattr(data, "languages", None):       story += self._languages(data)
        if getattr(data, "social_links", None):    story += self._social(data)

        return story

    def get_page_templates(self):
        full = Frame(
            self.ML,
            self.MB,
            self.PAGE_W - self.ML - self.MR,
            self.PAGE_H - self.MT - self.MB,
            id="full",
            showBoundary=0,
        )
        return [PageTemplate(id="Simple", frames=[full])]
    