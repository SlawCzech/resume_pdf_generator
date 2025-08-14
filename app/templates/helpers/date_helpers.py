import datetime as dt

MONTHS = [
    "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE",
    "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"
]

def fmt_mmyyyy(d: dt.date | None) -> str | None:
    if not d:
        return None
    return f"{MONTHS[d.month - 1]} {d.year}"

def fmt_range(start: dt.date | None, end: dt.date | None) -> str | None:
    if not start and not end:
        return None
    left = fmt_mmyyyy(start) or ""
    right = fmt_mmyyyy(end) if end else "PRESENT"
    return f"{left} – {right}".strip(" –")