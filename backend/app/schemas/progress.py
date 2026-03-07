from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ProgressRecord(BaseModel):
    employee_id: str
    display_name: str | None = None
    current_section: str | None = None
    completed_sections: list[str] = Field(default_factory=list)
    acknowledged_sections: list[str] = Field(default_factory=list)
    toolkit_completed: bool = False
    started_at: datetime | None = None
    updated_at: datetime | None = None
    core_total_sections: int = 0
    core_completion_ratio: float = 0.0


class ProgressUpdate(BaseModel):
    display_name: str | None = None
    current_section: str | None = None
    completed_sections: list[str] = Field(default_factory=list)
    acknowledged_sections: list[str] = Field(default_factory=list)
    toolkit_completed: bool = False


class AcknowledgmentUpdate(BaseModel):
    section_slug: str
    display_name: str | None = None
