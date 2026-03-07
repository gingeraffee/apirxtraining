from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock

from app.schemas.progress import AcknowledgmentUpdate, ProgressRecord, ProgressUpdate


ROOT_DIR = Path(__file__).resolve().parents[3]
STORE_PATH = ROOT_DIR / "backend" / "app" / "data" / "progress_store.json"
CORE_SECTION_COUNT = 7


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
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _write(self, payload: dict) -> None:
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def _decorate(self, employee_id: str, payload: dict) -> ProgressRecord:
        completed = payload.get("completed_sections", [])
        ratio = round(len(completed) / CORE_SECTION_COUNT, 3) if CORE_SECTION_COUNT else 0.0
        return ProgressRecord(
            employee_id=employee_id,
            display_name=payload.get("display_name"),
            current_section=payload.get("current_section"),
            completed_sections=completed,
            acknowledged_sections=payload.get("acknowledged_sections", []),
            toolkit_completed=payload.get("toolkit_completed", False),
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

            employees[employee_id] = {
                "display_name": update.display_name or existing.get("display_name"),
                "current_section": update.current_section,
                "completed_sections": sorted(set(update.completed_sections)),
                "acknowledged_sections": sorted(set(update.acknowledged_sections)),
                "toolkit_completed": update.toolkit_completed,
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

            completed = set(existing.get("completed_sections", []))
            completed.add(update.section_slug)
            acknowledged = set(existing.get("acknowledged_sections", []))
            acknowledged.add(update.section_slug)

            employees[employee_id] = {
                "display_name": update.display_name or existing.get("display_name"),
                "current_section": update.section_slug,
                "completed_sections": sorted(completed),
                "acknowledged_sections": sorted(acknowledged),
                "toolkit_completed": existing.get("toolkit_completed", False),
                "started_at": started_at,
                "updated_at": now,
            }
            self._write(payload)
            return self._decorate(employee_id, employees[employee_id])


progress_store = ProgressStore(STORE_PATH)
