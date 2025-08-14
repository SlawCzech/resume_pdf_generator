from reportlab.platypus import (
    Paragraph, Spacer, HRFlowable, Frame, PageTemplate, NextPageTemplate,
    Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors

from app.templates.helpers.date_helpers import fmt_range, fmt_mmyyyy


class VibrantTemplate:
    key = "vibrant"
    label = "Vibrant"

    PAGE_W, PAGE_H = A4
    ML, MR, MT, MB = 16 * mm, 16 * mm, 20 * mm, 16 * mm
    GAP = 6 * mm
    HEADER_H = 28 * mm

    LEFT_W = 58 * mm

    def __init__(self):
        base = getSampleStyleSheet()
        self.colors = {
            "ink": colors.HexColor("#111827"),
            "muted": colors.HexColor("#6B7280"),
            "accent": colors.HexColor("#CC5500"),
            "rule_strong": colors.HexColor("#CC5500"),
            "rule_soft": colors.HexColor("#C98453"),
        }

        # header
        self.h_name = ParagraphStyle(
            "h_name", parent=base["Heading1"],
            fontName="SourceSans-Bold", fontSize=22, leading=24,
            textColor=self.colors["ink"], spaceAfter=2
        )
        self.h_title = ParagraphStyle(
            "h_title", parent=base["BodyText"],
            fontName="SourceSans", fontSize=10.5, leading=14,
            textColor=self.colors["muted"], spaceAfter=6
        )
        self.meta = ParagraphStyle(
            "meta", parent=base["BodyText"],
            fontName="SourceSans", fontSize=9, leading=12,
            textColor=self.colors["muted"]
        )
        self.body = ParagraphStyle(
            "body", parent=base["BodyText"],
            fontName="SourceSans", fontSize=9.8, leading=13.2,
            textColor=self.colors["ink"]
        )
        self.h_left = ParagraphStyle(
            "h_left", parent=base["Heading2"],
            fontName="SourceSans-Bold", fontSize=10.5, leading=14,
            textColor=self.colors["accent"], spaceBefore=0, spaceAfter=0
        )

        self.SECTION_ORDER = [
            ("Profile",      self._profile,      "summary"),
            ("Experience",   self._experience,   "experiences"),
            ("Education",    self._education,    "education"),
            ("Projects",     self._projects,     "projects"),
            ("Skills",       self._skills,       "skills"),
            ("Certificates", self._certificates, "certificates"),
            ("Languages",    self._languages,    "languages"),
            ("Social",       self._social,       "social_links"),
        ]

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
        s.append(HRFlowable(width="100%", color=self.colors["rule_strong"], thickness=0.8,
                            spaceBefore=4, spaceAfter=8))
        return s

    def _clean_items(self, items):
        out = []
        for it in items:
            if isinstance(it, Spacer):
                if not out or isinstance(out[-1], Spacer):
                    continue
            out.append(it)
        if out and isinstance(out[-1], Spacer):
            out.pop()
        return out

    def _profile(self, data):
        return [Paragraph(data.summary, self.body)]

    def _experience(self, data):
        rows = []
        for exp in getattr(data, "experiences", []):
            left = f"{exp.company}" + (f", {exp.location}" if exp.location else "")
            rows.append(Paragraph(f"{left} — <b>{exp.job_title}</b>", self.body))
            rng = fmt_range(exp.start_date, exp.end_date)
            if rng:
                rows.append(Paragraph(rng.upper(), self.meta))
            if exp.description:
                rows.append(Paragraph(exp.description, self.body))
            if exp.challenge:
                rows.append(Paragraph(f"<i>Challenge:</i> {exp.challenge}", self.meta))
        return self._clean_items(rows)

    def _education(self, data):
        rows = []
        for ed in getattr(data, "education", []):
            left = f"{ed.school}" + (f", {ed.location}" if ed.location else "")
            title = f"{left} — <b>{ed.degree}</b>" if ed.degree else left
            rows.append(Paragraph(title, self.body))
            rng = fmt_range(ed.start_date, ed.end_date)
            if rng:
                rows.append(Paragraph(rng.upper(), self.meta))
            if ed.field_of_study:
                rows.append(Paragraph(ed.field_of_study, self.meta))
            if ed.description:
                rows.append(Paragraph(ed.description, self.body))
        return self._clean_items(rows)

    def _projects(self, data):
        rows = []
        for p in getattr(data, "projects", []):
            name = p.name or "Project"
            if getattr(p, "link", None):
                name_html = f"<link href='{p.link}'><font color='#6B7280'>{name}</font></link>"
            else:
                name_html = name
            rows.append(Paragraph(name_html, self.body))
            if getattr(p, "tech_stack", None):
                rows.append(Paragraph(", ".join(p.tech_stack), self.meta))
            if getattr(p, "description", None):
                rows.append(Paragraph(p.description, self.body))
        return self._clean_items(rows)

    def _skills(self, data):
        return [Paragraph(
            ", ".join([f"{x.name}{f' ({x.level})' if getattr(x, 'level', None) else ''}" for x in data.skills]),
            self.body
        )]

    def _certificates(self, data):
        rows = []
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
            rows.append(Paragraph(" — ".join(bits), self.body))
        return self._clean_items(rows)

    def _languages(self, data):
        return [Paragraph(
            ", ".join([f"{l.name}{f' ({l.level})' if getattr(l, 'level', None) else ''}" for l in data.languages]),
            self.body
        )]

    def _social(self, data):
        rows = []
        for sl in getattr(data, "social_links", []):
            label = sl.platform or "Profile"
            if getattr(sl, "url", None):
                txt = f"<link href='{sl.url}'><font color='#6B7280'>{label}</font></link>"
            else:
                txt = label
            if getattr(sl, "description", None):
                txt += f" — {sl.description}"
            rows.append(Paragraph(txt, self.body))
        return self._clean_items(rows)

    def _rows(self, data):
        rows = []

        def add_sec(label: str, right_items: list):
            if not right_items:
                return
            rows.append([Paragraph(label.upper(), self.h_left), right_items[0]])

            for item in right_items[1:]:
                rows.append(["", item])

            sep = HRFlowable(width="100%", color=self.colors["rule_soft"],
                             thickness=0.5, spaceBefore=0, spaceAfter=6)
            rows.append(["", sep])

        for label, builder, attr in self.SECTION_ORDER:
            if getattr(data, attr, None):
                add_sec(label, builder(data))

        return rows

    def build_story(self, data) -> list:
        story: list = []
        story += self._header_story(data)
        story.append(NextPageTemplate('Next'))

        table = Table(
            self._rows(data),
            colWidths=[self.LEFT_W, (self.PAGE_W - self.ML - self.MR) - self.LEFT_W],
            hAlign="LEFT",
            splitByRow=1,
            spaceBefore=0,
            spaceAfter=0,
        )
        table.setStyle(TableStyle([
            ("LEFTPADDING",  (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING",   (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
            ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ]))

        story.append(table)
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
        content_frame = Frame(
            self.ML,
            self.MB,
            self.PAGE_W - self.ML - self.MR,
            self.PAGE_H - self.MT - self.MB - self.HEADER_H,
            id="content",
            showBoundary=0,
        )
        full_content_frame = Frame(
            self.ML,
            self.MB,
            self.PAGE_W - self.ML - self.MR,
            self.PAGE_H - self.MT - self.MB,
            id="full_content",
            showBoundary=0,
        )

        first = PageTemplate(id="First", frames=[header_frame, content_frame])
        next_ = PageTemplate(id="Next", frames=[full_content_frame])
        return [first, next_]