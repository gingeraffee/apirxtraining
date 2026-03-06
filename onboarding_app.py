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
=======
# Native Streamlit logo — appears in the top-left corner of the sidebar
st.logo(_sidebar_logo, link="https://apirx.com")

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
render_html("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ════════════════════════════════════════════════
       MODERN APPLE — MIDNIGHT & CRIMSON DESIGN SYSTEM
       Glassmorphism · 8pt Grid · Inter Typeface
       ════════════════════════════════════════════════ */

    /* ── Design Tokens ── */
    :root {
        --apple-ink: #0A0A0B;
        --apple-surface: #F5F5F7;
        --apple-crimson: #B11226;
        --apple-crimson-soft: rgba(177,18,38,0.08);
        --apple-crimson-glow: rgba(177,18,38,0.18);
        --apple-gray-100: #F5F5F7;
        --apple-gray-200: #E8E8ED;
        --apple-gray-300: #D2D2D7;
        --apple-gray-400: #86868B;
        --apple-gray-500: #6E6E73;
        --apple-gray-600: #424245;
        --apple-white: #FFFFFF;
        --apple-radius-lg: 24px;
        --apple-radius-md: 16px;
        --apple-radius-sm: 12px;
        --apple-radius-xs: 8px;
        --apple-glass-bg: rgba(255,255,255,0.72);
        --apple-glass-border: 1px solid rgba(255,255,255,0.18);
        --apple-glass-blur: blur(20px);
        --apple-shadow-soft: 0 20px 50px rgba(0,0,0,0.05);
        --apple-shadow-hover: 0 24px 56px rgba(0,0,0,0.09);
        --apple-shadow-deep: 0 32px 64px rgba(0,0,0,0.12);
        --apple-transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }

    /* ── Base Reset ── */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Helvetica Neue', sans-serif !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    body { line-height: 1.7; color: var(--apple-ink); }

    .stApp {
        background: var(--apple-surface) !important;
    }

    /* ── Typography — Clear Hierarchy ── */
    h1, h2, h3 {
        font-family: 'Inter', -apple-system, 'SF Pro Display', sans-serif !important;
        color: var(--apple-ink) !important;
        letter-spacing: -0.025em;
        line-height: 1.2;
    }
    h1 { font-weight: 700 !important; }
    h2 { font-weight: 700 !important; }
    h3 { font-weight: 600 !important; }
    p, li, td, span { font-weight: 400; line-height: 1.7; }

    .page-title {
        font-family: 'Inter', -apple-system, 'SF Pro Display', sans-serif;
        font-size: 2.4rem;
        font-weight: 800;
        color: var(--apple-ink);
        letter-spacing: -0.035em;
        border-bottom: 2px solid var(--apple-gray-200);
        padding-bottom: 16px;
        margin-bottom: 8px;
    }
    .page-subtitle { color: var(--apple-gray-500); font-size: 1.05rem; margin-bottom: 32px; font-weight: 400; line-height: 1.7; }

    /* ── Sidebar Container — Frosted Midnight Glass ── */
    [data-testid="stSidebar"] {
        background: rgba(10,10,11,0.92) !important;
        backdrop-filter: blur(40px) saturate(180%);
        -webkit-backdrop-filter: blur(40px) saturate(180%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    [data-testid="stSidebar"] .block-container {
        padding-top: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    .sidebar-header {
        background: rgba(255,255,255,0.06);
        backdrop-filter: var(--apple-glass-blur);
        -webkit-backdrop-filter: var(--apple-glass-blur);
        border-radius: var(--apple-radius-md);
        padding: 20px 16px;
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .sidebar-header * { color: var(--apple-gray-100) !important; }
    .sidebar-header .sidebar-username {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
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
        background: var(--apple-crimson);
        transition: width 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    .sidebar-section-label {
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        color: rgba(255,255,255,0.36);
        margin: 12px 2px 8px;
        font-weight: 600;
    }

    /* ── Sidebar Radio Navigation — Subtle Glass Pills ── */
    [data-testid="stSidebar"] .stRadio > div { gap: 4px !important; }
    [data-testid="stSidebar"] .stRadio label {
        color: rgba(255,255,255,0.72) !important;
        border-radius: var(--apple-radius-sm) !important;
        padding: 10px 14px !important;
        transition: var(--apple-transition) !important;
        font-size: 0.84rem !important;
        font-weight: 500 !important;
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
        background: rgba(255,255,255,0.10) !important;
        border-color: rgba(255,255,255,0.20) !important;
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] .stRadio label:has(input[type="radio"]:checked) p,
    [data-testid="stSidebar"] .stRadio label:has(input[type="radio"]:checked) span {
        color: #FFFFFF !important;
        background: transparent !important;
    }
    [data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child {
        background: rgba(255,255,255,0.08) !important;
        border-color: rgba(255,255,255,0.20) !important;
    }
    [data-testid="stSidebar"] .stRadio [data-baseweb="radio"] [aria-checked="true"] > div:first-child,
    [data-testid="stSidebar"] .stRadio input[type="radio"]:checked + div > div:first-child {
        background: transparent !important;
        border-color: transparent !important;
        box-shadow: none !important;
    }

    /* ── Module Cards ── */
    .module-card {
        background: var(--apple-glass-bg);
        backdrop-filter: var(--apple-glass-blur);
        -webkit-backdrop-filter: var(--apple-glass-blur);
        border-radius: var(--apple-radius-md);
        padding: 24px;
        margin-bottom: 16px;
        border-left: 4px solid var(--apple-crimson);
        border-top: none;
        border-right: 1px solid rgba(255,255,255,0.18);
        border-bottom: 1px solid rgba(255,255,255,0.18);
        box-shadow: var(--apple-shadow-soft);
        transition: var(--apple-transition);
    }
    .module-card:hover { transform: translateY(-2px); box-shadow: var(--apple-shadow-hover); }
    .module-card.complete { border-left-color: #34C759; background: rgba(52,199,89,0.06); }

    /* ── Post-login Shell ── */
    .post-auth-shell {
        background: transparent;
        border-radius: var(--apple-radius-lg);
        padding: 0;
        margin-bottom: 24px;
    }

    .module-shell {
        background: var(--apple-glass-bg);
        backdrop-filter: var(--apple-glass-blur);
        -webkit-backdrop-filter: var(--apple-glass-blur);
        border-radius: var(--apple-radius-lg);
        border: 1px solid rgba(255,255,255,0.18);
        box-shadow: var(--apple-shadow-deep);
        padding: 32px;
        margin-bottom: 24px;
    }

    .module-page-hero {
        background: var(--apple-ink);
        border-radius: var(--apple-radius-lg);
        padding: 32px;
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: var(--apple-shadow-deep);
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .module-page-hero::after {
        content: "";
        position: absolute;
        width: 400px;
        height: 400px;
        right: -160px;
        top: -200px;
        background: radial-gradient(circle, var(--apple-crimson-glow) 0%, transparent 70%);
    }
    .module-page-title {
        color: var(--apple-gray-100) !important;
        font-family: 'Inter', -apple-system, 'SF Pro Display', sans-serif !important;
        font-size: 1.6rem;
        font-weight: 700;
        letter-spacing: -0.025em;
        margin: 4px 0 8px;
        position: relative;
        z-index: 1;
    }
    .module-page-sub {
        color: var(--apple-gray-400);
        font-size: 0.92rem;
        line-height: 1.7;
        margin: 0;
        position: relative;
        z-index: 1;
        max-width: 920px;
    }
    .module-meta-row {
        margin-top: 16px;
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        position: relative;
        z-index: 1;
    }

    /* ── Premium Hero (Home Dashboard) ── */
    .premium-hero {
        background: var(--apple-ink);
        border-radius: var(--apple-radius-lg);
        padding: 40px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: var(--apple-shadow-deep);
    }
    .premium-hero::before {
        content: "";
        position: absolute;
        width: 500px;
        height: 500px;
        right: -180px;
        top: -200px;
        background: radial-gradient(circle, rgba(177,18,38,0.25) 0%, transparent 65%);
    }
    .premium-hero::after {
        content: "";
        position: absolute;
        width: 400px;
        height: 400px;
        left: -150px;
        bottom: -200px;
        background: radial-gradient(circle, rgba(177,18,38,0.10) 0%, transparent 70%);
    }
    .premium-hero h1 {
        color: var(--apple-gray-100) !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.035em !important;
        margin: 0 0 8px 0 !important;
        position: relative;
        z-index: 1;
    }
    .premium-hero p {
        color: var(--apple-gray-400) !important;
        font-size: 1rem;
        line-height: 1.7;
        margin: 0 !important;
        max-width: 760px;
        position: relative;
        z-index: 1;
    }
    .premium-kicker {
        display: inline-block;
        font-size: 0.68rem;
        color: var(--apple-crimson);
        letter-spacing: 0.18em;
        text-transform: uppercase;
        font-weight: 700;
        margin-bottom: 12px;
        position: relative;
        z-index: 1;
    }

    /* ── Stat Cards ── */
    .premium-stat {
        background: var(--apple-glass-bg);
        backdrop-filter: var(--apple-glass-blur);
        -webkit-backdrop-filter: var(--apple-glass-blur);
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: var(--apple-radius-md);
        padding: 20px;
        box-shadow: var(--apple-shadow-soft);
        min-height: 110px;
        transition: var(--apple-transition);
    }
    .premium-stat:hover { transform: translateY(-2px); box-shadow: var(--apple-shadow-hover); }
    .premium-stat-label {
        font-size: 0.68rem;
        color: var(--apple-gray-500);
        letter-spacing: 0.10em;
        text-transform: uppercase;
        font-weight: 600;
    }
    .premium-stat-value {
        color: var(--apple-ink);
        font-size: 1.8rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin-top: 4px;
    }
    .premium-stat-sub { color: var(--apple-gray-400); font-size: 0.78rem; margin-top: 6px; line-height: 1.5; }

    /* ── Module Cards (Home Grid) ── */
    .module-card-premium {
        background: var(--apple-glass-bg);
        backdrop-filter: var(--apple-glass-blur);
        -webkit-backdrop-filter: var(--apple-glass-blur);
        border-radius: var(--apple-radius-md);
        border: 1px solid rgba(255,255,255,0.18);
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: var(--apple-shadow-soft);
        transition: var(--apple-transition);
    }
    .module-card-premium:hover {
        transform: translateY(-2px);
        box-shadow: var(--apple-shadow-hover);
        border-color: rgba(177,18,38,0.20);
    }
    .module-topline { display:flex; justify-content:space-between; align-items:flex-start; gap:12px; }
    .module-name { color: var(--apple-ink); font-weight:700; margin:0; font-size:1.01rem; letter-spacing:-0.015em; }
    .module-sub { color: var(--apple-gray-500); margin:8px 0 16px 0; font-size:0.86rem; line-height:1.7; }
    .module-meter { height:6px; background: var(--apple-gray-200); border-radius:999px; overflow:hidden; }
    .module-meter > span {
        display:block;
        height:100%;
        background: var(--apple-crimson);
        border-radius:inherit;
        transition: width 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }

    /* ── Pills / Chips ── */
    .pill {
        font-size: 0.64rem;
        border-radius: 99px;
        padding: 4px 12px;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        display: inline-block;
    }
    .pill.pending { background: var(--apple-gray-200); color: var(--apple-gray-600); }
    .pill.live { background: var(--apple-crimson-soft); color: var(--apple-crimson); }
    .pill.done { background: rgba(52,199,89,0.10); color: #248A3D; }

    .elite-chip {
        display: inline-block;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.10);
        color: var(--apple-gray-400);
        border-radius: 999px;
        padding: 5px 12px;
        font-size: 0.64rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        font-weight: 600;
        margin-right: 6px;
    }

    .sidebar-mini {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: var(--apple-radius-sm);
        padding: 12px 14px;
        margin-top: 16px;
    }

    /* ── Progress Bars ── */
    .stProgress > div > div { background-color: var(--apple-crimson) !important; }

    /* ── Primary Buttons — Crimson Accent ── */
    .stButton > button[kind="primary"],
    .stButton > button[kind="primary"][data-testid],
    [data-testid="stBaseButton-primary"] {
        background: var(--apple-crimson) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--apple-radius-sm) !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        letter-spacing: -0.01em !important;
        transition: var(--apple-transition) !important;
        box-shadow: 0 4px 16px rgba(177,18,38,0.20) !important;
    }
    .stButton > button[kind="primary"]:hover,
    [data-testid="stBaseButton-primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(177,18,38,0.30) !important;
        filter: brightness(1.08) !important;
    }
    .stButton > button:focus-visible {
        outline: 2px solid var(--apple-crimson) !important;
        outline-offset: 2px !important;
    }

    /* ── Secondary Buttons — Quiet Glass ── */
    .stButton > button[kind="secondary"],
    [data-testid="stBaseButton-secondary"] {
        background: var(--apple-glass-bg) !important;
        backdrop-filter: var(--apple-glass-blur) !important;
        border: 1px solid var(--apple-gray-300) !important;
        color: var(--apple-ink) !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        padding: 8px 20px !important;
        box-shadow: var(--apple-shadow-soft) !important;
        letter-spacing: -0.01em !important;
        border-radius: var(--apple-radius-sm) !important;
        transition: var(--apple-transition) !important;
    }
    .stButton > button[kind="secondary"]:hover,
    [data-testid="stBaseButton-secondary"]:hover {
        border-color: var(--apple-crimson) !important;
        box-shadow: var(--apple-shadow-hover) !important;
        transform: translateY(-2px) !important;
        color: var(--apple-crimson) !important;
    }

    /* ── Badges ── */
    .badge {
        display: inline-block;
        background: var(--apple-crimson);
        color: white;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 99px;
        margin-left: 8px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .badge.done { background: #34C759; }

    /* ── Welcome Banner ── */
    .welcome-banner {
        background: var(--apple-ink);
        border-radius: var(--apple-radius-lg);
        padding: 40px;
        margin-bottom: 32px;
        border-left: none;
    }
    .welcome-banner h1 {
        color: var(--apple-gray-100) !important;
        font-family: 'Inter', -apple-system, 'SF Pro Display', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.035em;
        margin-bottom: 8px;
    }
    .welcome-banner p { color: var(--apple-gray-400); font-size: 1.05rem; line-height: 1.7; }

    /* ── Callout ── */
    .callout {
        background: var(--apple-crimson-soft);
        border-left: 3px solid var(--apple-crimson);
        border-radius: 0 var(--apple-radius-xs) var(--apple-radius-xs) 0;
        padding: 16px 20px;
        margin: 16px 0;
        color: #6B0E16;
    }

    /* ── Dividers ── */
    hr { border: none; border-top: 1px solid var(--apple-gray-200); margin: 32px 0; }

    /* ── Resource Library ── */
    .resource-card {
        background: var(--apple-glass-bg);
        backdrop-filter: var(--apple-glass-blur);
        -webkit-backdrop-filter: var(--apple-glass-blur);
        border-radius: var(--apple-radius-md);
        padding: 16px 20px;
        margin-bottom: 8px;
        box-shadow: var(--apple-shadow-soft);
        border: 1px solid rgba(255,255,255,0.18);
        transition: var(--apple-transition);
    }
    .resource-card:hover {
        border-color: rgba(177,18,38,0.20);
        box-shadow: var(--apple-shadow-hover);
        transform: translateY(-2px);
    }
    .resource-id {
        display: inline-block;
        background: var(--apple-ink);
        color: white;
        font-size: 0.68rem;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: var(--apple-radius-xs);
        white-space: nowrap;
        margin-top: 3px;
        letter-spacing: 0.02em;
        min-width: 54px;
        text-align: center;
        flex-shrink: 0;
    }

    /* ── Mobile + Dark Mode Compatibility ── */
    @media (max-width: 768px) and (prefers-color-scheme: dark) {
      div[data-testid="stAppViewContainer"],
      section.main,
      .stApp {
        background: var(--apple-ink) !important;
        color: var(--apple-gray-100) !important;
      }
      div[data-testid="stMarkdownContainer"],
      div[data-testid="stMarkdownContainer"] p,
      div[data-testid="stMarkdownContainer"] li,
      div[data-testid="stMarkdownContainer"] span,
      div[data-testid="stMarkdownContainer"] div {
        color: var(--apple-gray-100) !important;
      }
      .page-title, .page-subtitle { color: var(--apple-gray-100) !important; }
      .resource-card, .module-card, .welcome-banner + div,
      div[style*="background:white"], div[style*="background: white"] {
        background: rgba(20,20,22,0.90) !important;
        border-color: rgba(255,255,255,0.08) !important;
      }
      div[style*="color:#0A1628"], div[style*="color: #0A1628"],
      span[style*="color:#0A1628"], span[style*="color: #0A1628"] { color: var(--apple-gray-100) !important; }
      div[style*="color:#5A6E8A"], div[style*="color: #5A6E8A"],
      span[style*="color:#5A6E8A"], span[style*="color: #5A6E8A"] { color: var(--apple-gray-300) !important; }
      div[data-testid="stTextInput"] input {
        background: rgba(20,20,22,0.90) !important;
        color: var(--apple-gray-100) !important;
        border-color: rgba(255,255,255,0.12) !important;
      }
      div[data-testid="stTextInput"] input::placeholder { color: rgba(255,255,255,0.40) !important; }
      table, td, th { color: var(--apple-gray-200) !important; border-color: rgba(255,255,255,0.08) !important; }
    }

    /* ── Sidebar Buttons ── */
    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        border-radius: var(--apple-radius-sm) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        background: rgba(255,255,255,0.06) !important;
        color: var(--apple-gray-100) !important;
        text-align: center !important;
        font-size: 0.84rem !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
        transition: var(--apple-transition) !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        transform: translateY(-2px) !important;
        background: rgba(255,255,255,0.10) !important;
    }
    [data-testid="stSidebar"] .stButton > button[kind="primary"],
    [data-testid="stSidebar"] [data-testid="stBaseButton-primary"] {
        background: rgba(177,18,38,0.25) !important;
        border-color: rgba(177,18,38,0.35) !important;
        color: #FFFFFF !important;
    }

    /* ── Content Sections — Glassmorphism Cards ── */
    .content-section {
        background: var(--apple-glass-bg);
        backdrop-filter: var(--apple-glass-blur);
        -webkit-backdrop-filter: var(--apple-glass-blur);
        border-radius: var(--apple-radius-md);
        padding: 32px;
        margin: 24px 0;
        box-shadow: var(--apple-shadow-soft);
        border: 1px solid rgba(255,255,255,0.18);
        border-top: none;
    }
    .content-section h2 {
        font-family: 'Inter', -apple-system, 'SF Pro Display', sans-serif;
        color: var(--apple-ink) !important;
        font-size: 1.6rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin: 0 0 16px 0;
        border-bottom: 1px solid var(--apple-gray-200);
        padding-bottom: 12px;
    }
    .content-section h3 {
        color: var(--apple-crimson) !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 0.76rem;
        font-weight: 700;
        margin: 24px 0 8px 0;
        font-family: 'Inter', -apple-system, 'SF Pro Display', sans-serif !important;
    }
    .content-section p {
        color: var(--apple-gray-600);
        line-height: 1.7;
    }
    .content-section li {
        color: var(--apple-gray-600);
        line-height: 1.7;
    }

    /* ── Info Boxes — Refined Callouts ── */
    .info-box {
        background: var(--apple-crimson-soft);
        border-left: 3px solid var(--apple-crimson);
        border-radius: 0 var(--apple-radius-xs) var(--apple-radius-xs) 0;
        padding: 16px 20px;
        margin: 20px 0;
        color: var(--apple-ink) !important;
        font-size: 0.9rem;
        line-height: 1.7;
    }
    .info-box.green { background: rgba(52,199,89,0.08); border-left-color: #34C759; }
    .info-box.yellow { background: rgba(255,159,10,0.08); border-left-color: #FF9F0A; }

    /* ── Tables — Clean Apple Style ── */
    .styled-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 0.88rem;
        margin: 16px 0;
        border-radius: var(--apple-radius-sm);
        overflow: hidden;
        box-shadow: var(--apple-shadow-soft);
        border: 1px solid var(--apple-gray-200);
    }
    .styled-table th {
        background: var(--apple-ink);
        color: var(--apple-gray-100);
        padding: 12px 16px;
        text-align: left;
        font-weight: 600;
        font-size: 0.78rem;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }
    .styled-table td {
        padding: 12px 16px;
        border-bottom: 1px solid var(--apple-gray-200);
        color: var(--apple-gray-600);
        background: var(--apple-white);
        line-height: 1.6;
    }
    .styled-table tr:nth-child(even) td { background: var(--apple-surface); }
    .styled-table tr:last-child td { border-bottom: none; }

    /* ── Premium Login — Hero Card ── */
    .lp-info-card {
        background: var(--apple-ink);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: var(--apple-radius-lg);
        padding: 48px 40px;
        box-shadow: var(--apple-shadow-deep);
        min-height: 460px;
        position: relative;
        overflow: hidden;
    }
    .lp-info-card::before {
        content: "";
        position: absolute;
        top: -100px; right: -80px;
        width: 320px; height: 320px;
        background: radial-gradient(circle, rgba(177,18,38,0.20) 0%, transparent 70%);
        pointer-events: none;
    }
    .lp-info-card::after {
        content: "";
        position: absolute;
        bottom: -120px; left: -80px;
        width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(177,18,38,0.08) 0%, transparent 70%);
        pointer-events: none;
    }
    .lp-kicker {
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        color: var(--apple-crimson);
        font-weight: 700;
        margin-bottom: 20px;
        position: relative;
        z-index: 1;
    }
    .lp-headline {
        font-family: 'Inter', -apple-system, 'SF Pro Display', sans-serif !important;
        font-size: 1.9rem !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
        line-height: 1.2 !important;
        letter-spacing: -0.035em !important;
        margin: 0 0 20px 0 !important;
        position: relative;
        z-index: 1;
    }
    .lp-body {
        color: var(--apple-gray-400);
        font-size: 0.92rem;
        line-height: 1.7;
        margin: 0 0 32px 0;
        position: relative;
        z-index: 1;
    }
    .lp-features {
        list-style: none;
        padding: 0;
        margin: 0;
        display: flex;
        flex-direction: column;
        gap: 8px;
        position: relative;
        z-index: 1;
    }
    .lp-features li {
        display: flex;
        align-items: center;
        gap: 12px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: var(--apple-radius-sm);
        padding: 12px 16px;
        color: var(--apple-gray-300);
        font-size: 0.86rem;
        font-weight: 500;
        transition: var(--apple-transition);
    }
    .lp-features li:hover {
        background: rgba(255,255,255,0.06);
        transform: translateX(4px);
    }
    .lp-divider {
        width: 40px;
        height: 3px;
        background: var(--apple-crimson);
        border-radius: 2px;
        margin: 0 0 24px 0;
        position: relative;
        z-index: 1;
    }

    /* ── Form Submit Button ── */
    div[data-testid="stFormSubmitButton"] button {
        background: var(--apple-crimson) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: var(--apple-radius-sm) !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
        font-size: 0.88rem !important;
        box-shadow: 0 4px 16px rgba(177,18,38,0.20) !important;
        transition: var(--apple-transition) !important;
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(177,18,38,0.30) !important;
        filter: brightness(1.08) !important;
    }

    /* ── Streamlit Tabs — Apple Style ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: var(--apple-gray-200);
        border-radius: var(--apple-radius-sm);
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: var(--apple-radius-xs) !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
        color: var(--apple-gray-500) !important;
        padding: 8px 16px !important;
        transition: var(--apple-transition) !important;
    }
    .stTabs [data-baseweb="tab"]:hover { color: var(--apple-ink) !important; }
    .stTabs [aria-selected="true"] {
        background: var(--apple-white) !important;
        color: var(--apple-ink) !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none !important; }
    .stTabs [data-baseweb="tab-border"] { display: none !important; }

    /* ── Streamlit Checkboxes ── */
    .stCheckbox label { font-size: 0.88rem !important; color: var(--apple-gray-600) !important; }

    /* ── Form Inputs ── */
    .stTextInput input, .stSelectbox select {
        border-radius: var(--apple-radius-sm) !important;
        border: 1.5px solid var(--apple-gray-200) !important;
        font-size: 0.92rem !important;
        padding: 10px 14px !important;
        transition: var(--apple-transition) !important;
    }
    .stTextInput input:focus, .stSelectbox select:focus {
        border-color: var(--apple-crimson) !important;
        box-shadow: 0 0 0 3px rgba(177,18,38,0.08) !important;
    }

</style>
""")

# ─────────────────────────────────────────────
#  GOOGLE SHEETS INTEGRATION
# ─────────────────────────────────────────────
@st.cache_resource
def get_gsheet_client():

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
        sheet = client.open("AAP New Hire Orientation Progress").sheet1
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

# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────
def pct_bar(pct):
    return dedent(f"""
    <div class="progress-container">
        <div class="progress-fill" style="width:{pct}%"></div>
    </div>
    <small style="color:rgba(255,255,255,0.36); font-size:0.72rem;">{pct}% complete</small>
    """).strip()


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

        /* Page background for login — Midnight */
        .stApp { background: #0A0A0B !important; }
        /* Style the form container as a frosted glass sign-in card */
        [data-testid="stForm"] {
            background: rgba(255,255,255,0.96);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 24px;
            padding: 40px 36px 32px !important;
            box-shadow: 0 32px 64px rgba(0,0,0,0.12);
            border: 1px solid rgba(255,255,255,0.18);
        }
        /* Input label styling */
        [data-testid="stForm"] label p {
            font-size: 0.72rem !important;
            font-weight: 600 !important;
            color: #86868B !important;
            text-transform: uppercase !important;
            letter-spacing: 0.10em !important;
        }
        /* Input field styling */
        [data-testid="stForm"] input {
            border: 1.5px solid #E8E8ED !important;
            border-radius: 12px !important;
            font-size: 0.92rem !important;
            background: #F5F5F7 !important;
            color: #0A0A0B !important;
            padding: 10px 14px !important;
            transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
        }
        [data-testid="stForm"] input:focus {
            border-color: #B11226 !important;
            box-shadow: 0 0 0 3px rgba(177,18,38,0.08) !important;
            background: #FFFFFF !important;
        }
        /* Radio label styling */
        [data-testid="stForm"] .stRadio label {
            color: #424245 !important;
            font-size: 0.88rem !important;
        }
>>>>>>> 527c6a4dfbae1df9f2c82ca8f7a67b16d4a7a281
    </style>
    """, unsafe_allow_html=True)

inject_css()
    render_html("<div style='padding-top:48px'></div>")


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

    outer_l, outer_m, outer_r = st.columns([0.5, 2, 0.5])
    with outer_m:
        # Logo
        render_html(f"""
        <div style="text-align:center; margin-bottom:40px;">
            <img src="{_login_logo_src}" alt="AAP / API Logo"
                 style="height:80px; max-width:280px; object-fit:contain;
                        filter: brightness(1.1);">
        </div>
        """)

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

        with panel_l:
            render_html("""
            <div class="lp-info-card">
                <div class="lp-kicker">New Hire Orientation</div>
                <h2 class="lp-headline">Welcome to your<br>orientation hub.</h2>
                <div class="lp-divider"></div>
                <p class="lp-body">
                    Begin your journey with a secure, guided onboarding experience.
                    Sign in to access your personalized modules and track your progress in real time.
                </p>
                <ul class="lp-features">
                    <li><span style="font-size:1rem;">&#9679;</span> Secure employee credential verification</li>
                    <li><span style="font-size:1rem;">&#9679;</span> Role-based learning path assignment</li>
                    <li><span style="font-size:1rem;">&#9679;</span> Live progress sync and tracking</li>
                </ul>
            </div>
            """)

        with panel_r:
            with st.form("login_form", clear_on_submit=False):
                render_html("""
                <p style="font-size:1.2rem; font-weight:800; color:#0A0A0B; margin:0 0 4px 0; letter-spacing:-0.025em;">
                    Employee Sign In
                </p>
                <p style="color:#86868B; font-size:0.86rem; margin:0 0 24px 0; line-height:1.7;">
                    Use the details provided by HR to continue.
                </p>
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
                render_html("<div style='margin-top:6px;'></div>")
                submitted = st.form_submit_button("Sign In  →", use_container_width=True)

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

                            st.rerun()
                        else:
                            st.error("Invalid credentials. Please check your access code, employee number, and name.")


        st.markdown("---")
        st.markdown('<p style="text-align:center;color:#94a3b8;font-size:0.82rem;">If you need login assistance, contact HR:<br><strong>Nicole Thornton</strong> · 256-574-7528 · nicole.thornton@apirx.com</p>', unsafe_allow_html=True)

        # Footer
        render_html("""
        <div style="text-align:center; margin-top:32px; padding-top:20px;
                    border-top:1px solid rgba(255,255,255,0.06);">
            <p style="color:#86868B; font-size:0.78rem; margin:0; line-height:2; letter-spacing:0.01em;">
                Need help? Contact HR &nbsp;·&nbsp;
                <strong style="color:#D2D2D7;">Nicole Thornton</strong>
                &nbsp;·&nbsp; nicole.thornton@apirx.com &nbsp;·&nbsp; 256-574-7528
            </p>
        </div>
        """)



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
        # ── White card: logo + label + username ──
        logo_src = _logo_img_src()
        render_html(f"""
        <div class="sidebar-header">
            <img src="{logo_src}"
                 style="max-height:48px; width:100%; object-fit:contain; margin-bottom:12px; opacity:0.9;" />
            <div style="font-size:0.62rem; font-weight:600; letter-spacing:0.14em;
                        color:rgba(255,255,255,0.36); text-transform:uppercase; margin-bottom:6px;">
                    Learning Interface
            </div>
            <div class="sidebar-username" style="font-size:0.93rem;">{st.session_state.username}</div>
        </div>
        """)

        # ── Overall progress ──
        total_pct = int(sum(st.session_state.progress.values()) / max(len(active_modules), 1))
        render_html(f"""
        <div style="font-size:0.66rem; font-weight:600; letter-spacing:0.10em;
                    color:rgba(255,255,255,0.36); text-transform:uppercase; margin: 8px 0 4px 0;">
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

        st.markdown("---")
        render_html("""
        <small style='color:rgba(255,255,255,0.40); line-height:1.7;'>
        <b style="color:rgba(255,255,255,0.56);">HR Contact</b><br>
        Nicole Thornton<br>
        HR Administrator<br>
        256-574-7528<br>
        Nicole.thornton@apirx.com
        </small>
        <div class="sidebar-mini">
            <div style="font-size:0.62rem; letter-spacing:0.12em; text-transform:uppercase; color:rgba(255,255,255,0.28); font-weight:600; margin-bottom:4px;">Experience</div>
            <div style="color:rgba(255,255,255,0.50); font-size:0.8rem; line-height:1.6;">Glassmorphism interface designed for clarity and focus.</div>
        </div>
        """)

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
    module_progress = [st.session_state.progress.get(m["key"], 0) for m in active_modules]
    completed = sum(1 for p in module_progress if p == 100)
    total_pct = int(sum(module_progress) / len(active_modules)) if active_modules else 0
    quizzes_done = sum(1 for m in active_modules if st.session_state.quiz_results.get(m["key"]) is not None)

    st.markdown('<div class="post-auth-shell">', unsafe_allow_html=True)

    render_html(f"""
    <div class="premium-hero">
        <span class="premium-kicker">Orientation</span>
        <h1>{track_label} Learning Center &middot; {name_display}</h1>
        <p>
            Your personalized orientation experience. Navigate modules, track milestones,
            and complete every checkpoint with confidence.
        </p>
        <div style="margin-top:16px; position:relative; z-index:1;">
            <span class="elite-chip">Progress Sync</span>
            <span class="elite-chip">Role-Based Path</span>
            <span class="elite-chip">Verified</span>
        </div>
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

    render_html('<div style="margin-top: 32px;"></div>')

    c1, c2, c3 = st.columns(3)
    with c1:
        render_html(f"""
        <div class="premium-stat">
            <div class="premium-stat-label">Milestones Closed</div>
            <div class="premium-stat-value">{completed}/{len(active_modules)}</div>
            <div class="premium-stat-sub">Completed training modules in your path</div>
        </div>
        <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width:{pct}%;"></div>
        </div>
        <div style="color:#64748b;font-size:0.82rem;margin-top:6px;">{done} of {total} items completed</div>

        """)
    with c3:
        render_html(f"""
        <div class="premium-stat">
            <div class="premium-stat-label">Assessments Submitted</div>
            <div class="premium-stat-value">{quizzes_done}/{len(active_modules)}</div>
            <div class="premium-stat-sub">Knowledge verifications completed</div>
        </div>
        """)

    render_html("""
    <div style="margin:24px 0 12px 0; display:flex; justify-content:space-between; align-items:center; gap:10px;">
        <div style="font-size:0.70rem; letter-spacing:0.10em; text-transform:uppercase; color:#86868B; font-weight:600;">Training Modules</div>
        <div style="font-size:0.78rem; color:#86868B;">Select a module to continue.</div>
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

            <p class="module-sub">{m['subtitle']}</p>
            <div class="module-meter"><span style="width:{pct}%"></span></div>
            <div style="margin-top:10px; color:#86868B; font-size:0.78rem; display:flex; justify-content:space-between;">
                <span>Progress</span><strong style="color:#0A0A0B;">{pct}%</strong>
            </div>
        </div>
        """)

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
        <h2>Welcome to AAP</h2>
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
