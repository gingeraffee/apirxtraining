import streamlit as st
import streamlit.components.v1 as components
import json
import inspect
import os
import base64
import gspread
from datetime import datetime
from textwrap import dedent



def render_html(content: str):
    """Render HTML/Markdown blocks reliably by removing Python indentation."""
    st.markdown(inspect.cleandoc(content), unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
COMPANY_LOGO_URL = "https://rxaap.com/wp-content/uploads/2021/03/AAP_Logo_White.png"
API_LOGO_PATH = "assets/api_logo.png"
_sidebar_logo = API_LOGO_PATH if os.path.exists(API_LOGO_PATH) else COMPANY_LOGO_URL

def _logo_img_src():
    """Return an img src usable inside raw HTML: base64 for local file, URL otherwise."""
    if os.path.exists(API_LOGO_PATH):
        with open(API_LOGO_PATH, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{b64}"
    return COMPANY_LOGO_URL

st.set_page_config(
    page_title="AAP New Hire Orientation",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Native Streamlit logo — appears in the top-left corner of the sidebar
st.logo(_sidebar_logo, link="https://apirx.com")

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
render_html("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Outfit:wght@300;400;500;600;700;800&display=swap');

    /* ── Base ── */
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    :root {
        --accent: #E05A3A;
        --accent-soft: #FFEAE4;
        --accent-glow: rgba(224,90,58,0.35);
        --surface: #FFFFFF;
        --surface-raised: #FEFEFE;
        --surface-dim: #F7F5F2;
        --ink: #1A1A1E;
        --ink-muted: #6B6B76;
        --ink-faint: #A0A0AB;
        --border-default: rgba(0,0,0,0.06);
        --border-hover: rgba(0,0,0,0.12);
        --radius-lg: 22px;
        --radius-md: 16px;
        --radius-sm: 12px;
        --shadow-card: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.06);
        --shadow-card-hover: 0 4px 12px rgba(0,0,0,0.06), 0 20px 40px rgba(0,0,0,0.10);
        --shadow-elevated: 0 8px 30px rgba(0,0,0,0.08), 0 30px 60px rgba(0,0,0,0.12);
        --transition-smooth: cubic-bezier(0.22, 1, 0.36, 1);
    }
    .stApp {
        background:
            radial-gradient(ellipse 120% 80% at 10% 0%, rgba(224,90,58,0.06) 0%, transparent 50%),
            radial-gradient(ellipse 100% 70% at 90% 0%, rgba(251,191,36,0.05) 0%, transparent 45%),
            linear-gradient(180deg, #F9F8F5 0%, #F5F3EF 40%, #F2F0EC 100%);
    }

    /* ── Sidebar Container ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1C1C1E 0%, #232326 50%, #1C1C1E 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 0.9rem !important;
        padding-left: 0.9rem !important;
        padding-right: 0.9rem !important;
    }

    .sidebar-header {
        background: rgba(255,255,255,0.05);
        border-radius: var(--radius-md);
        padding: 16px 14px;
        margin-bottom: 16px;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .sidebar-header * { color: #F0F0F2 !important; }
    .sidebar-header .sidebar-username {
        color: #E0E0E4 !important;
        font-weight: 600 !important;
        letter-spacing: 0.01em !important;
    }

    .progress-container {
        width: 100%;
        height: 6px;
        border-radius: 999px;
        background: rgba(255,255,255,0.08);
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        border-radius: inherit;
        background: linear-gradient(90deg, var(--accent) 0%, #FBBF24 100%);
        box-shadow: 0 0 12px var(--accent-glow);
        transition: width 0.7s var(--transition-smooth);
    }
    .sidebar-section-label {
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        color: rgba(255,255,255,0.35);
        margin: 8px 2px 8px;
        font-weight: 700;
    }

    /* ── Sidebar Radio Navigation ── */
    [data-testid="stSidebar"] .stRadio > div { gap: 4px !important; }
    [data-testid="stSidebar"] .stRadio label {
        color: rgba(255,255,255,0.72) !important;
        border-radius: var(--radius-sm) !important;
        padding: 9px 12px !important;
        transition: all 0.3s var(--transition-smooth) !important;
        font-size: 0.82rem !important;
        width: 100% !important;
        border: 1px solid transparent !important;
        background: transparent !important;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        color: #FFFFFF !important;
        background: rgba(255,255,255,0.06) !important;
        transform: translateX(2px) !important;
    }
    [data-testid="stSidebar"] .stRadio p,
    [data-testid="stSidebar"] .stRadio span {
        color: rgba(255,255,255,0.72) !important;
    }
    [data-testid="stSidebar"] .stRadio label:has(input[type="radio"]:checked) {
        background: rgba(224,90,58,0.12) !important;
        border-color: rgba(224,90,58,0.3) !important;
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] .stRadio label:has(input[type="radio"]:checked) p,
    [data-testid="stSidebar"] .stRadio label:has(input[type="radio"]:checked) span {
        background: transparent !important;
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child {
        background: rgba(255,255,255,0.08) !important;
        border-color: rgba(255,255,255,0.2) !important;
    }
    [data-testid="stSidebar"] .stRadio [data-baseweb="radio"] [aria-checked="true"] > div:first-child,
    [data-testid="stSidebar"] .stRadio input[type="radio"]:checked + div > div:first-child {
        background: linear-gradient(145deg, var(--accent) 0%, #F97316 100%) !important;
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(224,90,58,0.18) !important;
    }

    /* ── Typography ── */
    h1, h2, h3 { font-family: 'Outfit', sans-serif !important; color: var(--ink) !important; }
    .page-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--ink);
        border-bottom: 2px solid var(--accent);
        padding-bottom: 12px;
        margin-bottom: 8px;
    }
    .page-subtitle { color: var(--ink-muted); font-size: 1rem; margin-bottom: 28px; font-weight: 400; }

    /* ── Module Cards ── */
    .module-card {
        background: var(--surface);
        border-radius: var(--radius-md);
        padding: 20px 24px;
        margin-bottom: 16px;
        border-left: 4px solid var(--accent);
        box-shadow: var(--shadow-card);
        transition: all 0.4s var(--transition-smooth);
    }
    .module-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-card-hover); }
    .module-card.complete { border-left-color: #22C55E; background: #F0FFF6; }

    /* ── Animations ── */
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(16px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    @keyframes pulseGlow {
        0%, 100% { opacity: 0.4; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.05); }
    }
    @keyframes progressFill {
        from { width: 0; }
    }
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(-12px); }
        to { opacity: 1; transform: translateX(0); }
    }

    /* ── Post-login Shell ── */
    .post-auth-shell {
        animation: fadeUp 0.6s var(--transition-smooth) both;
        margin-bottom: 22px;
    }
    .module-shell {
        background: var(--surface);
        border-radius: var(--radius-lg);
        border: 1px solid var(--border-default);
        box-shadow: var(--shadow-elevated);
        padding: 24px;
        margin-bottom: 18px;
        animation: fadeUp 0.5s var(--transition-smooth) both;
    }
    .module-page-hero {
        background: linear-gradient(135deg, #1C1C1E 0%, #2C2C2E 60%, #3A3A3C 100%);
        border-radius: var(--radius-md);
        padding: 28px 28px;
        border: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 16px;
        position: relative;
        overflow: hidden;
        animation: fadeUp 0.5s var(--transition-smooth) 0.1s both;
    }
    .module-page-hero::after {
        content: "";
        position: absolute;
        width: 300px;
        height: 300px;
        right: -100px;
        top: -150px;
        background: radial-gradient(circle, var(--accent-glow) 0%, transparent 72%);
        animation: pulseGlow 6s ease-in-out infinite;
    }
    .module-page-title {
        color: #F8FAFC !important;
        font-family: 'Playfair Display', serif;
        font-size: 1.58rem;

        margin: 3px 0 8px;
        position: relative;
        z-index: 1;
        text-shadow: 0 6px 24px rgba(2,8,23,0.6);
    }
    .module-page-hero h1,
    .module-page-hero h2,
    .module-page-hero h3 {
        color: #F8FAFC !important;
    }
    .module-page-sub {
        color: rgba(255,255,255,0.6);
        font-size: 0.88rem;
        margin: 0;
        position: relative;
        z-index: 1;
        max-width: 920px;
    }
    .module-meta-row {
        margin-top: 14px;
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        position: relative;
        z-index: 1;
    }
    .premium-hero {
        background: linear-gradient(135deg, #1C1C1E 0%, #2C2C2E 60%, #3A3A3C 100%);
        border-radius: var(--radius-lg);
        padding: 32px 34px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.06);
    }
    .premium-hero::before {
        content: "";
        position: absolute;
        width: 350px;
        height: 350px;
        right: -100px;
        top: -140px;
        background: radial-gradient(circle, rgba(224,90,58,0.3) 0%, transparent 70%);
        animation: pulseGlow 5s ease-in-out infinite;
    }
    .premium-hero::after {
        content: "";
        position: absolute;
        width: 280px;
        height: 280px;
        left: -80px;
        bottom: -120px;
        background: radial-gradient(circle, rgba(251,191,36,0.2) 0%, transparent 72%);
        animation: pulseGlow 7s ease-in-out infinite;
    }
    .premium-hero h1 { color: #FAFAFA !important; font-size: 1.9rem !important; margin: 0 0 8px 0 !important; font-family: 'Outfit', sans-serif !important; }
    .premium-hero p { color: rgba(255,255,255,0.6) !important; font-size: 0.94rem; margin: 0 !important; max-width: 760px; }
    .premium-kicker {
        display: inline-block;
        font-size: 0.62rem;
        color: var(--accent);
        letter-spacing: 0.22em;
        text-transform: uppercase;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .premium-metric-grid { margin-top: 16px; }
    .premium-stat {
        background: var(--surface);
        border: 1px solid var(--border-default);
        border-radius: var(--radius-md);
        padding: 16px 18px;
        box-shadow: var(--shadow-card);
        min-height: 102px;
        transition: all 0.4s var(--transition-smooth);
        animation: fadeUp 0.5s var(--transition-smooth) both;
    }
    .premium-stat:hover { transform: translateY(-3px); box-shadow: var(--shadow-card-hover); }
    .premium-stat-label { font-size: 0.64rem; color: var(--ink-muted); letter-spacing: 0.14em; text-transform: uppercase; font-weight: 700; }
    .premium-stat-value { color: var(--ink); font-size: 1.5rem; font-weight: 700; margin-top: 4px; font-family: 'Outfit', sans-serif; }
    .premium-stat-sub { color: var(--ink-faint); font-size: 0.74rem; margin-top: 5px; }

    .module-card-premium {
        background: var(--surface);
        border-radius: var(--radius-md);
        border: 1px solid var(--border-default);
        padding: 20px 20px 18px;
        margin-bottom: 14px;
        box-shadow: var(--shadow-card);
        transition: all 0.4s var(--transition-smooth);
        animation: fadeUp 0.5s var(--transition-smooth) both;
    }
    .module-card-premium:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-card-hover);
        border-color: var(--border-hover);
    }
    .module-topline { display:flex; justify-content:space-between; align-items:flex-start; gap:12px; }
    .module-name { color:var(--ink); font-weight:700; margin:0; font-size:1rem; font-family:'Outfit',sans-serif; }
    .module-sub { color:var(--ink-muted); margin:6px 0 14px 0; font-size:0.84rem; }
    .module-meter { height:5px; background:var(--surface-dim); border-radius:999px; overflow:hidden; }
    .module-meter > span {
        display:block;
        height:100%;
        background:linear-gradient(90deg, var(--accent) 0%, #FBBF24 100%);
        border-radius: 999px;
        box-shadow: 0 0 10px var(--accent-glow);
        animation: progressFill 1s var(--transition-smooth) both;
    }
    .pill {
        font-size: 0.62rem;
        border-radius: 99px;
        padding: 4px 10px;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        display: inline-block;
    }
    .pill.pending { background: #F5F5F5; color: #8E8E93; }
    .pill.live { background: var(--accent-soft); color: var(--accent); }
    .pill.done { background: #DCFCE7; color: #15803D; }
    .sidebar-mini {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: var(--radius-sm);
        padding: 10px 12px;
        margin-top: 12px;
    }
    .elite-chip {
        display: inline-block;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.12);
        color: rgba(255,255,255,0.55);
        border-radius: 999px;
        padding: 4px 10px;
        font-size: 0.6rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-right: 6px;
        font-weight: 500;
    }
    /* ── Progress Bars ── */
    .stProgress > div > div { background-color: var(--accent) !important; }

    /* ── Primary Buttons ── */
    .stButton > button[kind="primary"],
    .stButton > button[kind="primary"][data-testid],
    [data-testid="stBaseButton-primary"] {
        background: var(--ink) !important;
        color: white !important;
        border: 1px solid transparent !important;
        border-radius: var(--radius-sm) !important;
        padding: 8px 20px !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        transition: all 0.35s var(--transition-smooth) !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.12) !important;
    }
    .stButton > button[kind="primary"]:hover,
    [data-testid="stBaseButton-primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.18) !important;
    }
    .stButton > button:focus-visible {
        outline: 2px solid var(--accent) !important;
        outline-offset: 2px !important;
    }

    /* ── Secondary Buttons ── */
    .stButton > button[kind="secondary"],
    [data-testid="stBaseButton-secondary"] {
        background: var(--surface) !important;
        border: 1px solid var(--border-default) !important;
        color: var(--ink) !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        padding: 0.4rem 0.9rem !important;
        box-shadow: var(--shadow-card) !important;
        letter-spacing: 0.04em !important;
        text-transform: uppercase !important;
        border-radius: var(--radius-sm) !important;
        transition: all 0.35s var(--transition-smooth) !important;
    }
    .stButton > button[kind="secondary"]:hover,
    [data-testid="stBaseButton-secondary"]:hover {
        border-color: var(--accent) !important;
        color: var(--accent) !important;
        box-shadow: var(--shadow-card-hover) !important;
        transform: translateY(-2px) !important;
    }

    /* ── Badges ── */
    .badge {
        display: inline-block;
        background: var(--accent);
        color: white;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 20px;
        margin-left: 8px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .badge.done { background: #22C55E; }

    /* ── Welcome Banner ── */
    .welcome-banner {
        background: linear-gradient(135deg, #1C1C1E 0%, #3A3A3C 100%);
        border-radius: var(--radius-md);
        padding: 32px 36px;
        margin-bottom: 28px;
        border-left: 4px solid var(--accent);
    }
    .welcome-banner h1 { color: white !important; font-family: 'Outfit', sans-serif; font-size: 2rem; margin-bottom: 8px; }
    .welcome-banner p { color: rgba(255,255,255,0.6); font-size: 1.05rem; }

    /* ── Callout ── */
    .callout { background: var(--accent-soft); border-left: 3px solid var(--accent); border-radius: 0 var(--radius-sm) var(--radius-sm) 0; padding: 14px 18px; margin: 16px 0; color: #7C2D12; }

    /* ── Dividers ── */
    hr { border: none; border-top: 1px solid var(--border-default); margin: 24px 0; }

    /* ── Resource Library ── */
    .resource-card {
        background: var(--surface);
        border-radius: var(--radius-md);
        padding: 14px 16px;
        margin-bottom: 7px;
        box-shadow: var(--shadow-card);
        border: 1px solid var(--border-default);
        transition: all 0.35s var(--transition-smooth);
    }
    .resource-card:hover {
        border-color: var(--border-hover);
        box-shadow: var(--shadow-card-hover);
        transform: translateY(-2px);
    }
    .resource-id {
        display: inline-block;
        background: var(--ink);
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
    /* ── Mobile dark-mode compatibility ── */
    @media (max-width: 768px) and (prefers-color-scheme: dark) {
      div[data-testid="stAppViewContainer"],
      section.main,
      .stApp {
        background: #1C1C1E !important;
        color: #F0F0F2 !important;
      }
      div[data-testid="stMarkdownContainer"],
      div[data-testid="stMarkdownContainer"] p,
      div[data-testid="stMarkdownContainer"] li,
      div[data-testid="stMarkdownContainer"] span,
      div[data-testid="stMarkdownContainer"] div {
        color: #F0F0F2 !important;
      }
      .page-title, .page-subtitle { color: #F0F0F2 !important; }
      .resource-card, .module-card,
      div[style*="background:white"],
      div[style*="background: white"] {
        background: #2C2C2E !important;
        border-color: rgba(255,255,255,0.08) !important;
      }
      div[data-testid="stTextInput"] input {
        background: #2C2C2E !important;
        color: #F0F0F2 !important;
        border-color: rgba(255,255,255,0.12) !important;
      }
      table, td, th {
        color: #E0E0E4 !important;
        border-color: rgba(255,255,255,0.08) !important;
      }
    }

    /* ── Sidebar action buttons ── */
    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        border-radius: var(--radius-sm) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        background: rgba(255,255,255,0.06) !important;
        color: #E0E0E4 !important;
        text-align: center !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.03em !important;
        transition: all 0.35s var(--transition-smooth) !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        transform: translateY(-1px) !important;
        background: rgba(255,255,255,0.10) !important;
    }
    [data-testid="stSidebar"] .stButton > button[kind="primary"],
    [data-testid="stSidebar"] [data-testid="stBaseButton-primary"] {
        background: rgba(224,90,58,0.2) !important;
        border-color: rgba(224,90,58,0.3) !important;
        color: #F0F0F2 !important;
    }

    /* ── Content sections ── */
    .content-section {
        background: var(--surface);
        border-radius: var(--radius-md);
        padding: 26px 28px;
        margin: 18px 0;
        box-shadow: var(--shadow-card);
        border: 1px solid var(--border-default);
        border-top: 3px solid var(--accent);
        animation: fadeUp 0.5s var(--transition-smooth) both;
        transition: all 0.35s var(--transition-smooth);
    }
    .content-section:hover { box-shadow: var(--shadow-card-hover); }
    .content-section h2 {
        font-family: 'Outfit', sans-serif;
        color: var(--ink) !important;
        font-size: 1.6rem;
        font-weight: 700;
        margin: 0 0 14px 0;
        border-bottom: 1px solid var(--border-default);
        padding-bottom: 10px;
    }
    .content-section h3 {
        color: var(--accent) !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-size: 0.78rem;
        font-weight: 700;
        margin: 20px 0 8px 0;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* ── Info boxes ── */
    .info-box {
        background: var(--accent-soft);
        border-left: 3px solid var(--accent);
        border-radius: var(--radius-sm);
        padding: 14px 16px;
        margin: 16px 0;
        color: var(--ink) !important;
        transition: all 0.3s var(--transition-smooth);
    }
    .info-box:hover { transform: translateX(3px); }
    .info-box.green { background: #F0FFF6; border-left-color: #22C55E; }
    .info-box.yellow { background: #FFFBEB; border-left-color: #F59E0B; }

    /* ── Tables ── */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.9rem;
        margin: 14px 0;
        border-radius: var(--radius-sm);
        overflow: hidden;
        box-shadow: var(--shadow-card);
    }
    .styled-table th {
        background: var(--ink);
        color: #FFFFFF;
        padding: 12px 14px;
        text-align: left;
        font-weight: 600;
        font-size: 0.82rem;
    }
    .styled-table td {
        padding: 11px 14px;
        border-bottom: 1px solid var(--border-default);
        color: var(--ink);
        background: var(--surface);
    }
    .styled-table tr:nth-child(even) td { background: var(--surface-dim); }
    .styled-table tr:last-child td { border-bottom: none; }
    .styled-table tr:hover td { background: var(--accent-soft); transition: background 0.25s ease; }

    /* ── Premium Login ── */
    :root { --login-card-height: 560px; }
    @keyframes loginAurora {
        0% { transform: translate3d(0, 0, 0) scale(1); opacity: 0.3; }
        50% { transform: translate3d(-14px, 10px, 0) scale(1.06); opacity: 0.55; }
        100% { transform: translate3d(0, 0, 0) scale(1); opacity: 0.3; }
    }
    @keyframes loginShimmer {
        0% { transform: translateX(-140%); }
        100% { transform: translateX(180%); }
    }
    .lp-info-card {
        background: linear-gradient(160deg, #1C1C1E 0%, #2C2C2E 50%, #3A3A3C 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: var(--radius-lg);
        padding: 44px 40px;
        min-height: var(--login-card-height);
        position: relative;
        overflow: hidden;
        transition: all 0.5s var(--transition-smooth);
    }
    .lp-info-card:hover {
        transform: translateY(-3px);
        border-color: rgba(224,90,58,0.3);
    }
    .lp-info-card::before {
        content: "";
        position: absolute;
        top: -90px;
        right: -80px;
        width: 320px;
        height: 320px;
        background: radial-gradient(circle, rgba(224,90,58,0.25) 0%, transparent 72%);
        pointer-events: none;
        animation: loginAurora 9s ease-in-out infinite;
    }
    .lp-info-card::after {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(115deg, transparent 20%, rgba(255,255,255,0.04) 45%, transparent 70%);
        opacity: 0.5;
        pointer-events: none;
        animation: loginShimmer 8s linear infinite;
    }
    .lp-kicker, .lp-headline, .lp-body, .lp-features, .lp-divider, .lp-stat-row { position: relative; z-index: 1; }
    .lp-kicker {
        font-size: 0.66rem;
        text-transform: uppercase;
        letter-spacing: 0.22em;
        color: var(--accent);
        font-weight: 700;
        margin-bottom: 18px;
    }
    .lp-headline {
        font-family: 'Outfit', sans-serif !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        line-height: 1.2 !important;
        margin: 0 0 18px 0 !important;
    }
    .lp-body {
        color: rgba(255,255,255,0.55);
        font-size: 0.93rem;
        line-height: 1.8;
        margin: 0 0 24px 0;
    }
    .lp-stat-row {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 12px;
        margin: 0 auto 20px auto;
        max-width: 420px;
    }
    .lp-stat {
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: var(--radius-sm);
        padding: 10px 12px;
        background: rgba(255,255,255,0.04);
        transition: all 0.35s var(--transition-smooth);
    }
    .lp-stat:hover {
        transform: translateY(-2px);
        background: rgba(255,255,255,0.07);
        border-color: rgba(224,90,58,0.3);
    }
    .lp-stat-label { color: rgba(255,255,255,0.4); font-size: 0.62rem; letter-spacing: 0.12em; text-transform: uppercase; font-weight: 700; }
    .lp-stat-value { color: #F0F0F2; font-size: 1rem; font-weight: 700; margin-top: 3px; font-family: 'Outfit', sans-serif; }
    .lp-features {
        list-style: none;
        padding: 0;
        margin: 0;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .lp-features li {
        display: flex;
        align-items: center;
        gap: 12px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: var(--radius-sm);
        padding: 12px 15px;
        color: rgba(255,255,255,0.7);
        font-size: 0.84rem;
        font-weight: 500;
        transition: all 0.35s var(--transition-smooth);
    }
    .lp-features li:hover {
        transform: translateX(4px);
        border-color: rgba(224,90,58,0.3);
        background: rgba(224,90,58,0.06);
    }
    .lp-divider {
        width: 42px;
        height: 3px;
        background: linear-gradient(90deg, var(--accent), #FBBF24);
        border-radius: 2px;
        margin: 0 0 20px 0;
    }
    /* Form submit button styling */
    div[data-testid="stFormSubmitButton"] button {
        background: var(--ink) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        padding: 12px 20px !important;
        font-weight: 700 !important;
        letter-spacing: 0.04em !important;
        text-transform: uppercase !important;
        font-size: 0.82rem !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.15) !important;
        transition: all 0.35s var(--transition-smooth) !important;
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.22) !important;
    }

    /* ── Checkbox enhancements ── */
    .stCheckbox label { transition: all 0.25s ease !important; }
    .stCheckbox label:hover { transform: translateX(2px) !important; }

    /* ── Tab styling ── */
    .stTabs [data-baseweb="tab-list"] { gap: 4px !important; }
    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-sm) !important;
        transition: all 0.3s var(--transition-smooth) !important;
    }

</style>
""")

# ─────────────────────────────────────────────
#  GOOGLE SHEETS INTEGRATION
# ─────────────────────────────────────────────
@st.cache_resource
def get_gsheet_client():
    try:
        creds_dict = dict(st.secrets["gcp_service_account"])
        scopes = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        return gspread.service_account_from_dict(creds_dict, scopes=scopes)
    except Exception:
        return None

def get_sheet(client):
    """Progress tracking sheet (Sheet1)."""
    try:
        return client.open("AAP New Hire Orientation Progress").sheet1
    except Exception:
        return None

def get_employee_sheet(client):
    """Employee roster sheet — tab named 'Employee Roster'."""
    try:
        return client.open("AAP New Hire Orientation Progress").worksheet("Employee Roster")
    except Exception:
        return None

# ─────────────────────────────────────────────
#  AUTHENTICATION
#
#  Three-part check:
#    1. Access Code  — shared company-wide password stored in Streamlit secrets.
#                      Keeps random internet strangers out.
#    2. Employee ID  — must exist in the Employee Roster sheet.
#                      Ensures only real, active employees can log in.
#    3. Full Name    — must match the name on file for that Employee ID.
#                      Prevents Employee A from logging in as Employee B.
#
#  The Employee Roster sheet must have these columns:
#    Employee ID | Full Name | Track
#  where Track is "General" or "Warehouse" (case-insensitive).
# ─────────────────────────────────────────────
def verify_employee(access_code, employee_id, full_name):
    """
    Returns (True, track_string, "") on success, where track_string is
    "general" or "warehouse" as set in the Employee Roster sheet.
    Returns (False, "", reason_string) on failure.
    Fails closed — any sheet/network error denies access.
    """
    # ── Step 1: Check access code against Streamlit secret ──────────────────
    try:
        correct_code = st.secrets["orientation_access_code"]
    except Exception as e:
        return False, "", f"Access code configuration error: {e}"

    if access_code.strip() != correct_code.strip():
        return False, "", f"Incorrect access code. (Entered {len(access_code.strip())} chars, expected {len(correct_code.strip())} chars)"

    # ── Step 2 & 3: Validate Employee ID + Name against roster ──────────────
    client = get_gsheet_client()
    if not client:
        return False, "", "Unable to connect to Google Sheets. Check gcp_service_account secret and service account permissions."

    emp_sheet = get_employee_sheet(client)
    if not emp_sheet:
        return False, "", "Could not open 'Employee Roster' tab. Check that the tab exists in 'AAP New Hire Orientation Progress'."

    try:
        records = emp_sheet.get_all_records()
        if not records:
            return False, "", "Employee Roster sheet appears to be empty. Please check the sheet has data."

        col_names = list(records[0].keys()) if records else []

        for row in records:
            row_id   = str(row.get("Employee ID", "")).strip().lower()
            row_name = str(row.get("Full Name",   "")).strip().lower()
            if row_id == employee_id.strip().lower():
                if row_name == full_name.strip().lower():
                    # Read the Track column; fall back to "general" if missing/blank
                    raw_track = str(row.get("Track", "")).strip().lower()
                    track = "warehouse" if raw_track == "warehouse" else "general"
                    return True, track, ""
                else:
                    return False, "", f"ID matched but name did not. Sheet has: '{row.get('Full Name', '')}' — you entered: '{full_name.strip()}'"
        return False, "", f"Employee ID '{employee_id.strip()}' not found. Sheet has {len(records)} rows. Columns found: {col_names}"
    except Exception as e:
        return False, "", f"Verification error: {e}"


def save_progress(employee_id, employee_name, module_key, pct, checklist_items, quiz_score):
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
            if row.get("Employee ID") == employee_id and row.get("Module Key") == module_key:
                row_idx = i
                break
        # Store both ID and name so the sheet is human-readable for HR
        data = [employee_id, employee_name, module_key, pct, checklist_json, quiz_score, now]
        if row_idx:
            sheet.update(f"A{row_idx}:G{row_idx}", [data])
        else:
            sheet.append_row(data)
    except Exception:
        pass

def load_progress(employee_id):
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
            if str(row.get("Employee ID", "")).strip() == employee_id.strip():
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
        "key": "timeoff",
        "number": 4,
        "title": "Time Off & Leave",
        "subtitle": "PTO, holidays, sick leave & attendance rules",
        "icon": "⏰",
    },
    {
        "key": "benefits",
        "number": 5,
        "title": "Benefits",
        "subtitle": "Health, 401k, life insurance & employee perks",
        "icon": "💼",
    },
    {
        "key": "firststeps",
        "number": 6,
        "title": "Your First Steps",
        "subtitle": "Systems, contacts & what to expect",
        "icon": "🚀",
    },
]

# ─────────────────────────────────────────────
#  SESSION STATE DEFAULTS
# ─────────────────────────────────────────────
# ─────────────────────────────────────────────
#  WAREHOUSE MODULES
# ─────────────────────────────────────────────
WAREHOUSE_MODULES = [
    {
        "key": "wh_welcome",
        "number": 1,
        "title": "Welcome to AAP — Warehouse Edition",
        "subtitle": "Our history, mission, values & your role in the warehouse",
        "icon": "🏢",
    },
    {
        "key": "wh_conduct",
        "number": 2,
        "title": "Code of Conduct & Ethics",
        "subtitle": "Expected behaviors, confidentiality & EEO in a warehouse setting",
        "icon": "⚖️",
    },
    {
        "key": "wh_safety",
        "number": 3,
        "title": "Warehouse Policies & Safety",
        "subtitle": "Attendance, PPE, safety rules & warehouse procedures",
        "icon": "🦺",
    },
    {
        "key": "wh_timeoff",
        "number": 4,
        "title": "Time Off & Leave",
        "subtitle": "PTO, holidays, sick leave & attendance rules",
        "icon": "⏰",
    },
    {
        "key": "wh_benefits",
        "number": 5,
        "title": "Benefits",
        "subtitle": "Health, 401k, life insurance & employee perks",
        "icon": "💼",
    },
    {
        "key": "wh_firststeps",
        "number": 6,
        "title": "Your First Steps — Warehouse",
        "subtitle": "Systems, contacts, equipment & what to expect on Day 1",
        "icon": "🚀",
    },
]

defaults = {
    "authenticated": False,
    "username": "",
    "employee_id": "",
    "role_track": "",          # "general" or "warehouse"
    "selected_module": None,
    "sheet_loaded": False,
    "progress": {m["key"]: 0 for m in MODULES},
    "quiz_results": {},
    "checklist_items": {m["key"]: {} for m in MODULES},
    "auth_error": "",
    "sound_enabled": True,
    "pending_sound": "",
    "last_milestone_bucket": 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────
def pct_bar(pct):
    return dedent(f"""
    <div class="progress-container">
        <div class="progress-fill" style="width:{pct}%"></div>
    </div>
    <small style="color:rgba(255,255,255,0.4)">{pct}% complete</small>
    """).strip()

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

def trigger_sound(event_name: str):
    st.session_state.pending_sound = f"{event_name}:{datetime.now().timestamp()}"

def render_sound_engine():
    event_payload = st.session_state.get("pending_sound", "")
    enabled = "true" if st.session_state.get("sound_enabled", True) else "false"
    components.html(f"""
    <script>
    (() => {{
        const enabled = {enabled};
        const payload = {json.dumps(event_payload)};
        if (!enabled || !payload) return;

        const event = payload.split(':')[0];
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;
        const ctx = new AudioCtx();

        const hit = (freq, type='sine', dur=0.12, gain=0.04, delay=0) => {{
            const now = ctx.currentTime + delay;
            const o = ctx.createOscillator();
            const g = ctx.createGain();
            o.type = type;
            o.frequency.setValueAtTime(freq, now);
            g.gain.setValueAtTime(0.0001, now);
            g.gain.exponentialRampToValueAtTime(gain, now + 0.015);
            g.gain.exponentialRampToValueAtTime(0.0001, now + dur);
            o.connect(g); g.connect(ctx.destination);
            o.start(now); o.stop(now + dur + 0.01);
        }};

        if (event === 'success') {{
            hit(523.25, 'triangle', 0.14, 0.045, 0);
            hit(659.25, 'triangle', 0.16, 0.04, 0.08);
            hit(783.99, 'triangle', 0.18, 0.038, 0.16);
        }} else if (event === 'correct') {{
            hit(587.33, 'sine', 0.1, 0.04, 0);
            hit(739.99, 'sine', 0.14, 0.035, 0.09);
        }} else if (event === 'milestone') {{
            hit(440.0, 'triangle', 0.09, 0.03, 0);
            hit(554.37, 'triangle', 0.12, 0.03, 0.08);
        }} else if (event === 'lesson_complete') {{
            hit(493.88, 'triangle', 0.12, 0.038, 0);
            hit(659.25, 'triangle', 0.15, 0.035, 0.08);
            hit(880.0, 'triangle', 0.18, 0.03, 0.16);
        }}
    }})();
    </script>
    """, height=0)

    st.session_state.pending_sound = ""

def finalize_quiz_submission(module_key, score, max_score):
    st.session_state.quiz_results[module_key] = score
    if score >= max_score:
        trigger_sound("correct")
    update_progress(module_key)

def update_progress(module_key):
    previous_pct = st.session_state.progress.get(module_key, 0)
    pct = calculate_module_pct(
        module_key,
        st.session_state.checklist_items,
        st.session_state.quiz_results,
    )
    st.session_state.progress[module_key] = pct

    if previous_pct < 100 and pct == 100 and not st.session_state.get("pending_sound"):
        trigger_sound("lesson_complete")

    active_modules = WAREHOUSE_MODULES if st.session_state.get("role_track") == "warehouse" else MODULES
    overall_pct = int(sum(st.session_state.progress.values()) / max(len(active_modules), 1))
    milestone_bucket = overall_pct // 25
    last_bucket = st.session_state.get("last_milestone_bucket", 0)
    if milestone_bucket > last_bucket and milestone_bucket in (1, 2, 3, 4):
        st.session_state.last_milestone_bucket = milestone_bucket
        if not st.session_state.get("pending_sound"):
            trigger_sound("milestone")

    if st.session_state.authenticated and st.session_state.employee_id:
        items = st.session_state.checklist_items.get(module_key, {})
        score = st.session_state.quiz_results.get(module_key)
        save_progress(
            st.session_state.employee_id,
            st.session_state.username,
            module_key, pct, items, score,
        )

def render_module_shell_start(module_key):
    is_warehouse = st.session_state.get("role_track") == "warehouse"
    active_modules = WAREHOUSE_MODULES if is_warehouse else MODULES
    module = next((m for m in active_modules if m["key"] == module_key), None)
    if not module:
        return

    pct = st.session_state.progress.get(module_key, 0)
    status = "Complete" if pct == 100 else "In Progress" if pct > 0 else "Queued"
    st.markdown('<div class="module-shell">', unsafe_allow_html=True)
    render_html(f"""
    <div class="module-page-hero">
        <span class="premium-kicker">Training Module</span>
        <h1 class="module-page-title">{module['icon']} Module {module['number']}: {module['title']}</h1>
        <p class="module-page-sub">{module['subtitle']}</p>
        <div class="module-meta-row">
            <span class="elite-chip">Completion · {pct}%</span>
            <span class="elite-chip">Status · {status}</span>
            <span class="elite-chip">Secure Learning Environment</span>
        </div>
    </div>
    """)

def render_module_shell_end():
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  LOGIN SCREEN
# ─────────────────────────────────────────────
def show_login():
    # Inject login-specific CSS overrides (scoped to this page only)
    render_html("""
    <style>
        /* Page background for login */
        .stApp { background: #1C1C1E !important; }

        .login-shell { max-width: 1240px; margin: 0 auto; perspective: 1200px; }

        /* Style the form container as the white sign-in card */
        [data-testid="stForm"] {
            background: linear-gradient(180deg, #FFFFFF 0%, #FAFAF8 100%);
            border-radius: var(--radius-lg);
            padding: 36px 34px 30px !important;
            min-height: var(--login-card-height);
            box-shadow: 0 20px 60px rgba(0,0,0,0.25);
            border: 1px solid rgba(0,0,0,0.06);
            transition: all 0.45s var(--transition-smooth);
            will-change: transform;
        }
        [data-testid="stForm"]:hover {
            transform: translateY(-2px);
            border-color: rgba(224,90,58,0.2);
            box-shadow: 0 30px 80px rgba(0,0,0,0.3);
        }
        [data-testid="stForm"] > div {
            min-height: calc(var(--login-card-height) - 66px);
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        .login-form-intro {
            margin-bottom: 6px;
            padding-bottom: 8px;
            border-bottom: 1px solid rgba(0,0,0,0.06);
        }
        .login-form-footnote {
            margin-top: auto;
            padding-top: 8px;
            font-size: 0.75rem;
            color: #A0A0AB;
            text-align: center;
            letter-spacing: 0.02em;
        }
        .login-celebrate {
            margin-top: 10px;
            background: linear-gradient(120deg, #ECFDF5 0%, #FFF7ED 100%);
            border: 1px solid rgba(224,90,58,0.15);
            color: #7C2D12;
            border-radius: var(--radius-sm);
            padding: 9px 11px;
            font-size: 0.78rem;
            font-weight: 600;
            text-align: center;
            animation: fadeIn 0.35s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(4px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Input label styling */
        [data-testid="stForm"] label p {
            font-size: 0.72rem !important;
            font-weight: 700 !important;
            color: var(--ink-muted) !important;
            text-transform: uppercase !important;
            letter-spacing: 0.12em !important;
            margin-top: 6px !important;
        }
        /* Input field styling */
        [data-testid="stForm"] input {
            border: 1.5px solid var(--border-default) !important;
            border-radius: var(--radius-sm) !important;
            font-size: 0.92rem !important;
            background: var(--surface-dim) !important;
            color: var(--ink) !important;
            min-height: 44px !important;
            transition: all 0.3s var(--transition-smooth) !important;
        }
        [data-testid="stForm"] input:focus {
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 3px rgba(224,90,58,0.1) !important;
            background: #FFFFFF !important;
        }
    </style>
    """)

    render_html("<div style='padding-top:36px'></div>")

    _login_logo_src = _logo_img_src()

    outer_l, outer_m, outer_r = st.columns([0.5, 2, 0.5])
    with outer_m:
        # Logo
        render_html(f"""
        <div class="login-shell"><div style="text-align:center; margin-bottom:32px;">
            <img src="{_login_logo_src}" alt="AAP / API Logo"
                 style="height:88px; max-width:300px; object-fit:contain;
                        filter: drop-shadow(0 6px 20px rgba(6,14,30,0.5)) brightness(1.05);">
        </div>
        """)

        # Two-panel layout: dark info card left, white form card right
        panel_l, panel_r = st.columns([1.4, 1], gap="large")

        with panel_l:
            render_html("""
            <div class="lp-info-card">
                <div class="lp-kicker">Welcome, we're glad you're here</div>
                <h2 class="lp-headline">Let’s make your first week feel easy, clear, and exciting.</h2>
                <div class="lp-divider"></div>
                <p class="lp-body">
                    Your onboarding space is designed to guide you step-by-step, celebrate your progress,
                    and help you feel confident from day one. Everything you need is right here.
                </p>
                <div class="lp-stat-row">
                    <div class="lp-stat"><div class="lp-stat-label">Modules</div><div class="lp-stat-value">5 Guided Steps</div></div>
                    <div class="lp-stat"><div class="lp-stat-label">Progress</div><div class="lp-stat-value">Live + Saved</div></div>
                </div>
                <ul class="lp-features">
                    <li><span>🔒</span> Secure employee credential verification</li>
                    <li><span>🧭</span> Role-calibrated module sequencing</li>
                    <li><span>📈</span> Progress visibility for HR and leadership</li>
                </ul>
            </div>
            """)

        with panel_r:
            with st.form("login_form", clear_on_submit=False):
                render_html("""
                <div class="login-form-intro">
                    <p style="font-size:1.2rem; font-weight:700; color:#1A1A1E; margin:0 0 4px 0; font-family:'Outfit',sans-serif;">
                        Employee Sign In
                    </p>
                    <p style="color:#6B6B76; font-size:0.84rem; margin:0;">
                        Access your onboarding inbox and continue where you left off.
                    </p>
                </div>
                """)

                access_code = st.text_input(
                    "Access Code",
                    placeholder="Enter the code HR gave you",
                    type="password",
                )
                employee_id = st.text_input(
                    "Employee ID",
                    placeholder="e.g. 10042",
                )
                full_name = st.text_input(
                    "Full Name",
                    placeholder="As it appears in your HR paperwork",
                )
                render_html("<div style='margin-top:10px;'></div>")
                submitted = st.form_submit_button("Sign In  →", use_container_width=True)
                render_html("<div class='login-form-footnote'>Enterprise access is monitored and encrypted.</div>")
                if st.session_state.get("auth_error") == "":
                    render_html("<div class='login-celebrate'>Ready when you are — your onboarding workspace is one sign-in away.</div>")

                if submitted:
                    if not access_code or not employee_id or not full_name:
                        st.error("Please fill in all three fields to continue.")
                    else:
                        with st.spinner("Verifying your credentials…"):
                            ok, track, reason = verify_employee(access_code, employee_id, full_name)
                        if ok:
                            if track == "warehouse":
                                prog_keys = {m["key"]: 0 for m in WAREHOUSE_MODULES}
                                chk_keys  = {m["key"]: {} for m in WAREHOUSE_MODULES}
                            else:
                                prog_keys = {m["key"]: 0 for m in MODULES}
                                chk_keys  = {m["key"]: {} for m in MODULES}
                            st.session_state.authenticated   = True
                            st.session_state.username        = full_name.strip()
                            st.session_state.employee_id     = employee_id.strip()
                            st.session_state.role_track      = track
                            st.session_state.progress        = prog_keys
                            st.session_state.checklist_items = chk_keys
                            st.session_state.quiz_results    = {}
                            st.session_state.sheet_loaded    = False
                            st.session_state.auth_error      = ""
                            st.toast("Welcome aboard! Launching your training workspace.", icon="✨")
                            trigger_sound("success")
                            st.balloons()
                            st.rerun()
                        else:
                            st.session_state.auth_error = reason
                            st.error(f"❌ {reason}")

        st.toggle("🔈 Interface sounds", key="sound_enabled", help="Mute/unmute subtle interaction sounds.")

        render_html("</div>")

        # Footer
        render_html("""
        <div style="text-align:center; margin-top:28px; padding-top:18px;
                    border-top:1px solid rgba(255,255,255,0.06);">
            <p style="color:rgba(255,255,255,0.35); font-size:0.78rem; margin:0; line-height:2;">
                Need help? Contact HR &nbsp;·&nbsp;
                <strong style="color:rgba(255,255,255,0.5);">Nicole Thornton</strong>
                &nbsp;·&nbsp; nicole.thornton@apirx.com &nbsp;·&nbsp; 256-574-7528
            </p>
        </div>
        """)


# ─────────────────────────────────────────────
#  SIDEBAR  (only rendered when authenticated)
# ─────────────────────────────────────────────
if st.session_state.authenticated:
    # Pick the right module list for the active track
    active_modules = WAREHOUSE_MODULES if st.session_state.get("role_track") == "warehouse" else MODULES

    with st.sidebar:
        # Load progress from sheet once per login session
        if not st.session_state.sheet_loaded:
            saved = load_progress(st.session_state.employee_id)
            if saved:
                for mk, data in saved.items():
                    st.session_state.progress[mk] = data.get("pct", 0)
                    st.session_state.checklist_items[mk] = data.get("checklist", {})
                    if data.get("quiz_score") is not None:
                        st.session_state.quiz_results[mk] = data["quiz_score"]
            st.session_state.sheet_loaded = True

        # ── White card: logo + label + username ──
        logo_src = _logo_img_src()
        render_html(f"""
        <div class="sidebar-header">
            <img src="{logo_src}"
                 style="max-height:56px; width:100%; object-fit:contain; margin-bottom:10px;" />
            <div style="font-size:0.6rem; font-weight:700; letter-spacing:0.18em;
                        color:rgba(255,255,255,0.35); text-transform:uppercase; margin-bottom:6px;">
                    Learning Interface
            </div>
            <div class="sidebar-username" style="font-size:0.93rem;">👤 {st.session_state.username}</div>
        </div>
        """)

        # ── Overall progress ──
        total_pct = int(sum(st.session_state.progress.values()) / max(len(active_modules), 1))
        render_html(f"""
        <div style="font-size:0.66rem; font-weight:700; letter-spacing:0.12em;
                    color:rgba(255,255,255,0.35); text-transform:uppercase; margin: 6px 0 4px 0;">
            Progress &middot; {total_pct}%
        </div>
        """)
        render_html(pct_bar(total_pct))

        render_html("<div class='sidebar-section-label'>Navigation</div>")

        # ── Radio navigation ──
        nav_options = ["🏠  Home"] + [
            f"{m['icon']}  {m['number']}. {m['title']}" for m in active_modules
        ]
        module_keys = [None] + [m["key"] for m in active_modules]

        try:
            current_idx = module_keys.index(st.session_state.selected_module)
        except ValueError:
            current_idx = 0

        selected_nav = st.radio(
            "Navigation",
            nav_options,
            index=current_idx,
            label_visibility="collapsed",
        )

        new_key = module_keys[nav_options.index(selected_nav)]
        if new_key != st.session_state.selected_module:
            st.session_state.selected_module = new_key
            st.rerun()

        st.markdown("---")

        st.toggle("🔈 Interface sounds", key="sound_enabled", help="Play subtle UI sounds for progress and confirmations.")

        # ── Sign Out ──
        if st.button("🚪 Sign Out", key="sign_out", type="primary", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        st.markdown("---")
        render_html("""
        <small style='color:rgba(255,255,255,0.4)'>
        <b>HR Contact</b><br>
        Nicole Thornton<br>
        HR Administrator<br>
        📞 256-574-7528<br>
        ✉ Nicole.thornton@apirx.com
        </small>
        <div class="sidebar-mini">
            <div style="font-size:0.6rem; letter-spacing:0.16em; text-transform:uppercase; color:rgba(255,255,255,0.3); font-weight:700; margin-bottom:4px;">Built with care</div>
            <div style="color:rgba(255,255,255,0.5); font-size:0.78rem; line-height:1.45;">Modern onboarding experience designed for clarity and confidence.</div>
        </div>
        """)

# ─────────────────────────────────────────────
#  MAIN CONTENT — HOME
# ─────────────────────────────────────────────
def show_home():
    is_warehouse = st.session_state.get("role_track") == "warehouse"
    active_modules = WAREHOUSE_MODULES if is_warehouse else MODULES
    track_label = "Warehouse" if is_warehouse else "General"
    name_display = st.session_state.username.strip() if st.session_state.username else "Team Member"

    module_progress = [st.session_state.progress.get(m["key"], 0) for m in active_modules]
    completed = sum(1 for p in module_progress if p == 100)
    total_pct = int(sum(module_progress) / len(active_modules)) if active_modules else 0
    quizzes_done = sum(1 for m in active_modules if st.session_state.quiz_results.get(m["key"]) is not None)

    st.markdown('<div class="post-auth-shell">', unsafe_allow_html=True)

    render_html(f"""
    <div class="premium-hero">
        <span class="premium-kicker">Your Onboarding Hub</span>
        <h1>{track_label} Learning Dashboard · {name_display}</h1>
        <p>
            Everything you need to get started — all in one place.
            Track your progress, complete modules, and feel confident from day one.
        </p>
        <div style="margin-top:14px;">
            <span class="elite-chip">Progress Synced</span>
            <span class="elite-chip">{track_label} Track</span>
            <span class="elite-chip">Secure</span>
        </div>
    </div>
    """)

    c1, c2, c3 = st.columns(3)
    with c1:
        render_html(f"""
        <div class="premium-stat">
            <div class="premium-stat-label">Modules Done</div>
            <div class="premium-stat-value">{completed}/{len(active_modules)}</div>
            <div class="premium-stat-sub">Completed training modules</div>
        </div>
        """)
    with c2:
        render_html(f"""
        <div class="premium-stat">
            <div class="premium-stat-label">Overall Progress</div>
            <div class="premium-stat-value">{total_pct}%</div>
            <div class="premium-stat-sub">Across all lessons and quizzes</div>
        </div>
        """)
    with c3:
        render_html(f"""
        <div class="premium-stat">
            <div class="premium-stat-label">Quizzes Passed</div>
            <div class="premium-stat-value">{quizzes_done}/{len(active_modules)}</div>
            <div class="premium-stat-sub">Knowledge checks completed</div>
        </div>
        """)

    render_html("""
    <div style="margin:18px 0 10px 0; display:flex; justify-content:space-between; align-items:center; gap:10px;">
        <div style="font-size:0.7rem; letter-spacing:0.14em; text-transform:uppercase; color:#A0A0AB; font-weight:700;">Training Modules</div>
        <div style="font-size:0.75rem; color:#6B6B76;">Pick up where you left off.</div>
    </div>
    """)

    for m in active_modules:
        pct = st.session_state.progress.get(m["key"], 0)
        if pct == 100:
            pill_class, pill_text = "done", "Complete"
        elif pct > 0:
            pill_class, pill_text = "live", "In Progress"
        else:
            pill_class, pill_text = "pending", "Queued"

        render_html(f"""
        <div class="module-card-premium">
            <div class="module-topline">
                <p class="module-name">{m['icon']} · Module {m['number']} · {m['title']}</p>
                <span class="pill {pill_class}">{pill_text}</span>
            </div>
            <p class="module-sub">{m['subtitle']}</p>
            <div class="module-meter"><span style="width:{pct}%"></span></div>
            <div style="margin-top:8px; color:#A0A0AB; font-size:0.76rem; display:flex; justify-content:space-between;">
                <span>Progress</span><strong style="color:#1A1A1E;">{pct}%</strong>
            </div>
        </div>
        """)

        if st.button(f"Launch Module {m['number']}", key=f"open_{m['key']}", type="secondary"):
            st.session_state.selected_module = m["key"]
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  MODULE 1 — WELCOME TO AAP
# ─────────────────────────────────────────────
def show_module_welcome():
    render_html("""
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
    """)

    values = [
        ("🎯", "Customer Focus", "Our primary focus is to meet customer requirements and strive to exceed customer expectations. Excellent service to the outside customer is dependent upon healthy internal customer service practices and teamwork. Customer Service is not just a department — it is an attitude."),
        ("🤝", "Integrity", "We act with honesty and integrity without compromising the truth. We maintain consistency in what we say and what we do to build trust."),
        ("💙", "Respect", "We treat others with the same dignity as we wish to be treated. We recognize the power of teamwork and appreciate the unique contributions that each member of a team can make. We encourage open and honest communication."),
        ("⭐", "Excellence", "We strive for the highest quality in everything that we do. We seek and pursue opportunities for continuous improvement and innovation."),
        ("🙋", "Ownership", "We seek responsibility and hold ourselves accountable for our actions. When things go wrong, we take responsibility."),
    ]

    for icon, value, desc in values:
        render_html(f"""
        <div class="content-section" style="padding:18px 24px;margin-bottom:10px;">
            <h3 style="margin-top:0">{icon} {value}</h3>
            <p style="margin:0">{desc}</p>
        </div>
        """)

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
                finalize_quiz_submission(mk, score, 4)
                st.rerun()

# ─────────────────────────────────────────────
#  MODULE 2 — CODE OF CONDUCT
# ─────────────────────────────────────────────
def show_module_conduct():
    render_html("""
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
    """)

    render_html("""
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
    """)

    render_html("""
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
    """)

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
                finalize_quiz_submission(mk, score, 4)
                st.rerun()

# ─────────────────────────────────────────────
#  MODULE 3 — WORKPLACE POLICIES
# ─────────────────────────────────────────────
def show_module_policies():
    render_html("""
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
    """)

    render_html("""
    <table class="styled-table">
        <tr><th>Reason</th><th>Points</th></tr>
        <tr><td>Tardy up to 5 minutes (grace period)</td><td>0</td></tr>
        <tr><td>Tardy or early leave (less than 4 hours)</td><td>½</td></tr>
        <tr><td>Full shift absence, tardy or early leave (4+ hours)</td><td>1</td></tr>
        <tr><td>Absence with no report or call 15+ minutes after start of workday</td><td>1½</td></tr>
    </table>
    """)

    render_html("""
    <table class="styled-table">
        <tr><th>Points Accumulated (in 12 months)</th><th>Action</th></tr>
        <tr><td>5 points</td><td>Coaching Session</td></tr>
        <tr><td>6 points</td><td>Verbal Warning</td></tr>
        <tr><td>7 points</td><td>Written Warning</td></tr>
        <tr><td>8 points</td><td>Termination</td></tr>
    </table>
    """)

    st.markdown(info_box("💡 <b>Perfect Attendance Rewards:</b> 1 point is removed after <b>2 consecutive months</b> of perfect attendance. Employees with <b>3 consecutive months</b> of perfect attendance receive a <b>$75 bonus</b> on their next paycheck."), unsafe_allow_html=True)
    st.markdown(info_box("⚠️ <b>No Call / No Show:</b> 2 consecutive days without reporting in will be treated as a voluntary resignation.", "yellow"), unsafe_allow_html=True)
    st.markdown(info_box("📋 <b>Doctor's Notes:</b> Required for illness greater than 1 day, up to a maximum of 3 consecutive days. The note must include dates of absence and the return-to-work date."), unsafe_allow_html=True)

    render_html("""
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
    """)

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
                finalize_quiz_submission(mk, score, 5)
                st.rerun()

# ─────────────────────────────────────────────
#  MODULE 4 — TIME OFF & LEAVE
# ─────────────────────────────────────────────
def show_module_timeoff():
    render_html("""
    <div class="content-section">
        <h2>⏰ Module 4: Time Off & Leave</h2>
        <p>Understand how attendance, leave, and time-off requests work so you can plan ahead with confidence.</p>

        <h3>🏖️ Vacation & Holiday Basics</h3>
        <ul>
            <li>Vacation eligibility and accrual depend on employment classification.</li>
            <li>Pre-approved vacation days are excluded from the attendance point system.</li>
            <li>AAP observes designated company holidays each year.</li>
        </ul>

        <h3>🩺 Sick Leave & Protected Time</h3>
        <ul>
            <li>Long-Term Sick Leave requires at least 3 consecutive physician-mandated days.</li>
            <li>FMLA eligibility requires 12 months of service and 1,250 hours worked.</li>
            <li>Notify HR within 30 days for qualifying life events affecting coverage.</li>
        </ul>
    </div>
    """)

    st.markdown("### ✅ Module 4 Checklist")
    checklist_items = {
        "vacation_rules": "I understand how pre-approved vacation impacts attendance points.",
        "holiday_awareness": "I know holiday/time-off expectations for my schedule.",
        "sick_leave_trigger": "I understand when Long-Term Sick Leave applies.",
        "fmla_baseline": "I know the baseline eligibility requirements for FMLA.",
        "life_event_window": "I know I must notify HR within 30 days for qualifying life events.",
    }

    mk = "timeoff"
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
        st.success(f"✅ Quiz completed! You scored {score}/4.")
    else:
        with st.form("quiz_timeoff"):
            q1 = st.radio("1. Pre-approved vacation days are excluded from the attendance point system.", ["True", "False"], key="to_q1", index=None)
            q2 = st.radio("2. Long-Term Sick Leave requires that an absence be:", ["At least 1 day", "At least 3 consecutive physician-mandated days", "At least 5 days", "Any absence with a doctor note"], key="to_q2", index=None)
            q3 = st.radio("3. FMLA eligibility requires:", ["60 days of employment", "6 months of employment", "12 months and 1,250 hours worked", "Manager approval only"], key="to_q3", index=None)
            q4 = st.radio("4. For qualifying life events that affect benefits, you should notify HR within:", ["7 days", "14 days", "30 days", "60 days"], key="to_q4", index=None)
            submitted = st.form_submit_button("Submit Quiz")
            if submitted:
                score = sum([
                    q1 == "True",
                    q2 == "At least 3 consecutive physician-mandated days",
                    q3 == "12 months and 1,250 hours worked",
                    q4 == "30 days",
                ])
                finalize_quiz_submission(mk, score, 4)
                st.rerun()

# ─────────────────────────────────────────────
#  MODULE 5 — BENEFITS
# ─────────────────────────────────────────────
def show_module_benefits():
    render_html("""
    <div class="content-section">
        <h2>💼 Module 5: Benefits</h2>
        <p>This module focuses on your benefit programs: medical, dental/vision, retirement, and employee support resources.</p>

        <h3>🏥 Health Benefits</h3>
        <ul>
            <li>Medical, dental, and vision become effective on the 1st of the month after 60 days of employment.</li>
            <li>AAP offers PPO and HDHP plan options for eligible employees.</li>
            <li>Teladoc is available day one for everyone in your household.</li>
        </ul>

        <h3>💰 Financial & Wellbeing Benefits</h3>
        <ul>
            <li>401(k) includes a 100% company match on the first 3% you contribute.</li>
            <li>Company-paid life insurance and EAP support are available for eligible employees.</li>
            <li>BenefitHub and LinkedIn Learning are available from day one.</li>
        </ul>
    </div>
    """)

    st.markdown("### ✅ Module 5 Checklist")
    checklist_items = {
        "health_effective": "I understand when medical/dental/vision coverage becomes active.",
        "plan_options": "I know there are multiple medical plan options available.",
        "401k_match": "I understand AAP's 401(k) match structure.",
        "teladoc_day1": "I know Teladoc is available on day one for my household.",
        "support_resources": "I know where to find EAP, BenefitHub, and LinkedIn Learning resources.",
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

    st.markdown("### 📝 Module 5 Quiz")
    if st.session_state.quiz_results.get(mk) is not None:
        score = st.session_state.quiz_results[mk]
        st.success(f"✅ Quiz completed! You scored {score}/4.")
    else:
        with st.form("quiz_benefits"):
            q1 = st.radio("1. Medical, dental, and vision benefits become effective on:",
                ["Your first day of work", "The 1st of the month following 60 days of employment", "After 90 days of employment", "January 1 of the following year"], key="b_q1", index=None)
            q2 = st.radio("2. What is AAP's 401(k) match for the first 3% you contribute?",
                ["50%", "75%", "100%", "200%"], key="b_q2", index=None)
            q3 = st.radio("3. Teladoc is available to:",
                ["Full-time employees only", "Full-time and part-time employees", "Everyone in your household, effective Day 1", "Employees after 60 days of service"], key="b_q3", index=None)
            q4 = st.radio("4. Which of the following is a day-one resource?",
                ["BenefitHub and LinkedIn Learning", "Medical plan enrollment only", "401(k) contributions", "FMLA leave"], key="b_q4", index=None)
            submitted = st.form_submit_button("Submit Quiz")
            if submitted:
                score = sum([
                    q1 == "The 1st of the month following 60 days of employment",
                    q2 == "100%",
                    q3 == "Everyone in your household, effective Day 1",
                    q4 == "BenefitHub and LinkedIn Learning",
                ])
                finalize_quiz_submission(mk, score, 4)
                st.rerun()

# ─────────────────────────────────────────────
#  MODULE 5 — FIRST STEPS
# ─────────────────────────────────────────────
def show_module_firststeps():
    render_html("""
    <div class="content-section">
        <h2>🚀 Module 6: Your First Steps</h2>
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
    """)

    render_html("""
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
    """)

    render_html("""
    <div class="content-section">
        <h3>👥 Key Contacts</h3>
    </div>
    """)

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

    contact_rows = "".join(
        f"<tr><td><b>{c[0]}</b></td><td>{c[1]}</td><td>{c[2]}{(' | ' + c[3]) if c[3] else ''}</td></tr>"
        for c in contacts
    )
    render_html(
        f'<table class="styled-table">'
        f"<tr><th>Name / Resource</th><th>Role</th><th>Contact</th></tr>"
        f"{contact_rows}</table>"
    )

    render_html("""
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
    """)

    st.markdown("### ✅ Module 6 Checklist")
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

    st.markdown("### 📝 Module 6 Quiz")
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
                finalize_quiz_submission(mk, score, 4)
                st.rerun()

    # Completion check
    total_pct = int(sum(st.session_state.progress.values()) / len(MODULES))
    if total_pct == 100:
        render_html("""
        <div class="content-section" style="border-left:4px solid #2ecc71;text-align:center;padding:36px;">
            <h2 style="color:#2ecc71;">🎉 Congratulations!</h2>
            <p style="font-size:1.1rem;">You have completed all six AAP orientation modules.
            Welcome to the team — we're glad you're here!</p>
        </div>
        """)


# ─────────────────────────────────────────────
#  WAREHOUSE MODULE 1 — WELCOME (WAREHOUSE)
# ─────────────────────────────────────────────
def show_wh_module_welcome():
    render_html("""
    <div class="content-section">
        <h2>🏢 Module 1: Welcome to AAP — Warehouse Edition</h2>

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
        <p>Today, AAP operates API, its independent warehouse and distributor, with <strong>two warehouse locations
        in the U.S.</strong> You are part of the team that makes this possible. The warehouse is the engine of API —
        the products that reach independent pharmacies and ultimately their patients pass through your hands every day.</p>

        <h3>Your Role in the Operation</h3>
        <p>As a warehouse employee, you are on the front lines of AAP's mission. Whether you are receiving shipments,
        pulling orders, stocking shelves, or preparing outbound freight, your accuracy, speed, and care directly
        affect the pharmacies we serve — and the patients who depend on them. <strong>What you do matters.</strong></p>

        <h3>Our Mission</h3>
        <p>AAP provides support and customized solutions for independent community pharmacies to enhance their
        profitability, streamline their operations and improve the quality of patient care.</p>

        <h3>Our Vision</h3>
        <p>Helping independent pharmacies thrive in a competitive healthcare market.</p>

        <h3>Our Values & Guiding Principles</h3>
        <p>Our values guide every decision, discussion and behavior — including every shift on the warehouse floor.</p>
    </div>
    """)

    values = [
        ("🎯", "Customer Focus", "Everything we do in the warehouse — accuracy, speed, careful handling — serves the independent pharmacies and the patients they care for. Customer service is not a department, it is an attitude that starts on the warehouse floor."),
        ("🤝", "Integrity", "We act with honesty and integrity. In a warehouse setting, this means accurate counts, honest reporting of damage or errors, and responsible use of company time and equipment."),
        ("💙", "Respect", "We treat coworkers, supervisors, and visitors with dignity and courtesy. We recognize the power of teamwork — no single role in this warehouse succeeds without the others."),
        ("⭐", "Excellence", "We strive for the highest quality in everything we do — from careful order fulfillment to proper storage and safe operation of equipment."),
        ("🙋", "Ownership", "We take responsibility for our work. When something goes wrong — a mispick, a damaged item, a near-miss — we report it honestly and help fix it."),
    ]

    for icon, value, desc in values:
        render_html(f"""
        <div class="content-section" style="padding:18px 24px;margin-bottom:10px;">
            <h3 style="margin-top:0">{icon} {value}</h3>
            <p style="margin:0">{desc}</p>
        </div>
        """)

    st.markdown("### ✅ Module 1 Checklist")
    checklist_items = {
        "ceo_welcome": "I have read the CEO welcome message.",
        "who_we_are": "I understand who AAP is and when it was founded.",
        "my_role": "I understand the warehouse team's role in serving pharmacies and patients.",
        "mission": "I can explain AAP's mission statement.",
        "vision": "I can explain AAP's vision statement.",
        "values_5": "I can name all five of AAP's core values.",
        "values_warehouse": "I understand how AAP's values apply to my work in the warehouse.",
    }

    mk = "wh_welcome"
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

    st.markdown("### 📝 Module 1 Quiz")
    if st.session_state.quiz_results.get(mk) is not None:
        score = st.session_state.quiz_results[mk]
        st.success(f"✅ Quiz completed! You scored {score}/4.")
    else:
        with st.form("quiz_wh_welcome"):
            q1 = st.radio("1. In what year was AAP formed?",
                ["2005", "2007", "2009", "2012"], key="ww_q1", index=None)
            q2 = st.radio("2. Which city is home to AAP's subsidiary API?",
                ["Phoenix, AZ", "Scottsboro, AL", "Huntsville, AL", "Nashville, TN"], key="ww_q2", index=None)
            q3 = st.radio("3. Which of the following is NOT one of AAP's five core values?",
                ["Integrity", "Ownership", "Innovation", "Excellence"], key="ww_q3", index=None)
            q4 = st.radio("4. How does the Ownership value apply to warehouse employees?",
                ["Only managers need to take ownership of problems",
                 "Report damage, errors, and near-misses honestly and help fix them",
                 "Ownership means protecting company assets from customers",
                 "Ownership refers to not losing your personal belongings at work"], key="ww_q4", index=None)
            submitted = st.form_submit_button("Submit Quiz")
            if submitted:
                score = sum([
                    q1 == "2009",
                    q2 == "Scottsboro, AL",
                    q3 == "Innovation",
                    q4 == "Report damage, errors, and near-misses honestly and help fix them",
                ])
                finalize_quiz_submission(mk, score, 4)
                st.rerun()


# ─────────────────────────────────────────────
#  WAREHOUSE MODULE 2 — CONDUCT (WAREHOUSE)
# ─────────────────────────────────────────────
def show_wh_module_conduct():
    render_html("""
    <div class="content-section">
        <h2>⚖️ Module 2: Code of Conduct & Ethics</h2>

        <h3>Our Commitment</h3>
        <p>The success of AAP is dependent upon our customers' trust — and in the warehouse, that trust is built
        every day through accuracy, honest reporting, and professional behavior. AAP will comply with all applicable
        laws and regulations and expects all employees to conduct themselves in accordance with those laws and with
        the highest ethical standards. <strong>Compliance with this policy is every AAP employee's responsibility.</strong></p>

        <h3>As an AAP Warehouse Employee, I Will…</h3>
        <ul>
            <li><strong>Work diligently and safely</strong> to meet the team's goals without cutting corners or
            creating hazards for others.</li>
            <li><strong>Protect company assets</strong> — including inventory, equipment, vehicles, and tools —
            from theft, misuse, or careless damage.</li>
            <li><strong>Report counts, pick errors, and damaged product honestly.</strong> Accurate records are
            essential to serving our pharmacy members correctly.</li>
            <li><strong>Treat coworkers, supervisors, and visitors</strong> with respect, dignity, and courtesy
            at all times — on the floor, in break areas, and in all company communications.</li>
            <li><strong>Follow all safety rules without exception.</strong> Shortcuts in a warehouse environment
            can cause serious injury to yourself or others.</li>
            <li><strong>Accept responsibility</strong> for my work and report any errors, near-misses, or damage
            to my supervisor immediately — not after the shift.</li>
            <li><strong>Protect confidential information</strong> — including inventory levels, pricing, customer
            data, and internal processes.</li>
            <li><strong>Report known or suspected illegal or unethical behavior</strong> to my supervisor immediately.</li>
            <li><strong>Avoid conflicts of interest</strong> and disclose any real or potential conflict to my employer.</li>
        </ul>
    </div>
    """)

    render_html("""
    <div class="content-section">
        <h3>⚠️ Unacceptable Conduct</h3>
        <p>The following are examples of conduct that may result in disciplinary action,
        <strong>up to and including termination of employment:</strong></p>
        <ul>
            <li>Theft or unauthorized removal of company property or inventory</li>
            <li>Falsification of records, including pick counts, timekeeping, or damage reports</li>
            <li>Working under the influence of alcohol or illegal drugs</li>
            <li>Possession, distribution, sale, or use of alcohol or illegal drugs on company premises</li>
            <li>Fighting, threatening violence, or creating a hostile environment on the warehouse floor</li>
            <li>Negligence or recklessness that leads to damage of inventory, equipment, or property</li>
            <li>Operating equipment (forklifts, pallet jacks, etc.) without authorization or proper certification</li>
            <li>Ignoring, bypassing, or disabling safety equipment or procedures</li>
            <li>Insubordination or other disrespectful conduct toward supervisors or coworkers</li>
            <li>Sexual or other unlawful harassment</li>
            <li>Possession of dangerous or unauthorized materials (explosives, unauthorized firearms) on premises</li>
            <li>Excessive absenteeism or any absence without notice</li>
            <li>Unauthorized use of company equipment, vehicles, or systems</li>
            <li>Unauthorized disclosure of business secrets or confidential information</li>
            <li>Unsatisfactory performance or conduct</li>
        </ul>
    </div>
    """)

    render_html("""
    <div class="content-section">
        <h3>🛡️ Equal Employment Opportunity (EEO)</h3>
        <p>Employment decisions at AAP are based on <strong>merit, qualifications, and abilities.</strong> AAP does
        not discriminate in employment opportunities or practices on the basis of race, color, religion, sex, national
        origin, age, disability, or any other characteristic protected by law.</p>
        <p>Employees can raise concerns and make reports without fear of reprisal. Anyone found to be engaging in
        unlawful discrimination will be subject to disciplinary action, up to and including termination.</p>

        <h3>🚫 Sexual & Other Unlawful Harassment</h3>
        <p>AAP is committed to providing a workplace free of discrimination and unlawful harassment — including on
        the warehouse floor, in break rooms, and in locker areas. Harassment can take many forms:</p>
        <ul>
            <li>Offensive comments, jokes, or insults</li>
            <li>Sexual advances or unnecessary touching</li>
            <li>Comments about a person's body</li>
            <li>Showing sexually suggestive images or objects</li>
            <li>Implied promises or threats tied to participation in sexual conduct</li>
        </ul>
        <p><strong>This conduct has no place at AAP and will not be tolerated anywhere on company premises.</strong></p>
        <p>If you believe you have been harassed, you should:</p>
        <ul>
            <li>Tell the offender their conduct is offensive (if comfortable doing so).</li>
            <li>Report it to your immediate supervisor or the HR department.</li>
            <li>If the harasser is your supervisor, contact the <strong>VP of Human Resources</strong> directly.</li>
        </ul>
        <p>No one will be retaliated against for complaining in good faith about harassment.</p>

        <h3>🔒 Confidentiality</h3>
        <p>All employees are required to sign a Confidentiality and Non-Disclosure Agreement upon hire. All written
        and verbal communication regarding the Company's operations or your position must remain strictly confidential
        unless otherwise permitted by your supervisor or by Company policy.
        <strong>Refusal to sign is grounds for immediate termination.</strong></p>
    </div>
    """)

    st.markdown("### ✅ Module 2 Checklist")
    checklist_items = {
        "code_reviewed": "I have read and understand the AAP Employee Code of Conduct.",
        "warehouse_honesty": "I understand the importance of honest reporting in a warehouse setting (counts, errors, damage).",
        "unacceptable": "I understand examples of unacceptable warehouse conduct, including unauthorized equipment operation.",
        "eeo": "I understand AAP's Equal Employment Opportunity policy.",
        "harassment": "I know how to report harassment and that retaliation is prohibited.",
        "confidentiality": "I understand my confidentiality obligations and will sign the NDA.",
        "reporting": "I know to report known or suspected illegal/unethical behavior to my supervisor immediately.",
    }

    mk = "wh_conduct"
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
        with st.form("quiz_wh_conduct"):
            q1 = st.radio("1. AAP's employment decisions are based on which of the following?",
                ["Seniority and connections",
                 "Merit, qualifications, and abilities",
                 "Education level only",
                 "Manager discretion"], key="wc_q1", index=None)
            q2 = st.radio("2. Operating a forklift or pallet jack without authorization or certification is considered:",
                ["Acceptable if supervised",
                 "Acceptable in an emergency",
                 "Unacceptable conduct and grounds for disciplinary action",
                 "Only a minor policy violation"], key="wc_q2", index=None)
            q3 = st.radio("3. If you find damaged inventory during your shift, you should:",
                ["Leave it and hope someone else handles it",
                 "Discard it to keep the floor clean",
                 "Report it to your supervisor immediately and document it accurately",
                 "Wait until end of shift to report it"], key="wc_q3", index=None)
            q4 = st.radio("4. Refusing to sign the Confidentiality and Non-Disclosure Agreement results in:",
                ["A written warning",
                 "A meeting with HR",
                 "Immediate termination",
                 "A probationary period"], key="wc_q4", index=None)
            submitted = st.form_submit_button("Submit Quiz")
            if submitted:
                score = sum([
                    q1 == "Merit, qualifications, and abilities",
                    q2 == "Unacceptable conduct and grounds for disciplinary action",
                    q3 == "Report it to your supervisor immediately and document it accurately",
                    q4 == "Immediate termination",
                ])
                finalize_quiz_submission(mk, score, 4)
                st.rerun()


# ─────────────────────────────────────────────
#  WAREHOUSE MODULE 3 — SAFETY & POLICIES
# ─────────────────────────────────────────────
def show_wh_module_safety():
    render_html("""
    <div class="content-section">
        <h2>🦺 Module 3: Warehouse Policies & Safety</h2>
        <p>This module covers the policies and safety expectations specific to your role in the warehouse.
        Safety is not optional — it protects you, your coworkers, and the products you handle every day.</p>

        <h3>🕐 Attendance & Punctuality</h3>
        <p>AAP uses a <strong>no-fault point system</strong> to manage attendance fairly and consistently for all
        non-exempt employees, including warehouse staff. In a warehouse environment, prompt attendance is especially
        critical — your absence affects pick rates, shipping schedules, and your teammates' workload.</p>

        <p><strong>Excluded from points (these do NOT count against you):</strong>
        FMLA leave, pre-approved personal leaves, bereavement leave, jury/witness duty, pre-approved vacation days,
        personal days, holidays, long-term sick leave, approved early leaves, short-term disability, and emergency
        closing absences.</p>

        <p><strong>Point Values:</strong></p>
    </div>
    """)

    render_html("""
    <table class="styled-table">
        <tr><th>Reason</th><th>Points</th></tr>
        <tr><td>Tardy up to 5 minutes (grace period)</td><td>0</td></tr>
        <tr><td>Tardy or early leave (less than 4 hours)</td><td>½</td></tr>
        <tr><td>Full shift absence, tardy or early leave (4+ hours)</td><td>1</td></tr>
        <tr><td>Absence with no report or call 15+ minutes after start of shift</td><td>1½</td></tr>
    </table>
    """)

    render_html("""
    <table class="styled-table">
        <tr><th>Points Accumulated (in 12 months)</th><th>Action</th></tr>
        <tr><td>5 points</td><td>Coaching Session</td></tr>
        <tr><td>6 points</td><td>Verbal Warning</td></tr>
        <tr><td>7 points</td><td>Written Warning</td></tr>
        <tr><td>8 points</td><td>Termination</td></tr>
    </table>
    """)

    st.markdown(info_box("💡 <b>Perfect Attendance Rewards:</b> 1 point is removed after <b>2 consecutive months</b> of perfect attendance. Employees with <b>3 consecutive months</b> of perfect attendance receive a <b>$75 bonus</b> on their next paycheck."), unsafe_allow_html=True)
    st.markdown(info_box("⚠️ <b>No Call / No Show:</b> 2 consecutive days without reporting in will be treated as a voluntary resignation.", "yellow"), unsafe_allow_html=True)
    st.markdown(info_box("📋 <b>Doctor's Notes:</b> Required for illness greater than 1 day, up to a maximum of 3 consecutive days. The note must include dates of absence and the return-to-work date."), unsafe_allow_html=True)

    render_html("""
    <div class="content-section">
        <h3>⏰ Shift Schedules & Overtime</h3>
    </div>
    """)

    st.markdown(info_box("📌 <b>PLACEHOLDER — Shift Schedule Details:</b> Update this section with your warehouse shift times, days of operation, and any rotation or on-call policies before publishing. Contact HR or your warehouse manager for these details.", "yellow"), unsafe_allow_html=True)

    render_html("""
    <div class="content-section">
        <p>Your supervisor will inform you of your assigned shift during your first day. All overtime must be
        <strong>pre-approved by your supervisor before it is performed.</strong> Unauthorized overtime or failure
        to work scheduled overtime may result in disciplinary action.</p>

        <h3>👔 Personal Appearance & Dress Code</h3>
        <p>Warehouse employees are expected to report to work dressed appropriately for a physical work environment.
        The following standards apply at all times:</p>
        <ul>
            <li>A neat, clean, and professional appearance is required.</li>
            <li><strong>Closed-toe shoes are required at all times on the warehouse floor.</strong>
            Open-toed shoes, sandals, or flip-flops are not permitted for safety reasons.</li>
            <li>Clothing must allow for safe, unrestricted movement.</li>
            <li>Avoid clothing with offensive or inappropriate logos or graphics.</li>
            <li>Due to allergies and asthma concerns, avoid wearing perfume or scented products.</li>
        </ul>
        <p>Employees found to be out of compliance with the dress code — especially closed-toe shoe requirements —
        will be asked to clock out, leave, and return dressed appropriately.</p>
    </div>
    """)

    render_html("""
    <div class="content-section">
        <h3>🦺 Personal Protective Equipment (PPE)</h3>
        <p>AAP provides PPE to all warehouse employees. You are responsible for using it properly and caring for
        the equipment issued to you.</p>

        <table class="styled-table">
            <tr><th>PPE Item</th><th>Requirement</th></tr>
            <tr><td>Closed-toe shoes / boots</td><td>Required — must be worn at all times on the warehouse floor</td></tr>
            <tr><td>Gloves</td><td>Available to all employees — recommended when handling boxes, sharp edges, or heavy items</td></tr>
        </table>
    </div>
    """)

    st.markdown(info_box("📌 <b>PLACEHOLDER — Additional PPE:</b> If your warehouse requires high-visibility vests, eye protection, hard hats, or other PPE for specific tasks or zones, add those requirements here before publishing.", "yellow"), unsafe_allow_html=True)

    render_html("""
    <div class="content-section">
        <h3>🛡️ Warehouse Safety Rules</h3>
        <p>The <strong>VP of Human Resources</strong> is responsible for AAP's safety program. Each warehouse
        employee is expected to:</p>
        <ul>
            <li>Obey all safety rules and exercise caution in all work activities at all times.</li>
            <li>Immediately report any unsafe condition, equipment malfunction, or hazard to your supervisor —
            do not wait until the end of your shift.</li>
            <li>Report <strong>all work-related injuries to HR or your supervisor immediately,</strong>
            no matter how minor. Even small injuries must be documented.</li>
            <li>Wear required PPE whenever you are on the warehouse floor.</li>
            <li>Keep aisles, emergency exits, and fire suppression equipment clear at all times.</li>
            <li>Never operate equipment (forklifts, pallet jacks, reach trucks) without proper training,
            authorization, and certification for that specific piece of equipment.</li>
            <li>Do not take shortcuts that compromise safety, even under time pressure.</li>
        </ul>
        <p><strong>Violating safety standards may result in disciplinary action, up to and including termination.</strong></p>
        <p>All work-related accidents require <strong>immediate drug and alcohol testing.</strong></p>

        <h3>🚜 Forklift & Equipment Policies</h3>
        <p>Forklifts, pallet jacks, reach trucks, and other powered industrial trucks are potentially dangerous
        equipment. The following rules apply to all warehouse employees:</p>
        <ul>
            <li>Only employees who are <strong>properly trained and certified</strong> for a specific piece of
            equipment may operate it.</li>
            <li>Certification is role-specific. Do not assume that certification for one type of equipment
            authorizes you to operate another.</li>
            <li>Conduct a <strong>pre-shift inspection</strong> of any equipment you will operate and report
            any defects to your supervisor before use.</li>
            <li>Never operate equipment at unsafe speeds or in a manner that endangers other employees.</li>
            <li>Pedestrians always have the right of way in designated pedestrian zones.</li>
            <li>Never allow unauthorized personnel to ride on or operate powered equipment.</li>
            <li>Report any equipment damage, malfunction, or near-miss immediately.</li>
        </ul>
    </div>
    """)

    st.markdown(info_box("📌 <b>PLACEHOLDER — Forklift Certification Roles:</b> Specify which warehouse roles require forklift or equipment certification, which piece(s) of equipment each role is authorized to operate, and the certification process/timeline here before publishing.", "yellow"), unsafe_allow_html=True)

    render_html("""
    <div class="content-section">
        <h3>📦 Warehouse Procedures & Receiving Process</h3>

        <h3>Receiving Inbound Shipments</h3>
        <ul>
            <li>Verify all inbound shipments against the <strong>purchase order (PO)</strong> or packing slip
            before signing for the delivery.</li>
            <li>Inspect all incoming product for damage before accepting the shipment. Note any damage on the
            delivery receipt and photograph damaged items before moving them.</li>
            <li>Do not accept shipments with missing, altered, or illegible documentation without supervisor approval.</li>
            <li>All discrepancies between the PO and the physical shipment must be reported to your supervisor
            and documented immediately.</li>
        </ul>

        <h3>Storage & Organization</h3>
        <ul>
            <li>All product must be stored in its designated location. Do not place product in random locations
            — this causes inventory errors that affect pharmacy orders.</li>
            <li>Follow <strong>FIFO (First In, First Out)</strong> rotation: older stock goes to the front,
            newer stock goes behind it.</li>
            <li>Do not stack product higher than designated height limits. Unstable stacking is a safety hazard.</li>
            <li>Report any product approaching expiration dates to your supervisor promptly.</li>
        </ul>

        <h3>Order Picking & Fulfillment</h3>
        <ul>
            <li>Pick orders accurately — errors in pharmaceutical distribution have real consequences for pharmacies
            and their patients.</li>
            <li>Double-check product NDC numbers, quantities, and lot numbers before placing items in an order.</li>
            <li>If a product cannot be located or is out of stock, notify your supervisor immediately. Do not
            substitute products without authorization.</li>
            <li>All picked orders must be verified before they are sealed and staged for shipping.</li>
        </ul>

        <h3>Outbound Shipping</h3>
        <ul>
            <li>All outbound orders must be properly packaged, labeled, and staged in designated shipping areas.</li>
            <li>Confirm the carrier and shipping method match the order before releasing freight.</li>
            <li>Any outbound discrepancies must be reported to your supervisor before the shipment leaves
            the facility.</li>
        </ul>

        <h3>🚭 Drug & Alcohol Policy</h3>
        <p>AAP maintains a <strong>drug and alcohol-free workplace.</strong> This is especially critical in a
        warehouse environment where impaired judgment can cause serious injury. Employees are subject to
        <strong>random drug testing at any time,</strong> and all work-related accidents require immediate
        drug and alcohol testing.</p>
        <ul>
            <li>Violations may result in immediate termination and/or required participation in a rehab program.</li>
            <li>The Employee Assistance Program (EAP) is available to employees who need support.</li>
        </ul>

        <h3>🚷 Workplace Violence</h3>
        <p>AAP has zero tolerance for workplace violence. All threatening incidents must be
        <strong>reported within 24 hours</strong> and will be investigated and documented by Human Resources.</p>
    </div>
    """)

    st.markdown("### ✅ Module 3 Checklist")
    checklist_items = {
        "point_system": "I understand the no-fault attendance point system and the point values.",
        "corrective_levels": "I know the corrective action steps (coaching at 5, verbal at 6, written at 7, termination at 8).",
        "perfect_att": "I know I can earn a point removal and a $75 bonus for perfect attendance.",
        "no_call": "I understand that 2 consecutive no-call/no-shows may be treated as a resignation.",
        "closed_toe": "I understand that closed-toe shoes are required on the warehouse floor at all times.",
        "ppe_gloves": "I know gloves are available to all warehouse employees.",
        "safety_report": "I know to immediately report any unsafe condition or work-related injury to my supervisor.",
        "equipment_cert": "I understand I may only operate equipment I am trained and certified for.",
        "receiving": "I understand the receiving process: verify PO, inspect for damage, document discrepancies.",
        "fifo": "I understand FIFO rotation and accurate order picking procedures.",
        "drug_policy": "I understand AAP's drug and alcohol-free workplace policy and accident testing requirement.",
    }

    mk = "wh_safety"
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
        with st.form("quiz_wh_safety"):
            q1 = st.radio("1. Which footwear is required at all times on the warehouse floor?",
                ["Any athletic shoe", "Closed-toe shoes or boots", "Steel-toed boots only", "Any shoes are acceptable"], key="ws_q1", index=None)
            q2 = st.radio("2. What should you do if you notice damage on an inbound shipment?",
                ["Accept it and report it later",
                 "Refuse to unload the truck",
                 "Note it on the delivery receipt, photograph the damage, then notify your supervisor",
                 "Set it aside and check again at end of shift"], key="ws_q2", index=None)
            q3 = st.radio("3. How many points within 12 months results in termination?",
                ["6 points", "7 points", "8 points", "10 points"], key="ws_q3", index=None)
            q4 = st.radio("4. What does FIFO mean in warehouse storage?",
                ["First In, First Out — older stock goes to the front",
                 "Fast Items, Fast Outbound — priority items ship first",
                 "Full Inventory, Full Order — no partial picks allowed",
                 "First Inspection, Final Output — check before shipping"], key="ws_q4", index=None)
            q5 = st.radio("5. You may operate a forklift if:",
                ["You have operated one before at a previous job",
                 "Your supervisor is watching",
                 "You are trained, authorized, and certified for that specific equipment",
                 "The regular operator is absent and it is an emergency"], key="ws_q5", index=None)
            submitted = st.form_submit_button("Submit Quiz")
            if submitted:
                score = sum([
                    q1 == "Closed-toe shoes or boots",
                    q2 == "Note it on the delivery receipt, photograph the damage, then notify your supervisor",
                    q3 == "8 points",
                    q4 == "First In, First Out — older stock goes to the front",
                    q5 == "You are trained, authorized, and certified for that specific equipment",
                ])
                finalize_quiz_submission(mk, score, 5)
                st.rerun()


# ─────────────────────────────────────────────
#  WAREHOUSE MODULE 4 — TIME OFF & LEAVE
# ─────────────────────────────────────────────
def show_wh_module_timeoff():
    render_html("""
    <div class="content-section">
        <h2>⏰ Module 4: Time Off & Leave — Warehouse Edition</h2>
        <p>Plan your time with confidence by understanding attendance points, leave, and request expectations.</p>

        <h3>🗓️ Attendance & Time-Off Essentials</h3>
        <ul>
            <li>Pre-approved vacation does not count toward attendance points.</li>
            <li>No-call/no-show and repeated absences accumulate points quickly.</li>
            <li>Use approved channels to report absences and request time off.</li>
        </ul>

        <h3>🩺 Leave Coverage</h3>
        <ul>
            <li>Long-Term Sick Leave applies to qualifying physician-mandated absences.</li>
            <li>FMLA eligibility requires 12 months of service and 1,250 hours worked.</li>
            <li>Report qualifying life events to HR within 30 days.</li>
        </ul>
    </div>
    """)

    st.markdown("### ✅ Module 4 Checklist")
    checklist_items = {
        "vacation_points": "I understand pre-approved vacation is excluded from attendance points.",
        "attendance_reporting": "I know how to report absences and request time off properly.",
        "ltsl_rules": "I understand when Long-Term Sick Leave applies.",
        "fmla_requirements": "I know the baseline requirements for FMLA eligibility.",
        "life_event_deadline": "I know life-event benefits updates must be reported within 30 days.",
    }

    mk = "wh_timeoff"
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
        st.success(f"✅ Quiz completed! You scored {score}/4.")
    else:
        with st.form("quiz_wh_timeoff"):
            q1 = st.radio("1. Pre-approved vacation days are excluded from attendance points.", ["True", "False"], key="wto_q1", index=None)
            q2 = st.radio("2. Long-Term Sick Leave requires:", ["At least 1 day", "At least 3 consecutive physician-mandated days", "At least 5 consecutive days", "Any verbal notice"], key="wto_q2", index=None)
            q3 = st.radio("3. FMLA eligibility is generally:", ["6 months of service", "12 months and 1,250 hours worked", "Immediately at hire", "Manager-only approval"], key="wto_q3", index=None)
            q4 = st.radio("4. Life-event benefit changes should be reported within:", ["7 days", "14 days", "30 days", "90 days"], key="wto_q4", index=None)
            submitted = st.form_submit_button("Submit Quiz")
            if submitted:
                score = sum([
                    q1 == "True",
                    q2 == "At least 3 consecutive physician-mandated days",
                    q3 == "12 months and 1,250 hours worked",
                    q4 == "30 days",
                ])
                finalize_quiz_submission(mk, score, 4)
                st.rerun()


# ─────────────────────────────────────────────
#  WAREHOUSE MODULE 5 — BENEFITS (WAREHOUSE)
# ─────────────────────────────────────────────
def show_wh_module_benefits():
    render_html("""
    <div class="content-section">
        <h2>💼 Module 5: Benefits — Warehouse Edition</h2>
        <p>This module focuses on the benefit programs available to warehouse team members, including health, retirement, and support resources.</p>

        <h3>🏥 Core Benefits</h3>
        <ul>
            <li>Medical, dental, and vision benefits activate on the 1st of the month after 60 days (for eligible employees).</li>
            <li>401(k) includes a 100% match on the first 3% of employee contribution.</li>
            <li>Teladoc and LinkedIn Learning are available from day one.</li>
        </ul>

        <h3>🤝 Support Programs</h3>
        <ul>
            <li>LifeMatters EAP is available 24/7 for confidential personal support.</li>
            <li>BenefitHub provides employee discounts and perks.</li>
            <li>HR can help with plan questions and enrollment timing.</li>
        </ul>
    </div>
    """)

    st.markdown("### ✅ Module 5 Checklist")
    checklist_items = {
        "effective_date": "I understand when eligible health benefits begin.",
        "retirement_match": "I understand the 401(k) matching structure.",
        "day1_resources": "I know Teladoc and LinkedIn Learning are available day one.",
        "eap_support": "I know how to access the EAP for confidential support.",
        "benefits_help": "I know who to contact for benefits help and enrollment questions.",
    }

    mk = "wh_benefits"
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
        with st.form("quiz_wh_benefits"):
            q1 = st.radio("1. When do eligible medical benefits become effective?",
                ["Day 1", "After 30 days", "The 1st of the month following 60 days", "After 1 year"], key="wb_q1", index=None)
            q2 = st.radio("2. What is AAP's 401(k) match for the first 3% contributed?",
                ["50%", "75%", "100%", "No match"], key="wb_q2", index=None)
            q3 = st.radio("3. Which resources are available on day one?",
                ["Only payroll", "Teladoc and LinkedIn Learning", "Medical plan enrollment", "401(k) loan options"], key="wb_q3", index=None)
            q4 = st.radio("4. Which resource provides confidential wellbeing support?",
                ["BenefitHub", "LifeMatters EAP", "Payroll portal", "OSHA"], key="wb_q4", index=None)
            submitted = st.form_submit_button("Submit Quiz")
            if submitted:
                score = sum([
                    q1 == "The 1st of the month following 60 days",
                    q2 == "100%",
                    q3 == "Teladoc and LinkedIn Learning",
                    q4 == "LifeMatters EAP",
                ])
                finalize_quiz_submission(mk, score, 4)
                st.rerun()


# ─────────────────────────────────────────────
#  WAREHOUSE MODULE 5 — FIRST STEPS (WAREHOUSE)
# ─────────────────────────────────────────────
def show_wh_module_firststeps():
    render_html("""
    <div class="content-section">
        <h2>🚀 Module 6: Your First Steps — Warehouse Edition</h2>
        <p>This module covers everything you need to get set up and hit the ground running on Day 1 and beyond
        in your warehouse role.</p>

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
            <li>Drug Policy Acknowledgment</li>
            <li>Employee's Responsibility to Report Drug Diversion</li>
            <li>API Staff Alerts</li>
            <li>Form I-9 (Employment Eligibility Verification)</li>
            <li>Employee Handbook Acknowledgment</li>
            <li>Warehouse Safety Acknowledgment</li>
        </ul>
    </div>
    """)

    render_html("""
    <div class="content-section">
        <h3>💻 Systems You'll Use</h3>

        <h3>Paylocity — Payroll & HR Self-Service</h3>
        <p>Paylocity is AAP's payroll platform where you'll view pay stubs, manage direct deposit, and access
        tax forms. <strong>API Company ID: 123959</strong></p>
        <p>To register: Go to <strong>access.paylocity.com</strong>, click "Register New User," and enter your
        Company ID, last name, SSN, and home zip code.</p>

        <h3>BambooHR — Employee Records & Directory</h3>
        <p>BambooHR is AAP's HRIS (HR Information System). You'll use it to access your employee records and
        the company directory. HR will walk you through BambooHR during orientation. Be sure to
        <strong>upload your profile photo</strong> after logging in.</p>

        <h3>Teladoc — Free Telehealth (Day 1)</h3>
        <p>Set up your Teladoc account by visiting <strong>Teladoc.com</strong> and clicking "Get Started."
        Select your health insurance plan from the drop-down and confirm coverage. General medical visits,
        mental health visits, and more are <strong>completely free.</strong></p>

        <h3>LinkedIn Learning — Professional Development (Day 1)</h3>
        <p>You should have received an activation email when you were offered the position. If you didn't receive
        it, contact HR. Over <strong>16,000 courses</strong> available on any device, at your own pace.</p>
    </div>
    """)

    render_html("""
    <div class="content-section">
        <h3>🏭 Your First Day on the Warehouse Floor</h3>
        <p>Here's what to expect when you arrive for your first shift:</p>
        <ul>
            <li>Report to <strong>HR or your assigned supervisor</strong> upon arrival to complete
            remaining paperwork and receive your facility tour.</li>
            <li>You will be shown your workstation, locker assignment (if applicable), break areas,
            emergency exits, and restroom locations.</li>
            <li>Review the facility's safety posting board — OSHA required postings and emergency
            procedures are located there.</li>
            <li>You will be issued any required PPE. Confirm fit and ask questions before heading to the floor.</li>
            <li>You will shadow a trainer or experienced teammate for your first shifts before working independently.</li>
            <li>Do not operate any equipment until you have been formally trained and authorized to do so.</li>
        </ul>
    </div>
    """)

    st.markdown(info_box("📌 <b>PLACEHOLDER — Equipment Training Schedule:</b> Add the specific timeline and process for forklift and equipment certification for applicable roles here before publishing. Include who schedules the training and approximately how many days of shadowing are expected before independent operation.", "yellow"), unsafe_allow_html=True)

    render_html("""
    <div class="content-section">
        <h3>📆 What to Expect in Your First 90 Days</h3>
        <ul>
            <li><strong>Days 1–30:</strong> Complete orientation and all paperwork. Receive your facility tour
            and safety briefing. Shadow experienced teammates. Get set up on Paylocity and BambooHR.
            Complete your 30-day check-in survey.</li>
            <li><strong>Days 31–60:</strong> Begin executing core warehouse responsibilities with supervisor
            support. Build speed and accuracy in your role. Complete your 60-day survey and become eligible
            for most benefits.</li>
            <li><strong>Days 61–90:</strong> Build consistency and confidence. Identify opportunities to improve
            your process. Complete equipment training/certification if applicable to your role.
            Your introductory period concludes at 90 days.</li>
        </ul>

        <h3>📬 Important Reminders Going Forward</h3>
        <ul>
            <li>Update HR immediately with any personal data changes (address, dependents, emergency contacts).</li>
            <li>If you have a qualifying life event (marriage, birth, etc.), notify HR within <strong>30 days</strong>
            to make benefits changes.</li>
            <li>Performance evaluations are conducted approximately every 12 months from your hire anniversary.</li>
            <li>AAP is an at-will employer — either party may end the relationship at any time for any lawful reason.</li>
            <li>Report all concerns through the problem resolution process — starting with your supervisor,
            then escalating to HR and management if needed.</li>
            <li><strong>Never hesitate to report a safety concern.</strong> You cannot get in trouble for reporting
            a genuine safety hazard — you can only get in trouble for ignoring one.</li>
        </ul>
    </div>
    """)

    render_html("""
    <div class="content-section">
        <h3>👥 Key Contacts</h3>
    </div>
    """)

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

    contact_rows = "".join(
        f"<tr><td><b>{c[0]}</b></td><td>{c[1]}</td><td>{c[2]}{(' | ' + c[3]) if c[3] else ''}</td></tr>"
        for c in contacts
    )
    render_html(
        f'<table class="styled-table">'
        f"<tr><th>Name / Resource</th><th>Role</th><th>Contact</th></tr>"
        f"{contact_rows}</table>"
    )

    st.markdown("### ✅ Module 6 Checklist")
    checklist_items = {
        "paperwork": "I understand which documents I need to sign during orientation.",
        "paylocity": "I know how to register for Paylocity (Company ID: 123959).",
        "bamboohr": "I understand what BambooHR is used for and that I need to upload my photo.",
        "teladoc_setup": "I know how to set up my Teladoc account.",
        "linkedin": "I have received or know how to request my LinkedIn Learning activation.",
        "day1_floor": "I know what to expect on my first day on the warehouse floor.",
        "no_equip": "I understand I cannot operate equipment until I am formally trained and authorized.",
        "key_contacts": "I know who to contact for HR, benefits, payroll, and safety questions.",
        "first90": "I understand what is expected of me in my first 30, 60, and 90 days.",
        "at_will": "I understand AAP is an at-will employer.",
        "life_event": "I know I have 30 days to notify HR of qualifying life events for benefits changes.",
        "safety_report_reminder": "I know I can and should always report genuine safety concerns without fear.",
    }

    mk = "wh_firststeps"
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

    st.markdown("### 📝 Module 6 Quiz")
    if st.session_state.quiz_results.get(mk) is not None:
        score = st.session_state.quiz_results[mk]
        st.success(f"✅ Quiz completed! You scored {score}/4.")
    else:
        with st.form("quiz_wh_firststeps"):
            q1 = st.radio("1. What is the Paylocity Company ID for API employees?",
                ["123456", "123959", "987654", "112358"], key="wf_q1", index=None)
            q2 = st.radio("2. How many days do you have to notify HR of a qualifying life event for benefits changes?",
                ["7 days", "14 days", "30 days", "60 days"], key="wf_q2", index=None)
            q3 = st.radio("3. When can you begin operating warehouse equipment such as a forklift?",
                ["After your first week of employment",
                 "Immediately if you have experience from a previous job",
                 "Only after you have been formally trained and authorized for that specific equipment",
                 "After your 90-day introductory period ends"], key="wf_q3", index=None)
            q4 = st.radio("4. AAP's employment relationship is best described as:",
                ["Guaranteed for a fixed term",
                 "At-will, meaning either party may end employment at any time for any lawful reason",
                 "Protected by a union contract",
                 "Governed by a mandatory 2-year commitment"], key="wf_q4", index=None)
            submitted = st.form_submit_button("Submit Quiz")
            if submitted:
                score = sum([
                    q1 == "123959",
                    q2 == "30 days",
                    q3 == "Only after you have been formally trained and authorized for that specific equipment",
                    q4 == "At-will, meaning either party may end employment at any time for any lawful reason",
                ])
                finalize_quiz_submission(mk, score, 4)
                st.rerun()

    # Completion check
    active_modules = WAREHOUSE_MODULES if st.session_state.get("role_track") == "warehouse" else MODULES
    total_pct = int(sum(st.session_state.progress.values()) / len(active_modules))
    if total_pct == 100:
        render_html("""

        <div class="content-section" style="border-left:4px solid #2ecc71;text-align:center;padding:36px;">
            <h2 style="color:#2ecc71;">🎉 Congratulations!</h2>
            <p style="font-size:1.1rem;">You have completed all six AAP Warehouse orientation modules.
            Welcome to the team — we're glad you're here!</p>
        </div>
        """)


# ─────────────────────────────────────────────
#  ROUTER  — gate everything behind authentication
# ─────────────────────────────────────────────
render_sound_engine()

if not st.session_state.authenticated:
    show_login()
else:
    general_map = {
        "welcome":    show_module_welcome,
        "conduct":    show_module_conduct,
        "policies":   show_module_policies,
        "timeoff":    show_module_timeoff,
        "benefits":   show_module_benefits,
        "firststeps": show_module_firststeps,
    }
    warehouse_map = {
        "wh_welcome":    show_wh_module_welcome,
        "wh_conduct":    show_wh_module_conduct,
        "wh_safety":     show_wh_module_safety,
        "wh_timeoff":    show_wh_module_timeoff,
        "wh_benefits":   show_wh_module_benefits,
        "wh_firststeps": show_wh_module_firststeps,
    }

    is_warehouse = st.session_state.get("role_track") == "warehouse"
    module_map   = warehouse_map if is_warehouse else general_map

    selected = st.session_state.selected_module
    if selected and selected in module_map:
        render_module_shell_start(selected)
        module_map[selected]()
        render_module_shell_end()
    else:
        show_home()