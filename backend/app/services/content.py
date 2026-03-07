from __future__ import annotations

from typing import Any

ORGANIZATION = {
    "name": "AAP/API",
    "headline": "A modern onboarding flow for the teams behind independent pharmacy success.",
    "tagline": "Confidence first. Clarity always. Momentum from day one.",
    "mission": "AAP provides support and customized solutions for independent community pharmacies to enhance profitability, streamline operations, and improve the quality of patient care.",
    "vision": "Helping independent pharmacies thrive in a competitive healthcare market.",
    "story": "American Associated Pharmacies is a national cooperative of more than 2,000 independent pharmacies. API operates as AAP's distribution arm, helping member pharmacies stay competitive with the tools, inventory access, and operational support they need.",
    "values": [
        {"name": "Customer Focus", "body": "External service starts with strong internal teamwork. Customer service is not just a department here; it is an operating posture."},
        {"name": "Integrity", "body": "Say what is true, do what is right, and keep trust intact even when the answer is inconvenient."},
        {"name": "Respect", "body": "Treat people with dignity, communicate honestly, and work like every role matters because it does."},
        {"name": "Excellence", "body": "Aim for quality, look for improvements, and keep standards high without making things harder than they need to be."},
        {"name": "Ownership", "body": "Take responsibility early, escalate clearly, and fix what is in your lane instead of waiting for someone else to notice."},
    ],
}

DASHBOARD_STATS = [
    {"label": "Core sections", "value": "7", "detail": "The main onboarding path for every new employee."},
    {"label": "Role toolkit", "value": "1", "detail": "A separate reference lane for the HR Administrative Assistant role."},
    {"label": "Intro period", "value": "60 days", "detail": "Initial introductory period for new and rehired employees."},
    {"label": "Support lane", "value": "HR + Leads", "detail": "Use HR for policy, benefits, confidentiality, or leave-specific questions."},
]

CONTACTS = [
    {"name": "Brandy Hooper", "role": "VP of Human Resources", "email": "brandy.hooper@rxaap.com", "phone": "256-574-7526", "note": "Escalation point for unresolved HR concerns and harassment reporting."},
    {"name": "Nicole Thornton", "role": "HR Administrator", "email": "nicole.thornton@apirx.com", "phone": "256-574-7528", "note": "Best first stop for onboarding, benefits coordination, and personnel questions."},
    {"name": "CBIZ Benefits", "role": "Benefits Support", "email": "Melissa.street@cbiz.com", "phone": "844.200.CBIZ (2249)", "note": "Benefits-plan support after HR has routed the request."},
    {"name": "LifeMatters", "role": "Employee Assistance Program", "email": "www.empathia.com", "phone": "800-634-6433", "note": "Confidential employee assistance resource."},
]

SECTIONS = [
    {
        "id": "welcome-to-aap-api",
        "slug": "welcome-to-aap-api",
        "eyebrow": "Start Here",
        "title": "Welcome to AAP/API",
        "summary": "Get the company story, the reason the role matters, and the values that shape how work gets done.",
        "estimatedMinutes": 10,
        "punchline": "This is the part where the big picture snaps into focus.",
        "quickFacts": [
            {"label": "Who we serve", "value": "2,000+ independent pharmacies"},
            {"label": "What API does", "value": "Warehouse and distribution support"},
            {"label": "Why this matters", "value": "Profitability, operations, and patient care"},
        ],
        "highlightCards": [
            {"title": "Why the company exists", "body": "AAP was formed to help independent pharmacies stay strong in a competitive healthcare market. The work behind the scenes supports better local care in the communities pharmacies serve.", "tone": "cyan"},
            {"title": "What success feels like", "body": "New hires should leave week one with context, reliable support contacts, and a clear sense of how their role connects to customers and teammates.", "tone": "navy"},
            {"title": "How the culture works", "body": "Values are meant to show up in decisions, conversations, escalations, and service habits. They are operational, not decorative.", "tone": "red"},
        ],
        "timeline": [
            {"label": "Day 1", "title": "Meet the company and support map", "body": "Learn the AAP/API story, your key contacts, and the basics of where to go when a question becomes policy-specific."},
            {"label": "Week 1", "title": "Build role confidence", "body": "Connect your job to the customer impact, finish the core onboarding path, and get comfortable escalating instead of guessing."},
            {"label": "Day 60", "title": "Cross the introductory milestone", "body": "The handbook's introductory period runs for the first 60 calendar days and is used to evaluate fit, habits, and performance."},
        ],
        "takeaways": [
            "AAP and API exist to help independent pharmacies perform better, operate smarter, and serve patients well.",
            "Mission, vision, and values should be visible in daily choices and not treated like poster copy.",
            "The company expects employees to ask early, escalate clearly, and stay aligned with policy instead of improvising.",
        ],
        "reminders": [
            "The handbook applies to employees of both AAP and API.",
            "Questions not answered in the handbook should be routed to HR.",
            "The handbook may be revised over time through official notices.",
        ],
        "faq": [
            {"question": "Does the handbook create a contract of employment?", "answer": "No. The handbook explains expectations, benefits, and policies, but it does not create an employment contract."},
            {"question": "Who should I contact when I am unsure which policy applies?", "answer": "Start with your supervisor for day-to-day context, and use HR for benefits, confidentiality, personnel-file access, leave, or sensitive conduct issues."},
        ],
        "resources": [
            {"title": "Mission", "body": "Support independent community pharmacies with customized solutions that improve profitability, operations, and patient care."},
            {"title": "Vision", "body": "Help independent pharmacies thrive in a competitive healthcare market."},
        ],
        "acknowledgment": {
            "title": "Orientation checkpoint",
            "statement": "I understand AAP/API's mission, vision, core values, and why my role contributes to a broader customer outcome.",
            "items": [
                "I can explain what AAP/API does in plain language.",
                "I know the five company values and how they show up in daily work.",
                "I know HR is the right escalation path when a policy question turns sensitive or specific.",
            ],
        },
    },
    {
        "id": "working-at-aap-api",
        "slug": "working-at-aap-api",
        "eyebrow": "How Work Runs",
        "title": "Working at AAP/API",
        "summary": "Understand employment status, employee records, equal opportunity expectations, and the practical rules behind day-to-day employment.",
        "estimatedMinutes": 12,
        "punchline": "The operating model is simple: know your status, keep records current, and escalate cleanly.",
        "quickFacts": [
            {"label": "Full-time threshold", "value": "30+ hours per week"},
            {"label": "Intro period", "value": "60 calendar days"},
            {"label": "Personnel file access", "value": "Through HR only"},
        ],
        "highlightCards": [
            {"title": "Employment is at-will", "body": "Employees and the company may end the employment relationship at any time, subject to applicable law.", "tone": "navy"},
            {"title": "Employment decisions are merit-based", "body": "AAP states that hiring and employment decisions are based on merit, qualifications, and abilities, without unlawful discrimination.", "tone": "cyan"},
            {"title": "Keep your records current", "body": "Changes to address, phone number, dependents, emergency contacts, or other personnel information should be reported promptly.", "tone": "red"},
        ],
        "timeline": [
            {"label": "Classification", "title": "Know your employment category", "body": "Employees are classified as exempt or nonexempt and also fall into categories such as regular full-time, part-time, introductory, or temporary."},
            {"label": "Records", "title": "Keep people data accurate", "body": "Notify HR when contact details, dependents, or emergency information change. Personnel files are company property with restricted access."},
            {"label": "Growth", "title": "Use internal mobility channels", "body": "AAP may post job openings internally to support development and advancement according to experience and fit."},
        ],
        "takeaways": [
            "Regular full-time status generally begins at 30 or more scheduled hours per week and is tied to benefit eligibility.",
            "The introductory period is used to evaluate performance, work habits, and overall fit.",
            "Employees may review their own personnel file only through HR, with reasonable notice, at company offices.",
        ],
        "reminders": [
            "Equal employment opportunity concerns can be raised without fear of reprisal.",
            "Outside employment cannot interfere with AAP/API job responsibilities.",
            "All employees sign a confidentiality and non-disclosure agreement upon hire.",
        ],
        "faq": [
            {"question": "What if my employment status changes because my hours increase?", "answer": "The handbook states that part-time employees who reach a six-month rolling average of 30 scheduled hours or more per week may be reclassified as regular full-time employees."},
            {"question": "Can I review my own personnel file whenever I want?", "answer": "Requests go through HR, require reasonable notice, and are reviewed in the office with an appointed representative present."},
        ],
        "resources": [
            {"title": "Problem resolution", "body": "Concerns should typically start with the immediate supervisor, then move up through HR or senior leadership if the issue remains unresolved or is inappropriate for the first-line path."},
            {"title": "Business ethics", "body": "Employees are expected to comply with applicable laws and avoid illegal, dishonest, or unethical conduct."},
        ],
        "acknowledgment": {
            "title": "Employment basics checkpoint",
            "statement": "I understand the employment framework, where my records live, and when HR is required for personnel or equity-related questions.",
            "items": [
                "I know the difference between employment classification and benefit eligibility.",
                "I know how to request a personnel-file review.",
                "I know to report personal data changes promptly to HR.",
            ],
        },
    },
    {
        "id": "attendance-timekeeping-and-pto",
        "slug": "attendance-timekeeping-and-pto",
        "eyebrow": "Show Up Sharp",
        "title": "Attendance, Timekeeping, and PTO",
        "summary": "Learn how attendance points work, how time off is requested, what PTO rules matter most, and where the line is between planning ahead and creating chaos.",
        "estimatedMinutes": 14,
        "punchline": "Reliable attendance is a team sport with actual math behind it.",
        "quickFacts": [
            {"label": "Request timing", "value": "By 5:00 PM the day before planned time off"},
            {"label": "No-call/no-report", "value": "1.5 attendance points"},
            {"label": "Perfect attendance bonus", "value": "$75 after 3 consecutive months"},
        ],
        "highlightCards": [
            {"title": "Attendance is tracked on a no-fault point system", "body": "For nonexempt employees, tardies, early leaves, and absences are assigned point values. Certain approved leave types are excluded.", "tone": "red"},
            {"title": "Time off cannot be used before it is accrued", "body": "Vacation and personal leave follow eligibility and accrual rules. Planned time off should be submitted in BambooHR with enough notice for staffing.", "tone": "cyan"},
            {"title": "Overtime requires approval", "body": "Overtime must be approved before it is worked. Paid time off does not count as hours worked for overtime calculations.", "tone": "navy"},
        ],
        "timeline": [
            {"label": "Daily", "title": "Be ready to work at start time", "body": "Tardiness is being away from your work area and not ready to work at the start of the day or after breaks."},
            {"label": "Before time off", "title": "Submit requests in the right channel", "body": "Employees review balances, submit the correct time-off type in BambooHR, and notify supervisors when plans change."},
            {"label": "As points increase", "title": "Corrective steps start at five points", "body": "Five points trigger coaching, six a verbal warning, seven a written warning, and eight may lead to termination within a consecutive 12-month period."},
        ],
        "takeaways": [
            "Tardy up to five minutes is a grace period. Less than half-shift tardy or early leave is 0.5 points, half-shift or more is 1 point, and a no-report absence is 1.5 points.",
            "Consecutive illness absences may count as a single point when supported by the required doctor's documentation.",
            "For planned time off, submit no later than 5:00 PM the day before. For unexpected personal leave, notify your supervisor before the scheduled start time whenever possible.",
        ],
        "reminders": [
            "Vacation for regular full-time employees becomes available after 60 days and accrues weekly based on service.",
            "Personal leave also has a 60-day waiting period and generally does not roll over or pay out at separation.",
            "If you work a designated holiday, the department coordinates a floating holiday to be used within 90 days.",
        ],
        "faq": [
            {"question": "What happens if I miss two consecutive days without reporting in?", "answer": "The handbook says the employee will be considered to have voluntarily quit without notice."},
            {"question": "Can I take more than five consecutive vacation days?", "answer": "Yes, but written approval by the Company President is required."},
            {"question": "Do vacation and other paid leave count toward overtime?", "answer": "No. Overtime is based on actual hours worked."},
        ],
        "resources": [
            {"title": "Vacation accrual", "body": "Regular full-time employees start at 24 hours per year after 60 days, increasing with service through a 152-hour annual accrual tier at 20 years and beyond."},
            {"title": "Holidays", "body": "Observed holidays that fall on Saturday move to Friday, and Sunday holidays move to Monday."},
        ],
        "acknowledgment": {
            "title": "Attendance and PTO checkpoint",
            "statement": "I understand attendance expectations, the point system, and the correct way to request or report time away from work.",
            "items": [
                "I know the difference between planned PTO requests and unexpected leave reporting.",
                "I understand how attendance points accumulate and when corrective action begins.",
                "I know overtime must be approved in advance and PTO does not count as hours worked for overtime.",
            ],
        },
    },
    {
        "id": "benefits-and-eligibility",
        "slug": "benefits-and-eligibility",
        "eyebrow": "Use The Good Stuff",
        "title": "Benefits and Eligibility",
        "summary": "Map the benefit timeline, understand what starts on day one versus after 60 days, and know which questions belong with HR or benefits support.",
        "estimatedMinutes": 13,
        "punchline": "Benefits are part of the compensation package, not a side quest.",
        "quickFacts": [
            {"label": "Day 1 benefits", "value": "LinkedIn Learning, EAP, AAP Perks"},
            {"label": "Full-time medical eligibility", "value": "1st of the month after 60 days"},
            {"label": "401(k) match", "value": "100% of first 3%, 50% of next 2%"},
        ],
        "highlightCards": [
            {"title": "Eligibility depends on timing and classification", "body": "Some benefits are available to all employees quickly, while others depend on full-time status, service time, age, or hours worked.", "tone": "cyan"},
            {"title": "Full-time employees get plan choice", "body": "Medical enrollment includes two medical plan options, PPO or HDHP with HSA, plus dental, vision, 401(k), and supplemental coverage after the standard waiting period.", "tone": "navy"},
            {"title": "The HSA option changes the math", "body": "The HDHP includes a Health Savings Account with company contributions, tax advantages, and funds that stay with the employee.", "tone": "red"},
        ],
        "timeline": [
            {"label": "Day 1", "title": "Activate the immediate resources", "body": "All employees can access LinkedIn Learning, the Employee Assistance Program, and AAP Perks."},
            {"label": "1st of month after hire", "title": "Teladoc turns on", "body": "Teladoc becomes active for all employees as a no-cost telehealth resource."},
            {"label": "60 days and after", "title": "PTO and benefit windows open", "body": "All employees become eligible to use personal time off at 60 days, while full-time employees gain vacation access at 60 days and medical enrollment on the first of the month after 60 days."},
        ],
        "takeaways": [
            "Children may be covered through the end of the month they turn 26.",
            "Part-time 401(k) eligibility requires one year of service, 1,000 hours worked, and age 21 or older.",
            "Dental and vision are through Guardian and do not issue insurance cards; coverage details live in Guardian Anytime.",
        ],
        "reminders": [
            "Benefit enrollment windows and qualified life event changes are time-sensitive.",
            "Employees must notify HR within 30 days of most qualified life events for enrollment changes.",
            "Questions about disputed eligibility dates, classification, or enrollment access should be escalated to HR.",
        ],
        "faq": [
            {"question": "When does medical coverage begin for regular full-time employees?", "answer": "Coverage begins on the first day of the month following 60 days of employment."},
            {"question": "What are the two medical-plan choices?", "answer": "Full-time employees may choose between a PPO plan and a high-deductible health plan paired with an HSA."},
            {"question": "What does the company match in the 401(k)?", "answer": "AAP matches 100 percent of the first 3 percent contributed and 50 percent of the next 2 percent."},
        ],
        "resources": [
            {"title": "Support contacts", "body": "HR remains the primary routing point. CBIZ and carrier partners help after eligibility or enrollment context is confirmed."},
            {"title": "Long-term sick leave milestone", "body": "Regular full-time employees gain 80 hours at the four-year anniversary, then again every five years, with a 180-hour bank limit and doctor-note requirement."},
        ],
        "acknowledgment": {
            "title": "Benefits checkpoint",
            "statement": "I understand the eligibility timeline for core benefits, the role of HR in enrollment questions, and the basics of the available plans.",
            "items": [
                "I know which resources are available on day one versus later milestones.",
                "I understand the waiting period for full-time medical enrollment.",
                "I know to escalate disputed eligibility or access issues to HR instead of guessing.",
            ],
        },
    },
    {
        "id": "conduct-confidentiality-and-workplace-standards",
        "slug": "conduct-confidentiality-and-workplace-standards",
        "eyebrow": "Standards That Matter",
        "title": "Conduct, Confidentiality, and Workplace Standards",
        "summary": "Cover business ethics, harassment protections, confidentiality rules, computer-use expectations, and the baseline behaviors that protect trust.",
        "estimatedMinutes": 15,
        "punchline": "Protect the people, protect the data, protect the trust.",
        "quickFacts": [
            {"label": "Confidentiality agreement", "value": "Signed upon hire"},
            {"label": "Harassment reporting", "value": "Supervisor, HR, or VP of HR"},
            {"label": "Data sharing rule", "value": "Need-to-know only"},
        ],
        "highlightCards": [
            {"title": "Harassment and retaliation are prohibited", "body": "AAP states that discrimination and unlawful harassment are not tolerated and that good-faith reporting is protected from retaliation.", "tone": "red"},
            {"title": "Company systems are company property", "body": "Computers, email, stored communications, and software are business-use systems and may be monitored within company policy.", "tone": "navy"},
            {"title": "Medical information is highly restricted", "body": "Medical and leave-related documentation should not be requested or distributed casually. Route it to HR immediately.", "tone": "cyan"},
        ],
        "timeline": [
            {"label": "Before sharing", "title": "Identify the information type", "body": "Determine whether the information is employee, payroll, medical, candidate, business, or proprietary data before you store or send it."},
            {"label": "When in doubt", "title": "Pause and consult HR", "body": "The confidentiality SOP explicitly says to stop and ask HR when it is unclear whether information can be shared."},
            {"label": "If something goes wrong", "title": "Report privacy incidents immediately", "body": "Misdirected emails, lost paperwork, unauthorized access, and suspicious system activity should be reported right away."},
        ],
        "takeaways": [
            "Personnel files are company property with restricted access, and employee review requests go through HR.",
            "Complaints involving harassment, discrimination, retaliation, or investigations are treated as confidential to the extent possible.",
            "Employees are responsible for returning company property and complying with workplace conduct, safety, and appearance expectations.",
        ],
        "reminders": [
            "Do not forward confidential material to personal email or store it on personal devices.",
            "Collect printed confidential documents immediately and use secure disposal methods.",
            "Route complaints, threats, retaliation concerns, or legal/compliance questions to HR without delay.",
        ],
        "faq": [
            {"question": "Can the company monitor email and computer use?", "answer": "Yes. Company computers, files, and email are company property intended for business use and may be monitored."},
            {"question": "What should I do if an employee asks to see their personnel file?", "answer": "Route the request to HR. The review must be scheduled with reasonable notice at company offices with an appointed representative present."},
            {"question": "What if I receive medical details that were sent to me accidentally?", "answer": "Do not redistribute them. Notify HR immediately and let HR direct the next step."},
        ],
        "resources": [
            {"title": "Problem resolution path", "body": "Concerns can move from supervisor to HR to senior leadership, with the Chief Executive Officer serving as the final internal resolution step if needed."},
            {"title": "Return of property", "body": "Employees must return company property immediately upon request or separation, and the company may recover costs where allowed by law."},
        ],
        "acknowledgment": {
            "title": "Standards checkpoint",
            "statement": "I understand conduct expectations, confidentiality rules, and the requirement to route sensitive personnel or medical matters through HR.",
            "items": [
                "I know harassment, retaliation, and discrimination concerns should be reported promptly.",
                "I understand the need-to-know standard for confidential information.",
                "I know company devices, email, and files are business systems governed by company policy.",
            ],
        },
    },
    {
        "id": "leave-and-support",
        "slug": "leave-and-support",
        "eyebrow": "Support Without Guesswork",
        "title": "Leave and Support",
        "summary": "Cover FMLA intake, confidential handling, support resources, and the difference between giving a general answer and promising something you cannot authorize.",
        "estimatedMinutes": 11,
        "punchline": "Some questions should be answered. Some should be escalated in under a minute.",
        "quickFacts": [
            {"label": "FMLA eligibility baseline", "value": "366 days and 1,250 hours"},
            {"label": "Annual FMLA entitlement", "value": "480 hours"},
            {"label": "FMLA pay status", "value": "Unpaid"},
        ],
        "highlightCards": [
            {"title": "FMLA requests go to HR immediately", "body": "If an employee asks about FMLA or hints at needing medical leave, the SOP says to escalate to the HR Manager right away.", "tone": "red"},
            {"title": "You can explain the basics but not promise approval", "body": "Employees can receive general information on eligibility and pay status, but approval and designation are handled by HR.", "tone": "cyan"},
            {"title": "Support is broader than leave", "body": "Employees also have access to the Employee Assistance Program and the formal problem-resolution path when work-related issues need help.", "tone": "navy"},
        ],
        "timeline": [
            {"label": "At the first mention", "title": "Escalate and protect confidentiality", "body": "Do not request medical details. Notify HR immediately and keep the conversation limited to approved general guidance."},
            {"label": "During review", "title": "HR manages certification", "body": "HR provides the required certification forms, handles follow-up, and manages tracking in BambooHR."},
            {"label": "During extended absence", "title": "Watch the 30-workday threshold", "body": "Longer absences may require updated documentation, return-to-work paperwork, or renewed certification."},
        ],
        "takeaways": [
            "Employees are not required to exhaust PTO before taking unpaid FMLA time.",
            "FMLA may be taken in one-hour increments when approved and tracked correctly.",
            "The EAP offers confidential support for life and work challenges, and it is available from day one.",
        ],
        "reminders": [
            "Questions involving disability accommodation, medical restrictions, workers' compensation, or leave certification should go to HR.",
            "Serious health conditions, ongoing treatment, or extended leave requests require immediate escalation.",
            "No employee should be penalized for raising work-related concerns in a reasonable and businesslike manner.",
        ],
        "faq": [
            {"question": "Do employees have to use PTO before FMLA?", "answer": "No. The SOP says employees are not required to exhaust PTO before using unpaid FMLA time."},
            {"question": "Can I tell someone they are approved for FMLA if they seem to qualify?", "answer": "No. Only HR confirms eligibility and designation."},
            {"question": "What if a concern is not medical but still feels unresolved?", "answer": "Use the problem-resolution process: start with the supervisor when appropriate, then escalate through HR or senior leadership if needed."},
        ],
        "resources": [
            {"title": "EAP", "body": "LifeMatters provides confidential support and can be reached at 800-634-6433."},
            {"title": "Safe escalation language", "body": "Here is the policy in general. Because your situation is specific, I want to make sure it is handled correctly and consistently, so I am connecting you with HR."},
        ],
        "acknowledgment": {
            "title": "Leave and support checkpoint",
            "statement": "I understand the basics of leave support, the confidentiality requirements around medical matters, and when immediate HR escalation is mandatory.",
            "items": [
                "I know the basic FMLA eligibility and entitlement rules.",
                "I understand that FMLA approval cannot be promised outside HR.",
                "I know where to route sensitive leave, accommodation, or workers' compensation questions.",
            ],
        },
    },
    {
        "id": "final-review-and-acknowledgments",
        "slug": "final-review-and-acknowledgments",
        "eyebrow": "Wrap It Cleanly",
        "title": "Final Review and Acknowledgments",
        "summary": "Finish the onboarding path with a clean review of the commitments that matter most and the acknowledgment language the handbook expects employees to understand.",
        "estimatedMinutes": 9,
        "punchline": "The end should feel crisp, not vague.",
        "quickFacts": [
            {"label": "Handbook status", "value": "Policy guide, not a contract"},
            {"label": "Revision authority", "value": "Official company notices"},
            {"label": "Best next move", "value": "Ask when something is unclear"},
        ],
        "highlightCards": [
            {"title": "Read the handbook like an operating guide", "body": "The handbook lays out responsibilities, benefits, working conditions, and policy expectations that employees are expected to understand and follow.", "tone": "navy"},
            {"title": "Policy updates may happen", "body": "The company may revise policies over time through official notices, with the at-will employment principle remaining unchanged unless required by law.", "tone": "cyan"},
            {"title": "Questions are part of compliance", "body": "A clean escalation to HR is better than a confident wrong answer. That is a feature, not a flaw.", "tone": "red"},
        ],
        "timeline": [
            {"label": "Review", "title": "Confirm the essentials", "body": "Revisit values, conduct standards, attendance basics, benefits timing, and the leave-support rules that require immediate escalation."},
            {"label": "Acknowledge", "title": "Confirm understanding", "body": "Employees should understand that the handbook contains important information and that questions not answered there should go to HR."},
            {"label": "Move forward", "title": "Use the platform as a reference", "body": "The onboarding experience is designed to stay useful after week one, especially for policy refreshers and support routing."},
        ],
        "takeaways": [
            "The handbook is not a legal contract and does not guarantee employment for a definite term.",
            "Either the employee or the company may end the employment relationship at will, subject to applicable law.",
            "Employees are responsible for reading and complying with policy updates communicated through official channels.",
        ],
        "reminders": [
            "Use HR when a question involves interpretation, an exception, or sensitive personal details.",
            "Role-specific content such as the HR Administrative Assistant toolkit lives in a separate lane from the universal onboarding path.",
            "Completion is not just clicking through. It means knowing what to do next when a real scenario shows up.",
        ],
        "faq": [
            {"question": "What if a policy changes after I finish onboarding?", "answer": "Official notices may revise or supersede current policy language, and employees are expected to follow the updated guidance."},
            {"question": "Where should I go when a real-world situation does not fit a clean example?", "answer": "Use HR or the appropriate supervisor and escalate sooner rather than later."},
        ],
        "resources": [
            {"title": "Acknowledgment mindset", "body": "The goal is not to memorize everything. It is to know the standards, the support map, and the moments when escalation is required."}
        ],
        "acknowledgment": {
            "title": "Final acknowledgment",
            "statement": "I understand that the handbook contains important policy information, that employment is at-will, and that I should use HR when a situation requires interpretation or sensitive handling.",
            "items": [
                "I know the handbook is a guide to policies and benefits, not a contract.",
                "I understand that policy revisions may be communicated through official notices.",
                "I know my next step when a policy question involves benefits, leave, confidentiality, or conduct concerns.",
            ],
        },
    },
]

TOOLKITS = [
    {
        "id": "hr-administrative-assistant-toolkit",
        "slug": "hr-administrative-assistant",
        "eyebrow": "Role-Specific Lane",
        "title": "HR Administrative Assistant Toolkit",
        "summary": "A separate operational reference for the HR Administrative Assistant role, built from the quick-reference guide and policy playbook.",
        "estimatedMinutes": 16,
        "punchline": "Fast routing, careful wording, zero freestyle policy interpretation.",
        "hero": {
            "title": "Front-desk confidence for policy-heavy moments",
            "body": "Use this toolkit to route common questions, stay within approved guidance, and escalate quickly when a situation moves from routine to sensitive.",
        },
        "overviewCards": [
            {"title": "Golden rule", "body": "Stay factual, stay consistent, and reference the handbook or SOP. If the situation involves a dispute, medical issue, harassment concern, or exception request, route it to HR."},
            {"title": "Primary systems", "body": "BambooHR for employee records and PTO workflows, PayClock for timecards, Employvio for background and drug screens, Paylocity for payroll reference, and Proton Pass for credential sharing."},
            {"title": "Best skill to build", "body": "Knowing when to stop answering and start escalating is more valuable than sounding certain."},
        ],
        "systems": [
            {"name": "BambooHR", "link": "www.aap.bamboohr.com", "use": "Employee profiles, onboarding tasks, PTO/benefits, job postings"},
            {"name": "PayClock", "link": "www.portal.payclock.com", "use": "Timeclock polling, timecard review, PTO entry"},
            {"name": "Employvio", "link": "www.clients.employvio.com", "use": "Background and drug-screen invites"},
            {"name": "Paylocity", "link": "www.access.paylocity.com", "use": "Payroll reference unless additional responsibilities are assigned"},
            {"name": "Proton Pass", "link": "app.proton.me/pass", "use": "Password-sharing vault for HR systems"},
            {"name": "HR Drive", "link": "S:\\Human Resources", "use": "Digital filing and document storage"},
        ],
        "playbooks": [
            {
                "title": "Quick routing for employee questions",
                "body": "Use the approved-answer scripts when the question is general. Shift to escalation if the issue becomes employee-specific, disputed, or sensitive.",
                "steps": [
                    "Identify whether the question is general policy, a personal dispute, or a sensitive case.",
                    "Answer general questions with the plain-language script tied to the handbook section.",
                    "Use the safe escalation line when the scenario becomes medical, disciplinary, or exception-based.",
                ],
                "escalateWhen": [
                    "Harassment, discrimination, or retaliation concerns",
                    "Disability accommodation or leave-certification questions",
                    "Threats, violence, drug-testing, or safety incidents",
                    "Attendance point disputes or any discipline-related scenario",
                ],
            },
            {
                "title": "Attendance and PTO triage",
                "body": "Stay consistent on attendance math, PTO timing, and who owns approval. Do not create side agreements.",
                "steps": [
                    "Confirm the employee's question relates to attendance, PTO balance, or time-entry workflow.",
                    "Reference the no-fault attendance structure and the PTO request timing rules.",
                    "Route disputed balances, operational exceptions, or policy conflicts to HR.",
                ],
                "escalateWhen": [
                    "Time-off balances appear incorrect",
                    "A manager requests an exception outside policy",
                    "A point assessment is disputed",
                    "A longer leave request may actually be FMLA-related",
                ],
            },
            {
                "title": "Benefits eligibility triage",
                "body": "Use milestone-based answers and avoid improv answers about coverage dates or special cases.",
                "steps": [
                    "Confirm whether the employee is full-time or part-time and what milestone they are asking about.",
                    "Use the benefits timeline: day-one resources, first-of-month Teladoc, 60-day PTO, first-of-month-after-60-days full-time enrollment, and part-time 401(k) rules.",
                    "Escalate disputed dates, enrollment-access problems, or plan-specific interpretation questions.",
                ],
                "escalateWhen": [
                    "Eligibility date is disputed",
                    "Employee classification or hours-worked data is unclear",
                    "Coverage options need interpretation",
                    "Long-term sick leave or nonstandard enrollment timing is requested",
                ],
            },
            {
                "title": "Confidential handling and records discipline",
                "body": "Treat employee data, medical information, complaints, and investigation material with a need-to-know standard every time.",
                "steps": [
                    "Identify the information type before sharing or storing it.",
                    "Keep medical information and complaints tightly controlled and routed through HR.",
                    "Use approved systems and avoid personal-device or personal-email storage.",
                ],
                "escalateWhen": [
                    "A data breach or unauthorized disclosure is suspected",
                    "Medical or leave documentation is involved",
                    "A complaint includes harassment, discrimination, or retaliation",
                    "It is unclear whether information can be shared",
                ],
            },
        ],
        "escalationContacts": [
            {"name": "Nicole Thornton", "role": "HR Manager contact path in daily workflow", "phone": "256-574-7528 ext 252", "email": "nicole.thornton@apirx.com"},
            {"name": "Brandy Hooper", "role": "VP of HR escalation path", "phone": "256-574-7526 ext 226", "email": "brandy.hooper@rxaap.com"},
            {"name": "Trevor Bowen", "role": "IT (Scottsboro)", "phone": "256-574-6819 ext 214", "email": "trevor.bowen@apirx.com"},
            {"name": "Phil Horton", "role": "IT (Memphis)", "phone": "901-800-4605 ext 405", "email": "phil.horton@apirx.com"},
            {"name": "Austin Wilson", "role": "IT (AAP)", "phone": "256-218-5527 ext 527", "email": "austin.wilson@rxaap.com"},
        ],
        "quickLinks": [
            "Scottsboro API: 211 Lonnie E Crawford Blvd, Scottsboro, AL 35769",
            "Memphis API: 5375 Mineral Wells Road, Memphis, TN 38125",
            "AAP: 201 Lonnie E Crawford Blvd, Scottsboro, AL 35769",
        ],
        "reminders": [
            "Do not give legal, medical, or disciplinary opinions from the front desk.",
            "When the question is specific to an employee's circumstances, use the safe escalation script.",
            "A clean handoff is better than an overconfident wrong answer.",
        ],
    }
]


def get_experience_content() -> dict[str, Any]:
    return {
        "organization": ORGANIZATION,
        "dashboardStats": DASHBOARD_STATS,
        "contacts": CONTACTS,
        "sections": SECTIONS,
        "toolkits": TOOLKITS,
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
