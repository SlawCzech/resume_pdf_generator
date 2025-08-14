import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def _project_fonts_root() -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "static", "fonts")


def _style_from_filename(filename_lower: str) -> str | None:
    is_bold = "bold" in filename_lower
    is_italic = "italic" in filename_lower or "ital" in filename_lower
    is_regular = "regular" in filename_lower or "normal" in filename_lower

    if is_bold and is_italic:
        return "boldItalic"
    if is_bold:
        return "bold"
    if is_italic:
        return "italic"
    if is_regular:
        return "normal"
    return None


def _register_family_in_dir(dir_path: str, family_name: str) -> None:
    registered = set(pdfmetrics.getRegisteredFontNames())
    if family_name in registered:
        return

    if not os.path.isdir(dir_path):
        return

    style_files: dict[str, str] = {}
    ttf_files = [f for f in os.listdir(dir_path) if f.lower().endswith(".ttf")]
    for fname in ttf_files:
        style = _style_from_filename(fname.lower())
        if style is None:
            style = "__unknown__:" + fname
        style_files[style] = os.path.join(dir_path, fname)

    if "normal" not in style_files:
        unknowns = [k for k in style_files.keys() if k.startswith("__unknown__:")]
        if unknowns:
            first_unknown = unknowns[0]
            style_files["normal"] = style_files[first_unknown]

    if "normal" not in style_files:
        return

    names = {
        "normal": family_name,
        "bold": f"{family_name}-Bold",
        "italic": f"{family_name}-Italic",
        "boldItalic": f"{family_name}-BoldItalic",
    }

    for style_key, font_name in names.items():
        path = style_files.get(style_key)
        if path and font_name not in registered:
            pdfmetrics.registerFont(TTFont(font_name, path))
            registered.add(font_name)

    aliases = {
        "normal": family_name.lower(),
        "bold": f"{family_name.lower()}-bold",
        "italic": f"{family_name.lower()}-italic",
        "boldItalic": f"{family_name.lower()}-bolditalic",
    }

    for style_key, alias_name in aliases.items():
        path = style_files.get(style_key)
        if path and alias_name not in registered:
            pdfmetrics.registerFont(TTFont(alias_name, path))
            registered.add(alias_name)

    pdfmetrics.registerFontFamily(
        family_name,
        normal=names["normal"] if names["normal"] in registered else None,
        bold=names["bold"] if names["bold"] in registered else None,
        italic=names["italic"] if names["italic"] in registered else None,
        boldItalic=names["boldItalic"] if names["boldItalic"] in registered else None,
    )


def _find_subdir_case_insensitive(root: str, name: str) -> str | None:
    wanted = name.lower()
    try:
        for entry in os.listdir(root):
            if os.path.isdir(os.path.join(root, entry)) and entry.lower() == wanted:
                return entry
    except FileNotFoundError:
        return None
    return None


def register_fonts() -> None:
    root = _project_fonts_root()
    families = ["Merriweather", "Nata", "Roboto", "SourceSans"]
    for family in families:
        subdir = _find_subdir_case_insensitive(root, family)
        if not subdir:
            continue
        family_dir = os.path.join(root, subdir)
        _register_family_in_dir(family_dir, family)