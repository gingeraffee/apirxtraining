# AGENTS.md

## Project identity
This repository is for an employee onboarding and training app.

Treat this project as a product that may be **recreated from scratch** when needed to achieve a higher-quality result. The current implementation is **not** the source of truth for design, structure, or UX quality. The source of truth is the **business purpose**, **training goals**, and the design/engineering standards in this file.

The goal is to create an onboarding experience that feels modern, engaging, interactive, premium, and easy for employees to use. The product should make employees feel confident, impressed, and interested while moving through training.

## Rebuild-first instruction
When a task calls for major improvement, you may:
- rebuild pages from scratch
- replace the current UI structure
- replace outdated layout patterns
- replace inconsistent styling
- reorganize component structure
- remove obsolete or low-quality frontend code

Do **not** feel obligated to preserve the current frontend implementation if it conflicts with the desired product quality.

Treat the existing app primarily as:
- a reference for business requirements
- a reference for training content
- a reference for important workflows
- a reference for backend or functional constraints that still matter

Do **not** treat the current UI, layout, styling, or component structure as sacred.

## Core product goals
Prioritize:
- clear navigation
- intuitive user flow
- digestible training content
- visually cohesive screens
- modular layouts
- polished interactions
- beginner-friendly experiences
- obvious next steps
- strong onboarding momentum

Avoid:
- dense walls of text
- confusing navigation
- cluttered layouts
- lifeless forms
- generic admin-dashboard styling
- inconsistent spacing or components
- placeholder-looking UI
- patchwork redesigns that still feel old underneath

## Design direction
The app should feel:
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

It should not feel:
- corporate
- overly professional
- boring
- plain
- stiff
- generic
- visually flat
- outdated

## Visual inspiration
Use the general product feel of Twitter/X as inspiration for:
- clarity
- crispness
- modularity
- speed
- confidence in layout and typography

Do not literally copy branding or layout. The goal is a social-product-inspired onboarding experience, not a clone.

## Color system
Primary palette:
- red
- navy
- cyan

Use the palette intentionally:
- navy for depth, structure, headers, major surfaces, and strong contrast
- cyan for highlights, interactive accents, hover/focus states, and modern energy
- red for calls to action, emphasis, status moments, and visual personality

Avoid muddy color combinations, washed-out neutral-heavy screens, or dark heavy interfaces that feel oppressive.

## Layout rules
Prefer:
- modular page structure
- card-based sections
- integrated page navigation
- consistent spacing
- strong visual hierarchy
- clean alignment
- clearly separated sections
- layouts that feel connected across the app

The UI should feel structured but lively, not bureaucratic.

## Motion and interactivity
Use moderate but subtle motion:
- hover states
- smooth transitions
- gentle feedback on click or completion
- polished card interactions
- responsive progress indicators
- tasteful micro-interactions

Animation should support the product feel without becoming flashy, chaotic, distracting, or gimmicky.

## Tone and copy
UI copy should be:
- clear
- modern
- concise
- helpful
- lightly witty where appropriate

Avoid:
- robotic wording
- generic filler text
- overly formal corporate language
- cheesy or confusing phrasing

Training content should be easy to scan and broken into digestible sections.

## UX expectations
When designing screens or features:
- reduce friction
- guide users clearly from one step to the next
- make actions obvious
- avoid overwhelming first-time users
- keep the experience interactive rather than static
- maintain confidence and momentum throughout onboarding

Employees using the app should feel:
- confident
- impressed
- interested

## Engineering expectations
When editing code:
- preserve important business logic unless replacement is clearly better
- preserve required backend functionality unless the task requires changing it
- prefer a clean rebuild over incremental patching when the current implementation is limiting quality
- make architecture decisions that improve long-term maintainability
- keep code modular and readable
- reuse solid patterns where appropriate
- remove obsolete or conflicting code when replacing old implementations
- write production-quality code, not demo-quality code
- do not add dependencies unless they are truly necessary

## Frontend quality bar
When working on UI:
- do not settle for “just functional” if a polished solution is achievable
- improve awkward, inconsistent, unfinished, or generic-looking areas
- maintain visual cohesion across all pages
- prefer premium product design over corporate dashboard design
- prefer clean cards and strong hierarchy over plain stacked layouts
- preserve responsiveness and readability

If the existing frontend is structurally weak, inconsistent, or visually outdated, replacing it is preferred over layering more fixes on top of it.

## Safe change boundaries
Unless explicitly requested:
- do not rewrite working backend logic purely for aesthetic reasons
- do not remove important business workflows
- do not break onboarding/training functionality in the name of redesign
- do not introduce unnecessary architectural complexity
- do not keep bad UI patterns just because they already exist

It is acceptable to replace:
- page layouts
- component structure
- styling systems
- navigation patterns
- low-quality helper code tied to outdated UI

as long as the rebuilt result better serves the product goals.

## Rebuild decision rule
When choosing between patching the current implementation or rebuilding it, prefer rebuilding if:
- the current page is visually inconsistent
- the layout is difficult to improve cleanly
- the UX feels outdated or awkward
- the code is fighting the desired design direction
- incremental edits would create a patchwork result
- a rebuild would produce a more cohesive and maintainable outcome

## Validation before finishing
Before finalizing work:
- check for broken imports
- check for syntax errors
- confirm navigation flow works
- confirm the updated feature still supports the onboarding use case
- confirm styling matches the design direction
- confirm spacing and hierarchy feel cohesive
- remove obsolete code that is no longer needed
- note what was preserved versus rebuilt
- note any assumptions if something was unclear

## Default standard
Every feature should feel:
modern, cohesive, interactive, visually confident, and premium — with personality and energy, but without clutter or excessive flash.