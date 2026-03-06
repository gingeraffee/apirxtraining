import streamlit as st
import json
import os
import base64
import gspread
from datetime import datetime
from textwrap import dedent

# ─────────────────────────────────────────────
#  CORE UTILS & ASSETS
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

    /* Global Variables */
    :root {{
        --primary-red: #B11226;
        --deep-navy: #0A1128;
        --glass-white: rgba(255, 255, 255, 0.85);
        --border-subtle: rgba(226, 232, 240, 0.8);
    }}

    /* Background Layering */
    .stApp {{
        background: radial-gradient(at 0% 0%, rgba(177, 18, 38, 0.03) 0px, transparent 50%),
                    radial-gradient(at 100% 100%, rgba(10, 17, 40, 0.03) 0px, transparent 50%),
                    #F8FAFC;
    }}

    /* Sidebar - High Contrast Glass */
    [data-testid="stSidebar"] {{
        background: var(--deep-navy) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255,255,255,0.05);
    }}

    /* Typography Overrides */
    h1, h2, h3 {{ font-family: 'Playfair Display', serif !important; color: var(--deep-navy) !important; font-weight: 700 !important; }}
    p, li, label, .stMarkdown {{ font-family: 'Inter', sans-serif !important; color: #334155 !important; line-height: 1.6; }}

    /* Premium Hero Component */
    .hero-banner {{
        background: linear-gradient(135deg, #0A1128 0%, #1C2C54 100%);
        padding: 60px;
        border-radius: 24px;
        color: white !important;
        margin-bottom: 40px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    }}
    .hero-banner h1 {{ color: white !important; font-size: 3.2rem !important; margin: 0; }}
    .hero-banner p {{ color: rgba(255,255,255,0.7) !important; font-size: 1.2rem !important; max-width: 800px; }}

    /* Content Cards */
    .premium-card {{
        background: var(--glass-white);
        backdrop-filter: blur(10px);
        border: 1px solid var(--border-subtle);
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.03);
        margin-bottom: 24px;
        transition: transform 0.3s ease;
    }}
    .premium-card:hover {{ transform: translateY(-4px); box-shadow: 0 15px 35px rgba(0,0,0,0.06); }}

    /* Styled Login Container */
    .login-box {{
        max-width: 450px;
        margin: 80px auto;
        background: white;
        padding: 50px;
        border-radius: 30px;
        box-shadow: 0 30px 60px rgba(0,0,0,0.1);
        text-align: center;
    }}

    /* Button Styling */
    .stButton>button {{
        background: var(--primary-red) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: 0.3s !important;
        width: 100%;
    }}
    .stButton>button:hover {{ opacity: 0.9; transform: scale(1.02); }}

    /* Progress & Tabs */
    .stProgress > div > div > div > div {{ background-color: var(--primary-red) !important; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 24px; }}
    .stTabs [data-baseweb="tab"] {{ font-family: 'Inter'; font-weight: 600; color: #94A3B8; }}
    .stTabs [aria-selected="true"] {{ color: var(--primary-red) !important; border-bottom-color: var(--primary-red) !important; }}
</style>
""")

# ─────────────────────────────────────────────
#  STATE MANAGEMENT
# ─────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_module" not in st.session_state:
    st.session_state.current_module = "welcome"

# ─────────────────────────────────────────────
#  LOGIN PAGE (PREMIUM)
# ─────────────────────────────────────────────
def show_login():
    render_html(f"""
    <div class="login-box">
        <img src="{_logo_img_src()}" width="200" style="margin-bottom:30px;">
        <h2>Employee Portal</h2>
        <p>Please enter your credentials to begin your journey with AAP.</p>
    </div>
    """)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            user = st.text_input("Username")
            track = st.selectbox("Position Track", ["Office/Management", "Warehouse Operations"])
            if st.button("Begin Orientation"):
                if user.strip():
                    st.session_state.authenticated = True
                    st.session_state.user_name = user
                    st.session_state.role_track = "warehouse" if "Warehouse" in track else "office"
                    st.rerun()

# ─────────────────────────────────────────────
#  MODULES: WAREHOUSE
# ─────────────────────────────────────────────
def show_wh_welcome():
    render_html(f"""
    <div class="hero-banner">
        <span style="text-transform:uppercase; letter-spacing:3px; font-size:0.8rem; opacity:0.7;">Module 01</span>
        <h1>Warehouse Operations</h1>
        <p>Welcome, {st.session_state.user_name}. You are the heartbeat of API operations.</p>
    </div>
    <div class="premium-card">
        <h2>A Mission of Excellence</h2>
        <p>Since 2009, AAP has grown into a national cooperative of 2,000+ independent pharmacies. Our Scottsboro facility is the logistics hub that makes patient care possible.</p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 30px;">
            <div style="padding:20px; background:#F1F5F9; border-radius:15px; border-left:4px solid var(--primary-red);">
                <h4 style="margin:0; font-size:0.9rem; color:var(--primary-red);">OUR MISSION</h4>
                <p style="margin:0; font-size:0.95rem;">To enhance profitability and improve patient care.</p>
            </div>
            <div style="padding:20px; background:#F1F5F9; border-radius:15px; border-left:4px solid var(--deep-navy);">
                <h4 style="margin:0; font-size:0.9rem; color:var(--deep-navy);">OUR VISION</h4>
                <p style="margin:0; font-size:0.95rem;">Helping independent pharmacies thrive in a competitive market.</p>
            </div>
        </div>
    </div>
    """)
    st.checkbox("I understand the mission and my role within it.")

# ─────────────────────────────────────────────
#  APP ROUTER
# ─────────────────────────────────────────────
if not st.session_state.authenticated:
    show_login()
else:
    # Sidebar Navigation
    with st.sidebar:
        st.markdown(f'<div style="text-align: center; padding: 20px 0;"><img src="{_logo_img_src()}" width="160"></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.session_state.role_track == "warehouse":
            nav_options = {"Dashboard": "welcome", "Safety": "safety", "Benefits": "benefits"}
        else:
            nav_options = {"Dashboard": "welcome", "Conduct": "conduct", "Benefits": "benefits"}
            
        selection = st.radio("Navigation", list(nav_options.keys()))
        st.session_state.current_module = nav_options[selection]
        
        st.markdown("---")
        st.caption(f"Logged in as: {st.session_state.user_name}")
        if st.button("Log Out"):
            st.session_state.authenticated = False
            st.rerun()

    # Page Rendering
    if st.session_state.current_module == "welcome":
        show_wh_welcome()
    else:
        render_html("""
        <div class="premium-card">
            <h2>Under Construction</h2>
            <p>This module is being stylized to meet the new premium standards.</p>
        </div>
        """)