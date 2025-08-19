import os
from reportlab import rl_config
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def _fonts_root() -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    default_path = os.path.join(base_dir, "static", "fonts")
    return os.environ.get("APP_FONTS_DIR", default_path)


FONTS = {
    "Merriweather": {
        "normal": "Merriweather/Merriweather-Regular.ttf",
        "bold": "Merriweather/Merriweather-Bold.ttf",
        "italic": "Merriweather/Merriweather-Italic.ttf",
        "boldItalic": "Merriweather/Merriweather-BoldItalic.ttf",
    },
    "Roboto": {
        "normal": "Roboto/Roboto-Regular.ttf",
        "bold": "Roboto/Roboto-Bold.ttf",
        "italic": "Roboto/Roboto-Italic.ttf",
        "boldItalic": "Roboto/Roboto-BoldItalic.ttf",
    },
    "SourceSans": {
        "normal": "SourceSans/SourceSans3-Regular.ttf",
        "bold": "SourceSans/SourceSans3-Bold.ttf",
        "italic": "SourceSans/SourceSans3-It.ttf",
        "boldItalic": "SourceSans/SourceSans3-BoldIt.ttf",
    },
}


def _font_name(family: str, style: str) -> str:
    suffix = {
        "normal": "",
        "bold": "-Bold",
        "italic": "-Italic",
        "boldItalic": "-BoldItalic",
    }[style]
    return f"{family}{suffix}" if suffix else family


def register_fonts() -> None:
    root = _fonts_root()

    if root not in rl_config.TTFSearchPath:
        rl_config.TTFSearchPath.insert(0, root)

    registered = set(pdfmetrics.getRegisteredFontNames())

    for family, styles in FONTS.items():
        names = {}
        for style, rel_path in styles.items():
            name = _font_name(family, style)
            if name in registered:
                names[style] = name
                continue
            try:
                pdfmetrics.registerFont(TTFont(name, rel_path))
                registered.add(name)
                names[style] = name
            except Exception as e:
                pass

        pdfmetrics.registerFontFamily(
            family,
            normal=names.get("normal"),
            bold=names.get("bold"),
            italic=names.get("italic"),
            boldItalic=names.get("boldItalic"),
        )
