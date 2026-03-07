# AGENTS.md

## Project identity
This repository is for a complete rebuild of an employee onboarding and training app.

The goal is to create a modern onboarding platform with a **Next.js frontend** and a **FastAPI backend**. This should feel like a polished SaaS product, not a Streamlit-style internal tool, generic dashboard, or corporate training portal.

The source of truth is:
1. the business purpose of the onboarding app
2. the uploaded onboarding/policy documents
3. the design and engineering standards in this file

The previous Streamlit implementation is only a reference for business intent and useful workflows. It is **not** the source of truth for frontend architecture, UI patterns, or visual quality.

---

## Core goal
Build an onboarding experience that makes employees feel:
- confident
- impressed
- interested
- guided

The product should feel:
- sleek
- modern
- glassy
- premium
- interactive
- crisp
- content-rich
- easy to navigate

It should not feel:
- corporate training
- compliance-heavy
- plain
- stiff
- generic
- boxy
- visually flat
- like a dashboard template

---

## Tech stack
### Frontend
Use **Next.js** as the frontend framework.

Frontend responsibilities:
- layouts
- routing
- navigation
- page composition
- visual system
- design components
- progress UI
- onboarding flow presentation
- role-specific page experiences
- rich content rendering

### Backend
Use **FastAPI** as the backend framework.

Backend responsibilities:
- content/API endpoints where needed
- progress tracking
- acknowledgments / quiz submissions
- role-based content retrieval
- business logic
- persistence / data access
- validation
- clean API structure

Do not collapse the app back into a monolithic one-file prototype.

---

## Rebuild-first instruction
This project may be rebuilt from scratch whenever needed to achieve a better result.

When the current implementation is limiting quality, it is acceptable to:
- replace old UI structure
- replace outdated layouts
- redesign navigation
- reorganize component structure
- remove obsolete frontend code
- replace weak or inconsistent styling systems
- introduce cleaner architecture

Do not preserve poor UI patterns just because they already exist.

Treat old implementations primarily as:
- business references
- workflow references
- content references
- logic references if still useful

Do not treat old page layouts, styling, or component structures as sacred.

---

## Content source of truth
Use the onboarding documents as the source of truth for content.

This includes content for:
- company introduction
- policies
- benefits
- attendance and PTO
- leave/support
- conduct/confidentiality
- acknowledgments
- role-specific guidance

Do not ignore the source documents and replace them with broad generic filler.

Do not dump source document text into the UI verbatim.
Instead:
- preserve meaning
- preserve policy accuracy
- rewrite for product UX
- organize into app-friendly sections
- make it easy to scan and understand

---

## Product structure
The main onboarding flow is for **all new employees**.

### General employee onboarding sections
Build the app around these main sections:
1. Welcome to AAP/API
2. Working at AAP/API
3. Attendance, Timekeeping, and PTO
4. Benefits and Eligibility
5. Conduct, Confidentiality, and Workplace Standards
6. Leave and Support
7. Final Review and Acknowledgments

### Role-specific section
Create a separate role-specific area:
- HR Administrative Assistant Toolkit

This role-specific area must stay separate from the general employee onboarding flow so the main experience remains relevant to all employees.

---

## UX direction
Prioritize:
- clear navigation
- strong onboarding momentum
- obvious next steps
- digestible content
- guided progression
- clean hierarchy
- rich but readable content presentation
- modular sections
- polished feedback states

Avoid:
- walls of text
- shallow module cards
- vague progress flow
- clutter
- lifeless forms
- weak hierarchy
- generic admin-panel aesthetics
- patchwork redesigns

The experience should feel like a guided product journey, not a static training database.

---

## Visual design direction
The interface should feel:
- fun
- witty
- engaging
- interactive
- clean
- cool
- crisp
- sleek
- trendy
- premium

The design should use a modern SaaS language with:
- layered glass-style panels
- subtle blur/transparency
- soft depth
- rich typography
- elegant spacing
- strong visual hierarchy
- polished interaction feedback
- modern card composition
- cohesive page rhythm

Do not create:
- thin outlined corporate boxes everywhere
- generic dashboard cards
- boring compliance screens
- flat visual presentation
- clunky training-module UI

---

## Color direction
Primary palette:
- navy
- cyan
- red

Use color intentionally:
- navy for structure, depth, headers, contrast, and grounding surfaces
- cyan for interactive energy, highlights, focus states, and fresh accents
- red for emphasis, calls to action, status moments, and visual personality

Avoid muddy combinations, washed-out neutral-heavy screens, or overly dark oppressive layouts.

---

## Content presentation rules
Do not present content as generic training modules with a title, one sentence, and a checkbox.

Use richer SaaS-style content patterns such as:
- hero sections
- rich text panels
- glass info cards
- key takeaway blocks
- accordion FAQs
- timeline / milestone components
- action guidance callouts
- escalation alerts
- completion / acknowledgment blocks
- resource panels
- quick-reference drawers

Each major section should generally include:
- a strong title
- a concise intro
- structured content blocks
- summary content from the source docs
- key takeaways
- actions or reminders where relevant
- next-step guidance
- completion state where appropriate

---

## Copy and tone
UI copy should be:
- clear
- modern
- concise
- helpful
- lightly polished
- human

It may be slightly witty where appropriate, but it should never become cheesy, confusing, or unprofessional.

Avoid:
- robotic text
- filler-heavy paragraphs
- over-corporate phrasing
- overly legalistic tone in every section

Training content should be easy to scan and should feel designed for software, not pasted from a handbook.

---

## Frontend architecture expectations
Use a maintainable Next.js structure with:
- route groups or clean route organization where helpful
- shared layout(s)
- reusable components
- clear separation between page-level UI and reusable UI primitives
- consistent styling patterns
- clean state handling
- responsive design
- scalable content composition

Prefer:
- modular component organization
- reusable section shells
- reusable cards/callouts/FAQ/timeline patterns
- clear design system thinking

Do not build the frontend as one giant page or as a pile of inconsistent page-specific hacks.

---

## Backend architecture expectations
Use a maintainable FastAPI structure with:
- clearly organized routers/endpoints
- schemas/models where appropriate
- separated business logic
- validation
- a clean service or domain layer when useful
- future-friendly structure for progress tracking and acknowledgments

Prefer clean backend boundaries over mixing business logic into frontend code.

Do not create a tangled backend that only works for one narrow page flow.

---

## Data and feature expectations
Support a structure that can handle:
- onboarding sections/modules
- employee progress state
- acknowledgments or completion markers
- quiz or knowledge-check submission if used
- role-specific content access
- future expansion of onboarding tracks

The implementation should be flexible enough to support growth without redoing the architecture.

---

## Safe change boundaries
Unless explicitly requested:
- do not preserve bad UI patterns from the old app
- do not rewrite backend logic purely for aesthetics
- do not remove important business workflows
- do not mix role-specific HR admin content into the general employee path
- do not over-engineer the system with unnecessary complexity
- do not add dependencies unless they clearly improve the product and are justified

It is acceptable to replace:
- page layouts
- styling systems
- navigation patterns
- weak helper code
- obsolete frontend structures
- low-quality scaffolding

as long as the new result better serves the product goals.

---

## Build sequence
When doing major work, prefer this order:
1. define the architecture and folder structure
2. scaffold the Next.js frontend and FastAPI backend
3. establish the design system and layout shell
4. implement general onboarding sections
5. implement role-specific HR Administrative Assistant Toolkit
6. wire progress / acknowledgment behavior
7. refine cohesion, polish, and responsiveness
8. review for completeness and quality

Do not jump straight into random page styling without first establishing a solid structure.

---

## Quality bar
This should feel like a real software product that could plausibly be deployed as a polished employee onboarding platform.

Do not settle for:
- placeholder admin UI
- generic dashboard screens
- shallow content structure
- weak typography
- ugly spacing rhythm
- “good enough” styling
- inconsistent components
- minimal redesign shortcuts

Prefer a cohesive, premium product experience over fast but bland output.

---

## Validation before finishing
Before finalizing work:
- check for broken imports
- check for syntax/type errors
- confirm routing/navigation works
- confirm frontend and backend boundaries are clean
- confirm all major content areas are represented
- confirm the UI matches the intended SaaS design direction
- confirm the role-specific toolkit is separate from the general onboarding flow
- remove obsolete code that is no longer needed
- note what is complete vs placeholder
- note key assumptions if anything was unclear

---

## Default standard
Every feature should feel:
modern, cohesive, guided, interactive, visually confident, and premium — with personality and energy, but without clutter or gimmicks.