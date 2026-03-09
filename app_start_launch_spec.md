# AAP Start Launch Spec

## Status
This document is the launch source of truth for the AAP Start onboarding portal.

For launch work, this spec overrides:
- legacy onboarding copy in the repo
- older content structures
- outdated branding labels
- prior assumptions about tracked modules, toolkits, progress, and time estimates

Do not merge conflicting legacy onboarding structures into the launch implementation.

---

## Product Identity

### Portal / Product Name
**AAP Start**

### Company Identity
**American Associated Pharmacies**  
Short name: **AAP**

Important:
- `AAP Start` is the portal/product name.
- `American Associated Pharmacies` / `AAP` is the company identity.
- Do not use `AAP Start` where the UI is referring to the company itself.
- Do not keep or reintroduce legacy branding such as:
  - `AAP/API Onboarding`
  - `AAP Onboarding Portal`
  - `AAP/API`
  - other mixed legacy labels unless explicitly required for historical file names only

---

## Launch Purpose

AAP Start is a guided onboarding experience for new hires across AAP.

Its purpose is to guide new employees through:
- essential company information
- workplace expectations
- required tools and systems
- key policies at a practical level
- support resources
- what to expect in the first 90 days

The launch experience should feel:
- warm
- polished
- modern
- welcoming
- clear
- employee-facing
- structured and easy to scan

It should **not** feel like:
- a document dump
- a raw handbook pasted into a portal
- internal admin training
- overly legalistic policy copy
- half-finished product scaffolding

---

## Launch Scope

### Tracked Onboarding Path at Launch
The tracked onboarding path contains exactly **9 live modules**:

1. Welcome to AAP
2. How We Show Up
3. Tools & Systems
4. How Work Works
5. Benefits, Pay & Time Away
6. Support, Leave & Employee Resources
7. Safety at AAP
8. Your First 90 Days
9. Final Review & Acknowledgment

### Visible but Untracked at Launch
These items must appear in navigation, but must **not** count toward progress:

- **Where You Make an Impact**
  - visible in nav
  - marked as **Coming Soon**
  - excluded from completion/progress
  - locked-state page only at launch

- **Resource Hub**
  - visible in nav
  - always available
  - excluded from completion/progress
  - launches with real categories and only approved live items

---

## Completion Rules

### Launch Completion Behavior
Launch completion must follow these rules:

- completion is **manual**
- modules are completed only when the user intentionally clicks the complete/continue action
- modules must **not** auto-complete on scroll
- modules must **not** auto-complete when the user reaches the bottom of a page
- progress must be calculated only from the 9 live tracked modules
- `Where You Make an Impact` must be excluded from progress
- `Resource Hub` must be excluded from progress
- `Final Review & Acknowledgment` must be the clearest finish line in the onboarding path

### Acknowledgment Structure
For launch:
- do not add quiz content
- do not add checkbox sets
- do not add interactive knowledge checks
- keep launch completion manual and reliable

If the current code requires an acknowledgment object for completion flow, it is acceptable to keep:

- `acknowledgment.mode = "manual"`
- empty `acknowledgment.items = []`

But the UI must not render:
- empty checklist shells
- `0/0 checkpoints`
- unfinished quiz/checklist visuals

The launch UI must hide checklist rendering when:
- `acknowledgment.mode == "manual"`
- or `acknowledgment.items.length === 0`

---

## Navigation Rules

### Source of Truth
Navigation must not be maintained in multiple conflicting places.

Use:
- `SECTIONS` as the source of truth for tracked modules
- `SUPPLEMENTAL_PAGES` as the source of truth for visible untracked pages

Navigation should be derived from those collections, or otherwise kept minimal and non-redundant.

Avoid parallel truth structures such as:
- separate tracked slug lists
- separate supplemental slug lists
- duplicated nav manifests
- duplicated module order declarations in multiple files unless strictly required

### Launch Navigation Behavior
The UI should show:
- the 9 tracked modules in the main onboarding journey
- `Where You Make an Impact` as a polished Coming Soon item
- `Resource Hub` as a real nav item outside completion tracking

Do not hide `Where You Make an Impact` completely.  
Do not count untracked pages in progress.

---

## Toolkits at Launch

Toolkits are **not part of launch**.

### Launch Rules
- `toolkits` should be empty at launch
- toolkit UI/nav should be hidden when no toolkit items exist
- do not show empty toolkit sections
- do not show role-specific toolkit links
- do not show “HR Admin Toolkit” in launch UI

Role-specific content is intentionally deferred.

---

## Time Estimate Rules

Launch must not show visible module time estimates.

### Required Cleanup
Remove or neutralize launch-facing dependencies on:
- `estimatedMinutes`
- remaining minutes
- average minutes
- “min left”
- any similar visible time estimate UI

If the codebase still needs a timing field internally for future use, move it to a non-launch, non-displayed field.  
Do not show module durations in the launch experience.

---

## Resource Hub Rules

### Launch Intent
The Resource Hub is a persistent reference shelf outside the tracked onboarding path.

It should launch with:
- real categories
- only approved live items
- no placeholder links exposed as if they are ready
- no pending items rendered as live content

### Allowed Launch Categories
Categories may exist at launch even with limited entries, but only real approved entries should appear.

Approved launch categories:
- Handbook & Policies
- Benefits
- Time Away
- Support Contacts

Deferred categories may be added later, but should not appear as half-ready launch clutter unless they have approved live entries.

### Launch-Ready Item Rule
Only items that are actually ready should be marked live.

Do **not** expose:
- pending external links
- empty download slots
- placeholder entries
- “coming later” resource clutter inside the Resource Hub

---

## Content Boundaries

### Keep Core Onboarding Universal
The launch modules should remain universal where possible.

Keep out of core onboarding:
- role-specific workflows
- department-only systems
- warehouse equipment/process training
- management-only content
- HR-admin-only content
- advanced compliance/process training
- location-specific operational details unless they apply company-wide

### Keep Legal / Policy Language Practical
Launch content should:
- stay high-level where appropriate
- avoid over-explaining leave/accommodation/legal details
- avoid policy promises
- avoid invented specifics

Do not expand beyond verified content.

---

## Locked Module Lineup

The launch module lineup must remain:

1. Welcome to AAP  
2. How We Show Up  
3. Tools & Systems  
4. How Work Works  
5. Benefits, Pay & Time Away  
6. Support, Leave & Employee Resources  
7. Safety at AAP  
8. Where You Make an Impact  
9. Your First 90 Days  
10. Final Review & Acknowledgment  
11. Resource Hub

Important:
- `Where You Make an Impact` is visible but untracked
- `Resource Hub` is visible but untracked
- the tracked live completion path still contains only 9 modules

---

## Locked Content Model Decisions

### Branding / Organization Model
The model must clearly distinguish:
- portal/product branding
- company identity

Recommended split:
- `brand.portalName = "AAP Start"`
- `organization.companyName = "American Associated Pharmacies"`
- `organization.companyShortName = "AAP"`

Do not collapse these into one ambiguous `name` field.

### Contacts
Contacts must include stable IDs so other content can reference them safely.

Required launch contacts:
- Nicole Thornton, HR Manager
- Brandy Hooper, VP of HR
- IT Support placeholder entry only if it is not surfaced as a broken live contact path

### Timekeeping Naming
Use one consistent employee-facing label for the timekeeping system across launch content.

Launch label:
**Timeclock**

Do not alternate between:
- Timeclock
- PayClock

Use `Timeclock` in employee-facing launch content.

### Benefits Timing Language
Keep benefits wording high-confidence and launch-safe.

Do not over-expand detailed benefit rules in core onboarding.  
Do not introduce uncertain plan details into the live module copy.

If a specific benefit timing statement is not clearly locked for launch, simplify it instead of stretching it.

### 401(k) Mention
Do not force explicit 401(k) timing language into the core launch module unless the developer confirms it is consistent with the locked launch content model and employee-facing scope.

Safer launch behavior:
- keep benefits timing general and classification-aware
- keep detailed benefit specifics in approved reference materials / Resource Hub

---

## Employee-Facing Launch Content Rules

### Voice
Keep the launch portal:
- warm
- human
- polished
- employee-friendly
- modern
- clear

Do not turn it into:
- handbook copy
- HR jargon soup
- marketing copy
- internal drafting memo voice

### Content Safety
Do not add:
- quiz content
- knowledge checks
- unfinished checklist copy
- placeholder “more coming later” blocks inside live modules

If something is not ready:
- keep it in the locked Coming Soon module
- or keep it out of live modules entirely

---

## Launch Data Shape

The launch implementation should use these high-level collections:

- `brand`
- `organization`
- `dashboardStats`
- `contacts`
- `sections`
- `supplementalPages`
- `toolkits`
- `track`

### Required Truth Rules
- `sections` = source of truth for live tracked modules
- `supplementalPages` = source of truth for visible untracked pages
- `toolkits = []` at launch
- nav should be derived from `sections` and `supplementalPages`
- progress should be derived only from tracked `sections`

---

## Developer Audit Requirements

Before implementing launch wiring, audit the repo for legacy conflicts.

Find and replace or neutralize:
- old branding strings:
  - `AAP/API Onboarding`
  - `AAP Onboarding Portal`
  - `AAP/API`
- old section slugs or module names that conflict with launch
- `estimatedMinutes` dependencies
- toolkit UI references
- old progress assumptions tied to outdated module counts
- old content seeds that conflict with the launch pack
- ambiguous `organization.name` usage where branding and company identity are mixed

---

## Required Pre-Wire Checks

Before wiring in launch content, confirm:

1. **File resolution**
   - Resource Hub file entries must resolve through a real backend/frontend file path
   - do not surface dead file items

2. **Manual completion UI behavior**
   - manual completion works without quiz/checklist content
   - empty acknowledgment items do not render empty checklist UI

3. **Toolkit hiding**
   - toolkit nav/UI is hidden when `toolkits.length === 0`

4. **Branding string replacement**
   - all legacy visible portal-brand labels are replaced with `AAP Start`
   - company references still correctly refer to `AAP` / `American Associated Pharmacies`

5. **Removal of estimatedMinutes dependencies**
   - no launch-facing minute estimates remain in UI
   - no broken code paths remain expecting visible time estimates

---

## Acceptance Criteria for Launch Implementation

The launch implementation is correct only if all of the following are true:

- The portal is branded as **AAP Start**
- The company identity remains **American Associated Pharmacies / AAP**
- The tracked path contains exactly 9 live modules
- `Where You Make an Impact` appears as Coming Soon
- `Where You Make an Impact` does not count toward progress
- `Resource Hub` is visible in nav
- `Resource Hub` does not count toward progress
- Progress is manual and based only on the 9 tracked modules
- `Final Review & Acknowledgment` is the clearest finish line
- Toolkit UI is hidden at launch
- No visible launch time estimates remain
- Resource Hub shows only approved live items
- No empty checklist UI or fake quiz UI appears
- No legacy `AAP/API` onboarding labels remain in visible launch surfaces

---

## Implementation Priority

When coding this launch version, work in this order:

1. audit repo for legacy conflicts  
2. update/lock data model  
3. replace launch content pack  
4. update nav/progress logic  
5. hide toolkit UI  
6. remove estimatedMinutes UI dependencies  
7. wire Resource Hub file resolution  
8. sweep branding strings  
9. run final legacy drift review

---

## Final Rule

When this spec conflicts with legacy repo content or structure, follow this spec.

Do not preserve old onboarding assumptions just because they already exist in code.
Launch correctness matters more than legacy compatibility for outdated onboarding copy, navigation, or UI labels.