from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.schemas.content import ContentResponse, SectionResponse, ToolkitResponse
from app.services.content import get_experience_content, get_section_by_slug, get_toolkit_by_slug


router = APIRouter(prefix="/content", tags=["content"])


@router.get("/experience", response_model=ContentResponse)
def read_experience(track: str = "default") -> ContentResponse:
    return ContentResponse(**get_experience_content(track_id=track))


@router.get("/sections/{slug}", response_model=SectionResponse)
def read_section(slug: str) -> SectionResponse:
    section = get_section_by_slug(slug)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return SectionResponse(section=section)


@router.get("/toolkits/{slug}", response_model=ToolkitResponse)
def read_toolkit(slug: str) -> ToolkitResponse:
    toolkit = get_toolkit_by_slug(slug)
    if not toolkit:
        raise HTTPException(status_code=404, detail="Toolkit not found")
    return ToolkitResponse(toolkit=toolkit)
