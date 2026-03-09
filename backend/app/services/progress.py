from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock

from app.schemas.progress import AcknowledgmentUpdate, ProgressRecord, ProgressUpdate
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

    def _read(self) -> dict:
        return json.loads(self.path.read_text(encoding="utf-8-sig"))

    def _write(self, payload: dict) -> None:
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def _normalize_completed(self, values: list[str] | None) -> list[str]:
        return sorted({slug for slug in values or [] if slug in TRACKED_SECTION_SLUGS})

    def _normalize_current(self, value: str | None) -> str | None:
        return value if value in ALL_PAGE_SLUGS else None

    def _decorate(self, employee_id: str, payload: dict) -> ProgressRecord:
        completed = self._normalize_completed(payload.get("completed_sections", []))
        acknowledged = self._normalize_completed(payload.get("acknowledged_sections", []))
        ratio = round(len(completed) / CORE_SECTION_COUNT, 3) if CORE_SECTION_COUNT else 0.0
        return ProgressRecord(
            employee_id=employee_id,
            display_name=payload.get("display_name"),
            current_section=self._normalize_current(payload.get("current_section")),
            completed_sections=completed,
            acknowledged_sections=acknowledged,
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

            employees[employee_id] = {
                "display_name": update.display_name or existing.get("display_name"),
                "current_section": current_section,
                "completed_sections": self._normalize_completed(update.completed_sections),
                "acknowledged_sections": self._normalize_completed(update.acknowledged_sections),
                "started_at": started_at,
                "updated_at": now,
            }
            self._write(payload)
            return self._decorate(employee_id, employees[employee_id])

    def acknowledge(self, employee_id: str, update: AcknowledgmentUpdate) -> ProgressRecord:
        with self._lock:
            payload = self._read()
            employees = payload["employees"]
            existing = employees.get(employee_id, {})
            now = datetime.now(timezone.utc).isoformat()
            started_at = existing.get("started_at") or now

            completed = set(self._normalize_completed(existing.get("completed_sections", [])))
            acknowledged = set(self._normalize_completed(existing.get("acknowledged_sections", [])))
            if get_section_by_slug(update.section_slug):
                completed.add(update.section_slug)
                acknowledged.add(update.section_slug)

            employees[employee_id] = {
                "display_name": update.display_name or existing.get("display_name"),
                "current_section": self._normalize_current(update.section_slug) or self._normalize_current(existing.get("current_section")),
                "completed_sections": sorted(completed),
                "acknowledged_sections": sorted(acknowledged),
                "started_at": started_at,
                "updated_at": now,
            }
            self._write(payload)
            return self._decorate(employee_id, employees[employee_id])


progress_store = ProgressStore(STORE_PATH)
