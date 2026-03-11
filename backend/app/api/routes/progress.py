from __future__ import annotations

from fastapi import APIRouter

from app.schemas.progress import AcknowledgmentUpdate, ProgressRecord, ProgressUpdate, QuizSubmissionResult, QuizSubmissionUpdate
from app.services.progress import progress_store


router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("/{employee_id}", response_model=ProgressRecord)
def read_progress(employee_id: str) -> ProgressRecord:
    return progress_store.get(employee_id)


@router.put("/{employee_id}", response_model=ProgressRecord)
def write_progress(employee_id: str, update: ProgressUpdate) -> ProgressRecord:
    return progress_store.save(employee_id, update)


@router.post("/{employee_id}/acknowledgments", response_model=ProgressRecord)
def submit_acknowledgment(employee_id: str, update: AcknowledgmentUpdate) -> ProgressRecord:
    return progress_store.acknowledge(employee_id, update)


@router.post("/{employee_id}/knowledge-checks", response_model=QuizSubmissionResult)
def submit_knowledge_check(employee_id: str, update: QuizSubmissionUpdate) -> QuizSubmissionResult:
    return progress_store.submit_knowledge_check(employee_id, update)
