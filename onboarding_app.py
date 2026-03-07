
# -*- coding: utf-8 -*-
"""
AAP / API — New Hire Orientation (Streamlit)
Refactored: safer auth messages, throttled Google Sheets I/O, clearer progress calc,
optional mock mode, centralized constants, friendlier copy and less corporate tone.

File: onboarding_app_clean.py
"""

import os
import json
import base64
import logging
from datetime import datetime
from textwrap import dedent

import streamlit as st
import streamlit.components.v1 as components

try:
    import gspread
except Exception:  # pragma: no cover
    gspread = None  # Allows mock mode without gspread installed

# ─────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aap_onboarding")

# ─────────────────────────────────────────────
# Constants & feature flags
# ─────────────────────────────────────────────
APP_TITLE = "AAP New Hire Orientation"
APP_EMOJI = "🎓"

COMPANY_LOGO_URL = "https://rxaap.com/wp-content/uploads/2021/03/AAP_Logo_White.png"
API_LOGO_PATH = "assets/api_logo.png"
PAYLOCITY_COMPANY_ID = "123959"

# Feature flags
USE_MOCK_SHEETS = os.getenv("MOCK_SHEETS", "0") == "1"
SHOW_PLACEHOLDERS = os.getenv("SHOW_PLACEHOLDERS", "0") == "1"
PASSING_FRACTION = 0.75  # quiz must reach >= 75% to award the 30% quiz credit

# Contacts (used in multiple modules)
CONTACTS = [
    ("Brandy Hooper", "VP of Human Resources", "brandy.hooper@rxaap.com", "256-574-7526"),
    ("Nicole Thornton", "HR Administrator (API)", "nicole.thornton@apirx.com", "256-574-7528"),
    ("CBIZ Benefits", "Benefits Broker", "844.200.CBIZ (2249)", ""),
    ("Teladoc", "Free Telehealth", "800-835-2362 / Teladoc.com", ""),
    ("LifeMatters EAP", "Employee Assistance", "800-634-6433 / mylifematters.com", ""),
    ("BCBS of Alabama", "Medical Insurance", "888-267-2955 / bcbsal.org", ""),
    ("Guardian", "Dental, Vision, Life, Disability", "888-482-7342 / guardiananytime.com", ""), 
    ("HealthEquity", "HSA Accounts", "866-274-9887 / healthequity.com", ""),
]

# ─────────────────────────────────────────────
# Utility helpers
# ─────────────────────────────────────────────
def _logo_img_src() -> str:
    """Return an img src usable inside raw HTML: base64 for local file, URL otherwise."""
    if os.path.exists(API_LOGO_PATH):
        with open(API_LOGO_PATH, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            return f"data:image/png;base64,{b64}"
    return COMPANY_LOGO_URL


def pct_bar(pct: int) -> str:
    pct = max(0, min(100, int(pct)))
    return dedent(f"""
    <div style="height:10px;background:#F0F2F6;border-radius:999px;overflow:hidden;">
      <div style="width:{pct}%;height:10px;background:linear-gradient(90deg,#84fab0,#8fd3f4);"></div>
    </div>
    <div style="font-size:12px;color:#6c757d;margin-top:6px;">{pct}% complete</div>
    """).strip()


# ─────────────────────────────────────────────
# Streamlit page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_EMOJI,
    layout="wide",
    initial_sidebar_state="expanded",
)

# Native Streamlit logo in sidebar
st.logo(API_LOGO_PATH if os.path.exists(API_LOGO_PATH) else COMPANY_LOGO_URL, link="https://apirx.com")

# ─────────────────────────────────────────────
# Google Sheets integration (with mock mode)
# ─────────────────────────────────────────────

# Mock storage (for local dev/testing)
_mock_progress_rows = []  # list of dicts representing sheet rows


@st.cache_resource
def get_gsheet_client():
    if USE_MOCK_SHEETS:
        return None  # not needed in mock mode
    if gspread is None:
        logger.warning("gspread not available; enable MOCK_SHEETS=1 for local testing.")
        return None
    try:
        creds_dict = dict(st.secrets["gcp_service_account"])  # type: ignore[index]
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        return gspread.service_account_from_dict(creds_dict, scopes=scopes)  # type: ignore[attr-defined]
    except Exception as e:  # pragma: no cover
        logger.exception("Failed to init GSheet client: %s", e)
        return None


def get_sheet(client):
    if USE_MOCK_SHEETS:
        class MockSheet:
            def get_all_records(self):
                return [
                    {
                        "Employee ID": r[0],
                        "Employee Name": r[1],
                        "Module Key": r[2],
                        "Completion %": r[3],
                        "Checklist Items": r[4],
                        "Quiz Score": r[5],
                        "Last Updated": r[6],
                    } for r in _mock_progress_rows
                ]

            def update(self, _range, data):
                # data is [[cols...]]
                values = data[0]
                emp_id, emp_name, module_key = values[0], values[1], values[2]
                for i, r in enumerate(_mock_progress_rows):
                    if r[0] == emp_id and r[2] == module_key:
                        _mock_progress_rows[i] = values
                        break

            def append_row(self, data):
                _mock_progress_rows.append(data)
        return MockSheet()

    try:
        return client.open("AAP New Hire Orientation Progress").sheet1  # type: ignore[union-attr]
    except Exception as e:  # pragma: no cover
        logger.exception("Failed to open progress sheet: %s", e)
        return None


def get_employee_sheet(client):
    if USE_MOCK_SHEETS:
        class MockRoster:
            def get_all_records(self):
                # A tiny fake roster for local runs
                return [
                    {"Employee ID": "10001", "Full Name": "Sample User", "Track": "General"},
                    {"Employee ID": "20001", "Full Name": "Warehouse User", "Track": "Warehouse"},
                ]
        return MockRoster()
    try:
        return client.open("AAP New Hire Orientation Progress").worksheet("Employee Roster")  # type: ignore[union-attr]
    except Exception as e:  # pragma: no cover
        logger.exception("Failed to open roster sheet: %s", e)
        return None


# ─────────────────────────────────────────────
# Authentication
# ─────────────────────────────────────────────

def verify_employee(access_code: str, employee_id: str, full_name: str) -> tuple[bool, str, str]:
    """Three-part check; returns (ok, track, reason). Track is 'general' or 'warehouse'."""
    try:
        correct_code = st.secrets["orientation_access_code"]  # type: ignore[index]
    except Exception:
        return False, "", "Configuration error. Please contact HR."

    if access_code.strip() != correct_code.strip():
        return False, "", "Incorrect credentials."

    client = get_gsheet_client()
    emp_sheet = get_employee_sheet(client) if not USE_MOCK_SHEETS else get_employee_sheet(None)
    if not emp_sheet:
        return False, "", "Employee roster is unavailable right now. Please try again."

    try:
        records = emp_sheet.get_all_records()
        if not records:
            return False, "", "Employee roster is empty. Please contact HR."

        emp_id_norm = employee_id.strip().lower()
        name_norm = full_name.strip().lower()

        for row in records:
            row_id = str(row.get("Employee ID", "")).strip().lower()
            row_name = str(row.get("Full Name", "")).strip().lower()
            if row_id == emp_id_norm:
                if row_name == name_norm:
                    raw_track = str(row.get("Track", "")).strip().lower()
                    track = "warehouse" if raw_track == "warehouse" else "general"
                    return True, track, ""
                else:
                    return False, "", "Employee ID and name did not match our records."
        return False, "", "Employee record not found. Please verify your ID or contact HR."
    except Exception as e:  # pragma: no cover
        logger.exception("Verification error: %s", e)
        return False, "", "Verification error. Please try again."


# ─────────────────────────────────────────────
# Progress storage (debounced & cached row index)
# ─────────────────────────────────────────────
if "row_index_cache" not in st.session_state:
    st.session_state["row_index_cache"] = {}


def save_progress(employee_id: str, employee_name: str, module_key: str, pct: int,
                   checklist_items: dict, quiz_tuple: tuple | None):
    client = get_gsheet_client()
    sheet = get_sheet(client) if not USE_MOCK_SHEETS else get_sheet(None)
    if not sheet:
        return
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        checklist_json = json.dumps(checklist_items)
        quiz_score = None if not quiz_tuple else quiz_tuple[0]
        data = [employee_id, employee_name, module_key, pct, checklist_json, quiz_score, now]

        cache_key = (employee_id, module_key)
        row_idx = st.session_state["row_index_cache"].get(cache_key)

        if row_idx is None:
            records = sheet.get_all_records()
            for i, row in enumerate(records, start=2):
                if row.get("Employee ID") == employee_id and row.get("Module Key") == module_key:
                    row_idx = i
                    st.session_state["row_index_cache"][cache_key] = row_idx
                    break

        if row_idx:
            sheet.update(f"A{row_idx}:G{row_idx}", [data])
        else:
            sheet.append_row(data)
    except Exception as e:  # pragma: no cover
        logger.exception("Failed to save progress: %s", e)



def load_progress(employee_id: str) -> dict:
    client = get_gsheet_client()
    sheet = get_sheet(client) if not USE_MOCK_SHEETS else get_sheet(None)
    if not sheet:
        return {}
    try:
        records = sheet.get_all_records()
        result = {}
        for row in records:
            if str(row.get("Employee ID", "")).strip() == employee_id.strip():
                mk = row.get("Module Key", "")
                try:
                    checklist = json.loads(row.get("Checklist Items", "{}"))
                except Exception:
                    checklist = {}
                result[mk] = {
                    "pct": row.get("Completion %", 0),
                    "checklist": checklist,
                    "quiz": None if row.get("Quiz Score") is None else (int(row.get("Quiz Score")), None),
                }
        return result
    except Exception as e:  # pragma: no cover
        logger.exception("Failed to load progress: %s", e)
        return {}


# ─────────────────────────────────────────────
# Module definitions (metadata only; content rendered below)
# ─────────────────────────────────────────────
MODULES = [
    {"key": "welcome", "number": 1, "title": "Welcome to AAP", "subtitle": "Our history, mission, vision & values", "icon": "🏢"},
    {"key": "conduct", "number": 2, "title": "Code of Conduct & Ethics", "subtitle": "Expected behaviors, confidentiality & EEO", "icon": "⚖️"},
    {"key": "policies", "number": 3, "title": "Workplace Policies", "subtitle": "Attendance, appearance, safety & more", "icon": "📋"},
    {"key": "timeoff", "number": 4, "title": "Time Off & Leave", "subtitle": "PTO, holidays, sick leave & attendance rules", "icon": "⏰"},
    {"key": "benefits", "number": 5, "title": "Benefits", "subtitle": "Health, 401k, life insurance & perks", "icon": "💼"},
    {"key": "firststeps", "number": 6, "title": "Your First Steps", "subtitle": "Systems, contacts & what to expect", "icon": "🚀"},
]

WAREHOUSE_MODULES = [
    {"key": "wh_welcome", "number": 1, "title": "Welcome to AAP — Warehouse", "subtitle": "Mission, values & your role", "icon": "🏢"},
    {"key": "wh_conduct", "number": 2, "title": "Code of Conduct & Ethics", "subtitle": "Warehouse-specific expectations", "icon": "⚖️"},
    {"key": "wh_safety", "number": 3, "title": "Warehouse Policies & Safety", "subtitle": "Attendance, PPE, safety rules", "icon": "🦺"},
    {"key": "wh_timeoff", "number": 4, "title": "Time Off & Leave", "subtitle": "Requests, FMLA & life events", "icon": "⏰"},
    {"key": "wh_benefits", "number": 5, "title": "Benefits — Warehouse", "subtitle": "Health, 401k & support programs", "icon": "💼"},
    {"key": "wh_firststeps", "number": 6, "title": "Your First Steps — Warehouse", "subtitle": "Day 1, training & contacts", "icon": "🚀"},
]

# ─────────────────────────────────────────────
# Session state defaults
# ─────────────────────────────────────────────
def _init_state():
    defaults = {
        "authenticated": False,
        "username": "",
        "employee_id": "",
        "role_track": "",  # "general" or "warehouse"
        "selected_module": None,
        "sheet_loaded": False,
        "progress": {},
        "quiz_results": {},  # key -> (score, max)
        "checklist_items": {},
        "auth_error": "",
        "sound_enabled": True,
        "last_milestone_bucket": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


_init_state()


# ─────────────────────────────────────────────
# Progress math
# ─────────────────────────────────────────────

def calculate_module_pct(module_key: str, checklists: dict, quiz_results: dict) -> int:
    items = checklists.get(module_key, {})
    total = len(items)
    checked = sum(1 for v in items.values() if v)
    checklist_pct = (checked / total * 70) if total > 0 else 0

    qt = quiz_results.get(module_key)  # (score, max)
    quiz_pct = 0
    if qt:
        score, mx = qt
        if mx and mx > 0 and (score / mx) >= PASSING_FRACTION:
            quiz_pct = 30
    return int(checklist_pct + quiz_pct)


def update_progress(module_key: str):
    prev = st.session_state.progress.get(module_key, 0)
    st.session_state.progress[module_key] = calculate_module_pct(
        module_key, st.session_state.checklist_items, st.session_state.quiz_results
    )

    # Celebrate module completion
    if prev < 100 and st.session_state.progress[module_key] == 100:
        st.toast("Nice! Module completed.", icon="🎉")

    # Persist
    if st.session_state.authenticated and st.session_state.employee_id:
        items = st.session_state.checklist_items.get(module_key, {})
        quiz_tuple = st.session_state.quiz_results.get(module_key)
        save_progress(
            st.session_state.employee_id,
            st.session_state.username,
            module_key,
            st.session_state.progress[module_key],
            items,
            quiz_tuple,
        )


# ─────────────────────────────────────────────
# UI helpers
# ─────────────────────────────────────────────

def section_header(title: str, subtitle: str | None = None, emoji: str | None = None):
    e = (emoji + " ") if emoji else ""
    st.markdown(f"## {e}{title}")
    if subtitle:
        st.caption(subtitle)


def inject_ui_enhancements(sound_enabled: bool):
    """Inject a modern visual skin + subtle interaction audio hooks."""
    st.markdown(
        """
        <style>
        :root {
            --brand-start: #6d5efc;
            --brand-end: #15c5ff;
            --soft-border: rgba(109, 94, 252, 0.18);
            --card-shadow: 0 12px 34px rgba(26, 43, 93, 0.08);
        }
        .stApp {
            background:
                radial-gradient(circle at top right, rgba(21,197,255,0.10), transparent 40%),
                radial-gradient(circle at top left, rgba(109,94,252,0.08), transparent 35%),
                #f8faff;
        }
        [data-testid="stMetric"] {
            border: 1px solid var(--soft-border);
            border-radius: 16px;
            padding: 10px 14px;
            background: rgba(255,255,255,0.78);
            backdrop-filter: blur(4px);
            box-shadow: var(--card-shadow);
            transition: transform 180ms ease, box-shadow 180ms ease;
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 38px rgba(26, 43, 93, 0.12);
        }
        [data-testid="stVerticalBlockBorderWrapper"] {
            border: 1px solid var(--soft-border) !important;
            border-radius: 18px !important;
            background: rgba(255,255,255,0.86);
            box-shadow: var(--card-shadow);
            animation: fadeInUp 280ms ease;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(255,255,255,0.92), rgba(248,250,255,0.92));
            border-right: 1px solid rgba(109, 94, 252, 0.14);
        }
        .stButton > button, .stFormSubmitButton > button {
            border-radius: 12px;
            border: 1px solid transparent;
            background: linear-gradient(90deg, var(--brand-start), var(--brand-end));
            color: #fff;
            font-weight: 600;
            transition: transform 150ms ease, filter 150ms ease;
        }
        .stButton > button:hover, .stFormSubmitButton > button:hover {
            transform: translateY(-1px);
            filter: brightness(1.04);
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(4px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @media (prefers-reduced-motion: reduce) {
            * { animation: none !important; transition: none !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    components.html(
        f"""
        <script>
        (function() {{
            const parentDoc = window.parent.document;
            window.aapSoundEnabled = {str(sound_enabled).lower()};
            if (parentDoc.body.dataset.aapEnhanceBound === "1") return;
            parentDoc.body.dataset.aapEnhanceBound = "1";

            let ctx;
            const tone = (freq, dur, type = "sine", vol = 0.03) => {{
                if (!window.aapSoundEnabled) return;
                try {{
                    ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
                    const o = ctx.createOscillator();
                    const g = ctx.createGain();
                    o.type = type;
                    o.frequency.value = freq;
                    g.gain.value = vol;
                    o.connect(g);
                    g.connect(ctx.destination);
                    const t = ctx.currentTime;
                    g.gain.setValueAtTime(vol, t);
                    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
                    o.start(t);
                    o.stop(t + dur);
                }} catch (e) {{}}
            }};

            const playNav = () => {{ tone(480, 0.09, "triangle", 0.03); setTimeout(() => tone(660, 0.10, "triangle", 0.022), 55); }};
            const playCheck = () => {{ tone(740, 0.08, "sine", 0.026); }};
            const playQuiz = () => {{ tone(520, 0.12, "triangle", 0.028); setTimeout(() => tone(660, 0.13, "triangle", 0.024), 90); setTimeout(() => tone(880, 0.16, "sine", 0.022), 180); }};

            parentDoc.addEventListener("click", (event) => {{
                const nav = event.target.closest('[data-testid="stSidebar"] [role="radiogroup"] label');
                if (nav) playNav();

                const btn = event.target.closest("button");
                if (btn && /submit quiz/i.test((btn.innerText || "").trim())) playQuiz();
            }}, true);

            parentDoc.addEventListener("change", (event) => {{
                const checkbox = event.target.closest('input[type="checkbox"]');
                if (checkbox) playCheck();
            }}, true);
        }})();
        </script>
        """,
        height=0,
    )


# ─────────────────────────────────────────────
# LOGIN SCREEN
# ─────────────────────────────────────────────

def show_login():
    logo_src = _logo_img_src()

    col_l, col_m, col_r = st.columns([0.5, 2, 0.5])
    with col_m:
        st.markdown(
            f"""
            <div style="text-align:center;">
              <img src="{logo_src}" alt="AAP/API" style="height:48px;margin-bottom:10px;"/>
              <div style="font-size:30px;font-weight:700;">Welcome to Your First Week ✨</div>
              <div style="color:#6c757d;">Friendly, guided onboarding — made for humans, not handbooks.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")
        with st.form("login_form", clear_on_submit=False):
            st.subheader("Employee sign in")
            st.caption("Enter the info HR shared with you.")
            access_code = st.text_input("Access Code", type="password")
            employee_id = st.text_input("Employee ID", placeholder="e.g., 10042")
            full_name = st.text_input("Full Name", placeholder="As it appears in your HR paperwork")
            submitted = st.form_submit_button("Sign in →", use_container_width=True)

        if st.session_state.get("auth_error"):
            st.error(st.session_state.auth_error)
        else:
            st.info("We keep this secure and private.")

        if submitted:
            if not access_code or not employee_id or not full_name:
                st.error("Please fill in all three fields to continue.")
            else:
                with st.spinner("Verifying your credentials…"):
                    ok, track, reason = verify_employee(access_code, employee_id, full_name)
                    if ok:
                        # Initialize track-specific keys
                        active = WAREHOUSE_MODULES if track == "warehouse" else MODULES
                        st.session_state.authenticated = True
                        st.session_state.username = full_name.strip()
                        st.session_state.employee_id = employee_id.strip()
                        st.session_state.role_track = track
                        st.session_state.progress = {m["key"]: 0 for m in active}
                        st.session_state.checklist_items = {m["key"]: {} for m in active}
                        st.session_state.quiz_results = {}
                        st.session_state.sheet_loaded = False
                        st.session_state.auth_error = ""
                        st.toast("Welcome aboard!", icon="✨")
                        st.balloons()
                        st.rerun()
                    else:
                        st.session_state.auth_error = reason
                        st.error(reason)

        st.write("")
        st.caption("Need help? HR · Nicole Thornton · nicole.thornton@apirx.com · 256-574-7528")


# ─────────────────────────────────────────────
# Sidebar (when authenticated)
# ─────────────────────────────────────────────

def render_sidebar():
    active_modules = WAREHOUSE_MODULES if st.session_state.get("role_track") == "warehouse" else MODULES

    # Load progress from sheet once per login session
    if not st.session_state.sheet_loaded:
        saved = load_progress(st.session_state.employee_id)
        if saved:
            for mk, data in saved.items():
                st.session_state.progress[mk] = data.get("pct", 0)
                st.session_state.checklist_items[mk] = data.get("checklist", {})
                if data.get("quiz"):
                    st.session_state.quiz_results[mk] = data["quiz"]
        st.session_state.sheet_loaded = True

    # Header card
    st.markdown(
        f"""
        <div style="padding:8px 0 2px 0;">
          <div style="font-weight:700;font-size:16px;">Learning Interface</div>
          <div style="color:#6c757d;">👤 {st.session_state.username}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    active_keys = [m["key"] for m in active_modules]
    total_pct = int(sum(st.session_state.progress.get(k, 0) for k in active_keys) / max(len(active_keys), 1))
    st.markdown(pct_bar(total_pct), unsafe_allow_html=True)

    st.markdown("### Navigation")
    nav_options = ["🏠 Home"] + [f"{m['icon']} {m['number']}. {m['title']}" for m in active_modules]
    module_keys = [None] + [m["key"] for m in active_modules]

    try:
        current_idx = module_keys.index(st.session_state.selected_module)
    except ValueError:
        current_idx = 0

    selected_nav = st.radio("Navigation", nav_options, index=current_idx, label_visibility="collapsed")
    new_key = module_keys[nav_options.index(selected_nav)]
    if new_key != st.session_state.selected_module:
        destination = "Home" if new_key is None else next((m["title"] for m in active_modules if m["key"] == new_key), "Module")
        st.toast(f"Navigating to {destination}", icon="🧭")
        st.session_state.selected_module = new_key
        st.rerun()

    st.markdown("---")
    st.toggle("🔈 Interface sounds", key="sound_enabled")

    if st.button("🚪 Sign Out", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.markdown("---")
    st.caption("Built with care — an onboarding experience designed for clarity and confidence.")


# ─────────────────────────────────────────────
# Home view
# ─────────────────────────────────────────────

def render_module_card(module: dict):
    pct = st.session_state.progress.get(module["key"], 0)
    status = "Complete ✓" if pct == 100 else ("In Progress" if pct > 0 else "Queued")

    with st.container(border=True):
        st.markdown(f"**{module['icon']} Module {module['number']}: {module['title']}**  ")
        st.caption(module["subtitle"])
        st.progress(pct)
        st.write(status)
        if st.button(f"Launch Module {module['number']}", key=f"open_{module['key']}", use_container_width=True):
            st.session_state.selected_module = module["key"]
            st.rerun()


def show_home():
    is_wh = st.session_state.get("role_track") == "warehouse"
    active_modules = WAREHOUSE_MODULES if is_wh else MODULES
    track_label = "Warehouse" if is_wh else "General"
    name_display = st.session_state.username or "Team Member"

    module_progress = [st.session_state.progress.get(m["key"], 0) for m in active_modules]
    completed = sum(1 for p in module_progress if p == 100)
    total_pct = int(sum(module_progress) / max(len(active_modules), 1))
    quizzes_done = sum(1 for m in active_modules if st.session_state.quiz_results.get(m["key"]))

    st.markdown(f"## {track_label} Learning Dashboard · {name_display}")
    st.caption("Everything you need to get started — all in one place.")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Modules Done", f"{completed}/{len(active_modules)}")
    with c2:
        st.metric("Overall Progress", f"{total_pct}%")
    with c3:
        st.metric("Quizzes Submitted", f"{quizzes_done}/{len(active_modules)}")

    st.markdown("### Training Modules — pick up where you left off")
    left_col, right_col = st.columns(2)
    for idx, module in enumerate(active_modules):
        target_col = left_col if idx % 2 == 0 else right_col
        with target_col:
            render_module_card(module)


# ─────────────────────────────────────────────
# Module content renderers (trimmed HTML; warm tone)
# Each uses the same checklist/quiz patterns as original.
# ─────────────────────────────────────────────

def checklist_block(mk: str, items: dict):
    if mk not in st.session_state.checklist_items or not st.session_state.checklist_items[mk]:
        st.session_state.checklist_items[mk] = {k: False for k in items}
    changed = False
    for key, label in items.items():
        val = st.checkbox(label, value=st.session_state.checklist_items[mk].get(key, False), key=f"{mk}_chk_{key}")
        if val != st.session_state.checklist_items[mk].get(key, False):
            st.session_state.checklist_items[mk][key] = val
            changed = True
    if changed:
        checked_count = sum(1 for v in st.session_state.checklist_items[mk].values() if v)
        total_items = len(st.session_state.checklist_items[mk])
        st.toast(f"Checklist updated · {checked_count}/{total_items}", icon="✅")
        update_progress(mk)


def quiz_block(mk: str, questions: list[tuple[str, list[str], str]]):
    existing = st.session_state.quiz_results.get(mk)
    if existing:
        score, mx = existing
        st.success(f"✅ Quiz submitted! You scored {score}/{mx}.")
        return
    with st.form(f"quiz_{mk}"):
        selections = []
        for i, (prompt, options, _answer) in enumerate(questions, start=1):
            sel = st.radio(f"{i}. {prompt}", options, index=None, key=f"{mk}_q{i}")
            selections.append(sel)
        submitted = st.form_submit_button("Submit Quiz")
        if submitted:
            score = 0
            for sel, (_, options, answer) in zip(selections, questions):
                if sel == answer:
                    score += 1
            st.session_state.quiz_results[mk] = (score, len(questions))
            if score == len(questions):
                st.toast("Perfect score! Outstanding work.", icon="🏆")
            else:
                st.toast(f"Quiz submitted · {score}/{len(questions)}", icon="🧠")
            update_progress(mk)
            st.rerun()


# --- General modules ---

def show_module_welcome():
    section_header("Module 1: Welcome to AAP", "Our history, mission, vision & values", "🏢")
    st.write(
        """
        On behalf of your colleagues — welcome! We believe each teammate contributes
        directly to AAP's success, and we’re excited you’re here. This orientation gives
        you the essentials without the corporate fluff.

        **Who we are**  
        AAP (American Associated Pharmacies) formed in **2009**, combining two major
        cooperatives to support independent pharmacies nationwide. Today we operate API,
        our independent warehouse and distributor, with two U.S. locations.

        **Mission** — Support independent community pharmacies with solutions that
        increase profitability, streamline operations, and improve patient care.

        **Vision** — Help independent pharmacies thrive in a competitive market.

        **Values** — Customer Focus · Integrity · Respect · Excellence · Ownership
        """
    )
    st.markdown("### ✅ Checklist")
    checklist_block("welcome", {
        "ceo_welcome": "I read the welcome message.",
        "who_we_are": "I understand who AAP is and when it was founded.",
        "mission": "I can explain AAP's mission.",
        "vision": "I can explain AAP's vision.",
        "values_5": "I can name all five core values.",
        "values_conduct": "I understand values guide both what we do and how we do it.",
        "two_locations": "I know API operates two warehouse locations.",
    })
    st.markdown("### 📝 Quick Quiz")
    quiz_block("welcome", [
        ("In what year was AAP formed?", ["2005", "2007", "2009", "2012"], "2009"),
        ("Which city is home to API?", ["Phoenix, AZ", "Scottsboro, AL", "Huntsville, AL", "Nashville, TN"], "Scottsboro, AL"),
        ("Which is NOT a core value?", ["Integrity", "Ownership", "Innovation", "Excellence"], "Innovation"),
        ("Customer service is best described as:", [
            "A department that handles complaints",
            "An attitude shared by all employees",
            "Management’s responsibility only",
            "A program run by HR"],
            "An attitude shared by all employees"
        ),
    ])


def show_module_conduct():
    section_header("Module 2: Code of Conduct & Ethics", "Do the right thing, every time", "⚖️")
    st.write(
        """
        Trust is our backbone. We comply with laws and expect everyone to act with
        integrity, professionalism, and respect. Report concerns promptly — no retaliation.

        **Unacceptable conduct (examples)** — Theft, falsifying records, harassment,
        unsafe behavior, working under the influence, unauthorized equipment use, 
        no‑call/no‑show, and disclosing confidential information.

        **EEO** — Employment decisions are based on merit, qualifications, and abilities.
        """
    )
    st.markdown("### ✅ Checklist")
    checklist_block("conduct", {
        "code_reviewed": "I’ve read the Code of Conduct.",
        "unacceptable": "I understand examples of unacceptable conduct.",
        "eeo": "I understand AAP's EEO policy.",
        "harassment": "I know how to report harassment (no retaliation).",
        "confidentiality": "I understand confidentiality and will sign the NDA.",
        "conflicts": "I will disclose any conflicts of interest.",
        "reporting": "I will report known/suspected illegal or unethical behavior.",
    })
    st.markdown("### 📝 Quick Quiz")
    quiz_block("conduct", [
        ("AAP's employment decisions are based on:", ["Seniority", "Merit, qualifications, and abilities", "Education only", "Manager discretion"], "Merit, qualifications, and abilities"),
        ("If you witness suspected unethical behavior, you should:", ["Ignore it", "Post on social", "Report to your supervisor immediately", "Wait to see if it repeats"], "Report to your supervisor immediately"),
        ("Which is NOT sexual harassment?", ["Offensive jokes about appearance", "A professional performance evaluation", "Showing sexual images", "Implied promises tied to sexual conduct"], "A professional performance evaluation"),
        ("Refusing to sign the NDA results in:", ["Warning", "HR meeting", "Immediate termination", "Probation"], "Immediate termination"),
    ])


def show_module_policies():
    section_header("Module 3: Workplace Policies", "Attendance, appearance, safety & more", "📋")
    st.write(
        """
        **Attendance (no‑fault points)**  
        • Tardy ≤ 5 min: 0  
        • Tardy/early leave (< 4 hrs): ½  
        • 4+ hrs absence/tardy/early leave: 1  
        • No call ≥ 15 min after start: 1½  

        **Corrective actions (12‑month window)**  
        • 5 pts: Coaching  
        • 6 pts: Verbal warning  
        • 7 pts: Written warning  
        • 8 pts: Termination  

        **Perks for perfect attendance** — 1 point removed after **2 consecutive months**; **$75** bonus after **3 months**.

        **Other highlights** — Dress appropriately; Drug & alcohol‑free workplace; Report safety issues and injuries immediately; Company systems are for business use.
        """
    )
    st.info("No‑call/no‑show for 2 consecutive days may be treated as a voluntary resignation.")

    st.markdown("### ✅ Checklist")
    checklist_block("policies", {
        "point_system": "I understand the attendance point system.",
        "corrective_levels": "I know corrective steps (5: coaching · 6: verbal · 7: written · 8: termination).",
        "perfect_att": "I know point removal and $75 bonus rules.",
        "no_call": "I understand 2-day no‑call/no‑show can be a resignation.",
        "appearance": "I understand appearance standards.",
        "drug_policy": "I understand the drug & alcohol policy.",
        "safety": "I will report unsafe conditions or injuries immediately.",
        "computer_policy": "I understand business‑use of computer/email systems.",
    })
    st.markdown("### 📝 Quick Quiz")
    quiz_block("policies", [
        ("Points for a full shift no‑call/no‑show?", ["½", "1", "1½", "2"], "1½"),
        ("At how many points is employment terminated?", ["6", "7", "8", "10"], "8"),
        ("Consecutive months for $75 bonus?", ["1", "2", "3", "6"], "3"),
        ("Who owns the safety program?", ["CEO", "VP of HR", "Dept heads", "OSHA"], "VP of HR"),
        ("Pre‑approved vacation days are excluded from points.", ["True", "False"], "True"),
    ])


def show_module_timeoff():
    section_header("Module 4: Time Off & Leave", "Plan ahead with confidence", "⏰")
    st.write(
        """
        **Vacation & holidays** — Pre‑approved vacation days don’t add attendance points.  
        **Sick leave** — Long‑Term Sick Leave requires **3+ consecutive physician‑mandated days**.  
        **FMLA** — Generally requires **12 months** of service and **1,250** hours worked.  
        **Life events** — Notify HR within **30 days** to update benefits.
        """
    )
    st.markdown("### ✅ Checklist")
    checklist_block("timeoff", {
        "vacation_rules": "I understand pre‑approved vacation & points.",
        "holiday_awareness": "I know holiday/time‑off expectations for my schedule.",
        "sick_leave_trigger": "I know when Long‑Term Sick Leave applies.",
        "fmla_baseline": "I know baseline FMLA eligibility.",
        "life_event_window": "I know the 30‑day window for benefits changes.",
    })
    st.markdown("### 📝 Quick Quiz")
    quiz_block("timeoff", [
        ("Pre‑approved vacation days are excluded from points.", ["True", "False"], "True"),
        ("LTSL requires:", ["1 day", "3+ consecutive physician‑mandated days", "5 days", "Any doctor note"], "3+ consecutive physician‑mandated days"),
        ("FMLA eligibility requires:", ["60 days", "6 months", "12 months & 1,250 hours", "Manager approval"], "12 months & 1,250 hours"),
        ("Report qualifying life events within:", ["7 days", "14 days", "30 days", "60 days"], "30 days"),
    ])


def show_module_benefits():
    section_header("Module 5: Benefits", "Health, retirement & day‑one resources", "💼")
    st.write(
        """
        **Health** — Medical, dental, vision become effective on the **1st of the month after 60 days** (eligibility applies).  
        **401(k)** — Company matches **100%** of the first **3%** you contribute.  
        **Day‑one** — Teladoc and LinkedIn Learning are available right away.
        """
    )
    st.markdown("### ✅ Checklist")
    checklist_block("benefits", {
        "health_effective": "I know when health coverage begins.",
        "plan_options": "I know there are multiple medical plan options.",
        "401k_match": "I understand the 401(k) match.",
        "teladoc_day1": "I know Teladoc is available day one for my household.",
        "support_resources": "I can find EAP, BenefitHub, and LinkedIn Learning.",
    })
    st.markdown("### 📝 Quick Quiz")
    quiz_block("benefits", [
        ("Health benefits become effective on:", [
            "Your first day",
            "1st of the month after 60 days",
            "After 90 days",
            "January 1 next year"], "1st of the month after 60 days"),
        ("401(k) match on the first 3%:", ["50%", "75%", "100%", "200%"], "100%"),
        ("Teladoc is available to:", ["FT only", "FT & PT", "Everyone in your household, Day 1", "After 60 days"], "Everyone in your household, Day 1"),
        ("Day‑one resource:", ["BenefitHub & LinkedIn Learning", "Medical enrollment", "401(k) contributions", "FMLA"], "BenefitHub & LinkedIn Learning"),
    ])


def show_module_firststeps():
    section_header("Module 6: Your First Steps", "Let’s get you set up", "🚀")
    st.write(
        f"""
        **Documents to sign** — Direct Deposit · Acknowledgments · W‑4/A‑4 · NDA · I‑9 · Handbook.  
        **Paylocity** — Register at access.paylocity.com (Company ID: **{PAYLOCITY_COMPANY_ID}**).  
        **BambooHR** — HR will walk you through it. Add a profile photo.  
        **LinkedIn Learning** — Activation email at offer; ask HR if missing.  
        **Teladoc** — Visit Teladoc.com → Get Started. Free general & mental health visits.
        """
    )

    st.markdown("### 👥 Key Contacts")
    for name, role, contact, phone in CONTACTS:
        line = f"**{name}** — {role} · {contact}"
        if phone:
            line += f" · {phone}"
        st.write("- " + line)

    st.markdown("### ✅ Checklist")
    checklist_block("firststeps", {
        "paperwork": "I know what I’m signing during orientation.",
        "paylocity": f"I know how to register for Paylocity (Company ID: {PAYLOCITY_COMPANY_ID}).",
        "bamboohr": "I know what BambooHR is for (and to upload my photo).",
        "linkedin": "I have my LinkedIn Learning activation or know how to request it.",
        "teladoc_setup": "I know how to set up my Teladoc account.",
        "key_contacts": "I know who to contact for HR, benefits, payroll, and telehealth.",
        "first90": "I know the 30/60/90‑day expectations.",
        "at_will": "I understand AAP is an at‑will employer.",
        "life_event": "I know I have 30 days to notify HR of qualifying life events.",
    })
    st.markdown("### 📝 Quick Quiz")
    quiz_block("firststeps", [
        ("What’s the Paylocity Company ID?", ["123456", "123959", "987654", "112358"], "123959"),
        ("Notify HR of a qualifying life event within:", ["7 days", "14 days", "30 days", "60 days"], "30 days"),
        ("Which is available Day 1?", ["Medical", "Vacation accrual", "Teladoc & LinkedIn Learning", "401(k)"], "Teladoc & LinkedIn Learning"),
        ("Employment at AAP is:", ["Fixed term", "At‑will", "Union‑protected", "2‑year commitment"], "At‑will"),
    ])


# --- Warehouse modules (content adapted) ---

def show_wh_module_welcome():
    section_header("Module 1: Welcome — Warehouse", "Your role in the operation", "🏢")
    st.write(
        """
        You’re on the front lines of AAP’s mission. Accuracy, speed, and care in the
        warehouse directly impact pharmacies and their patients. What you do matters.

        Mission · Vision · Values are the same — now applied to the warehouse floor.
        """
    )
    st.markdown("### ✅ Checklist")
    checklist_block("wh_welcome", {
        "ceo_welcome": "I read the CEO welcome message.",
        "who_we_are": "I understand who AAP is and when it was founded.",
        "my_role": "I understand the warehouse team’s role.",
        "mission": "I can explain AAP's mission.",
        "vision": "I can explain AAP's vision.",
        "values_5": "I can name all five core values.",
        "values_warehouse": "I know how our values apply on the floor.",
    })
    st.markdown("### 📝 Quick Quiz")
    quiz_block("wh_welcome", [
        ("In what year was AAP formed?", ["2005", "2007", "2009", "2012"], "2009"),
        ("Which city is home to API?", ["Phoenix, AZ", "Scottsboro, AL", "Huntsville, AL", "Nashville, TN"], "Scottsboro, AL"),
        ("Which is NOT a core value?", ["Integrity", "Ownership", "Innovation", "Excellence"], "Innovation"),
        ("Ownership on the floor means:", [
            "Only managers take ownership",
            "Report damage/errors/near‑misses and help fix them",
            "Protect assets from customers",
            "Not losing personal items"],
            "Report damage/errors/near‑misses and help fix them"
        ),
    ])


def show_wh_module_conduct():
    section_header("Module 2: Conduct — Warehouse", "Ethics, honesty, respect", "⚖️")
    st.write(
        """
        Accuracy and honesty matter. Report counts, pick errors, and damaged product
        promptly. Treat coworkers and visitors with respect. Follow all safety rules.

        **Unacceptable** — Theft, falsifying counts/time, unauthorized equipment use,
        harassment, violence, impairment at work, unsafe shortcuts.
        """
    )
    st.markdown("### ✅ Checklist")
    checklist_block("wh_conduct", {
        "code_reviewed": "I’ve read the Code of Conduct.",
        "warehouse_honesty": "I will report counts/errors/damage honestly.",
        "unacceptable": "I understand unacceptable conduct (incl. unauthorized equipment).",
        "eeo": "I understand EEO.",
        "harassment": "I know how to report harassment (no retaliation).",
        "confidentiality": "I understand confidentiality.",
        "reporting": "I will report illegal/unethical behavior immediately.",
    })
    st.markdown("### 📝 Quick Quiz")
    quiz_block("wh_conduct", [
        ("AAP decisions are based on:", ["Seniority", "Merit, qualifications, and abilities", "Education only", "Manager discretion"], "Merit, qualifications, and abilities"),
        ("Operating a forklift without authorization is:", ["OK if supervised", "OK in emergency", "Unacceptable (discipline)", "Minor"], "Unacceptable (discipline)"),
        ("If you find damaged inventory:", ["Leave it", "Discard it", "Report and document immediately", "Report at end of shift"], "Report and document immediately"),
        ("Refusing to sign the NDA results in:", ["Warning", "HR meeting", "Immediate termination", "Probation"], "Immediate termination"),
    ])


def show_wh_module_safety():
    section_header("Module 3: Warehouse Policies & Safety", "PPE, attendance & equipment", "🦺")
    st.write(
        """
        **Attendance (no‑fault points)** and corrective actions mirror the general policy.  
        **Dress code** — Closed‑toe shoes/boots are required on the warehouse floor.  
        **PPE** — Gloves available; add any role‑specific PPE here.

        **Safety** — Report hazards immediately; keep aisles/exits clear; wear PPE; only
        operate equipment you’re trained and certified to use.
        """
    )
    if SHOW_PLACEHOLDERS:
        st.warning("PLACEHOLDER: Add shift schedules, additional PPE, and certification details before publishing.")

    st.markdown("### ✅ Checklist")
    checklist_block("wh_safety", {
        "point_system": "I understand the attendance point system.",
        "corrective_levels": "I know corrective steps (5: coaching · 6: verbal · 7: written · 8: termination).",
        "perfect_att": "I know point removal and $75 bonus rules.",
        "no_call": "I understand 2‑day no‑call/no‑show can be a resignation.",
        "closed_toe": "I know closed‑toe shoes are required on the floor.",
        "ppe_gloves": "I know gloves are available.",
        "safety_report": "I will report unsafe conditions/injuries immediately.",
        "equipment_cert": "I’ll operate only equipment I’m trained & certified to use.",
        "receiving": "I understand receiving: verify PO, inspect, document discrepancies.",
        "fifo": "I understand FIFO rotation & accurate picking.",
        "drug_policy": "I understand the drug & alcohol policy and accident testing.",
    })
    st.markdown("### 📝 Quick Quiz")
    quiz_block("wh_safety", [
        ("Footwear required on the floor:", ["Any athletic shoe", "Closed‑toe shoes/boots", "Steel‑toed only", "Any shoes"], "Closed‑toe shoes/boots"),
        ("Damage on inbound shipment:", [
            "Accept then report later",
            "Refuse to unload",
            "Note on receipt, photograph, notify supervisor",
            "Set aside for later"], "Note on receipt, photograph, notify supervisor"),
        ("Points for termination (12 mo):", ["6", "7", "8", "10"], "8"),
        ("FIFO means:", ["First In, First Out", "Fast Items, Fast Out", "Full Inventory, Full Order", "First Inspection, Final Output"], "First In, First Out"),
        ("Operate a forklift when:", ["Used one before", "Supervisor watching", "Trained, authorized & certified", "Emergency"], "Trained, authorized & certified"),
    ])


def show_wh_module_timeoff():
    section_header("Module 4: Time Off & Leave — Warehouse", "Requests, FMLA & life events", "⏰")
    st.write(
        """
        Pre‑approved vacation doesn’t add points. Use proper channels to report
        absences and request time off. LTSL requires 3+ days with physician mandate.
        FMLA as defined; life events within 30 days.
        """
    )
    st.markdown("### ✅ Checklist")
    checklist_block("wh_timeoff", {
        "vacation_points": "I know pre‑approved vacation is excluded from points.",
        "attendance_reporting": "I know the correct channels for reporting absences and requesting time off.",
        "ltsl_rules": "I understand when Long‑Term Sick Leave applies.",
        "fmla_requirements": "I know baseline FMLA requirements.",
        "life_event_deadline": "I know life‑event updates must be within 30 days.",
    })
    st.markdown("### 📝 Quick Quiz")
    quiz_block("wh_timeoff", [
        ("Pre‑approved vacation days are excluded from points.", ["True", "False"], "True"),
        ("LTSL requires:", ["1 day", "3+ consecutive physician‑mandated days", "5 days", "Verbal notice"], "3+ consecutive physician‑mandated days"),
        ("FMLA eligibility:", ["6 months", "12 months & 1,250 hours", "At hire", "Manager only"], "12 months & 1,250 hours"),
        ("Report life‑event changes within:", ["7", "14", "30", "90"], "30"),
    ])


def show_wh_module_benefits():
    section_header("Module 5: Benefits — Warehouse", "Health, retirement & support", "💼")
    st.write(
        """
        Health coverage: 1st of the month after 60 days (eligibility).  
        401(k): 100% match on first 3%.  
        Day‑one: Teladoc & LinkedIn Learning. EAP available 24/7.
        """
    )
    st.markdown("### ✅ Checklist")
    checklist_block("wh_benefits", {
        "effective_date": "I know when eligible health benefits begin.",
        "retirement_match": "I understand the 401(k) match.",
        "day1_resources": "I know Teladoc & LinkedIn Learning are day‑one resources.",
        "eap_support": "I know how to access the EAP.",
        "benefits_help": "I know who to contact for benefits questions.",
    })
    st.markdown("### 📝 Quick Quiz")
    quiz_block("wh_benefits", [
        ("When do eligible health benefits begin?", ["Day 1", "After 30 days", "1st of month after 60 days", "After 1 year"], "1st of month after 60 days"),
        ("401(k) match on first 3%:", ["50%", "75%", "100%", "No match"], "100%"),
        ("Day‑one resources:", ["Payroll only", "Teladoc & LinkedIn Learning", "Medical enrollment", "401(k) loan options"], "Teladoc & LinkedIn Learning"),
        ("Confidential wellbeing support:", ["BenefitHub", "LifeMatters EAP", "Payroll", "OSHA"], "LifeMatters EAP"),
    ])


def show_wh_module_firststeps():
    section_header("Module 6: Your First Steps — Warehouse", "Day 1, training & contacts", "🚀")
    st.write(
        f"""
        **Day 1** — Tour, paperwork, safety briefing, PPE issued, shadow a trainer.  
        **Do not operate equipment** until you’re trained and authorized.  
        **Paylocity** — Register (Company ID: **{PAYLOCITY_COMPANY_ID}**).  
        **BambooHR** — Get set up; add a profile photo.  
        **LinkedIn Learning** — Ask HR if you need the activation email.  
        **Teladoc** — Set up at Teladoc.com.
        """
    )

    st.markdown("### 👥 Key Contacts")
    for name, role, contact, phone in CONTACTS:
        line = f"**{name}** — {role} · {contact}"
        if phone:
            line += f" · {phone}"
        st.write("- " + line)

    st.markdown("### ✅ Checklist")
    checklist_block("wh_firststeps", {
        "paperwork": "I know what I’m signing during orientation.",
        "paylocity": f"I know how to register for Paylocity (Company ID: {PAYLOCITY_COMPANY_ID}).",
        "bamboohr": "I know what BambooHR is used for.",
        "teladoc_setup": "I know how to set up my Teladoc account.",
        "linkedin": "I have or can request my LinkedIn Learning activation.",
        "day1_floor": "I know what to expect on my first day on the floor.",
        "no_equip": "I won’t operate equipment until trained & authorized.",
        "key_contacts": "I know who to contact for HR, benefits, payroll, and safety.",
        "first90": "I know the 30/60/90‑day expectations.",
        "at_will": "I understand AAP is an at‑will employer.",
        "life_event": "I know life‑event benefit changes must be within 30 days.",
        "safety_report_reminder": "I’ll report safety concerns immediately.",
    })
    st.markdown("### 📝 Quick Quiz")
    quiz_block("wh_firststeps", [
        ("Paylocity Company ID?", ["123456", "123959", "987654", "112358"], "123959"),
        ("Notify HR of life events within:", ["7", "14", "30", "60"], "30"),
        ("When can you operate a forklift?", [
            "After first week",
            "Immediately if experienced",
            "Only after you’re trained & authorized for that equipment",
            "After 90‑day period"], "Only after you’re trained & authorized for that equipment"),
        ("Employment at AAP is:", ["Fixed term", "At‑will", "Union‑protected", "2‑year commitment"], "At‑will"),
    ])


# ─────────────────────────────────────────────
# Router & layout
# ─────────────────────────────────────────────

def render_module_shell_start(module_key: str):
    is_wh = st.session_state.get("role_track") == "warehouse"
    modules = WAREHOUSE_MODULES if is_wh else MODULES
    module = next((m for m in modules if m["key"] == module_key), None)
    if not module:
        return
    pct = st.session_state.progress.get(module_key, 0)
    status = "Complete" if pct == 100 else ("In Progress" if pct > 0 else "Queued")
    with st.container(border=True):
        st.markdown(f"### {module['icon']} Module {module['number']}: {module['title']}")
        st.caption(module["subtitle"]) 
        st.markdown(pct_bar(pct), unsafe_allow_html=True)
        st.caption(f"Status · {status}")


def render_module_shell_end():
    st.write("")


# Mapping
GENERAL_MAP = {
    "welcome": show_module_welcome,
    "conduct": show_module_conduct,
    "policies": show_module_policies,
    "timeoff": show_module_timeoff,
    "benefits": show_module_benefits,
    "firststeps": show_module_firststeps,
}
WAREHOUSE_MAP = {
    "wh_welcome": show_wh_module_welcome,
    "wh_conduct": show_wh_module_conduct,
    "wh_safety": show_wh_module_safety,
    "wh_timeoff": show_wh_module_timeoff,
    "wh_benefits": show_wh_module_benefits,
    "wh_firststeps": show_wh_module_firststeps,
}


# ─────────────────────────────────────────────
# Main app
# ─────────────────────────────────────────────
inject_ui_enhancements(st.session_state.get("sound_enabled", True))

if not st.session_state.authenticated:
    show_login()
else:
    with st.sidebar:
        render_sidebar()

    is_warehouse = st.session_state.get("role_track") == "warehouse"
    module_map = WAREHOUSE_MAP if is_warehouse else GENERAL_MAP

    selected = st.session_state.selected_module
    if selected and selected in module_map:
        render_module_shell_start(selected)
        module_map[selected]()
        render_module_shell_end()
    else:
        show_home()
