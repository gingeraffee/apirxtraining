import streamlit as st
import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AAP New Hire Orientation",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

    /* ── Base ── */
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #EEF2F7; }

    /* ── Sidebar Container ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A1628 0%, #12213A 50%, #1B3A5C 100%);
        border-right: 2px solid #CC2936;
        box-shadow: 4px 0 24px rgba(0,0,0,0.4);
    }

    /* ── Sidebar Header — bright white card so logo stands out ── */
    .sidebar-header {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 16px 14px 14px 14px;
        margin-bottom: 18px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.25);
    }
    .sidebar-header * { color: #0A1628 !important; }
    .sidebar-header .sidebar-username {
        color: #CC2936 !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
    }

    /* ── Sidebar Navigation — explicit white text so nothing disappears ── */
    [data-testid="stSidebar"] .stRadio label {
        color: rgba(255,255,255,0.88) !important;
        border-radius: 8px !important;
        padding: 7px 10px !important;
        transition: all 0.15s ease !important;
        font-size: 0.9rem !important;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(204,41,54,0.22) !important;
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] .stRadio p,
    [data-testid="stSidebar"] .stRadio span {
        color: rgba(255,255,255,0.88) !important;
    }

    /* ── Typography ── */
    h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #0A1628 !important; }
    .page-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #0A1628;
        border-bottom: 3px solid #CC2936;
        padding-bottom: 12px;
        margin-bottom: 8px;
    }
    .page-subtitle { color: #5A6E8A; font-size: 1.05rem; margin-bottom: 28px; font-weight: 400; }

    /* ── Module Cards ── */
    .module-card {
        background: white;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 16px;
        border-left: 5px solid #CC2936;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .module-card:hover { transform: translateY(-2px); box-shadow: 0 5px 18px rgba(0,0,0,0.11); }
    .module-card.complete { border-left-color: #1A9E5C; background: #F0FFF6; }

    /* ── Progress Bars ── */
    .stProgress > div > div { background-color: #CC2936 !important; }

    /* ── Primary Buttons — deep navy, red on hover ── */
    .stButton > button[kind="primary"],
    .stButton > button[kind="primary"][data-testid],
    [data-testid="stBaseButton-primary"] {
        background-color: #0A1628 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 20px !important;
        font-weight: 500 !important;
        letter-spacing: 0.02em !important;
        transition: background 0.2s ease !important;
    }
    .stButton > button[kind="primary"]:hover,
    [data-testid="stBaseButton-primary"]:hover {
        background-color: #CC2936 !important;
    }

    /* ── Secondary Buttons — red underline link ── */
    .stButton > button[kind="secondary"],
    [data-testid="stBaseButton-secondary"] {
        background: none !important;
        border: none !important;
        color: #CC2936 !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        padding: 0 4px !important;
        height: auto !important;
        min-height: 0 !important;
        box-shadow: none !important;
        text-decoration: underline !important;
        text-underline-offset: 3px !important;
    }
    .stButton > button[kind="secondary"]:hover,
    [data-testid="stBaseButton-secondary"]:hover {
        background: none !important;
        color: #A01E27 !important;
        box-shadow: none !important;
    }

    /* ── Badges ── */
    .badge {
        display: inline-block;
        background: #CC2936;
        color: white;
        font-size: 0.74rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 20px;
        margin-left: 8px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge.done { background: #1A9E5C; }

    /* ── Welcome Banner ── */
    .welcome-banner {
        background: linear-gradient(135deg, #0A1628 0%, #1B3A5C 100%);
        border-radius: 16px;
        padding: 32px 36px;
        margin-bottom: 28px;
        border-left: 6px solid #CC2936;
    }
    .welcome-banner h1 { color: white !important; font-family: 'Playfair Display', serif; font-size: 2rem; margin-bottom: 8px; }
    .welcome-banner p { color: #B0C4D8; font-size: 1.05rem; }

    /* ── Callout ── */
    .callout { background: #FEF2F3; border-left: 4px solid #CC2936; border-radius: 0 8px 8px 0; padding: 14px 18px; margin: 16px 0; color: #6B0E16; }

    /* ── Dividers ── */
    hr { border: none; border-top: 1px solid #D8E1EB; margin: 24px 0; }

    /* ── Resource Library ── */
    .resource-card {
        background: white;
        border-radius: 8px;
        padding: 13px 16px;
        margin-bottom: 7px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
        border-left: 3px solid transparent;
        transition: border-color 0.15s ease, box-shadow 0.15s ease, transform 0.12s ease;
    }
    .resource-card:hover {
        border-left-color: #0A1628;
        box-shadow: 0 3px 12px rgba(0,0,0,0.10);
        transform: translateX(3px);
    }
    .resource-id {
        display: inline-block;
        background: #0A1628;
        color: white;
        font-size: 0.68rem;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 6px;
        white-space: nowrap;
        margin-top: 3px;
        letter-spacing: 0.03em;
        min-width: 54px;
        text-align: center;
        flex-shrink: 0;
    }
    /* ─────────────────────────────────────────────────────────────
       Mobile + Dark Mode Compatibility Patch
       (keeps desktop exactly the same)
       ───────────────────────────────────────────────────────────── */
    @media (max-width: 768px) and (prefers-color-scheme: dark) {

      /* App background + default text */
      div[data-testid="stAppViewContainer"],
      section.main,
      .stApp {
        background: #0B1220 !important;
        color: #F9FAFB !important;
      }

      /* Streamlit markdown text */
      div[data-testid="stMarkdownContainer"],
      div[data-testid="stMarkdownContainer"] p,
      div[data-testid="stMarkdownContainer"] li,
      div[data-testid="stMarkdownContainer"] span,
      div[data-testid="stMarkdownContainer"] div {
        color: #F9FAFB !important;
      }

      /* Your custom headings/subtitles (you use these a lot) */
      .page-title,
      .page-subtitle {
        color: #F9FAFB !important;
      }

      /* Cards you set to white in light mode */
      .resource-card,
      .module-card,
      .welcome-banner + div,
      div[style*="background:white"],
      div[style*="background: white"] {
        background: #111827 !important;
        border-color: rgba(255,255,255,0.10) !important;
      }

      /* Override your common “dark ink” inline colors */
      div[style*="color:#0A1628"],
      div[style*="color: #0A1628"],
      span[style*="color:#0A1628"],
      span[style*="color: #0A1628"] {
        color: #F9FAFB !important;
      }

      /* Override your muted slate inline color */
      div[style*="color:#5A6E8A"],
      div[style*="color: #5A6E8A"],
      span[style*="color:#5A6E8A"],
      span[style*="color: #5A6E8A"] {
        color: #CBD5E1 !important;
      }

      /* Inputs (you also set these explicitly on Downloads page) */
      div[data-testid="stTextInput"] input {
        background: #0F172A !important;
        color: #F9FAFB !important;
        border-color: rgba(255,255,255,0.18) !important;
      }
      div[data-testid="stTextInput"] input::placeholder {
        color: rgba(255,255,255,0.55) !important;
      }

      /* Tables you render with dark headers + light bodies */
      table, td, th {
        color: #E5E7EB !important;
        border-color: rgba(255,255,255,0.12) !important;
      }
    }
    </style>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  GOOGLE SHEETS INTEGRATION
# ─────────────────────────────────────────────
@st.cache_resource
def get_gsheet_client():
    try:
        creds_dict = dict(st.secrets["gcp_service_account"])
        scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        return gspread.authorize(creds)
    except Exception:
        return None

def get_sheet(client):
    try:
        return client.open("AAP New Hire Orientation Progress").sheet1
    except Exception:
        return None

def save_progress(username, module_key, pct, checklist_items, quiz_score):
    client = get_gsheet_client()
    if not client:
        return
    sheet = get_sheet(client)
    if not sheet:
        return
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        checklist_json = json.dumps(checklist_items)
        records = sheet.get_all_records()
        row_idx = None
        for i, row in enumerate(records, start=2):
            if row.get("Trainee Name") == username and row.get("Module Key") == module_key:
                row_idx = i
                break
        data = [username, module_key, pct, checklist_json, quiz_score, now]
        if row_idx:
            sheet.update(f"A{row_idx}:F{row_idx}", [data])
        else:
            sheet.append_row(data)
    except Exception:
        pass

def load_progress(username):
    client = get_gsheet_client()
    if not client:
        return {}
    sheet = get_sheet(client)
    if not sheet:
        return {}
    try:
        records = sheet.get_all_records()
        result = {}
        for row in records:
            if row.get("Trainee Name") == username:
                mk = row.get("Module Key", "")
                result[mk] = {
                    "pct": row.get("Completion %", 0),
                    "checklist": json.loads(row.get("Checklist Items", "{}")),
                    "quiz_score": row.get("Quiz Score", None),
                }
        return result
    except Exception:
        return {}

# ─────────────────────────────────────────────
#  MODULE DATA
# ─────────────────────────────────────────────
MODULES = [
    {
        "key": "welcome",
        "number": 1,
        "title": "Welcome to AAP",
        "subtitle": "Our history, mission, vision & values",
        "icon": "🏢",
    },
    {
        "key": "conduct",
        "number": 2,
        "title": "Code of Conduct & Ethics",
        "subtitle": "Expected behaviors, confidentiality & EEO",
        "icon": "⚖️",
    },
    {
        "key": "policies",
        "number": 3,
        "title": "Workplace Policies",
        "subtitle": "Attendance, appearance, safety & more",
        "icon": "📋",
    },
    {
        "key": "benefits",
        "number": 4,
        "title": "Benefits & Time Off",
        "subtitle": "Health, leave, 401k & employee perks",
        "icon": "💼",
    },
    {
        "key": "firststeps",
        "number": 5,
        "title": "Your First Steps",
        "subtitle": "Systems, contacts & what to expect",
        "icon": "🚀",
    },
]

# ─────────────────────────────────────────────
#  SESSION STATE DEFAULTS
# ─────────────────────────────────────────────
defaults = {
    "username": "",
    "selected_module": None,
    "sheet_loaded": False,
    "progress": {m["key"]: 0 for m in MODULES},
    "quiz_results": {},
    "checklist_items": {m["key"]: {} for m in MODULES},
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────
def pct_bar(pct):
    return f"""
    <div class="progress-container">
        <div class="progress-fill" style="width:{pct}%"></div>
    </div>
    <small style="color:#8BA3C7">{pct}% complete</small>
    """

def info_box(text, color="default"):
    cls = "info-box " + ("green" if color == "green" else "yellow" if color == "yellow" else "")
    return f'<div class="{cls}">{text}</div>'

def calculate_module_pct(module_key, checklists, quiz_results):
    items = checklists.get(module_key, {})
    total = len(items)
    checked = sum(1 for v in items.values() if v)
    checklist_pct = (checked / total * 70) if total > 0 else 0
    quiz_pct = 30 if quiz_results.get(module_key) is not None else 0
    return int(checklist_pct + quiz_pct)

def update_progress(module_key):
    pct = calculate_module_pct(
        module_key,
        st.session_state.checklist_items,
        st.session_state.quiz_results,
    )
    st.session_state.progress[module_key] = pct
    if st.session_state.username:
        items = st.session_state.checklist_items.get(module_key, {})
        score = st.session_state.quiz_results.get(module_key)
        save_progress(st.session_state.username, module_key, pct, items, score)

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 💊 AAP Orientation")
    st.markdown("---")

    name_input = st.text_input("Your Name", value=st.session_state.username, placeholder="Enter your name")
    if name_input != st.session_state.username:
        st.session_state.username = name_input
        st.session_state.sheet_loaded = False

    if st.session_state.username and not st.session_state.sheet_loaded:
        saved = load_progress(st.session_state.username)
        if saved:
            for mk, data in saved.items():
                st.session_state.progress[mk] = data.get("pct", 0)
                st.session_state.checklist_items[mk] = data.get("checklist", {})
                if data.get("quiz_score") is not None:
                    st.session_state.quiz_results[mk] = data["quiz_score"]
        st.session_state.sheet_loaded = True

    st.markdown("---")
    st.markdown("**Modules**")

    if st.button("🏠  Home", key="nav_home"):
        st.session_state.selected_module = None

    for m in MODULES:
        pct = st.session_state.progress.get(m["key"], 0)
        label = f"{m['icon']}  {m['number']}. {m['title']}"
        if st.button(label, key=f"nav_{m['key']}"):
            st.session_state.selected_module = m["key"]
        st.markdown(pct_bar(pct), unsafe_allow_html=True)

    st.markdown("---")
    total_pct = int(sum(st.session_state.progress.values()) / len(MODULES))
    st.markdown(f"**Overall Progress: {total_pct}%**")
    st.markdown(pct_bar(total_pct), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <small style='color:#8BA3C7'>
    <b>HR Contact</b><br>
    Nicole Thornton<br>
    HR Administrator<br>
    📞 256-574-7528<br>
    ✉ Nicole.thornton@apirx.com
    </small>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  MAIN CONTENT — HOME
# ─────────────────────────────────────────────
def show_home():
    name_display = f", {st.session_state.username}" if st.session_state.username else ""
    st.markdown(f"""
    <div class="welcome-banner">
        <h1>Welcome to American Associated Pharmacies{name_display}! 🎉</h1>
        <p>We're thrilled to have you on board. Complete all five orientation modules below to finish your onboarding.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.username:
        st.markdown(info_box("👆 <b>Enter your name in the sidebar to track your progress.</b>"), unsafe_allow_html=True)

    # Summary metrics
    completed = sum(1 for p in st.session_state.progress.values() if p == 100)
    total_pct = int(sum(st.session_state.progress.values()) / len(MODULES))
    col1, col2, col3 = st.columns(3)
    col1.metric("Modules Complete", f"{completed} / {len(MODULES)}")
    col2.metric("Overall Progress", f"{total_pct}%")
    col3.metric("Quizzes Passed", f"{sum(1 for v in st.session_state.quiz_results.values() if v is not None)} / {len(MODULES)}")

    st.markdown("---")
    st.markdown("### 📚 Your Orientation Modules")

    for m in MODULES:
        pct = st.session_state.progress.get(m["key"], 0)
        badge_class = "complete" if pct == 100 else ""
        badge_text = "✅ Complete" if pct == 100 else f"⏳ {pct}% Done"
        st.markdown(f"""
        <div class="module-card">
            <span class="badge {badge_class}">{badge_text}</span>
            <h3>{m['icon']} Module {m['number']}: {m['title']}</h3>
            <p>{m['subtitle']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Open Module {m['number']}", key=f"open_{m['key']}"):
            st.session_state.selected_module = m["key"]
            st.rerun()

# ─────────────────────────────────────────────
#  MODULE 1 — WELCOME TO AAP
# ─────────────────────────────────────────────
def show_module_welcome():
    st.markdown("""
    <div class="content-section">
        <h2>🏢 Module 1: Welcome to AAP</h2>

        <h3>A Message From Our CEO</h3>
        <p>On behalf of your colleagues, I welcome you to AAP and wish you every success here. We believe that each
        employee contributes directly to AAP's growth and success, and we hope you will take pride in being a member
        of our team. This handbook was developed to describe some of the expectations of our employees and to outline
        the policies, programs, and benefits available to eligible employees.</p>
        <p>We hope that your experience here will be challenging, enjoyable, and rewarding.</p>
        <p><strong>— Jon Copeland, R.Ph., Chief Executive Officer</strong></p>

        <h3>Who We Are</h3>
        <p>American Associated Pharmacies (AAP) is a national cooperative of more than <strong>2,000 independent
        pharmacies</strong>. AAP began in <strong>2009</strong>, when two major pharmacy cooperatives —
        <strong>United Drugs</strong> of Phoenix, AZ, and <strong>Associated Pharmacies, Inc. (API)</strong>
        of Scottsboro, AL — joined forces to form one of America's largest independent pharmacy organizations.</p>
        <p>Today, AAP continues to operate API, its independent warehouse and distributor, with two warehouse locations
        in the U.S. Along with its subsidiaries, AAP provides member-focused support and serves as a collaborative
        professional advocate, bringing innovative and cost-saving programs to its member pharmacies, improving both
        profitability and patient care.</p>

        <h3>Our Mission</h3>
        <p>AAP provides support and customized solutions for independent community pharmacies to enhance their
        profitability, streamline their operations and improve the quality of patient care.</p>

        <h3>Our Vision</h3>
        <p>Helping independent pharmacies thrive in a competitive healthcare market.</p>

        <h3>Our Values & Guiding Principles</h3>
        <p>Our values guide every decision, discussion and behavior. It's not only <em>what</em> we do that matters,
        but <em>how</em> we do it.</p>
    </div>
    """, unsafe_allow_html=True)

    values = [
        ("🎯", "Customer Focus", "Our primary focus is to meet customer requirements and strive to exceed customer expectations. Excellent service to the outside customer is dependent upon healthy internal customer service practices and teamwork. Customer Service is not just a department — it is an attitude."),
        ("🤝", "Integrity", "We act with honesty and integrity without compromising the truth. We maintain consistency in what we say and what we do to build trust."),
        ("💙", "Respect", "We treat others with the same dignity as we wish to be treated. We recognize the power of teamwork and appreciate the unique contributions that each member of a team can make. We encourage open and honest communication."),
        ("⭐", "Excellence", "We strive for the highest quality in everything that we do. We seek and pursue opportunities for continuous improvement and innovation."),
        ("🙋", "Ownership", "We seek responsibility and hold ourselves accountable for our actions. When things go wrong, we take responsibility."),
    ]

    for icon, value, desc in values:
        st.markdown(f"""
        <div class="content-section" style="padding:18px 24px;margin-bottom:10px;">
            <h3 style="margin-top:0">{icon} {value}</h3>
            <p style="margin:0">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

    # CHECKLIST
    st.markdown("### ✅ Module 1 Checklist")
    st.markdown("Check off each item as you review it.")

    checklist_items = {
        "ceo_welcome": "I have read the CEO welcome message.",
        "who_we_are": "I understand who AAP is and when it was founded.",
        "mission": "I can explain AAP's mission statement.",
        "vision": "I can explain AAP's vision statement.",
        "values_5": "I can name all five of AAP's core values.",
        "value_conduct": "I understand that values guide both what we do AND how we do it.",
        "two_locations": "I know AAP operates two warehouse locations through its subsidiary, API.",
    }

    mk = "welcome"
    if mk not in st.session_state.checklist_items or not st.session_state.checklist_items[mk]:
        st.session_state.checklist_items[mk] = {k: False for k in checklist_items}

    changed = False
    for key, label in checklist_items.items():
        val = st.checkbox(label, value=st.session_state.checklist_items[mk].get(key, False), key=f"{mk}_chk_{key}")
        if val != st.session_state.checklist_items[mk].get(key, False):
            st.session_state.checklist_items[mk][key] = val
            changed = True
    if changed:
        update_progress(mk)

    # QUIZ
    st.markdown("### 📝 Module 1 Quiz")
    if st.session_state.quiz_results.get(mk) is not None:
        score = st.session_state.quiz_results[mk]
        st.success(f"✅ Quiz completed! You scored {score}/4.")
    else:
        with st.form("quiz_welcome"):
            q1 = st.radio("1. In what year was AAP formed?",
                ["2005", "2007", "2009", "2012"], key="w_q1", index=None)
            q2 = st.radio("2. Which city is home to AAP's subsidiary API?",
                ["Phoenix, AZ", "Scottsboro, AL", "Huntsville, AL", "Nashville, TN"], key="w_q2", index=None)
            q3 = st.radio("3. Which of the following is NOT one of AAP's five core values?",
                ["Integrity", "Ownership", "Innovation", "Excellence"], key="w_q3", index=None)
            q4 = st.radio("4. According to AAP's values, customer service is best described as:",
                ["A department that handles complaints",
                 "An attitude shared by all employees",
                 "The responsibility of management only",
                 "A program run by the VP of HR"], key="w_q4", index=None)
            submitted = st.form_submit_button("Submit Quiz")
            if submitted:
                score = sum([
                    q1 == "2009",
                    q2 == "Scottsboro, AL",
                    q3 == "Innovation",
                    q4 == "An attitude shared by all employees",
                ])
                st.session_state.quiz_results[mk] = score
                update_progress(mk)
                st.rerun()

# ─────────────────────────────────────────────
#  MODULE 2 — CODE OF CONDUCT
# ─────────────────────────────────────────────
def show_module_conduct():
    st.markdown("""
    <div class="content-section">
        <h2>⚖️ Module 2: Code of Conduct & Ethics</h2>

        <h3>Our Commitment</h3>
        <p>The success of AAP is dependent upon our customers' trust and we are dedicated to preserving that trust.
        Employees owe a duty to AAP, its customers, and shareholders to act in a way that will merit the continued
        trust and confidence of the public. AAP will comply with all applicable laws and regulations and expects its
        directors, officers, and employees to conduct business in accordance with the letter, spirit, and intent of
        all relevant laws — and to refrain from any illegal, dishonest, or unethical conduct.</p>
        <p>Compliance with this policy of business ethics is the responsibility of <strong>every AAP employee.</strong></p>

        <h3>As an AAP Employee, I Will…</h3>
        <ul>
            <li><strong>Work diligently</strong> to pursue the Company's objectives without disrupting others.</li>
            <li><strong>Protect company assets</strong> — including information systems, intellectual property, equipment,
            and cash — from theft, misuse, or misappropriation.</li>
            <li><strong>Conduct myself with the highest level of professionalism, integrity, and ability,</strong>
            treating coworkers, vendors, visitors, and members with respect, dignity, and courtesy.</li>
            <li><strong>Use appropriate judgment</strong> in all communications (email, memos, notes) and avoid
            inappropriate or derogatory comments about anyone I work with.</li>
            <li><strong>Accept full responsibility</strong> for the work I perform and report any errors or omissions
            to my supervisor immediately.</li>
            <li><strong>Not misuse authority or company property</strong> entrusted to me.</li>
            <li><strong>Build and share knowledge</strong> for the betterment of AAP and my coworkers.</li>
            <li><strong>Protect the privacy and confidentiality</strong> of all information entrusted to me.</li>
            <li><strong>Behave ethically</strong> and report any known or suspected illegal or unethical behavior
            to my supervisor immediately.</li>
            <li><strong>Avoid conflicts of interest</strong> and ensure my employer is aware of any real, perceived,
            or potential conflict of interest.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="content-section">
        <h3>⚠️ Unacceptable Conduct</h3>
        <p>The following are examples of conduct that may result in disciplinary action, <strong>up to and including
        termination of employment:</strong></p>
        <ul>
            <li>Theft or inappropriate removal or possession of property</li>
            <li>Falsification of records, including timekeeping records</li>
            <li>Working under the influence of alcohol or illegal drugs</li>
            <li>Possession, distribution, sale, transfer, or use of alcohol or illegal drugs in the workplace</li>
            <li>Fighting or threatening violence in the workplace</li>
            <li>Boisterous or disruptive activity in the workplace</li>
            <li>Negligence or improper conduct leading to damage of employer-owned or customer-owned property</li>
            <li>Insubordination or other disrespectful conduct</li>
            <li>Violation of safety or health rules</li>
            <li>Sexual or other unlawful or unwelcomed harassment</li>
            <li>Possession of dangerous or unauthorized materials (explosives, firearms) in the workplace</li>
            <li>Excessive absenteeism or any absence without notice</li>
            <li>Unauthorized use of telephones, mail system, or other employer-owned equipment</li>
            <li>Unauthorized disclosure of business secrets or confidential information</li>
            <li>Unsatisfactory performance or conduct</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="content-section">
        <h3>🛡️ Equal Employment Opportunity (EEO)</h3>
        <p>Employment decisions at AAP are based on <strong>merit, qualifications, and abilities.</strong> AAP does
        not discriminate in employment opportunities or practices on the basis of race, color, religion, sex, national
        origin, age, disability, or any other characteristic protected by law.</p>
        <p>Employees can raise concerns and make reports without fear of reprisal. Anyone found to be engaging in any
        type of unlawful discrimination will be subject to disciplinary action, up to and including termination.</p>

        <h3>🚫 Sexual & Other Unlawful Harassment</h3>
        <p>AAP is committed to providing a work environment that is free of discrimination and unlawful harassment.
        Sexual harassment can take many forms, including:</p>
        <ul>
            <li>Offensive comments or jokes</li>
            <li>Sexual advances or unnecessary touching</li>
            <li>Comments about a person's body</li>
            <li>Showing sexually suggestive pictures or objects</li>
            <li>Implied promises or threats tied to participation in sexual conduct</li>
        </ul>
        <p><strong>This conduct has no place at AAP and will not be tolerated.</strong></p>
        <p>If you believe you have been harassed, you should:</p>
        <ul>
            <li>Tell the offender their conduct is offensive (if comfortable doing so).</li>
            <li>Report it to your immediate supervisor or the HR department.</li>
            <li>If the harasser is your supervisor, contact the <strong>VP of Human Resources</strong> directly.</li>
        </ul>
        <p>No one will be retaliated against for complaining in good faith about sexual harassment.</p>

        <h3>🔒 Confidentiality</h3>
        <p>All employees are required to sign a Confidentiality and Non-Disclosure Agreement upon hire. All written
        and verbal communication regarding the Company's operations or your position must remain strictly confidential
        unless otherwise permitted by your supervisor or by Company policy. <strong>Refusal to sign is grounds for
        immediate termination.</strong></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ✅ Module 2 Checklist")
    checklist_items = {
        "code_reviewed": "I have read and understand the AAP Employee Code of Conduct.",
        "unacceptable": "I understand examples of unacceptable workplace conduct.",
        "eeo": "I understand AAP's Equal Employment Opportunity policy.",
        "harassment": "I know how to report harassment and that retaliation is prohibited.",
        "confidentiality": "I understand my confidentiality obligations and will sign the NDA.",
        "conflicts": "I understand my obligation to disclose any real or potential conflicts of interest.",
        "reporting": "I know to report known or suspected illegal/unethical behavior to my supervisor.",
    }

    mk = "conduct"
    if mk not in st.session_state.checklist_items or not st.session_state.checklist_items[mk]:
        st.session_state.checklist_items[mk] = {k: False for k in checklist_items}

    changed = False
    for key, label in checklist_items.items():
        val = st.checkbox(label, value=st.session_state.checklist_items[mk].get(key, False), key=f"{mk}_chk_{key}")
        if val != st.session_state.checklist_items[mk].get(key, False):
            st.session_state.checklist_items[mk][key] = val
            changed = True
    if changed:
        update_progress(mk)

    st.markdown("### 📝 Module 2 Quiz")
    if st.session_state.quiz_results.get(mk) is not None:
        score = st.session_state.quiz_results[mk]
        st.success(f"✅ Quiz completed! You scored {score}/4.")
    else:
        with st.form("quiz_conduct"):
            q1 = st.radio("1. AAP's employment decisions are based on which of the following?",
                ["Seniority and connections",
                 "Merit, qualifications, and abilities",
                 "Education level only",
                 "Manager discretion"], key="c_q1", index=None)
            q2 = st.radio("2. If you witness suspected illegal or unethical behavior, you should:",
                ["Ignore it to avoid conflict",
                 "Post about it on social media",
                 "Report it to your supervisor immediately",
                 "Wait to see if it happens again"], key="c_q2", index=None)
            q3 = st.radio("3. Which of the following is NOT considered sexual harassment?",
                ["Making offensive jokes about a coworker's appearance",
                 "Giving a coworker a professional performance evaluation",
                 "Showing sexually suggestive images to coworkers",
                 "Making implied promises tied to sexual conduct"], key="c_q3", index=None)
            q4 = st.radio("4. Refusing to sign the Confidentiality and Non-Disclosure Agreement results in:",
                ["A written warning",
                 "A meeting with HR",
                 "Immediate termination",
                 "A probationary period"], key="c_q4", index=None)
            submitted = st.form_submit_button("Submit Quiz")
            if submitted:
                score = sum([
                    q1 == "Merit, qualifications, and abilities",
                    q2 == "Report it to your supervisor immediately",
                    q3 == "Giving a coworker a professional performance evaluation",
                    q4 == "Immediate termination",
                ])
                st.session_state.quiz_results[mk] = score
                update_progress(mk)
                st.rerun()

# ─────────────────────────────────────────────
#  MODULE 3 — WORKPLACE POLICIES
# ─────────────────────────────────────────────
def show_module_policies():
    st.markdown("""
    <div class="content-section">
        <h2>📋 Module 3: Workplace Policies</h2>

        <h3>🕐 Attendance & Punctuality</h3>
        <p>AAP uses a <strong>no-fault point system</strong> to manage attendance fairly and consistently for all
        non-exempt employees. Absences are tracked regardless of the reason, with a few specific exclusions.</p>

        <p><strong>Excluded from points (these do NOT count against you):</strong>
        FMLA leave, pre-approved personal leaves, bereavement leave, jury/witness duty, pre-approved vacation days,
        personal days, holidays, long-term sick leave, approved early leaves, short-term disability, and emergency
        closing absences.</p>

        <p><strong>Point Values:</strong></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <table class="styled-table">
        <tr><th>Reason</th><th>Points</th></tr>
        <tr><td>Tardy up to 5 minutes (grace period)</td><td>0</td></tr>
        <tr><td>Tardy or early leave (less than 4 hours)</td><td>½</td></tr>
        <tr><td>Full shift absence, tardy or early leave (4+ hours)</td><td>1</td></tr>
        <tr><td>Absence with no report or call 15+ minutes after start of workday</td><td>1½</td></tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("""
    <table class="styled-table">
        <tr><th>Points Accumulated (in 12 months)</th><th>Action</th></tr>
        <tr><td>5 points</td><td>Coaching Session</td></tr>
        <tr><td>6 points</td><td>Verbal Warning</td></tr>
        <tr><td>7 points</td><td>Written Warning</td></tr>
        <tr><td>8 points</td><td>Termination</td></tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown(info_box("💡 <b>Perfect Attendance Rewards:</b> 1 point is removed after <b>2 consecutive months</b> of perfect attendance. Employees with <b>3 consecutive months</b> of perfect attendance receive a <b>$75 bonus</b> on their next paycheck."), unsafe_allow_html=True)
    st.markdown(info_box("⚠️ <b>No Call / No Show:</b> 2 consecutive days without reporting in will be treated as a voluntary resignation.", "yellow"), unsafe_allow_html=True)
    st.markdown(info_box("📋 <b>Doctor's Notes:</b> Required for illness greater than 1 day, up to a maximum of 3 consecutive days. The note must include dates of absence and the return-to-work date."), unsafe_allow_html=True)

    st.markdown("""
    <div class="content-section">
        <h3>👔 Personal Appearance</h3>
        <p>Dress requirements vary by department. Your supervisor will advise you on department-specific expectations.
        The following standards apply to <strong>all employees at all times:</strong></p>
        <ul>
            <li>A neat, clean, and well-groomed appearance is required.</li>
            <li>All clothing must be work-appropriate — nothing too revealing or inappropriate.</li>
            <li>Avoid clothing with offensive or inappropriate stamps/logos.</li>
            <li>Due to allergies and asthma concerns, avoid wearing perfume or perfume-scented products.</li>
        </ul>
        <p>Employees found to be out of compliance will be asked to clock out, leave, and return dressed appropriately.</p>

        <h3>🚭 Drug & Alcohol Policy</h3>
        <p>AAP maintains a <strong>drug and alcohol-free workplace.</strong> Employees may not use or be under the
        influence of alcohol, drugs, or any intoxicating substance while at work. Employees are subject to
        <strong>random drug testing at any time.</strong></p>
        <ul>
            <li>All work-related accidents require immediate drug and alcohol testing.</li>
            <li>Violations may result in immediate termination and/or required participation in a rehab program.</li>
            <li>The Employee Assistance Program (EAP) is available to employees who need support with substance concerns.</li>
        </ul>

        <h3>🛡️ Workplace Safety</h3>
        <p>The <strong>VP of Human Resources</strong> is responsible for AAP's safety program. Each employee is
        expected to:</p>
        <ul>
            <li>Obey all safety rules and exercise caution in all work activities.</li>
            <li>Immediately report any unsafe condition to the appropriate supervisor.</li>
            <li>Report all work-related injuries to HR or a supervisor immediately, no matter how minor.</li>
        </ul>
        <p>Violating safety standards may result in disciplinary action, up to and including termination.</p>

        <h3>💻 Computer & Email Use</h3>
        <p>All computers, files, email systems, and software are <strong>AAP property</strong> intended for
        business use. AAP may monitor computer and email usage to ensure compliance.</p>
        <ul>
            <li>Do not use a password, access a file, or retrieve stored communications without authorization.</li>
            <li>Transmission of sexually explicit images, ethnic slurs, racial comments, or off-color jokes
            is strictly prohibited.</li>
            <li>Do not illegally duplicate software or its documentation.</li>
        </ul>

        <h3>🚷 Workplace Violence</h3>
        <p>AAP has zero tolerance for workplace violence. This includes verbal or physical harassment or threats,
        assaults, bullying, and any behavior that causes others to feel unsafe.</p>
        <p>All threatening incidents must be <strong>reported within 24 hours</strong> and will be investigated
        and documented by Human Resources.</p>

        <h3>⏰ Work Schedules & Overtime</h3>
        <p>Your supervisor will advise you of your individual work schedule. Staffing needs may require variations
        in hours. <strong>All overtime must be approved by your supervisor before it is performed.</strong>
        Unauthorized overtime or failure to work scheduled overtime may result in disciplinary action.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ✅ Module 3 Checklist")
    checklist_items = {
        "point_system": "I understand the no-fault attendance point system and the point values.",
        "corrective_levels": "I know the corrective action steps (coaching at 5, verbal at 6, written at 7, termination at 8).",
        "perfect_att": "I know I can earn a point removal and a $75 bonus for perfect attendance.",
        "no_call": "I understand that 2 consecutive no-call/no-shows may be treated as a resignation.",
        "appearance": "I understand AAP's personal appearance standards.",
        "drug_policy": "I understand AAP's drug and alcohol-free workplace policy.",
        "safety": "I know to immediately report any unsafe condition or work-related injury.",
        "computer_policy": "I understand that company computers and email are for business use and may be monitored.",
    }

    mk = "policies"
    if mk not in st.session_state.checklist_items or not st.session_state.checklist_items[mk]:
        st.session_state.checklist_items[mk] = {k: False for k in checklist_items}

    changed = False
    for key, label in checklist_items.items():
        val = st.checkbox(label, value=st.session_state.checklist_items[mk].get(key, False), key=f"{mk}_chk_{key}")
        if val != st.session_state.checklist_items[mk].get(key, False):
            st.session_state.checklist_items[mk][key] = val
            changed = True
    if changed:
        update_progress(mk)

    st.markdown("### 📝 Module 3 Quiz")
    if st.session_state.quiz_results.get(mk) is not None:
        score = st.session_state.quiz_results[mk]
        st.success(f"✅ Quiz completed! You scored {score}/5.")
    else:
        with st.form("quiz_policies"):
            q1 = st.radio("1. How many points does a full shift no-call / no-show receive?",
                ["½ point", "1 point", "1½ points", "2 points"], key="p_q1", index=None)
            q2 = st.radio("2. At how many points within 12 months is an employee terminated?",
                ["6 points", "7 points", "8 points", "10 points"], key="p_q2", index=None)
            q3 = st.radio("3. How many consecutive months of perfect attendance earns the $75 bonus?",
                ["1 month", "2 months", "3 months", "6 months"], key="p_q3", index=None)
            q4 = st.radio("4. Who is responsible for AAP's safety program?",
                ["The CEO",
                 "The VP of Human Resources",
                 "Each individual department head",
                 "OSHA"], key="p_q4", index=None)
            q5 = st.radio("5. Pre-approved vacation days are excluded from the attendance point system.",
                ["True", "False"], key="p_q5", index=None)
            submitted = st.form_submit_button("Submit Quiz")
            if submitted:
                score = sum([
                    q1 == "1½ points",
                    q2 == "8 points",
                    q3 == "3 months",
                    q4 == "The VP of Human Resources",
                    q5 == "True",
                ])
                st.session_state.quiz_results[mk] = score
                update_progress(mk)
                st.rerun()

# ─────────────────────────────────────────────
#  MODULE 4 — BENEFITS & TIME OFF
# ─────────────────────────────────────────────
def show_module_benefits():
    st.markdown("""
    <div class="content-section">
        <h2>💼 Module 4: Benefits & Time Off</h2>
        <p>Benefits eligibility depends on your employment classification. Review the key differences below, then
        explore each benefit area.</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["⏰ Leave & Holidays", "🏥 Health Benefits", "💰 401k & Life", "🌟 Perks & EAP", "FT vs PT Summary"])

    with tab1:
        st.markdown("""
        <div class="content-section">
            <h3>🏖️ Vacation (Full-Time Only)</h3>
            <p>Vacation begins accruing after <strong>60 days of full-time service</strong> and is accrued weekly.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <table class="styled-table">
            <tr><th>Length of Employment</th><th>Days Per Year</th><th>Hours Per Year</th><th>Accrual Rate</th></tr>
            <tr><td>60 days → 1st Anniversary</td><td>3</td><td>24</td><td>0.46 hrs/week</td></tr>
            <tr><td>1st → 2nd Anniversary</td><td>5</td><td>40</td><td>0.77 hrs/week</td></tr>
            <tr><td>2nd → 3rd Anniversary</td><td>7</td><td>56</td><td>1.07 hrs/week</td></tr>
            <tr><td>3rd → 5th Anniversary</td><td>10</td><td>80</td><td>1.54 hrs/week</td></tr>
            <tr><td>5th → 9th Anniversary</td><td>15</td><td>120</td><td>2.31 hrs/week</td></tr>
            <tr><td>10th → 19th Anniversary</td><td>17</td><td>136</td><td>2.62 hrs/week</td></tr>
            <tr><td>20th Anniversary+</td><td>19</td><td>152</td><td>2.93 hrs/week</td></tr>
        </table>
        """, unsafe_allow_html=True)
        st.markdown(info_box("Unused vacation may be banked up to 19 days (152 hours) total. Any remaining time beyond the bank limit is paid out. Accrued vacation is paid out upon termination."), unsafe_allow_html=True)

        st.markdown("""
        <div class="content-section">
            <h3>📅 Personal Leave</h3>
            <p>Available to full-time and part-time employees after the initial 60-day waiting period.
            Personal leave <strong>does not carry over</strong> year to year and is not paid out upon termination.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <table class="styled-table">
            <tr><th>Classification</th><th>Upon Initial Eligibility</th><th>After 1 Year</th><th>After 5 Years</th></tr>
            <tr><td>Full-Time</td><td>24 hours (3 days)</td><td>32 hours (4 days)</td><td>40 hours (5 days)</td></tr>
            <tr><td>Part-Time</td><td>1 hr per 30 hrs worked, up to 24 hrs</td><td>Up to 32 hrs</td><td>Up to 40 hrs</td></tr>
        </table>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="content-section">
            <h3>🎄 Paid Holidays</h3>
            <p>Eligible after <strong>60 days of service.</strong> To receive holiday pay, employees must work the
            last scheduled day <em>before</em> and the first scheduled day <em>after</em> the holiday.</p>
            <ul>
                <li>New Year's Day (January 1)</li>
                <li>Memorial Day (last Monday in May)</li>
                <li>Independence Day (July 4)</li>
                <li>Labor Day (first Monday in September)</li>
                <li>Thanksgiving (fourth Thursday in November)</li>
                <li>Christmas Day (December 25)</li>
                <li><strong>Floating Holiday:</strong> Christmas Eve OR Day After Thanksgiving (based on scheduling needs)</li>
                <li><strong>Floating Holiday:</strong> Same as above — department-dependent</li>
            </ul>
            <p>Employees asked to work a designated holiday will receive a floating holiday to use within 90 days.</p>

            <h3>😷 Long-Term Sick Leave (Full-Time Only)</h3>
            <p>Reserved for serious illness requiring <strong>3 or more consecutive days</strong> away from work,
            as mandated by a physician. Cannot be used for cosmetic procedures, routine follow-up visits, or
            absences under 3 consecutive days.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <table class="styled-table">
            <tr><th>Years of Service</th><th>Days Earned</th></tr>
            <tr><td>4 years</td><td>10 days (80 hours)</td></tr>
            <tr><td>9 years</td><td>Additional 10 days</td></tr>
            <tr><td>14 years</td><td>Additional 10 days</td></tr>
            <tr><td>19 years</td><td>Additional 10 days</td></tr>
            <tr><td>Every 5 years thereafter</td><td>Additional 10 days</td></tr>
        </table>
        """, unsafe_allow_html=True)
        st.markdown(info_box("Long-term sick leave can be banked up to 40 days (320 hours) total. It is NOT paid out upon termination."), unsafe_allow_html=True)

        st.markdown("""
        <div class="content-section">
            <h3>🏥 FMLA Leave</h3>
            <p>Eligible full-time employees who have completed <strong>365 calendar days of service</strong> may
            request up to <strong>12 weeks of unpaid, job-protected leave</strong> in a 12-month period for:</p>
            <ul>
                <li>A serious health condition of the employee</li>
                <li>Birth or adoption of a child</li>
                <li>Care for a spouse, child, or parent with a serious health condition</li>
                <li>Qualifying military exigencies (up to 26 weeks for care of a seriously injured service member)</li>
            </ul>
            <p>Health insurance benefits continue during approved FMLA leave. Requests should be made at least
            <strong>30 days in advance</strong> for foreseeable events.</p>

            <h3>🌸 Other Leave Types</h3>
            <ul>
                <li><strong>Bereavement:</strong> Up to 5 paid days for immediate family members (spouse, parent, child, sibling, grandparents, grandchildren, and their spouses).</li>
                <li><strong>Jury Duty:</strong> Up to 2 weeks paid leave per year.</li>
                <li><strong>Voting:</strong> Employees unable to vote outside of work hours may request reasonable time off.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="content-section">
            <h3>🏥 Medical Insurance</h3>
            <p>Eligible after <strong>60 days of employment.</strong> Benefits are effective the
            <strong>1st of the month following 60 days</strong> of service. Full-time employees working
            30+ hours per week are eligible.</p>
            <p>AAP offers <strong>two plans through BlueCross BlueShield of Alabama:</strong></p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <table class="styled-table">
            <tr><th></th><th>Option 1: PPO Plan</th><th>Option 2: HDHP + HSA</th></tr>
            <tr><td><b>Employee Only</b></td><td>$157.20/mo</td><td>$136.34/mo</td></tr>
            <tr><td><b>Employee + Spouse</b></td><td>$492.32/mo</td><td>$404.66/mo</td></tr>
            <tr><td><b>Employee + Child(ren)</b></td><td>$444.36/mo</td><td>$373.04/mo</td></tr>
            <tr><td><b>Employee + Family</b></td><td>$678.62/mo</td><td>$581.72/mo</td></tr>
            <tr><td><b>Deductible (Ind/Fam)</b></td><td>$500 / $1,000</td><td>$1,700 / $3,400</td></tr>
            <tr><td><b>Coinsurance</b></td><td>20%</td><td>10%</td></tr>
            <tr><td><b>AAP HSA Contribution</b></td><td>N/A</td><td>$900 / $1,800 per year</td></tr>
            <tr><td><b>Out-of-Pocket Max (Ind/Fam)</b></td><td>$2,250 / $4,500</td><td>$3,400 / $6,800</td></tr>
            <tr><td><b>Preventive Care</b></td><td>100%</td><td>100%</td></tr>
            <tr><td><b>PCP / Specialist Copay</b></td><td>$30 / $45</td><td>Ded then 10%</td></tr>
            <tr><td><b>Telehealth (Teladoc)</b></td><td>FREE (company paid)</td><td>FREE (company paid)</td></tr>
        </table>
        """, unsafe_allow_html=True)
        st.markdown(info_box("📌 <b>HDHP HSA tip:</b> The HSA is owned by <b>you</b> — funds roll over year to year and go with you if you leave AAP. 2026 contribution limits: $4,400 (Single) / $8,750 (Family). If age 55+, add an extra $1,000."), unsafe_allow_html=True)

        st.markdown("""
        <div class="content-section">
            <h3>🦷 Dental Insurance (Guardian)</h3>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <table class="styled-table">
            <tr><th></th><th>Base Plan</th><th>High Plan</th></tr>
            <tr><td>Employee</td><td>$6.78/mo</td><td>$10.66/mo</td></tr>
            <tr><td>Employee + Spouse</td><td>$20.56/mo</td><td>$28.80/mo</td></tr>
            <tr><td>Employee + Child(ren)</td><td>$20.76/mo</td><td>$28.32/mo</td></tr>
            <tr><td>Employee + Family</td><td>$34.54/mo</td><td>$47.10/mo</td></tr>
            <tr><td>Annual Max Benefit</td><td>$1,500/member</td><td>$3,000/member</td></tr>
            <tr><td>Preventive (exams, cleanings)</td><td>100%</td><td>100%</td></tr>
            <tr><td>Basic Services</td><td>80% after deductible</td><td>100%</td></tr>
            <tr><td>Major Services</td><td>50% after deductible</td><td>50% after deductible</td></tr>
            <tr><td>Orthodontics Lifetime Max</td><td>$1,000</td><td>$1,500</td></tr>
        </table>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="content-section">
            <h3>👓 Vision Insurance (Guardian / Davis Vision)</h3>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <table class="styled-table">
            <tr><th></th><th>Cost / Coverage</th></tr>
            <tr><td>Employee</td><td>$6.93/mo</td></tr>
            <tr><td>Employee + One Dependent</td><td>$10.04/mo</td></tr>
            <tr><td>Employee + Family</td><td>$18.00/mo</td></tr>
            <tr><td>Eye Exam</td><td>$10 copay (every 12 months)</td></tr>
            <tr><td>Lenses</td><td>$25 copay (every 12 months)</td></tr>
            <tr><td>Frames Allowance</td><td>$130 (every 24 months)</td></tr>
            <tr><td>Contacts</td><td>$130 max (every 12 months)</td></tr>
        </table>
        """, unsafe_allow_html=True)
        st.markdown(info_box("📅 <b>Enrollment reminder:</b> New employees must enroll within <b>30 days of hire.</b> Benefits take effect the 1st of the month following 60 days. Qualified life events allow mid-year changes within 30 days of the event."), unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="content-section">
            <h3>💰 401(k) Savings Plan</h3>
            <p>Eligible on the <strong>1st of the month following 60 days</strong> of continuous full-time employment.</p>
            <ul>
                <li>AAP matches <strong>100%</strong> of the first <strong>3%</strong> you contribute.</li>
                <li>AAP matches <strong>50%</strong> of the next <strong>2%</strong> you contribute.</li>
                <li>Company match is <strong>100% vested immediately</strong> — it's yours from day one.</li>
            </ul>
            <p>Part-time employees are eligible after <strong>1 year of service and 1,000 hours worked.</strong></p>

            <h3>🛡️ Life Insurance & AD&D</h3>
            <p>AAP provides <strong>Basic Life and AD&D insurance at no cost to you</strong>, equal to your annual
            earnings up to a maximum of $270,000, through Guardian. This coverage is effective the 1st of the month
            after 60 days of employment.</p>
            <p>You may also elect <strong>Voluntary Life and AD&D</strong> for yourself, your spouse, and/or
            dependents during your initial enrollment period:</p>
            <ul>
                <li><strong>Employee:</strong> $10,000 minimum up to 5x annual salary or $500,000 (guarantee issue up to $100,000)</li>
                <li><strong>Spouse:</strong> $5,000 minimum up to $100,000 (guarantee issue up to $50,000)</li>
                <li><strong>Child(ren):</strong> $2,000–$10,000 (guarantee issue up to $10,000)</li>
            </ul>
            <p>⚠️ If you do not enroll during initial enrollment, future enrollment requires Evidence of Insurability (EOI) approval from Guardian.</p>

            <h3>♿ Disability Insurance</h3>
            <ul>
                <li><strong>Short-Term Disability:</strong> 60% of basic weekly earnings up to $1,250/week, after a 7-day elimination period. Benefits continue up to 12 weeks. <em>Employee pays the premium.</em></li>
                <li><strong>Long-Term Disability:</strong> 60% of basic monthly earnings up to $10,000/month, after a 90-day waiting period. <em>AAP pays 100% of the premium.</em></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with tab4:
        st.markdown("""
        <div class="content-section">
            <h3>📞 Teladoc — Free Telehealth (Day 1)</h3>
            <p>Teladoc is a <strong>company-paid benefit effective on your date of hire</strong> — no copays,
            no appointments needed. Available to <strong>everyone in your household.</strong></p>
            <ul>
                <li>General Medical: Board-certified clinicians by phone or video, 24/7</li>
                <li>Mental Health: Connect with a therapist or psychiatrist, 7 days/week</li>
                <li>Access at Teladoc.com or by calling 1-800-835-2362</li>
            </ul>

            <h3>🤝 Employee Assistance Program — LifeMatters (Day 1)</h3>
            <p>Free, confidential counseling and support services available <strong>24/7/365</strong> to you
            and your eligible dependents.</p>
            <ul>
                <li>Stress, depression, and personal problems</li>
                <li>Balancing work and personal needs</li>
                <li>Family and relationship concerns</li>
                <li>Financial consultation and legal consultation</li>
                <li>Child and elder care resources</li>
            </ul>
            <p>Call: <strong>1-800-634-6433</strong> | Web: mylifematters.com (password: AAP1)</p>

            <h3>🎁 Employee Perks — BenefitHub</h3>
            <p>AAP has partnered with BenefitHub to give you access to discounts on travel, entertainment,
            restaurants, auto, electronics, fitness, and more — across 1,000s of brands including Hertz,
            Groupon, Sam's Club, Dell, and Legoland.</p>
            <ul>
                <li>Register at: <strong>aapperks.benefithub.com</strong></li>
                <li>Referral Code: <strong>9Y7G26</strong></li>
            </ul>

            <h3>📚 LinkedIn Learning (Day 1)</h3>
            <p>AAP provides a company-paid LinkedIn Learning subscription effective on your date of hire.
            Access over 16,000 courses in business, technology, personal development, and more.
            Check your email for your activation invitation from HR.</p>

            <h3>📱 Verizon Wireless Discount</h3>
            <p>AAP employees are eligible for a <strong>22% discount</strong> on Verizon Wireless.
            The account must be in your name. Ask HR for details.</p>
        </div>
        """, unsafe_allow_html=True)

    with tab5:
        st.markdown("""
        <div class="content-section">
            <h3>Full-Time vs. Part-Time: Key Differences</h3>
            <p>Full-time employees work <strong>30+ hours per week.</strong> Part-time employees work
            <strong>fewer than 30 hours per week.</strong> Any part-time employee who averages 30+ scheduled
            hours per week over a 6-month rolling period will be reclassified as full-time.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <table class="styled-table">
            <tr><th>Benefit</th><th>Full-Time</th><th>Part-Time</th></tr>
            <tr><td>Vacation Time</td><td>✅ Accrues weekly based on tenure</td><td>❌ Not eligible</td></tr>
            <tr><td>Personal Time</td><td>✅ Lump sum annually</td><td>✅ 1 hr per 30 hrs worked</td></tr>
            <tr><td>Paid Holidays</td><td>✅ 8 paid holidays</td><td>✅ 8 paid holidays</td></tr>
            <tr><td>Health/Dental/Vision</td><td>✅ After 60 days</td><td>❌ Not eligible</td></tr>
            <tr><td>401(k)</td><td>✅ After 60 days</td><td>✅ After 1 year + 1,000 hours</td></tr>
            <tr><td>Company-Paid Life Insurance</td><td>✅ After 60 days</td><td>❌ Not eligible</td></tr>
            <tr><td>Long-Term Disability</td><td>✅ After 60 days</td><td>❌ Not eligible</td></tr>
            <tr><td>Long-Term Sick Leave</td><td>✅ After 4 years</td><td>❌ Not eligible</td></tr>
            <tr><td>Teladoc</td><td>✅ Day 1</td><td>✅ Day 1</td></tr>
            <tr><td>LinkedIn Learning</td><td>✅ Day 1</td><td>✅ Day 1</td></tr>
            <tr><td>EAP / LifeMatters</td><td>✅ Day 1</td><td>✅ Day 1</td></tr>
        </table>
        """, unsafe_allow_html=True)

    st.markdown("### ✅ Module 4 Checklist")
    checklist_items = {
        "vacation_schedule": "I understand the vacation accrual schedule and when I become eligible.",
        "personal_leave": "I understand personal leave amounts and that they do not roll over.",
        "holidays": "I know the 6 standard paid holidays plus 2 floating holidays.",
        "medical_plans": "I understand the two medical plan options (PPO and HDHP/HSA).",
        "dental_vision": "I know dental and vision are available through Guardian.",
        "401k": "I understand the 401k match formula and immediate vesting.",
        "life_insurance": "I know AAP provides basic life insurance at no cost to me.",
        "teladoc": "I know Teladoc is free, effective Day 1, and available to my household.",
        "eap": "I know the EAP (LifeMatters) is free, confidential, and available 24/7.",
        "benefithub": "I know about the BenefitHub perks program and the referral code.",
        "ft_pt_diff": "I understand the key differences between full-time and part-time benefits.",
    }

    mk = "benefits"
    if mk not in st.session_state.checklist_items or not st.session_state.checklist_items[mk]:
        st.session_state.checklist_items[mk] = {k: False for k in checklist_items}

    changed = False
    for key, label in checklist_items.items():
        val = st.checkbox(label, value=st.session_state.checklist_items[mk].get(key, False), key=f"{mk}_chk_{key}")
        if val != st.session_state.checklist_items[mk].get(key, False):
            st.session_state.checklist_items[mk][key] = val
            changed = True
    if changed:
        update_progress(mk)

    st.markdown("### 📝 Module 4 Quiz")
    if st.session_state.quiz_results.get(mk) is not None:
        score = st.session_state.quiz_results[mk]
        st.success(f"✅ Quiz completed! You scored {score}/5.")
    else:
        with st.form("quiz_benefits"):
            q1 = st.radio("1. Medical, dental, and vision benefits become effective on:",
                ["Your first day of work",
                 "The 1st of the month following 60 days of employment",
                 "After 90 days of employment",
                 "January 1 of the following year"], key="b_q1", index=None)
            q2 = st.radio("2. What is AAP's 401(k) match for the first 3% you contribute?",
                ["50%", "75%", "100%", "200%"], key="b_q2", index=None)
            q3 = st.radio("3. Teladoc is available to:",
                ["Full-time employees only",
                 "Full-time and part-time employees",
                 "Everyone in your household, effective Day 1",
                 "Employees after 60 days of service"], key="b_q3", index=None)
            q4 = st.radio("4. Long-Term Sick Leave requires that the absence be:",
                ["Any absence longer than 1 day",
                 "Any physician-mandated absence",
                 "At least 3 consecutive days mandated by a physician",
                 "At least 5 consecutive days"], key="b_q4", index=None)
            q5 = st.radio("5. Part-time employees are eligible for which of the following?",
                ["Vacation accrual",
                 "Company-paid life insurance",
                 "Health insurance after 60 days",
                 "Teladoc and LinkedIn Learning from Day 1"], key="b_q5", index=None)
            submitted = st.form_submit_button("Submit Quiz")
            if submitted:
                score = sum([
                    q1 == "The 1st of the month following 60 days of employment",
                    q2 == "100%",
                    q3 == "Everyone in your household, effective Day 1",
                    q4 == "At least 3 consecutive days mandated by a physician",
                    q5 == "Teladoc and LinkedIn Learning from Day 1",
                ])
                st.session_state.quiz_results[mk] = score
                update_progress(mk)
                st.rerun()

# ─────────────────────────────────────────────
#  MODULE 5 — FIRST STEPS
# ─────────────────────────────────────────────
def show_module_firststeps():
    st.markdown("""
    <div class="content-section">
        <h2>🚀 Module 5: Your First Steps</h2>
        <p>This module covers everything you need to get set up and hit the ground running on Day 1 and beyond.</p>

        <h3>📋 Documents to Sign at Hire</h3>
        <ul>
            <li>Payroll Direct Deposit</li>
            <li>Employee Acknowledgment Form</li>
            <li>Employee Code of Conduct</li>
            <li>Employee Withholding (W-4 and A-4)</li>
            <li>Confidentiality &amp; Non-Disclosure Agreement</li>
            <li>Form: Employee Medical Information</li>
            <li>"No Sexual Harassment" Statement</li>
            <li>Overtime / Company Premises Memo</li>
            <li>DEA Applicant Information Release Authorization</li>
            <li>Motor Vehicle Report Release Form</li>
            <li>Drug Policy Acknowledgment</li>
            <li>Employee's Responsibility to Report Drug Diversion</li>
            <li>API Staff Alerts</li>
            <li>Form I-9 (Employment Eligibility Verification)</li>
            <li>Employee Handbook Acknowledgment</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="content-section">
        <h3>💻 Systems You'll Use</h3>

        <h3>Paylocity — Payroll & HR Self-Service</h3>
        <p>Paylocity is AAP's payroll platform where you'll view pay stubs, manage direct deposit, and access
        tax forms. <strong>API Company ID: 123959</strong></p>
        <p>To register: Go to <strong>access.paylocity.com</strong>, click "Register New User," and enter your
        Company ID, last name, SSN, and home zip code. You'll set up a username, password, and security questions.</p>

        <h3>BambooHR — Employee Records & Directory</h3>
        <p>BambooHR is AAP's HRIS (HR Information System). You'll use it to access your employee records, view
        the company directory, and more. HR will walk you through BambooHR navigation during orientation.
        Be sure to <strong>upload your profile photo</strong> after logging in.</p>

        <h3>LinkedIn Learning — Professional Development</h3>
        <p>You should have received an activation email when you were offered the position. If you didn't receive
        it, contact HR. LinkedIn Learning gives you access to <strong>over 16,000 courses</strong> in business,
        technology, and personal development — available on any device, at your own pace.</p>

        <h3>Teladoc — Free Telehealth</h3>
        <p>Set up your Teladoc account by visiting <strong>Teladoc.com</strong> and clicking "Get Started."
        Select your health insurance plan from the drop-down and confirm coverage. Once set up, general medical
        visits, mental health visits, and more are <strong>completely free.</strong></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="content-section">
        <h3>👥 Key Contacts</h3>
    </div>
    """, unsafe_allow_html=True)

    contacts = [
        ("Brandy Hooper", "VP of Human Resources", "brandy.hooper@rxaap.com", "256-574-7526"),
        ("Nicole Thornton", "HR Administrator (API)", "nicole.thornton@apirx.com", "256-574-7528"),
        ("CBIZ Benefits", "Benefits Broker", "844.200.CBIZ (2249)", ""),
        ("Teladoc", "Free Telehealth", "800-835-2362 | Teladoc.com", ""),
        ("LifeMatters EAP", "Employee Assistance", "800-634-6433 | mylifematters.com", ""),
        ("BCBS of Alabama", "Medical Insurance", "888-267-2955 | bcbsal.org", ""),
        ("Guardian", "Dental, Vision, Life, Disability", "888-482-7342 | guardiananytime.com", ""),
        ("HealthEquity", "HSA Accounts", "866-274-9887 | healthequity.com", ""),
    ]

    st.markdown("""
    <table class="styled-table">
        <tr><th>Name / Resource</th><th>Role</th><th>Contact</th></tr>
    """ + "".join(
        f"<tr><td><b>{c[0]}</b></td><td>{c[1]}</td><td>{c[2]}{(' | ' + c[3]) if c[3] else ''}</td></tr>"
        for c in contacts
    ) + "</table>", unsafe_allow_html=True)

    st.markdown("""
    <div class="content-section">
        <h3>📆 What to Expect in Your First 90 Days</h3>
        <ul>
            <li><strong>Days 1–30:</strong> Complete orientation, sign all paperwork, get access to systems,
            meet your team, shadow key processes, and complete 30-day survey.</li>
            <li><strong>Days 31–60:</strong> Begin independently executing your core responsibilities with
            supervisor support. Complete your 60-day survey. Become eligible for most benefits.</li>
            <li><strong>Days 61–90:</strong> Build confidence and consistency in your role. Identify opportunities
            for improvement. Full introductory period concludes.</li>
        </ul>

        <h3>📬 Important Policies to Remember Going Forward</h3>
        <ul>
            <li>Update HR immediately with any personal data changes (address, dependents, emergency contacts).</li>
            <li>If you have a qualifying life event (marriage, birth, etc.), notify HR within <strong>30 days</strong>
            to make benefits changes.</li>
            <li>Performance evaluations are conducted approximately every 12 months from your hire anniversary.</li>
            <li>AAP is an at-will employer — either party may end the relationship at any time for any lawful reason.</li>
            <li>Report all concerns through the problem resolution process — starting with your supervisor,
            then escalating to HR and management if needed.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ✅ Module 5 Checklist")
    checklist_items = {
        "paperwork": "I understand which documents I need to sign during orientation.",
        "paylocity": "I know how to register for Paylocity (Company ID: 123959).",
        "bamboohr": "I understand what BambooHR is used for and that I need to upload my photo.",
        "linkedin": "I have received or know how to request my LinkedIn Learning activation.",
        "teladoc_setup": "I know how to set up my Teladoc account.",
        "key_contacts": "I know who to contact for HR, benefits, payroll, and telehealth questions.",
        "first90": "I understand what is expected of me in my first 30, 60, and 90 days.",
        "at_will": "I understand AAP is an at-will employer.",
        "life_event": "I know I have 30 days to notify HR of qualifying life events for benefits changes.",
    }

    mk = "firststeps"
    if mk not in st.session_state.checklist_items or not st.session_state.checklist_items[mk]:
        st.session_state.checklist_items[mk] = {k: False for k in checklist_items}

    changed = False
    for key, label in checklist_items.items():
        val = st.checkbox(label, value=st.session_state.checklist_items[mk].get(key, False), key=f"{mk}_chk_{key}")
        if val != st.session_state.checklist_items[mk].get(key, False):
            st.session_state.checklist_items[mk][key] = val
            changed = True
    if changed:
        update_progress(mk)

    st.markdown("### 📝 Module 5 Quiz")
    if st.session_state.quiz_results.get(mk) is not None:
        score = st.session_state.quiz_results[mk]
        st.success(f"✅ Quiz completed! You scored {score}/4.")
    else:
        with st.form("quiz_firststeps"):
            q1 = st.radio("1. What is the Paylocity Company ID for API employees?",
                ["123456", "123959", "987654", "112358"], key="f_q1", index=None)
            q2 = st.radio("2. How many days do you have to notify HR of a qualifying life event for benefits changes?",
                ["7 days", "14 days", "30 days", "60 days"], key="f_q2", index=None)
            q3 = st.radio("3. Which of the following is available to you on your very first day of employment?",
                ["Medical insurance",
                 "Vacation accrual",
                 "Teladoc and LinkedIn Learning",
                 "401(k) enrollment"], key="f_q3", index=None)
            q4 = st.radio("4. AAP's employment relationship is best described as:",
                ["Guaranteed for a fixed term",
                 "At-will, meaning either party may end employment at any time for any lawful reason",
                 "Protected by a union contract",
                 "Governed by a mandatory 2-year commitment"], key="f_q4", index=None)
            submitted = st.form_submit_button("Submit Quiz")
            if submitted:
                score = sum([
                    q1 == "123959",
                    q2 == "30 days",
                    q3 == "Teladoc and LinkedIn Learning",
                    q4 == "At-will, meaning either party may end employment at any time for any lawful reason",
                ])
                st.session_state.quiz_results[mk] = score
                update_progress(mk)
                st.rerun()

    # Completion check
    total_pct = int(sum(st.session_state.progress.values()) / len(MODULES))
    if total_pct == 100:
        st.markdown("""
        <div class="content-section" style="border-left:4px solid #2ecc71;text-align:center;padding:36px;">
            <h2 style="color:#2ecc71;">🎉 Congratulations!</h2>
            <p style="font-size:1.1rem;">You have completed all five AAP orientation modules.
            Welcome to the team — we're glad you're here!</p>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  ROUTER
# ─────────────────────────────────────────────
module_map = {
    "welcome": show_module_welcome,
    "conduct": show_module_conduct,
    "policies": show_module_policies,
    "benefits": show_module_benefits,
    "firststeps": show_module_firststeps,
}

selected = st.session_state.selected_module
if selected and selected in module_map:
    module_map[selected]()
else:
    show_home()
