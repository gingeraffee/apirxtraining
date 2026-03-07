from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class ContentResponse(BaseModel):
    organization: dict[str, Any]
    dashboardStats: list[dict[str, Any]]
    contacts: list[dict[str, Any]]
    sections: list[dict[str, Any]]
    toolkits: list[dict[str, Any]]


class SectionResponse(BaseModel):
    section: dict[str, Any]


class ToolkitResponse(BaseModel):
    toolkit: dict[str, Any]
