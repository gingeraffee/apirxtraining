import streamlit as st
import json
import os
import base64
from datetime import datetime

# ─── Page Config ───
st.set_page_config(
    page_title="AAP Employee Onboarding Portal",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Google Sheets Auth ───
def validate_login(access_code, employee_num, full_name):
    """Validate credentials against Google Sheet."""
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds_dict = json.loads(os.environ.get("GSHEET_CREDS", "{}"))
        if not creds_dict:
            st.error("Google Sheets credentials not configured.")
            return False
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        client = gspread.authorize(creds)
        sheet = client.open("AAP_Onboarding_Employees").sheet1
        records = sheet.get_all_records()
        for row in records:
            if (str(row.get("Access Code", "")).strip().lower() == access_code.strip().lower()
                and str(row.get("Employee #", "")).strip().lower() == employee_num.strip().lower()
                and str(row.get("Full Name", "")).strip().lower() == full_name.strip().lower()):
                st.session_state["emp_department"] = str(row.get("Department", ""))
                st.session_state["emp_position"] = str(row.get("Position", ""))
                st.session_state["emp_start_date"] = str(row.get("Start Date", ""))
                return True
        return False
    except Exception as e:
        st.error(f"Login error: {e}")
        return False


# ─── Session State Defaults ───
defaults = {
    "logged_in": False,
    "emp_name": "",
    "emp_number": "",
    "emp_department": "",
    "emp_position": "",
    "emp_start_date": "",
    "current_page": "home",
    "current_module": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Initialize progress tracking
MODULE_KEYS = ["welcome", "conduct", "attendance", "workplace", "benefits", "firststeps"]
MODULE_NAMES = {
    "welcome": "Welcome to AAP",
    "conduct": "Code of Conduct & Ethics",
    "attendance": "Attendance & PTO Policies",
    "workplace": "Workplace Policies",
    "benefits": "Benefits Overview",
    "firststeps": "First Steps"
}
MODULE_ICONS = {
    "welcome": "🏢",
    "conduct": "📋",
    "attendance": "⏰",
    "workplace": "🏗️",
    "benefits": "🩺",
    "firststeps": "🚀"
}

for mk in MODULE_KEYS:
    if f"quiz_{mk}_passed" not in st.session_state:
        st.session_state[f"quiz_{mk}_passed"] = False
    if f"checklist_{mk}" not in st.session_state:
        st.session_state[f"checklist_{mk}"] = {}


# ─── Logo Helper ───
def get_logo_base64():
    logo_path = os.path.join(os.path.dirname(__file__), "AAP_API.PNG")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


# ─── CSS ───
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Global */
    .stApp { font-family: 'Inter', sans-serif; }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1628 0%, #1a2a4a 100%);
    }
    section[data-testid="stSidebar"] * {
        color: #e0e8f5 !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.15) !important;
    }

    /* Card containers */
    .module-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
        transition: all 0.2s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .module-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 4px 12px rgba(59,130,246,0.15);
        transform: translateY(-2px);
    }
    .module-card h3 { margin: 0 0 8px 0; color: #1e293b; font-size: 1.1rem; }
    .module-card p { margin: 0; color: #64748b; font-size: 0.9rem; }

    /* Progress bar */
    .progress-container {
        background: #f1f5f9;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 24px;
    }
    .progress-bar-bg {
        background: #e2e8f0;
        border-radius: 8px;
        height: 14px;
        overflow: hidden;
        margin-top: 8px;
    }
    .progress-bar-fill {
        height: 100%;
        border-radius: 8px;
        background: linear-gradient(90deg, #2563eb, #3b82f6, #60a5fa);
        transition: width 0.5s ease;
    }

    /* Status badges */
    .badge-complete {
        background: #dcfce7; color: #166534;
        padding: 3px 10px; border-radius: 20px;
        font-size: 0.78rem; font-weight: 600;
        display: inline-block;
    }
    .badge-incomplete {
        background: #fef3c7; color: #92400e;
        padding: 3px 10px; border-radius: 20px;
        font-size: 0.78rem; font-weight: 600;
        display: inline-block;
    }
    .badge-locked {
        background: #f1f5f9; color: #94a3b8;
        padding: 3px 10px; border-radius: 20px;
        font-size: 0.78rem; font-weight: 600;
        display: inline-block;
    }

    /* Welcome banner */
    .welcome-banner {
        background: linear-gradient(135deg, #0a1628, #1e3a5f);
        color: white;
        padding: 36px 40px;
        border-radius: 16px;
        margin-bottom: 28px;
    }
    .welcome-banner h1 {
        color: white !important;
        font-size: 1.8rem;
        margin-bottom: 8px;
    }
    .welcome-banner p { color: #cbd5e1; font-size: 1rem; margin: 0; }

    /* Quiz styling */
    .quiz-section {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
    }
    .quiz-pass {
        background: #dcfce7;
        border: 1px solid #86efac;
        color: #166534;
        padding: 16px;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
    }
    .quiz-fail {
        background: #fef2f2;
        border: 1px solid #fca5a5;
        color: #991b1b;
        padding: 16px;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
    }

    /* Checklist */
    .checklist-section {
        background: #fffbeb;
        border: 1px solid #fde68a;
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
    }

    /* Section header */
    .section-header {
        background: linear-gradient(135deg, #0a1628, #1e3a5f);
        color: white;
        padding: 24px 28px;
        border-radius: 12px;
        margin-bottom: 24px;
    }
    .section-header h2 { color: white !important; margin: 0 0 4px 0; }
    .section-header p { color: #94a3b8; margin: 0; }

    /* Info boxes */
    .info-box {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 16px 20px;
        border-radius: 0 8px 8px 0;
        margin: 12px 0;
    }

    /* Timeline */
    .timeline-item {
        border-left: 3px solid #3b82f6;
        padding: 0 0 20px 20px;
        margin-left: 10px;
        position: relative;
    }
    .timeline-item::before {
        content: '';
        width: 12px; height: 12px;
        background: #3b82f6;
        border-radius: 50%;
        position: absolute;
        left: -7.5px; top: 4px;
    }
    .timeline-item:last-child { border-left-color: transparent; }

    /* Hide Streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    /* Login page */
    .login-container {
        max-width: 440px;
        margin: 60px auto;
        background: white;
        border-radius: 16px;
        padding: 40px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }

    /* Sidebar employee card */
    .emp-card {
        background: rgba(255,255,255,0.08);
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 12px;
    }
    .emp-card-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.6; margin-bottom: 2px; }
    .emp-card-value { font-size: 0.88rem; font-weight: 600; }

    /* Table styling */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        margin: 12px 0;
        font-size: 0.9rem;
    }
    .styled-table th {
        background: #0a1628;
        color: white;
        padding: 10px 14px;
        text-align: left;
        font-weight: 600;
    }
    .styled-table td {
        padding: 10px 14px;
        border-bottom: 1px solid #e2e8f0;
    }
    .styled-table tr:nth-child(even) td { background: #f8fafc; }
    </style>
    """, unsafe_allow_html=True)

inject_css()


# ═══════════════════════════════════════════════
# LOGIN PAGE
# ═══════════════════════════════════════════════
def show_login():
    logo_b64 = get_logo_base64()
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if logo_b64:
            st.markdown(f'<div style="text-align:center;margin-bottom:8px;"><img src="data:image/png;base64,{logo_b64}" style="height:90px;"></div>', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align:center;color:#0a1628;margin-bottom:4px;">Employee Onboarding Portal</h2>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center;color:#64748b;margin-bottom:28px;">Please log in with your onboarding credentials.</p>', unsafe_allow_html=True)

        with st.form("login_form"):
            access_code = st.text_input("Access Code", placeholder="Enter your access code")
            employee_num = st.text_input("Employee #", placeholder="Enter your employee number")
            full_name = st.text_input("Full Name", placeholder="Enter your full name")
            submitted = st.form_submit_button("Log In", use_container_width=True)

            if submitted:
                if not access_code or not employee_num or not full_name:
                    st.error("Please fill in all fields.")
                else:
                    with st.spinner("Verifying credentials..."):
                        if validate_login(access_code, employee_num, full_name):
                            st.session_state["logged_in"] = True
                            st.session_state["emp_name"] = full_name.strip().title()
                            st.session_state["emp_number"] = employee_num.strip()
                            st.rerun()
                        else:
                            st.error("Invalid credentials. Please check your access code, employee number, and name.")

        st.markdown("---")
        st.markdown('<p style="text-align:center;color:#94a3b8;font-size:0.82rem;">If you need login assistance, contact HR:<br><strong>Nicole Thornton</strong> · 256-574-7528 · nicole.thornton@apirx.com</p>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════
def show_sidebar():
    with st.sidebar:
        logo_b64 = get_logo_base64()
        if logo_b64:
            st.markdown(f'<div style="text-align:center;padding:12px 0;"><img src="data:image/png;base64,{logo_b64}" style="height:70px;"></div>', unsafe_allow_html=True)

        st.markdown("### Onboarding Portal")
        st.markdown("---")

        # Employee info card
        st.markdown(f"""
        <div class="emp-card">
            <div class="emp-card-label">Employee</div>
            <div class="emp-card-value">{st.session_state['emp_name']}</div>
        </div>
        <div class="emp-card">
            <div class="emp-card-label">Employee #</div>
            <div class="emp-card-value">{st.session_state['emp_number']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.session_state.get("emp_department"):
            st.markdown(f"""
            <div class="emp-card">
                <div class="emp-card-label">Department</div>
                <div class="emp-card-value">{st.session_state['emp_department']}</div>
            </div>
            """, unsafe_allow_html=True)
        if st.session_state.get("emp_position"):
            st.markdown(f"""
            <div class="emp-card">
                <div class="emp-card-label">Position</div>
                <div class="emp-card-value">{st.session_state['emp_position']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Navigation
        if st.button("🏠  Home", use_container_width=True, key="nav_home"):
            st.session_state["current_page"] = "home"
            st.session_state["current_module"] = None
            st.rerun()

        st.markdown("**Training Modules**")
        for mk in MODULE_KEYS:
            icon = MODULE_ICONS[mk]
            name = MODULE_NAMES[mk]
            passed = st.session_state.get(f"quiz_{mk}_passed", False)
            check_items = st.session_state.get(f"checklist_{mk}", {})
            # Determine total checklist items per module
            total_checks = get_checklist_count(mk)
            done_checks = sum(1 for v in check_items.values() if v)
            complete = passed and done_checks >= total_checks
            status = " ✅" if complete else ""
            if st.button(f"{icon}  {name}{status}", use_container_width=True, key=f"nav_{mk}"):
                st.session_state["current_page"] = "module"
                st.session_state["current_module"] = mk
                st.rerun()

        st.markdown("---")
        st.markdown("""
        <div style="font-size:0.8rem;opacity:0.85;">
            <strong>HR Contact</strong><br>
            Nicole Thornton<br>
            HR Manager<br>
            📞 256-574-7528<br>
            ✉️ nicole.thornton@apirx.com
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Log Out", use_container_width=True, key="logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


def get_checklist_count(mk):
    counts = {
        "welcome": 4,
        "conduct": 4,
        "attendance": 5,
        "workplace": 5,
        "benefits": 5,
        "firststeps": 6
    }
    return counts.get(mk, 4)


# ═══════════════════════════════════════════════
# PROGRESS CALCULATION
# ═══════════════════════════════════════════════
def calc_progress():
    total = 0
    done = 0
    for mk in MODULE_KEYS:
        # Quiz
        total += 1
        if st.session_state.get(f"quiz_{mk}_passed", False):
            done += 1
        # Checklist
        ct = get_checklist_count(mk)
        total += ct
        checks = st.session_state.get(f"checklist_{mk}", {})
        done += sum(1 for v in checks.values() if v)
    return done, total


# ═══════════════════════════════════════════════
# HOME PAGE
# ═══════════════════════════════════════════════
def show_home():
    name = st.session_state["emp_name"]
    first = name.split()[0] if name else "there"

    st.markdown(f"""
    <div class="welcome-banner">
        <h1>Welcome, {first}! 👋</h1>
        <p>We're glad to have you on the AAP team. Complete each training module below to finish your onboarding.</p>
    </div>
    """, unsafe_allow_html=True)

    # Progress
    done, total = calc_progress()
    pct = int((done / total) * 100) if total > 0 else 0
    st.markdown(f"""
    <div class="progress-container">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <strong style="color:#1e293b;">Onboarding Progress</strong>
            <span style="color:#3b82f6;font-weight:700;">{pct}%</span>
        </div>
        <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width:{pct}%;"></div>
        </div>
        <div style="color:#64748b;font-size:0.82rem;margin-top:6px;">{done} of {total} items completed</div>
    </div>
    """, unsafe_allow_html=True)

    # Module cards
    descriptions = {
        "welcome": "Learn about AAP's history, mission, vision, and guiding principles.",
        "conduct": "Understand AAP's expectations for ethical behavior and professional conduct.",
        "attendance": "Review PTO policies, the attendance point system, vacation and personal leave accruals.",
        "workplace": "Dress code, safety, drug & alcohol policy, computer use, harassment prevention, and more.",
        "benefits": "Explore health, dental, vision, 401(k), and supplemental benefits available to you.",
        "firststeps": "Your action items, system access, onboarding timeline, and 90-day roadmap."
    }

    cols = st.columns(2)
    for i, mk in enumerate(MODULE_KEYS):
        passed = st.session_state.get(f"quiz_{mk}_passed", False)
        checks = st.session_state.get(f"checklist_{mk}", {})
        ct = get_checklist_count(mk)
        done_c = sum(1 for v in checks.values() if v)
        complete = passed and done_c >= ct

        if complete:
            badge = '<span class="badge-complete">✅ Complete</span>'
        elif passed or done_c > 0:
            badge = '<span class="badge-incomplete">🔶 In Progress</span>'
        else:
            badge = '<span class="badge-locked">⬜ Not Started</span>'

        with cols[i % 2]:
            st.markdown(f"""
            <div class="module-card">
                <div style="display:flex;justify-content:space-between;align-items:start;">
                    <h3>{MODULE_ICONS[mk]} {MODULE_NAMES[mk]}</h3>
                    {badge}
                </div>
                <p>{descriptions[mk]}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Open Module →", key=f"open_{mk}", use_container_width=True):
                st.session_state["current_page"] = "module"
                st.session_state["current_module"] = mk
                st.rerun()


# ═══════════════════════════════════════════════
# QUIZ HELPER
# ═══════════════════════════════════════════════
def render_quiz(module_key, questions):
    """
    questions: list of dicts with keys: q, options, answer (index)
    """
    st.markdown("---")
    st.markdown("### 📝 Module Quiz")

    if st.session_state.get(f"quiz_{module_key}_passed", False):
        st.markdown('<div class="quiz-pass">✅ Quiz Passed! Great job.</div>', unsafe_allow_html=True)
        return

    st.markdown('<div class="quiz-section">', unsafe_allow_html=True)
    st.markdown("Answer all questions correctly to pass. You can retake as many times as needed.")

    answers = {}
    for i, q in enumerate(questions):
        answers[i] = st.radio(
            f"**Q{i+1}.** {q['q']}",
            options=q["options"],
            index=None,
            key=f"quiz_{module_key}_q{i}"
        )

    if st.button("Submit Quiz", key=f"submit_quiz_{module_key}", type="primary"):
        correct = 0
        for i, q in enumerate(questions):
            if answers[i] == q["options"][q["answer"]]:
                correct += 1
        if correct == len(questions):
            st.session_state[f"quiz_{module_key}_passed"] = True
            st.markdown('<div class="quiz-pass">🎉 You passed! All answers correct.</div>', unsafe_allow_html=True)
            st.rerun()
        else:
            st.markdown(f'<div class="quiz-fail">❌ {correct}/{len(questions)} correct. Review the material and try again.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# CHECKLIST HELPER
# ═══════════════════════════════════════════════
def render_checklist(module_key, items):
    """items: list of strings"""
    st.markdown("---")
    st.markdown("### ✅ Understanding Checklist")
    st.markdown('<div class="checklist-section">', unsafe_allow_html=True)
    st.markdown("Check each item to confirm your understanding:")

    checks = st.session_state.get(f"checklist_{module_key}", {})
    for i, item in enumerate(items):
        key = f"cl_{module_key}_{i}"
        val = st.checkbox(item, value=checks.get(key, False), key=key)
        checks[key] = val
    st.session_state[f"checklist_{module_key}"] = checks

    done = sum(1 for v in checks.values() if v)
    if done == len(items):
        st.success("All items confirmed!")
    else:
        st.info(f"{done}/{len(items)} confirmed")
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# MODULE 1: WELCOME TO AAP
# ═══════════════════════════════════════════════
def module_welcome():
    st.markdown(f"""
    <div class="section-header">
        <h2>🏢 Welcome to AAP</h2>
        <p>Company History, Mission, Vision & Guiding Principles</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Who We Are")
    st.markdown("""
    American Associated Pharmacies (AAP) is a national cooperative of more than **2,000 independent pharmacies**. 
    AAP was formed in 2009 when two major pharmacy cooperatives — **United Drugs** of Phoenix, Arizona and 
    **Associated Pharmacies, Inc. (API)** of Scottsboro, Alabama — joined forces to create one of America's largest 
    independent pharmacy organizations.

    Today, AAP continues to operate API, its independent warehouse and distributor, with two warehouse locations 
    in the U.S. Along with its subsidiaries, AAP provides member-focused support and serves as a collaborative 
    professional advocate, bringing innovative and cost-saving programs to its member pharmacies.
    """)

    st.markdown('<div class="info-box"><strong>Key Fact:</strong> With its competitive Prime Vendor Agreement with a national wholesaler, AAP saves its member pharmacies millions in operating and acquisition costs each year.</div>', unsafe_allow_html=True)

    st.markdown("## Our Mission")
    st.markdown("""
    AAP provides support and customized solutions for independent community pharmacies to enhance their 
    profitability, streamline their operations, and improve the quality of patient care.
    """)

    st.markdown("## Our Vision")
    st.markdown("*Helping independent pharmacies thrive in a competitive healthcare market.*")

    st.markdown("## Our Values & Guiding Principles")
    st.markdown("""
    Our values guide every decision, discussion, and behavior. It's not only *what* we do that matters, but *how* we do it.
    """)

    val_cols = st.columns(5)
    values = [
        ("🎯", "Customer Focus", "Our primary focus is meeting customer requirements and striving to exceed expectations. Customer service is not just a department — it's an attitude."),
        ("⚖️", "Integrity", "We act with honesty and integrity without compromising the truth. We maintain consistency in what we say and do to build trust."),
        ("🤝", "Respect", "We treat others with the same dignity we wish to receive. We recognize the power of teamwork and encourage open, honest communication."),
        ("⭐", "Excellence", "We strive for the highest quality in everything we do. We seek and pursue opportunities for continuous improvement and innovation."),
        ("🔑", "Ownership", "We seek responsibility and hold ourselves accountable for our actions. When things go wrong, we take responsibility.")
    ]
    for col, (icon, title, desc) in zip(val_cols, values):
        with col:
            st.markdown(f"**{icon} {title}**")
            st.caption(desc)

    # Quiz
    questions = [
        {"q": "When was AAP formed?", "options": ["2001", "2005", "2009", "2012"], "answer": 2},
        {"q": "AAP is a national cooperative of approximately how many independent pharmacies?", "options": ["500", "1,000", "2,000", "5,000"], "answer": 2},
        {"q": "Which of the following is NOT one of AAP's five core values?", "options": ["Customer Focus", "Integrity", "Profitability", "Ownership"], "answer": 2},
        {"q": "What is AAP's vision?", "options": [
            "To be the largest pharmacy in the world",
            "Helping independent pharmacies thrive in a competitive healthcare market",
            "Maximizing shareholder returns",
            "Providing the cheapest prescriptions"
        ], "answer": 1},
    ]
    render_quiz("welcome", questions)

    # Checklist
    items = [
        "I understand AAP's history and how it was formed.",
        "I can identify AAP's mission and vision statements.",
        "I understand the five core values: Customer Focus, Integrity, Respect, Excellence, and Ownership.",
        "I understand that AAP is a cooperative serving independent pharmacies."
    ]
    render_checklist("welcome", items)


# ═══════════════════════════════════════════════
# MODULE 2: CODE OF CONDUCT & ETHICS
# ═══════════════════════════════════════════════
def module_conduct():
    st.markdown("""
    <div class="section-header">
        <h2>📋 Code of Conduct & Ethics</h2>
        <p>Professional Standards, Ethical Behavior & Workplace Expectations</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Business Ethics and Conduct")
    st.markdown("""
    The success of AAP depends on our customers' trust, and we are dedicated to preserving that trust. Every employee 
    owes a duty to AAP, its customers, and shareholders to act in a way that merits continued public confidence.

    AAP complies with all applicable laws and regulations and expects its directors, officers, and employees to conduct 
    business in accordance with the letter, spirit, and intent of all relevant laws — and to refrain from any illegal, dishonest, 
    or unethical conduct. Failure to comply can lead to disciplinary action, up to and including termination.
    """)

    st.markdown("## Key Conduct Expectations")

    tab1, tab2, tab3, tab4 = st.tabs(["Conflicts of Interest", "Confidentiality", "Outside Employment", "Equal Opportunity"])

    with tab1:
        st.markdown("""
        Employees must conduct business within guidelines that prohibit actual or potential conflicts of interest. 
        If you have questions, contact the HR department.
        """)

    with tab2:
        st.markdown("""
        All employees sign a **confidentiality and non-disclosure agreement** upon hire. Refusal is grounds for 
        immediate termination. Confidential information must only be shared on a need-to-know basis. Personnel files 
        are company property with restricted access.
        """)

    with tab3:
        st.markdown("""
        You may hold a job with another organization as long as you satisfactorily perform your AAP responsibilities. 
        If outside work interferes with performance or presents a conflict, you may be asked to choose. All employees 
        are held to the same performance standards regardless of outside work.
        """)

    with tab4:
        st.markdown("""
        Employment decisions are based on merit, qualifications, and abilities. AAP does not discriminate on the basis 
        of race, color, religion, sex, national origin, age, disability, or any other characteristic protected by law. 
        Report discrimination concerns to your supervisor or HR without fear of reprisal.
        """)

    st.markdown("## Immigration & Hiring")
    st.markdown("""
    All employees must be authorized to work in the United States. AAP uses **E-Verify** to confirm work authorization. 
    A background check will be conducted for all applicants.
    """)

    st.markdown("## Problem Resolution")
    st.markdown("""
    AAP encourages open and fair resolution of work-related concerns. If you believe a condition of employment or 
    decision is unjust, follow these steps:

    1. Present the concern to your immediate supervisor (or HR if the supervisor is unavailable or inappropriate).
    2. If unresolved, escalate to the next level of management (VP → President → CEO).
    3. The CEO has full authority to make appropriate adjustments.
    4. If still unresolved, the Board of Directors may review the concern.

    No employee will be penalized for voicing a complaint in a reasonable and professional manner.
    """)

    # Quiz
    questions = [
        {"q": "What must all employees sign upon hire?", "options": [
            "A non-compete agreement",
            "A confidentiality and non-disclosure agreement",
            "A social media policy",
            "A union membership form"
        ], "answer": 1},
        {"q": "What system does AAP use to verify work authorization?", "options": [
            "HIPAA", "E-Verify", "ADP Screening", "LinkedIn"
        ], "answer": 1},
        {"q": "If you have a workplace concern, who should you approach first?", "options": [
            "The CEO directly",
            "A coworker",
            "Your immediate supervisor or HR",
            "An outside attorney"
        ], "answer": 2},
        {"q": "Outside employment is permitted as long as:", "options": [
            "You work fewer than 20 hours elsewhere",
            "You satisfactorily perform your AAP responsibilities",
            "Your manager gives verbal approval",
            "It is in a different industry"
        ], "answer": 1},
    ]
    render_quiz("conduct", questions)

    items = [
        "I understand AAP's business ethics expectations and my responsibility to uphold them.",
        "I understand the confidentiality and non-disclosure requirements.",
        "I know the problem resolution steps if I have a workplace concern.",
        "I understand AAP's equal employment opportunity policy."
    ]
    render_checklist("conduct", items)


# ═══════════════════════════════════════════════
# MODULE 3: ATTENDANCE & PTO
# ═══════════════════════════════════════════════
def module_attendance():
    st.markdown("""
    <div class="section-header">
        <h2>⏰ Attendance & PTO Policies</h2>
        <p>Vacation, Personal Leave, Holidays & the Attendance Point System</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Vacation Benefits")
    st.markdown("*Available to regular full-time employees. Must complete 60 days of service. Vacation may be taken in minimum increments of **2 hours**.*")

    st.markdown("""
    <table class="styled-table">
        <tr><th>Length of Employment</th><th>Paid Days/Year</th><th>Accrual Rate</th></tr>
        <tr><td>60 days – 1st Anniversary</td><td>3 days (24 hrs)</td><td>0.46 hrs/week</td></tr>
        <tr><td>1st – 2nd Anniversary</td><td>5 days (40 hrs)</td><td>0.77 hrs/week</td></tr>
        <tr><td>2nd – 3rd Anniversary</td><td>7 days (56 hrs)</td><td>1.07 hrs/week</td></tr>
        <tr><td>3rd – 5th Anniversary</td><td>10 days (80 hrs)</td><td>1.54 hrs/week</td></tr>
        <tr><td>5th – 9th Anniversary</td><td>15 days (120 hrs)</td><td>2.31 hrs/week</td></tr>
        <tr><td>10th – 19th Anniversary</td><td>17 days (136 hrs)</td><td>2.62 hrs/week</td></tr>
        <tr><td>20th Anniversary+</td><td>19 days (152 hrs)</td><td>2.93 hrs/week</td></tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
    <strong>Key Rules:</strong> Vacation cannot be taken before it is accrued. More than 5 consecutive days requires written approval from the 
    Company President. Accrued but unused vacation may be banked up to 19 days (152 hours) max. Unused vacation is paid out at termination.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Personal Leave")
    st.markdown("*Available to all employees. May be taken in minimum increments of **1 hour**. 60-day waiting period before use.*")

    st.markdown("""
    **Full-time employees:**
    - Upon eligibility: 3 personal days (24 hours)
    - After 1 year: 4 personal days (32 hours)
    - After 5 years: 5 personal days (40 hours)

    **Part-time employees:**
    - Earn 1 hour per 30 hours worked, same tier caps apply

    ⚠️ Unused personal leave is **forfeited** at end of benefit year (unless state law requires carryover). Not paid out at termination.
    """)

    st.markdown("## Holiday Schedule")
    holidays = [
        "New Year's Day (January 1)", "Memorial Day (last Monday in May)",
        "Independence Day (July 4)", "Labor Day (first Monday in September)",
        "Thanksgiving (fourth Thursday in November)",
        "Day after Thanksgiving *or* Floating Holiday",
        "Christmas Eve *or* Floating Holiday", "Christmas Day (December 25)"
    ]
    for h in holidays:
        st.markdown(f"- 🗓️ {h}")

    st.markdown("""
    <div class="info-box">
    <strong>Observed Holidays:</strong> Saturday holidays are observed the preceding Friday; Sunday holidays are observed the following Monday. 
    If you work on a designated holiday, you receive a floating holiday to use within 90 days.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Attendance Point System")
    st.markdown("AAP uses a **no-fault** point system for non-exempt employees. Points accumulate regardless of the reason for absence (with specific exclusions like FMLA, pre-approved vacation, jury duty, etc.).")

    st.markdown("""
    <table class="styled-table">
        <tr><th>Reason</th><th>Points</th></tr>
        <tr><td>Tardy up to 5 minutes (grace period)</td><td>0</td></tr>
        <tr><td>Tardy or early leave (less than 4 hours)</td><td>½</td></tr>
        <tr><td>Full shift absence, tardy or early leave (4+ hours)</td><td>1</td></tr>
        <tr><td>Absence — no report or call 15+ min after start</td><td>1½</td></tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("### Corrective Action Schedule")
    st.markdown("""
    <table class="styled-table">
        <tr><th>Points (in 12 months)</th><th>Action</th></tr>
        <tr><td>5 points</td><td>Coaching Session</td></tr>
        <tr><td>6 points</td><td>Verbal Warning</td></tr>
        <tr><td>7 points</td><td>Written Warning</td></tr>
        <tr><td>8 points</td><td>Termination</td></tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
    <strong>Good News:</strong> Employees can have 1 point removed for 2 consecutive months of perfect attendance. 
    Three consecutive months of perfect attendance earns a <strong>$75 bonus</strong>!
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Two consecutive days absent without reporting in = voluntary resignation.**")

    # Quiz
    questions = [
        {"q": "What is the minimum increment for taking vacation time?", "options": ["1 hour", "2 hours", "4 hours", "8 hours"], "answer": 1},
        {"q": "What is the minimum increment for personal leave?", "options": ["1 hour", "2 hours", "4 hours", "8 hours"], "answer": 0},
        {"q": "How many points does a no-call/no-show absence (15+ min after start) carry?", "options": ["½ point", "1 point", "1½ points", "2 points"], "answer": 2},
        {"q": "At how many points does termination occur?", "options": ["6", "7", "8", "10"], "answer": 2},
        {"q": "How many consecutive days absent without reporting results in voluntary resignation?", "options": ["1", "2", "3", "5"], "answer": 1},
    ]
    render_quiz("attendance", questions)

    items = [
        "I understand the vacation accrual schedule and the 2-hour minimum increment.",
        "I understand personal leave accrues separately and has a 1-hour minimum increment.",
        "I know the 8 company holidays and the floating holiday rules.",
        "I understand the attendance point system and corrective action thresholds.",
        "I understand that 2 consecutive no-call/no-show days is considered voluntary resignation."
    ]
    render_checklist("attendance", items)


# ═══════════════════════════════════════════════
# MODULE 4: WORKPLACE POLICIES
# ═══════════════════════════════════════════════
def module_workplace():
    st.markdown("""
    <div class="section-header">
        <h2>🏗️ Workplace Policies</h2>
        <p>Safety, Dress Code, Drug & Alcohol, Technology, Harassment & More</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Dress Code", "Safety", "Drug & Alcohol",
        "Computer & Email", "Harassment Prevention", "Other Policies"
    ])

    with tab1:
        st.markdown("## Personal Appearance")
        st.markdown("""
        Dress requirements vary by department. However, these rules always apply:
        - A **neat, clean, and well-groomed** appearance is required for all employees.
        - Clothes must be work-appropriate — nothing too revealing or inappropriate.
        - Avoid clothing with offensive or inappropriate stamps/messages.
        - Due to allergies/asthma among staff, avoid **offensive odors, perfumes, or heavily scented products**.

        If you are out of compliance, your supervisor will ask you to clock out and return when dressed appropriately.
        """)

    with tab2:
        st.markdown("## Workplace Safety")
        st.markdown("""
        The VP of Human Resources oversees the safety program. Key expectations:
        - Obey all safety rules and exercise caution in all work activities.
        - **Immediately report** any unsafe condition to your supervisor.
        - **Immediately report** any work-related injury to HR or your supervisor, no matter how minor.
        - All work-related accidents require **immediate alcohol and drug testing**.
        - Violating safety standards may result in disciplinary action, up to and including termination.
        """)

    with tab3:
        st.markdown("## Drug & Alcohol Policy")
        st.markdown("""
        AAP maintains a **drug and alcohol-free** work environment.
        - Being under the influence of drugs or alcohol on the job is **strictly prohibited**.
        - Employees may be subject to **random drug testing** at any time.
        - Violations may lead to disciplinary action up to and including **immediate termination**.
        - The Employee Assistance Program (EAP) is available for employees needing support.
        """)

    with tab4:
        st.markdown("## Computer & Email Usage")
        st.markdown("""
        Computers, files, email, and software are **AAP property** intended for business use.
        - Do not use passwords, access files, or retrieve stored communications without authorization.
        - **Usage may be monitored.**
        - Prohibited uses include: sexually explicit content, ethnic slurs, racial comments, off-color jokes, or anything construed as harassment.
        - Do not illegally duplicate software.
        - Violations result in disciplinary action, up to and including termination.
        """)

    with tab5:
        st.markdown("## Sexual & Unlawful Harassment Prevention")
        st.markdown("""
        AAP is committed to a work environment **free of discrimination and unlawful harassment**. 
        Sexual harassment in any form is strictly prohibited — including offensive comments, unwanted advances, 
        inappropriate touching, or implied threats related to job status.

        **If you experience or witness harassment:**
        1. Tell the offender their conduct is offensive and must stop (if you feel comfortable).
        2. Report to your supervisor or HR department.
        3. If your supervisor is the issue, contact the VP of Human Resources.

        ⚠️ **No retaliation** will occur for good-faith complaints. Violators face disciplinary action up to and including termination.
        """)

    with tab6:
        st.markdown("## Work Schedules & Overtime")
        st.markdown("""
        Schedules vary by department. Overtime must receive **prior supervisor approval**. Non-exempt employees receive 
        overtime pay per federal/state law. Failure to work scheduled overtime or unauthorized overtime may result in 
        disciplinary action.
        """)

        st.markdown("## Business Travel & Expenses")
        st.markdown("AAP reimburses reasonable business travel expenses. Falsifying expense reports is grounds for termination.")

        st.markdown("## Workplace Violence Prevention")
        st.markdown("""
        AAP has **zero tolerance** for workplace violence — including verbal/physical harassment, threats, assaults, 
        bullying, or any behavior causing others to feel unsafe. All incidents must be reported within 24 hours.
        """)

    # Quiz
    questions = [
        {"q": "What happens after a work-related accident?", "options": [
            "Nothing unless someone is injured",
            "An incident report is filed only",
            "Immediate alcohol and drug testing of those involved",
            "The employee goes home for the day"
        ], "answer": 2},
        {"q": "AAP's computer and email systems are:", "options": [
            "Personal property of the employee",
            "Company property intended for business use and may be monitored",
            "Freely available for personal use during work hours",
            "Only monitored during investigations"
        ], "answer": 1},
        {"q": "What is the first step if you experience harassment?", "options": [
            "Post about it on social media",
            "Ignore it and hope it stops",
            "Tell the offender to stop (if comfortable) or report to supervisor/HR",
            "Confront the person publicly"
        ], "answer": 2},
        {"q": "Overtime must be:", "options": [
            "Approved by a coworker",
            "Approved by your supervisor in advance",
            "Reported after the fact",
            "Self-authorized if needed"
        ], "answer": 1},
    ]
    render_quiz("workplace", questions)

    items = [
        "I understand the dress code expectations and the consequences of non-compliance.",
        "I understand the safety reporting requirements and my responsibilities.",
        "I understand the drug and alcohol policy, including random testing.",
        "I understand that computer/email usage is monitored and subject to company policy.",
        "I know how to report harassment and understand the no-retaliation policy."
    ]
    render_checklist("workplace", items)


# ═══════════════════════════════════════════════
# MODULE 5: BENEFITS
# ═══════════════════════════════════════════════
def module_benefits():
    st.markdown("""
    <div class="section-header">
        <h2>🩺 Benefits Overview</h2>
        <p>Health, Dental, Vision, Retirement, and Supplemental Benefits</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
    <strong>Eligibility:</strong> New full-time employees (30+ hours/week) must enroll within 30 days of hire. 
    Benefits become effective the <strong>1st of the month following 60 days</strong> of employment. 
    Dependents up to age 26 can be covered.
    </div>
    """, unsafe_allow_html=True)

    ft_tab, pt_tab = st.tabs(["🏢 Full-Time Benefits", "⏱️ Part-Time & All Employee Benefits"])

    with ft_tab:
        st.markdown("## Medical Insurance (BlueCross BlueShield of Alabama)")
        st.markdown("Choose between two plans:")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Option 1: PPO Plan")
            st.markdown("""
            | Tier | Monthly Cost |
            |---|---|
            | Employee | $157.20 |
            | Employee + Spouse | $492.32 |
            | Employee + Child(ren) | $444.36 |
            | Employee + Family | $678.62 |

            **Deductible:** $500 individual / $1,000 family  
            **Coinsurance:** 20%  
            **Out-of-Pocket Max:** $2,250 / $4,500  
            **PCP/Specialist:** $30 / $45 copay  
            **Rx:** $10 generic / $30 preferred / $50 non-preferred
            """)

        with col2:
            st.markdown("### Option 2: HDHP with HSA")
            st.markdown("""
            | Tier | Monthly Cost |
            |---|---|
            | Employee | $136.34 |
            | Employee + Spouse | $404.66 |
            | Employee + Child(ren) | $373.04 |
            | Employee + Family | $581.72 |

            **Deductible:** $1,700 / $3,400  
            **Coinsurance:** 10%  
            **Out-of-Pocket Max:** $3,400 / $6,800  
            **Company HSA Contribution:** $900 / $1,800 per year  
            **HSA Limits (2026):** $4,400 single / $8,750 family
            """)

        st.markdown("## Dental Insurance (Guardian)")
        st.markdown("""
        | | Base Plan | High Plan |
        |---|---|---|
        | Employee | $6.78/mo | $10.66/mo |
        | Employee + Spouse | $20.56/mo | $28.80/mo |
        | Employee + Child(ren) | $20.76/mo | $28.32/mo |
        | Employee + Family | $34.54/mo | $47.10/mo |

        **Preventive (Coverage A):** 100% both plans  
        **Basic (Coverage B):** 80% Base / 100% High  
        **Major (Coverage C):** 50% both plans (12-month waiting period)  
        **Annual Max:** $1,500 (Base) / $3,000 (High)
        """)

        st.markdown("## Vision Insurance (Guardian / Davis Vision)")
        st.markdown("""
        | Tier | Monthly Cost |
        |---|---|
        | Employee | $6.93 |
        | Employee + 1 Dependent | $10.04 |
        | Employee + Family | $18.00 |

        Exams and lenses every 12 months. Frames every 24 months. $130 frame allowance.
        """)

        st.markdown("## Life & Disability")
        st.markdown("""
        - **Basic Life & AD&D:** Provided at **no cost** — equal to your annual earnings up to $270,000 (through Guardian).
        - **Voluntary Life:** Available from $10,000 to 5x salary (max $500,000). Guarantee issue up to $100,000 during initial enrollment.
        - **Short-Term Disability:** 60% of weekly earnings, max $1,250/week. 7-day elimination period. Up to 12 weeks. Employee-paid.
        - **Long-Term Disability:** 60% of monthly earnings, max $10,000/month. 90-day waiting period. **Company-paid.**
        """)

        st.markdown("## Supplemental Coverage (Guardian)")
        st.markdown("""
        - **Accident Insurance:** Employee $14.55/mo, Family $35.35/mo. No EOI required.
        - **Cancer Insurance:** Employee $21.28/mo, Family $45.41/mo. Health questions required.
        - **Critical Illness:** Benefit amounts from $5,000–$20,000. Rates vary by age.
        """)

        st.markdown("## 401(k) Savings Plan")
        st.markdown("""
        Available the **1st of the month following 60 days** of employment.

        **Company Match:** 100% of the first 3% you contribute + 50% of the next 2% = **4% match if you contribute 5%**.  
        Company match is **100% vested immediately**.
        """)

    with pt_tab:
        st.markdown("## Benefits Available to ALL Employees")
        st.markdown("The following benefits are available to both full-time and part-time employees at **no cost**:")

        st.markdown("### 📱 Teladoc (Telehealth)")
        st.markdown("""
        **Free** for all employees — paid for by AAP! See a doctor from your phone or computer 24/7 without an appointment. 
        Covers general medical, mental health, and therapy services. Call 1-800-TELADOC or visit teladoc.com.
        """)

        st.markdown("### 🧠 LifeMatters EAP (Employee Assistance Program)")
        st.markdown("""
        **Free, confidential** counseling and support for stress, depression, family concerns, legal/financial consultation, 
        substance dependency, and more. Available 24/7 at **1-800-634-6433** or mylifematters.com (password: AAP1).
        """)

        st.markdown("### 📚 LinkedIn Learning")
        st.markdown("All employees receive access to LinkedIn Learning's full course library for professional development.")

        st.markdown("### 🎁 AAP BenefitHub Employee Perks")
        st.markdown("""
        Discounts on travel, electronics, apparel, entertainment, restaurants, auto, and more through BenefitHub. 
        Register at **aapperks.benefithub.com** with referral code **9Y7G26**.
        """)

        st.markdown("### 🕐 Personal Time Off")
        st.markdown("All employees (full-time and part-time) earn personal leave. See the Attendance & PTO module for details.")

    # Quiz
    questions = [
        {"q": "When do benefits become effective for new full-time employees?", "options": [
            "Immediately on Day 1",
            "After 30 days",
            "1st of the month following 60 days of employment",
            "After 90 days"
        ], "answer": 2},
        {"q": "What is the company's 401(k) match if you contribute 5% of your salary?", "options": ["2%", "3%", "4%", "5%"], "answer": 2},
        {"q": "Which benefit is provided at NO cost to ALL employees?", "options": [
            "Dental insurance",
            "Short-term disability",
            "Teladoc telehealth",
            "Vision insurance"
        ], "answer": 2},
        {"q": "Basic Life and AD&D coverage is provided by AAP at:", "options": [
            "50% employer-paid",
            "No cost to the employee",
            "Employee-paid through payroll deduction",
            "Only if you enroll during open enrollment"
        ], "answer": 1},
    ]
    render_quiz("benefits", questions)

    items = [
        "I understand the two medical plan options (PPO vs. HDHP/HSA) and their cost differences.",
        "I know the 401(k) match structure and when I become eligible.",
        "I understand which benefits are available to all employees at no cost (Teladoc, EAP, LinkedIn Learning, BenefitHub).",
        "I know that benefits enrollment must happen within 30 days of hire.",
        "I understand supplemental coverage options like accident, cancer, and critical illness insurance."
    ]
    render_checklist("benefits", items)


# ═══════════════════════════════════════════════
# MODULE 6: FIRST STEPS
# ═══════════════════════════════════════════════
def module_firststeps():
    st.markdown("""
    <div class="section-header">
        <h2>🚀 First Steps</h2>
        <p>Your Action Items, System Access & 90-Day Roadmap</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Getting Started — Action Items")
    st.markdown("Complete these tasks as soon as possible to ensure a smooth start:")

    actions = [
        ("✅", "Verify Account Access", "Confirm you can access your AAP email, systems, and internal tools."),
        ("📝", "Sign All New Hire Documents", "Ensure your onboarding packet in BambooHR is fully completed and all documents are signed."),
        ("📚", "Activate LinkedIn Learning", 'Go to **https://linkedin.com/learning** and log in with your company email to activate your account.'),
        ("📄", "Provide I-9 Documents", "Bring your I-9 identification documents (e.g., passport, driver's license + Social Security card) to HR within 3 business days of your start date."),
        ("💰", "Register for Paylocity", "Set up your Paylocity account for payroll, pay stubs, and tax documents."),
        ("📱", "Download BambooHR App", "Download the BambooHR app on your mobile device and log in with your credentials to access your employee profile, time off, and documents."),
    ]
    for icon, title, desc in actions:
        st.markdown(f"**{icon} {title}**")
        st.markdown(f"> {desc}")

    st.markdown("---")
    st.markdown("## Your 90-Day Onboarding Timeline")

    st.markdown("""
    <div class="timeline-item">
        <h4 style="margin:0 0 4px 0;color:#1e293b;">📅 Days 1–30: Orientation & Foundation</h4>
        <ul style="color:#475569;margin:4px 0;">
            <li>Complete orientation and all onboarding training modules</li>
            <li>Sign all required paperwork and provide I-9 documentation</li>
            <li>Get access to all necessary systems and tools</li>
            <li>Meet your team and key contacts across departments</li>
            <li>Shadow key processes and learn day-to-day workflows</li>
            <li>Complete the <strong>30-Day Survey</strong></li>
        </ul>
    </div>
    <div class="timeline-item">
        <h4 style="margin:0 0 4px 0;color:#1e293b;">📅 Days 31–60: Building Independence</h4>
        <ul style="color:#475569;margin:4px 0;">
            <li>Begin independently executing core job responsibilities</li>
            <li>Complete the <strong>60-Day Survey</strong></li>
            <li>Become eligible for <strong>PTO and holiday pay</strong> (after 60 days)</li>
            <li><strong>End of probationary period</strong></li>
            <li>Set a personal goal for the next 30 days and inform your supervisor</li>
        </ul>
    </div>
    <div class="timeline-item">
        <h4 style="margin:0 0 4px 0;color:#1e293b;">📅 Days 61–90: Growth & Review</h4>
        <ul style="color:#475569;margin:4px 0;">
            <li>Build confidence and consistency in your role</li>
            <li>Identify opportunities for improvement or professional development</li>
            <li>Have your <strong>first performance review</strong></li>
            <li><strong>Benefit eligibility</strong> — full benefits become effective (1st of month after 60 days)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## Key Contacts")
    st.markdown("""
    | Contact | Role | Phone | Email |
    |---|---|---|---|
    | Nicole Thornton | HR Manager | 256-574-7528 | nicole.thornton@apirx.com |
    | Brandy Hooper | VP of Human Resources | 256-574-7526 | brandy.hooper@rxaap.com |
    """)

    # Quiz
    questions = [
        {"q": "Within how many business days must you provide I-9 documents?", "options": ["1 day", "3 days", "5 days", "10 days"], "answer": 1},
        {"q": "When does the probationary period end?", "options": ["30 days", "60 days", "90 days", "120 days"], "answer": 1},
        {"q": "When do you become eligible for PTO and holiday pay?", "options": [
            "Day 1", "After 30 days", "After 60 days", "After 90 days"
        ], "answer": 2},
        {"q": "What app should you download for accessing your employee profile and time off?", "options": [
            "Workday", "BambooHR", "ADP", "Gusto"
        ], "answer": 1},
    ]
    render_quiz("firststeps", questions)

    items = [
        "I know to verify my account access and sign all onboarding documents.",
        "I will activate my LinkedIn Learning account using my company email.",
        "I understand I must provide I-9 documents within 3 business days.",
        "I will register for Paylocity and download the BambooHR app.",
        "I understand the 90-day onboarding timeline and milestone expectations.",
        "I know who to contact in HR if I have questions."
    ]
    render_checklist("firststeps", items)


# ═══════════════════════════════════════════════
# MODULE ROUTER
# ═══════════════════════════════════════════════
MODULE_FUNCTIONS = {
    "welcome": module_welcome,
    "conduct": module_conduct,
    "attendance": module_attendance,
    "workplace": module_workplace,
    "benefits": module_benefits,
    "firststeps": module_firststeps,
}

def show_module(mk):
    # Back button
    if st.button("← Back to Home", key="back_home"):
        st.session_state["current_page"] = "home"
        st.session_state["current_module"] = None
        st.rerun()

    MODULE_FUNCTIONS[mk]()

    # Navigation at bottom
    st.markdown("---")
    idx = MODULE_KEYS.index(mk)
    col1, col2 = st.columns(2)
    if idx > 0:
        prev_mk = MODULE_KEYS[idx - 1]
        with col1:
            if st.button(f"← {MODULE_NAMES[prev_mk]}", key="prev_mod"):
                st.session_state["current_module"] = prev_mk
                st.rerun()
    if idx < len(MODULE_KEYS) - 1:
        next_mk = MODULE_KEYS[idx + 1]
        with col2:
            if st.button(f"{MODULE_NAMES[next_mk]} →", key="next_mod"):
                st.session_state["current_module"] = next_mk
                st.rerun()


# ═══════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════
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
