from .base import ResumeTemplate
from .elegant import ElegantTemplate
from .simple import SimpleTemplate
from .vibrant import VibrantTemplate

TEMPLATES: dict[str, ResumeTemplate] = {
    SimpleTemplate.key: SimpleTemplate(),
    VibrantTemplate.key: VibrantTemplate(),
    ElegantTemplate.key: ElegantTemplate(),
}