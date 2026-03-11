from __future__ import annotations

from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[3]
FRONTEND_PUBLIC_DIR = ROOT_DIR / "frontend" / "public"


def manual_acknowledgment(title: str, statement: str) -> dict[str, Any]:
    return {"mode": "manual", "title": title, "statement": statement, "items": []}


def build_knowledge_check(
    *,
    intro: str,
    questions: list[tuple[str, str, list[str], int]],
    passing_percent: float = 1.0,
) -> dict[str, Any]:
    return {
        "title": "Knowledge Check",
        "intro": intro,
        "passingPercent": passing_percent,
        "questions": [
            {
                "id": question_id,
                "prompt": prompt,
                "options": options,
                "correctOptionIndex": correct_option_index,
            }
            for question_id, prompt, options, correct_option_index in questions
        ],
    }


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
    knowledge_check: dict[str, Any],
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
        "knowledgeCheck": knowledge_check,
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
    {"id": "lifematters", "name": "LifeMatters", "role": "Employee Assistance Program", "email": "", "phone": "800-634-6433", "note": "Confidential employee assistance support available from day one."},
]

SECTIONS = [
    build_section(
        section_id="welcome-to-aap",
        slug="welcome-to-aap",
        eyebrow="Start Here",
        title="Welcome to AAP",
        summary="You\u2019re joining a company that supports more than 2,000 independent and community pharmacies, and every role helps that mission move forward. Whether your work is operational, administrative, customer-facing, or behind the scenes, it plays a part in helping member pharmacies stay strong, supported, and competitive.",
        purpose="",
        focuses=["Who AAP supports", "What AAP Start is for", "Where questions go"],
        essentials=[
            ("What AAP Start Is", "AAP Start is your onboarding guide. It is designed to make your first stretch at AAP clearer, easier to follow, and easier to complete by organizing key information, training, and next steps in one place.\n\nAAP\u2019s CEO, Jon Copeland, puts it simply: every employee contributes directly to the company\u2019s growth and success. The goal of this experience is to help you understand how AAP works, what\u2019s expected of you, where to go for help, and what to expect as you get settled in."),
            ("Who AAP Is", "American Associated Pharmacies, or AAP, is a member-owned cooperative that supports independent and community pharmacies. AAP was formed in 2009 through the joining of two pharmacy organizations, and API continues to operate as AAP\u2019s warehouse and distribution arm."),
            ("Core Values", "The way we work matters just as much as the work itself. \n\nAt AAP, we lead with customer focus, act with integrity, treat people with respect, aim for excellence, and take ownership of what we do."),
            ("Mission and Vision", "Mission: Provide support and customized solutions for independent and community pharmacies to enhance profitability, streamline operations, and improve the quality of patient care.\n\nVision: Help independent pharmacies thrive in a competitive healthcare market."),
        ],
        policy_areas=[
            ("Who AAP is", [
                ("What AAP supports", "American Associated Pharmacies, or AAP, is a member-owned cooperative that supports independent and community pharmacies."),
                ("Where API fits", "AAP was formed in 2009 through the joining of two pharmacy organizations. API continues to operate as AAP\u2019s warehouse and distribution arm."),
                ("Where AAP works", "AAP operates from locations in Scottsboro, Alabama and Memphis, Tennessee. Your offer letter and orientation will confirm which site applies to your role."),
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
        knowledge_check=build_knowledge_check(
            intro="Complete this required check before you move into the acknowledgment step.",
            questions=[
                ("welcome-purpose", "Which description best matches what AAP Start is for?", ["A place to memorize every policy on day one.", "A guided launch path that orients you, shows where to look, and helps you know where questions go.", "A role-specific toolkit that replaces supervisor training."], 1),
                ("welcome-support", "Who is the primary onboarding and employee-support contact named in this module?", ["Nicole Thornton, HR Manager", "CBIZ Benefits", "LifeMatters"], 0),
            ],
        ),
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
        summary="See how respect, direct communication, and confidentiality shape the way people work together at AAP.",
        purpose="This chapter keeps culture practical: how people speak to each other, protect trust, and handle sensitive situations before they become bigger problems.",
        focuses=["Values in practice", "Respectful conduct", "Confidentiality and trust"],
        essentials=[
            ("Values should be visible", "Customer focus, integrity, respect, excellence, and ownership are not slogans. They set the standard for how people communicate, make decisions, and treat each other every day."),
            ("Respect is a work standard", "Professional conduct means clear and honest communication, responsible judgment, and raising issues through the right channels instead of letting them build."),
            ("Confidentiality protects everyone", "Sensitive information \u2014 personnel records, medical documentation, benefits details, and proprietary business data \u2014 stays with the people who need it to do their jobs. Sharing it casually or carelessly can cause real harm."),
        ],
        policy_areas=[
            ("How people work together", [
                ("Communication", "Be direct, respectful, and professional. When something is unclear, ask. When something needs to be said, say it honestly instead of avoiding the conversation."),
                ("Workplace behavior", "Harassment, retaliation, threats, discrimination, and other unsafe conduct are not gray areas. These are escalation issues that should be raised immediately."),
                ("Honesty over guessing", "If you are not sure about an answer, say so and follow up. Employees and teammates appreciate honesty, even when the answer is 'I need to check on that and get back to you.'"),
            ]),
            ("Protecting confidentiality and trust", [
                ("Need-to-know handling", "Sensitive information \u2014 personnel records, medical details, benefits data, and proprietary business information \u2014 stays with the people who need it to do their jobs. Before sharing anything sensitive, confirm it is going to the right person for the right reason."),
                ("Email and digital security", "Verify the recipient before sending any email with sensitive content. Do not forward work materials to personal email addresses or store company data on personal devices. Company systems are for company business, and usage may be monitored."),
                ("Physical documents", "Printed materials with sensitive information should be retrieved immediately from printers, never left unattended in shared spaces, and shredded when no longer needed."),
                ("Reporting privacy concerns", "If you suspect a privacy mistake \u2014 a misdirected email, unauthorized access, or misplaced documents \u2014 report it to HR and IT right away. Early reporting prevents small issues from becoming serious ones."),
            ]),
        ],
        actions=[
            "Pause before forwarding or sharing sensitive information \u2014 confirm it is going to the right person.",
            "Use respectful directness when something needs to be addressed.",
            "Raise concerns early, while they are still manageable.",
            "If you are unsure how to handle a sensitive question, say so honestly and follow up through the right channel.",
        ],
        escalation=[
            "Escalate harassment, retaliation, violence, or discrimination concerns immediately.",
            "Report suspected privacy breaches or unauthorized access to HR and IT right away.",
            "Use HR when a people issue becomes sensitive, personal, or employee-specific.",
        ],
        knowledge_check=build_knowledge_check(
            intro="This required check confirms the practical culture habits from this chapter before you acknowledge it.",
            questions=[
                ("culture-directness", "When you do not know the answer to a sensitive question, what is the best response?", ["Give your best guess so the conversation keeps moving.", "Say you need to check and follow up through the right channel.", "Share the question with anyone nearby until someone answers it."], 1),
                ("culture-privacy", "What should you do if you suspect a privacy breach or unauthorized access?", ["Wait to see if it becomes a larger problem.", "Report it to HR and IT right away.", "Mention it casually to a teammate and move on."], 1),
            ],
        ),
        acknowledgment_title="Leave with this",
        acknowledgment_statement="At AAP, strong culture is visible in respectful communication, good judgment, and careful handling of sensitive information.",
        chapter_intros=[
            "The standard is not abstract. It shows up in ordinary moments: how you answer, how you correct, how you raise concerns, and how carefully you handle information other people trust you with.",
            "The clearest test is not what you know in theory. It is what you do when a conversation gets awkward, when a situation crosses a line, or when information should travel no farther.",
            "Leave this chapter with a short list of habits you can use right away and a clear sense of which situations should be escalated instead of absorbed.",
        ],
    ),
    build_section(
        section_id="tools-and-systems",
        slug="tools-and-systems",
        eyebrow="Systems",
        title="Tools & Systems",
        summary="Get familiar with the core systems and the habits that keep access, records, and work moving smoothly.",
        purpose="You do not need to master every tool on day one, but you should know the key systems, the right names, and the rules around using them responsibly.",
        focuses=["Core systems", "Access basics", "Password security"],
        essentials=[
            ("Systems have owners", "Each system your team uses has an owner and a support path. Use approved company tools for company work, and reach out to the right contact when something does not look right."),
            ("Protect access from day one", "Passwords belong only in the company\u2019s approved password manager \u2014 never in email, chat messages, or shared documents. Treat login credentials as sensitive from your first day."),
            ("Verify your access early", "During your first week, confirm you can log into the systems your role requires. If something is missing or not working, flag it right away instead of waiting until it blocks you."),
        ],
        policy_areas=[
            ("Working with systems", [
                ("Use approved tools", "Store work in approved systems and avoid moving company data into personal tools, personal email, or side channels."),
                ("Ask early", "When something looks off in a system or a workflow does not match what you expected, get help instead of building a workaround."),
            ]),
            ("Getting oriented", [
                ("Your team will guide you", "Your supervisor and trainer will walk you through the specific systems and tools your role uses. You are not expected to learn everything from this module alone."),
                ("Support routing", "For day-to-day system questions, start with your manager or trainer. For access issues or IT-related problems, contact your site\u2019s IT team. IT generally prefers Teams for support requests."),
            ]),
        ],
        actions=[
            "Learn the names of the core systems you will use in your role.",
            "Keep passwords in the approved password manager and nowhere else.",
            "Flag access issues early so they do not slow down your first week.",
        ],
        escalation=[
            "Escalate access problems that prevent core work from moving forward.",
            "Escalate data-handling concerns or suspected misdirected information to HR.",
            "Ask for help if a system instruction conflicts with policy or team guidance.",
        ],
        knowledge_check=build_knowledge_check(
            intro="Pass this required check before you acknowledge the systems basics for this module.",
            questions=[
                ("systems-passwords", "Where should work passwords be stored?", ["In your personal notes app so you can reach them anywhere.", "Only in the approved company password manager.", "In a shared team spreadsheet so backup coverage is easy."], 1),
                ("systems-access", "What should you do if a key system is not working during your first week?", ["Build a workaround and ask about it later.", "Flag it early through the right support path.", "Share your credentials with a teammate who has access."], 1),
            ],
        ),
        acknowledgment_title="Systems basics are clear",
        acknowledgment_statement="I understand the basic expectations around system access, password security, and where to go when something needs help.",
    ),
    build_section(
        section_id="how-work-works",
        slug="how-work-works",
        eyebrow="Work Basics",
        title="How Work Works",
        summary="Understand the communication, ownership, and follow-through habits that reflect what makes AAP a strong and respectful place to work.",
        purpose="This module is about the culture behind the work. AAP runs on direct communication, real ownership, and people who follow through on what they say they will do. When these habits show up consistently, teams work well and people feel confident in the work around them.",
        focuses=["Culture and values in practice", "Ownership and follow-through", "Open communication"],
        essentials=[
            ("Clarity beats guessing", "If something about a process, a priority, or an expectation is unclear, ask. A short question asked early is almost always better than a confident mistake discovered later."),
            ("Follow-through builds trust", "When you commit to a timeline or a follow-up, keep it. If circumstances change, communicate that before the deadline passes. Reliable follow-through is one of the simplest ways to earn trust."),
            ("Know your lane and your neighbors", "Every role has ownership boundaries. Your manager handles day-to-day direction and priorities. HR handles people, policy, pay, and sensitive issues. IT handles systems and access. Knowing who owns what keeps questions moving to the right place."),
        ],
        policy_areas=[
            ("Communication and accountability", [
                ("Be direct and professional", "Clear, honest, and respectful communication reduces confusion and prevents rework. When something needs to be said \u2014 a question, a concern, a correction \u2014 say it directly and professionally."),
                ("Document important interactions", "When a conversation involves a decision, a commitment, or a follow-up, capture the key details: what was discussed, what was agreed, and when the next step happens. This protects everyone involved."),
                ("Follow up by every committed date", "If you told someone you would get back to them by a specific time, do it. If the timeline shifts, let them know before the deadline passes \u2014 not after."),
            ]),
            ("What makes AAP work", [
                ("Open door culture", "AAP values an open and approachable work environment. If you have a question, a concern, or an idea, you are encouraged to raise it with your supervisor or with HR. You should never feel like you need to wait for a formal moment to speak up."),
                ("Ownership matters", "AAP\u2019s values are customer focus, integrity, respect, excellence, and ownership. These are not just words on a wall \u2014 they shape how people treat each other, how decisions get made, and how problems get solved. When something matters, move it forward instead of waiting for someone else to catch it."),
                ("Keep your records current", "When personal details change \u2014 address, emergency contact, tax information, or anything that affects benefits or payroll \u2014 update HR promptly so your records stay accurate."),
            ]),
        ],
        actions=[
            "Communicate directly and professionally \u2014 say what needs to be said.",
            "Document decisions and commitments so nothing falls through the cracks.",
            "Use your manager for day-to-day questions and HR for policy, pay, or people issues.",
            "Return to AAP Start when you need a refresher on expectations or support paths.",
        ],
        escalation=[
            "Use HR when a question involves pay, policy, benefits, or anything employee-specific.",
            "Escalate conflicting instructions that could affect compliance or fairness.",
            "Raise recurring blockers with your manager instead of working around them indefinitely.",
        ],
        knowledge_check=build_knowledge_check(
            intro="Use this required check to confirm the work habits and support lanes from the chapter.",
            questions=[
                ("work-follow-up", "If a deadline or follow-up you promised is going to change, what should you do?", ["Wait until the original deadline passes, then explain what happened.", "Communicate the change before the deadline passes.", "Assume people will understand if the work is important enough."], 1),
                ("work-hr-lane", "Which team owns people, policy, pay, and other sensitive employee issues?", ["HR", "IT", "Any experienced coworker"], 0),
            ],
        ),
        acknowledgment_title="Day-to-day expectations make sense",
        acknowledgment_statement="I understand the communication, follow-through, and ownership expectations that keep work moving well at AAP.",
    ),
    build_section(
        section_id="benefits-pay-and-time-away",
        slug="benefits-pay-and-time-away",
        eyebrow="Benefits",
        title="Benefits, Pay & Time Away",
        summary="Understand the practical basics of benefits timing, the attendance point system, paid time off, and where to go when pay or benefits questions come up.",
        purpose="This section gives you the essentials \u2014 the timing, the rules that affect you most, and the right paths to follow when something needs attention. For detailed plan documents and accrual schedules, the Resource Hub and HR are your best references.",
        focuses=["Benefits timing", "Attendance system", "Time-away basics"],
        essentials=[
            ("Benefits open in stages", "Some support \u2014 like the Employee Assistance Program and LinkedIn Learning \u2014 is available from day one. Others, like PTO, medical, dental, and 401(k), depend on your hire date, employment status, and eligibility milestones. HR can walk you through your specific timeline."),
            ("Attendance is tracked through a point system", "AAP uses a point-based attendance system. Not every workplace uses one, so this may be new to you \u2014 it simply means attendance is tracked through assigned points rather than written warnings or manager discretion. Understanding how the system works early is one of the easiest ways to stay in good standing."),
            ("Time away has different paths", "Planned vacation, personal time, unexpected absences, and protected leave each follow different rules and different request paths. Knowing which one applies \u2014 and when to involve HR \u2014 keeps things from getting complicated."),
        ],
        policy_areas=[
            ("Benefits and pay basics", [
                ("Eligibility milestones", "Benefits become available in stages. PTO eligibility begins after 60 days. Medical, dental, vision, and 401(k) enrollment opens on the first of the month after 60 days of full-time employment. AAP matches 401(k) contributions \u2014 HR can provide the current details on matching."),
                ("Pay questions go to HR", "If something about your paycheck looks off \u2014 hours, deductions, overtime, or a bonus \u2014 bring it to HR. Pay questions should always go through the proper channel instead of being guessed at or handled informally."),
            ]),
            ("Attendance point system", [
                ("How it works", "Points are assigned based on the type of absence or tardiness \u2014 a brief tardiness carries fewer points than a full-shift absence, and an unreported absence carries the most. Points accumulate over a rolling 12-month window, and higher totals lead to progressive corrective steps."),
                ("How points come off", "There are two paths. First, points naturally roll off after 12 months \u2014 once a point is 12 months old, it drops from your record automatically. Second, there is an accelerated path through perfect attendance: two consecutive months of perfect attendance removes one point early, and three consecutive months of perfect attendance earns a $75 bonus. Consistent attendance is recognized and rewarded."),
                ("What does not count", "Certain absences are excluded from the point system entirely, including FMLA leave, pre-approved vacation, bereavement, jury duty, and company holidays."),
                ("Two-day rule", "Two consecutive workdays of absence without any call-in notification is treated as a voluntary resignation under company policy. If you cannot report to work, always notify your supervisor as early as possible."),
            ]),
            ("Time away at a glance", [
                ("Vacation", "Full-time employees begin accruing vacation after 60 days, and accrual rates increase with tenure. Vacation must be taken in two-hour minimum increments. Requests for planned time off should be submitted by the end of the day before the time is needed. Unused vacation is paid out at separation."),
                ("Personal time", "Personal leave follows a separate accrual schedule, must be taken in one-hour minimum increments, and does not carry over from year to year. It is not paid out at separation."),
                ("Holidays", "AAP observes several standard holidays throughout the year. When a holiday falls on a weekend, it is observed on the nearest weekday. Employees required to work a holiday receive a floating holiday to use within 90 days."),
                ("FMLA", "AAP offers Family and Medical Leave Act protection to eligible employees who have worked for the company for at least one year. If you think FMLA may apply to your situation, contact HR directly."),
            ]),
        ],
        actions=[
            "Understand your benefits eligibility timeline \u2014 HR can confirm the specifics for your hire date and status.",
            "Learn how the attendance point system works and what keeps your record in good standing.",
            "Submit planned time-off requests on time and notify your supervisor as early as possible for unexpected absences.",
            "Bring pay or benefits questions to HR instead of trying to sort them out on your own.",
        ],
        escalation=[
            "Escalate pay discrepancies or unexpected deductions to HR.",
            "Escalate time-away questions that involve medical situations, leave certification, or anything beyond routine PTO.",
            "Use HR whenever benefits timing, eligibility, or classification seems inconsistent with what you expected.",
        ],
        knowledge_check=build_knowledge_check(
            intro="This required check keeps the basics practical before you move into the acknowledgment.",
            questions=[
                ("benefits-attendance", "What does two consecutive months of perfect attendance do under this module's attendance overview?", ["It removes one point early.", "It adds a floating holiday.", "It resets your entire attendance record."], 0),
                ("benefits-leave", "If a time-away question involves a medical situation or FMLA, what is the right move?", ["Wait for your next annual review to bring it up.", "Move it to HR directly.", "Ask a coworker what usually happens."], 1),
            ],
        ),
        acknowledgment_title="Benefits, pay, and attendance basics understood",
        acknowledgment_statement="I understand the basics of benefits timing, the attendance point system, time-away expectations, and when HR needs to be involved.",
    ),
    build_section(
        section_id="support-leave-and-employee-resources",
        slug="support-leave-and-employee-resources",
        eyebrow="Support",
        title="Support, Leave & Employee Resources",
        summary="Know where support comes from, how urgency shapes routing, and what resources are available when a question goes beyond routine.",
        purpose="This module keeps leave and support guidance practical: know the right lane, know when not to improvise, and know who can actually help.",
        focuses=["Leave routing", "Support resources", "Escalation paths"],
        essentials=[
            ("Leave questions can turn sensitive fast", "Medical conditions, accommodations, and employee-specific leave situations should move to HR early. These are not questions to handle casually or improvise answers for."),
            ("Urgency determines the path", "Not every question follows the same route. Pay discrepancies, safety concerns, harassment, and medical or leave issues need immediate attention. Workplace conflicts should be raised the same day. Routine policy questions and PTO disputes can usually wait until the next business day."),
            ("Help exists before things get complicated", "Support contacts, the Employee Assistance Program, and HR are all available to help before strain turns into a bigger problem. LifeMatters is confidential and available from day one."),
        ],
        policy_areas=[
            ("Leave and sensitive situations", [
                ("Medical and leave questions go to HR", "If a question involves a medical condition, a leave need, or a workplace accommodation, move it to HR directly. Do not try to interpret policy or promise an outcome \u2014 let the right process determine what applies."),
                ("Use careful language", "When someone raises a sensitive topic, listen and acknowledge it. Do not speculate about what will happen or what they might be entitled to. Careful language protects everyone."),
            ]),
            ("Support options and routing", [
                ("HR support", "HR can help with onboarding questions, benefits timing, employee records, pay concerns, and sensitive workplace issues. For most employee-related questions beyond day-to-day work, HR is the right destination."),
                ("Employee Assistance Program", "LifeMatters provides confidential support from day one \u2014 counseling, financial guidance, and personal assistance. You do not need permission or a referral to use it."),
                ("IT support", "For system access, equipment, or technical issues, contact your site\u2019s IT team. IT generally prefers Teams for support requests."),
                ("Your supervisor", "For day-to-day work questions, scheduling, priorities, and team-specific guidance, your supervisor is the natural first point of contact."),
            ]),
        ],
        actions=[
            "Use the right support route as soon as a question becomes personal or sensitive.",
            "Keep leave questions factual and move them to HR early.",
            "Know that LifeMatters is available from day one for confidential personal support.",
            "When in doubt about where a question belongs, ask HR \u2014 they will route it correctly.",
        ],
        escalation=[
            "Escalate medical, accommodation, or leave questions to HR immediately.",
            "Escalate pay or safety concerns through the proper channel without delay.",
            "Use HR when a situation involves privacy, fairness, or interpretation of policy.",
        ],
        knowledge_check=build_knowledge_check(
            intro="Pass this required check to confirm where support should go before you acknowledge the module.",
            questions=[
                ("support-hr", "Where should medical, leave, and accommodation questions go?", ["To HR directly", "To the Resource Hub only", "To any teammate who has handled it before"], 0),
                ("support-eap", "How can employees use LifeMatters?", ["Only after HR approval", "Only after 90 days", "Confidentially from day one without a referral"], 2),
            ],
        ),
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
        knowledge_check=build_knowledge_check(
            intro="Finish this required check before you acknowledge the shared safety expectations.",
            questions=[
                ("safety-urgent", "If something feels unsafe or threatening, what should you do?", ["Wait for a calmer time to mention it.", "Escalate it immediately.", "Keep working unless someone else stops."], 1),
                ("safety-reporting", "Which answer reflects the module's safety standard?", ["Near misses and hazards should be reported promptly.", "Only injuries that require medical treatment need to be reported.", "Minor hazards are fine if you can work around them."], 0),
            ],
        ),
        acknowledgment_title="Safety expectations are clear",
        acknowledgment_statement="I understand the shared safety expectations and the importance of speaking up quickly when something does not look right.",
    ),
    build_section(
        section_id="your-first-90-days",
        slug="your-first-90-days",
        eyebrow="Looking Ahead",
        title="Your First 90 Days",
        summary="What to expect in your first days, your first week, and the first 90 days \u2014 and why building steady habits matters more than memorizing everything at once.",
        purpose="The first 90 days are about getting oriented, building rhythm, and knowing how to ask for what you need. The pace depends on your role and team \u2014 this section covers the shared starting points that apply to everyone.",
        focuses=["Getting started", "Building confidence", "Feedback loops"],
        essentials=[
            ("Day one is about orientation, not mastery", "Your first day will typically include an HR orientation, a building tour, a badge photo, and introductions to your supervisor and trainer. The goal is to get settled and to know where things are \u2014 not to learn everything."),
            ("Your first week is for shadowing and settling in", "During your first week, expect to shadow your trainer, learn the basics of your role, and begin building the routines that will carry you through the first few months. It is normal to have a lot of questions."),
            ("Confidence comes from repetition", "The first 90 days are for practicing the work, asking good questions, and returning to resources like AAP Start when you need a refresher. Steady momentum beats memorization."),
        ],
        policy_areas=[
            ("What healthy momentum looks like", [
                ("Learning curve", "It is normal to still be building confidence, context, and speed during the first 90 days. Your manager and trainer expect that and will support you through it."),
                ("The introductory period", "The first 60 days are considered the introductory period. During this time, attendance expectations are especially important, and some benefits \u2014 like PTO accrual \u2014 have not started yet."),
                ("Detailed plans are role-specific", "A true 30/60/90-day development plan depends on your department and role. Your supervisor or trainer will guide you through the specific milestones and expectations that apply to your position."),
            ]),
            ("How to stay oriented", [
                ("Use the portal again", "Come back to AAP Start whenever you need a fast refresher on policies, support paths, or expectations. It stays available after onboarding."),
                ("Keep asking", "A short question asked early is almost always better than a polished mistake discovered later. Use your supervisor, your trainer, and HR as real resources \u2014 not last resorts."),
            ]),
        ],
        actions=[
            "Use your first 90 days to build rhythm, not pressure.",
            "Keep notes on recurring questions and bring them into check-ins with your supervisor.",
            "Return to AAP Start whenever you need a refresher.",
            "Ask for help early \u2014 it is always better than guessing.",
        ],
        escalation=[
            "Escalate blockers that keep repeating without getting resolved.",
            "Use your manager when priorities or expectations still feel unclear.",
            "Use HR when a people or policy issue outgrows routine team support.",
        ],
        knowledge_check=build_knowledge_check(
            intro="Use this required check to confirm the practical expectations for your first stretch at AAP.",
            questions=[
                ("first-90-days-day-one", "What is day one mainly for according to this module?", ["Orientation and getting settled", "Independent mastery of your full role", "Completing every system training in one day"], 0),
                ("first-90-days-questions", "What is the better move when something still feels unclear in your first 90 days?", ["Stay quiet until you have a perfect question.", "Ask early and use your support routes.", "Wait until onboarding is fully finished."], 1),
            ],
        ),
        acknowledgment_title="The next stretch feels navigable",
        acknowledgment_statement="I understand what the first days and weeks look like, what the introductory period means, and how to keep using support instead of guessing.",
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
        knowledge_check=build_knowledge_check(
            intro="Complete this required final check before you finish the tracked launch path.",
            questions=[
                ("final-review-reference", "What does successful launch completion mean in this module?", ["You memorized every policy detail.", "You know the essentials, where to look, and who to ask.", "You should not need support anymore."], 1),
                ("final-review-hub", "How should you use the Resource Hub after onboarding?", ["As a live reference shelf for files, contacts, and refreshers.", "Only if your manager gives written approval.", "Only after all future modules are released."], 0),
            ],
        ),
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

