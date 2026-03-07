
# -*- coding: utf-8 -*-
"""Rebuilt onboarding portal with premium card UI and preserved business flow."""

from __future__ import annotations

import base64
import json
import logging
import os
from datetime import datetime
from typing import Any

import streamlit as st

try:
    import gspread
except Exception:  # pragma: no cover
    gspread = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api_onboarding")

APP_TITLE = "API Onboarding Studio"
APP_ICON = ":material/school:"
API_LOGO_PATH = "assets/api_logo.png"
FALLBACK_LOGO_URL = "https://rxaap.com/wp-content/uploads/2021/03/AAP_Logo_White.png"
PASSING_FRACTION = 0.75
USE_MOCK_SHEETS = os.getenv("MOCK_SHEETS", "0") == "1"
PAYLOCITY_COMPANY_ID = "123959"

CONTACTS = [
    ("Brandy Hooper", "VP of Human Resources", "brandy.hooper@rxaap.com", "256-574-7526"),
    ("Nicole Thornton", "HR Administrator", "nicole.thornton@apirx.com", "256-574-7528"),
    ("CBIZ Benefits", "Benefits Broker", "844.200.CBIZ (2249)", ""),
    ("LifeMatters EAP", "Employee Assistance", "800-634-6433 / mylifematters.com", ""),
]


def make_module(key: str, number: int, title: str, subtitle: str, intro: str, bullets: list[str], checklist: list[str], quiz: list[tuple[str, list[str], str]]) -> dict[str, Any]:
    return {
        "key": key,
        "number": number,
        "title": title,
        "subtitle": subtitle,
        "intro": intro,
        "bullets": bullets,
        "checklist": {f"i{idx}": item for idx, item in enumerate(checklist, start=1)},
        "quiz": [{"q": q, "options": opts, "answer": ans} for q, opts, ans in quiz],
    }


GENERAL_MODULES = [
    make_module("welcome", 1, "Welcome to API", "Mission, values, and role impact.", "Get context fast so day one feels focused.", ["API supports independent pharmacies nationwide.", "Values: customer focus, integrity, respect, excellence, ownership.", "Your first week is about confidence and momentum."], ["I can summarize API mission and values.", "I understand how my role impacts customers.", "I know what success in week one looks like."], [("Which is not a core value?", ["Integrity", "Ownership", "Hierarchy", "Respect"], "Hierarchy"), ("API primarily supports:", ["Independent pharmacies", "Retail banks", "Hospitals only", "Manufacturing"], "Independent pharmacies"), ("Day-one onboarding should create:", ["Confusion", "Confidence", "Silence", "Delay"], "Confidence"), ("Values should guide:", ["Only leaders", "Daily decisions", "Only HR", "Annual audits"], "Daily decisions")]),
    make_module("conduct", 2, "Conduct and Ethics", "Protect trust and psychological safety.", "Behavior standards are practical and non-negotiable.", ["Report concerns quickly without fear of retaliation.", "Protect confidential information.", "Employment decisions are merit-based."], ["I know where to report concerns.", "I understand confidentiality expectations.", "I understand EEO and respectful workplace standards."], [("If you witness unethical behavior:", ["Ignore it", "Report it promptly", "Wait a month", "Post online"], "Report it promptly"), ("Employment decisions are based on:", ["Rumors", "Merit and qualifications", "Personal preference", "Seniority only"], "Merit and qualifications"), ("Retaliation for reporting concerns is:", ["Allowed", "Case-by-case", "Not acceptable", "Optional"], "Not acceptable"), ("Confidential information should be:", ["Public", "Protected", "Shared casually", "Optional"], "Protected")]),
    make_module("policies", 3, "Workplace Policies", "Attendance, communication, accountability.", "Keep expectations clear and easy to execute.", ["Attendance reliability supports team performance.", "Professional communication reduces friction.", "Safety and policy consistency are baseline expectations."], ["I understand attendance expectations.", "I know team communication standards.", "I understand accountability and escalation paths."], [("Policy question best action:", ["Guess", "Ask lead/HR", "Ignore", "Wait for review"], "Ask lead/HR"), ("Attendance affects:", ["Nothing", "Team reliability", "Only payroll", "Only HR"], "Team reliability"), ("Safety ownership belongs to:", ["Managers only", "Everyone", "New hires only", "Facilities only"], "Everyone"), ("Professional communication should be:", ["Vague", "Delayed", "Clear and respectful", "Optional"], "Clear and respectful")]),
    make_module("timeoff", 4, "Time Off and Leave", "Use leave workflows without surprises.", "Learn the process once and avoid avoidable issues.", ["Report absences through approved channels.", "FMLA baseline is 12 months and 1,250 hours.", "Life-event updates are due within 30 days."], ["I know absence reporting channels.", "I understand PTO/FMLA basics.", "I know life-event deadlines."], [("Life-event update deadline:", ["7 days", "14 days", "30 days", "90 days"], "30 days"), ("FMLA baseline includes:", ["3 months and 500 hours", "12 months and 1,250 hours", "Immediate eligibility", "Manager only"], "12 months and 1,250 hours"), ("Absence reporting should be:", ["Unofficial", "Official and timely", "Skipped", "Social"], "Official and timely"), ("Time-off planning helps:", ["No one", "Team continuity", "Only payroll", "Only records"], "Team continuity")]),
    make_module("benefits", 5, "Benefits Overview", "Coverage, retirement, and support tools.", "Use your benefits early and intentionally.", ["Eligible health coverage begins first of month after 60 days.", "401(k) includes 100% match on first 3%.", "Telehealth and support resources are available."], ["I know health eligibility timing.", "I understand 401(k) match details.", "I know where to ask benefits questions."], [("Health coverage typically begins:", ["Day one", "After 30 days", "1st month after 60 days", "After 1 year"], "1st month after 60 days"), ("401(k) match on first 3%:", ["0%", "50%", "75%", "100%"], "100%"), ("A day-one resource is:", ["Telehealth", "Annual bonus", "Open enrollment only", "None"], "Telehealth"), ("Benefits questions should go to:", ["No one", "HR/support contacts", "Public forums", "Anyone"], "HR/support contacts")]),
    make_module("firststeps", 6, "Your First Steps", "Systems setup and first-90-day momentum.", "Complete this to be operational and supported.", [f"Set up Paylocity using company ID {PAYLOCITY_COMPANY_ID}.", "Configure BambooHR and learning access.", "Know your support contact map."], ["I can complete required account setup.", "I know my support contacts.", "I understand first-30/60/90-day expectations."], [("Paylocity company ID:", ["123959", "100000", "404404", "987654"], "123959"), ("If blocked during onboarding:", ["Pause silently", "Escalate to support contacts", "Skip step", "Wait a week"], "Escalate to support contacts"), ("First-90-day success depends on:", ["Luck", "Consistency and learning", "Isolation", "Skipping feedback"], "Consistency and learning"), ("System setup priority is:", ["Ignore tools", "Complete core setup", "Delay 60 days", "Outsource"], "Complete core setup")]),
]

WAREHOUSE_MODULES = [
    make_module("wh_welcome", 1, "Welcome to Warehouse Ops", "Role clarity and operational impact.", "Your accuracy powers reliable pharmacy service.", ["Precision and safety are daily requirements.", "Communication prevents avoidable delays.", "Role discipline protects customers and team."], ["I understand warehouse role impact.", "I understand why scan/count accuracy matters.", "I know escalation expectations."], [("Top warehouse priority:", ["Speed only", "Accuracy and safety", "Silence", "Skipping checks"], "Accuracy and safety"), ("Operational issues should be:", ["Hidden", "Reported quickly", "Ignored", "Delayed"], "Reported quickly"), ("Warehouse work impacts:", ["Only reports", "Pharmacy customers", "Only managers", "Only vendors"], "Pharmacy customers"), ("Warehouse communication should be:", ["Delayed", "Clear and timely", "Optional", "One-way"], "Clear and timely")]),
    make_module("wh_conduct", 2, "Conduct and Accountability", "Honesty, respect, and no shortcuts.", "Ethics is visible in every shift and scan.", ["Report damage and errors immediately.", "Unauthorized equipment use is prohibited.", "Respect is expected in every interaction."], ["I will report damage/errors immediately.", "I understand equipment authorization rules.", "I understand respectful workplace standards."], [("Unauthorized equipment use is:", ["Fine if fast", "Not acceptable", "Allowed weekends", "Allowed with peer"], "Not acceptable"), ("Damaged inventory should be:", ["Ignored", "Documented and reported", "Moved quietly", "Discarded"], "Documented and reported"), ("Professional behavior includes:", ["Retaliation", "Respectful communication", "Harassment", "Falsifying logs"], "Respectful communication"), ("Operational ethics are:", ["Optional", "Critical", "Only HR concern", "Seasonal"], "Critical")]),
    make_module("wh_safety", 3, "Safety and Warehouse Policies", "PPE, equipment, and safe movement.", "Safety discipline keeps shifts stable and productive.", ["Wear required footwear and PPE.", "Operate equipment only when trained and authorized.", "Report hazards immediately and keep aisles clear."], ["I know PPE and footwear requirements.", "I will operate only authorized equipment.", "I know hazard reporting expectations."], [("Forklift use is allowed when:", ["Curious", "Authorized and trained", "Peer says okay", "Rushed"], "Authorized and trained"), ("If you spot a hazard:", ["Ignore", "Report immediately", "Wait until break", "Chat only"], "Report immediately"), ("Safety ownership belongs to:", ["Supervisors only", "Everyone", "New hires only", "Vendors"], "Everyone"), ("Clear aisles help:", ["Looks only", "Reduce risk and delays", "No impact", "Audit only"], "Reduce risk and delays")]),
    make_module("wh_timeoff", 4, "Time Off and Leave", "Attendance reliability and leave process.", "Use approved channels and protect schedule continuity.", ["Follow official attendance and leave workflows.", "Approved vacation timing matters.", "Life-event updates are due within 30 days."], ["I understand attendance process.", "I know how to report absences.", "I know critical deadline rules."], [("Life-event deadline:", ["7", "30", "60", "120"], "30"), ("Attendance reporting should be:", ["Consistent and timely", "Optional", "Shift-end only", "By coworkers"], "Consistent and timely"), ("Approved leave supports:", ["Unplanned gaps", "Reliable staffing", "No impact", "Policy avoidance"], "Reliable staffing"), ("If unsure about leave process:", ["Guess", "Ask lead/HR", "Skip", "Wait for annual training"], "Ask lead/HR")]),
    make_module("wh_benefits", 5, "Benefits and Support", "Coverage, retirement, wellbeing resources.", "Benefits are part of compensation; use them intentionally.", ["Health eligibility starts first of month after 60 days.", "401(k) includes 100% match on first 3%.", "EAP and telehealth support are available."], ["I know coverage timing.", "I understand retirement match details.", "I know support resources."], [("401(k) match on first 3%:", ["25%", "50%", "100%", "No match"], "100%"), ("Coverage start for eligible employees:", ["Immediately", "1st month after 60 days", "After a year", "Open enrollment only"], "1st month after 60 days"), ("Confidential support resource:", ["EAP", "Timesheet app", "Dock", "Scanner"], "EAP"), ("Benefits questions should go to:", ["No one", "HR/support contacts", "Public forum", "Anyone"], "HR/support contacts")]),
    make_module("wh_firststeps", 6, "First Steps on the Floor", "Day-one setup and support map.", "Complete this module to begin with clarity and confidence.", [f"Set up systems including Paylocity ({PAYLOCITY_COMPANY_ID}).", "Follow trainer guidance before equipment use.", "Use contacts for HR, benefits, and operations support."], ["I know required account setup steps.", "I understand training-before-equipment rules.", "I know first-90-day expectations and support contacts."], [("Paylocity company ID:", ["123959", "120000", "300111", "404404"], "123959"), ("Operate specialized equipment when:", ["Trained and authorized", "Rushed", "Peer approved", "Never trained"], "Trained and authorized"), ("If blocked during onboarding:", ["Stop communicating", "Escalate to contacts", "Wait silently", "Skip task"], "Escalate to contacts"), ("First-90-day success depends on:", ["Luck", "Consistency and coachability", "Isolation", "Avoiding feedback"], "Consistency and coachability")]),
]

TRACKS = {
    "general": {"label": "General", "modules": GENERAL_MODULES},
    "warehouse": {"label": "Warehouse", "modules": WAREHOUSE_MODULES},
}

_mock_progress_rows: list[list[Any]] = []


@st.cache_resource
def get_gsheet_client():
    if USE_MOCK_SHEETS:
        return None
    if gspread is None:
        logger.warning("gspread unavailable; use MOCK_SHEETS=1 for local testing.")
        return None
    try:
        creds_dict = dict(st.secrets["gcp_service_account"])
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        return gspread.service_account_from_dict(creds_dict, scopes=scopes)
    except Exception as exc:  # pragma: no cover
        logger.exception("GSheet client init failed: %s", exc)
        return None


def get_sheet(client):
    if USE_MOCK_SHEETS:
        class MockSheet:
            def get_all_records(self):
                return [{"Employee ID": r[0], "Employee Name": r[1], "Module Key": r[2], "Completion %": r[3], "Checklist Items": r[4], "Quiz Score": r[5], "Last Updated": r[6]} for r in _mock_progress_rows]

            def update(self, _cell_range, data):
                values = data[0]
                for idx, row in enumerate(_mock_progress_rows):
                    if row[0] == values[0] and row[2] == values[2]:
                        _mock_progress_rows[idx] = values
                        return

            def append_row(self, data):
                _mock_progress_rows.append(data)

        return MockSheet()

    try:
        return client.open("AAP New Hire Orientation Progress").sheet1
    except Exception as exc:  # pragma: no cover
        logger.exception("Open progress sheet failed: %s", exc)
        return None


def get_employee_sheet(client):
    if USE_MOCK_SHEETS:
        class MockRoster:
            def get_all_records(self):
                return [
                    {"Employee ID": "10001", "Full Name": "Sample User", "Track": "General"},
                    {"Employee ID": "20001", "Full Name": "Warehouse User", "Track": "Warehouse"},
                ]

        return MockRoster()
    try:
        return client.open("AAP New Hire Orientation Progress").worksheet("Employee Roster")
    except Exception as exc:  # pragma: no cover
        logger.exception("Open roster failed: %s", exc)
        return None


def verify_employee(access_code: str, employee_id: str, full_name: str) -> tuple[bool, str, str]:
    try:
        expected_code = str(st.secrets["orientation_access_code"]).strip()
    except Exception:
        return False, "", "Configuration issue detected. Contact HR."

    if access_code.strip() != expected_code:
        return False, "", "Incorrect credentials."

    client = get_gsheet_client()
    roster = get_employee_sheet(client) if not USE_MOCK_SHEETS else get_employee_sheet(None)
    if not roster:
        return False, "", "Employee roster unavailable right now."

    try:
        entered_id = employee_id.strip().lower()
        entered_name = full_name.strip().lower()
        for row in roster.get_all_records():
            row_id = str(row.get("Employee ID", "")).strip().lower()
            row_name = str(row.get("Full Name", "")).strip().lower()
            if row_id != entered_id:
                continue
            if row_name != entered_name:
                return False, "", "Employee ID and full name did not match records."
            track = "warehouse" if str(row.get("Track", "")).strip().lower() == "warehouse" else "general"
            return True, track, ""
        return False, "", "Employee record not found."
    except Exception as exc:  # pragma: no cover
        logger.exception("Verification failed: %s", exc)
        return False, "", "Verification error. Try again."


def save_progress(employee_id: str, employee_name: str, module_key: str, pct: int, checklist_items: dict, quiz_tuple: tuple[int, int] | None):
    client = get_gsheet_client()
    sheet = get_sheet(client) if not USE_MOCK_SHEETS else get_sheet(None)
    if not sheet:
        return

    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        payload = [employee_id, employee_name, module_key, int(pct), json.dumps(checklist_items), None if not quiz_tuple else quiz_tuple[0], now]
        cache_key = (employee_id, module_key)
        row_index = st.session_state["row_index_cache"].get(cache_key)

        if row_index is None:
            for idx, row in enumerate(sheet.get_all_records(), start=2):
                if row.get("Employee ID") == employee_id and row.get("Module Key") == module_key:
                    row_index = idx
                    st.session_state["row_index_cache"][cache_key] = row_index
                    break

        if row_index:
            sheet.update(f"A{row_index}:G{row_index}", [payload])
        else:
            sheet.append_row(payload)
    except Exception as exc:  # pragma: no cover
        logger.exception("Save progress failed: %s", exc)


def load_progress(employee_id: str) -> dict[str, dict[str, Any]]:
    client = get_gsheet_client()
    sheet = get_sheet(client) if not USE_MOCK_SHEETS else get_sheet(None)
    if not sheet:
        return {}

    out: dict[str, dict[str, Any]] = {}
    try:
        for row in sheet.get_all_records():
            if str(row.get("Employee ID", "")).strip() != employee_id.strip():
                continue
            mk = str(row.get("Module Key", "")).strip()
            try:
                checklist = json.loads(row.get("Checklist Items", "{}"))
            except Exception:
                checklist = {}
            quiz_score = row.get("Quiz Score")
            out[mk] = {"pct": int(row.get("Completion %", 0) or 0), "checklist": checklist, "quiz_score": None if quiz_score in (None, "") else int(quiz_score)}
    except Exception as exc:  # pragma: no cover
        logger.exception("Load progress failed: %s", exc)
    return out

def logo_src() -> str:
    if os.path.exists(API_LOGO_PATH):
        with open(API_LOGO_PATH, "rb") as img:
            return f"data:image/png;base64,{base64.b64encode(img.read()).decode('utf-8')}"
    return FALLBACK_LOGO_URL


def active_modules() -> list[dict[str, Any]]:
    track = st.session_state.get("role_track") or "general"
    return TRACKS[track]["modules"]


def get_module(module_key: str | None) -> dict[str, Any] | None:
    if not module_key:
        return None
    for module in active_modules():
        if module["key"] == module_key:
            return module
    return None


def initialize_state():
    defaults = {
        "authenticated": False,
        "username": "",
        "employee_id": "",
        "role_track": "",
        "nav_key": "home",
        "progress": {},
        "checklist_items": {},
        "quiz_results": {},
        "sheet_loaded": False,
        "auth_error": "",
        "row_index_cache": {},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def seed_track_state(track: str):
    modules = TRACKS[track]["modules"]
    st.session_state.role_track = track
    st.session_state.progress = {m["key"]: 0 for m in modules}
    st.session_state.checklist_items = {m["key"]: {k: False for k in m["checklist"]} for m in modules}
    st.session_state.quiz_results = {}
    st.session_state.nav_key = "home"
    st.session_state.sheet_loaded = False


def overall_progress() -> int:
    mods = active_modules()
    if not mods:
        return 0
    return int(sum(st.session_state.progress.get(m["key"], 0) for m in mods) / len(mods))


def calc_module_pct(module_key: str) -> int:
    items = st.session_state.checklist_items.get(module_key, {})
    total = len(items)
    checked = sum(1 for v in items.values() if v)
    checklist_credit = (checked / total * 70) if total else 0

    quiz_credit = 0
    qt = st.session_state.quiz_results.get(module_key)
    if qt:
        score, max_score = qt
        if max_score and (score / max_score) >= PASSING_FRACTION:
            quiz_credit = 30
    return int(checklist_credit + quiz_credit)


def update_module_progress(module_key: str):
    previous = st.session_state.progress.get(module_key, 0)
    current = calc_module_pct(module_key)
    st.session_state.progress[module_key] = current
    if previous < 100 <= current:
        st.toast("Module complete. Nice work.")

    if st.session_state.authenticated and st.session_state.employee_id:
        save_progress(st.session_state.employee_id, st.session_state.username, module_key, current, st.session_state.checklist_items.get(module_key, {}), st.session_state.quiz_results.get(module_key))


def load_progress_once():
    if st.session_state.sheet_loaded or not st.session_state.employee_id:
        return

    modules = active_modules()
    question_counts = {m["key"]: len(m["quiz"]) for m in modules}
    saved = load_progress(st.session_state.employee_id)

    for module in modules:
        mk = module["key"]
        if mk not in saved:
            continue
        saved_data = saved[mk]
        st.session_state.progress[mk] = int(saved_data.get("pct", 0) or 0)

        ck = saved_data.get("checklist", {})
        if isinstance(ck, dict):
            for item_key in st.session_state.checklist_items[mk].keys():
                st.session_state.checklist_items[mk][item_key] = bool(ck.get(item_key, False))

        quiz_score = saved_data.get("quiz_score")
        if quiz_score is not None:
            st.session_state.quiz_results[mk] = (int(quiz_score), question_counts.get(mk, 0))

    st.session_state.sheet_loaded = True


def inject_theme():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Sora:wght@600;700&display=swap');
        :root {
            --navy-950:#061428;
            --navy-900:#0b1f45;
            --navy-700:#173f83;
            --cyan-500:#12d8ff;
            --cyan-300:#9ef1ff;
            --red-500:#ff3f60;
            --red-400:#ff5b76;
            --ink:#0d264f;
            --muted:#4d6489;
            --line:rgba(17,53,110,.17);
            --panel:#ffffff;
        }
        html, body, [class*="css"] {font-family:'Space Grotesk',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;}
        h1, h2, h3 {font-family:'Sora','Space Grotesk',sans-serif; letter-spacing:-0.02em;}
        .stApp {
            background:
                radial-gradient(circle at 82% -18%, rgba(18,216,255,.35), transparent 36%),
                radial-gradient(circle at 3% 8%, rgba(255,63,96,.20), transparent 28%),
                linear-gradient(180deg, #f8fdff 0%, #eef6ff 62%, #f4fbff 100%);
            color: var(--ink);
        }
        [data-testid="stHeader"] {background:transparent;}
        [data-testid="stToolbar"] {right: 12px;}
        [data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 20px !important;
            border: 1px solid var(--line) !important;
            background: var(--panel);
            box-shadow: 0 18px 36px rgba(10,31,69,.10);
            animation: rise 280ms ease;
            transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
        }
        [data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-2px);
            border-color: rgba(17,53,110,.24) !important;
            box-shadow: 0 22px 44px rgba(10,31,69,.14);
        }
        [data-testid="stMetric"] {
            border: 1px solid var(--line);
            border-radius: 16px;
            background: rgba(255,255,255,.86);
            box-shadow: 0 10px 24px rgba(15,43,86,.08);
            padding: 8px 10px;
        }
        .hero {
            border: 1px solid rgba(18,216,255,.42);
            border-radius: 24px;
            padding: 24px;
            color: #f4fbff;
            background:
                radial-gradient(circle at 90% 10%, rgba(18,216,255,.24), transparent 40%),
                linear-gradient(132deg, rgba(6,20,40,.97), rgba(13,40,82,.96));
            box-shadow: 0 24px 46px rgba(7,23,49,.38);
        }
        .pill {
            display: inline-block;
            padding: 6px 11px;
            border-radius: 999px;
            background: rgba(10,38,81,.56);
            border: 1px solid rgba(18,216,255,.62);
            color: #dcfbff;
            font-size: .78rem;
            margin-bottom: 10px;
            letter-spacing: .02em;
            text-transform: uppercase;
            font-weight: 600;
        }
        .module-head {
            border-radius: 16px;
            border: 1px solid rgba(255,63,96,.31);
            background: linear-gradient(130deg, rgba(255,63,96,.10), rgba(18,216,255,.12));
            padding: 14px;
            margin-bottom: 10px;
        }
        .module-head h3 {margin:0;font-size:1.16rem;color:var(--navy-900);}
        .module-head p {margin:6px 0 0;color:var(--muted);}
        .progress-rail {
            width: 100%;
            height: 11px;
            background: #d9e8fb;
            border-radius: 999px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--red-500), var(--cyan-500));
            transition: width .34s ease;
        }
        .nav-caption {
            color: var(--muted);
            font-size: .9rem;
            margin: 0 0 10px;
            display:flex;
            justify-content: space-between;
            align-items: center;
        }
        .caption-pill {
            font-size: .74rem;
            border: 1px solid rgba(18,216,255,.42);
            color: #145085;
            border-radius: 999px;
            padding: 4px 9px;
            background: rgba(18,216,255,.12);
            font-weight: 600;
        }
        .stat-strip {
            border-radius: 20px;
            border: 1px solid rgba(17,53,110,.18);
            background:
                linear-gradient(135deg, rgba(255,63,96,.08), rgba(255,255,255,.72) 30%, rgba(18,216,255,.08));
            padding: 14px;
            margin-bottom: 12px;
        }
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 10px;
        }
        .stat-card {
            border-radius: 14px;
            border: 1px solid rgba(17,53,110,.16);
            background: rgba(255,255,255,.86);
            padding: 10px;
        }
        .stat-label {
            font-size: .75rem;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: .04em;
            margin-bottom: 4px;
        }
        .stat-value {
            font-family: 'Sora','Space Grotesk',sans-serif;
            font-size: 1.08rem;
            color: var(--navy-900);
            font-weight: 700;
        }
        .guide-list {margin:0;padding-left:18px;}
        .guide-list li {margin:6px 0;color:var(--ink);}
        .quick-note {
            border: 1px dashed rgba(23,58,120,.24);
            border-radius: 12px;
            padding: 10px;
            font-size: .9rem;
            background: rgba(10,31,69,.04);
            color: #1b447e;
        }
        .support-item {
            border: 1px solid rgba(17,53,110,.14);
            border-radius: 12px;
            background: rgba(250,254,255,.9);
            padding: 9px 10px;
            margin-bottom: 8px;
        }
        .support-item strong {color: var(--navy-900);}
        .stButton > button,
        .stFormSubmitButton > button {
            border-radius: 12px;
            font-weight: 700;
            transition: transform .12s ease, filter .12s ease, box-shadow .12s ease;
            border: 1px solid rgba(17,53,110,.18);
            background: rgba(255,255,255,.76);
            color: var(--navy-900);
        }
        .stButton > button[kind="primary"],
        .stFormSubmitButton > button[kind="primary"] {
            background: linear-gradient(90deg, #f03250, #ff4866);
            color: #fff;
            border: 0;
            box-shadow: 0 10px 22px rgba(255,66,94,.34);
        }
        .stButton > button:hover,
        .stFormSubmitButton > button:hover {
            transform: translateY(-1px);
            filter: saturate(1.04);
            box-shadow: 0 12px 24px rgba(10,31,69,.18);
        }
        [data-baseweb="radio"] > div,
        [data-baseweb="checkbox"] > div {transition: transform .12s ease;}
        [data-baseweb="radio"]:hover > div,
        [data-baseweb="checkbox"]:hover > div {transform: translateX(2px);}
        @keyframes rise {
            from {opacity:0;transform:translateY(5px);} 
            to {opacity:1;transform:translateY(0);} 
        }
        @media (prefers-reduced-motion: reduce) { * {animation:none !important; transition:none !important;} }
        @media (max-width: 980px) {
            .stat-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def progress_bar(pct: int):
    safe = max(0, min(100, int(pct)))
    st.markdown(f'<div class="progress-rail"><div class="progress-fill" style="width:{safe}%;"></div></div>', unsafe_allow_html=True)


def module_status(pct: int) -> str:
    if pct >= 100:
        return "Complete"
    if pct > 0:
        return "In Progress"
    return "Queued"


def next_incomplete_module() -> dict[str, Any] | None:
    for module in active_modules():
        if st.session_state.progress.get(module["key"], 0) < 100:
            return module
    return None


def render_login():
    st.markdown(
        "<section class='hero' style='max-width:980px;margin:0 auto 10px;'><div class='pill'>API Onboarding Studio</div><h1 style='margin:0;'>First Week, But Make It Smooth</h1><p style='margin-top:10px;'>One clean path. Bite-size modules. Zero handbook chaos.</p></section>",
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.05, 1], gap="large")
    with left:
        with st.container(border=True):
            st.markdown("### What Happens Next")
            st.markdown(
                """
                <ul class="guide-list">
                    <li>Sign in with your HR-provided credentials.</li>
                    <li>Complete each module in short, guided checkpoints.</li>
                    <li>Watch progress update instantly as you go.</li>
                </ul>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("<div class='quick-note'>Most employees finish this orientation in focused short sessions, not one long marathon.</div>", unsafe_allow_html=True)

    with right:
        with st.container(border=True):
            st.markdown(
                f"<div style='text-align:center;margin-bottom:10px;'><img src='{logo_src()}' alt='API' style='height:56px;margin-bottom:8px;'/><div style='font-size:1.08rem;font-weight:700;'>Employee Sign In</div><div style='color:#4f6586;'>Use the exact name listed in your HR records.</div></div>",
                unsafe_allow_html=True,
            )
            with st.form("login_form", clear_on_submit=False):
                access_code = st.text_input("Access Code", type="password")
                employee_id = st.text_input("Employee ID", placeholder="Example: 10042")
                full_name = st.text_input("Full Name", placeholder="Exactly as listed in HR records")
                submitted = st.form_submit_button("Enter Portal", type="primary", use_container_width=True)

            if st.session_state.auth_error:
                st.error(st.session_state.auth_error)
            else:
                st.info("Progress saves automatically as you complete modules.")

            if submitted:
                if not access_code.strip() or not employee_id.strip() or not full_name.strip():
                    st.error("Please complete all fields.")
                    return
                with st.spinner("Verifying credentials..."):
                    ok, track, reason = verify_employee(access_code, employee_id, full_name)
                if not ok:
                    st.session_state.auth_error = reason
                    st.error(reason)
                    return
                st.session_state.authenticated = True
                st.session_state.username = full_name.strip()
                st.session_state.employee_id = employee_id.strip()
                st.session_state.auth_error = ""
                seed_track_state(track)
                st.toast("Welcome in. Your onboarding map is ready.")
                st.rerun()

        st.caption("Need help signing in? Contact Nicole Thornton at nicole.thornton@apirx.com")


def render_top_shell():
    track = st.session_state.role_track or "general"
    total_pct = overall_progress()
    next_module = next_incomplete_module()

    left, right = st.columns([1.65, 1], gap="large")
    with left:
        st.markdown(
            f"<section class='hero'><div class='pill'>{TRACKS[track]['label']} Track</div><h1 style='margin:0;'>Welcome, {st.session_state.username or 'New Teammate'}</h1><p style='margin-top:10px;'>Your onboarding flow is modular, guided, and always picks up where you left off.</p></section>",
            unsafe_allow_html=True,
        )
        progress_bar(total_pct)
        st.caption(f"Overall progress: {total_pct}%")

    with right:
        with st.container(border=True):
            st.markdown("### Your Snapshot")
            st.markdown(f"**Employee ID:** {st.session_state.employee_id}")
            st.markdown(f"**Track:** {TRACKS[track]['label']}")
            if next_module:
                st.markdown(f"**Next Up:** Module {next_module['number']} - {next_module['title']}")
            else:
                st.markdown("**Next Up:** All modules complete. Nicely done.")
            st.markdown("<div class='quick-note'>Flow tip: checkboxes first, quick quiz second, then jump to next module.</div>", unsafe_allow_html=True)

        if st.button("Sign Out", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


def render_nav():
    options: list[tuple[str, str]] = [("home", "Home")]
    options.extend((module["key"], f"{module['number']:02d}") for module in active_modules())
    current = st.session_state.nav_key

    with st.container(border=True):
        current_label = "Home"
        if current != "home":
            selected = get_module(current)
            if selected:
                current_label = f"Module {selected['number']}: {selected['title']}"
        st.markdown(
            f"<div class='nav-caption'><span>Jump between modules without losing progress.</span><span class='caption-pill'>Viewing: {current_label}</span></div>",
            unsafe_allow_html=True,
        )
        cols = st.columns(len(options), gap="small")
        for i, (dest, label) in enumerate(options):
            with cols[i]:
                button_label = label if dest == "home" else f"M{label}"
                if st.button(button_label, key=f"nav_{dest}", type="primary" if current == dest else "secondary", use_container_width=True):
                    st.session_state.nav_key = dest
                    st.rerun()


def render_home():
    modules = active_modules()
    done = sum(1 for m in modules if st.session_state.progress.get(m["key"], 0) == 100)
    quiz_done = sum(1 for m in modules if m["key"] in st.session_state.quiz_results)
    next_module = next_incomplete_module()

    next_focus = "Done" if not next_module else f"M{next_module['number']}"
    st.markdown(
        f"""
        <div class="stat-strip">
            <div class="stat-grid">
                <div class="stat-card"><div class="stat-label">Modules Complete</div><div class="stat-value">{done}/{len(modules)}</div></div>
                <div class="stat-card"><div class="stat-label">Overall Progress</div><div class="stat-value">{overall_progress()}%</div></div>
                <div class="stat-card"><div class="stat-label">Quizzes Submitted</div><div class="stat-value">{quiz_done}/{len(modules)}</div></div>
                <div class="stat-card"><div class="stat-label">Current Focus</div><div class="stat-value">{next_focus}</div></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Training Path")
    st.caption("Choose a module card to continue. The experience stays guided and modular.")

    grid = st.columns(2)
    for idx, module in enumerate(modules):
        pct = st.session_state.progress.get(module["key"], 0)
        status = module_status(pct)
        checklist_total = len(module["checklist"])
        checklist_done = sum(1 for v in st.session_state.checklist_items.get(module["key"], {}).values() if v)
        quiz_result = st.session_state.quiz_results.get(module["key"])
        quiz_text = f"{quiz_result[0]}/{quiz_result[1]}" if quiz_result else "Not submitted"

        with grid[idx % 2]:
            with st.container(border=True):
                st.markdown(f"<div class='module-head'><h3>Module {module['number']}: {module['title']}</h3><p>{module['subtitle']}</p></div>", unsafe_allow_html=True)
                progress_bar(pct)
                st.caption(f"Status: {status} | Progress: {pct}%")
                st.markdown(f"Checklist: **{checklist_done}/{checklist_total}**  |  Quiz: **{quiz_text}**")
                if st.button("Open Module", key=f"open_{module['key']}", use_container_width=True, type="primary"):
                    st.session_state.nav_key = module["key"]
                    st.rerun()

def render_contacts():
    with st.container(border=True):
        st.markdown("### Support Contacts")
        for name, role, email, phone in CONTACTS:
            extra = f" | {phone}" if phone else ""
            st.markdown(f"<div class='support-item'><strong>{name}</strong><br/>{role}<br/>{email}{extra}</div>", unsafe_allow_html=True)


def render_checklist(module: dict[str, Any]):
    mk = module["key"]
    with st.container(border=True):
        st.markdown("### Checklist")
        st.caption("Mark each checkpoint as you go. This section contributes 70% of module progress.")
        checklist_values = st.session_state.checklist_items.get(mk, {})
        checked = sum(1 for v in checklist_values.values() if v)
        total = max(1, len(module["checklist"]))
        progress_bar(int(checked / total * 100))
        st.caption(f"Checklist completion: {checked}/{len(module['checklist'])}")

        changed = False
        for item_key, label in module["checklist"].items():
            widget_key = f"ck_{mk}_{item_key}"
            current = st.session_state.checklist_items[mk].get(item_key, False)
            value = st.checkbox(label, key=widget_key, value=current)
            if value != current:
                st.session_state.checklist_items[mk][item_key] = value
                changed = True

        if changed:
            update_module_progress(mk)
            checked = sum(1 for flag in st.session_state.checklist_items[mk].values() if flag)
            st.toast(f"Checklist updated: {checked}/{len(module['checklist'])}")


def render_quiz(module: dict[str, Any]):
    mk = module["key"]
    quiz = module["quiz"]
    with st.container(border=True):
        st.markdown("### Quick Quiz")
        st.caption(f"Quiz credit unlocks at {int(PASSING_FRACTION * 100)}% or higher. Keep it quick and clean.")

        existing = st.session_state.quiz_results.get(mk)
        if existing:
            score, total = existing
            st.success(f"Submitted score: {score}/{total}")
            return

        with st.form(f"quiz_{mk}"):
            answers: list[str | None] = []
            for idx, q in enumerate(quiz, start=1):
                answers.append(st.radio(f"{idx}. {q['q']}", q["options"], index=None, key=f"quiz_{mk}_{idx}"))
            submitted = st.form_submit_button("Submit Quiz", type="primary", use_container_width=True)

        if not submitted:
            return

        if any(a is None for a in answers):
            st.warning("Please answer every quiz question before submitting.")
            return

        score = sum(1 for ans, q in zip(answers, quiz) if ans == q["answer"])
        st.session_state.quiz_results[mk] = (score, len(quiz))
        update_module_progress(mk)
        st.toast("Perfect score." if score == len(quiz) else f"Quiz submitted: {score}/{len(quiz)}")
        st.rerun()


def render_module(module: dict[str, Any]):
    mk = module["key"]
    pct = st.session_state.progress.get(mk, 0)
    mods = active_modules()
    keys = [m["key"] for m in mods]
    idx = keys.index(mk)
    prev_key = keys[idx - 1] if idx > 0 else "home"
    next_key = keys[idx + 1] if idx < len(keys) - 1 else "home"

    st.markdown(f"<div class='module-head'><h3>Module {module['number']}: {module['title']}</h3><p>{module['subtitle']}</p></div>", unsafe_allow_html=True)

    left, right = st.columns([2.1, 1], gap="large")
    with left:
        with st.container(border=True):
            st.markdown("### What This Module Covers")
            st.caption(module["intro"])
            st.markdown("<ul class='guide-list'>" + "".join(f"<li>{bullet}</li>" for bullet in module["bullets"]) + "</ul>", unsafe_allow_html=True)
        render_checklist(module)
        render_quiz(module)

    with right:
        with st.container(border=True):
            st.markdown("### Module Progress")
            progress_bar(pct)
            st.caption(f"{pct}% complete | Status: {module_status(pct)}")
            st.markdown("<div class='quick-note'>Progress formula: 70% checklist + 30% quiz (passing score required).</div>", unsafe_allow_html=True)
            st.markdown("**Guided flow**")
            st.markdown(
                """
                <ul class="guide-list">
                    <li>Read the module context.</li>
                    <li>Complete checklist checkpoints.</li>
                    <li>Submit quiz and move to next module.</li>
                </ul>
                """,
                unsafe_allow_html=True,
            )

        if mk in ("firststeps", "wh_firststeps"):
            render_contacts()

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Previous", key=f"prev_{mk}", use_container_width=True):
                st.session_state.nav_key = prev_key
                st.rerun()
        with c2:
            if st.button("Next", key=f"next_{mk}", use_container_width=True, type="primary"):
                st.session_state.nav_key = next_key
                st.rerun()


def render_app():
    load_progress_once()
    render_top_shell()
    render_nav()

    if st.session_state.nav_key == "home":
        render_home()
        return

    module = get_module(st.session_state.nav_key)
    if not module:
        st.session_state.nav_key = "home"
        st.rerun()
        return
    render_module(module)


def main():
    st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide", initial_sidebar_state="collapsed")
    st.logo(API_LOGO_PATH if os.path.exists(API_LOGO_PATH) else FALLBACK_LOGO_URL, link="https://apirx.com")

    initialize_state()
    inject_theme()

    if not st.session_state.authenticated:
        render_login()
    else:
        render_app()


if __name__ == "__main__":
    main()
