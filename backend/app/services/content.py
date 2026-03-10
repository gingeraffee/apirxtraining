from __future__ import annotations

from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[3]
FRONTEND_PUBLIC_DIR = ROOT_DIR / "frontend" / "public"


def manual_acknowledgment(title: str, statement: str) -> dict[str, Any]:
    return {"mode": "manual", "title": title, "statement": statement, "items": []}


def build_section(
    *,
    section_id: str,
    slug: str,
    eyebrow: str,
    title: str,
    summary: str,
    purpose: str,
    focuses: list[str],
    essentials: list[tuple[str, str]],
    policy_areas: list[tuple[str, list[tuple[str, str]]]],
    actions: list[str],
    escalation: list[str],
    acknowledgment_title: str,
    acknowledgment_statement: str,
    chapter_intros: list[str] | None = None,
    context_sidebar: tuple[str, list[str]] | None = None,
) -> dict[str, Any]:
    section: dict[str, Any] = {
        "id": section_id,
        "slug": slug,
        "eyebrow": eyebrow,
        "title": title,
        "summary": summary,
        "purpose": purpose,
        "focuses": focuses,
        "essentials": [{"title": item_title, "body": body} for item_title, body in essentials],
        "policyAreas": [
            {
                "title": area_title,
                "items": [{"label": label, "body": body} for label, body in items],
            }
            for area_title, items in policy_areas
        ],
        "actions": actions,
        "escalation": escalation,
        "acknowledgment": manual_acknowledgment(acknowledgment_title, acknowledgment_statement),
    }
    if chapter_intros is not None:
        section["chapterIntros"] = chapter_intros
    if context_sidebar is not None:
        section["contextSidebar"] = {"title": context_sidebar[0], "body": context_sidebar[1]}
    return section


def public_file_item(item_id: str, title: str, description: str, public_path: str) -> dict[str, Any] | None:
    normalized_path = public_path.lstrip("/")
    if not (FRONTEND_PUBLIC_DIR / normalized_path).exists():
        return None
    return {
        "id": item_id,
        "type": "file",
        "title": title,
        "description": description,
        "href": public_path,
        "download": True,
    }


BRAND = {"portalName": "AAP Start"}

ORGANIZATION = {
    "companyName": "American Associated Pharmacies",
    "companyShortName": "AAP",
    "headline": "A polished starting point for how work, support, and expectations come together at AAP.",
    "tagline": "Clear next steps, practical guidance, and a calm first-week experience.",
    "mission": "AAP\u2019s mission is to provide support and customized solutions for independent and community pharmacies to enhance profitability, streamline operations, and improve the quality of patient care.",
    "vision": "Helping independent pharmacies thrive in a competitive healthcare market.",
    "story": "American Associated Pharmacies, or AAP, is a member-owned cooperative that supports independent and community pharmacies. AAP was formed in 2009 through the joining of two pharmacy organizations, and API continues to operate as AAP\u2019s warehouse and distribution arm. AAP Start turns the first stretch of employment into a guided experience so new teammates can build confidence without getting buried in handbook noise.",
    "values": [
        {"name": "Customer Focus", "body": "The work should make life easier for pharmacies, teammates, and the people depending on both."},
        {"name": "Integrity", "body": "Do the right thing clearly, consistently, and without side-stepping hard conversations."},
        {"name": "Respect", "body": "Treat people with dignity, communicate directly, and keep the tone human."},
        {"name": "Excellence", "body": "Aim for work that is thoughtful, accurate, and worth trusting."},
        {"name": "Ownership", "body": "When something matters, move it forward instead of waiting for someone else to catch it."},
    ],
}

DASHBOARD_STATS = [
    {"label": "Tracked path", "value": "9 live modules", "detail": "The launch path covers the shared essentials every new employee should see first."},
    {"label": "Launch extras", "value": "2 reference pages", "detail": "Where You Make an Impact and Resource Hub stay visible without affecting progress."},
    {"label": "First stretch", "value": "90 days", "detail": "The path is built to orient the first week and still stay useful through the first 90 days."},
]

CONTACTS = [
    {"id": "nicole-thornton", "name": "Nicole Thornton", "role": "HR Manager", "email": "nicole.thornton@apirx.com", "phone": "256-574-7528", "note": "Primary contact for onboarding questions, benefits timing, time-away routing, and general next-step help."},
    {"id": "brandy-hooper", "name": "Brandy Hooper", "role": "VP of Human Resources", "email": "brandy.hooper@rxaap.com", "phone": "256-574-7526", "note": "Escalation contact for sensitive HR concerns, unresolved issues, and higher-level employee support."},
    {"id": "cbiz-benefits", "name": "CBIZ Benefits", "role": "Benefits Support", "email": "melissa.street@cbiz.com", "phone": "844.200.2249", "note": "Benefits support after HR has routed the request and confirmed what needs action."},
    {"id": "lifematters", "name": "LifeMatters", "role": "Employee Assistance Program", "email": "", "phone": "800-634-6433", "note": "Confidential employee assistance support available from day one."},
]

SECTIONS = [
    build_section(
        section_id="welcome-to-aap",
        slug="welcome-to-aap",
        eyebrow="Start Here",
        title="Welcome to AAP",
        summary="You\u2019re joining a company that supports more than 2,000 independent and community pharmacies, and every role helps that mission move forward. Whether your work is operational, administrative, customer-facing, or behind the scenes, it plays a part in helping member pharmacies stay strong, supported, and competitive.",
        purpose="AAP Start is here to make your first stretch of onboarding clearer and easier to follow. The goal is to help you understand how AAP works, what\u2019s expected of you, where to go for help, and what to expect as you get settled in. The handbook is meant to answer many of your early questions and give you a foundation for working at AAP.",
        focuses=["Who AAP supports", "What AAP Start is for", "Where questions go"],
        essentials=[
            ("Who AAP is", "American Associated Pharmacies, or AAP, is a member-owned cooperative that supports independent and community pharmacies. AAP was formed in 2009 through the joining of two pharmacy organizations, and API continues to operate as AAP\u2019s warehouse and distribution arm."),
            ("Mission", "AAP\u2019s mission is to provide support and customized solutions for independent and community pharmacies to enhance profitability, streamline operations, and improve the quality of patient care."),
            ("Vision and values", "AAP\u2019s vision is helping independent pharmacies thrive in a competitive healthcare market. The values\u2014customer focus, integrity, respect, excellence, and ownership\u2014are meant to show up in day-to-day behavior."),
        ],
        policy_areas=[
            ("Who AAP is", [
                ("What AAP supports", "American Associated Pharmacies, or AAP, is a member-owned cooperative that supports independent and community pharmacies."),
                ("Where API fits", "AAP was formed in 2009 through the joining of two pharmacy organizations. API continues to operate as AAP\u2019s warehouse and distribution arm."),
            ]),
            ("Using AAP Start", [
                ("The right goal for day one", "You are not expected to memorize everything on day one. The goal is to help you get oriented, know the basics, and know where to look when you need a refresher."),
            ]),
        ],
        actions=[
            "Understand the basics of working at AAP.",
            "Learn where key tools and systems live.",
            "Get a clear overview of important expectations and policies.",
            "Know where to go for help.",
            "Feel more confident in your first 90 days.",
        ],
        escalation=[
            "For general onboarding, policy, benefits, or employee-record questions, contact Nicole Thornton, HR Manager.",
            "For higher-level escalation, contact Brandy Hooper, VP of HR.",
            "Your supervisor is also an important first point of contact for day-to-day support.",
        ],
        acknowledgment_title="Ready for the path",
        acknowledgment_statement="I understand what AAP Start is for, what AAP exists to support, and where to go when a question needs real context.",
        chapter_intros=[
            "Get the orientation anchor first: what AAP Start is for, what AAP does, and how support is delivered.",
            "Understand who API is, what API does, and how API references fit with AAP language in this launch experience.",
            "Use this page as a working guide for how to move through AAP Start and where to route questions in real situations.",
        ],
        context_sidebar=("Where API fits", [
            "In this launch onboarding experience, company identity is centered on American Associated Pharmacies (AAP). API appears as a historical identity reference connected to that same support mission.",
            "When API is referenced, use the same operating context covered in this module: practical programs, operational help, and dependable service for independent community pharmacies.",
        ]),
    ),
    build_section(
        section_id="how-we-show-up",
        slug="how-we-show-up",
        eyebrow="Culture",
        title="How We Show Up",
        summary="Learn the values, conduct expectations, and communication habits that shape the employee experience.",
        purpose="This module turns culture into something useful: how people are expected to treat each other, communicate, and protect trust at work.",
        focuses=["Values in practice", "Respectful conduct", "Confidentiality"],
        essentials=[
            ("Values should be visible", "Customer focus, integrity, respect, excellence, and ownership are meant to show up in day-to-day behavior."),
            ("Respect is a work standard", "Professional conduct includes respectful communication, responsible judgment, and raising issues the right way."),
            ("Confidentiality matters", "Sensitive information should stay with the people who need it to do their jobs."),
        ],
        policy_areas=[
            ("How people work together", [("Communication", "Clear, direct, and respectful communication beats vague answers and avoidable confusion."), ("Workplace behavior", "Harassment, retaliation, threats, and other unsafe conduct are escalation issues, not gray areas.")]),
            ("Protecting trust", [("Need-to-know handling", "Sensitive information should stay inside the proper process instead of getting shared casually."), ("Using company systems", "Company tools and records are for company business and should be used responsibly.")]),
        ],
        actions=["Pause before forwarding or sharing sensitive information.", "Use respectful directness when something needs to be clarified.", "Raise concerns early while they are still easy to address."],
        escalation=["Escalate harassment, retaliation, violence, or discrimination concerns immediately.", "Escalate suspected privacy mistakes or unauthorized access.", "Use HR when a people issue becomes sensitive or employee-specific."],
        acknowledgment_title="Values, clearly understood",
        acknowledgment_statement="I understand the conduct expectations, confidentiality standards, and respectful ways of working at AAP.",
    ),
    build_section(
        section_id="tools-and-systems",
        slug="tools-and-systems",
        eyebrow="Systems",
        title="Tools & Systems",
        summary="Get familiar with the core systems and the habits that keep access, records, and work moving smoothly.",
        purpose="You do not need to master every tool on day one, but you should know the key systems, the right names, and the rules around using them responsibly.",
        focuses=["Core systems", "Access basics", "Timeclock naming"],
        essentials=[
            ("Systems have owners", "Use approved company systems and go to the right support contact when access, data, or workflows do not look right."),
            ("Timeclock is the employee-facing label", "In launch materials, the timekeeping system is referred to as Timeclock so the language stays consistent."),
            ("Protect access from day one", "Passwords, shared data, and employee records should stay inside approved workflows and systems."),
        ],
        policy_areas=[
            ("Working with systems", [("Use approved tools", "Store work in approved systems and avoid moving company data into personal tools or side channels."), ("Ask early", "When something looks off in a system, get help instead of building a workaround.")]),
            ("Common launch references", [("Timeclock", "Use Timeclock consistently when referring to employee-facing timekeeping workflows."), ("Support routing", "Use your manager, HR, or the right support contact when access or setup work needs real help.")]),
        ],
        actions=["Learn the names of the systems you will actually use first.", "Keep sensitive data inside approved tools and approved channels.", "Flag access issues quickly instead of waiting until they block your work."],
        escalation=["Escalate access problems that prevent core work from moving forward.", "Escalate data-handling concerns or suspected misdirected information.", "Ask for help if a system instruction conflicts with policy or team guidance."],
        acknowledgment_title="Systems basics locked in",
        acknowledgment_statement="I understand the launch-safe system guidance and the employee-facing use of the label Timeclock.",
    ),
    build_section(
        section_id="how-work-works",
        slug="how-work-works",
        eyebrow="Work Basics",
        title="How Work Works",
        summary="Cover the practical expectations around schedules, communication, records, and staying aligned with your team.",
        purpose="This module focuses on the day-to-day operating habits that keep work clear, dependable, and easier to navigate in the first few weeks.",
        focuses=["Schedules and attendance", "Records and updates", "Who to ask"],
        essentials=[
            ("Clarity beats guessing", "If something about schedules, priorities, or process is unclear, ask early instead of making a silent assumption."),
            ("Accurate records matter", "Time worked, employee information, and routine updates should stay accurate and current."),
            ("Consistency helps teams move", "Reliable communication and follow-through reduce avoidable friction for everyone around you."),
        ],
        policy_areas=[
            ("Workday basics", [("Schedules", "Follow your team schedule and use the right path if an absence, delay, or change needs to be reported."), ("Communication", "Use your manager and team norms to stay aligned on work, deadlines, and expectations.")]),
            ("Records and responsibility", [("Employee information", "Keep HR updated when personal details that affect records or benefits need correction."), ("Responsible judgment", "Bring concerns forward early rather than letting confusion turn into rework or risk.")]),
        ],
        actions=["Confirm who to notify when your schedule changes.", "Keep your records current with HR when details change.", "Use your manager as the first stop for role-specific workflow questions."],
        escalation=["Use HR when a people, pay, or policy question goes beyond routine team guidance.", "Escalate conflicting instructions that affect compliance or fairness.", "Raise recurring blockers instead of working around them indefinitely."],
        acknowledgment_title="Day-to-day expectations make sense",
        acknowledgment_statement="I understand the practical expectations around schedules, records, and asking for help early.",
    ),
    build_section(
        section_id="benefits-pay-and-time-away",
        slug="benefits-pay-and-time-away",
        eyebrow="Benefits",
        title="Benefits, Pay & Time Away",
        summary="Get the launch-safe overview of benefits timing, pay basics, and how time away should be handled responsibly.",
        purpose="The goal here is confidence, not overloading you with plan trivia. You should know the timing basics and when to bring HR in.",
        focuses=["Benefits timing", "Pay basics", "Time-away awareness"],
        essentials=[
            ("Benefits open in stages", "Some support starts right away, while other benefits depend on classification, hire timing, or eligibility milestones."),
            ("Pay and time records need accuracy", "Time entries and pay-related questions should be handled promptly and through the right path."),
            ("Time away is not one-size-fits-all", "Planned time away, benefits questions, and leave questions each have different handling paths."),
        ],
        policy_areas=[
            ("Benefits and pay", [("Timing matters", "Benefits questions are often about timing, classification, or eligibility, so it is worth checking instead of assuming."), ("Use HR for clarity", "If pay or benefits information looks off, HR is the right place to get it corrected.")]),
            ("Time away at a high level", [("Planned requests", "Use the normal request path for planned time away and give your team as much notice as you can."), ("Unexpected absences", "Unexpected time away should be reported quickly through the right manager or team process.")]),
        ],
        actions=["Keep an eye on your own eligibility timing and ask if something looks off.", "Use Timeclock and your normal team process to keep time records accurate.", "Bring HR in quickly when benefits or pay details seem unclear."],
        escalation=["Escalate pay, deduction, or benefits-access issues to HR.", "Escalate time-away questions that do not look like normal planned PTO.", "Use HR when eligibility timing or classification looks inconsistent."],
        acknowledgment_title="Benefits and pay basics understood",
        acknowledgment_statement="I understand the launch-safe overview of benefits, pay, and time-away handling, and I know when HR needs to be involved.",
    ),
    build_section(
        section_id="support-leave-and-employee-resources",
        slug="support-leave-and-employee-resources",
        eyebrow="Support",
        title="Support, Leave & Employee Resources",
        summary="Know where support comes from, when leave questions need HR immediately, and what resources are available beyond a routine question.",
        purpose="This module keeps leave and support guidance practical: know the right lane, know when not to improvise, and know who can actually help.",
        focuses=["Leave routing", "Support resources", "Escalation paths"],
        essentials=[
            ("Leave questions can turn sensitive fast", "Medical, accommodation, and employee-specific leave situations should move to HR early instead of being handled casually."),
            ("Not every problem needs the same path", "Some questions start with a manager, while others belong with HR or a support resource right away."),
            ("Help exists before things get messy", "Support contacts and the Employee Assistance Program exist to help before strain becomes a bigger issue."),
        ],
        policy_areas=[
            ("Leave and accommodation routing", [("Medical and leave questions", "If a question becomes specific to a medical condition, leave need, or accommodation, move it to HR."), ("Do not promise outcomes", "Use careful language and let the right process determine what applies.")]),
            ("Support options", [("HR support", "HR can help with onboarding questions, benefits timing, employee records, and sensitive workplace issues."), ("Employee assistance", "LifeMatters is available as a confidential support resource from day one.")]),
        ],
        actions=["Use the right support route as soon as a question gets personal or sensitive.", "Keep leave questions factual and move them to HR early.", "Use support resources before a stressful situation snowballs."],
        escalation=["Escalate medical, accommodation, or leave-certification questions to HR immediately.", "Escalate unresolved support concerns that need higher-level help.", "Use HR when a situation affects privacy, consistency, or employee-specific interpretation."],
        acknowledgment_title="Support routes are clear",
        acknowledgment_statement="I understand when to use support resources, when leave questions require HR, and why sensitive issues should not be improvised.",
    ),
    build_section(
        section_id="safety-at-aap",
        slug="safety-at-aap",
        eyebrow="Safety",
        title="Safety at AAP",
        summary="Review the shared expectations that keep people, spaces, and day-to-day work safe across the company.",
        purpose="Safety is part of how work gets done here. This module keeps the launch guidance broad, practical, and relevant across teams.",
        focuses=["Shared responsibility", "Speak-up culture", "Incident awareness"],
        essentials=[
            ("Safety belongs to everyone", "Pay attention to your surroundings, use the right process, and do not ignore hazards because they seem minor."),
            ("Reporting matters", "Near misses, injuries, unsafe conditions, and urgent concerns should be reported quickly so they can be addressed."),
            ("Ask before improvising", "If a safety expectation is unclear, stop and get direction instead of guessing."),
        ],
        policy_areas=[
            ("Safe work habits", [("Use approved processes", "Follow the training and local guidance that applies to your workspace and responsibilities."), ("Take concerns seriously", "Unsafe conditions should be reported early, even when they seem easy to work around in the moment.")]),
            ("When to speak up", [("Urgent concerns", "If something feels unsafe or threatening, escalate immediately instead of waiting for a better time."), ("Injuries and incidents", "Report incidents and follow the company process so support and documentation happen correctly.")]),
        ],
        actions=["Learn the specific safety expectations that apply to your work area.", "Report hazards, near misses, and injuries promptly.", "Pause and ask for guidance when the safe path is not obvious."],
        escalation=["Escalate urgent safety issues immediately.", "Escalate incidents, injuries, or threats through the correct company path.", "Use your manager or HR when a safety concern overlaps with employee support needs."],
        acknowledgment_title="Safety expectations are clear",
        acknowledgment_statement="I understand the shared safety expectations and the importance of speaking up quickly when something does not look right.",
    ),
    build_section(
        section_id="your-first-90-days",
        slug="your-first-90-days",
        eyebrow="Looking Ahead",
        title="Your First 90 Days",
        summary="Shift from day-one orientation into what momentum, feedback, and confidence-building should look like in the first 90 days.",
        purpose="The first 90 days are about learning the role, building steady habits, and knowing how to ask for what you need without losing momentum.",
        focuses=["Settling in", "Feedback loops", "Building confidence"],
        essentials=[
            ("You are not expected to know everything immediately", "The first few months are for learning the role, the team rhythm, and the standards that matter most."),
            ("Feedback is part of the process", "Use conversations with your manager to calibrate priorities, progress, and where you still need support."),
            ("Confidence comes from repetition", "Returning to the portal, asking good questions, and practicing the work beats trying to memorize everything at once."),
        ],
        policy_areas=[
            ("What healthy momentum looks like", [("Learning curve", "It is normal to still be building confidence, context, and speed during the first 90 days."), ("Manager support", "Use regular check-ins to confirm priorities, progress, and what great work looks like in your role.")]),
            ("How to stay oriented", [("Use the portal again", "Come back to the sections that answer the questions you are running into most often."), ("Keep asking", "A short question asked early is usually better than a polished mistake discovered later.")]),
        ],
        actions=["Use your first 90 days to build rhythm, not pressure.", "Keep notes on recurring questions and bring them into check-ins.", "Return to the portal whenever you need a fast reset on expectations or support paths."],
        escalation=["Escalate blockers that keep repeating without getting resolved.", "Use your manager when priorities or expectations still feel unclear.", "Use HR when a people or policy issue outgrows routine team support."],
        acknowledgment_title="The next stretch feels navigable",
        acknowledgment_statement="I understand what the first 90 days are meant to feel like and how to keep using support instead of guessing.",
    ),
    build_section(
        section_id="final-review-and-acknowledgment",
        slug="final-review-and-acknowledgment",
        eyebrow="Finish Line",
        title="Final Review & Acknowledgment",
        summary="Wrap the launch path with the core takeaways, the right support map, and a clean manual finish.",
        purpose="This is the clearest finish line in AAP Start: a final pass through what matters most and a manual confirmation that you have completed the launch path.",
        focuses=["Core reminders", "Support map", "Manual finish"],
        essentials=[
            ("Use the handbook and portal as references", "You are not expected to memorize policy language. You are expected to know where to look and who to ask."),
            ("The finish line is manual on purpose", "Completion happens when you intentionally mark the section complete, not because you reached the bottom of a page."),
            ("Support still matters after onboarding", "Finishing launch onboarding should leave you oriented, not on your own."),
        ],
        policy_areas=[
            ("What this completion means", [("You reviewed the launch essentials", "The tracked path covers the shared onboarding topics employees should see first."), ("You know the right routes", "You should leave the launch path knowing where to go when work, support, or policy questions come up.")]),
            ("What happens next", [("Use the Resource Hub", "Keep the hub close for the live handbook file and support contacts."), ("Keep asking for context", "Completion is not the end of questions. It is the start of knowing where to ask them.")]),
        ],
        actions=["Take one last pass through anything that still feels fuzzy.", "Use the Resource Hub as your live reference shelf.", "Mark this section complete when you are ready to finish the launch path."],
        escalation=["Use HR when a real situation needs interpretation or sensitive handling.", "Use your manager when role-specific expectations still need clarity.", "Escalate unresolved questions instead of assuming completion means total certainty."],
        acknowledgment_title="Launch path complete",
        acknowledgment_statement="I have completed the launch onboarding path and I know where to go for support, clarification, and live reference materials.",
    ),
]

SUPPLEMENTAL_PAGES = [
    {
        "id": "where-you-make-an-impact",
        "slug": "where-you-make-an-impact",
        "eyebrow": "Coming Soon",
        "title": "Where You Make an Impact",
        "summary": "A launch-visible preview of how teams connect across AAP and where different roles create momentum.",
        "state": "coming_soon",
        "description": "This page stays visible at launch so employees can see where the experience is heading next, but it does not affect progress and it is intentionally not live yet.",
        "callout": "Coming Soon",
        "content": [
            {"title": "Why it is visible now", "body": "The page is part of the launch navigation so new hires can see that role context is planned, even though it is not part of the tracked path yet."},
            {"title": "What to expect later", "body": "A future version can connect company-wide onboarding to team and role impact without cluttering the launch experience."},
        ],
    },
    {
        "id": "resource-hub",
        "slug": "resource-hub",
        "eyebrow": "Reference Shelf",
        "title": "Resource Hub",
        "summary": "Live files, approved links, and support contacts that are useful after the first read-through too.",
        "state": "live",
        "description": "Resource Hub is outside tracked progress by design. It stays available as a clean shelf of live references instead of a pile of placeholders.",
        "resourceCategories": [
            {
                "id": "handbook-and-policies",
                "title": "Handbook & Policies",
                "description": "Reference materials that are live and ready to open.",
                "items": [item for item in [public_file_item("employee-handbook", "AAP Employee Handbook", "Launch-approved handbook PDF for reference.", "/resources/aap-employee-handbook-effective-5-1-24.pdf")] if item],
            },
            {
                "id": "benefits",
                "title": "Benefits",
                "description": "Live benefits support paths for questions that need real follow-through.",
                "items": [
                    {"id": "benefits-support-contact", "type": "contact", "title": "CBIZ Benefits", "description": "Benefits support contact once HR has routed the request.", "contactId": "cbiz-benefits"},
                    {"id": "benefits-module-link", "type": "link", "title": "Benefits, Pay & Time Away", "description": "Revisit the launch-safe overview inside the tracked path.", "href": "/modules/benefits-pay-and-time-away"},
                ],
            },
            {
                "id": "time-away",
                "title": "Time Away",
                "description": "Helpful launch-safe paths when time-away questions need the right lane.",
                "items": [
                    {"id": "time-away-module-link", "type": "link", "title": "Support, Leave & Employee Resources", "description": "Reopen the support and leave routing module.", "href": "/modules/support-leave-and-employee-resources"},
                    {"id": "hr-time-away-contact", "type": "contact", "title": "Nicole Thornton", "description": "Use HR for leave-routing, onboarding, and employee support questions.", "contactId": "nicole-thornton"},
                ],
            },
            {
                "id": "support-contacts",
                "title": "Support Contacts",
                "description": "People and programs to keep close when questions need a real person.",
                "items": [
                    {"id": "hr-manager-contact", "type": "contact", "title": "Nicole Thornton", "description": "Primary onboarding and employee-support contact.", "contactId": "nicole-thornton"},
                    {"id": "vp-hr-contact", "type": "contact", "title": "Brandy Hooper", "description": "Escalation support for sensitive or unresolved HR concerns.", "contactId": "brandy-hooper"},
                    {"id": "eap-contact", "type": "contact", "title": "LifeMatters", "description": "Confidential employee assistance support.", "contactId": "lifematters"},
                ],
            },
        ],
    },
]

SUPPLEMENTAL_PAGES = [
    {
        **page,
        "resourceCategories": [
            {**category, "items": [item for item in category.get("items", []) if item]}
            for category in page.get("resourceCategories", [])
            if any(category.get("items", []))
        ]
        if page["slug"] == "resource-hub"
        else page.get("resourceCategories"),
    }
    for page in SUPPLEMENTAL_PAGES
]

TRACKS: dict[str, dict[str, Any]] = {
    "default": {
        "id": "default",
        "name": "Launch onboarding",
        "supportContactId": "nicole-thornton",
        "section_overrides": {},
    }
}

TOOLKITS: list[dict[str, Any]] = []
TRACKED_SECTION_SLUGS = tuple(section["slug"] for section in SECTIONS)
SUPPLEMENTAL_PAGE_SLUGS = tuple(page["slug"] for page in SUPPLEMENTAL_PAGES)
ALL_PAGE_SLUGS = TRACKED_SECTION_SLUGS + SUPPLEMENTAL_PAGE_SLUGS

if len(SECTIONS) != 9:
    raise RuntimeError("Launch content must include exactly 9 tracked sections.")


def get_experience_content(track_id: str = "default") -> dict[str, Any]:
    track = TRACKS.get(track_id, TRACKS["default"])
    return {
        "brand": BRAND,
        "organization": ORGANIZATION,
        "dashboardStats": DASHBOARD_STATS,
        "contacts": CONTACTS,
        "sections": SECTIONS,
        "supplementalPages": SUPPLEMENTAL_PAGES,
        "toolkits": TOOLKITS,
        "track": track,
    }


def get_tracked_section_slugs() -> tuple[str, ...]:
    return TRACKED_SECTION_SLUGS


def get_all_page_slugs() -> tuple[str, ...]:
    return ALL_PAGE_SLUGS


def get_section_by_slug(slug: str) -> dict[str, Any] | None:
    return next((section for section in SECTIONS if section["slug"] == slug), None)


def get_supplemental_page_by_slug(slug: str) -> dict[str, Any] | None:
    return next((page for page in SUPPLEMENTAL_PAGES if page["slug"] == slug), None)


def get_toolkit_by_slug(slug: str) -> dict[str, Any] | None:
    return next((toolkit for toolkit in TOOLKITS if toolkit["slug"] == slug), None)

