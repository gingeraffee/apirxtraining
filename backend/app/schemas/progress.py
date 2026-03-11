from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ProgressRecord(BaseModel):
    employee_id: str
    display_name: str | None = None
    current_section: str | None = None
    completed_sections: list[str] = Field(default_factory=list)
    acknowledged_sections: list[str] = Field(default_factory=list)
    quiz_passed_sections: list[str] = Field(default_factory=list)
    started_at: datetime | None = None
    updated_at: datetime | None = None
    core_total_sections: int = 0
    core_completion_ratio: float = 0.0


class ProgressUpdate(BaseModel):
    display_name: str | None = None
    current_section: str | None = None
    completed_sections: list[str] = Field(default_factory=list)
    acknowledged_sections: list[str] = Field(default_factory=list)
    quiz_passed_sections: list[str] = Field(default_factory=list)


class AcknowledgmentUpdate(BaseModel):
    section_slug: str
    display_name: str | None = None


class QuizSubmissionUpdate(BaseModel):
    section_slug: str
    answers: list[int] = Field(default_factory=list)
    display_name: str | None = None


class QuizSubmissionResult(BaseModel):
    section_slug: str
    passed: bool
    correct_count: int
    total_questions: int
    score: float
    passing_percent: float
    progress: ProgressRecord
