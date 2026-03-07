from __future__ import annotations

from typing import Any

ORGANIZATION = {
    "name": "AAP/API",
    "headline": "A guided onboarding flow built around what new employees actually need to know first.",
    "tagline": "Clear structure, real policy guidance, and less noise.",
    "mission": "AAP provides support and customized solutions for independent community pharmacies to enhance profitability, streamline operations, and improve the quality of patient care.",
    "vision": "Helping independent pharmacies thrive in a competitive healthcare market.",
    "story": "American Associated Pharmacies is a national cooperative of more than 2,000 independent pharmacies. API operates as AAP's distribution arm, helping member pharmacies stay competitive with inventory access, operational support, and practical tools.",
    "values": [
        {"name": "Customer Focus", "body": "Strong internal teamwork supports strong external service."},
        {"name": "Integrity", "body": "Act honestly and consistently so trust stays intact."},
        {"name": "Respect", "body": "Treat people with dignity and communicate directly."},
        {"name": "Excellence", "body": "Aim for high quality and keep improving the work."},
        {"name": "Ownership", "body": "Take responsibility early instead of waiting to be asked."},
    ],
}

DASHBOARD_STATS = [
    {"label": "Core path", "value": "7 sections", "detail": "The universal onboarding flow for every new employee."},
    {"label": "Intro period", "value": "60 days", "detail": "The first 60 calendar days are the introductory period."},
    {"label": "Benefits timing", "value": "30-day window", "detail": "Most life-event changes must be reported to HR within 30 days."},
]

CONTACTS = [
    {"name": "Brandy Hooper", "role": "VP of Human Resources", "email": "brandy.hooper@rxaap.com", "phone": "256-574-7526", "note": "Escalation point for unresolved HR concerns and harassment reporting."},
    {"name": "Nicole Thornton", "role": "HR Administrator", "email": "nicole.thornton@apirx.com", "phone": "256-574-7528", "note": "Primary onboarding, benefits, and employee-record support contact."},
    {"name": "CBIZ Benefits", "role": "Benefits Support", "email": "Melissa.street@cbiz.com", "phone": "844.200.CBIZ (2249)", "note": "Benefits support after HR has routed the request."},
    {"name": "LifeMatters", "role": "Employee Assistance Program", "email": "www.empathia.com", "phone": "800-634-6433", "note": "Confidential employee assistance resource available from day one."},
]

SECTIONS = [
    {
        "id": "welcome-to-aap-api",
        "slug": "welcome-to-aap-api",
        "eyebrow": "Start Here",
        "title": "Welcome to AAP/API",
        "summary": "Start with the company story, the reason the organization exists, and what day-one onboarding is meant to set up.",
        "estimatedMinutes": 9,
        "purpose": "Understand who AAP/API serves, why the business exists, and how the first stretch of onboarding should help you build confidence quickly.",
        "focuses": ["Company story", "Mission and values", "First 60 days"],
        "essentials": [
            {"title": "Who AAP/API is", "body": "AAP is a national cooperative supporting more than 2,000 independent pharmacies, and API operates as the warehouse and distribution arm that helps those pharmacies stay competitive."},
            {"title": "What the company is aiming for", "body": "The mission is to support independent community pharmacies with solutions that improve profitability, streamline operations, and improve patient care."},
            {"title": "How culture is supposed to work", "body": "Customer focus, integrity, respect, excellence, and ownership are meant to show up in daily behavior, not just in orientation copy."},
        ],
        "policyAreas": [
            {
                "title": "Company context",
                "items": [
                    {"label": "Who we serve", "body": "Independent community pharmacies across the country rely on AAP/API for programs, operational support, and distribution."},
                    {"label": "Why your role matters", "body": "Even roles that are not customer-facing affect service quality, team reliability, and pharmacy support outcomes."},
                ],
            },
            {
                "title": "What the handbook is for",
                "items": [
                    {"label": "Scope", "body": "The handbook applies to employees in the service of both American Associated Pharmacies and Associated Pharmacies, Inc."},
                    {"label": "How to use it", "body": "Use it as the baseline guide for policies, benefits, and working conditions, then go to HR when a specific situation needs interpretation."},
                    {"label": "Policy changes", "body": "The company may revise handbook policies through official notices over time."},
                ],
            },
            {
                "title": "What this first phase should do",
                "items": [
                    {"label": "Orientation goal", "body": "The first part of onboarding should help you understand the business, your support map, and the standards you are responsible for following."},
                    {"label": "Introductory period", "body": "New and rehired employees work on an introductory basis for the first 60 calendar days after hire."},
                ],
            },
        ],
        "actions": [
            "Connect your role to the customer and team impact it supports.",
            "Use the section sequence to build context before diving into detailed policy questions.",
            "Keep HR in the loop when a handbook question turns specific or sensitive.",
        ],
        "escalation": [
            "Use HR when the handbook does not fully answer a policy question.",
            "Use your supervisor for role-specific expectations and first-line context.",
            "Escalate sensitive employee-specific questions instead of guessing.",
        ],
        "acknowledgment": {
            "title": "Orientation checkpoint",
            "statement": "I understand what AAP/API does, what the company is trying to accomplish, and where to go when a question becomes policy-specific.",
            "items": [
                "I can explain AAP/API in plain language.",
                "I know the five company values.",
                "I know HR is the right path for policy interpretation and sensitive issues.",
            ],
        },
    },
    {
        "id": "working-at-aap-api",
        "slug": "working-at-aap-api",
        "eyebrow": "Employment Basics",
        "title": "Working at AAP/API",
        "summary": "Cover the employment framework, employee records, equal-opportunity expectations, and the rules that shape day-to-day employment.",
        "estimatedMinutes": 11,
        "purpose": "Understand how employment status works, what the company expects around fairness and conduct, and how employee information is handled.",
        "focuses": ["Employment framework", "Employee records", "Fair workplace rules"],
        "essentials": [
            {"title": "Employment is at-will", "body": "The handbook explains that either the employee or the company may end the employment relationship at any time, subject to applicable law."},
            {"title": "Employment decisions are merit-based", "body": "AAP states that hiring and employment decisions are based on merit, qualifications, and abilities without unlawful discrimination."},
            {"title": "Records matter", "body": "Personnel files are company property, and employees should keep their contact and dependent information current through HR."},
        ],
        "policyAreas": [
            {
                "title": "Employment categories and status",
                "items": [
                    {"label": "Exempt and nonexempt", "body": "Employees are designated as exempt or nonexempt for wage-and-hour purposes."},
                    {"label": "Regular full-time", "body": "Regular full-time employees are generally scheduled at 30 or more hours per week and are the group that typically qualifies for the core benefits package."},
                    {"label": "Part-time, temporary, introductory", "body": "Part-time, temporary, and introductory categories carry different expectations and benefit eligibility rules."},
                ],
            },
            {
                "title": "Records and employee data",
                "items": [
                    {"label": "Personnel files", "body": "Employees may review their own personnel file only through HR, with reasonable notice, at company offices and with an appointed representative present."},
                    {"label": "Data changes", "body": "Address, phone number, emergency contacts, dependents, and similar personnel details should be updated promptly through HR."},
                    {"label": "Introductory period", "body": "The initial introductory period lasts 60 calendar days and may be extended when significant absences affect evaluation."},
                ],
            },
            {
                "title": "Workplace standards tied to employment",
                "items": [
                    {"label": "Business ethics", "body": "Employees are expected to comply with law and avoid dishonest, illegal, or unethical conduct."},
                    {"label": "Outside employment", "body": "Outside work cannot interfere with AAP/API performance or create an adverse conflict of interest."},
                    {"label": "Internal growth", "body": "AAP may post job openings internally to support movement and development when appropriate."},
                ],
            },
        ],
        "actions": [
            "Confirm your employment classification and ask if it is unclear.",
            "Keep your records current with HR.",
            "Raise work concerns through the supervisor or HR route instead of letting them drift.",
        ],
        "escalation": [
            "Report discrimination or retaliation concerns promptly.",
            "Use HR for personnel-file access and employee-data corrections.",
            "Ask HR if outside employment or a conflict issue needs review.",
        ],
        "acknowledgment": {
            "title": "Employment basics checkpoint",
            "statement": "I understand the employment framework, how employee records are handled, and when HR must be involved.",
            "items": [
                "I know the introductory period is 60 calendar days.",
                "I know how personnel-file access works.",
                "I know to route employment-data changes through HR.",
            ],
        },
    },
    {
        "id": "attendance-timekeeping-and-pto",
        "slug": "attendance-timekeeping-and-pto",
        "eyebrow": "Attendance and Time",
        "title": "Attendance, Timekeeping, and PTO",
        "summary": "Bring attendance rules, timekeeping expectations, overtime, PTO, and holiday handling into one cleaner section.",
        "estimatedMinutes": 14,
        "purpose": "Know how work time is recorded, how attendance points work, and how to request time away without creating avoidable issues.",
        "focuses": ["Timekeeping accuracy", "Attendance points", "PTO and holiday rules"],
        "essentials": [
            {"title": "Timekeeping has to be accurate", "body": "Hours worked should be recorded accurately, overtime must be approved in advance, and paid time off does not count as hours worked for overtime calculations."},
            {"title": "PTO follows eligibility and accrual rules", "body": "Vacation and personal leave cannot be taken before they are accrued, and planned requests should be submitted in BambooHR with enough time for staffing decisions."},
            {"title": "Attendance is measured", "body": "AAP uses a no-fault attendance point program for nonexempt employees, with corrective action beginning at five points within a consecutive 12-month period."},
        ],
        "policyAreas": [
            {
                "title": "Timekeeping, schedules, and overtime",
                "items": [
                    {"label": "Timekeeping", "body": "Record time accurately and follow department scheduling expectations."},
                    {"label": "Rest periods", "body": "The policy playbook states that full-time nonexempt employees receive two paid 15-minute rest periods each workday."},
                    {"label": "Overtime", "body": "Overtime must be approved before it is worked and is based on actual hours worked, not paid leave."},
                ],
            },
            {
                "title": "PTO and holidays",
                "items": [
                    {"label": "Vacation", "body": "Regular full-time employees become eligible for vacation after 60 days of full-time service, and vacation accrues weekly based on length of service."},
                    {"label": "Personal leave", "body": "Personal leave has a 60-day waiting period, may be used in one-hour increments, and generally does not roll over or pay out at termination unless required by law."},
                    {"label": "Holiday rules", "body": "If you are required to work a designated or observed holiday, the department coordinates a floating holiday to be used within 90 days."},
                ],
            },
            {
                "title": "Attendance points and absence handling",
                "items": [
                    {"label": "Point values", "body": "Tardy under five minutes is a grace period, less than half-shift tardy or early leave is 0.5 points, half-shift or more is 1 point, and a no-report absence is 1.5 points."},
                    {"label": "Corrective steps", "body": "Five points trigger coaching, six a verbal warning, seven a written warning, and eight may result in termination."},
                    {"label": "Call-in expectations", "body": "For unexpected personal leave, notify your supervisor before your scheduled start time whenever possible and on each additional day of absence."},
                ],
            },
        ],
        "actions": [
            "Record hours worked accurately and ask before working overtime.",
            "Submit planned PTO no later than 5:00 PM the day before time off is needed.",
            "Call in quickly for unexpected absences instead of waiting for the shift to start.",
        ],
        "escalation": [
            "Use HR when time-off balances or attendance points are disputed.",
            "Escalate operational exceptions instead of making side agreements about PTO.",
            "If the absence may actually be medical leave, move it to the leave-support path immediately.",
        ],
        "acknowledgment": {
            "title": "Attendance and PTO checkpoint",
            "statement": "I understand timekeeping expectations, how attendance points work, and how to request or report time away from work.",
            "items": [
                "I know overtime must be approved before it is worked.",
                "I know PTO cannot be used before it is accrued.",
                "I understand when attendance points begin to trigger corrective action.",
            ],
        },
    },
    {
        "id": "benefits-and-eligibility",
        "slug": "benefits-and-eligibility",
        "eyebrow": "Benefits",
        "title": "Benefits and Eligibility",
        "summary": "Lay out the real benefits timeline, the plan categories, and the windows where timing matters.",
        "estimatedMinutes": 13,
        "purpose": "Understand when major benefits become available, what options exist, and when HR needs to step in to clarify timing or enrollment issues.",
        "focuses": ["Eligibility timeline", "Coverage choices", "Benefits support"],
        "essentials": [
            {"title": "Benefits open in stages", "body": "Some resources are available on day one, while others depend on full-time status, service time, age, or hours worked."},
            {"title": "Full-time employees get the main enrollment window", "body": "Medical, dental, vision, 401(k), and supplemental coverages become available to regular full-time employees on the first of the month after 60 days."},
            {"title": "Timing matters", "body": "Eligibility disputes, access issues, and qualified life event changes should move quickly through HR instead of being handled informally."},
        ],
        "policyAreas": [
            {
                "title": "Eligibility milestones",
                "items": [
                    {"label": "Day 1", "body": "All employees have access to LinkedIn Learning, the Employee Assistance Program, and AAP Perks."},
                    {"label": "Early milestones", "body": "Teladoc becomes available on the first of the month after hire, and all employees become eligible to use personal time off after 60 days."},
                    {"label": "Later milestones", "body": "Part-time 401(k) eligibility begins only after one year of service, 1,000 hours worked, and age 21 or older."},
                ],
            },
            {
                "title": "Medical, dental, vision, and retirement",
                "items": [
                    {"label": "Medical options", "body": "Regular full-time employees choose between a PPO plan and an HDHP with HSA when the medical enrollment window opens."},
                    {"label": "Dental and vision", "body": "Dental and vision coverage are through Guardian, and coverage details are accessed through Guardian Anytime instead of physical cards."},
                    {"label": "401(k)", "body": "AAP matches 100 percent of the first 3 percent an employee contributes and 50 percent of the next 2 percent."},
                ],
            },
            {
                "title": "Other support and important rules",
                "items": [
                    {"label": "HSA basics", "body": "The HDHP option includes an HSA, which carries tax advantages and stays with the employee."},
                    {"label": "Life-event changes", "body": "Most qualified life event changes must be submitted to HR within 30 days."},
                    {"label": "Long-term sick leave and service awards", "body": "Regular full-time employees reach long-term sick leave milestones at four years and then every five years after, and service awards begin at five years."},
                ],
            },
        ],
        "actions": [
            "Track your own eligibility dates instead of waiting for them to surprise you.",
            "Use HR if your classification, hire date, or hours-worked information looks wrong.",
            "Respond quickly when a qualified life event affects benefits enrollment.",
        ],
        "escalation": [
            "Escalate disputed eligibility dates or enrollment-access problems to HR.",
            "Use HR when plan options or deduction timing need clarification.",
            "Route long-term sick leave usage questions through HR instead of treating them like standard PTO.",
        ],
        "acknowledgment": {
            "title": "Benefits checkpoint",
            "statement": "I understand the benefits timeline, the main coverage options, and when HR is required for eligibility or enrollment questions.",
            "items": [
                "I know which benefits begin on day one versus later milestones.",
                "I understand when full-time medical enrollment becomes available.",
                "I know qualified life event changes are time-sensitive.",
            ],
        },
    },
    {
        "id": "conduct-confidentiality-and-workplace-standards",
        "slug": "conduct-confidentiality-and-workplace-standards",
        "eyebrow": "Standards",
        "title": "Conduct, Confidentiality, and Workplace Standards",
        "summary": "Keep conduct, confidentiality, computer-use rules, and complaint handling in one focused section.",
        "estimatedMinutes": 14,
        "purpose": "Understand the standards that protect trust: ethical behavior, respectful conduct, controlled information sharing, and proper reporting.",
        "focuses": ["Code of conduct", "Privacy and systems", "Reporting concerns"],
        "essentials": [
            {"title": "Ethics and respect are baseline expectations", "body": "Business ethics, respectful conduct, and non-retaliation are not optional standards or manager preferences."},
            {"title": "Confidentiality is active work", "body": "Employee records, medical information, complaints, and proprietary information should be handled on a need-to-know basis only."},
            {"title": "Company systems are business systems", "body": "Computers, email, files, and software are company property intended for business use and may be monitored."},
        ],
        "policyAreas": [
            {
                "title": "Conduct and respectful workplace rules",
                "items": [
                    {"label": "Business ethics", "body": "Employees are expected to comply with law and avoid illegal, dishonest, or unethical conduct."},
                    {"label": "Harassment and retaliation", "body": "Unlawful harassment is prohibited, complaints should be investigated promptly, and good-faith reporting is protected from retaliation."},
                    {"label": "Drug and alcohol rules", "body": "AAP expects a drug- and alcohol-free workplace and may conduct testing according to policy and law."},
                ],
            },
            {
                "title": "Confidentiality and records handling",
                "items": [
                    {"label": "Non-disclosure", "body": "Employees sign a confidentiality and non-disclosure agreement upon hire."},
                    {"label": "Need-to-know sharing", "body": "Personnel, payroll, benefits, medical, complaint, and business records should be shared only with people who require the information to do their job."},
                    {"label": "Approved storage only", "body": "Use approved company systems and locations. Do not forward confidential material to personal email or store it on personal devices."},
                ],
            },
            {
                "title": "Systems, appearance, and property",
                "items": [
                    {"label": "Computer and email usage", "body": "Company devices, files, and stored communications are company property and may be monitored under policy."},
                    {"label": "Personal appearance", "body": "Dress expectations vary by department, but employees are expected to present a neat, clean, work-appropriate appearance."},
                    {"label": "Return of property", "body": "Employees must return company property, materials, and written information immediately when requested or upon separation."},
                ],
            },
        ],
        "actions": [
            "Verify recipients before sending employee or company information.",
            "Keep complaints and sensitive information out of casual conversation.",
            "Report concerns quickly instead of trying to contain them informally.",
        ],
        "escalation": [
            "Escalate harassment, discrimination, retaliation, or violence concerns immediately.",
            "Escalate suspected data breaches, unauthorized access, or misdirected confidential information.",
            "Route medical information and complaint investigations through HR.",
        ],
        "acknowledgment": {
            "title": "Standards checkpoint",
            "statement": "I understand conduct expectations, confidentiality rules, and the requirement to route sensitive employee matters through HR.",
            "items": [
                "I know harassment and retaliation concerns should be reported promptly.",
                "I understand the need-to-know standard for confidential information.",
                "I know company devices and systems are governed by company policy.",
            ],
        },
    },
    {
        "id": "leave-and-support",
        "slug": "leave-and-support",
        "eyebrow": "Leave and Support",
        "title": "Leave and Support",
        "summary": "Focus the leave section on medical-leave handling, other protected time away, and the support routes that matter in practice.",
        "estimatedMinutes": 12,
        "purpose": "Know when leave questions can be answered generally, when they must be escalated, and what support resources exist for employees beyond PTO.",
        "focuses": ["FMLA and medical leave", "Other leave types", "Support routes"],
        "essentials": [
            {"title": "FMLA is immediate-escalation territory", "body": "If an employee asks about FMLA or hints at needing medical leave, the SOP says to notify HR right away and avoid requesting medical details."},
            {"title": "Not all time away is PTO", "body": "Bereavement, jury duty, witness duty, workers' compensation, accommodation requests, and longer medical absences follow different rules and should not be handled casually."},
            {"title": "Support includes escalation and assistance", "body": "Employees have access to the EAP and to a formal problem-resolution path when work-related issues need help beyond a routine question."},
        ],
        "policyAreas": [
            {
                "title": "FMLA and medical leave handling",
                "items": [
                    {"label": "Eligibility baseline", "body": "The SOP states FMLA eligibility at 366 days of work and 1,250 hours in the last 12 months, with an annual entitlement of 480 hours."},
                    {"label": "What not to do", "body": "Do not promise approval and do not request medical details outside the approved HR process."},
                    {"label": "Key rules", "body": "FMLA is unpaid, employees are not required to exhaust PTO before using unpaid FMLA time, and approved use may be tracked in one-hour increments."},
                ],
            },
            {
                "title": "Other leave and support categories",
                "items": [
                    {"label": "Other protected absences", "body": "Bereavement, jury duty, witness duty, and approved personal leaves have separate rules from standard PTO."},
                    {"label": "Accommodation and injury", "body": "Disability accommodation requests, work-related injuries, and workers' compensation questions should move to HR immediately."},
                    {"label": "EAP", "body": "LifeMatters is available as a confidential support resource from day one."},
                ],
            },
            {
                "title": "How support and escalation should work",
                "items": [
                    {"label": "Problem resolution", "body": "Concerns generally start with the immediate supervisor when appropriate, then move to HR or higher leadership if unresolved or inappropriate for that first step."},
                    {"label": "Safe escalation language", "body": "Use a general policy answer, then say the issue needs to be handled correctly and consistently through HR because it is specific to the employee's situation."},
                    {"label": "Extended absences", "body": "Longer absences or 30-plus consecutive workday absences may require additional documentation or return-to-work follow-up through HR."},
                ],
            },
        ],
        "actions": [
            "Move medical and leave-certification questions to HR immediately.",
            "Use the EAP when personal or work strain calls for confidential support.",
            "Escalate early when a leave question becomes employee-specific.",
        ],
        "escalation": [
            "Escalate any FMLA request or hint of serious health-related leave right away.",
            "Escalate disability accommodation requests and workers' compensation issues.",
            "Escalate extended absences that need certification or return-to-work guidance.",
        ],
        "acknowledgment": {
            "title": "Leave and support checkpoint",
            "statement": "I understand the basics of leave handling, the confidentiality rules around medical matters, and when immediate HR escalation is required.",
            "items": [
                "I know not to promise FMLA approval.",
                "I know medical details should stay inside the HR process.",
                "I know where to route accommodation, injury, and extended-leave questions.",
            ],
        },
    },
    {
        "id": "final-review-and-acknowledgments",
        "slug": "final-review-and-acknowledgments",
        "eyebrow": "Final Review",
        "title": "Final Review and Acknowledgments",
        "summary": "Close the general onboarding path with the core handbook commitments and the practical next steps that should remain after onboarding ends.",
        "estimatedMinutes": 8,
        "purpose": "Confirm the major commitments from the handbook, make the acknowledgment language clear, and turn the portal into an ongoing reference rather than a one-time checklist.",
        "focuses": ["Core commitments", "Acknowledgment language", "What happens next"],
        "essentials": [
            {"title": "The handbook is a guide, not a contract", "body": "The handbook explains policies, benefits, and expectations, but it does not create a contract of employment."},
            {"title": "At-will and policy updates remain important", "body": "Employment remains at-will, and handbook revisions may be communicated through official notices."},
            {"title": "Completion should leave you with a support map", "body": "The goal is not memorization. It is knowing what the standards are and where to go when a real question shows up."},
        ],
        "policyAreas": [
            {
                "title": "What employees are acknowledging",
                "items": [
                    {"label": "Responsibility to review", "body": "Employees are expected to read the handbook, follow the policies in it, and ask HR when a question is not answered clearly there."},
                    {"label": "At-will employment", "body": "The employment relationship does not have a specified length and may end at any time, subject to applicable law."},
                    {"label": "Policy revisions", "body": "Revisions may supersede existing handbook language through official notice."},
                ],
            },
            {
                "title": "Practical next-step reminders",
                "items": [
                    {"label": "Use the portal as reference", "body": "Return to the relevant section when you need a clean policy refresher instead of relying on memory or hallway answers."},
                    {"label": "Property and exit basics", "body": "Company property must be returned upon request or separation, and the handbook requests notice for resignation even though it is voluntary."},
                    {"label": "Role-specific content stays separate", "body": "The HR Administrative Assistant toolkit is intentionally separate from the main flow so the general path stays relevant to all employees."},
                ],
            },
        ],
        "actions": [
            "Finish any remaining acknowledgments and return to any section that still feels unclear.",
            "Keep HR as the path for interpretation, exceptions, and sensitive employee matters.",
            "Use the role-specific toolkit only if it is relevant to your job responsibilities.",
        ],
        "escalation": [
            "Escalate unresolved questions instead of treating completion as full policy mastery.",
            "Use HR whenever a real scenario goes beyond general handbook guidance.",
            "Treat sensitive benefits, leave, confidentiality, and conduct questions as escalation items.",
        ],
        "acknowledgment": {
            "title": "Final acknowledgment",
            "statement": "I understand that the handbook contains important policy information, that employment is at-will, and that I should use HR when a situation needs interpretation or sensitive handling.",
            "items": [
                "I know the handbook is not a contract of employment.",
                "I understand policy revisions may be communicated through official notices.",
                "I know where to go when a real employee situation needs more than a general answer.",
            ],
        },
    },
]

TRACKS: dict[str, dict[str, Any]] = {
    "default": {
        "id": "default",
        "name": "General Onboarding",
        "support_contact": {
            "name": "Nicole Thornton",
            "role": "HR Manager",
            "phone": "256-574-7528",
            "email": "nicole.thornton330@gmail.com",
        },
        "toolkit_slugs": [],
        "section_overrides": {},
    },
    "hr-admin": {
        "id": "hr-admin",
        "name": "HR Administrative Assistant",
        "support_contact": {
            "name": "Nicole Thornton",
            "role": "HR Manager",
            "phone": "256-574-7528",
            "email": "nicole.thornton330@gmail.com",
        },
        "toolkit_slugs": ["hr-administrative-assistant"],
        "section_overrides": {},
    },
}

TOOLKITS = [
    {
        "id": "hr-administrative-assistant-toolkit",
        "slug": "hr-administrative-assistant",
        "eyebrow": "Role-Specific Toolkit",
        "title": "HR Administrative Assistant Toolkit",
        "summary": "Keep HR Administrative Assistant guidance in its own lane so the general onboarding path stays clean for all employees.",
        "estimatedMinutes": 16,
        "purpose": "This toolkit is for day-to-day routing, systems awareness, and approved answer patterns. It is not part of the universal new-hire path.",
        "whenToUse": [
            "Use this when the role includes front-desk or HR support responsibilities.",
            "Use it for policy routing, system lookup, and approved answer scripts.",
            "Leave it separate from the general employee onboarding flow.",
        ],
        "systems": [
            {"name": "BambooHR", "link": "www.aap.bamboohr.com", "use": "Employee profiles, onboarding tasks, PTO and benefits, job postings"},
            {"name": "PayClock", "link": "www.portal.payclock.com", "use": "Timeclock polling, timecard review, PTO entry"},
            {"name": "Employvio", "link": "www.clients.employvio.com", "use": "Background and drug-screen invites"},
            {"name": "Paylocity", "link": "www.access.paylocity.com", "use": "Payroll reference unless broader payroll duties are assigned"},
            {"name": "Proton Pass", "link": "app.proton.me/pass", "use": "Password-sharing vault for HR systems"},
            {"name": "HR Drive", "link": "S:\\Human Resources", "use": "Digital filing and approved document storage"},
        ],
        "playbooks": [
            {
                "title": "Employee question routing",
                "summary": "Answer only the general policy question. Once it becomes employee-specific, move it to HR.",
                "doThis": [
                    "Identify whether the question is a general handbook question or a personal case.",
                    "Use the handbook section or SOP to give a plain-language general answer.",
                    "Use the safe escalation line when the issue becomes disputed, medical, or exception-based.",
                ],
                "escalateWhen": [
                    "Harassment, discrimination, retaliation, or discipline concerns",
                    "Medical restrictions, certification, or accommodation questions",
                    "Threats, violence, drug testing, or safety incidents",
                ],
            },
            {
                "title": "Attendance and PTO triage",
                "summary": "Stay factual on points, timing, and approval paths. Do not invent exceptions.",
                "doThis": [
                    "Confirm whether the employee needs a general attendance or PTO answer, a time-entry fix, or an actual exception request.",
                    "Use the no-fault attendance structure and PTO timing rules as written.",
                    "Move balance disputes or point disputes to HR.",
                ],
                "escalateWhen": [
                    "Attendance point disputes",
                    "Time-off balances that appear incorrect",
                    "Longer absences that may actually be medical leave",
                ],
            },
            {
                "title": "Benefits eligibility triage",
                "summary": "Use milestone-based answers, not memory or assumptions.",
                "doThis": [
                    "Confirm full-time versus part-time status and the milestone being asked about.",
                    "Use the documented timing for day-one resources, 60-day PTO, and full-time enrollment windows.",
                    "Send disputed dates or enrollment-access issues to HR.",
                ],
                "escalateWhen": [
                    "Eligibility dates are disputed",
                    "Classification or hours-worked records are unclear",
                    "Coverage interpretation requires HR review",
                ],
            },
            {
                "title": "Confidential handling",
                "summary": "Protect employee information, complaints, and medical material with a strict need-to-know approach.",
                "doThis": [
                    "Identify the type of information before sharing or storing it.",
                    "Use approved systems and keep medical and complaint material inside the HR process.",
                    "Pause and ask HR if it is unclear whether the information can be shared.",
                ],
                "escalateWhen": [
                    "A data breach or unauthorized disclosure is suspected",
                    "Medical or leave documentation is involved",
                    "A complaint involves harassment, discrimination, or retaliation",
                ],
            },
        ],
        "quickAnswers": [
            {"question": "How do rest breaks work?", "answer": "Full-time nonexempt employees receive two paid 15-minute rest periods each workday.", "reference": "Policy Playbook, Section 505"},
            {"question": "What if someone works a holiday?", "answer": "When staffing requires an employee to work a designated or observed holiday, the department coordinates a floating holiday to be used within 90 days.", "reference": "PTO SOP and handbook holiday guidance"},
            {"question": "How do attendance points work?", "answer": "Use the no-fault attendance matrix: grace period up to five minutes, 0.5 points for less than half-shift tardy or early leave, 1 point for half shift or more, and 1.5 points for a no-report absence.", "reference": "Handbook Section 704"},
            {"question": "What is the safest confidentiality rule?", "answer": "If the information is employee-specific, medical, complaint-related, or unclear, keep it on a need-to-know basis and move it through HR.", "reference": "Confidentiality SOP"},
        ],
        "escalateImmediately": [
            "Harassment, discrimination, retaliation, threats, violence, or discipline issues",
            "FMLA, accommodation, medical restrictions, or leave-certification questions",
            "Attendance point disputes or operational exception requests",
            "Privacy breaches, unauthorized disclosures, or uncertain sharing decisions",
        ],
        "contacts": [
            {"name": "Nicole Thornton", "role": "HR Administrator", "phone": "256-574-7528 ext 252", "email": "nicole.thornton@apirx.com"},
            {"name": "Brandy Hooper", "role": "VP of Human Resources", "phone": "256-574-7526 ext 226", "email": "brandy.hooper@rxaap.com"},
            {"name": "Trevor Bowen", "role": "IT (Scottsboro)", "phone": "256-574-6819 ext 214", "email": "trevor.bowen@apirx.com"},
            {"name": "Phil Horton", "role": "IT (Memphis)", "phone": "901-800-4605 ext 405", "email": "phil.horton@apirx.com"},
            {"name": "Austin Wilson", "role": "IT (AAP)", "phone": "256-218-5527 ext 527", "email": "austin.wilson@rxaap.com"},
        ],
        "acknowledgment": {
            "title": "Toolkit review",
            "statement": "I understand that the HR Administrative Assistant toolkit is a separate operational reference, and that employee-specific or sensitive questions should move to HR quickly.",
            "items": [
                "I know this toolkit is separate from the general employee onboarding flow.",
                "I know when to stop answering and start escalating.",
                "I know which systems and contacts are relevant to the role.",
            ],
        },
    }
]


def get_experience_content(track_id: str = "default") -> dict[str, Any]:
    track = TRACKS.get(track_id, TRACKS["default"])
    return {
        "organization": ORGANIZATION,
        "dashboardStats": DASHBOARD_STATS,
        "contacts": CONTACTS,
        "sections": SECTIONS,
        "toolkits": TOOLKITS,
        "track": track,
    }


def get_section_by_slug(slug: str) -> dict[str, Any] | None:
    for section in SECTIONS:
        if section["slug"] == slug:
            return section
    return None


def get_toolkit_by_slug(slug: str) -> dict[str, Any] | None:
    for toolkit in TOOLKITS:
        if toolkit["slug"] == slug:
            return toolkit
    return None
