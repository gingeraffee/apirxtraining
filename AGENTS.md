# AGENTS.md

## Purpose
This repository contains the launch version of the **AAP Start** onboarding portal.

Your job is to implement the launch experience using the current launch spec as the primary source of truth, while preventing legacy onboarding structures, branding, assumptions, and UI behavior from leaking back into the codebase.

## Source of Truth
Treat the following file as the controlling launch spec:

- `app_start_launch_spec.md`

When this spec conflicts with:
- legacy onboarding copy
- older content structures
- outdated branding
- existing navigation assumptions
- old progress logic
- old toolkit behavior
- visible time-estimate behavior

follow the launch spec.

Do **not** merge conflicting legacy onboarding structures into the launch implementation.

## Core Launch Rules

### Branding
Keep portal branding separate from company identity.

- Portal / product name: **AAP Start**
- Company identity: **American Associated Pharmacies**
- Company short name: **AAP**

Do not use `AAP Start` where the UI is referring to the company itself.

Replace old visible branding such as:
- `AAP/API Onboarding`
- `AAP Onboarding Portal`
- `AAP/API`
- other mixed legacy onboarding labels

unless a legacy label must remain only for historical filename/reference reasons and is not user-facing.

---

### Launch Navigation
The launch UI must show:

#### Tracked onboarding path
Exactly 9 live tracked modules:
1. Welcome to AAP
2. How We Show Up
3. Tools & Systems
4. How Work Works
5. Benefits, Pay & Time Away
6. Support, Leave & Employee Resources
7. Safety at AAP
8. Your First 90 Days
9. Final Review & Acknowledgment

#### Visible but untracked
- `Where You Make an Impact`
  - visible in nav
  - Coming Soon
  - excluded from progress
- `Resource Hub`
  - visible in nav
  - excluded from progress

Do not hide `Where You Make an Impact`.
Do not count `Where You Make an Impact` or `Resource Hub` toward progress.

---

### Progress and Completion
Launch completion behavior must be:

- manual only
- no auto-complete on scroll
- no auto-complete on page-end reach
- progress calculated only from the 9 live tracked modules
- Final Review & Acknowledgment is the clearest finish line

If the current code relies on an acknowledgment object:
- manual launch mode is allowed
- empty checklist items are allowed only if the UI does not render fake checklist shells

Do not show:
- `0/0 checkpoints`
- empty checklist containers
- quiz placeholders
- unfinished interactive blocks

---

### Toolkits
Toolkits are not part of launch.

Rules:
- `toolkits` should be empty at launch
- hide toolkit nav when `toolkits.length === 0`
- hide toolkit UI sections when empty
- do not render empty role-specific areas
- do not show `HR Admin Toolkit` in launch UI

---

### Time Estimates
Launch must not show visible module time estimates.

Remove or neutralize launch-facing dependencies on:
- `estimatedMinutes`
- remaining minutes
- average minutes
- `min left`
- other visible duration language

If a timing field must remain internally for future work, keep it out of the launch UI.

---

### Resource Hub
Resource Hub must launch with:
- real categories
- only approved live items
- no pending links rendered as live
- no placeholder clutter exposed in UI

Allowed launch behavior:
- categories may exist with a limited number of real entries
- only approved files/contacts/links should render

Do not expose:
- fake polished placeholders
- dead links
- “coming later” junk in live hub sections

---

## Data Model Rules

### Preferred launch truth
Use these collections as the truth:

- `sections` = tracked live modules
- `supplementalPages` = visible untracked pages
- `toolkits` = empty at launch

Navigation should be derived from:
- `sections`
- `supplementalPages`

Avoid keeping the same module truth in multiple parallel structures.

Do not maintain redundant launch truth across:
- tracked slug arrays
- supplemental slug arrays
- duplicate nav manifests
- duplicate module order definitions

unless absolutely required for app stability.

---

### Branding model
Do not use one ambiguous `organization.name` field for both company identity and product branding.

Preferred pattern:
- `brand.portalName = "AAP Start"`
- `organization.companyName = "American Associated Pharmacies"`
- `organization.companyShortName = "AAP"`

---

### Contacts
Contacts must have stable IDs.

Other structures, especially Resource Hub entries, must reference contacts by stable ID rather than relying on matching names or invented refs.

---

### Timekeeping naming
Use one consistent employee-facing label across the launch implementation:

**Timeclock**

Do not alternate between:
- `Timeclock`
- `PayClock`

Use `Timeclock` in employee-facing launch UI and content.

---

## Content Safety Rules
Do not invent or expand:
- legal language
- leave/accommodation details
- benefits specifics beyond the locked launch content
- attendance thresholds beyond approved launch level
- policy promises
- role-specific content not approved for launch

Do not add:
- quiz content
- checklist content
- knowledge checks
- half-built “more coming later” content inside live modules

Keep launch content:
- warm
- polished
- practical
- employee-facing
- structured
- easy to scan

Do not turn launch content into:
- handbook paste
- marketing copy
- internal drafting memo
- legal wall-of-text

---

## Required Working Style
Before making implementation edits, do the following:

1. audit the repo for launch conflicts
2. identify files where old onboarding assumptions still exist
3. replace outdated structures rather than blending them
4. report remaining conflicts clearly if they cannot be resolved safely

Do not quietly preserve legacy behavior just because it already exists.

---

## Audit Targets
Before coding, check for:

### Old branding
- `AAP/API Onboarding`
- `AAP Onboarding Portal`
- `AAP/API`
- mixed old labels in metadata, rails, hero copy, loading states, headings

### Old launch assumptions
- outdated module counts
- old section slugs
- legacy onboarding content seeds
- hardcoded toolkit links
- old progress math
- old route labels
- ambiguous `organization.name` usage

### Time estimate drift
- `estimatedMinutes`
- remaining minutes
- average minutes
- path time summaries
- hero minute summaries

### UI leakage
- empty toolkit UI
- empty checklist UI
- pending Resource Hub items rendered as live
- role-specific content surfacing before role logic exists

---

## High-Risk Files
Pay especially close attention to files like:
- `content.py`
- `types.ts`
- `api.ts`
- `portal-experience.tsx`
- `overview-screen.tsx`
- `overview-hero.tsx`
- `course-path.tsx`
- rail/sidebar/nav components
- layout metadata
- progress logic files

These are the most likely places for legacy assumptions to leak into launch behavior.

---

## Implementation Priorities
When implementing the launch version, work in this order:

1. audit repo for conflicts
2. update and lock data model
3. replace launch content pack
4. update nav and progress logic
5. hide toolkit UI
6. remove visible time-estimate dependencies
7. wire Resource Hub file resolution
8. replace legacy branding strings
9. run final drift review

---

## Reporting Requirements
After making changes, provide a concise implementation report that includes:

1. files changed
2. legacy strings replaced
3. outdated structures removed or neutralized
4. progress logic changes made
5. toolkit UI gating changes made
6. estimatedMinutes dependencies removed
7. any remaining launch risks or unresolved follow-ups

If something could not be safely changed, say so clearly.

Do not pretend a conflict is resolved if it is not.

---

## Final Rule
When in doubt:
- prefer launch correctness over legacy compatibility
- prefer replacement over patching
- prefer explicit truth over repo vibes
- prefer visible clarity over hidden assumptions