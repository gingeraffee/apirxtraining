import streamlit as st
import os
import base64
from textwrap import dedent

# ─────────────────────────────────────────────
#  PAGE CONFIG & ASSETS
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AAP | Premium Onboarding",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

COMPANY_LOGO_URL = "https://rxaap.com/wp-content/uploads/2021/03/AAP_Logo_White.png"
API_LOGO_PATH = "assets/api_logo.png"

def _logo_img_src():
    """Returns base64 for local asset or URL for fallback."""
    if os.path.exists(API_LOGO_PATH):
        with open(API_LOGO_PATH, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{b64}"
    return COMPANY_LOGO_URL

def render_html(content: str):
    st.markdown(dedent(content).strip(), unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PREMIUM DESIGN SYSTEM (CSS)
# ─────────────────────────────────────────────
render_html(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');

    :root {{
        --primary-accent: #B11226; /* Crimson Red */
        --deep-midnight: #0A1128;
        --glass-bg: rgba(255, 255, 255, 0.95);
        --text-main: #334155;
    }}

    /* Global Background */
    .stApp {{
        background: radial-gradient(at 0% 0%, rgba(177, 18, 38, 0.05) 0px, transparent 50%),
                    radial-gradient(at 100% 100%, rgba(10, 17, 40, 0.05) 0px, transparent 50%),
                    #F8FAFC;
    }}

    /* Sidebar Refinement */
    [data-testid="stSidebar"] {{
        background-color: var(--deep-midnight) !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }}
    [data-testid="stSidebar"] * {{ color: white !important; }}

    /* Typography */
    h1, h2, h3 {{ font-family: 'Playfair Display', serif !important; color: var(--deep-midnight) !important; font-weight: 700 !important; }}
    p, li, label, .stMarkdown {{ font-family: 'Inter', sans-serif !important; color: var(--text-main) !important; line-height: 1.7; }}

    /* Components: Hero Banner */
    .hero-banner {{
        background: linear-gradient(135deg, #0A1128 0%, #1C2C54 100%);
        padding: 60px;
        border-radius: 30px;
        color: white !important;
        margin-bottom: 40px;
        box-shadow: 0 20px 50px rgba(10, 17, 40, 0.2);
    }}
    .hero-banner h1 {{ color: white !important; font-size: 3.5rem !important; margin-bottom: 10px; }}
    .hero-banner p {{ color: rgba(255,255,255,0.7) !important; font-size: 1.2rem !important; }}

    /* Components: Premium Card */
    .premium-card {{
        background: var(--glass-bg);
        padding: 40px;
        border-radius: 24px;
        border: 1px solid rgba(226, 232, 240, 0.8);
        box-shadow: 0 10px 30px rgba(0,0,0,0.02);
        margin-bottom: 24px;
        transition: transform 0.3s ease;
    }}
    .premium-card:hover {{ transform: translateY(-5px); box-shadow: 0 15px 40px rgba(0,0,0,0.05); }}

    /* Login Form Styling */
    .login-container {{
        background: white;
        padding: 50px;
        border-radius: 35px;
        box-shadow: 0 40px 100px rgba(0,0,0,0.1);
        text-align: center;
        margin-top: 50px;
    }}

    /* Buttons */
    div.stButton > button {{
        background: var(--primary-accent) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 15px 30px !important;
        font-weight: 600 !important;
        width: 100%;
        transition: 0.3s;
    }}
    div.stButton > button:hover {{ transform: scale(1.02); opacity: 0.9; }}
</style>
""")

# ─────────────────────────────────────────────
#  APP STATE LOGIC
# ─────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "role_track" not in st.session_state:
    st.session_state.role_track = "office"

# ─────────────────────────────────────────────
#  LOGIN VIEW
# ─────────────────────────────────────────────
def show_login():
    _, col, _ = st.columns([1, 1.8, 1])
    with col:
        render_html(f"""
        <div class="login-container">
            <img src="{_logo_img_src()}" width="240" style="margin-bottom:30px;">
            <h2 style="margin-bottom:10px;">Employee Portal</h2>
            <p style="margin-bottom:40px; color:#64748b;">Welcome to the family. Please verify your identity to begin.</p>
        </div>
        """)
        
        # Streamlit widgets must be outside raw HTML strings to function properly
        name = st.text_input("Full Name", placeholder="Enter your full name")
        role = st.selectbox("Position Track", ["Warehouse Operations", "Office & Management"])
        access_code = st.text_input("Security Access Code", type="password")
        
        if st.button("Initialize Orientation"):
            if name.strip() and access_code == "AAP2026": # Mock security code
                st.session_state.authenticated = True
                st.session_state.user_name = name
                st.session_state.role_track = "warehouse" if "Warehouse" in role else "office"
                st.rerun()
            else:
                st.error("Please provide your name and the correct access code.")

# ─────────────────────────────────────────────
#  MODULE CONTENT: WAREHOUSE
# ─────────────────────────────────────────────
def module_wh_welcome():
    render_html(f"""
    <div class="hero-banner">
        <span style="letter-spacing:3px; font-weight:600; opacity:0.7; font-size:0.8rem;">MODULE 01</span>
        <h1>Welcome, {st.session_state.user_name}</h1>
        <p>Your journey at API/AAP starts here. You are the vital link in the community healthcare chain.</p>
    </div>
    
    <div class="premium-card">
        <h3>Our Mission & Vision</h3>
        <p>Since 2009, AAP has grown into a national cooperative of 2,000+ pharmacies. At our Scottsboro facility, you ensure every order is handled with the precision our partners deserve.</p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top:30px;">
            <div style="background:#F1F5F9; padding:25px; border-radius:15px; border-left:5px solid var(--primary-accent);">
                <small style="color:var(--primary-accent); font-weight:bold;">MISSION</small>
                <p style="margin:0; font-size:0.95rem;">Enhancing profitability and improving patient care for independent pharmacies.</p>
            </div>
            <div style="background:#F1F5F9; padding:25px; border-radius:15px; border-left:5px solid var(--deep-midnight);">
                <small style="color:var(--deep-midnight); font-weight:bold;">VISION</small>
                <p style="margin:0; font-size:0.95rem;">To be the premier partner for community pharmacies nationwide.</p>
            </div>
        </div>
    </div>
    """)
    st.checkbox("I have read and understood the Warehouse Welcome.")

def module_wh_safety():
    render_html("""
    <div class="premium-card">
        <h2>Safety First. Always.</h2>
        <p>In a high-velocity warehouse environment, safety isn't just a rule—it's our culture.</p>
        <ul>
            <li><b>PPE:</b> High-visibility vests and safety shoes are mandatory in active zones.</li>
            <li><b>Equipment:</b> Do not operate forklifts or pallet jacks unless certified.</li>
            <li><b>Reporting:</b> Report all "near-misses" immediately to your floor lead.</li>
        </ul>
    </div>
    """)
    st.info("💡 Remember: Safety is everyone's responsibility.")
    st.checkbox("I agree to follow all safety protocols.")

# ─────────────────────────────────────────────
#  MODULE CONTENT: OFFICE
# ─────────────────────────────────────────────
def module_office_welcome():
    render_html(f"""
    <div class="hero-banner" style="background: linear-gradient(135deg, #B11226 0%, #7A0C1A 100%);">
        <span style="letter-spacing:3px; font-weight:600; opacity:0.8; font-size:0.8rem;">MANAGEMENT TRACK</span>
        <h1>Excellence in Leadership</h1>
        <p>Welcome, {st.session_state.user_name}. We are glad to have your expertise at the corporate level.</p>
    </div>
    <div class="premium-card">
        <h2>Corporate Strategy</h2>
        <p>At the office level, we focus on member relations, procurement strategy, and business development to support our 2,000+ independent owners.</p>
    </div>
    """)

# ─────────────────────────────────────────────
#  MAIN ROUTER
# ─────────────────────────────────────────────
if not st.session_state.authenticated:
    show_login()
else:
    # Sidebar
    with st.sidebar:
        st.markdown(f'<div style="text-align: center; padding: 20px 0;"><img src="{_logo_img_src()}" width="160"></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.session_state.role_track == "warehouse":
            nav = st.radio("Orientation Path", ["Dashboard", "Safety & OSHA", "Benefits", "First Steps"])
        else:
            nav = st.radio("Orientation Path", ["Dashboard", "Code of Conduct", "Policy Overview", "Benefits"])
            
        st.markdown("---")
        st.progress(25)
        st.caption("Module 1 of 4 Complete")
        
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()

    # Dashboard/Module Selection
    if nav == "Dashboard":
        if st.session_state.role_track == "warehouse":
            module_wh_welcome()
        else:
            module_office_welcome()
    elif nav == "Safety & OSHA":
        module_wh_safety()
    else:
        render_html("""
        <div class="premium-card" style="text-align:center; padding:100px;">
            <h3>Module Optimized</h3>
            <p>We are currently polishing this section for the premium experience. Please check back in a few minutes.</p>
        </div>
        """)
        import streamlit as st
import os
import base64
from textwrap import dedent

# ─────────────────────────────────────────────
#  1. PAGE CONFIG & ASSETS
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AAP | Elite Onboarding",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

COMPANY_LOGO_URL = "https://rxaap.com/wp-content/uploads/2021/03/AAP_Logo_White.png"
API_LOGO_PATH = "assets/api_logo.png"

def _logo_img_src():
    if os.path.exists(API_LOGO_PATH):
        with open(API_LOGO_PATH, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{b64}"
    return COMPANY_LOGO_URL

def render_html(content: str):
    st.markdown(dedent(content).strip(), unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  2. PREMIUM DESIGN SYSTEM (CSS)
# ─────────────────────────────────────────────
render_html(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');

    :root {{
        --primary-accent: #B11226; /* AAP Crimson */
        --deep-midnight: #0A1128; /* Professional Navy */
        --glass-white: rgba(255, 255, 255, 0.9);
        --border-subtle: rgba(226, 232, 240, 0.8);
    }}

    /* Background Canvas */
    .stApp {{
        background: radial-gradient(at 0% 0%, rgba(177, 18, 38, 0.04) 0px, transparent 50%),
                    radial-gradient(at 100% 100%, rgba(10, 17, 40, 0.04) 0px, transparent 50%),
                    #F8FAFC;
    }}

    /* Typography Hierarchy */
    h1, h2, h3 {{ font-family: 'Playfair Display', serif !important; color: var(--deep-midnight) !important; font-weight: 700 !important; }}
    p, li, label, .stMarkdown {{ font-family: 'Inter', sans-serif !important; color: #334155 !important; line-height: 1.7; font-size: 1.05rem !important; }}

    /* Sidebar Refinement */
    [data-testid="stSidebar"] {{
        background-color: var(--deep-midnight) !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }}
    [data-testid="stSidebar"] * {{ color: white !important; font-family: 'Inter', sans-serif !important; }}

    /* Layout Components */
    .hero-banner {{
        background: linear-gradient(135deg, #0A1128 0%, #1C2C54 100%);
        padding: 60px;
        border-radius: 32px;
        color: white !important;
        margin-bottom: 40px;
        box-shadow: 0 20px 50px rgba(10, 17, 40, 0.15);
        position: relative;
        overflow: hidden;
    }}
    .hero-banner h1 {{ color: white !important; font-size: 3.2rem !important; margin: 0; }}
    .hero-banner p {{ color: rgba(255,255,255,0.7) !important; font-size: 1.2rem !important; margin-top: 10px; }}

    .premium-card {{
        background: var(--glass-white);
        backdrop-filter: blur(10px);
        padding: 40px;
        border-radius: 24px;
        border: 1px solid var(--border-subtle);
        box-shadow: 0 10px 30px rgba(0,0,0,0.02);
        margin-bottom: 24px;
    }}

    /* Form Elements & Buttons */
    div.stButton > button {{
        background: var(--primary-accent) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        font-weight: 600 !important;
        width: 100%;
        transition: 0.3s;
        margin-top: 15px;
    }}
    div.stButton > button:hover {{ transform: translateY(-2px); box-shadow: 0 10px 20px rgba(177, 18, 38, 0.2); }}

    /* Information Grid */
    .info-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
    .info-item {{ background: #F1F5F9; padding: 25px; border-radius: 16px; border-left: 4px solid var(--primary-accent); }}
</style>
""")

# ─────────────────────────────────────────────
#  3. SESSION STATE INITIALIZATION
# ─────────────────────────────────────────────
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'role_track' not in st.session_state:
    st.session_state.role_track = "office"
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"

# ─────────────────────────────────────────────
#  4. LOGIN VIEW
# ─────────────────────────────────────────────
def show_login():
    # Use columns to center the login container
    _, col, _ = st.columns([1, 1.8, 1])
    with col:
        render_html(f"""
        <div style="background: white; padding: 60px; border-radius: 35px; box-shadow: 0 40px 100px rgba(0,0,0,0.1); text-align: center; margin-top: 60px;">
            <img src="{_logo_img_src()}" width="240" style="margin-bottom:30px;">
            <h2 style="margin-bottom:10px;">Orientation Portal</h2>
            <p style="margin-bottom:40px; color:#64748b;">Welcome to AAP. Please enter your credentials to proceed.</p>
        </div>
        """)
        
        # Placing inputs in a container immediately following the stylized header
        with st.container():
            name = st.text_input("Full Name", placeholder="e.g. John Smith")
            role = st.selectbox("Department / Track", ["Office & Management", "Warehouse Operations"])
            # In production, replace the access code check with your real authentication
            access_code = st.text_input("Security Code", type="password", placeholder="Enter authorization code")
            
            if st.button("Access Portal"):
                if name.strip() and access_code == "AAP2024": # Simple mock check
                    st.session_state.authenticated = True
                    st.session_state.user_name = name
                    st.session_state.role_track = "warehouse" if "Warehouse" in role else "office"
                    st.rerun()
                else:
                    st.error("Invalid details. Please check your name and security code.")

# ─────────────────────────────────────────────
#  5. MODULE CONTENT (WAREHOUSE)
# ─────────────────────────────────────────────
def render_wh_welcome():
    render_html(f"""
    <div class="hero-banner">
        <span style="letter-spacing:2px; font-weight:600; opacity:0.8; font-size:0.8rem;">WAREHOUSE TRACK</span>
        <h1>Welcome, {st.session_state.user_name}</h1>
        <p>You are part of the engine that keeps independent pharmacies running.</p>
    </div>
    <div class="premium-card">
        <h2>A Message From Our CEO</h2>
        <p><em>"We believe that each employee contributes directly to AAP's growth and success... We hope that your experience here will be challenging, enjoyable, and rewarding."</em></p>
        <p style="font-weight:700; color:var(--primary-accent);">— Jon Copeland, R.Ph., CEO</p>
    </div>
    <div class="premium-card">
        <h3>The Engine of AAP</h3>
        <p>AAP is a national cooperative of over 2,000 independent pharmacies. At our API warehouse in Scottsboro, AL, we ensure pharmacies get what they need, when they need it.</p>
        <div class="info-grid">
            <div class="info-item">
                <small style="color:var(--primary-accent); font-weight:700;">OUR MISSION</small>
                <p>Enhancing profitability and improving patient care for community pharmacies.</p>
            </div>
            <div class="info-item" style="border-left-color: var(--deep-midnight);">
                <small style="color:var(--deep-midnight); font-weight:700;">OUR VISION</small>
                <p>To be the premier partner for independent pharmacies in a competitive market.</p>
            </div>
        </div>
    </div>
    """)
    st.checkbox("I have read and agree to the Warehouse Module 1 content.")

def render_wh_safety():
    render_html("""
    <div class="premium-card">
        <h2>Safety & Operational Excellence</h2>
        <p>Safety is not a checkbox; it is our foundation. Every team member is responsible for maintaining a secure environment.</p>
    </div>
    <div class="info-grid">
        <div class="premium-card">
            <h4>Mandatory PPE</h4>
            <ul>
                <li>High-Visibility Vests</li>
                <li>Safety Toed Shoes</li>
                <li>Gloves as required per station</li>
            </ul>
        </div>
        <div class="premium-card">
            <h4>OSHA Standards</h4>
            <p>We strictly adhere to OSHA guidelines. All accidents or "near-misses" must be reported within 24 hours.</p>
        </div>
    </div>
    """)
    st.checkbox("I confirm that I will follow all safety and PPE protocols.")

# ─────────────────────────────────────────────
#  6. MODULE CONTENT (OFFICE)
# ─────────────────────────────────────────────
def render_office_welcome():
    render_html(f"""
    <div class="hero-banner" style="background: linear-gradient(135deg, #B11226 0%, #7A0C1A 100%);">
        <span style="letter-spacing:2px; font-weight:600; opacity:0.8; font-size:0.8rem;">CORPORATE TRACK</span>
        <h1>Strategic Excellence</h1>
        <p>Welcome, {st.session_state.user_name}. Let's define the future of independent pharmacy.</p>
    </div>
    <div class="premium-card">
        <h2>Professional Standards</h2>
        <p>At the corporate level, your role involves representing AAP to over 2,000 pharmacy owners. We maintain the highest standards of integrity and communication.</p>
    </div>
    """)
    st.checkbox("I understand the corporate standards and my role in AAP.")

# ─────────────────────────────────────────────
#  7. THE ROUTER
# ─────────────────────────────────────────────
if not st.session_state.authenticated:
    show_login()
else:
    # Sidebar Navigation Logic
    with st.sidebar:
        st.markdown(f'<div style="text-align: center; padding: 20px 0;"><img src="{_logo_img_src()}" width="180"></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.session_state.role_track == "warehouse":
            nav_list = ["Dashboard", "Safety & Conduct", "Benefits", "First Steps"]
        else:
            nav_list = ["Dashboard", "Code of Conduct", "Corporate Policies", "Benefits"]
            
        st.session_state.current_page = st.radio("Navigation", nav_list)
        
        st.markdown("---")
        st.progress(33)
        st.caption("Orientation 33% Complete")
        
        if st.button("Sign Out"):
            st.session_state.authenticated = False
            st.rerun()

    # Page Rendering based on Nav selection
    if st.session_state.current_page == "Dashboard":
        if st.session_state.role_track == "warehouse":
            render_wh_welcome()
        else:
            render_office_welcome()
    elif st.session_state.current_page in ["Safety & Conduct", "Code of Conduct"]:
        if st.session_state.role_track == "warehouse":
            render_wh_safety()
        else:
            render_html("""<div class="premium-card"><h2>Code of Conduct</h2><p>Please refer to the employee handbook for the full AAP Professional Code of Conduct.</p></div>""")
    else:
        render_html(f"""
        <div class="premium-card" style="text-align:center; padding: 100px 0;">
            <h3>Module: {st.session_state.current_page}</h3>
            <p>We are currently finalizing the premium visual assets for this module. Content is available in your hard-copy handbook.</p>
        </div>
        """)