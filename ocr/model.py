from dataclasses import dataclass


@dataclass
class OCRTaskStatus:
    task_id: str
    status: str

@dataclass
class OCRResult:
    pages: list[str]