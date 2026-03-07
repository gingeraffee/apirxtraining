import type { ExperienceContent, ProgressRecord, ProgressUpdate } from "@/lib/types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return (await response.json()) as T;
}

export function fetchExperience(): Promise<ExperienceContent> {
  return request<ExperienceContent>("/content/experience");
}

export function fetchProgress(employeeId: string): Promise<ProgressRecord> {
  return request<ProgressRecord>(`/progress/${employeeId}`);
}

export function saveProgress(employeeId: string, payload: ProgressUpdate): Promise<ProgressRecord> {
  return request<ProgressRecord>(`/progress/${employeeId}`, {
    method: "PUT",
    body: JSON.stringify(payload),
  });
}

export function acknowledgeSection(employeeId: string, sectionSlug: string, displayName: string): Promise<ProgressRecord> {
  return request<ProgressRecord>(`/progress/${employeeId}/acknowledgments`, {
    method: "POST",
    body: JSON.stringify({ section_slug: sectionSlug, display_name: displayName }),
  });
}

