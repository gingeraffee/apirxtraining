import streamlit as st
import os
import base64
from textwrap import dedent

# ─────────────────────────────────────────────
#  CORE UTILS
# ─────────────────────────────────────────────
COMPANY_LOGO_URL = "https://rxaap.com/wp-content/uploads/2021/03/AAP_Logo_White.png"
API_LOGO_PATH = "assets/api_logo.png"

def _logo_img_src():
    if os.path.exists(API_LOGO_PATH):
        with open(API_LOGO_PATH, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{b64}"
    return COMPANY_LOGO_URL

st.set_page_config(
    page_title="AAP | Elite Onboarding",
    page_icon="✨",
    layout="wide",
)

def render_html(content: str):
    st.markdown(dedent(content).strip(), unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PREMIUM DESIGN SYSTEM (CSS)
# ─────────────────────────────────────────────
render_html(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');

    :root {{
        --primary-red: #B11226;
        --deep-navy: #0A1128;
        --glass-white: rgba(255, 255, 255, 0.9);
        --border-subtle: rgba(226, 232, 240, 0.8);
    }}

    .stApp {{
        background: radial-gradient(at 0% 0%, rgba(177, 18, 38, 0.03) 0px, transparent 50%),
                    radial-gradient(at 100% 100%, rgba(10, 17, 40, 0.03) 0px, transparent 50%),
                    #F8FAFC;
    }}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background: var(--deep-navy) !important;
        backdrop-filter: blur(15px);
    }}

    /* LOGIN CONTAINER - Now Auto-Scaling */
    .login-wrapper {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 40px 20px;
    }}

    .login-card {{
        background: white;
        padding: 60px;
        border-radius: 32px;
        box-shadow: 0 40px 100px rgba(0,0,0,0.08);
        width: 100%;
        max-width: 500px; /* Wider for all fields */
        text-align: center;
        border: 1px solid var(--border-subtle);
    }}

    h1, h2, h3 {{ font-family: 'Playfair Display', serif !important; color: var(--deep-navy) !important; }}
    p, label, .stMarkdown {{ font-family: 'Inter', sans-serif !important; color: #475569 !important; }}

    /* Hero Banner for Dashboard */
    .hero-banner {{
        background: linear-gradient(135deg, #0A1128 0%, #1C2C54 100%);
        padding: 60px;
        border-radius: 28px;
        color: white !important;
        margin-bottom: 40px;
        box-shadow: 0 20px 40px rgba(10, 17, 40, 0.15);
    }}
    .hero-banner h1 {{ color: white !important; margin: 0; font-size: 3rem !important; }}

    /* Premium Content Cards */
    .premium-card {{
        background: var(--glass-white);
        backdrop-filter: blur(10px);
        padding: 40px;
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.02);
        margin-bottom: 24px;
        border: 1px solid var(--border-subtle);
    }}

    /* Make buttons pop */
    div.stButton > button {{
        background: var(--primary-red) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 14px 28px !important;
        width: 100%;
        font-weight: 600 !important;
        margin-top: 20px;
    }}
</style>
""")

# ─────────────────────────────────────────────
#  STATE & LOGIN LOGIC
# ─────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def show_login():
    # We use a column layout to center the login card
    _, center_col, _ = st.columns([1, 2, 1])
    
    with center_col:
        render_html(f"""
        <div class="login-wrapper">
            <div class="login-card">
                <img src="{_logo_img_src()}" width="220" style="margin-bottom:30px;">
                <h2 style="margin-bottom:10px;">Welcome Back</h2>
                <p style="margin-bottom:30px;">Enter your details to access the AAP Orientation Portal.</p>
            </div>
        </div>
        """)
        
        # Inputs placed directly under the card styling for perfect fit
        with st.container():
            name = st.text_input("Full Name", placeholder="e.g. John Doe")
            track = st.selectbox("Your Department", ["Warehouse Operations", "Office / Corporate"])
            access_code = st.text_input("Access Code", type="password")
            
            if st.button("Begin Your Journey"):
                if name and access_code == "AAP2024": # Replace with your logic
                    st.session_state.authenticated = True
                    st.session_state.user_name = name
                    st.session_state.role_track = "warehouse" if "Warehouse" in track else "office"
                    st.rerun()
                else:
                    st.error("Please fill in all fields and use the correct access code.")

# ─────────────────────────────────────────────
#  DASHBOARD & MODULES
# ─────────────────────────────────────────────
def show_dashboard():
    role_label = "Logistics Expert" if st.session_state.role_track == "warehouse" else "Corporate Professional"
    
    render_html(f"""
    <div class="hero-banner">
        <span style="text-transform:uppercase; letter-spacing:2px; font-size:0.8rem; opacity:0.8;">Orientation Dashboard</span>
        <h1>Welcome, {st.session_state.user_name}</h1>
        <p>You are joining us as a <b>{role_label}</b>. Use the sidebar to navigate your modules.</p>
    </div>
    
    <div class="premium-card">
        <h3>Our Legacy</h3>
        <p>American Associated Pharmacies (AAP) represents the collective strength of over 2,000 independent pharmacies. Your role is critical in ensuring our members receive the support they need to provide community healthcare.</p>
    </div>
    """)

# ─────────────────────────────────────────────
#  MAIN APP ROUTER
# ─────────────────────────────────────────────
if not st.session_state.authenticated:
    show_login()
else:
    # Sidebar Navigation
    with st.sidebar:
        st.markdown(f'<div style="text-align: center; padding: 30px 0;"><img src="{_logo_img_src()}" width="180"></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        nav = st.radio("Navigation", ["Dashboard", "Code of Conduct", "Health & Safety", "Benefits"])
        
        st.markdown("---")
        if st.button("Sign Out"):
            st.session_state.authenticated = False
            st.rerun()

    # Page Content Logic
    if nav == "Dashboard":
        show_dashboard()
    else:
        render_html(f"""
        <div class="premium-card">
            <h2>{nav}</h2>
            <p>This module is currently being optimized for the premium experience. Please check back shortly.</p>
        </div>
        """)