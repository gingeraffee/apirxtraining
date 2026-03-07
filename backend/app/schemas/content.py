from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class TrackInfo(BaseModel):
    id: str
    name: str
    support_contact: dict[str, str]
    toolkit_slugs: list[str]
    section_overrides: dict[str, Any] = {}


class ContentResponse(BaseModel):
    organization: dict[str, Any]
    dashboardStats: list[dict[str, Any]]
    contacts: list[dict[str, Any]]
    sections: list[dict[str, Any]]
    toolkits: list[dict[str, Any]]
    track: TrackInfo


class SectionResponse(BaseModel):
    section: dict[str, Any]


class ToolkitResponse(BaseModel):
    toolkit: dict[str, Any]
