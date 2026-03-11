from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any

from app.schemas.progress import AcknowledgmentUpdate, ProgressRecord, ProgressUpdate, QuizSubmissionResult, QuizSubmissionUpdate
from app.services.content import get_all_page_slugs, get_section_by_slug, get_tracked_section_slugs


ROOT_DIR = Path(__file__).resolve().parents[3]
STORE_PATH = ROOT_DIR / "backend" / "app" / "data" / "progress_store.json"
TRACKED_SECTION_SLUGS = set(get_tracked_section_slugs())
ALL_PAGE_SLUGS = set(get_all_page_slugs())
CORE_SECTION_COUNT = len(TRACKED_SECTION_SLUGS)


class ProgressStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._lock = Lock()
        self._ensure_store()

    def _ensure_store(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text(json.dumps({"employees": {}}, indent=2), encoding="utf-8")

    def _read(self) -> dict[str, Any]:
        return json.loads(self.path.read_text(encoding="utf-8-sig"))

    def _write(self, payload: dict[str, Any]) -> None:
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def _normalize_sections(self, values: list[str] | None) -> list[str]:
        return sorted({slug for slug in values or [] if slug in TRACKED_SECTION_SLUGS})

    def _normalize_current(self, value: str | None) -> str | None:
        return value if value in ALL_PAGE_SLUGS else None

    def _quiz_passed_from_payload(self, payload: dict[str, Any]) -> list[str]:
        if "quiz_passed_sections" in payload:
            return self._normalize_sections(payload.get("quiz_passed_sections", []))
        # Preserve legacy completion progress by treating older completed sections
        # as already-passed quizzes during migration to gated quiz completion.
        return self._normalize_sections(payload.get("completed_sections", []))

    def _derive_completed(self, acknowledged_sections: list[str], quiz_passed_sections: list[str]) -> list[str]:
        return sorted(set(acknowledged_sections) & set(quiz_passed_sections))

    def _employee_payload(
        self,
        *,
        existing: dict[str, Any],
        display_name: str | None,
        current_section: str | None,
        acknowledged_sections: list[str],
        quiz_passed_sections: list[str],
        started_at: str,
        updated_at: str,
    ) -> dict[str, Any]:
        completed_sections = self._derive_completed(acknowledged_sections, quiz_passed_sections)
        return {
            "display_name": display_name or existing.get("display_name"),
            "current_section": current_section,
            "completed_sections": completed_sections,
            "acknowledged_sections": acknowledged_sections,
            "quiz_passed_sections": quiz_passed_sections,
            "started_at": started_at,
            "updated_at": updated_at,
        }

    def _decorate(self, employee_id: str, payload: dict[str, Any]) -> ProgressRecord:
        acknowledged = self._normalize_sections(payload.get("acknowledged_sections", []))
        quiz_passed = self._quiz_passed_from_payload(payload)
        completed = self._derive_completed(acknowledged, quiz_passed)
        ratio = round(len(completed) / CORE_SECTION_COUNT, 3) if CORE_SECTION_COUNT else 0.0
        return ProgressRecord(
            employee_id=employee_id,
            display_name=payload.get("display_name"),
            current_section=self._normalize_current(payload.get("current_section")),
            completed_sections=completed,
            acknowledged_sections=acknowledged,
            quiz_passed_sections=quiz_passed,
            started_at=payload.get("started_at"),
            updated_at=payload.get("updated_at"),
            core_total_sections=CORE_SECTION_COUNT,
            core_completion_ratio=ratio,
        )

    def get(self, employee_id: str) -> ProgressRecord:
        with self._lock:
            payload = self._read()
            employee = payload["employees"].get(employee_id)
            if not employee:
                return self._decorate(employee_id, {})
            return self._decorate(employee_id, employee)

    def save(self, employee_id: str, update: ProgressUpdate) -> ProgressRecord:
        with self._lock:
            payload = self._read()
            employees = payload["employees"]
            existing = employees.get(employee_id, {})
            now = datetime.now(timezone.utc).isoformat()
            started_at = existing.get("started_at") or now
            current_section = self._normalize_current(update.current_section) or self._normalize_current(existing.get("current_section"))
            acknowledged_sections = self._normalize_sections(update.acknowledged_sections or existing.get("acknowledged_sections", []))
            quiz_passed_sections = self._normalize_sections(update.quiz_passed_sections or self._quiz_passed_from_payload(existing))

            employees[employee_id] = self._employee_payload(
                existing=existing,
                display_name=update.display_name,
                current_section=current_section,
                acknowledged_sections=acknowledged_sections,
                quiz_passed_sections=quiz_passed_sections,
                started_at=started_at,
                updated_at=now,
            )
            self._write(payload)
            return self._decorate(employee_id, employees[employee_id])

    def acknowledge(self, employee_id: str, update: AcknowledgmentUpdate) -> ProgressRecord:
        with self._lock:
            payload = self._read()
            employees = payload["employees"]
            existing = employees.get(employee_id, {})
            now = datetime.now(timezone.utc).isoformat()
            started_at = existing.get("started_at") or now

            acknowledged = set(self._normalize_sections(existing.get("acknowledged_sections", [])))
            quiz_passed_sections = self._quiz_passed_from_payload(existing)
            if get_section_by_slug(update.section_slug):
                acknowledged.add(update.section_slug)

            employees[employee_id] = self._employee_payload(
                existing=existing,
                display_name=update.display_name,
                current_section=self._normalize_current(update.section_slug) or self._normalize_current(existing.get("current_section")),
                acknowledged_sections=sorted(acknowledged),
                quiz_passed_sections=quiz_passed_sections,
                started_at=started_at,
                updated_at=now,
            )
            self._write(payload)
            return self._decorate(employee_id, employees[employee_id])

    def submit_knowledge_check(self, employee_id: str, update: QuizSubmissionUpdate) -> QuizSubmissionResult:
        with self._lock:
            payload = self._read()
            employees = payload["employees"]
            existing = employees.get(employee_id, {})
            now = datetime.now(timezone.utc).isoformat()
            started_at = existing.get("started_at") or now

            section = get_section_by_slug(update.section_slug) or {}
            knowledge_check = section.get("knowledgeCheck") or {}
            questions = knowledge_check.get("questions", [])
            total_questions = len(questions)
            correct_count = sum(
                1
                for index, question in enumerate(questions)
                if index < len(update.answers) and update.answers[index] == question.get("correctOptionIndex")
            )
            score = round(correct_count / total_questions, 3) if total_questions else 0.0
            passing_percent = float(knowledge_check.get("passingPercent", 1.0))
            answered_everything = len(update.answers) == total_questions and total_questions > 0
            passed = answered_everything and score >= passing_percent

            quiz_passed = set(self._quiz_passed_from_payload(existing))
            if passed and get_section_by_slug(update.section_slug):
                quiz_passed.add(update.section_slug)

            employees[employee_id] = self._employee_payload(
                existing=existing,
                display_name=update.display_name,
                current_section=self._normalize_current(update.section_slug) or self._normalize_current(existing.get("current_section")),
                acknowledged_sections=self._normalize_sections(existing.get("acknowledged_sections", [])),
                quiz_passed_sections=sorted(quiz_passed),
                started_at=started_at,
                updated_at=now,
            )
            self._write(payload)
            progress = self._decorate(employee_id, employees[employee_id])
            return QuizSubmissionResult(
                section_slug=update.section_slug,
                passed=passed,
                correct_count=correct_count,
                total_questions=total_questions,
                score=score,
                passing_percent=passing_percent,
                progress=progress,
            )


progress_store = ProgressStore(STORE_PATH)
