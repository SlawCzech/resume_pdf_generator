from reportlab.platypus import (
    Paragraph, Spacer, HRFlowable, Frame, PageTemplate, FrameBreak, NextPageTemplate
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors

from app.templates.helpers.date_helpers import fmt_mmyyyy, fmt_range


class ElegantTemplate:
    key = "elegant"
    label = "Elegant"

    PAGE_W, PAGE_H = A4
    ML, MR, MT, MB = 16 * mm, 16 * mm, 20 * mm, 16 * mm
    GAP = 6 * mm
    HEADER_H = 28 * mm
    LEFT_W = 58 * mm
    RIGHT_W = PAGE_W - ML - MR - LEFT_W - GAP
    BODY_H = PAGE_H - MT - MB - HEADER_H

    def __init__(self):
        base = getSampleStyleSheet()
        self.colors = {
            "ink": colors.HexColor("#111827"),
            "muted": colors.HexColor("#6B7280"),
            "rule": colors.HexColor("#111827"),
            "blue_accent": colors.HexColor("#0052be"),
        }
        self.h_name = ParagraphStyle(
            "h_name", parent=base["Heading1"],
            fontName="Merriweather", fontSize=24, leading=22,
            textColor=self.colors["ink"], spaceAfter=2
        )
        self.h_title = ParagraphStyle(
            "h_title", parent=base["BodyText"],
            fontName="Roboto", fontSize=10.5, leading=14,
            textColor=self.colors["muted"], spaceAfter=6
        )
        self.h_sec = ParagraphStyle(
            "h_sec", parent=base["Heading2"],
            fontName="Merriweather", fontSize=10.5, leading=14,
            textColor=self.colors["blue_accent"], spaceBefore=6, spaceAfter=4
        )
        self.body = ParagraphStyle(
            "body", parent=base["BodyText"],
            fontName="Roboto", fontSize=9.8, leading=13.2, textColor=self.colors["ink"]
        )
        self.meta = ParagraphStyle(
            "meta", parent=self.body,
            fontName="Roboto", fontSize=9, leading=12, textColor=self.colors["muted"]
        )

    def _rule(self, thickness=0.6):
        return HRFlowable(width="100%", color=self.colors["rule"], thickness=thickness, spaceBefore=2, spaceAfter=6)

    def _section_title(self, text: str) -> list:
        return [Paragraph(text.upper(), self.h_sec), self._rule(0.5)]

    def _header_story(self, data) -> list:
        s: list = []
        fullname = getattr(data, "fullname", None)
        s.append(Paragraph(fullname or "RESUME", self.h_name))
        if getattr(data, "professional_title", None):
            s.append(Paragraph(data.professional_title, self.h_title))
        meta_bits = [getattr(data, "location", None), getattr(data, "phone", None)]
        meta_line = " · ".join([b for b in meta_bits if b])
        if meta_line:
            s.append(Paragraph(meta_line, self.meta))
        s.append(self._rule(0.8))
        return s

    def _left_story(self, data) -> list:
        s: list = []
        if getattr(data, "skills", None):
            s += self._section_title("Skills")
            s.append(Paragraph(
                ", ".join([f"{x.name}{f' ({x.level})' if x.level else ''}" for x in data.skills]),
                self.body
            ))
            s.append(Spacer(1, 6))
        if getattr(data, "languages", None):
            s += self._section_title("Languages")
            s.append(Paragraph(
                ", ".join([f"{l.name}{f' ({l.level})' if l.level else ''}" for l in data.languages]),
                self.body
            ))
            s.append(Spacer(1, 6))
            if getattr(data, "certificates", None):
                s += self._section_title("Certificates")

                for c in data.certificates:
                    name = c.name or ""
                    issuer = c.issuer or ""
                    date_txt = (
                        fmt_mmyyyy(c.date_issued)
                        if getattr(c, "date_issued", None)
                        else ""
                    )

                    if issuer and getattr(c, "link", None):
                        issuer_link = f"<link href='{c.link}' color='darkblue'>{issuer}</link>"
                    else:
                        issuer_link = issuer

                    bits = [x for x in [name, issuer_link, date_txt] if x]
                    line = " — ".join(bits)

                    s.append(Paragraph(line, self.body))
            s.append(Spacer(1, 6))
        if getattr(data, "social_links", None):
            s += self._section_title("Social")
            for sl in data.social_links:
                text = sl.platform or "Profile"
                text = f"<link href='{sl.url}' color='darkblue'>{text}</link>"
                if sl.description: text += f" — {sl.description}"
                s.append(Paragraph(text, self.body))
            s.append(Spacer(1, 6))
        return s

    def _right_story(self, data) -> list:
        s: list = []
        if getattr(data, "summary", None):
            s += self._section_title("Profile")
            s.append(Paragraph(data.summary, self.body))
            s.append(Spacer(1, 8))
        if getattr(data, "experiences", None):
            s += self._section_title("Experience")
            for exp in data.experiences:
                left = f"{exp.company}" + (f", {exp.location}" if exp.location else "")
                s.append(Paragraph(f"{left} — <b>{exp.job_title}</b>", self.body))
                rng = fmt_range(exp.start_date, exp.end_date)
                if rng: s.append(Paragraph(rng.upper(), self.meta))
                if exp.description: s.append(Paragraph(exp.description, self.body))
                if exp.challenge: s.append(Paragraph(f"<i>Challenge:</i> {exp.challenge}", self.body))
                s.append(Spacer(1, 6))
        if getattr(data, "education", None):
            s += self._section_title("Education")
            for ed in data.education:
                left = f"{ed.school}" + (f", {ed.location}" if ed.location else "")
                title = f"{left} — <b>{ed.degree}</b>" if ed.degree else left
                s.append(Paragraph(title, self.body))
                rng = fmt_range(ed.start_date, ed.end_date)
                if rng: s.append(Paragraph(rng.upper(), self.meta))
                if ed.field_of_study: s.append(Paragraph(ed.field_of_study, self.meta))
                if ed.description: s.append(Paragraph(ed.description, self.body))
                s.append(Spacer(1, 6))
        if getattr(data, "projects", None):
            s += self._section_title("Projects")
            for p in data.projects:
                title = p.name
                if p.link: title = f"<link href='{p.link}' color='darkblue'>{p.name}</link>"
                s.append(Paragraph(title, self.body))
                if p.tech_stack: s.append(Paragraph(", ".join(p.tech_stack), self.meta))
                if p.description: s.append(Paragraph(p.description, self.body))
                s.append(Spacer(1, 6))
        return s

    def build_story(self, data) -> list:
        story: list = []

        story += self._header_story(data)

        story += self._left_story(data)
        story.append(FrameBreak())

        story.append(NextPageTemplate('RightOnly'))

        story += self._right_story(data)
        return story

    def get_page_templates(self):
        header_frame = Frame(
            self.ML,
            self.PAGE_H - self.MT - self.HEADER_H,
            self.PAGE_W - self.ML - self.MR,
            self.HEADER_H,
            id="header",
            showBoundary=0,
        )
        left_frame = Frame(
            self.ML,
            self.MB,
            self.LEFT_W,
            self.BODY_H,
            id="left",
            showBoundary=0,
        )
        right_frame = Frame(
            self.ML + self.LEFT_W + self.GAP,
            self.MB,
            self.RIGHT_W,
            self.BODY_H,
            id="right",
            showBoundary=0,
        )

        first = PageTemplate(id="TwoColFirst", frames=[header_frame, left_frame, right_frame])

        full_frame = Frame(self.ML, self.MB, self.PAGE_W - self.ML - self.MR, self.PAGE_H - self.MT - self.MB, id="full")
        right_only = PageTemplate(id="RightOnly", frames=[full_frame])

        return [first, right_only]