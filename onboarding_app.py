import base64
import os
from dataclasses import dataclass
from typing import Any, Dict, List

import gspread
import streamlit as st

st.set_page_config(page_title="AAP Onboarding Experience", page_icon="✨", layout="wide", initial_sidebar_state="expanded")


# =========================
# Data model
# =========================

@dataclass(frozen=True)
class ModuleSpec:
    key: str
    number: str
    title: str
    subtitle: str
    summary: str
    image: str
    checklist_count: int


MODULES: List[ModuleSpec] = [
    ModuleSpec(
        key="welcome",
        number="01",
        title="Welcome to AAP",
        subtitle="Your first look at AAP's mission, story, and values.",
        summary="Company history, mission, vision & guiding principles",
        image="https://images.unsplash.com/photo-1521791136064-7986c2920216?auto=format&fit=crop&w=1800&q=80",
        checklist_count=4,
    ),
    ModuleSpec(
        key="conduct",
        number="02",
        title="Code of Conduct & Ethics",
        subtitle="How we work with trust, fairness, and accountability.",
        summary="Ethics, confidentiality & professional conduct standards",
        image="https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=1800&q=80",
        checklist_count=4,
    ),
    ModuleSpec(
        key="attendance",
        number="03",
        title="Attendance & PTO Policies",
        subtitle="Time-off, attendance expectations, and point system.",
        summary="PTO accruals, point system, holidays & leave policies",
        image="https://images.unsplash.com/photo-1506784365847-bbad939e9335?auto=format&fit=crop&w=1800&q=80",
        checklist_count=5,
    ),
    ModuleSpec(
        key="workplace",
        number="04",
        title="Workplace Policies",
        subtitle="Safety, technology, conduct, and respect in daily work.",
        summary="Safety, dress code, technology, harassment & conduct",
        image="https://images.unsplash.com/photo-1497366811353-6870744d04b2?auto=format&fit=crop&w=1800&q=80",
        checklist_count=5,
    ),
    ModuleSpec(
        key="benefits",
        number="05",
        title="Benefits Overview",
        subtitle="Health, retirement, and support resources available to you.",
        summary="Medical, dental, vision, 401(k) & supplemental coverage",
        image="https://images.unsplash.com/photo-1579621970588-a35d0e7ab9b6?auto=format&fit=crop&w=1800&q=80",
        checklist_count=5,
    ),
    ModuleSpec(
        key="firststeps",
        number="06",
        title="First Steps",
        subtitle="Critical actions and your 90-day onboarding roadmap.",
        summary="System access, onboarding checklist & 90-day roadmap",
        image="https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1800&q=80",
        checklist_count=6,
    ),
]
MODULE_INDEX = {m.key: m for m in MODULES}

SESSION_DEFAULTS: Dict[str, Any] = {
    "logged_in": False,
    "emp_name": "",
    "emp_number": "",
    "emp_department": "",
    "emp_position": "",
    "emp_start_date": "",
    "emp_track": "general",
    "current_page": "home",
    "current_module": None,
    "audio_enabled": True,
    "last_sound": "",
}

MODULE_CONTENT: Dict[str, Dict[str, Any]] = {
    "welcome": {
        "sections": [
            {
                "type": "markdown",
                "title": "Who We Are",
                "body": """
American Associated Pharmacies (AAP) is a national cooperative of more than **2,000 independent pharmacies**.
Founded in 2009 when **United Drugs** (Phoenix, AZ) and **Associated Pharmacies, Inc. (API)** (Scottsboro, AL)
merged to form one of the largest independent pharmacy organizations in America.

Today, AAP operates API with two U.S. warehouse locations, providing member-focused support,
innovative programs, and significant cost savings through its Prime Vendor Agreement.
                """,
            },
            {
                "type": "callout",
                "style": "info",
                "body": "AAP saves its member pharmacies millions in operating and acquisition costs every year through its competitive Prime Vendor Agreement.",
            },
            {
                "type": "bullets",
                "title": "Our Core Values",
                "items": [
                    "🎯 **Customer Focus** — Customer service is an attitude, not a department.",
                    "⚖️ **Integrity** — We act honestly and build trust through consistency.",
                    "🤝 **Respect** — We treat others with dignity and encourage open communication.",
                    "⭐ **Excellence** — We pursue quality, innovation, and continuous improvement.",
                    "🔑 **Ownership** — We take responsibility and stay accountable.",
                ],
            },
        ],
        "quiz": [
            {"q": "When was AAP formed?", "options": ["2001", "2005", "2009", "2012"], "answer": 2},
            {"q": "AAP is a cooperative of approximately how many pharmacies?", "options": ["500", "1,000", "2,000", "5,000"], "answer": 2},
            {"q": "Which is NOT one of AAP's five core values?", "options": ["Customer Focus", "Integrity", "Profitability", "Ownership"], "answer": 2},
            {"q": "What is AAP's vision statement?", "options": ["To be the largest pharmacy chain", "Helping independent pharmacies thrive in a competitive healthcare market", "Maximizing shareholder value", "Providing the lowest drug prices"], "answer": 1},
        ],
        "checklist": [
            "I understand AAP's history and formation.",
            "I can identify the mission and vision statements.",
            "I know the five core values and what they mean.",
            "I understand that AAP is a cooperative serving independent pharmacies.",
        ],
    },
    "conduct": {
        "sections": [
            {"type": "markdown", "title": "Business Ethics & Conduct", "body": "The success of AAP depends on customer trust. Every employee must act with honesty, integrity, and legal compliance. Illegal, dishonest, or unethical behavior can result in disciplinary action up to termination."},
            {"type": "tabs", "title": "Key Policies", "tabs": {
                "Conflicts of Interest": "Employees must avoid actual or potential conflicts of interest in all business dealings.",
                "Confidentiality": "All employees sign a confidentiality and non-disclosure agreement upon hire. Company systems and files may be monitored.",
                "Outside Employment": "Outside work is permitted if it does not interfere with performance or create a conflict.",
                "Equal Opportunity": "AAP bases employment decisions on merit and prohibits discrimination and retaliation.",
            }},
            {"type": "bullets", "title": "Problem Resolution Process", "items": [
                "1) Raise concerns with your immediate supervisor (or HR if appropriate).",
                "2) If unresolved, escalate: VP → President → CEO.",
                "3) CEO has authority to resolve the matter.",
                "4) Board review is available as a final step.",
            ]},
        ],
        "quiz": [
            {"q": "What must all employees sign upon hire?", "options": ["Non-compete agreement", "Confidentiality and non-disclosure agreement", "Social media policy", "Union membership form"], "answer": 1},
            {"q": "What system does AAP use to verify work authorization?", "options": ["HIPAA", "E-Verify", "ADP Screening", "LinkedIn"], "answer": 1},
            {"q": "Who should you approach first with a workplace concern?", "options": ["CEO", "A coworker", "Your immediate supervisor or HR", "An attorney"], "answer": 2},
            {"q": "Outside employment is allowed as long as:", "options": ["You work under 20 hours elsewhere", "You satisfactorily perform your AAP responsibilities", "Your manager gives verbal approval", "It is in a different industry"], "answer": 1},
        ],
        "checklist": [
            "I understand AAP's ethics expectations and my responsibility.",
            "I understand the confidentiality and NDA requirements.",
            "I know the problem resolution steps for workplace concerns.",
            "I understand the equal employment opportunity policy.",
        ],
    },
    "attendance": {
        "sections": [
            {"type": "markdown", "title": "Vacation Benefits", "body": "Regular full-time employees have a 60-day waiting period and vacation can be used in 2-hour increments."},
            {"type": "table", "columns": ["Length of Employment", "Paid Days / Year", "Accrual Rate"], "rows": [
                ["60 days – 1st Anniversary", "3 days (24 hrs)", "0.46 hrs/week"],
                ["1st – 2nd Anniversary", "5 days (40 hrs)", "0.77 hrs/week"],
                ["2nd – 3rd Anniversary", "7 days (56 hrs)", "1.07 hrs/week"],
                ["3rd – 5th Anniversary", "10 days (80 hrs)", "1.54 hrs/week"],
                ["5th – 9th Anniversary", "15 days (120 hrs)", "2.31 hrs/week"],
                ["10th – 19th Anniversary", "17 days (136 hrs)", "2.62 hrs/week"],
                ["20th Anniversary+", "19 days (152 hrs)", "2.93 hrs/week"],
            ]},
            {"type": "callout", "style": "warn", "body": "Two consecutive days absent without reporting in is considered voluntary resignation."},
        ],
        "quiz": [
            {"q": "What is the minimum increment for vacation time?", "options": ["1 hour", "2 hours", "4 hours", "8 hours"], "answer": 1},
            {"q": "What is the minimum increment for personal leave?", "options": ["1 hour", "2 hours", "4 hours", "8 hours"], "answer": 0},
            {"q": "How many points does a no-call absence carry?", "options": ["½ point", "1 point", "1½ points", "2 points"], "answer": 2},
            {"q": "At how many points does termination occur?", "options": ["6", "7", "8", "10"], "answer": 2},
            {"q": "Consecutive no-call days that equals resignation?", "options": ["1", "2", "3", "5"], "answer": 1},
        ],
        "checklist": [
            "I understand the vacation accrual schedule and 2-hour minimum.",
            "I understand personal leave uses 1-hour increments and forfeits at year-end.",
            "I know the holiday and floating holiday rules.",
            "I understand the attendance point system and corrective action thresholds.",
            "I understand that 2 consecutive no-call days is considered voluntary resignation.",
        ],
    },
    "workplace": {
        "sections": [
            {"type": "tabs", "title": "Policy Areas", "tabs": {
                "Dress Code": "Employees must maintain a neat, clean, work-appropriate appearance. Strong scents and offensive messaging are not acceptable.",
                "Safety": "Unsafe conditions and injuries must be reported immediately. Work accidents require immediate drug/alcohol testing.",
                "Drug & Alcohol": "AAP maintains a zero-tolerance workplace. Random testing may occur.",
                "Computer & Email": "All systems are company property and may be monitored. Offensive/illegal content is prohibited.",
                "Harassment": "Zero tolerance for harassment and retaliation. Report concerns to supervisor, HR, or VP HR.",
                "Other": "Overtime requires prior approval. Workplace violence is zero tolerance. Travel expenses must be truthful.",
            }},
        ],
        "quiz": [
            {"q": "What happens after a work-related accident?", "options": ["Nothing unless serious", "Incident report only", "Immediate drug and alcohol testing", "Employee goes home"], "answer": 2},
            {"q": "AAP's computer systems are:", "options": ["Personal property", "Company property, may be monitored", "Free for personal use", "Monitored only in investigations"], "answer": 1},
            {"q": "If harassed, what should you do first?", "options": ["Post online", "Ignore it", "Tell offender to stop or report to HR", "Confront publicly"], "answer": 2},
            {"q": "Overtime requires:", "options": ["Coworker approval", "Prior supervisor approval", "After-the-fact report", "Self-authorization"], "answer": 1},
        ],
        "checklist": [
            "I understand dress code expectations.",
            "I understand safety reporting requirements.",
            "I understand the drug and alcohol policy.",
            "I understand computer/email monitoring.",
            "I know how to report harassment.",
        ],
    },
    "benefits": {
        "sections": [
            {"type": "callout", "style": "info", "body": "Full-time employees (30+ hrs/week) enroll within 30 days. Benefits become effective the 1st of the month after 60 days."},
            {"type": "tabs", "title": "Benefits", "tabs": {
                "Full-Time": "Medical (PPO/HDHP), Dental, Vision, Basic Life/AD&D, LTD/STD, supplemental options, and 401(k) with up to 4% employer match on 5% contribution.",
                "All Employees": "Teladoc, LifeMatters EAP, LinkedIn Learning, BenefitHub perks, and PTO support are available for all employees.",
            }},
        ],
        "quiz": [
            {"q": "When do full-time benefits become effective?", "options": ["Day 1", "After 30 days", "1st of month after 60 days", "After 90 days"], "answer": 2},
            {"q": "401(k) match if you contribute 5%?", "options": ["2%", "3%", "4%", "5%"], "answer": 2},
            {"q": "Which benefit is free for ALL employees?", "options": ["Dental", "Short-term disability", "Teladoc", "Vision"], "answer": 2},
            {"q": "Basic Life/AD&D is provided at:", "options": ["50% employer-paid", "No cost to employee", "Employee-paid", "Enrollment required"], "answer": 1},
        ],
        "checklist": [
            "I understand the two medical plans.",
            "I know the 401(k) match.",
            "I know which benefits are free for everyone.",
            "I know enrollment is within 30 days.",
            "I understand supplemental options.",
        ],
    },
    "firststeps": {
        "sections": [
            {"type": "bullets", "title": "Immediate Action Items", "items": [
                "Verify account access (email + systems).",
                "Sign all new-hire documents in BambooHR.",
                "Activate LinkedIn Learning.",
                "Provide I-9 documents within 3 business days.",
                "Register for Paylocity.",
                "Download the BambooHR app.",
            ]},
            {"type": "bullets", "title": "90-Day Roadmap", "items": [
                "Days 1–30: complete orientation, paperwork, and onboarding workflows.",
                "Days 31–60: build independence and complete 60-day milestone tasks.",
                "Days 61–90: performance stabilization, review, and full benefits readiness.",
            ]},
        ],
        "quiz": [
            {"q": "I-9 documents must be provided within?", "options": ["1 day", "3 business days", "5 days", "10 days"], "answer": 1},
            {"q": "Probationary period ends at?", "options": ["30 days", "60 days", "90 days", "120 days"], "answer": 1},
            {"q": "PTO eligibility begins after?", "options": ["Day 1", "30 days", "60 days", "90 days"], "answer": 2},
            {"q": "Which app for your employee profile?", "options": ["Workday", "BambooHR", "ADP", "Gusto"], "answer": 1},
        ],
        "checklist": [
            "I will verify access and sign all documents.",
            "I will activate LinkedIn Learning.",
            "I will provide I-9 within 3 business days.",
            "I will register for Paylocity and download BambooHR.",
            "I understand the 90-day timeline.",
            "I know who to contact in HR.",
        ],
    },
}


# =========================
# Utility / state / auth
# =========================

def ui(html: str) -> None:
    st.markdown(html, unsafe_allow_html=True)


def init_state() -> None:
    for key, value in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value

    for mod in MODULES:
        if f"quiz_{mod.key}_passed" not in st.session_state:
            st.session_state[f"quiz_{mod.key}_passed"] = False
        if f"checklist_{mod.key}" not in st.session_state:
            st.session_state[f"checklist_{mod.key}"] = {}


def logo_base64() -> str | None:
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AAP_API.PNG")
    if not os.path.exists(logo_path):
        return None
    with open(logo_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def completion_progress() -> tuple[int, int]:
    done = 0
    total = 0
    for mod in MODULES:
        total += 1 + mod.checklist_count
        done += int(st.session_state.get(f"quiz_{mod.key}_passed", False))
        done += sum(1 for v in st.session_state.get(f"checklist_{mod.key}", {}).values() if v)
    return done, total


def is_complete(module_key: str) -> bool:
    mod = MODULE_INDEX[module_key]
    quiz_ok = st.session_state.get(f"quiz_{module_key}_passed", False)
    checklist_done = sum(1 for v in st.session_state.get(f"checklist_{module_key}", {}).values() if v)
    return quiz_ok and checklist_done >= mod.checklist_count


def gsheet_client():
    try:
        creds = dict(st.secrets["gcp_service_account"])
        return gspread.service_account_from_dict(
            creds,
            scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"],
        )
    except Exception:
        return None


def validate_login(access_code: str, emp_id: str, full_name: str) -> bool:
    try:
        expected = st.secrets["orientation_access_code"]
    except Exception:
        st.error("Access code not configured.")
        return False

    if access_code.strip() != expected.strip():
        st.error("Incorrect access code.")
        return False

    client = gsheet_client()
    if not client:
        st.error("Cannot connect to Google Sheets.")
        return False

    try:
        roster = client.open("AAP New Hire Orientation Progress").worksheet("Employee Roster")
        rows = roster.get_all_records()
    except Exception:
        st.error("Cannot open Employee Roster tab.")
        return False

    for row in rows:
        if str(row.get("Employee ID", "")).strip().lower() != emp_id.strip().lower():
            continue
        if str(row.get("Full Name", "")).strip().lower() != full_name.strip().lower():
            st.error("Name does not match.")
            return False

        st.session_state["emp_track"] = "warehouse" if str(row.get("Track", "")).strip().lower() == "warehouse" else "general"
        st.session_state["emp_department"] = str(row.get("Department", ""))
        st.session_state["emp_position"] = str(row.get("Position", ""))
        st.session_state["emp_start_date"] = str(row.get("Start Date", ""))
        return True

    st.error("Employee ID not found.")
    return False


# =========================
# Style + interactions
# =========================

def inject_styles() -> None:
    ui(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
  --bg:#05060f;
  --surface:#101425;
  --line:rgba(255,255,255,.11);
  --text:#f6f7ff;
  --muted:#b7bfdc;
  --accent:#7c8cff;
  --accent2:#1de3ce;
  --ok:#37d394;
  --warn:#f5bc42;
}

html, body, [class*="css"] { font-family:'Manrope',sans-serif!important; }
.stApp {
  background:
    radial-gradient(circle at 6% 8%, rgba(124,140,255,.3), transparent 28%),
    radial-gradient(circle at 92% 8%, rgba(29,227,206,.22), transparent 28%),
    var(--bg);
}

[data-testid="stSidebar"] {
  background: linear-gradient(180deg,#0b0f1d,#090c17);
  border-right:1px solid rgba(255,255,255,.08);
}

.card, .module-shell {
  border:1px solid var(--line);
  background:linear-gradient(160deg,rgba(255,255,255,.08),rgba(255,255,255,.02));
  border-radius:20px;
  backdrop-filter: blur(10px);
  box-shadow:0 16px 45px rgba(0,0,0,.35);
}

.hero { padding:34px; position:relative; overflow:hidden; animation:fadeUp .45s ease; }
.hero h1 { margin:.4rem 0 .6rem; color:#fff!important; font-size:clamp(1.7rem,4vw,2.8rem)!important; }
.hero p { color:#d9dff9!important; margin:0; max-width:760px; line-height:1.75; }
.kicker { text-transform:uppercase; letter-spacing:.14em; font-size:.68rem; color:var(--muted); }

.metric { padding:18px 20px; border-radius:15px; border:1px solid var(--line); background:rgba(255,255,255,.03); }
.metric .n{font-size:2rem;font-weight:800;color:#fff}
.metric .l{text-transform:uppercase;letter-spacing:.11em;font-size:.62rem;color:var(--muted)}

.module-tile {border:1px solid var(--line);border-radius:16px;overflow:hidden;background:#0f1324;transition:all .2s ease;margin-bottom:12px}
.module-tile:hover{transform:translateY(-2px);box-shadow:0 14px 28px rgba(0,0,0,.35)}
.module-img{height:128px;background-size:cover;background-position:center;filter:contrast(1.08) saturate(1.15)}
.module-info{padding:16px}
.module-title{font-weight:700;color:#fff;font-size:1rem;margin:.3rem 0}
.module-desc{color:#c7cfea;font-size:.86rem;line-height:1.55;margin:0}
.status-pill{display:inline-block;margin-top:.6rem;padding:4px 12px;border-radius:999px;font-size:.66rem;letter-spacing:.09em;text-transform:uppercase}
.status-pill.todo{background:rgba(255,255,255,.08);color:#d0d6ef}
.status-pill.wip{background:rgba(245,188,66,.2);color:#ffd477}
.status-pill.done{background:rgba(55,211,148,.2);color:#8af5c3}

.module-hero{height:220px;border-radius:18px;overflow:hidden;border:1px solid var(--line);background-size:cover;background-position:center;position:relative;animation:fadeUp .35s ease}
.module-hero::before{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(4,6,12,.2),rgba(4,6,12,.88));}
.module-hero .inner{position:absolute;left:24px;right:24px;bottom:20px}
.module-hero h2{color:#fff!important;margin:0!important}
.module-hero p{color:#e0e5ff!important;margin:.35rem 0 0}

.section{padding:22px;border-radius:16px;border:1px solid var(--line);background:rgba(255,255,255,.03);margin:12px 0}
.section h3{color:#fff!important}
.section p,.section li{color:#d8dff7}
.callout{padding:12px 14px;border-radius:12px;border-left:3px solid var(--accent2);background:rgba(29,227,206,.15);color:#d7fff9}
.callout.warn{border-left-color:var(--warn);background:rgba(245,188,66,.16);color:#ffe9b2}

[data-testid="stBaseButton-primary"], div[data-testid="stFormSubmitButton"] button {
  border-radius:12px!important; border:none!important; color:#fff!important;
  background:linear-gradient(90deg,var(--accent),#9ca8ff)!important; font-weight:700!important;
  box-shadow:0 8px 24px rgba(124,140,255,.35)!important;
}
[data-testid="stBaseButton-secondary"]{border-radius:12px!important}

.stTabs [data-baseweb="tab-list"]{background:rgba(255,255,255,.03);border:1px solid var(--line);border-radius:12px;padding:4px;gap:5px}
.stTabs [aria-selected="true"]{background:rgba(124,140,255,.22)!important;border-radius:10px!important;color:#fff!important}

@keyframes fadeUp { from {opacity:0; transform:translateY(8px);} to {opacity:1; transform:translateY(0);} }
</style>
        """
    )


def play_sound(cue: str) -> None:
    if not st.session_state.get("audio_enabled", True):
        return
    if st.session_state.get("last_sound") == cue:
        return

    tone = "UklGRlQAAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YTAAAAAAAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8="
    ui(f"<audio autoplay style='display:none'><source src='data:audio/wav;base64,{tone}' type='audio/wav'></audio>")
    st.session_state["last_sound"] = cue


# =========================
# Reusable renderers
# =========================

def render_section(section: Dict[str, Any]) -> None:
    typ = section["type"]
    ui("<div class='section'>")

    if typ == "markdown":
        if section.get("title"):
            st.markdown(f"### {section['title']}")
        st.markdown(section.get("body", ""))

    elif typ == "bullets":
        if section.get("title"):
            st.markdown(f"### {section['title']}")
        for item in section.get("items", []):
            st.markdown(f"- {item}")

    elif typ == "table":
        st.table(section.get("rows", []))

    elif typ == "tabs":
        if section.get("title"):
            st.markdown(f"### {section['title']}")
        labels = list(section["tabs"].keys())
        tabs = st.tabs(labels)
        for i, lab in enumerate(labels):
            with tabs[i]:
                st.markdown(section["tabs"][lab])

    elif typ == "callout":
        style = section.get("style", "info")
        klass = "warn" if style == "warn" else ""
        ui(f"<div class='callout {klass}'>{section.get('body', '')}</div>")

    ui("</div>")


def render_quiz(module_key: str, questions: List[Dict[str, Any]]) -> None:
    st.markdown("---")
    st.markdown("### Module Assessment")

    if st.session_state.get(f"quiz_{module_key}_passed", False):
        st.success("Assessment complete — all answers are correct.")
        return

    answers: Dict[int, Any] = {}
    for i, q in enumerate(questions):
        answers[i] = st.radio(f"**Q{i+1}.** {q['q']}", options=q["options"], index=None, key=f"q_{module_key}_{i}")

    if st.button("Submit Answers", key=f"submit_{module_key}", type="primary"):
        correct = sum(answers[i] == q["options"][q["answer"]] for i, q in enumerate(questions))
        if correct == len(questions):
            st.session_state[f"quiz_{module_key}_passed"] = True
            play_sound(f"quiz-pass-{module_key}")
            st.rerun()
        st.error(f"{correct} of {len(questions)} correct — review and try again.")


def render_checklist(module_key: str, items: List[str]) -> None:
    st.markdown("---")
    st.markdown("### Confirmation Checklist")
    checklist = st.session_state.get(f"checklist_{module_key}", {})

    for i, item in enumerate(items):
        key = f"c_{module_key}_{i}"
        checklist[key] = st.checkbox(item, value=checklist.get(key, False), key=key)

    st.session_state[f"checklist_{module_key}"] = checklist
    done = sum(1 for v in checklist.values() if v)
    st.caption(f"{done} of {len(items)} confirmed")


# =========================
# Screens
# =========================

def show_login() -> None:
    ui("<div style='height:5vh'></div>")
    _, c, _ = st.columns([1, 1.2, 1])
    with c:
        logo = logo_base64()
        if logo:
            ui(f"<div style='text-align:center;margin-bottom:16px'><img src='data:image/png;base64,{logo}' style='height:70px;filter:drop-shadow(0 8px 20px rgba(0,0,0,.35));'></div>")

        ui("<div class='card' style='padding:28px'>")
        st.markdown("### Welcome to AAP Onboarding")
        st.caption("A modern, interactive orientation experience")
        with st.form("login_form"):
            access_code = st.text_input("Access Code", type="password", placeholder="Enter access code")
            employee_id = st.text_input("Employee ID", placeholder="e.g. 10042")
            full_name = st.text_input("Full Name", placeholder="As shown in your HR paperwork")
            submitted = st.form_submit_button("Enter Experience", use_container_width=True)
        ui("</div>")

        c1, c2 = st.columns([1, 1])
        with c1:
            st.toggle("Micro-sounds", key="audio_enabled")
        with c2:
            st.caption("Need help? Nicole Thornton · 256-574-7528")

        if submitted:
            if not access_code or not employee_id or not full_name:
                st.error("All fields are required.")
            else:
                with st.spinner("Verifying..."):
                    if validate_login(access_code, employee_id, full_name):
                        st.session_state["logged_in"] = True
                        st.session_state["emp_name"] = full_name.strip().title()
                        st.session_state["emp_number"] = employee_id.strip()
                        play_sound("login-success")
                        st.rerun()


def show_sidebar() -> None:
    with st.sidebar:
        logo = logo_base64()
        if logo:
            ui(f"<div style='text-align:center;margin-top:8px'><img src='data:image/png;base64,{logo}' style='height:46px;opacity:.95'></div>")

        done, total = completion_progress()
        pct = int((done / total) * 100) if total else 0
        st.markdown(f"**{st.session_state['emp_name']}**")
        if st.session_state.get("emp_position"):
            st.caption(st.session_state["emp_position"])
        st.progress(pct / 100)
        st.caption(f"{pct}% complete")

        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state["current_page"] = "home"
            st.session_state["current_module"] = None
            st.rerun()

        for mod in MODULES:
            suffix = " ✓" if is_complete(mod.key) else ""
            if st.button(f"{mod.number}  {mod.title}{suffix}", key=f"nav_{mod.key}", use_container_width=True):
                st.session_state["current_page"] = "module"
                st.session_state["current_module"] = mod.key
                play_sound(f"open-{mod.key}")
                st.rerun()

        st.markdown("---")
        st.toggle("Micro-sounds", key="audio_enabled")
        if st.button("Sign Out", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


def show_home() -> None:
    first = st.session_state["emp_name"].split()[0] if st.session_state["emp_name"] else "there"
    done, total = completion_progress()
    pct = int((done / total) * 100) if total else 0
    modules_complete = sum(1 for m in MODULES if is_complete(m.key))

    ui(
        f"""
        <div class='module-shell hero'>
            <div class='kicker'>AAP · Interactive Onboarding</div>
            <h1>Welcome, {first}</h1>
            <p>This experience is designed around you: visual modules, quick assessments, and clear milestones. Move at your pace — your progress auto-saves.</p>
        </div>
        """
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        ui(f"<div class='metric'><div class='n'>{pct}%</div><div class='l'>overall progress</div></div>")
    with c2:
        ui(f"<div class='metric'><div class='n'>{modules_complete}/{len(MODULES)}</div><div class='l'>modules complete</div></div>")
    with c3:
        ui(f"<div class='metric'><div class='n'>{done}/{total}</div><div class='l'>items done</div></div>")

    st.markdown("### Continue Learning")
    cols = st.columns(2)
    for i, mod in enumerate(MODULES):
        quiz_done = st.session_state.get(f"quiz_{mod.key}_passed", False)
        checklist_done = sum(1 for v in st.session_state.get(f"checklist_{mod.key}", {}).values() if v)
        if is_complete(mod.key):
            status, cls = "Complete", "done"
        elif quiz_done or checklist_done:
            status, cls = "In Progress", "wip"
        else:
            status, cls = "Not Started", "todo"

        with cols[i % 2]:
            ui(
                f"""
                <div class='module-tile'>
                    <div class='module-img' style="background-image:url('{mod.image}')"></div>
                    <div class='module-info'>
                        <div class='kicker'>Module {mod.number}</div>
                        <div class='module-title'>{mod.title}</div>
                        <p class='module-desc'>{mod.summary}</p>
                        <span class='status-pill {cls}'>{status}</span>
                    </div>
                </div>
                """
            )
            if st.button("Open Module", key=f"open_{mod.key}", use_container_width=True):
                st.session_state["current_page"] = "module"
                st.session_state["current_module"] = mod.key
                play_sound(f"open-{mod.key}")
                st.rerun()


def show_module(module_key: str) -> None:
    mod = MODULE_INDEX[module_key]

    if st.button("← Back to Dashboard"):
        st.session_state["current_page"] = "home"
        st.session_state["current_module"] = None
        st.rerun()

    ui(
        f"""
        <div class='module-hero' style="background-image:url('{mod.image}')">
          <div class='inner'>
            <div class='kicker'>Module {mod.number}</div>
            <h2>{mod.title}</h2>
            <p>{mod.subtitle}</p>
          </div>
        </div>
        """
    )

    content = MODULE_CONTENT[module_key]
    for section in content["sections"]:
        render_section(section)

    render_quiz(module_key, content["quiz"])
    render_checklist(module_key, content["checklist"])

    st.markdown("---")
    idx = [m.key for m in MODULES].index(module_key)
    pcol, ncol = st.columns(2)
    if idx > 0:
        prev = MODULES[idx - 1]
        with pcol:
            if st.button(f"← {prev.title}", key=f"prev_{prev.key}", use_container_width=True):
                st.session_state["current_module"] = prev.key
                st.rerun()
    if idx < len(MODULES) - 1:
        nxt = MODULES[idx + 1]
        with ncol:
            if st.button(f"{nxt.title} →", key=f"next_{nxt.key}", use_container_width=True):
                st.session_state["current_module"] = nxt.key
                st.rerun()


def main() -> None:
    init_state()
    inject_styles()

    if not st.session_state["logged_in"]:
        show_login()
        return

    show_sidebar()
    if st.session_state["current_page"] == "module" and st.session_state["current_module"]:
        show_module(st.session_state["current_module"])
    else:
        show_home()


if __name__ == "__main__":
    main()
