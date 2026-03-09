from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class TrackInfo(BaseModel):
    id: str
    name: str
    supportContactId: str
    section_overrides: dict[str, Any] = Field(default_factory=dict)


class ContentResponse(BaseModel):
    brand: dict[str, Any]
    organization: dict[str, Any]
    dashboardStats: list[dict[str, Any]]
    contacts: list[dict[str, Any]]
    sections: list[dict[str, Any]]
    supplementalPages: list[dict[str, Any]]
    toolkits: list[dict[str, Any]]
    track: TrackInfo


class SectionResponse(BaseModel):
    section: dict[str, Any]


class ToolkitResponse(BaseModel):
    toolkit: dict[str, Any]
