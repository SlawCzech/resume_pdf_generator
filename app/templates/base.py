from typing import Protocol, Any


class ResumeTemplate(Protocol):
    key: str
    label: str

    def build_story(self, data: Any) -> list: ...
