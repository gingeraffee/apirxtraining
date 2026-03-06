
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

# -----------------------------------------------------------------------------
# Page setup
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AAP Onboarding Portal",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# Styling
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    .portal-hero {
        padding: 1.35rem 1.5rem;
        border-radius: 18px;
        background: linear-gradient(135deg, rgba(17, 52, 125, 0.08), rgba(220, 0, 30, 0.06));
        border: 1px solid rgba(17, 52, 125, 0.15);
        margin-bottom: 1rem;
    }
    .module-card {
        border: 1px solid rgba(49, 51, 63, 0.15);
        border-radius: 16px;
        padding: 1rem 1rem 0.85rem 1rem;
        background: rgba(255,255,255,0.72);
        box-shadow: 0 6px 18px rgba(0,0,0,0.04);
        min-height: 220px;
    }
    .pill {
        display: inline-block;
        padding: 0.20rem 0.55rem;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 0.55rem;
        background: rgba(17, 52, 125, 0.08);
        color: rgb(17, 52, 125);
    }
    .small-note {
        color: #5f6368;
        font-size: 0.92rem;
    }
    .section-box {
        border: 1px solid rgba(49, 51, 63, 0.12);
        border-radius: 16px;
        padding: 1rem 1rem 0.5rem 1rem;
        margin-bottom: 0.9rem;
        background: rgba(255,255,255,0.66);
    }
    .timeline-box {
        border-left: 4px solid #11347d;
        padding: 0.1rem 0 0.1rem 1rem;
        margin: 0.5rem 0 1rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
APP_DIR = Path(__file__).resolve().parent
LOGO_CANDIDATES = [
    APP_DIR / "AAP_API.PNG",
    APP_DIR / "aap_api.png",
    Path("/mnt/data/AAP_API.PNG"),  # helpful for local testing in ChatGPT
]

SHEET_REFERENCE = st.secrets.get("SPREADSHEET_ID", st.secrets.get("access_sheet_name", ""))
ACCESS_WORKSHEET = st.secrets.get("access_worksheet", "Access")
PROGRESS_WORKSHEET = st.secrets.get("progress_worksheet", "Progress")
STATIC_ACCESS_CODE = str(st.secrets.get("access_code", "")).strip()

CONTACT_BLOCK = {
    "name": "Nicole Thornton",
    "title": "HR Manager",
    "phone": "256-574-7528",
    "email": "nicole.thornton@apirx.com",
}

# -----------------------------------------------------------------------------
# Content
# -----------------------------------------------------------------------------
MODULES = [
    {
        "id": "welcome",
        "title": "Welcome to AAP",
        "blurb": "Company history, mission, vision, and guiding principles.",
        "sections": [
            {
                "title": "Who We Are",
                "body": [
                    "American Associated Pharmacies (AAP) is a national cooperative of more than 2,000 independent pharmacies.",
                    "AAP was formed in 2009 when United Drugs of Phoenix and Associated Pharmacies, Inc. (API) of Scottsboro joined forces.",
                    "AAP continues to operate API as its warehouse and distributor with two U.S. warehouse locations.",
                ],
            },
            {
                "title": "Our Mission and Vision",
                "body": [
                    "Mission: AAP provides support and customized solutions for independent community pharmacies to enhance profitability, streamline operations, and improve the quality of patient care.",
                    "Vision: Helping independent pharmacies thrive in a competitive healthcare market.",
                ],
            },
            {
                "title": "Values and Guiding Principles",
                "body": [
                    "Customer Focus — serve customers well internally and externally.",
                    "Integrity — act honestly and build trust.",
                    "Respect — treat others with dignity and encourage open communication.",
                    "Excellence — pursue quality, innovation, and continuous improvement.",
                    "Ownership — take responsibility and stay accountable.",
                ],
            },
        ],
        "checklist": [
            "I understand what AAP does and who it serves.",
            "I know AAP was formed in 2009 and continues to operate API.",
            "I can explain AAP’s mission and vision in plain language.",
            "I understand the five core value areas: Customer Focus, Integrity, Respect, Excellence, and Ownership.",
        ],
        "quiz": [
            {
                "question": "AAP was formed when two pharmacy cooperatives joined forces in:",
                "options": ["1999", "2009", "2014", "2020"],
                "answer": "2009",
            },
            {
                "question": "AAP’s vision is best described as:",
                "options": [
                    "Becoming the largest hospital chain in the Southeast",
                    "Helping independent pharmacies thrive in a competitive healthcare market",
                    "Selling direct-to-consumer medications nationwide",
                    "Replacing all local pharmacy distributors",
                ],
                "answer": "Helping independent pharmacies thrive in a competitive healthcare market",
            },
            {
                "question": "Which value focuses on taking responsibility when things go wrong?",
                "options": ["Respect", "Ownership", "Customer Focus", "Innovation"],
                "answer": "Ownership",
            },
            {
                "question": "AAP primarily supports:",
                "options": [
                    "Independent community pharmacies",
                    "National grocery chains only",
                    "Insurance carriers",
                    "Large hospital systems only",
                ],
                "answer": "Independent community pharmacies",
            },
        ],
    },
    {
        "id": "conduct",
        "title": "Code of Conduct and Ethics",
        "blurb": "Expected professional behavior, confidentiality, and ethical standards.",
        "sections": [
            {
                "title": "What AAP Expects",
                "body": [
                    "Work productively and pursue the company’s objectives without disrupting others.",
                    "Protect company assets, information, equipment, timekeeping accuracy, and business resources.",
                    "Treat coworkers, vendors, visitors, members, and other contacts with professionalism, dignity, and courtesy.",
                    "Use good judgment in e-mail, memos, notes, and other formal or informal business communication.",
                    "Report errors, omissions, suspected illegal activity, unethical behavior, and conflicts of interest.",
                ],
            },
            {
                "title": "Confidentiality and Professional Responsibility",
                "body": [
                    "Employees are expected to protect confidential information entrusted to them.",
                    "All employees sign a confidentiality and non-disclosure agreement upon hire.",
                    "Company systems and business communications should be used appropriately and professionally.",
                ],
            },
            {
                "title": "Examples of Unacceptable Conduct",
                "body": [
                    "Theft or inappropriate removal of property.",
                    "Falsification of records, including timekeeping records.",
                    "Working under the influence of alcohol or illegal drugs.",
                    "Threatening violence, harassment, insubordination, unsafe conduct, unauthorized disclosure of confidential information, or unauthorized use of company systems/equipment.",
                ],
            },
        ],
        "checklist": [
            "I understand that professionalism and respectful communication are required.",
            "I know that confidentiality and conflicts of interest must be taken seriously.",
            "I understand that falsifying records, harassment, threats, and misuse of company property can lead to discipline up to termination.",
            "I know I should report unethical or illegal behavior promptly.",
        ],
        "quiz": [
            {
                "question": "Which of the following is part of AAP’s Code of Conduct?",
                "options": [
                    "Use company systems however you want after work hours",
                    "Protect confidential information and company assets",
                    "Ignore small timekeeping errors",
                    "Keep concerns to yourself unless asked",
                ],
                "answer": "Protect confidential information and company assets",
            },
            {
                "question": "Which item is listed as unacceptable conduct?",
                "options": [
                    "Reporting an error to a supervisor",
                    "Taking ownership of a mistake",
                    "Falsifying timekeeping records",
                    "Using respectful language in e-mail",
                ],
                "answer": "Falsifying timekeeping records",
            },
            {
                "question": "Business communications should:",
                "options": [
                    "Include informal insults if no customer sees them",
                    "Be handled with judgment and discretion",
                    "Be sent from personal email whenever possible",
                    "Avoid documenting problems",
                ],
                "answer": "Be handled with judgment and discretion",
            },
            {
                "question": "Employees are expected to report known or suspected unethical behavior:",
                "options": ["Never", "Only after 90 days", "Immediately", "Only if a coworker agrees"],
                "answer": "Immediately",
            },
        ],
    },
    {
        "id": "attendance_pto",
        "title": "Attendance & PTO Policies",
        "blurb": "Attendance expectations, point system basics, PTO rules, and time-off increments.",
        "sections": [
            {
                "title": "Attendance Point Basics",
                "body": [
                    "AAP uses a no-fault attendance program for non-exempt employees.",
                    "Tardy up to 5 minutes is a grace period with 0 points.",
                    "Tardy or early leave of less than 4 hours = 0.5 points.",
                    "Full shift absence, tardy, or early leave of 4 hours or more = 1 point.",
                    "No-report absence or calling 15 minutes after the workday starts = 1.5 points.",
                    "Consecutive absences for the employee’s illness count as a single absence if supported by the required doctor’s note.",
                ],
            },
            {
                "title": "PTO and Request Rules",
                "body": [
                    "PTO cannot be used before it is accrued.",
                    "Planned time off should be submitted no later than 5:00 p.m. the day before time off is needed.",
                    "Unexpected personal leave should be reported to the supervisor before the scheduled start time whenever possible, and on each additional day of absence.",
                    "Vacation requests over five consecutive days require written approval by the Company President.",
                ],
            },
            {
                "title": "Vacation, Personal Leave, and Holidays",
                "body": [
                    "Regular full-time employees become eligible for vacation after 60 days of full-time service.",
                    "Vacation may be used in minimum increments of 2 hours.",
                    "Personal leave has a 60-day waiting period and may be requested in 1-hour increments.",
                    "Part-time employees earn personal leave at 1 hour for every 30 hours worked, subject to annual maximums based on length of service.",
                    "Holiday schedules and floating holiday rules apply by company policy and department staffing needs.",
                ],
            },
        ],
        "checklist": [
            "I understand the main point values for tardies, absences, and no-call/no-show situations.",
            "I know personal leave may be requested in 1-hour increments.",
            "I know vacation must be taken in at least 2-hour increments.",
            "I know planned PTO requests should be submitted by 5:00 p.m. the day before whenever possible.",
            "I understand PTO cannot be used before it is accrued.",
        ],
        "quiz": [
            {
                "question": "How many points does a tardy or early leave of less than 4 hours carry?",
                "options": ["0", "0.5", "1.0", "1.5"],
                "answer": "0.5",
            },
            {
                "question": "How may personal leave be requested?",
                "options": ["In 30-minute increments", "In 1-hour increments", "Only in full-day increments", "Only in 2-hour increments"],
                "answer": "In 1-hour increments",
            },
            {
                "question": "What is the minimum increment for vacation time?",
                "options": ["30 minutes", "1 hour", "2 hours", "4 hours"],
                "answer": "2 hours",
            },
            {
                "question": "A no-report absence or calling 15 minutes after the workday starts is:",
                "options": ["0 points", "0.5 points", "1 point", "1.5 points"],
                "answer": "1.5 points",
            },
            {
                "question": "Planned time off should generally be submitted no later than:",
                "options": [
                    "The end of the pay period",
                    "5:00 p.m. the day before the time off is needed",
                    "Seven days in advance only",
                    "After the time off is taken",
                ],
                "answer": "5:00 p.m. the day before the time off is needed",
            },
        ],
    },
    {
        "id": "workplace",
        "title": "Workplace Policies",
        "blurb": "Safety, conduct, dress code, technology use, schedules, and respect in the workplace.",
        "sections": [
            {
                "title": "Safety and Work Environment",
                "body": [
                    "Employees receive workplace safety training and are expected to follow safe work practices.",
                    "Unsafe conditions must be reported immediately to the appropriate supervisor.",
                    "All work-related accidents should be reported immediately, no matter how minor they may seem.",
                    "Smoking is only allowed in designated areas and only during scheduled breaks and lunch.",
                ],
            },
            {
                "title": "Schedules, Breaks, and Overtime",
                "body": [
                    "Work schedules vary by department and supervisors advise employees of their schedules.",
                    "Full-time nonexempt employees are provided with two paid 15-minute rest periods each workday.",
                    "Overtime must receive prior supervisor authorization.",
                    "Failure to work scheduled overtime or working overtime without approval may lead to discipline.",
                ],
            },
            {
                "title": "Technology, Visitors, and Expenses",
                "body": [
                    "Computers, files, e-mail, and software are company property intended for business use.",
                    "Employees should not access files or stored communications without authorization.",
                    "Computer and e-mail usage may be monitored.",
                    "Reasonable business travel expenses may be reimbursed; falsifying expense reports can lead to discipline.",
                    "Only authorized visitors are allowed in the workplace, and employees are responsible for the conduct and safety of their visitors.",
                ],
            },
            {
                "title": "Harassment, Violence, and Dress",
                "body": [
                    "AAP prohibits unlawful harassment and investigates complaints.",
                    "Workplace violence, threats, bullying, and behavior that causes others to feel unsafe are not tolerated.",
                    "Threatening behavior should be reported to management immediately.",
                    "Employees should maintain a neat, clean, well-groomed, and work-appropriate appearance.",
                ],
            },
        ],
        "checklist": [
            "I understand I must report unsafe conditions and work-related accidents right away.",
            "I know overtime must be approved in advance.",
            "I understand company technology is for business use and may be monitored.",
            "I know harassment, threats, and workplace violence are not tolerated.",
            "I understand the basic dress and appearance expectations.",
        ],
        "quiz": [
            {
                "question": "What should you do if you notice an unsafe condition?",
                "options": [
                    "Wait until the end of the week",
                    "Report it immediately",
                    "Only mention it if someone gets hurt",
                    "Post about it in a group chat first",
                ],
                "answer": "Report it immediately",
            },
            {
                "question": "Overtime should be worked:",
                "options": [
                    "Any time you choose",
                    "Only with prior supervisor authorization",
                    "Only on holidays",
                    "Without recording it if it is brief",
                ],
                "answer": "Only with prior supervisor authorization",
            },
            {
                "question": "Company computers and e-mail are:",
                "options": [
                    "Private personal systems once you log in",
                    "Company property intended for business use",
                    "Free for any outside business activity",
                    "Never monitored",
                ],
                "answer": "Company property intended for business use",
            },
            {
                "question": "AAP’s stance on workplace violence and threats is:",
                "options": [
                    "Allowed if there is no physical contact",
                    "Handled only by peers",
                    "Not tolerated",
                    "Only reviewed during annual evaluations",
                ],
                "answer": "Not tolerated",
            },
            {
                "question": "Personal appearance at work should be:",
                "options": [
                    "Neat, clean, well-groomed, and work-appropriate",
                    "Based only on personal preference",
                    "Ignored unless a customer complains",
                    "Unrelated to company expectations",
                ],
                "answer": "Neat, clean, well-groomed, and work-appropriate",
            },
        ],
    },
    {
        "id": "benefits",
        "title": "Benefits",
        "blurb": "Full-time and part-time benefit differences, timelines, and key coverage options.",
        "sections": [
            {
                "title": "Benefits Timeline",
                "body": [
                    "Day 1 (all employees): LinkedIn Learning, Employee Assistance Program (LifeMatters), and AAP Perks.",
                    "1st of the month after hire (all employees): Teladoc.",
                    "60 days: all employees may use Personal Time Off; full-time employees may also use Vacation Time.",
                    "1st of the month after 60 days (full-time): medical, dental, vision, 401(k), and supplemental coverages become available for enrollment.",
                    "Part-time 401(k): eligible after 1 year of service, 1,000 hours worked, and age 21+.",
                ],
            },
            {
                "title": "Full-Time Benefits",
                "body": [
                    "Medical plan choices include a PPO plan or HDHP with HSA.",
                    "Dental options include a Guardian Base Plan or High Plan.",
                    "Vision coverage is through Guardian.",
                    "Basic Life and AD&D is company-paid for eligible full-time employees.",
                    "Supplemental options may include voluntary life, spouse/dependent life, short-term disability, long-term disability, accident, cancer, and critical illness coverage.",
                    "401(k) company match: 100% of the first 3% contributed and 50% of the next 2%.",
                    "Long-Term Sick Leave becomes available at the 4-year milestone, then every 5 years after under policy rules.",
                ],
            },
            {
                "title": "All-Employee / Shared Benefits",
                "body": [
                    "LinkedIn Learning, LifeMatters EAP, AAP Perks, Teladoc, and Personal Time Off are shared benefits highlighted for employees.",
                    "Personal Time Off eligibility and usage rules still depend on policy timing and accrual.",
                    "Benefit questions or eligibility disputes should be directed to HR.",
                ],
            },
            {
                "title": "Part-Time Highlights",
                "body": [
                    "Part-time employees do not earn vacation under the uploaded materials.",
                    "Part-time personal leave accrues at 1 hour for every 30 hours worked.",
                    "Part-time employees may become eligible for 401(k) after 1 year, 1,000 hours worked, and age 21+.",
                    "The uploaded materials note that part-time employees do not receive company-paid life insurance.",
                ],
            },
        ],
        "checklist": [
            "I know which benefits are available on Day 1.",
            "I know Teladoc becomes available on the 1st of the month after hire.",
            "I understand full-time medical/dental/vision and 401(k) enrollment timing.",
            "I understand part-time personal leave accrual and 401(k) timing basics.",
            "I know to contact HR if I have questions about eligibility or enrollment.",
        ],
        "quiz": [
            {
                "question": "Which benefits are available to all employees on Day 1?",
                "options": [
                    "Medical, dental, and vision",
                    "LinkedIn Learning, EAP, and AAP Perks",
                    "Vacation and long-term sick leave",
                    "401(k) and HSA only",
                ],
                "answer": "LinkedIn Learning, EAP, and AAP Perks",
            },
            {
                "question": "When does Teladoc become available to all employees?",
                "options": [
                    "Day 1",
                    "After 30 calendar days exactly",
                    "The 1st of the month after hire",
                    "At the 90-day mark",
                ],
                "answer": "The 1st of the month after hire",
            },
            {
                "question": "Full-time medical, dental, vision, 401(k), and supplemental elections generally open:",
                "options": [
                    "Immediately on Day 1",
                    "At 60 days exactly, same day",
                    "On the 1st of the month after 60 days",
                    "After 1 full year",
                ],
                "answer": "On the 1st of the month after 60 days",
            },
            {
                "question": "AAP’s 401(k) company match is:",
                "options": [
                    "50% of all contributions",
                    "100% of the first 3% and 50% of the next 2%",
                    "A flat 1% annually",
                    "Not available until 5 years",
                ],
                "answer": "100% of the first 3% and 50% of the next 2%",
            },
            {
                "question": "Part-time personal leave generally accrues at:",
                "options": [
                    "2 hours per 30 hours worked",
                    "1 day per month",
                    "1 hour for every 30 hours worked",
                    "It does not accrue at all",
                ],
                "answer": "1 hour for every 30 hours worked",
            },
        ],
    },
    {
        "id": "first_steps",
        "title": "First Steps",
        "blurb": "What to do next, system setup, and your 30/60/90-day onboarding roadmap.",
        "sections": [
            {
                "title": "Immediate Setup Tasks",
                "body": [
                    "Verify your account access and make sure required systems are working.",
                    "Complete and sign all new-hire documents.",
                    "Provide acceptable I-9 documentation and complete work authorization steps.",
                    "Register for Paylocity and confirm payroll details.",
                    "Download the BambooHR app and log in.",
                    "Activate LinkedIn Learning and enter your email to get started.",
                ],
            },
            {
                "title": "Helpful Links",
                "body": [
                    "LinkedIn Learning: https://linkedin.com/learning",
                    "BambooHR: https://www.aap.bamboohr.com",
                    "Paylocity: https://www.access.paylocity.com",
                ],
            },
            {
                "title": "Day 1–30",
                "body": [
                    "Complete orientation.",
                    "Sign all paperwork.",
                    "Get access to systems.",
                    "Meet your team.",
                    "Shadow key processes.",
                    "Complete your 30-day survey.",
                ],
            },
            {
                "title": "Day 31–60",
                "body": [
                    "Begin independently executing core responsibilities.",
                    "Complete your 60-day survey.",
                    "Become eligible for PTO and holiday-related milestones as policy timing allows.",
                    "Reach the end of the probationary period.",
                    "Set a goal for yourself for the next 30 days and inform your supervisor.",
                ],
            },
            {
                "title": "Day 61–90",
                "body": [
                    "Build confidence and consistency in your role.",
                    "Identify opportunities for improvement.",
                    "Have your first performance review.",
                    "Review benefit eligibility and next enrollment steps as applicable to your status.",
                ],
            },
        ],
        "checklist": [
            "I know I need to verify account access and complete new-hire documents.",
            "I know I need to provide I-9 documents and register for Paylocity.",
            "I know I should download BambooHR and activate LinkedIn Learning.",
            "I understand the general Day 1–30, 31–60, and 61–90 onboarding timeline.",
        ],
        "quiz": [
            {
                "question": "Which task belongs in your first steps?",
                "options": [
                    "Ignore account issues until your annual review",
                    "Wait 90 days to complete paperwork",
                    "Verify access, complete documents, and register for systems",
                    "Skip I-9 documentation if you know your supervisor",
                ],
                "answer": "Verify access, complete documents, and register for systems",
            },
            {
                "question": "Which site is listed for LinkedIn Learning activation?",
                "options": [
                    "linkedin.com/careers",
                    "linkedin.com/learning",
                    "learning.linkedinjobs.com",
                    "my.linkedinhr.com",
                ],
                "answer": "linkedin.com/learning",
            },
            {
                "question": "Which milestone is part of Day 1–30?",
                "options": [
                    "Annual open enrollment only",
                    "Meet your team and complete orientation",
                    "Retirement exit interview",
                    "Five-year service award",
                ],
                "answer": "Meet your team and complete orientation",
            },
            {
                "question": "During Day 31–60, employees are expected to:",
                "options": [
                    "Avoid setting goals",
                    "Begin independently executing core responsibilities",
                    "Ignore surveys",
                    "Stop meeting with their supervisor",
                ],
                "answer": "Begin independently executing core responsibilities",
            },
        ],
    },
]


# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------
def norm_text(value: Any) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def digits_only(value: Any) -> str:
    return re.sub(r"\D", "", str(value or ""))


def header_key(value: Any) -> str:
    text = str(value or "").strip().lower()
    return re.sub(r"[^a-z0-9]+", "_", text).strip("_")


def find_logo_path() -> Path | None:
    for candidate in LOGO_CANDIDATES:
        if candidate.exists():
            return candidate
    return None


@st.cache_resource(show_spinner=False)
def get_gsheet_client():
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except Exception:
        return None

    service_info = None

    if "gcp_service_account" in st.secrets:
        service_info = dict(st.secrets["gcp_service_account"])
    elif "GOOGLE_SERVICE_ACCOUNT" in os.environ:
        try:
            service_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT"])
        except json.JSONDecodeError:
            service_info = None

    if not service_info:
        return None

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.readonly",
    ]
    creds = Credentials.from_service_account_info(service_info, scopes=scopes)
    return gspread.authorize(creds)


def open_sheet(workbook_ref: str, worksheet_name: str):
    client = get_gsheet_client()
    if not client or not workbook_ref:
        return None

    workbook_ref = str(workbook_ref).strip()
    try:
        if re.fullmatch(r"[A-Za-z0-9-_]{20,}", workbook_ref):
            wb = client.open_by_key(workbook_ref)
        else:
            wb = client.open(workbook_ref)
        return wb.worksheet(worksheet_name)
    except Exception:
        return None


def detect_columns(headers: list[str]) -> dict[str, str | None]:
    key_map = {header_key(h): h for h in headers}

    def pick(candidates: list[str]) -> str | None:
        for candidate in candidates:
            if candidate in key_map:
                return key_map[candidate]
        return None

    return {
        "full_name": pick(
            [
                "full_name",
                "employee_name",
                "name",
                "fulllegalname",
                "employee_full_name",
            ]
        ),
        "employee_number": pick(
            [
                "employee_number",
                "employee_no",
                "emp_number",
                "emp_no",
                "employee",
                "id",
                "employee_id",
            ]
        ),
        "access_code": pick(
            [
                "access_code",
                "code",
                "portal_code",
                "login_code",
            ]
        ),
        "location": pick(["location", "site", "building"]),
        "department": pick(["department", "dept"]),
        "title": pick(["title", "job_title", "position"]),
    }


def validate_login(access_code: str, employee_number: str, full_name: str):
    access_code = str(access_code or "").strip()
    employee_number_digits = digits_only(employee_number)
    full_name_norm = norm_text(full_name)

    ws = open_sheet(SHEET_REFERENCE, ACCESS_WORKSHEET)
    if ws is None:
        if STATIC_ACCESS_CODE and access_code == STATIC_ACCESS_CODE and employee_number_digits and full_name_norm:
            return {
                "full_name": full_name.strip(),
                "employee_number": employee_number_digits,
                "department": "",
                "location": "",
                "title": "",
                "validation_mode": "access_code_only",
            }, None
        return None, "Login sheet could not be reached. Check Streamlit secrets or worksheet settings."

    try:
        values = ws.get_all_values()
    except Exception:
        values = []

    if not values or len(values) < 2:
        return None, "The access worksheet is empty or missing employee rows."

    headers = values[0]
    rows = values[1:]
    columns = detect_columns(headers)

    full_name_col = columns["full_name"] or (headers[2] if len(headers) > 2 else None)
    employee_col = columns["employee_number"] or (headers[1] if len(headers) > 1 else None)
    access_col = columns["access_code"] or (headers[0] if len(headers) > 0 else None)

    if not full_name_col or not employee_col:
        return None, "The access worksheet needs name and employee number columns."

    records = []
    for row in rows:
        padded = row + [""] * (len(headers) - len(row))
        record = dict(zip(headers, padded))
        records.append(record)

    for record in records:
        record_name = norm_text(record.get(full_name_col, ""))
        record_emp = digits_only(record.get(employee_col, ""))
        record_code = str(record.get(access_col, "")).strip() if access_col else ""

        name_match = record_name == full_name_norm
        emp_match = record_emp == employee_number_digits

        if not (name_match and emp_match):
            continue

        if access_col:
            if access_code != record_code:
                return None, "Access code is incorrect for that employee record."
        elif STATIC_ACCESS_CODE and access_code != STATIC_ACCESS_CODE:
            return None, "Access code is incorrect."

        return {
            "full_name": record.get(full_name_col, full_name.strip()) or full_name.strip(),
            "employee_number": record.get(employee_col, employee_number_digits) or employee_number_digits,
            "department": record.get(columns["department"] or "", ""),
            "location": record.get(columns["location"] or "", ""),
            "title": record.get(columns["title"] or "", ""),
            "validation_mode": "google_sheet",
        }, None

    return None, "No matching employee record was found. Check the employee number and full name."


def init_state():
    st.session_state.setdefault("authenticated", False)
    st.session_state.setdefault("employee", {})
    st.session_state.setdefault("current_page", "home")
    st.session_state.setdefault("quiz_scores", {})
    st.session_state.setdefault("quiz_passed", {})
    st.session_state.setdefault("progress_loaded", False)


def module_checkbox_key(module_id: str, idx: int) -> str:
    return f"check::{module_id}::{idx}"


def all_checklist_done(module_id: str, items: list[str]) -> bool:
    return all(st.session_state.get(module_checkbox_key(module_id, i), False) for i in range(len(items)))


def module_progress(module: dict) -> dict[str, Any]:
    checklist_complete = all_checklist_done(module["id"], module["checklist"])
    quiz_score = st.session_state["quiz_scores"].get(module["id"], 0)
    quiz_passed = st.session_state["quiz_passed"].get(module["id"], False)
    complete = checklist_complete and quiz_passed
    return {
        "checklist_complete": checklist_complete,
        "quiz_score": quiz_score,
        "quiz_passed": quiz_passed,
        "complete": complete,
    }


def overall_progress() -> tuple[int, int, float]:
    completed = 0
    total = len(MODULES)
    for module in MODULES:
        if module_progress(module)["complete"]:
            completed += 1
    pct = (completed / total) if total else 0.0
    return completed, total, pct


def load_saved_progress():
    if st.session_state.get("progress_loaded"):
        return

    employee = st.session_state.get("employee", {})
    emp_no = digits_only(employee.get("employee_number", ""))
    if not emp_no:
        st.session_state["progress_loaded"] = True
        return

    ws = open_sheet(SHEET_REFERENCE, PROGRESS_WORKSHEET)
    if ws is None:
        st.session_state["progress_loaded"] = True
        return

    try:
        records = ws.get_all_records()
    except Exception:
        st.session_state["progress_loaded"] = True
        return

    for record in records:
        if digits_only(record.get("employee_number", "")) != emp_no:
            continue

        module_id = str(record.get("module_id", "")).strip()
        if not module_id:
            continue

        try:
            checklist_state = json.loads(record.get("checklist_state_json", "{}") or "{}")
        except Exception:
            checklist_state = {}

        for idx_str, value in checklist_state.items():
            st.session_state[module_checkbox_key(module_id, int(idx_str))] = bool(value)

        try:
            st.session_state["quiz_scores"][module_id] = int(float(record.get("quiz_score", 0) or 0))
        except Exception:
            st.session_state["quiz_scores"][module_id] = 0

        raw_passed = str(record.get("quiz_passed", "")).strip().lower()
        st.session_state["quiz_passed"][module_id] = raw_passed in {"true", "1", "yes", "y"}

    st.session_state["progress_loaded"] = True


def save_module_progress(module: dict):
    employee = st.session_state.get("employee", {})
    emp_no = digits_only(employee.get("employee_number", ""))
    full_name = employee.get("full_name", "")
    if not emp_no:
        return

    ws = open_sheet(SHEET_REFERENCE, PROGRESS_WORKSHEET)
    if ws is None:
        return

    checklist_state = {
        str(i): bool(st.session_state.get(module_checkbox_key(module["id"], i), False))
        for i in range(len(module["checklist"]))
    }
    progress = module_progress(module)

    header = [
        "employee_number",
        "full_name",
        "module_id",
        "checklist_state_json",
        "checklist_complete",
        "quiz_score",
        "quiz_passed",
        "updated_at",
    ]
    row_values = [
        emp_no,
        full_name,
        module["id"],
        json.dumps(checklist_state),
        str(progress["checklist_complete"]),
        str(progress["quiz_score"]),
        str(progress["quiz_passed"]),
        datetime.now().isoformat(timespec="seconds"),
    ]

    try:
        current = ws.get_all_values()
        if not current:
            ws.append_row(header, value_input_option="RAW")
            current = [header]

        if current[0] != header:
            # Best effort: only create expected headers if sheet is blank.
            pass

        target_row_number = None
        for row_number, row in enumerate(current[1:], start=2):
            padded = row + [""] * (len(header) - len(row))
            if digits_only(padded[0]) == emp_no and str(padded[2]).strip() == module["id"]:
                target_row_number = row_number
                break

        if target_row_number:
            ws.update(f"A{target_row_number}:H{target_row_number}", [row_values])
        else:
            ws.append_row(row_values, value_input_option="RAW")
    except Exception:
        return


# -----------------------------------------------------------------------------
# Rendering helpers
# -----------------------------------------------------------------------------
def render_sidebar():
    with st.sidebar:
        logo_path = find_logo_path()
        if logo_path:
            st.image(str(logo_path), use_container_width=True)

        st.markdown("---")

        if st.session_state.get("authenticated"):
            employee = st.session_state.get("employee", {})
            st.subheader("Employee")
            st.write(f"**Name:** {employee.get('full_name', '')}")
            st.write(f"**Employee #:** {employee.get('employee_number', '')}")
            if employee.get("title"):
                st.write(f"**Title:** {employee.get('title')}")
            if employee.get("department"):
                st.write(f"**Department:** {employee.get('department')}")
            if employee.get("location"):
                st.write(f"**Location:** {employee.get('location')}")

            st.markdown("---")
            st.subheader("Navigation")
            nav_labels = {
                "home": "Home",
                "welcome": "Welcome to AAP",
                "conduct": "Code of Conduct and Ethics",
                "attendance_pto": "Attendance & PTO Policies",
                "workplace": "Workplace Policies",
                "benefits": "Benefits",
                "first_steps": "First Steps",
            }
            page = st.radio(
                "Go to",
                list(nav_labels.keys()),
                index=list(nav_labels.keys()).index(st.session_state.get("current_page", "home")),
                format_func=lambda x: nav_labels[x],
                label_visibility="collapsed",
            )
            st.session_state["current_page"] = page

            completed, total, pct = overall_progress()
            st.markdown("---")
            st.subheader("Progress")
            st.progress(pct)
            st.caption(f"{completed} of {total} modules completed")

            if st.button("Log out", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

        st.markdown("---")
        st.subheader("HR Contact")
        st.write(f"**{CONTACT_BLOCK['name']}**")
        st.write(CONTACT_BLOCK["title"])
        st.write(CONTACT_BLOCK["phone"])
        st.write(CONTACT_BLOCK["email"])


def render_login():
    st.markdown(
        """
        <div class="portal-hero">
            <h1 style="margin-bottom:0.25rem;">AAP Employee Onboarding Portal</h1>
            <div class="small-note">
                Welcome aboard. Enter your access code, employee number, and full name to begin orientation.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.2, 0.8], gap="large")

    with left:
        st.subheader("Sign in")
        with st.form("login_form", clear_on_submit=False):
            access_code = st.text_input("Access Code", type="password", placeholder="Enter your access code")
            employee_number = st.text_input("Employee #", placeholder="Enter your employee number")
            full_name = st.text_input("Full Name", placeholder="Enter your full legal name")
            submitted = st.form_submit_button("Enter Portal", use_container_width=True)

        if submitted:
            if not access_code or not employee_number or not full_name:
                st.error("Please complete all three login fields.")
            else:
                employee, error = validate_login(access_code, employee_number, full_name)
                if error:
                    st.error(error)
                else:
                    st.session_state["authenticated"] = True
                    st.session_state["employee"] = employee
                    st.session_state["current_page"] = "home"
                    st.session_state["progress_loaded"] = False
                    load_saved_progress()
                    st.rerun()

    with right:
        st.markdown(
            """
            <div class="section-box">
                <h4>What’s inside</h4>
                <ul>
                    <li>Welcome to AAP</li>
                    <li>Code of Conduct and Ethics</li>
                    <li>Attendance &amp; PTO Policies</li>
                    <li>Workplace Policies</li>
                    <li>Benefits</li>
                    <li>First Steps</li>
                </ul>
                <p class="small-note">
                    Each module includes a quick summary, a checklist of understanding, and a quiz.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.info(
            "This portal is a training summary designed for onboarding. Official handbook language, policy documents, and HR guidance control if anything changes or conflicts."
        )


def render_home():
    employee = st.session_state.get("employee", {})
    completed, total, pct = overall_progress()

    st.markdown(
        f"""
        <div class="portal-hero">
            <h1 style="margin-bottom:0.25rem;">Welcome, {employee.get("full_name", "Employee")} 👋</h1>
            <div class="small-note">
                Start with the module list below, track your progress, and work through each section at your own pace.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Modules Completed", f"{completed}/{total}")
    c2.metric("Overall Progress", f"{int(pct * 100)}%")
    avg_quiz = 0
    if MODULES:
        scores = [st.session_state["quiz_scores"].get(m["id"], 0) for m in MODULES]
        avg_quiz = round(sum(scores) / len(scores))
    c3.metric("Average Quiz Score", f"{avg_quiz}%")

    st.progress(pct)

    st.markdown("### Training Modules")
    cols = st.columns(2, gap="large")
    for idx, module in enumerate(MODULES):
        target_col = cols[idx % 2]
        progress = module_progress(module)
        status = "✅ Complete" if progress["complete"] else "🟡 In Progress" if (progress["checklist_complete"] or progress["quiz_score"]) else "⬜ Not Started"

        with target_col:
            st.markdown(
                f"""
                <div class="module-card">
                    <div class="pill">{status}</div>
                    <h4 style="margin-top:0.1rem;">{module["title"]}</h4>
                    <p>{module["blurb"]}</p>
                    <p class="small-note">
                        Checklist: {"Done" if progress["checklist_complete"] else "Pending"}<br>
                        Quiz: {progress["quiz_score"]}% {"(passed)" if progress["quiz_passed"] else ""}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Open {module['title']}", key=f"open_{module['id']}", use_container_width=True):
                st.session_state["current_page"] = module["id"]
                st.rerun()

    st.markdown("### Orientation Notes")
    st.info(
        "Your checklist + quiz progress can be stored in a Google Sheet when the optional Progress worksheet is configured. If it is not configured, progress still works for the current session."
    )


def render_module(module: dict):
    progress = module_progress(module)

    st.markdown(
        f"""
        <div class="portal-hero">
            <h1 style="margin-bottom:0.25rem;">{module["title"]}</h1>
            <div class="small-note">{module["blurb"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    top1, top2, top3 = st.columns(3)
    top1.metric("Checklist", "Complete" if progress["checklist_complete"] else "In Progress")
    top2.metric("Quiz Score", f"{progress['quiz_score']}%")
    top3.metric("Module Status", "Complete" if progress["complete"] else "Not Complete")

    st.caption("Training summary only — official policy documents and HR guidance control in the event of a conflict.")

    content_tab, checklist_tab, quiz_tab = st.tabs(["Overview", "Checklist of Understanding", "Quiz"])

    with content_tab:
        for section in module["sections"]:
            st.markdown(f'<div class="section-box">', unsafe_allow_html=True)
            st.subheader(section["title"])
            for bullet in section["body"]:
                st.markdown(f"- {bullet}")
            st.markdown("</div>", unsafe_allow_html=True)

        if module["id"] == "first_steps":
            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            st.subheader("90-Day Onboarding Roadmap")
            st.markdown('<div class="timeline-box"><strong>Day 1–30</strong><br>Complete orientation, paperwork, system setup, team introductions, process shadowing, and your 30-day survey.</div>', unsafe_allow_html=True)
            st.markdown('<div class="timeline-box"><strong>Day 31–60</strong><br>Begin owning core responsibilities, complete your 60-day survey, reach probation milestones, and set a goal with your supervisor.</div>', unsafe_allow_html=True)
            st.markdown('<div class="timeline-box"><strong>Day 61–90</strong><br>Build confidence, identify improvements, complete your first performance review, and review benefit next steps where applicable.</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with checklist_tab:
        st.write("Check each item once you understand it.")
        changed = False
        for i, item in enumerate(module["checklist"]):
            key = module_checkbox_key(module["id"], i)
            before = st.session_state.get(key, False)
            after = st.checkbox(item, key=key)
            if after != before:
                changed = True

        progress = module_progress(module)
        if progress["checklist_complete"]:
            st.success("Nice — your understanding checklist is complete.")
        else:
            st.info("Complete every checkbox to finish this part of the module.")

        if changed:
            save_module_progress(module)

    with quiz_tab:
        st.write("Score 80% or higher to pass the module quiz.")
        with st.form(f"quiz_form::{module['id']}"):
            responses = {}
            for idx, item in enumerate(module["quiz"]):
                responses[idx] = st.radio(
                    item["question"],
                    item["options"],
                    key=f"quiz::{module['id']}::{idx}",
                    index=None,
                )
            submitted = st.form_submit_button("Submit Quiz", use_container_width=True)

        if submitted:
            total = len(module["quiz"])
            correct = 0
            for idx, item in enumerate(module["quiz"]):
                if responses.get(idx) == item["answer"]:
                    correct += 1

            score = int(round((correct / total) * 100)) if total else 0
            passed = score >= 80
            st.session_state["quiz_scores"][module["id"]] = score
            st.session_state["quiz_passed"][module["id"]] = passed
            save_module_progress(module)

            if passed:
                st.success(f"Quiz passed — {score}%")
            else:
                st.warning(f"Quiz score: {score}%. Review the module and try again.")

        stored_score = st.session_state["quiz_scores"].get(module["id"])
        if stored_score is not None and module["id"] in st.session_state["quiz_scores"]:
            stored_passed = st.session_state["quiz_passed"].get(module["id"], False)
            st.caption(f"Latest saved score: {stored_score}% {'• passed' if stored_passed else '• not yet passed'}")


# -----------------------------------------------------------------------------
# App flow
# -----------------------------------------------------------------------------
init_state()
render_sidebar()

if not st.session_state.get("authenticated"):
    render_login()
else:
    load_saved_progress()
    current_page = st.session_state.get("current_page", "home")
    if current_page == "home":
        render_home()
    else:
        selected = next((m for m in MODULES if m["id"] == current_page), None)
        if selected is None:
            st.session_state["current_page"] = "home"
            st.rerun()
        render_module(selected)
