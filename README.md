# AAP Onboarding Platform

This repository is a two-app onboarding platform:

- `frontend/`: Next.js application for the employee experience
- `backend/`: FastAPI application for content, progress tracking, and acknowledgments

## Product shape

The rebuilt experience follows the structure defined in `AGENTS.md`:

1. Welcome to AAP
2. Working at AAP
3. Attendance, Timekeeping, and PTO
4. Benefits and Eligibility
5. Conduct, Confidentiality, and Workplace Standards
6. Leave and Support
7. Final Review and Acknowledgments
8. Separate role-specific toolkit: HR Administrative Assistant Toolkit

## Frontend

The frontend uses the Next.js App Router and a shared design system built with plain CSS.

Suggested local setup:

```bash
cd frontend
npm install
npm run dev
```

The frontend expects the API at `http://127.0.0.1:8000/api/v1` by default. Override with `NEXT_PUBLIC_API_BASE_URL`.

## Backend

The backend exposes content, toolkit, progress, and acknowledgment endpoints.

Suggested local setup:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API includes:

- `GET /api/v1/health`
- `GET /api/v1/content/experience`
- `GET /api/v1/content/sections/{slug}`
- `GET /api/v1/content/toolkits/{slug}`
- `GET /api/v1/progress/{employee_id}`
- `PUT /api/v1/progress/{employee_id}`
- `POST /api/v1/progress/{employee_id}/acknowledgments`

Progress is persisted locally in `backend/app/data/progress_store.json`.

## Source content

The source-of-truth documents remain in the repo root and `.extracted_docs/`. The API content is a product-UX rewrite of those materials, not a verbatim dump.