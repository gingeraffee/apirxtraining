import streamlit as st
import json
import os
import base64
import gspread

st.set_page_config(
    page_title="AAP Employee Onboarding Portal",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

MODULE_KEYS = ["welcome", "conduct", "attendance", "workplace", "benefits", "firststeps"]
MODULE_NAMES = {
    "welcome": "Welcome to AAP",
    "conduct": "Code of Conduct & Ethics",
    "attendance": "Attendance & PTO Policies",
    "workplace": "Workplace Policies",
    "benefits": "Benefits Overview",
    "firststeps": "First Steps",
}
MODULE_ICONS = {
    "welcome": "🏢", "conduct": "📋", "attendance": "⏰",
    "workplace": "🏗️", "benefits": "🩺", "firststeps": "🚀",
}
MODULE_DESCRIPTIONS = {
    "welcome": "Company history, mission, vision & guiding principles.",
    "conduct": "Ethical behavior, confidentiality & professional standards.",
    "attendance": "PTO policies, point system, vacation & personal leave accruals.",
    "workplace": "Dress code, safety, drug policy, technology use & harassment prevention.",
    "benefits": "Health, dental, vision, 401(k), and supplemental benefits.",
    "firststeps": "Action items, system access & your 90-day roadmap.",
}
CHECKLIST_COUNTS = {"welcome": 4, "conduct": 4, "attendance": 5, "workplace": 5, "benefits": 5, "firststeps": 6}

_defaults = {"logged_in": False, "emp_name": "", "emp_number": "", "emp_department": "", "emp_position": "", "emp_start_date": "", "current_page": "home", "current_module": None}
for _k, _v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v
for _mk in MODULE_KEYS:
    if f"quiz_{_mk}_passed" not in st.session_state:
        st.session_state[f"quiz_{_mk}_passed"] = False
    if f"checklist_{_mk}" not in st.session_state:
        st.session_state[f"checklist_{_mk}"] = {}

def _logo_b64():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AAP_API.PNG")
    if os.path.exists(p):
        with open(p, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def html(text):
    st.markdown(text, unsafe_allow_html=True)

def calc_progress():
    done = total = 0
    for mk in MODULE_KEYS:
        total += 1
        if st.session_state.get(f"quiz_{mk}_passed"):
            done += 1
        ct = CHECKLIST_COUNTS[mk]
        total += ct
        done += sum(1 for v in st.session_state.get(f"checklist_{mk}", {}).values() if v)
    return done, total

def is_module_complete(mk):
    passed = st.session_state.get(f"quiz_{mk}_passed", False)
    checks = st.session_state.get(f"checklist_{mk}", {})
    return passed and sum(1 for v in checks.values() if v) >= CHECKLIST_COUNTS[mk]

def get_gsheet_client():
    """Connect to Google Sheets using gcp_service_account secret."""
    try:
        import gspread
        creds_dict = dict(st.secrets["gcp_service_account"])
        scopes = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        return gspread.service_account_from_dict(creds_dict, scopes=scopes)
    except Exception:
        return None

def validate_login(access_code, employee_id, full_name):
    """
    Validates login using:
    1. Access code checked against st.secrets["orientation_access_code"]
    2. Employee ID + Full Name checked against 'Employee Roster' tab
    """
    # Step 1: Check access code
    try:
        correct_code = st.secrets["orientation_access_code"]
    except Exception:
        st.error("Access code not configured in Streamlit secrets.")
        return False

    if access_code.strip() != correct_code.strip():
        st.error("Incorrect access code.")
        return False

    # Step 2: Validate Employee ID + Name against roster
    client = get_gsheet_client()
    if not client:
        st.error("Unable to connect to Google Sheets. Check gcp_service_account secret.")
        return False

    try:
        emp_sheet = client.open("AAP New Hire Orientation Progress").worksheet("Employee Roster")
    except Exception:
        st.error("Could not open 'Employee Roster' tab.")
        return False

    try:
        records = emp_sheet.get_all_records()
        for row in records:
            row_id = str(row.get("Employee ID", "")).strip().lower()
            row_name = str(row.get("Full Name", "")).strip().lower()
            if row_id == employee_id.strip().lower():
                if row_name == full_name.strip().lower():
                    raw_track = str(row.get("Track", "")).strip().lower()
                    st.session_state["emp_track"] = "warehouse" if raw_track == "warehouse" else "general"
                    st.session_state["emp_department"] = str(row.get("Department", ""))
                    st.session_state["emp_position"] = str(row.get("Position", ""))
                    st.session_state["emp_start_date"] = str(row.get("Start Date", ""))
                    return True
                else:
                    st.error("Employee ID found but name does not match our records.")
                    return False
        st.error("Employee ID not found.")
        return False
    except Exception as e:
        st.error(f"Verification error: {e}")
        return False

def inject_css():
    html("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    :root{--ink:#0A0A0B;--surface:#F5F5F7;--crimson:#B11226;--crimson-soft:rgba(177,18,38,0.08);--g100:#F5F5F7;--g200:#E8E8ED;--g300:#D2D2D7;--g400:#86868B;--g500:#6E6E73;--g600:#424245;--white:#FFF;--rlg:24px;--rmd:16px;--rsm:12px;--rxs:8px;--glass:rgba(255,255,255,0.72);--blur:blur(20px);--sh1:0 20px 50px rgba(0,0,0,0.05);--sh2:0 24px 56px rgba(0,0,0,0.09);--sh3:0 32px 64px rgba(0,0,0,0.12);--ease:all .3s cubic-bezier(.25,.46,.45,.94)}
    html,body,[class*="css"]{font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif!important;-webkit-font-smoothing:antialiased}
    .stApp{background:var(--surface)!important}
    h1,h2,h3{font-family:'Inter',-apple-system,sans-serif!important;color:var(--ink)!important;letter-spacing:-.025em;line-height:1.2}
    h1{font-weight:700!important}h2{font-weight:700!important}h3{font-weight:600!important}
    [data-testid="stSidebar"]{background:rgba(10,10,11,0.92)!important;backdrop-filter:blur(40px) saturate(180%);border-right:1px solid rgba(255,255,255,0.06)}
    [data-testid="stSidebar"] .block-container{padding:1rem!important}
    [data-testid="stSidebar"] .stButton>button{width:100%!important;border-radius:var(--rsm)!important;border:1px solid rgba(255,255,255,0.10)!important;background:rgba(255,255,255,0.06)!important;color:var(--g100)!important;font-size:.84rem!important;font-weight:600!important;transition:var(--ease)!important;text-align:left!important}
    [data-testid="stSidebar"] .stButton>button:hover{background:rgba(255,255,255,0.10)!important;transform:translateX(2px)!important}
    [data-testid="stSidebar"] [data-testid="stBaseButton-primary"]{background:rgba(177,18,38,0.25)!important;border-color:rgba(177,18,38,0.35)!important;color:#fff!important}
    .sidebar-header{background:rgba(255,255,255,0.06);backdrop-filter:var(--blur);border-radius:var(--rmd);padding:20px 16px;margin-bottom:16px;border:1px solid rgba(255,255,255,0.08)}
    .sidebar-header *{color:var(--g100)!important}
    .sidebar-label{font-size:.62rem;text-transform:uppercase;letter-spacing:.14em;color:rgba(255,255,255,0.36);font-weight:600;margin-bottom:2px}
    .sidebar-value{font-size:.9rem;font-weight:600;color:#fff}
    .sidebar-section-label{font-size:.65rem;text-transform:uppercase;letter-spacing:.14em;color:rgba(255,255,255,0.36);margin:16px 2px 8px;font-weight:600}
    .sidebar-progress-bg{width:100%;height:6px;border-radius:999px;background:rgba(255,255,255,0.08);overflow:hidden}
    .sidebar-progress-fill{height:100%;border-radius:inherit;background:var(--crimson);transition:width .4s cubic-bezier(.25,.46,.45,.94)}
    .sidebar-hr-card{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.06);border-radius:var(--rsm);padding:14px;margin-top:12px}
    .sidebar-hr-card *{color:rgba(255,255,255,0.50)!important;font-size:.78rem;line-height:1.7}
    .sidebar-hr-card strong{color:rgba(255,255,255,0.70)!important}
    .premium-hero{background:var(--ink);border-radius:var(--rlg);padding:40px;position:relative;overflow:hidden;border:1px solid rgba(255,255,255,0.06);box-shadow:var(--sh3);margin-bottom:28px}
    .premium-hero::before{content:"";position:absolute;width:500px;height:500px;right:-180px;top:-200px;background:radial-gradient(circle,rgba(177,18,38,0.25) 0%,transparent 65%)}
    .premium-hero h1{color:var(--g100)!important;font-size:2.2rem!important;font-weight:800!important;letter-spacing:-.035em!important;margin:0 0 8px!important;position:relative;z-index:1}
    .premium-hero p{color:var(--g400)!important;font-size:1rem;margin:0!important;max-width:760px;position:relative;z-index:1;line-height:1.7}
    .premium-kicker{display:inline-block;font-size:.68rem;color:var(--crimson);letter-spacing:.18em;text-transform:uppercase;font-weight:700;margin-bottom:12px;position:relative;z-index:1}
    .module-card{background:var(--glass);backdrop-filter:var(--blur);border-radius:var(--rmd);border:1px solid rgba(255,255,255,0.18);border-left:4px solid var(--crimson);padding:24px;margin-bottom:16px;box-shadow:var(--sh1);transition:var(--ease)}
    .module-card:hover{transform:translateY(-2px);box-shadow:var(--sh2)}
    .module-card.complete{border-left-color:#34C759}
    .module-name{color:var(--ink);font-weight:700;font-size:1.01rem;margin:0}
    .module-sub{color:var(--g500);font-size:.86rem;margin:8px 0 12px;line-height:1.7}
    .pill{font-size:.64rem;border-radius:99px;padding:4px 12px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;display:inline-block}
    .pill.pending{background:var(--g200);color:var(--g600)}.pill.live{background:var(--crimson-soft);color:var(--crimson)}.pill.done{background:rgba(52,199,89,0.10);color:#248A3D}
    .stat-card{background:var(--glass);backdrop-filter:var(--blur);border:1px solid rgba(255,255,255,0.18);border-radius:var(--rmd);padding:20px;box-shadow:var(--sh1);transition:var(--ease)}
    .stat-card:hover{transform:translateY(-2px);box-shadow:var(--sh2)}
    .stat-label{font-size:.68rem;color:var(--g500);letter-spacing:.10em;text-transform:uppercase;font-weight:600}
    .stat-value{color:var(--ink);font-size:1.8rem;font-weight:800;letter-spacing:-.03em;margin-top:4px}
    .module-hero{background:var(--ink);border-radius:var(--rlg);padding:32px;margin-bottom:24px;border:1px solid rgba(255,255,255,0.06);box-shadow:var(--sh3);position:relative;overflow:hidden}
    .module-hero::after{content:"";position:absolute;width:400px;height:400px;right:-160px;top:-200px;background:radial-gradient(circle,rgba(177,18,38,0.18) 0%,transparent 70%)}
    .module-hero h2{color:var(--g100)!important;position:relative;z-index:1;margin:4px 0 8px}
    .module-hero p{color:var(--g400);position:relative;z-index:1;margin:0}
    .info-box{background:var(--crimson-soft);border-left:3px solid var(--crimson);border-radius:0 var(--rxs) var(--rxs) 0;padding:16px 20px;margin:20px 0;color:var(--ink)!important;font-size:.9rem;line-height:1.7}
    .info-box.green{background:rgba(52,199,89,0.08);border-left-color:#34C759}
    .styled-table{width:100%;border-collapse:separate;border-spacing:0;font-size:.88rem;margin:16px 0;border-radius:var(--rsm);overflow:hidden;box-shadow:var(--sh1);border:1px solid var(--g200)}
    .styled-table th{background:var(--ink);color:var(--g100);padding:12px 16px;text-align:left;font-weight:600;font-size:.78rem;letter-spacing:.03em;text-transform:uppercase}
    .styled-table td{padding:12px 16px;border-bottom:1px solid var(--g200);color:var(--g600);background:var(--white);line-height:1.6}
    .styled-table tr:nth-child(even) td{background:var(--surface)}.styled-table tr:last-child td{border-bottom:none}
    .timeline-item{border-left:3px solid var(--crimson);padding:0 0 20px 20px;margin-left:10px;position:relative}
    .timeline-item::before{content:'';width:12px;height:12px;background:var(--crimson);border-radius:50%;position:absolute;left:-7.5px;top:4px}
    .timeline-item:last-child{border-left-color:transparent}
    .quiz-pass{background:rgba(52,199,89,0.10);border:1px solid rgba(52,199,89,0.30);color:#248A3D;padding:16px;border-radius:var(--rsm);text-align:center;font-weight:600}
    .quiz-fail{background:rgba(177,18,38,0.08);border:1px solid rgba(177,18,38,0.20);color:var(--crimson);padding:16px;border-radius:var(--rsm);text-align:center;font-weight:600}
    [data-testid="stBaseButton-primary"]{background:var(--crimson)!important;color:white!important;border:none!important;border-radius:var(--rsm)!important;font-weight:600!important;box-shadow:0 4px 16px rgba(177,18,38,0.20)!important}
    [data-testid="stBaseButton-primary"]:hover{transform:translateY(-2px)!important;box-shadow:0 8px 24px rgba(177,18,38,0.30)!important}
    div[data-testid="stFormSubmitButton"] button{background:var(--crimson)!important;color:#fff!important;border:none!important;border-radius:var(--rsm)!important;font-weight:700!important;box-shadow:0 4px 16px rgba(177,18,38,0.20)!important}
    .stTabs [data-baseweb="tab-list"]{gap:0;background:var(--g200);border-radius:var(--rsm);padding:4px}
    .stTabs [data-baseweb="tab"]{border-radius:var(--rxs)!important;font-weight:600!important;font-size:.82rem!important;color:var(--g500)!important;padding:8px 16px!important}
    .stTabs [aria-selected="true"]{background:var(--white)!important;color:var(--ink)!important;box-shadow:0 1px 4px rgba(0,0,0,0.08)!important}
    .stTabs [data-baseweb="tab-highlight"],.stTabs [data-baseweb="tab-border"]{display:none!important}
    .stTextInput input{border-radius:var(--rsm)!important;border:1.5px solid var(--g200)!important;font-size:.92rem!important;padding:10px 14px!important}
    .stTextInput input:focus{border-color:var(--crimson)!important;box-shadow:0 0 0 3px rgba(177,18,38,0.08)!important}
    [data-testid="stForm"]{background:rgba(255,255,255,0.96);backdrop-filter:blur(20px);border-radius:var(--rlg);padding:40px 36px 32px!important;box-shadow:var(--sh3);border:1px solid rgba(255,255,255,0.18)}
    #MainMenu{visibility:hidden}footer{visibility:hidden}
    </style>""")

inject_css()


def show_login():
    html("<style>.stApp { background: #0A0A0B !important; }</style>")
    _, center, _ = st.columns([1, 2, 1])
    with center:
        logo = _logo_b64()
        if logo:
            html(f'<div style="text-align:center; margin: 60px 0 40px;"><img src="data:image/png;base64,{logo}" style="height:80px; max-width:280px; object-fit:contain; filter:brightness(1.1);"></div>')
        html('<p style="text-align:center; font-size:1.2rem; font-weight:800; color:#FFFFFF; margin:0 0 4px;">Employee Sign In</p><p style="text-align:center; color:#86868B; font-size:0.86rem; margin:0 0 24px; line-height:1.7;">Use the credentials provided by HR to continue.</p>')
        with st.form("login_form"):
            access_code = st.text_input("Access Code", placeholder="Enter the code HR gave you", type="password")
            employee_id = st.text_input("Employee ID", placeholder="e.g. 10042")
            full_name = st.text_input("Full Name", placeholder="As it appears in your HR paperwork")
            submitted = st.form_submit_button("Sign In", use_container_width=True)
            if submitted:
                if not access_code or not employee_id or not full_name:
                    st.error("Please fill in all three fields to continue.")
                else:
                    with st.spinner("Verifying credentials..."):
                        if validate_login(access_code, employee_id, full_name):
                            st.session_state["logged_in"] = True
                            st.session_state["emp_name"] = full_name.strip().title()
                            st.session_state["emp_number"] = employee_id.strip()
                            st.rerun()
                        else:
                            st.error("Invalid credentials. Please check your access code, employee number, and name.")
        html('<div style="text-align:center; margin-top:32px; padding-top:20px; border-top:1px solid rgba(255,255,255,0.06);"><p style="color:#86868B; font-size:0.78rem; margin:0; line-height:2;">Need help? <strong style="color:#D2D2D7;">Nicole Thornton</strong> | nicole.thornton@apirx.com | 256-574-7528</p></div>')


def show_sidebar():
    with st.sidebar:
        logo = _logo_b64()
        logo_html = f'<img src="data:image/png;base64,{logo}" style="max-height:48px; width:100%; object-fit:contain; margin-bottom:12px; opacity:0.9;">' if logo else ""
        html(f'<div class="sidebar-header">{logo_html}<div class="sidebar-label">Employee</div><div class="sidebar-value">{st.session_state["emp_name"]}</div></div>')
        done, total = calc_progress()
        pct = int((done / total) * 100) if total > 0 else 0
        html(f'<div class="sidebar-label" style="margin:8px 0 4px;">Progress &middot; {pct}%</div><div class="sidebar-progress-bg"><div class="sidebar-progress-fill" style="width:{pct}%"></div></div>')
        html('<div class="sidebar-section-label">Navigation</div>')
        if st.button("Home", use_container_width=True, key="nav_home"):
            st.session_state["current_page"] = "home"
            st.session_state["current_module"] = None
            st.rerun()
        for mk in MODULE_KEYS:
            check = " ✅" if is_module_complete(mk) else ""
            if st.button(f"{MODULE_ICONS[mk]}  {MODULE_NAMES[mk]}{check}", use_container_width=True, key=f"nav_{mk}"):
                st.session_state["current_page"] = "module"
                st.session_state["current_module"] = mk
                st.rerun()
        st.markdown("---")
        html('<div class="sidebar-hr-card"><strong>HR Contact</strong><br>Nicole Thornton<br>HR Manager<br>256-574-7528<br>nicole.thornton@apirx.com</div>')
        st.markdown("")
        if st.button("Log Out", use_container_width=True, key="logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


def show_home():
    first = st.session_state["emp_name"].split()[0] if st.session_state["emp_name"] else "there"
    done, total = calc_progress()
    pct = int((done / total) * 100) if total > 0 else 0
    completed = sum(1 for mk in MODULE_KEYS if is_module_complete(mk))
    html(f'<div class="premium-hero"><div class="premium-kicker">New Hire Onboarding</div><h1>Welcome, {first} 👋</h1><p>Complete each training module below to finish your onboarding.</p></div>')
    c1, c2, c3 = st.columns(3)
    with c1:
        html(f'<div class="stat-card"><div class="stat-label">Overall</div><div class="stat-value">{pct}%</div></div>')
    with c2:
        html(f'<div class="stat-card"><div class="stat-label">Modules Done</div><div class="stat-value">{completed}/{len(MODULE_KEYS)}</div></div>')
    with c3:
        html(f'<div class="stat-card"><div class="stat-label">Items Done</div><div class="stat-value">{done}/{total}</div></div>')
    st.markdown("")
    cols = st.columns(2)
    for i, mk in enumerate(MODULE_KEYS):
        complete = is_module_complete(mk)
        passed = st.session_state.get(f"quiz_{mk}_passed", False)
        checks = st.session_state.get(f"checklist_{mk}", {})
        done_c = sum(1 for v in checks.values() if v)
        if complete:
            pill = '<span class="pill done">Complete</span>'
            ecls = " complete"
        elif passed or done_c > 0:
            pill = '<span class="pill live">In Progress</span>'
            ecls = ""
        else:
            pill = '<span class="pill pending">Not Started</span>'
            ecls = ""
        with cols[i % 2]:
            html(f'<div class="module-card{ecls}"><div style="display:flex;justify-content:space-between;align-items:start;"><p class="module-name">{MODULE_ICONS[mk]} {MODULE_NAMES[mk]}</p>{pill}</div><p class="module-sub">{MODULE_DESCRIPTIONS[mk]}</p></div>')
            if st.button("Open Module", key=f"open_{mk}", use_container_width=True):
                st.session_state["current_page"] = "module"
                st.session_state["current_module"] = mk
                st.rerun()


def render_quiz(module_key, questions):
    st.markdown("---")
    st.markdown("### Module Quiz")
    if st.session_state.get(f"quiz_{module_key}_passed"):
        html('<div class="quiz-pass">✅ Quiz Passed!</div>')
        return
    st.info("Answer all questions correctly to pass. Retake as needed.")
    answers = {}
    for i, q in enumerate(questions):
        answers[i] = st.radio(f"**Q{i+1}.** {q['q']}", options=q["options"], index=None, key=f"quiz_{module_key}_q{i}")
    if st.button("Submit Quiz", key=f"submit_quiz_{module_key}", type="primary"):
        correct = sum(1 for i, q in enumerate(questions) if answers[i] == q["options"][q["answer"]])
        if correct == len(questions):
            st.session_state[f"quiz_{module_key}_passed"] = True
            html('<div class="quiz-pass">🎉 All correct!</div>')
            st.rerun()
        else:
            html(f'<div class="quiz-fail">❌ {correct}/{len(questions)} correct. Try again.</div>')


def render_checklist(module_key, items):
    st.markdown("---")
    st.markdown("### Understanding Checklist")
    checks = st.session_state.get(f"checklist_{module_key}", {})
    for i, item in enumerate(items):
        key = f"cl_{module_key}_{i}"
        checks[key] = st.checkbox(item, value=checks.get(key, False), key=key)
    st.session_state[f"checklist_{module_key}"] = checks
    done = sum(1 for v in checks.values() if v)
    if done == len(items):
        st.success("All items confirmed!")
    else:
        st.info(f"{done}/{len(items)} confirmed")


def module_welcome():
    html('<div class="module-hero"><div class="premium-kicker">Module 1</div><h2>🏢 Welcome to AAP</h2><p>Company History, Mission, Vision & Guiding Principles</p></div>')
    st.markdown("## Who We Are")
    st.markdown("American Associated Pharmacies (AAP) is a national cooperative of more than **2,000 independent pharmacies**. Formed in 2009 when **United Drugs** (Phoenix, AZ) and **Associated Pharmacies, Inc. (API)** (Scottsboro, AL) joined forces. Today AAP operates API with two U.S. warehouse locations, providing member-focused support and cost-saving programs.")
    html('<div class="info-box"><strong>Key Fact:</strong> AAP saves its member pharmacies millions in operating and acquisition costs each year through its Prime Vendor Agreement.</div>')
    st.markdown("## Our Mission")
    st.markdown("AAP provides support and customized solutions for independent community pharmacies to enhance profitability, streamline operations, and improve patient care.")
    st.markdown("## Our Vision")
    st.markdown("*Helping independent pharmacies thrive in a competitive healthcare market.*")
    st.markdown("## Our Values")
    for icon, title, desc in [("🎯","Customer Focus","Meeting and exceeding customer expectations. Service is an attitude."),("⚖️","Integrity","Honesty without compromising truth. Consistency builds trust."),("🤝","Respect","Dignity for all. Teamwork and open communication."),("⭐","Excellence","Highest quality. Continuous improvement."),("🔑","Ownership","Accountability. Taking responsibility.")]:
        st.markdown(f"**{icon} {title}** — {desc}")
    render_quiz("welcome", [
        {"q": "When was AAP formed?", "options": ["2001","2005","2009","2012"], "answer": 2},
        {"q": "How many independent pharmacies?", "options": ["500","1,000","2,000","5,000"], "answer": 2},
        {"q": "Which is NOT a core value?", "options": ["Customer Focus","Integrity","Profitability","Ownership"], "answer": 2},
        {"q": "AAP's vision?", "options": ["Largest pharmacy","Helping pharmacies thrive in a competitive market","Maximize returns","Cheapest prescriptions"], "answer": 1},
    ])
    render_checklist("welcome", ["I understand AAP's history.","I can identify the mission and vision.","I know the five core values.","I understand AAP is a cooperative."])


def module_conduct():
    html('<div class="module-hero"><div class="premium-kicker">Module 2</div><h2>📋 Code of Conduct & Ethics</h2><p>Professional Standards & Workplace Expectations</p></div>')
    st.markdown("## Business Ethics")
    st.markdown("AAP's success depends on customer trust. Employees must act with honesty and integrity. Non-compliance leads to disciplinary action up to termination.")
    tab1, tab2, tab3, tab4 = st.tabs(["Conflicts of Interest","Confidentiality","Outside Employment","Equal Opportunity"])
    with tab1:
        st.markdown("Avoid actual or potential conflicts. Contact HR with questions.")
    with tab2:
        st.markdown("All employees sign a **confidentiality/NDA** upon hire. Refusal = immediate termination. Personnel files are company property.")
    with tab3:
        st.markdown("Outside jobs permitted if AAP performance is satisfactory. Conflicts may require choosing.")
    with tab4:
        st.markdown("Decisions based on merit. No discrimination on any protected characteristic. Report concerns to supervisor or HR.")
    st.markdown("## Problem Resolution")
    st.markdown("1. Supervisor or HR → 2. VP → President → CEO → 3. Board if needed. No retaliation for good-faith complaints.")
    render_quiz("conduct", [
        {"q": "What must employees sign upon hire?", "options": ["Non-compete","Confidentiality/NDA","Social media policy","Union form"], "answer": 1},
        {"q": "Work authorization verification system?", "options": ["HIPAA","E-Verify","ADP","LinkedIn"], "answer": 1},
        {"q": "First contact for workplace concerns?", "options": ["CEO","Coworker","Supervisor or HR","Attorney"], "answer": 2},
        {"q": "Outside employment allowed if:", "options": ["<20 hrs elsewhere","AAP performance satisfactory","Manager verbal OK","Different industry"], "answer": 1},
    ])
    render_checklist("conduct", ["I understand ethics expectations.","I understand confidentiality/NDA requirements.","I know the problem resolution steps.","I understand equal opportunity policy."])


def module_attendance():
    html('<div class="module-hero"><div class="premium-kicker">Module 3</div><h2>⏰ Attendance & PTO Policies</h2><p>Vacation, Personal Leave, Holidays & Point System</p></div>')
    st.markdown("## Vacation (Full-time, 2-hour min increment)")
    html("""<table class="styled-table"><tr><th>Tenure</th><th>Days/Year</th><th>Rate</th></tr>
    <tr><td>60 days - 1yr</td><td>3 (24h)</td><td>0.46/wk</td></tr>
    <tr><td>1-2 yrs</td><td>5 (40h)</td><td>0.77/wk</td></tr>
    <tr><td>2-3 yrs</td><td>7 (56h)</td><td>1.07/wk</td></tr>
    <tr><td>3-5 yrs</td><td>10 (80h)</td><td>1.54/wk</td></tr>
    <tr><td>5-9 yrs</td><td>15 (120h)</td><td>2.31/wk</td></tr>
    <tr><td>10-19 yrs</td><td>17 (136h)</td><td>2.62/wk</td></tr>
    <tr><td>20+ yrs</td><td>19 (152h)</td><td>2.93/wk</td></tr></table>""")
    html('<div class="info-box">No advance use. 5+ consecutive days = President approval. Bank up to 152 hrs. Paid at termination.</div>')
    st.markdown("## Personal Leave (All employees, 1-hour min increment)")
    st.markdown("**Full-time:** 3 days initially, 4 after 1yr, 5 after 5yrs. **Part-time:** 1hr per 30hrs worked. 60-day waiting period. **Forfeited** at year-end. Not paid at termination.")
    st.markdown("## Holidays")
    for h in ["New Year's Day","Memorial Day","Independence Day","Labor Day","Thanksgiving","Day after Thanksgiving/Floating","Christmas Eve/Floating","Christmas Day"]:
        st.markdown(f"- {h}")
    html('<div class="info-box">Sat holidays = Fri. Sun holidays = Mon. Work a holiday = floating holiday within 90 days.</div>')
    st.markdown("## Point System (Non-exempt)")
    html("""<table class="styled-table"><tr><th>Event</th><th>Points</th></tr>
    <tr><td>Tardy ≤5 min</td><td>0</td></tr><tr><td>Tardy/early leave <4hrs</td><td>½</td></tr>
    <tr><td>Full absence/4+ hrs</td><td>1</td></tr><tr><td>No-call (15+ min late)</td><td>1½</td></tr></table>""")
    html("""<table class="styled-table"><tr><th>Points (12 mo)</th><th>Action</th></tr>
    <tr><td>5</td><td>Coaching</td></tr><tr><td>6</td><td>Verbal Warning</td></tr>
    <tr><td>7</td><td>Written Warning</td></tr><tr><td>8</td><td>Termination</td></tr></table>""")
    html('<div class="info-box green"><strong>Bonus:</strong> 2 months perfect = remove 1 point. 3 months perfect = $75 bonus!</div>')
    st.warning("2 consecutive no-call days = voluntary resignation.")
    render_quiz("attendance", [
        {"q": "Vacation minimum increment?", "options": ["1 hour","2 hours","4 hours","8 hours"], "answer": 1},
        {"q": "Personal leave minimum increment?", "options": ["1 hour","2 hours","4 hours","8 hours"], "answer": 0},
        {"q": "No-call/no-show points?", "options": ["½","1","1½","2"], "answer": 2},
        {"q": "Termination at how many points?", "options": ["6","7","8","10"], "answer": 2},
        {"q": "Consecutive no-call days = resignation?", "options": ["1","2","3","5"], "answer": 1},
    ])
    render_checklist("attendance", ["I understand vacation accrual and 2-hour increment.","I understand personal leave 1-hour increment, forfeits at year-end.","I know the 8 holidays and floating holiday rules.","I understand the point system and thresholds.","I understand 2 no-call days = voluntary resignation."])


def module_workplace():
    html('<div class="module-hero"><div class="premium-kicker">Module 4</div><h2>🏗️ Workplace Policies</h2><p>Safety, Dress Code, Drug Policy, Technology & More</p></div>')
    tabs = st.tabs(["Dress Code","Safety","Drug & Alcohol","Computer/Email","Harassment","Other"])
    with tabs[0]:
        st.markdown("Neat, clean, appropriate. No offensive clothing. No heavy perfumes. Non-compliance = sent home.")
    with tabs[1]:
        st.markdown("Report unsafe conditions and all injuries immediately. Work-related accidents = **immediate drug/alcohol testing**.")
    with tabs[2]:
        st.markdown("Zero tolerance. **Random testing** anytime. Violations = immediate termination. EAP available.")
    with tabs[3]:
        st.markdown("Company property, business use. **May be monitored.** No inappropriate content. No illegal software copying.")
    with tabs[4]:
        st.markdown("Zero tolerance for harassment/discrimination. Report to supervisor or HR. **No retaliation.**")
    with tabs[5]:
        st.markdown("**Overtime:** Prior supervisor approval required.\n\n**Violence:** Zero tolerance. Report within 24hrs.\n\n**Travel:** Reasonable expenses reimbursed. Falsifying reports = termination.")
    render_quiz("workplace", [
        {"q": "After a work accident?", "options": ["Nothing","Report only","Immediate drug/alcohol test","Go home"], "answer": 2},
        {"q": "Computer systems are:", "options": ["Personal","Company property, monitored","Free for personal use","Monitored only in investigations"], "answer": 1},
        {"q": "If harassed, first step?", "options": ["Social media","Ignore","Tell offender to stop or report to HR","Confront publicly"], "answer": 2},
        {"q": "Overtime requires:", "options": ["Coworker approval","Prior supervisor approval","After-the-fact report","Self-authorization"], "answer": 1},
    ])
    render_checklist("workplace", ["I understand dress code.","I understand safety reporting.","I understand drug/alcohol policy.","I understand computer monitoring.","I know harassment reporting and no-retaliation."])


def module_benefits():
    html('<div class="module-hero"><div class="premium-kicker">Module 5</div><h2>🩺 Benefits Overview</h2><p>Health, Dental, Vision, Retirement & Supplemental</p></div>')
    html('<div class="info-box"><strong>Eligibility:</strong> Full-time (30+ hrs) enroll within 30 days. Effective <strong>1st of month after 60 days</strong>. Dependents to age 26.</div>')
    ft, pt = st.tabs(["Full-Time Benefits","All Employee Benefits"])
    with ft:
        st.markdown("## Medical (BCBS Alabama)")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### PPO Plan\nEmployee: **$157.20**/mo | Family: **$678.62**/mo\n\nDeductible: $500/$1K | 20% coinsurance | OOP: $2,250/$4,500\n\nPCP $30 / Specialist $45 | Rx: $10/$30/$50")
        with c2:
            st.markdown("### HDHP + HSA\nEmployee: **$136.34**/mo | Family: **$581.72**/mo\n\nDeductible: $1,700/$3,400 | 10% coinsurance | OOP: $3,400/$6,800\n\nCompany HSA: $900/$1,800/yr | Limits: $4,400/$8,750")
        st.markdown("## Dental (Guardian)\nBase: $6.78/mo | High: $10.66/mo. Preventive 100%. Basic 80%/100%. Major 50% (12-mo wait).")
        st.markdown("## Vision (Guardian)\nEmployee $6.93/mo. Exams/lenses 12mo. Frames 24mo. $130 allowance.")
        st.markdown("## Life & Disability\n**Basic Life/AD&D:** Free (annual earnings up to $270K). **STD:** 60% weekly, employee-paid. **LTD:** 60% monthly, **company-paid**.")
        st.markdown("## Supplemental\nAccident $14.55/mo | Cancer $21.28/mo | Critical Illness $5K-$20K (age-based).")
        st.markdown("## 401(k)\nAfter 60 days. **Match:** 100% of first 3% + 50% of next 2% = **4% on 5%**. Vested immediately.")
    with pt:
        st.markdown("## Free for ALL Employees")
        st.markdown("**📱 Teladoc** — Free 24/7 telehealth. 1-800-835-2362 / teladoc.com")
        st.markdown("**🧠 LifeMatters EAP** — Free counseling, legal, financial. 1-800-634-6433 / mylifematters.com (pw: AAP1)")
        st.markdown("**📚 LinkedIn Learning** — Full course library for development.")
        st.markdown("**🎁 BenefitHub** — aapperks.benefithub.com, code **9Y7G26**")
        st.markdown("**🕐 Personal Time Off** — All employees earn personal leave.")
    render_quiz("benefits", [
        {"q": "Benefits effective when?", "options": ["Day 1","30 days","1st of month after 60 days","90 days"], "answer": 2},
        {"q": "401(k) match on 5% contribution?", "options": ["2%","3%","4%","5%"], "answer": 2},
        {"q": "Free for ALL employees?", "options": ["Dental","STD","Teladoc","Vision"], "answer": 2},
        {"q": "Basic Life/AD&D cost?", "options": ["50% employer","No cost","Employee-paid","Enrollment required"], "answer": 1},
    ])
    render_checklist("benefits", ["I understand PPO vs HDHP/HSA.","I know the 401(k) match.","I know free benefits (Teladoc, EAP, LinkedIn, BenefitHub).","I know enrollment is within 30 days.","I understand supplemental options."])


def module_firststeps():
    html('<div class="module-hero"><div class="premium-kicker">Module 6</div><h2>🚀 First Steps</h2><p>Action Items, System Access & 90-Day Roadmap</p></div>')
    st.markdown("## Action Items")
    for icon, title, desc in [("✅","Verify Account Access","Confirm email and system access."),("📝","Sign Documents","Complete BambooHR onboarding packet."),("📚","Activate LinkedIn Learning","https://linkedin.com/learning with company email."),("📄","Provide I-9 Documents","Within **3 business days** of start."),("💰","Register for Paylocity","Set up payroll account."),("📱","Download BambooHR App","Employee profile, time off & documents.")]:
        st.markdown(f"**{icon} {title}** — {desc}")
    st.markdown("---")
    st.markdown("## 90-Day Timeline")
    html("""<div class="timeline-item"><h4 style="margin:0 0 4px;color:var(--ink);">Days 1-30: Orientation</h4><ul style="color:var(--g600);margin:4px 0;"><li>Complete orientation and training</li><li>Sign paperwork, provide I-9</li><li>Get system access, meet team, shadow processes</li><li>Complete 30-Day Survey</li></ul></div>
    <div class="timeline-item"><h4 style="margin:0 0 4px;color:var(--ink);">Days 31-60: Independence</h4><ul style="color:var(--g600);margin:4px 0;"><li>Execute core responsibilities independently</li><li>Complete 60-Day Survey</li><li>PTO and holiday pay eligibility</li><li>End of probationary period</li><li>Set a 30-day goal with your supervisor</li></ul></div>
    <div class="timeline-item"><h4 style="margin:0 0 4px;color:var(--ink);">Days 61-90: Growth</h4><ul style="color:var(--g600);margin:4px 0;"><li>Build consistency in your role</li><li>Identify improvement opportunities</li><li>First performance review</li><li>Full benefits eligibility</li></ul></div>""")
    render_quiz("firststeps", [
        {"q": "I-9 documents due within?", "options": ["1 day","3 business days","5 days","10 days"], "answer": 1},
        {"q": "Probation ends at?", "options": ["30 days","60 days","90 days","120 days"], "answer": 1},
        {"q": "PTO eligibility after?", "options": ["Day 1","30 days","60 days","90 days"], "answer": 2},
        {"q": "App for profile & time off?", "options": ["Workday","BambooHR","ADP","Gusto"], "answer": 1},
    ])
    render_checklist("firststeps", ["I will verify access and sign documents.","I will activate LinkedIn Learning.","I will provide I-9 within 3 days.","I will register for Paylocity and BambooHR.","I understand the 90-day timeline.","I know who to contact in HR."])


_MODULE_FN = {"welcome": module_welcome, "conduct": module_conduct, "attendance": module_attendance, "workplace": module_workplace, "benefits": module_benefits, "firststeps": module_firststeps}

def show_module(mk):
    if st.button("< Back to Home", key="back_home"):
        st.session_state["current_page"] = "home"
        st.session_state["current_module"] = None
        st.rerun()
    _MODULE_FN[mk]()
    st.markdown("---")
    idx = MODULE_KEYS.index(mk)
    c1, c2 = st.columns(2)
    if idx > 0:
        with c1:
            if st.button(f"< {MODULE_NAMES[MODULE_KEYS[idx-1]]}", key="prev_mod"):
                st.session_state["current_module"] = MODULE_KEYS[idx-1]
                st.rerun()
    if idx < len(MODULE_KEYS) - 1:
        with c2:
            if st.button(f"{MODULE_NAMES[MODULE_KEYS[idx+1]]} >", key="next_mod"):
                st.session_state["current_module"] = MODULE_KEYS[idx+1]
                st.rerun()


def main():
    if not st.session_state["logged_in"]:
        show_login()
    else:
        show_sidebar()
        if st.session_state["current_page"] == "module" and st.session_state["current_module"]:
            show_module(st.session_state["current_module"])
        else:
            show_home()

if __name__ == "__main__":
    main()
