import base64
import os
from typing import Dict, List

import gspread
import streamlit as st

st.set_page_config(
    page_title="AAP Onboarding Studio",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)

MODULE_KEYS = ["welcome", "conduct", "attendance", "workplace", "benefits", "firststeps"]
MODULE_META = {
    "welcome": {
        "num": "01",
        "name": "Welcome to AAP",
        "desc": "Company history, mission, vision & guiding principles",
        "checklist_count": 4,
        "image": "https://images.unsplash.com/photo-1521791136064-7986c2920216?auto=format&fit=crop&w=1400&q=80",
    },
    "conduct": {
        "num": "02",
        "name": "Code of Conduct & Ethics",
        "desc": "Ethics, confidentiality & professional conduct standards",
        "checklist_count": 4,
        "image": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1400&q=80",
    },
    "attendance": {
        "num": "03",
        "name": "Attendance & PTO Policies",
        "desc": "PTO accruals, point system, holidays & leave policies",
        "checklist_count": 5,
        "image": "https://images.unsplash.com/photo-1506784365847-bbad939e9335?auto=format&fit=crop&w=1400&q=80",
    },
    "workplace": {
        "num": "04",
        "name": "Workplace Policies",
        "desc": "Safety, dress code, technology, harassment & conduct",
        "checklist_count": 5,
        "image": "https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&fit=crop&w=1400&q=80",
    },
    "benefits": {
        "num": "05",
        "name": "Benefits Overview",
        "desc": "Medical, dental, vision, 401(k) & supplemental coverage",
        "checklist_count": 5,
        "image": "https://images.unsplash.com/photo-1576086213369-97a306d36557?auto=format&fit=crop&w=1400&q=80",
    },
    "firststeps": {
        "num": "06",
        "name": "First Steps",
        "desc": "System access, onboarding checklist & 90-day roadmap",
        "checklist_count": 6,
        "image": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1400&q=80",
    },
}

SESSION_DEFAULTS = {
    "logged_in": False,
    "emp_name": "",
    "emp_number": "",
    "emp_department": "",
    "emp_position": "",
    "emp_start_date": "",
    "emp_track": "general",
    "current_page": "home",
    "current_module": None,
    "sound_armed": False,
}


def init_state() -> None:
    for key, value in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value

    for module_key in MODULE_KEYS:
        quiz_key = f"quiz_{module_key}_passed"
        checklist_key = f"checklist_{module_key}"
        if quiz_key not in st.session_state:
            st.session_state[quiz_key] = False
        if checklist_key not in st.session_state:
            st.session_state[checklist_key] = {}


def logo_b64() -> str | None:
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AAP_API.PNG")
    if not os.path.exists(img_path):
        return None
    with open(img_path, "rb") as handle:
        return base64.b64encode(handle.read()).decode("utf-8")


def h(html: str) -> None:
    st.markdown(html, unsafe_allow_html=True)


def completion_score() -> tuple[int, int]:
    done, total = 0, 0
    for key in MODULE_KEYS:
        total += 1
        done += int(st.session_state.get(f"quiz_{key}_passed", False))
        total += MODULE_META[key]["checklist_count"]
        done += sum(st.session_state.get(f"checklist_{key}", {}).values())
    return done, total


def module_complete(module_key: str) -> bool:
    checklist_done = sum(st.session_state.get(f"checklist_{module_key}", {}).values())
    checklist_needed = MODULE_META[module_key]["checklist_count"]
    return st.session_state.get(f"quiz_{module_key}_passed", False) and checklist_done >= checklist_needed


def gsheet_client():
    try:
        creds = dict(st.secrets["gcp_service_account"])
    except Exception:
        return None

    try:
        return gspread.service_account_from_dict(
            creds,
            scopes=[
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive",
            ],
        )
    except Exception:
        return None


def validate_login(access_code: str, employee_id: str, full_name: str) -> bool:
    try:
        secret_code = st.secrets["orientation_access_code"]
    except Exception:
        st.error("Access code not configured.")
        return False

    if access_code.strip() != secret_code.strip():
        st.error("Incorrect access code.")
        return False

    client = gsheet_client()
    if not client:
        st.error("Cannot connect to Google Sheets.")
        return False

    try:
        worksheet = client.open("AAP New Hire Orientation Progress").worksheet("Employee Roster")
        records = worksheet.get_all_records()
    except Exception:
        st.error("Cannot open Employee Roster tab.")
        return False

    for row in records:
        if str(row.get("Employee ID", "")).strip().lower() != employee_id.strip().lower():
            continue

        if str(row.get("Full Name", "")).strip().lower() != full_name.strip().lower():
            st.error("Name does not match.")
            return False

        st.session_state["emp_track"] = (
            "warehouse"
            if str(row.get("Track", "")).strip().lower() == "warehouse"
            else "general"
        )
        st.session_state["emp_department"] = str(row.get("Department", ""))
        st.session_state["emp_position"] = str(row.get("Position", ""))
        st.session_state["emp_start_date"] = str(row.get("Start Date", ""))
        return True

    st.error("Employee ID not found.")
    return False


def inject_styles() -> None:
    h(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

        :root {
            --bg: #05070f;
            --surface: #0c1020;
            --surface-soft: #11162a;
            --line: rgba(255, 255, 255, 0.1);
            --text: #f6f7ff;
            --muted: #a7aec7;
            --accent: #5f7cff;
            --accent-2: #10d1bf;
            --good: #1dc48d;
            --warn: #f7b731;
            --bad: #ff5c7c;
            --shadow: 0 20px 55px rgba(0, 0, 0, 0.35);
        }

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, sans-serif !important;
        }

        .stApp {
            background:
                radial-gradient(circle at 10% 5%, rgba(95,124,255,.26), transparent 32%),
                radial-gradient(circle at 90% 2%, rgba(16,209,191,.18), transparent 32%),
                var(--bg);
            color: var(--text);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #090d1b 0%, #080a15 100%);
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        [data-testid="stSidebar"] * {
            color: var(--text);
        }

        .glass {
            background: linear-gradient(160deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
            border: 1px solid var(--line);
            border-radius: 20px;
            box-shadow: var(--shadow);
            backdrop-filter: blur(12px);
        }

        .hero {
            position: relative;
            overflow: hidden;
            padding: 34px;
            margin-bottom: 1.2rem;
            animation: rise .6s ease;
        }

        .hero::after {
            content: '';
            position: absolute;
            inset: -30% -10% auto auto;
            width: 340px;
            height: 340px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(95,124,255,.55), rgba(95,124,255,0));
            filter: blur(6px);
            animation: pulse 6s ease-in-out infinite;
        }

        .kicker { letter-spacing: .16em; text-transform: uppercase; font-size: .66rem; color: var(--muted); }
        .hero h1 { margin: .35rem 0 .5rem 0; font-size: clamp(1.8rem, 4vw, 2.8rem); color: white; }
        .hero p { margin: 0; color: #d8dcf3; max-width: 760px; line-height: 1.7; }

        .metric {
            padding: 18px 20px;
            border-radius: 16px;
            border: 1px solid var(--line);
            background: linear-gradient(140deg, rgba(255,255,255,.08), rgba(255,255,255,.02));
        }
        .metric .n { font-size: 2rem; font-weight: 800; color: white; }
        .metric .l { text-transform: uppercase; letter-spacing: .13em; font-size: .64rem; color: var(--muted); }

        .module-card {
            border-radius: 18px;
            border: 1px solid var(--line);
            overflow: hidden;
            margin-bottom: .8rem;
            background: var(--surface);
            transition: transform .22s ease, box-shadow .22s ease;
            box-shadow: 0 8px 24px rgba(0,0,0,.26);
        }
        .module-card:hover { transform: translateY(-3px); box-shadow: 0 18px 40px rgba(0,0,0,.4); }
        .module-cover { height: 130px; background-size: cover; background-position: center; filter: contrast(1.15) saturate(1.12); }
        .module-body { padding: 18px; }
        .tag { font-size: .62rem; letter-spacing: .13em; text-transform: uppercase; color: var(--muted); }
        .module-title { margin: .35rem 0; color: #fff; font-size: 1rem; font-weight: 700; }
        .module-desc { color: #c2c8e4; margin: 0; font-size: .88rem; line-height: 1.55; }
        .pill { margin-top: .75rem; display: inline-block; font-size: .66rem; text-transform: uppercase; letter-spacing: .1em; padding: 4px 12px; border-radius: 999px; }
        .pill.todo { background: rgba(255,255,255,.08); color: #cfd5ee; }
        .pill.wip { background: rgba(247,183,49,.18); color: #ffc75f; }
        .pill.done { background: rgba(29,196,141,.2); color: #7cf3c8; }

        .content-section {
            padding: 24px;
            margin: 12px 0;
            border-radius: 18px;
            border: 1px solid var(--line);
            background: linear-gradient(170deg, rgba(255,255,255,.07), rgba(255,255,255,.02));
        }
        .content-section h2, .content-section h3, .content-section h4 { color: #fff; }
        .content-section p, .content-section li { color: #d7dbf1; line-height: 1.7; }
        .content-section strong { color: #fff; }

        .module-hero {
            height: 220px;
            border-radius: 20px;
            position: relative;
            overflow: hidden;
            background-size: cover;
            background-position: center;
            margin-bottom: 1rem;
            border: 1px solid var(--line);
            animation: rise .5s ease;
        }
        .module-hero::before {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(180deg, rgba(3,6,14,.18), rgba(3,6,14,.86));
        }
        .module-hero .inner { position: absolute; inset: auto 24px 22px 24px; }
        .module-hero h2 { color: white; margin: 0; }
        .module-hero p { color: #d8dcf4; margin: .35rem 0 0 0; }

        .subtle-note {
            border-left: 3px solid var(--accent-2);
            padding: 12px 14px;
            background: rgba(16,209,191,.12);
            border-radius: 0 10px 10px 0;
            color: #d8fff8;
            margin: 10px 0;
        }

        .quiz-pass, .quiz-fail {
            padding: 14px;
            border-radius: 12px;
            font-weight: 600;
            margin-top: .6rem;
        }
        .quiz-pass { background: rgba(29,196,141,.17); border: 1px solid rgba(29,196,141,.4); color: #8af0cb; }
        .quiz-fail { background: rgba(255,92,124,.17); border: 1px solid rgba(255,92,124,.4); color: #ffc6d3; }

        [data-testid="stBaseButton-primary"], div[data-testid="stFormSubmitButton"] button {
            border-radius: 12px !important;
            border: 0 !important;
            color: white !important;
            font-weight: 700 !important;
            background: linear-gradient(90deg, var(--accent), #7b92ff) !important;
            box-shadow: 0 6px 22px rgba(95,124,255,.35) !important;
        }

        [data-testid="stBaseButton-secondary"] {
            border-radius: 12px !important;
            border: 1px solid var(--line) !important;
            color: #ebeeff !important;
            background: rgba(255,255,255,.03) !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            background: rgba(255,255,255,.03);
            border: 1px solid var(--line);
            border-radius: 12px;
            padding: 4px;
            gap: 4px;
        }

        .stTabs [aria-selected="true"] {
            background: rgba(95,124,255,.22) !important;
            border-radius: 10px !important;
            color: white !important;
        }

        @keyframes rise {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes pulse {
            0%,100% { transform: scale(1); opacity: .85; }
            50% { transform: scale(1.13); opacity: 1; }
        }
        </style>
        """
    )


def add_soft_sound(trigger_key: str) -> None:
    if st.session_state.get("sound_armed") == trigger_key:
        return

    wav_b64 = (
        "UklGRlQAAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YTAAAAAAAP8AAP8AAP8AAP8A"
        "AP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8="
    )
    h(
        f"""
        <audio autoplay style="display:none">
          <source src="data:audio/wav;base64,{wav_b64}" type="audio/wav">
        </audio>
        """
    )
    st.session_state["sound_armed"] = trigger_key


def show_login() -> None:
    h("<div style='height:5vh'></div>")
    _, center, _ = st.columns([1, 1.2, 1])
    with center:
        logo = logo_b64()
        if logo:
            h(
                f"<div style='text-align:center;margin-bottom:18px'><img src='data:image/png;base64,{logo}' style='height:72px;filter:drop-shadow(0 10px 24px rgba(0,0,0,.34));'></div>"
            )

        h("<div class='glass' style='padding:30px'>")
        st.markdown("### Welcome to the AAP Onboarding Experience")
        st.caption("Use your HR-provided credentials to continue.")

        with st.form("login"):
            access_code = st.text_input("Access Code", type="password", placeholder="Enter access code")
            employee_id = st.text_input("Employee ID", placeholder="e.g. 10042")
            full_name = st.text_input("Full Name", placeholder="As shown in HR paperwork")
            submit = st.form_submit_button("Enter Onboarding Portal", use_container_width=True)

        h("</div>")
        h(
            "<p style='text-align:center;color:#c2c8e4;font-size:.82rem;margin-top:12px'>"
            "Need help? Nicole Thornton · nicole.thornton@apirx.com · 256-574-7528"
            "</p>"
        )

        if submit:
            if not access_code or not employee_id or not full_name:
                st.error("All fields are required.")
                return
            with st.spinner("Verifying credentials..."):
                if validate_login(access_code, employee_id, full_name):
                    st.session_state["logged_in"] = True
                    st.session_state["emp_name"] = full_name.strip().title()
                    st.session_state["emp_number"] = employee_id.strip()
                    st.rerun()


def show_sidebar() -> None:
    with st.sidebar:
        logo = logo_b64()
        if logo:
            h(
                f"<div style='text-align:center;margin:8px 0 14px'><img src='data:image/png;base64,{logo}' style='height:48px;opacity:.95'></div>"
            )

        done, total = completion_score()
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

        st.markdown("---")
        for key in MODULE_KEYS:
            suffix = " ✓" if module_complete(key) else ""
            if st.button(
                f"{MODULE_META[key]['num']}  {MODULE_META[key]['name']}{suffix}",
                key=f"nav_{key}",
                use_container_width=True,
            ):
                st.session_state["current_page"] = "module"
                st.session_state["current_module"] = key
                st.rerun()

        st.markdown("---")
        st.caption("HR Support")
        st.caption("Nicole Thornton · 256-574-7528")
        st.caption("nicole.thornton@apirx.com")

        if st.button("Sign Out", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


def show_home() -> None:
    first = st.session_state["emp_name"].split()[0] if st.session_state["emp_name"] else "there"
    done, total = completion_score()
    pct = int((done / total) * 100) if total else 0
    complete_modules = sum(module_complete(k) for k in MODULE_KEYS)

    h(
        f"""
        <div class="glass hero">
            <div class="kicker">New Hire Orientation · AAP</div>
            <h1>Welcome, {first}</h1>
            <p>Move through each module, pass every assessment, and confirm each checklist item. Progress is saved automatically.</p>
        </div>
        """
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        h(f"<div class='metric'><div class='n'>{pct}%</div><div class='l'>overall progress</div></div>")
    with c2:
        h(f"<div class='metric'><div class='n'>{complete_modules}/{len(MODULE_KEYS)}</div><div class='l'>modules complete</div></div>")
    with c3:
        h(f"<div class='metric'><div class='n'>{done}/{total}</div><div class='l'>items completed</div></div>")

    st.markdown("### Modules")
    columns = st.columns(2)
    for idx, key in enumerate(MODULE_KEYS):
        quiz_done = st.session_state.get(f"quiz_{key}_passed", False)
        checklist_done = sum(st.session_state.get(f"checklist_{key}", {}).values())
        if module_complete(key):
            label, cls = "Complete", "done"
        elif quiz_done or checklist_done:
            label, cls = "In Progress", "wip"
        else:
            label, cls = "Not Started", "todo"

        with columns[idx % 2]:
            meta = MODULE_META[key]
            h(
                f"""
                <div class="module-card">
                    <div class="module-cover" style="background-image:url('{meta['image']}')"></div>
                    <div class="module-body">
                        <div class="tag">Module {meta['num']}</div>
                        <div class="module-title">{meta['name']}</div>
                        <p class="module-desc">{meta['desc']}</p>
                        <span class="pill {cls}">{label}</span>
                    </div>
                </div>
                """
            )
            if st.button("Open Module", key=f"open_{key}", use_container_width=True):
                add_soft_sound(f"open_{key}")
                st.session_state["current_page"] = "module"
                st.session_state["current_module"] = key
                st.rerun()


def render_quiz(module_key: str, questions: List[Dict]) -> None:
    st.markdown("---")
    st.markdown("### Module Assessment")

    if st.session_state.get(f"quiz_{module_key}_passed"):
        h("<div class='quiz-pass'>✓ Assessment complete — all answers correct.</div>")
        return

    st.caption("Answer all questions correctly to pass. You can retry.")
    answers = {}
    for idx, question in enumerate(questions):
        answers[idx] = st.radio(
            f"**Q{idx + 1}.** {question['q']}",
            options=question["options"],
            index=None,
            key=f"quiz_{module_key}_{idx}",
        )

    if st.button("Submit Answers", key=f"submit_{module_key}", type="primary"):
        correct = sum(
            answers[i] == q["options"][q["answer"]] for i, q in enumerate(questions)
        )
        if correct == len(questions):
            st.session_state[f"quiz_{module_key}_passed"] = True
            add_soft_sound(f"pass_{module_key}")
            h("<div class='quiz-pass'>✓ All answers are correct.</div>")
            st.rerun()
        else:
            h(
                f"<div class='quiz-fail'>{correct} of {len(questions)} correct — please review and retry.</div>"
            )


def render_checklist(module_key: str, items: List[str]) -> None:
    st.markdown("---")
    st.markdown("### Confirmation Checklist")
    checklist = st.session_state.get(f"checklist_{module_key}", {})

    for idx, item in enumerate(items):
        checkbox_key = f"check_{module_key}_{idx}"
        checklist[checkbox_key] = st.checkbox(item, value=checklist.get(checkbox_key, False), key=checkbox_key)

    st.session_state[f"checklist_{module_key}"] = checklist
    done = sum(checklist.values())
    st.caption(f"{done} of {len(items)} confirmed")


def module_header(module_key: str, subtitle: str) -> None:
    meta = MODULE_META[module_key]
    h(
        f"""
        <div class="module-hero" style="background-image:url('{meta['image']}')">
            <div class="inner">
                <div class="tag">Module {meta['num']}</div>
                <h2>{meta['name']}</h2>
                <p>{subtitle}</p>
            </div>
        </div>
        """
    )


def module_welcome() -> None:
    module_header("welcome", "Learn about our history, mission, vision, and the values that guide everything we do.")
    h("<div class='content-section'>")
    st.markdown("## Who We Are")
    st.markdown(
        """
American Associated Pharmacies (AAP) is a national cooperative of more than **2,000 independent pharmacies**.
Founded in 2009 when **United Drugs** (Phoenix, AZ) and **Associated Pharmacies, Inc. (API)** (Scottsboro, AL)
merged to form one of the largest independent pharmacy organizations in America.

Today, AAP operates API with two U.S. warehouse locations, providing member-focused support,
innovative programs, and significant cost savings through its Prime Vendor Agreement.
        """
    )
    h("<div class='subtle-note'><strong>Did you know?</strong> AAP saves its member pharmacies millions in operating and acquisition costs every year through its competitive Prime Vendor Agreement.</div>")
    st.markdown("## Our Mission")
    st.markdown("AAP provides support and customized solutions for independent community pharmacies to enhance their profitability, streamline their operations, and improve the quality of patient care.")
    st.markdown("## Our Vision")
    st.markdown("*Helping independent pharmacies thrive in a competitive healthcare market.*")
    st.markdown("## Our Core Values")
    for icon, title, desc in [
        ("🎯", "Customer Focus", "Our primary focus is meeting and exceeding customer expectations. Customer service is not just a department — it's an attitude."),
        ("⚖️", "Integrity", "We act with honesty without compromising truth. We build trust through consistency in our words and actions."),
        ("🤝", "Respect", "We treat others with dignity, recognize the power of teamwork, and encourage open, honest communication."),
        ("⭐", "Excellence", "We strive for the highest quality in everything we do and pursue continuous improvement and innovation."),
        ("🔑", "Ownership", "We seek responsibility, hold ourselves accountable, and take ownership when things go wrong."),
    ]:
        st.markdown(f"- **{icon} {title}:** {desc}")
    h("</div>")

    render_quiz(
        "welcome",
        [
            {"q": "When was AAP formed?", "options": ["2001", "2005", "2009", "2012"], "answer": 2},
            {"q": "AAP is a cooperative of approximately how many pharmacies?", "options": ["500", "1,000", "2,000", "5,000"], "answer": 2},
            {"q": "Which is NOT one of AAP's five core values?", "options": ["Customer Focus", "Integrity", "Profitability", "Ownership"], "answer": 2},
            {"q": "What is AAP's vision statement?", "options": ["To be the largest pharmacy chain", "Helping independent pharmacies thrive in a competitive healthcare market", "Maximizing shareholder value", "Providing the lowest drug prices"], "answer": 1},
        ],
    )
    render_checklist(
        "welcome",
        [
            "I understand AAP's history and formation.",
            "I can identify the mission and vision statements.",
            "I know the five core values and what they mean.",
            "I understand that AAP is a cooperative serving independent pharmacies.",
        ],
    )


def module_conduct() -> None:
    module_header("conduct", "Professional standards, ethical behavior, and workplace expectations.")
    h("<div class='content-section'>")
    st.markdown("## Business Ethics & Conduct")
    st.markdown("The success of AAP depends on our customers' trust. Every employee must act with honesty and integrity, comply with all applicable laws, and refrain from any illegal, dishonest, or unethical conduct. Failure to comply leads to disciplinary action, up to and including termination.")
    st.markdown("## Key Policies")
    tab1, tab2, tab3, tab4 = st.tabs(["Conflicts of Interest", "Confidentiality", "Outside Employment", "Equal Opportunity"])
    with tab1:
        st.markdown("Employees must avoid actual or potential conflicts of interest in all business dealings. Contact HR with any questions.")
    with tab2:
        st.markdown("All employees sign a **confidentiality and non-disclosure agreement** upon hire. Refusal is grounds for immediate termination. Personnel files are company property with restricted access. Electronic systems may be monitored.")
    with tab3:
        st.markdown("Outside employment is permitted as long as you satisfactorily perform your AAP responsibilities. If outside work creates a conflict or interferes with performance, you may be asked to choose.")
    with tab4:
        st.markdown("All employment decisions are based on merit, qualifications, and abilities. AAP does not discriminate on the basis of race, color, religion, sex, national origin, age, disability, or any other protected characteristic. Report concerns without fear of reprisal.")
    st.markdown("## Problem Resolution Process")
    st.markdown("1. Present concerns to your **immediate supervisor** (or HR if inappropriate)\n2. If unresolved, escalate: **VP → President → CEO**\n3. CEO has full authority to resolve\n4. Board of Directors review available as final step\n\nNo employee will be penalized for voicing a complaint in a reasonable, professional manner.")
    h("</div>")

    render_quiz(
        "conduct",
        [
            {"q": "What must all employees sign upon hire?", "options": ["Non-compete agreement", "Confidentiality and non-disclosure agreement", "Social media policy", "Union membership form"], "answer": 1},
            {"q": "What system does AAP use to verify work authorization?", "options": ["HIPAA", "E-Verify", "ADP Screening", "LinkedIn"], "answer": 1},
            {"q": "Who should you approach first with a workplace concern?", "options": ["CEO", "A coworker", "Your immediate supervisor or HR", "An attorney"], "answer": 2},
            {"q": "Outside employment is allowed as long as:", "options": ["You work under 20 hours elsewhere", "You satisfactorily perform your AAP responsibilities", "Your manager gives verbal approval", "It is in a different industry"], "answer": 1},
        ],
    )
    render_checklist(
        "conduct",
        [
            "I understand AAP's ethics expectations and my responsibility.",
            "I understand the confidentiality and NDA requirements.",
            "I know the problem resolution steps for workplace concerns.",
            "I understand the equal employment opportunity policy.",
        ],
    )


def module_attendance() -> None:
    module_header("attendance", "Vacation accruals, personal leave, holidays, and the attendance point system.")
    h("<div class='content-section'>")
    st.markdown("## Vacation Benefits")
    st.caption("Regular full-time employees · 60-day waiting period · Minimum increment: 2 hours")
    st.table(
        [
            ["60 days – 1st Anniversary", "3 days (24 hrs)", "0.46 hrs/week"],
            ["1st – 2nd Anniversary", "5 days (40 hrs)", "0.77 hrs/week"],
            ["2nd – 3rd Anniversary", "7 days (56 hrs)", "1.07 hrs/week"],
            ["3rd – 5th Anniversary", "10 days (80 hrs)", "1.54 hrs/week"],
            ["5th – 9th Anniversary", "15 days (120 hrs)", "2.31 hrs/week"],
            ["10th – 19th Anniversary", "17 days (136 hrs)", "2.62 hrs/week"],
            ["20th Anniversary+", "19 days (152 hrs)", "2.93 hrs/week"],
        ]
    )
    st.markdown("Vacation cannot be taken before accrual. 5+ consecutive days require President approval. Employees may bank up to 19 days (152 hours). Accrued vacation is paid out at termination.")
    st.markdown("## Personal Leave")
    st.markdown("**Full-time employees:** 3 personal days (24 hrs) initially → 4 days after 1 year → 5 days after 5 years.\n\n**Part-time employees:** Earn 1 hour per 30 hours worked, with the same tier caps.\n\nUnused personal leave is **forfeited** at end of benefit year (unless state law requires carryover). Personal leave is **not paid out** at termination.")
    st.markdown("## Company Holidays")
    st.markdown("New Year's Day · Memorial Day · Independence Day · Labor Day · Thanksgiving · Day after Thanksgiving (or floating) · Christmas Eve (or floating) · Christmas Day")
    st.markdown("Saturday holidays are observed on Friday. Sunday holidays are observed on Monday. Employees who work on a holiday receive a floating holiday to use within 90 days.")
    st.markdown("## Attendance Point System")
    st.markdown("- Tardy up to 5 minutes: **0 points**\n- Tardy or early leave under 4 hours: **½ point**\n- Full shift absence/tardy/early leave 4+ hours: **1 point**\n- No-call absence (15+ minutes after start): **1½ points**")
    st.markdown("**Corrective Action Thresholds:** 5 points coaching · 6 verbal warning · 7 written warning · 8 termination.")
    st.warning("Two consecutive days absent without reporting in is considered voluntary resignation.")
    h("</div>")

    render_quiz(
        "attendance",
        [
            {"q": "What is the minimum increment for vacation time?", "options": ["1 hour", "2 hours", "4 hours", "8 hours"], "answer": 1},
            {"q": "What is the minimum increment for personal leave?", "options": ["1 hour", "2 hours", "4 hours", "8 hours"], "answer": 0},
            {"q": "How many points does a no-call absence carry?", "options": ["½ point", "1 point", "1½ points", "2 points"], "answer": 2},
            {"q": "At how many points does termination occur?", "options": ["6", "7", "8", "10"], "answer": 2},
            {"q": "Consecutive no-call days that equals resignation?", "options": ["1", "2", "3", "5"], "answer": 1},
        ],
    )
    render_checklist(
        "attendance",
        [
            "I understand the vacation accrual schedule and 2-hour minimum.",
            "I understand personal leave uses 1-hour increments and forfeits at year-end.",
            "I know the 8 company holidays and floating holiday rules.",
            "I understand the attendance point system and corrective action thresholds.",
            "I understand that 2 consecutive no-call days is considered voluntary resignation.",
        ],
    )


def module_workplace() -> None:
    module_header("workplace", "Safety, dress code, technology, harassment prevention, and conduct expectations.")
    h("<div class='content-section'>")
    tabs = st.tabs(["Dress Code", "Safety", "Drug & Alcohol", "Computer & Email", "Harassment", "Other Policies"])
    with tabs[0]:
        st.markdown("A neat, clean, and well-groomed appearance is required. Clothing must be work-appropriate, non-offensive, and not strongly scented. Non-compliance may mean being sent home to change while clocked out.")
    with tabs[1]:
        st.markdown("Immediately report unsafe conditions and all work-related injuries to HR. All work-related accidents require immediate drug and alcohol testing.")
    with tabs[2]:
        st.markdown("AAP maintains a zero-tolerance drug and alcohol-free workplace. Random drug testing may occur at any time. Violations can result in immediate termination.")
    with tabs[3]:
        st.markdown("All computers, files, email, and software are AAP property, for business use, and may be monitored. Offensive or illegal content is prohibited.")
    with tabs[4]:
        st.markdown("Zero tolerance for discrimination and unlawful harassment. Report issues to your supervisor or HR, and no retaliation is allowed for good-faith complaints.")
    with tabs[5]:
        st.markdown("Overtime requires prior supervisor approval. Workplace violence is zero tolerance and must be reported within 24 hours. Business travel expenses are reimbursable when legitimate.")
    h("</div>")

    render_quiz(
        "workplace",
        [
            {"q": "What happens after a work-related accident?", "options": ["Nothing unless serious", "Incident report only", "Immediate drug and alcohol testing", "Employee goes home"], "answer": 2},
            {"q": "AAP's computer systems are:", "options": ["Personal property", "Company property, may be monitored", "Free for personal use", "Monitored only in investigations"], "answer": 1},
            {"q": "If harassed, what should you do first?", "options": ["Post online", "Ignore it", "Tell offender to stop or report to HR", "Confront publicly"], "answer": 2},
            {"q": "Overtime requires:", "options": ["Coworker approval", "Prior supervisor approval", "After-the-fact report", "Self-authorization"], "answer": 1},
        ],
    )
    render_checklist(
        "workplace",
        [
            "I understand dress code expectations.",
            "I understand safety reporting requirements.",
            "I understand the drug and alcohol policy.",
            "I understand computer/email monitoring.",
            "I know how to report harassment.",
        ],
    )


def module_benefits() -> None:
    module_header("benefits", "Medical, dental, vision, retirement, and supplemental coverage options.")
    h("<div class='content-section'>")
    st.markdown("Full-time employees (30+ hrs/week) must enroll within 30 days. Benefits are effective the 1st of the month after 60 days. Dependents can be covered to age 26.")
    full_time, all_staff = st.tabs(["Full-Time Benefits", "Benefits for All Employees"])
    with full_time:
        st.markdown("### Medical Insurance — BCBS Alabama")
        st.markdown("**PPO Plan:** Employee $157.20/mo · Family $678.62/mo · Deductible $500/$1,000 · Coinsurance 20% · OOP max $2,250/$4,500.")
        st.markdown("**HDHP with HSA:** Employee $136.34/mo · Family $581.72/mo · Deductible $1,700/$3,400 · Coinsurance 10% · OOP max $3,400/$6,800 · Company HSA $900/$1,800 yearly.")
        st.markdown("Dental (Guardian), Vision (Guardian/Davis Vision), Basic Life/AD&D (no cost), LTD (company-paid), STD (employee-paid), supplemental options, and 401(k) with a 4% maximum match on 5% contribution are available.")
    with all_staff:
        st.markdown("Teladoc, LifeMatters EAP, LinkedIn Learning, BenefitHub perks, and personal time off are available to all employees.")
    h("</div>")

    render_quiz(
        "benefits",
        [
            {"q": "When do full-time benefits become effective?", "options": ["Day 1", "After 30 days", "1st of month after 60 days", "After 90 days"], "answer": 2},
            {"q": "401(k) match if you contribute 5%?", "options": ["2%", "3%", "4%", "5%"], "answer": 2},
            {"q": "Which benefit is free for ALL employees?", "options": ["Dental", "Short-term disability", "Teladoc", "Vision"], "answer": 2},
            {"q": "Basic Life/AD&D is provided at:", "options": ["50% employer-paid", "No cost to employee", "Employee-paid", "Enrollment required"], "answer": 1},
        ],
    )
    render_checklist(
        "benefits",
        [
            "I understand the two medical plans.",
            "I know the 401(k) match.",
            "I know which benefits are free for everyone.",
            "I know enrollment is within 30 days.",
            "I understand supplemental options.",
        ],
    )


def module_firststeps() -> None:
    module_header("firststeps", "Your action items, system access setup, and 90-day onboarding roadmap.")
    h("<div class='content-section'>")
    st.markdown("## Immediate Action Items")
    st.markdown("- Verify account access\n- Sign all new hire documents in BambooHR\n- Activate LinkedIn Learning\n- Provide I-9 documents within 3 business days\n- Register for Paylocity\n- Download BambooHR app")
    st.markdown("## Your 90-Day Roadmap")
    st.markdown("**Days 1–30:** complete orientation, paperwork, system access, and team onboarding.\n\n**Days 31–60:** build independence, complete 60-day survey, and complete probation period.\n\n**Days 61–90:** increase consistency, identify improvements, complete first performance review, and reach full benefits eligibility.")
    h("</div>")

    render_quiz(
        "firststeps",
        [
            {"q": "I-9 documents must be provided within?", "options": ["1 day", "3 business days", "5 days", "10 days"], "answer": 1},
            {"q": "Probationary period ends at?", "options": ["30 days", "60 days", "90 days", "120 days"], "answer": 1},
            {"q": "PTO eligibility begins after?", "options": ["Day 1", "30 days", "60 days", "90 days"], "answer": 2},
            {"q": "Which app for your employee profile?", "options": ["Workday", "BambooHR", "ADP", "Gusto"], "answer": 1},
        ],
    )
    render_checklist(
        "firststeps",
        [
            "I will verify access and sign all documents.",
            "I will activate LinkedIn Learning.",
            "I will provide I-9 within 3 business days.",
            "I will register for Paylocity and download BambooHR.",
            "I understand the 90-day timeline.",
            "I know who to contact in HR.",
        ],
    )


MODULE_VIEW = {
    "welcome": module_welcome,
    "conduct": module_conduct,
    "attendance": module_attendance,
    "workplace": module_workplace,
    "benefits": module_benefits,
    "firststeps": module_firststeps,
}


def show_module(module_key: str) -> None:
    left, right = st.columns([1, 4])
    with left:
        if st.button("← Dashboard", use_container_width=True):
            st.session_state["current_page"] = "home"
            st.session_state["current_module"] = None
            st.rerun()

    MODULE_VIEW[module_key]()

    st.markdown("---")
    index = MODULE_KEYS.index(module_key)
    prev_col, next_col = st.columns(2)

    if index > 0:
        prev_key = MODULE_KEYS[index - 1]
        with prev_col:
            if st.button(f"← {MODULE_META[prev_key]['name']}", use_container_width=True):
                st.session_state["current_module"] = prev_key
                st.rerun()

    if index < len(MODULE_KEYS) - 1:
        next_key = MODULE_KEYS[index + 1]
        with next_col:
            if st.button(f"{MODULE_META[next_key]['name']} →", use_container_width=True):
                st.session_state["current_module"] = next_key
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
