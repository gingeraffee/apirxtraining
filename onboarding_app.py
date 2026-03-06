import streamlit as st
import json, os, base64, gspread

st.set_page_config(page_title="AAP Onboarding", page_icon="💊", layout="wide", initial_sidebar_state="expanded")

# ━━━ CONSTANTS ━━━
MK = ["welcome","conduct","attendance","workplace","benefits","firststeps"]
MNAME = {"welcome":"Welcome to AAP","conduct":"Code of Conduct & Ethics","attendance":"Attendance & PTO Policies","workplace":"Workplace Policies","benefits":"Benefits Overview","firststeps":"First Steps"}
MNUM = {"welcome":"01","conduct":"02","attendance":"03","workplace":"04","benefits":"05","firststeps":"06"}
MDESC = {"welcome":"Company history, mission, vision & guiding principles","conduct":"Ethics, confidentiality & professional conduct standards","attendance":"PTO accruals, point system, holidays & leave policies","workplace":"Safety, dress code, technology, harassment & conduct","benefits":"Medical, dental, vision, 401(k) & supplemental coverage","firststeps":"System access, onboarding checklist & 90-day roadmap"}
MCLCT = {"welcome":4,"conduct":4,"attendance":5,"workplace":5,"benefits":5,"firststeps":6}

for _k,_v in {"logged_in":False,"emp_name":"","emp_number":"","emp_department":"","emp_position":"","emp_start_date":"","emp_track":"general","current_page":"home","current_module":None}.items():
    if _k not in st.session_state: st.session_state[_k]=_v
for _m in MK:
    if f"quiz_{_m}_passed" not in st.session_state: st.session_state[f"quiz_{_m}_passed"]=False
    if f"checklist_{_m}" not in st.session_state: st.session_state[f"checklist_{_m}"]={}

def _logo():
    p=os.path.join(os.path.dirname(os.path.abspath(__file__)),"AAP_API.PNG")
    if os.path.exists(p):
        with open(p,"rb") as f: return base64.b64encode(f.read()).decode()
    return None
def H(t): st.markdown(t,unsafe_allow_html=True)
def prog():
    d=t=0
    for m in MK:
        t+=1; d+=(1 if st.session_state.get(f"quiz_{m}_passed") else 0)
        ct=MCLCT[m]; t+=ct; d+=sum(1 for v in st.session_state.get(f"checklist_{m}",{}).values() if v)
    return d,t
def isdone(m):
    return st.session_state.get(f"quiz_{m}_passed",False) and sum(1 for v in st.session_state.get(f"checklist_{m}",{}).values() if v)>=MCLCT[m]

# ━━━ AUTH ━━━
def get_gsheet_client():
    try:
        return gspread.service_account_from_dict(dict(st.secrets["gcp_service_account"]),scopes=["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"])
    except: return None

def validate_login(ac,eid,fn):
    try: cc=st.secrets["orientation_access_code"]
    except: st.error("Access code not configured."); return False
    if ac.strip()!=cc.strip(): st.error("Incorrect access code."); return False
    cl=get_gsheet_client()
    if not cl: st.error("Cannot connect to Google Sheets."); return False
    try: es=cl.open("AAP New Hire Orientation Progress").worksheet("Employee Roster")
    except: st.error("Cannot open Employee Roster tab."); return False
    try:
        for r in es.get_all_records():
            if str(r.get("Employee ID","")).strip().lower()==eid.strip().lower():
                if str(r.get("Full Name","")).strip().lower()==fn.strip().lower():
                    st.session_state["emp_track"]="warehouse" if str(r.get("Track","")).strip().lower()=="warehouse" else "general"
                    st.session_state["emp_department"]=str(r.get("Department",""))
                    st.session_state["emp_position"]=str(r.get("Position",""))
                    st.session_state["emp_start_date"]=str(r.get("Start Date",""))
                    return True
                else: st.error("Name does not match."); return False
        st.error("Employee ID not found."); return False
    except Exception as e: st.error(f"Error: {e}"); return False


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  DESIGN SYSTEM
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def inject_css():
    H("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800&display=swap');

    :root {
        --bg: #F4F4F8;
        --card: #FFFFFF;
        --ink: #111118;
        --ink-secondary: #3C3C50;
        --ink-muted: #6E6E85;
        --ink-faint: #9D9DB5;
        --border: rgba(0,0,0,0.06);
        --border-hover: rgba(0,0,0,0.12);
        --accent: #003087;
        --accent-light: #4A7BF7;
        --accent-wash: rgba(0,48,135,0.06);
        --red: #D6293E;
        --red-wash: rgba(214,41,62,0.06);
        --green: #1A9960;
        --green-wash: rgba(26,153,96,0.06);
        --amber: #C27803;
        --amber-wash: rgba(194,120,3,0.06);
        --sidebar-bg: #0C0F1A;
        --sidebar-surface: rgba(255,255,255,0.05);
        --sidebar-border: rgba(255,255,255,0.07);
        --sidebar-text: rgba(255,255,255,0.92);
        --sidebar-muted: rgba(255,255,255,0.50);
        --sidebar-faint: rgba(255,255,255,0.28);
        --r-2xl: 24px; --r-xl: 20px; --r-lg: 16px; --r-md: 12px; --r-sm: 8px; --r-xs: 6px;
        --sh-xs: 0 1px 2px rgba(0,0,0,0.04);
        --sh-sm: 0 2px 8px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.03);
        --sh-md: 0 4px 16px rgba(0,0,0,0.05), 0 2px 4px rgba(0,0,0,0.03);
        --sh-lg: 0 12px 48px rgba(0,0,0,0.07), 0 4px 12px rgba(0,0,0,0.03);
        --sh-xl: 0 24px 64px rgba(0,0,0,0.08), 0 8px 24px rgba(0,0,0,0.04);
        --ease: all .2s cubic-bezier(.4,0,.2,1);
        --ease-spring: all .35s cubic-bezier(.34,1.56,.64,1);
    }

    html,body,[class*="css"]{
        font-family:'Plus Jakarta Sans',-apple-system,BlinkMacSystemFont,sans-serif!important;
        -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;
    }
    .stApp{background:var(--bg)!important}
    h1{font-weight:800!important;color:var(--ink)!important;letter-spacing:-.035em;line-height:1.08}
    h2{font-weight:700!important;color:var(--ink)!important;letter-spacing:-.025em;line-height:1.15}
    h3{font-weight:700!important;color:var(--ink-secondary)!important;letter-spacing:-.015em}
    p,li{color:var(--ink-muted);line-height:1.8;font-size:.94rem}
    strong{color:var(--ink-secondary)}
    hr{border:none;border-top:1px solid var(--border);margin:40px 0}
    [data-testid="stHeader"]{background:transparent!important}
    #MainMenu,footer{visibility:hidden}

    /* ━━ SIDEBAR ━━ */
    [data-testid="stSidebar"]{
        background:var(--sidebar-bg)!important;
        border-right:1px solid rgba(255,255,255,0.04)!important;
    }
    [data-testid="stSidebar"] .block-container{padding:1.5rem 1.25rem!important}
    [data-testid="stSidebar"] .stButton>button{
        width:100%!important;border-radius:var(--r-md)!important;
        border:1px solid var(--sidebar-border)!important;
        background:var(--sidebar-surface)!important;
        color:var(--sidebar-text)!important;
        font-size:.85rem!important;font-weight:600!important;
        padding:11px 16px!important;text-align:left!important;
        transition:var(--ease)!important;
        letter-spacing:-.01em!important;
    }
    [data-testid="stSidebar"] .stButton>button:hover{
        background:rgba(255,255,255,0.09)!important;
        border-color:rgba(255,255,255,0.12)!important;
        transform:translateX(3px)!important;
    }
    [data-testid="stSidebar"] [data-testid="stBaseButton-primary"]{
        background:var(--red)!important;border:none!important;color:#fff!important;
        box-shadow:0 4px 20px rgba(214,41,62,0.30)!important;
    }
    .sb-logo{text-align:center;padding:4px 0 24px;border-bottom:1px solid var(--sidebar-border);margin-bottom:24px}
    .sb-card{background:var(--sidebar-surface);border:1px solid var(--sidebar-border);border-radius:var(--r-md);padding:14px 16px;margin-bottom:10px}
    .sb-lbl{font-size:.60rem;font-weight:700;text-transform:uppercase;letter-spacing:.18em;color:var(--sidebar-faint);margin-bottom:4px}
    .sb-val{font-size:.92rem;font-weight:700;color:var(--sidebar-text);letter-spacing:-.01em}
    .sb-section{font-size:.60rem;font-weight:700;text-transform:uppercase;letter-spacing:.18em;color:var(--sidebar-faint);margin:24px 0 12px 2px}
    .sb-pbar{height:4px;background:rgba(255,255,255,0.06);border-radius:99px;overflow:hidden;margin-top:8px}
    .sb-pfill{height:100%;border-radius:99px;background:linear-gradient(90deg,#4A7BF7,#7C9EFF);transition:width .6s ease}
    .sb-contact{background:var(--sidebar-surface);border:1px solid var(--sidebar-border);border-radius:var(--r-md);padding:16px;margin-top:8px}
    .sb-contact *{font-size:.78rem!important;line-height:1.8!important;color:var(--sidebar-muted)!important}
    .sb-contact strong{color:var(--sidebar-text)!important}

    /* ━━ HERO ━━ */
    .hero{
        background:linear-gradient(160deg,#0C0F1A 0%,#111840 35%,#1A2B6B 70%,#2545A8 100%);
        border-radius:var(--r-2xl);padding:52px 56px;position:relative;overflow:hidden;
        margin-bottom:36px;box-shadow:var(--sh-xl);
    }
    .hero::before{content:"";position:absolute;inset:0;
        background:radial-gradient(ellipse 70% 60% at 85% 20%,rgba(74,123,247,0.18),transparent),
                   radial-gradient(ellipse 50% 50% at 10% 80%,rgba(214,41,62,0.08),transparent);pointer-events:none}
    .hero *{position:relative;z-index:1}
    .hero-chip{display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.10);
        color:rgba(255,255,255,0.75);font-size:.68rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
        padding:6px 16px;border-radius:99px;margin-bottom:20px;backdrop-filter:blur(8px)}
    .hero-chip::before{content:"";width:6px;height:6px;border-radius:50%;background:#4A7BF7;box-shadow:0 0 8px rgba(74,123,247,0.50)}
    .hero h1{color:#fff!important;font-size:clamp(1.8rem,4vw,2.6rem)!important;margin:0 0 14px!important}
    .hero p{color:rgba(255,255,255,0.50)!important;font-size:1.05rem;max-width:680px;margin:0!important;line-height:1.75;font-weight:400}

    /* ━━ STAT ROW ━━ */
    .stat{background:var(--card);border:1px solid var(--border);border-radius:var(--r-xl);padding:28px;transition:var(--ease);box-shadow:var(--sh-sm)}
    .stat:hover{box-shadow:var(--sh-md);transform:translateY(-2px)}
    .stat-top{display:flex;align-items:baseline;gap:4px}
    .stat-n{font-size:2.4rem;font-weight:800;color:var(--ink);letter-spacing:-.04em;line-height:1}
    .stat-unit{font-size:1rem;font-weight:500;color:var(--ink-faint)}
    .stat-l{font-size:.66rem;font-weight:700;color:var(--ink-faint);text-transform:uppercase;letter-spacing:.12em;margin-top:10px}
    .stat-bar{height:3px;background:var(--bg);border-radius:99px;margin-top:14px;overflow:hidden}
    .stat-bar-fill{height:100%;border-radius:99px;background:linear-gradient(90deg,var(--accent),var(--accent-light));transition:width .6s ease}

    /* ━━ MODULE CARDS ━━ */
    .mc{background:var(--card);border:1px solid var(--border);border-radius:var(--r-xl);overflow:hidden;transition:var(--ease-spring);margin-bottom:18px;box-shadow:var(--sh-xs)}
    .mc:hover{box-shadow:var(--sh-lg);transform:translateY(-4px);border-color:var(--border-hover)}
    .mc-inner{padding:28px 28px 0;display:flex;gap:18px;align-items:start}
    .mc-badge{width:44px;height:44px;border-radius:var(--r-md);display:flex;align-items:center;justify-content:center;font-size:.74rem;font-weight:800;letter-spacing:.02em;flex-shrink:0;transition:var(--ease)}
    .mc-badge.todo{background:var(--bg);color:var(--ink-faint);border:1px solid var(--border)}
    .mc-badge.wip{background:var(--amber-wash);color:var(--amber);border:1px solid rgba(194,120,3,0.12)}
    .mc-badge.ok{background:var(--green-wash);color:var(--green);border:1px solid rgba(26,153,96,0.12)}
    .mc-info{flex:1;min-width:0}
    .mc-title{font-weight:700;color:var(--ink);font-size:.98rem;margin:0 0 5px;letter-spacing:-.015em}
    .mc-desc{color:var(--ink-faint);font-size:.84rem;line-height:1.6;margin:0}
    .mc-foot{display:flex;align-items:center;justify-content:space-between;padding:18px 28px;margin-top:20px;border-top:1px solid var(--border)}
    .mc-pill{font-size:.60rem;font-weight:700;letter-spacing:.10em;text-transform:uppercase;padding:5px 14px;border-radius:99px}
    .mc-pill.todo{background:var(--bg);color:var(--ink-faint)}
    .mc-pill.wip{background:var(--amber-wash);color:var(--amber)}
    .mc-pill.ok{background:var(--green-wash);color:var(--green)}
    .mc-arrow{color:var(--ink-faint);font-size:.82rem;transition:var(--ease)}
    .mc:hover .mc-arrow{color:var(--accent);transform:translateX(3px)}

    /* ━━ MODULE PAGE HERO ━━ */
    .mhero{background:linear-gradient(160deg,#0C0F1A,#111840 40%,#1A2B6B);
        border-radius:var(--r-2xl);padding:40px 44px;margin-bottom:32px;position:relative;overflow:hidden;box-shadow:var(--sh-lg)}
    .mhero::after{content:"";position:absolute;inset:0;
        background:radial-gradient(ellipse 60% 50% at 90% 15%,rgba(74,123,247,0.15),transparent);pointer-events:none}
    .mhero *{position:relative;z-index:1}
    .mhero-num{display:inline-block;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.08);color:rgba(255,255,255,0.60);font-size:.62rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase;padding:4px 14px;border-radius:99px;margin-bottom:14px}
    .mhero h2{color:#fff!important;font-size:1.7rem!important;margin:0 0 10px!important}
    .mhero p{color:rgba(255,255,255,0.45);font-size:.94rem;margin:0;line-height:1.65}

    /* ━━ CONTENT ━━ */
    .info-box{background:var(--accent-wash);border-left:3px solid var(--accent);border-radius:0 var(--r-sm) var(--r-sm) 0;padding:18px 22px;margin:24px 0;font-size:.90rem;line-height:1.8;color:var(--ink-secondary)}
    .info-box.green{background:var(--green-wash);border-left-color:var(--green)}
    .info-box.red{background:var(--red-wash);border-left-color:var(--red)}

    .styled-table{width:100%;border-collapse:separate;border-spacing:0;font-size:.86rem;margin:20px 0;border-radius:var(--r-lg);overflow:hidden;border:1px solid var(--border);box-shadow:var(--sh-xs)}
    .styled-table th{background:var(--ink);color:#fff;padding:13px 18px;text-align:left;font-weight:700;font-size:.70rem;letter-spacing:.08em;text-transform:uppercase}
    .styled-table td{padding:13px 18px;border-bottom:1px solid var(--border);color:var(--ink-secondary);background:var(--card)}
    .styled-table tr:nth-child(even) td{background:var(--bg)}
    .styled-table tr:last-child td{border-bottom:none}

    .timeline-item{border-left:2px solid var(--accent-light);padding:0 0 28px 28px;margin-left:8px;position:relative}
    .timeline-item::before{content:'';width:10px;height:10px;background:var(--card);border:2.5px solid var(--accent);border-radius:50%;position:absolute;left:-6px;top:3px}
    .timeline-item:last-child{border-left-color:transparent;padding-bottom:0}
    .tl-title{font-weight:700;color:var(--ink);font-size:.96rem;margin:0 0 8px;letter-spacing:-.01em}
    .tl-body{color:var(--ink-muted);font-size:.88rem;line-height:1.85}
    .tl-body li{margin-bottom:3px}

    .action-card{background:var(--card);border:1px solid var(--border);border-radius:var(--r-lg);padding:18px 22px;margin-bottom:10px;display:flex;align-items:start;gap:16px;transition:var(--ease)}
    .action-card:hover{box-shadow:var(--sh-sm);border-color:var(--border-hover)}
    .action-icon{font-size:1.3rem;flex-shrink:0;margin-top:1px}
    .action-title{font-weight:700;color:var(--ink);font-size:.92rem}
    .action-desc{color:var(--ink-muted);font-size:.86rem;line-height:1.65;margin-top:2px}

    /* ━━ QUIZ ━━ */
    .quiz-pass{background:var(--green-wash);border:1px solid rgba(26,153,96,0.15);color:var(--green);padding:22px;border-radius:var(--r-lg);text-align:center;font-weight:700;font-size:.95rem}
    .quiz-fail{background:var(--red-wash);border:1px solid rgba(214,41,62,0.12);color:var(--red);padding:22px;border-radius:var(--r-lg);text-align:center;font-weight:700;font-size:.95rem}

    /* ━━ BUTTONS ━━ */
    [data-testid="stBaseButton-primary"]{background:var(--accent)!important;color:#fff!important;border:none!important;border-radius:var(--r-md)!important;font-weight:700!important;font-size:.86rem!important;letter-spacing:-.01em!important;box-shadow:0 2px 12px rgba(0,48,135,0.20)!important;transition:var(--ease)!important}
    [data-testid="stBaseButton-primary"]:hover{box-shadow:0 6px 24px rgba(0,48,135,0.30)!important;transform:translateY(-1px)!important}
    [data-testid="stBaseButton-secondary"]{border-radius:var(--r-md)!important;font-weight:600!important;border-color:var(--border)!important;color:var(--ink-secondary)!important;transition:var(--ease)!important}
    [data-testid="stBaseButton-secondary"]:hover{border-color:var(--accent)!important;color:var(--accent)!important}
    div[data-testid="stFormSubmitButton"] button{background:var(--accent)!important;color:#fff!important;border:none!important;border-radius:var(--r-md)!important;font-weight:700!important;font-size:.90rem!important;padding:14px 28px!important;box-shadow:0 4px 20px rgba(0,48,135,0.20)!important;letter-spacing:-.005em!important;transition:var(--ease)!important}
    div[data-testid="stFormSubmitButton"] button:hover{box-shadow:0 8px 32px rgba(0,48,135,0.28)!important;transform:translateY(-2px)!important}

    /* ━━ TABS ━━ */
    .stTabs [data-baseweb="tab-list"]{gap:4px;background:var(--bg);border-radius:var(--r-md);padding:4px;border:1px solid var(--border)}
    .stTabs [data-baseweb="tab"]{border-radius:var(--r-sm)!important;font-weight:600!important;font-size:.82rem!important;color:var(--ink-faint)!important;padding:9px 18px!important;transition:var(--ease)!important}
    .stTabs [data-baseweb="tab"]:hover{color:var(--ink-secondary)!important}
    .stTabs [aria-selected="true"]{background:var(--card)!important;color:var(--ink)!important;box-shadow:var(--sh-xs)!important;font-weight:700!important}
    .stTabs [data-baseweb="tab-highlight"],.stTabs [data-baseweb="tab-border"]{display:none!important}

    /* ━━ INPUTS ━━ */
    .stTextInput label p{font-size:.72rem!important;font-weight:700!important;color:var(--ink-faint)!important;text-transform:uppercase!important;letter-spacing:.12em!important}
    .stTextInput input{border-radius:var(--r-md)!important;border:1.5px solid var(--border)!important;font-size:.94rem!important;padding:13px 18px!important;background:var(--card)!important;transition:var(--ease)!important;color:var(--ink)!important}
    .stTextInput input:focus{border-color:var(--accent)!important;box-shadow:0 0 0 4px rgba(0,48,135,0.06)!important}
    .stTextInput input::placeholder{color:var(--ink-faint)!important}
    [data-testid="stForm"]{background:var(--card);border-radius:var(--r-2xl);padding:44px 40px 36px!important;box-shadow:var(--sh-xl);border:1px solid var(--border)}

    /* ━━ CHECKBOX ━━ */
    .stCheckbox label span{font-size:.90rem!important;color:var(--ink-muted)!important}

    /* ━━ VALUE CARDS ━━ */
    .val-card{background:var(--card);border:1px solid var(--border);border-radius:var(--r-lg);padding:22px 24px;transition:var(--ease);margin-bottom:12px}
    .val-card:hover{box-shadow:var(--sh-sm)}
    .val-title{font-weight:700;color:var(--ink);font-size:.94rem;margin-bottom:6px}
    .val-desc{color:var(--ink-muted);font-size:.86rem;line-height:1.65}
    </style>""")

inject_css()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  LOGIN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def show_login():
    H("<style>.stApp{background:linear-gradient(160deg,#0C0F1A 0%,#111840 40%,#1A2B6B 100%)!important}</style>")
    st.markdown("")
    _,c,_=st.columns([1,1.5,1])
    with c:
        logo=_logo()
        if logo: H(f'<div style="text-align:center;margin:48px 0 36px"><img src="data:image/png;base64,{logo}" style="height:68px;filter:brightness(1.2) drop-shadow(0 2px 16px rgba(0,0,0,0.30))"></div>')
        with st.form("login_form"):
            H('<p style="font-size:1.4rem;font-weight:800;color:var(--ink);margin:0 0 4px;letter-spacing:-.03em">Sign in to Onboarding</p>')
            H('<p style="color:var(--ink-faint);font-size:.88rem;margin:0 0 28px">Enter the credentials provided by Human Resources.</p>')
            ac=st.text_input("Access Code",placeholder="Enter access code",type="password")
            eid=st.text_input("Employee ID",placeholder="e.g. 10042")
            fn=st.text_input("Full Name",placeholder="As shown in your HR paperwork")
            H("<div style='height:10px'></div>")
            sub=st.form_submit_button("Continue",use_container_width=True)
            if sub:
                if not ac or not eid or not fn: st.error("All fields are required.")
                else:
                    with st.spinner("Verifying..."):
                        if validate_login(ac,eid,fn):
                            st.session_state["logged_in"]=True; st.session_state["emp_name"]=fn.strip().title(); st.session_state["emp_number"]=eid.strip(); st.rerun()
        H('<div style="text-align:center;margin-top:32px"><p style="color:rgba(255,255,255,0.35);font-size:.78rem;line-height:2.2">Need help? &nbsp;<span style="color:rgba(255,255,255,0.60)">Nicole Thornton</span>&nbsp; · &nbsp;nicole.thornton@apirx.com&nbsp; · &nbsp;256-574-7528</p></div>')


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SIDEBAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def show_sidebar():
    with st.sidebar:
        logo=_logo()
        if logo: H(f'<div class="sb-logo"><img src="data:image/png;base64,{logo}" style="height:48px;opacity:.95"></div>')
        d,t=prog(); pct=int((d/t)*100) if t>0 else 0
        H(f'<div class="sb-card"><div class="sb-lbl">Signed In</div><div class="sb-val">{st.session_state["emp_name"]}</div></div>')
        if st.session_state.get("emp_position"):
            H(f'<div class="sb-card"><div class="sb-lbl">Role</div><div class="sb-val">{st.session_state["emp_position"]}</div></div>')
        H(f'<div class="sb-card"><div class="sb-lbl">Progress</div><div class="sb-val">{pct}%</div><div class="sb-pbar"><div class="sb-pfill" style="width:{pct}%"></div></div></div>')
        H('<div class="sb-section">Modules</div>')
        if st.button("🏠  Dashboard",use_container_width=True,key="nav_home"):
            st.session_state["current_page"]="home"; st.session_state["current_module"]=None; st.rerun()
        for m in MK:
            ck=" ✓" if isdone(m) else ""
            if st.button(f"{MNUM[m]}  {MNAME[m]}{ck}",use_container_width=True,key=f"nav_{m}"):
                st.session_state["current_page"]="module"; st.session_state["current_module"]=m; st.rerun()
        H('<div style="height:8px"></div>')
        H('<div class="sb-contact"><strong>HR Support</strong><br>Nicole Thornton · HR Manager<br>256-574-7528<br>nicole.thornton@apirx.com</div>')
        st.markdown("")
        if st.button("Sign Out",use_container_width=True,key="logout"):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  HOME
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def show_home():
    first=st.session_state["emp_name"].split()[0] if st.session_state["emp_name"] else "there"
    d,t=prog(); pct=int((d/t)*100) if t>0 else 0; cdone=sum(1 for m in MK if isdone(m))
    H(f'<div class="hero"><div class="hero-chip">New Hire Onboarding</div><h1>Welcome, {first}</h1><p>Complete each training module to finish your orientation. Your progress saves automatically as you go.</p></div>')
    c1,c2,c3=st.columns(3)
    with c1: H(f'<div class="stat"><div class="stat-top"><span class="stat-n">{pct}</span><span class="stat-unit">%</span></div><div class="stat-l">Overall Progress</div><div class="stat-bar"><div class="stat-bar-fill" style="width:{pct}%"></div></div></div>')
    with c2: H(f'<div class="stat"><div class="stat-top"><span class="stat-n">{cdone}</span><span class="stat-unit">/ {len(MK)}</span></div><div class="stat-l">Modules Complete</div></div>')
    with c3: H(f'<div class="stat"><div class="stat-top"><span class="stat-n">{d}</span><span class="stat-unit">/ {t}</span></div><div class="stat-l">Items Completed</div></div>')
    H("<div style='height:16px'></div>")
    cols=st.columns(2)
    for i,m in enumerate(MK):
        dn=isdone(m); p=st.session_state.get(f"quiz_{m}_passed",False); ch=st.session_state.get(f"checklist_{m}",{}); dc=sum(1 for v in ch.values() if v)
        if dn: cls="ok"; txt="Complete"
        elif p or dc>0: cls="wip"; txt="In Progress"
        else: cls="todo"; txt="Not Started"
        with cols[i%2]:
            H(f'<div class="mc"><div class="mc-inner"><div class="mc-badge {cls}">{MNUM[m]}</div><div class="mc-info"><p class="mc-title">{MNAME[m]}</p><p class="mc-desc">{MDESC[m]}</p></div></div><div class="mc-foot"><span class="mc-pill {cls}">{txt}</span><span class="mc-arrow">→</span></div></div>')
            if st.button("Open Module",key=f"open_{m}",use_container_width=True):
                st.session_state["current_page"]="module"; st.session_state["current_module"]=m; st.rerun()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  QUIZ + CHECKLIST
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_quiz(mk,questions):
    st.markdown("---"); st.markdown("### Module Assessment")
    if st.session_state.get(f"quiz_{mk}_passed"):
        H('<div class="quiz-pass">✓ &nbsp;Assessment complete — all answers correct.</div>'); return
    st.caption("Answer every question correctly to pass. Retake as needed.")
    ans={}
    for i,q in enumerate(questions):
        ans[i]=st.radio(f"**Q{i+1}.** {q['q']}",options=q["options"],index=None,key=f"quiz_{mk}_q{i}")
    if st.button("Submit Answers",key=f"submit_{mk}",type="primary"):
        c=sum(1 for i,q in enumerate(questions) if ans[i]==q["options"][q["answer"]])
        if c==len(questions):
            st.session_state[f"quiz_{mk}_passed"]=True; H('<div class="quiz-pass">✓ &nbsp;All correct!</div>'); st.rerun()
        else: H(f'<div class="quiz-fail">{c} of {len(questions)} correct — review and retry.</div>')

def render_checklist(mk,items):
    st.markdown("---"); st.markdown("### Confirmation Checklist")
    st.caption("Check each item to confirm you understand:")
    ch=st.session_state.get(f"checklist_{mk}",{})
    for i,item in enumerate(items):
        k=f"cl_{mk}_{i}"; ch[k]=st.checkbox(item,value=ch.get(k,False),key=k)
    st.session_state[f"checklist_{mk}"]=ch
    dn=sum(1 for v in ch.values() if v)
    if dn==len(items): st.success(f"All {len(items)} items confirmed.")
    else: st.info(f"{dn} of {len(items)} confirmed.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  MODULES 1–6
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def module_welcome():
    H('<div class="mhero"><span class="mhero-num">Module 01</span><h2>Welcome to AAP</h2><p>Learn about our history, mission, vision, and the values that guide everything we do.</p></div>')
    st.markdown("## Who We Are")
    st.markdown("""American Associated Pharmacies (AAP) is a national cooperative of more than **2,000 independent pharmacies**. Founded in 2009 when **United Drugs** (Phoenix, AZ) and **Associated Pharmacies, Inc. (API)** (Scottsboro, AL) merged to form one of the largest independent pharmacy organizations in America.

Today, AAP operates API with two U.S. warehouse locations, providing member-focused support, innovative programs, and significant cost savings through its Prime Vendor Agreement.""")
    H('<div class="info-box"><strong>Did you know?</strong> AAP saves its member pharmacies millions in operating and acquisition costs every year through its competitive Prime Vendor Agreement.</div>')
    st.markdown("## Our Mission")
    st.markdown("AAP provides support and customized solutions for independent community pharmacies to enhance their profitability, streamline their operations, and improve the quality of patient care.")
    st.markdown("## Our Vision")
    st.markdown("*Helping independent pharmacies thrive in a competitive healthcare market.*")
    st.markdown("## Our Core Values")
    for icon,title,desc in [("🎯","Customer Focus","Our primary focus is meeting and exceeding customer expectations. Customer service is not just a department — it's an attitude."),("⚖️","Integrity","We act with honesty without compromising truth. We build trust through consistency in our words and actions."),("🤝","Respect","We treat others with dignity, recognize the power of teamwork, and encourage open, honest communication."),("⭐","Excellence","We strive for the highest quality in everything we do and pursue continuous improvement and innovation."),("🔑","Ownership","We seek responsibility, hold ourselves accountable, and take ownership when things go wrong.")]:
        H(f'<div class="val-card"><div class="val-title">{icon} &nbsp;{title}</div><div class="val-desc">{desc}</div></div>')
    render_quiz("welcome",[
        {"q":"When was AAP formed?","options":["2001","2005","2009","2012"],"answer":2},
        {"q":"AAP is a cooperative of approximately how many pharmacies?","options":["500","1,000","2,000","5,000"],"answer":2},
        {"q":"Which is NOT one of AAP's five core values?","options":["Customer Focus","Integrity","Profitability","Ownership"],"answer":2},
        {"q":"What is AAP's vision statement?","options":["To be the largest pharmacy chain","Helping independent pharmacies thrive in a competitive healthcare market","Maximizing shareholder value","Providing the lowest drug prices"],"answer":1}])
    render_checklist("welcome",["I understand AAP's history and formation.","I can identify the mission and vision statements.","I know the five core values and what they mean.","I understand that AAP is a cooperative serving independent pharmacies."])

def module_conduct():
    H('<div class="mhero"><span class="mhero-num">Module 02</span><h2>Code of Conduct & Ethics</h2><p>Professional standards, ethical behavior, and workplace expectations.</p></div>')
    st.markdown("## Business Ethics & Conduct")
    st.markdown("The success of AAP depends on our customers' trust. Every employee must act with honesty and integrity, comply with all applicable laws, and refrain from any illegal, dishonest, or unethical conduct. Failure to comply leads to disciplinary action, up to and including termination.")
    st.markdown("## Key Policies")
    tab1,tab2,tab3,tab4=st.tabs(["Conflicts of Interest","Confidentiality","Outside Employment","Equal Opportunity"])
    with tab1: st.markdown("Employees must avoid actual or potential conflicts of interest in all business dealings. Contact HR with any questions.")
    with tab2: st.markdown("All employees sign a **confidentiality and non-disclosure agreement** upon hire. Refusal is grounds for immediate termination. Personnel files are company property with restricted access. Electronic systems may be monitored.")
    with tab3: st.markdown("Outside employment is permitted as long as you satisfactorily perform your AAP responsibilities. If outside work creates a conflict or interferes with performance, you may be asked to choose.")
    with tab4: st.markdown("All employment decisions are based on merit, qualifications, and abilities. AAP does not discriminate on the basis of race, color, religion, sex, national origin, age, disability, or any other protected characteristic. Report concerns without fear of reprisal.")
    st.markdown("## Problem Resolution Process")
    st.markdown("1. Present concerns to your **immediate supervisor** (or HR if inappropriate)\n2. If unresolved, escalate: **VP → President → CEO**\n3. CEO has full authority to resolve\n4. Board of Directors review available as final step\n\nNo employee will be penalized for voicing a complaint in a reasonable, professional manner.")
    render_quiz("conduct",[
        {"q":"What must all employees sign upon hire?","options":["Non-compete agreement","Confidentiality and non-disclosure agreement","Social media policy","Union membership form"],"answer":1},
        {"q":"What system does AAP use to verify work authorization?","options":["HIPAA","E-Verify","ADP Screening","LinkedIn"],"answer":1},
        {"q":"Who should you approach first with a workplace concern?","options":["CEO","A coworker","Your immediate supervisor or HR","An attorney"],"answer":2},
        {"q":"Outside employment is allowed as long as:","options":["You work under 20 hours elsewhere","You satisfactorily perform your AAP responsibilities","Your manager gives verbal approval","It is in a different industry"],"answer":1}])
    render_checklist("conduct",["I understand AAP's ethics expectations and my responsibility.","I understand the confidentiality and NDA requirements.","I know the problem resolution steps for workplace concerns.","I understand the equal employment opportunity policy."])

def module_attendance():
    H('<div class="mhero"><span class="mhero-num">Module 03</span><h2>Attendance & PTO Policies</h2><p>Vacation accruals, personal leave, holidays, and the attendance point system.</p></div>')
    st.markdown("## Vacation Benefits")
    st.caption("Regular full-time employees · 60-day waiting period · Minimum increment: 2 hours")
    H("""<table class="styled-table"><tr><th>Length of Employment</th><th>Paid Days / Year</th><th>Accrual Rate</th></tr>
    <tr><td>60 days – 1st Anniversary</td><td>3 days (24 hrs)</td><td>0.46 hrs/week</td></tr>
    <tr><td>1st – 2nd Anniversary</td><td>5 days (40 hrs)</td><td>0.77 hrs/week</td></tr>
    <tr><td>2nd – 3rd Anniversary</td><td>7 days (56 hrs)</td><td>1.07 hrs/week</td></tr>
    <tr><td>3rd – 5th Anniversary</td><td>10 days (80 hrs)</td><td>1.54 hrs/week</td></tr>
    <tr><td>5th – 9th Anniversary</td><td>15 days (120 hrs)</td><td>2.31 hrs/week</td></tr>
    <tr><td>10th – 19th Anniversary</td><td>17 days (136 hrs)</td><td>2.62 hrs/week</td></tr>
    <tr><td>20th Anniversary+</td><td>19 days (152 hrs)</td><td>2.93 hrs/week</td></tr></table>""")
    H('<div class="info-box"><strong>Key rules:</strong> Vacation cannot be taken before accrual. 5+ consecutive days require President approval. Bank up to 19 days (152 hrs). Accrued vacation is paid out at termination.</div>')
    st.markdown("## Personal Leave")
    st.caption("All employees · Minimum increment: 1 hour · 60-day waiting period")
    st.markdown("""**Full-time employees:** 3 personal days (24 hrs) initially → 4 days after 1 year → 5 days after 5 years.

**Part-time employees:** Earn 1 hour per 30 hours worked, with the same tier caps.

Unused personal leave is **forfeited** at end of benefit year (unless state law requires carryover). Personal leave is **not paid out** at termination.""")
    st.markdown("## Company Holidays")
    c1,c2=st.columns(2)
    with c1:
        for h in ["New Year's Day (Jan 1)","Memorial Day","Independence Day (Jul 4)","Labor Day"]: st.markdown(f"🗓️ &nbsp; {h}")
    with c2:
        for h in ["Thanksgiving","Day after Thanksgiving *or Floating*","Christmas Eve *or Floating*","Christmas Day (Dec 25)"]: st.markdown(f"🗓️ &nbsp; {h}")
    H('<div class="info-box">Saturday holidays are observed on Friday. Sunday holidays are observed on Monday. Employees who work on a holiday receive a floating holiday to use within 90 days.</div>')
    st.markdown("## Attendance Point System")
    st.caption("No-fault basis for non-exempt employees")
    H("""<table class="styled-table"><tr><th>Event</th><th>Points</th></tr>
    <tr><td>Tardy up to 5 minutes (grace period)</td><td>0</td></tr>
    <tr><td>Tardy or early leave (less than 4 hours)</td><td>½</td></tr>
    <tr><td>Full shift absence, tardy or early leave (4+ hours)</td><td>1</td></tr>
    <tr><td>No-call absence (15+ min after start)</td><td>1½</td></tr></table>""")
    st.markdown("### Corrective Action Thresholds")
    H("""<table class="styled-table"><tr><th>Points (rolling 12 months)</th><th>Action Taken</th></tr>
    <tr><td>5 points</td><td>Coaching Session</td></tr><tr><td>6 points</td><td>Verbal Warning</td></tr>
    <tr><td>7 points</td><td>Written Warning</td></tr><tr><td>8 points</td><td>Termination</td></tr></table>""")
    H('<div class="info-box green"><strong>Perfect attendance rewards:</strong> 2 consecutive months of perfect attendance removes 1 point. 3 consecutive months earns a <strong>$75 bonus</strong>.</div>')
    st.warning("Two consecutive days absent without reporting in is considered **voluntary resignation**.")
    render_quiz("attendance",[
        {"q":"What is the minimum increment for vacation time?","options":["1 hour","2 hours","4 hours","8 hours"],"answer":1},
        {"q":"What is the minimum increment for personal leave?","options":["1 hour","2 hours","4 hours","8 hours"],"answer":0},
        {"q":"How many points does a no-call absence carry?","options":["½ point","1 point","1½ points","2 points"],"answer":2},
        {"q":"At how many points does termination occur?","options":["6","7","8","10"],"answer":2},
        {"q":"Consecutive no-call days that equals resignation?","options":["1","2","3","5"],"answer":1}])
    render_checklist("attendance",["I understand the vacation accrual schedule and 2-hour minimum.","I understand personal leave uses 1-hour increments and forfeits at year-end.","I know the 8 company holidays and floating holiday rules.","I understand the attendance point system and corrective action thresholds.","I understand that 2 consecutive no-call days is considered voluntary resignation."])

def module_workplace():
    H('<div class="mhero"><span class="mhero-num">Module 04</span><h2>Workplace Policies</h2><p>Safety, dress code, technology, harassment prevention, and conduct expectations.</p></div>')
    tabs=st.tabs(["Dress Code","Safety","Drug & Alcohol","Computer & Email","Harassment","Other Policies"])
    with tabs[0]:
        st.markdown("### Personal Appearance")
        st.markdown("A neat, clean, and well-groomed appearance is required. Dress varies by department, but universally:\n- All clothing must be work-appropriate — nothing revealing or offensive\n- Avoid offensive stamps or messages on clothing\n- Due to allergies and asthma, avoid strong perfumes and scented products\n\nNon-compliance means being sent home to change (clocked out).")
    with tabs[1]:
        st.markdown("### Workplace Safety")
        st.markdown("- **Immediately report** unsafe conditions to your supervisor\n- **Immediately report** all work-related injuries to HR, no matter how minor\n- All work-related accidents require **immediate drug and alcohol testing**\n- Safety violations may result in disciplinary action up to termination")
    with tabs[2]:
        st.markdown("### Drug & Alcohol Policy")
        st.markdown("AAP maintains a **zero-tolerance** drug and alcohol-free workplace.\n- Being under the influence is strictly prohibited\n- **Random drug testing** may occur at any time\n- Violations may result in **immediate termination**\n- The Employee Assistance Program (EAP) is available")
    with tabs[3]:
        st.markdown("### Computer & Email Usage")
        st.markdown("All computers, files, email, and software are **AAP property** for business use.\n- Usage **may be monitored** at any time\n- Prohibited: sexually explicit content, ethnic slurs, off-color jokes, or anything constituting harassment\n- Illegal duplication of software is prohibited\n- Violations result in discipline up to termination")
    with tabs[4]:
        st.markdown("### Harassment Prevention")
        st.markdown("**Zero tolerance** for discrimination and unlawful harassment.\n\n**If you experience or witness harassment:**\n1. Tell the offender their conduct must stop (if comfortable)\n2. Report to your supervisor or HR\n3. If supervisor is involved, contact the VP of Human Resources\n\n**No retaliation** for good-faith complaints.")
    with tabs[5]:
        st.markdown("### Overtime & Schedules\nAll overtime requires **prior supervisor approval**. Non-exempt employees receive OT pay per law.")
        st.markdown("### Workplace Violence\nZero tolerance. Report all incidents within 24 hours.")
        st.markdown("### Business Travel\nReasonable expenses reimbursed per policy. Falsifying reports is grounds for termination.")
    render_quiz("workplace",[
        {"q":"What happens after a work-related accident?","options":["Nothing unless serious","Incident report only","Immediate drug and alcohol testing","Employee goes home"],"answer":2},
        {"q":"AAP's computer systems are:","options":["Personal property","Company property, may be monitored","Free for personal use","Monitored only in investigations"],"answer":1},
        {"q":"If harassed, what should you do first?","options":["Post online","Ignore it","Tell offender to stop or report to HR","Confront publicly"],"answer":2},
        {"q":"Overtime requires:","options":["Coworker approval","Prior supervisor approval","After-the-fact report","Self-authorization"],"answer":1}])
    render_checklist("workplace",["I understand dress code expectations.","I understand safety reporting requirements.","I understand the drug and alcohol policy.","I understand computer/email monitoring.","I know how to report harassment."])

def module_benefits():
    H('<div class="mhero"><span class="mhero-num">Module 05</span><h2>Benefits Overview</h2><p>Medical, dental, vision, retirement, and supplemental coverage options.</p></div>')
    H('<div class="info-box"><strong>Eligibility:</strong> Full-time (30+ hrs/week) must enroll within 30 days. Benefits effective <strong>1st of month after 60 days</strong>. Dependents to age 26.</div>')
    ft,pt=st.tabs(["Full-Time Benefits","Benefits for All Employees"])
    with ft:
        st.markdown("## Medical Insurance — BCBS Alabama")
        c1,c2=st.columns(2)
        with c1:
            st.markdown("### PPO Plan")
            st.markdown("**Premiums:** Employee $157.20/mo · Family $678.62/mo\n\nDeductible: $500 / $1,000 · Coinsurance: 20%\n\nOut-of-Pocket Max: $2,250 / $4,500\n\nPCP $30 · Specialist $45 · Rx: $10/$30/$50")
        with c2:
            st.markdown("### HDHP with HSA")
            st.markdown("**Premiums:** Employee $136.34/mo · Family $581.72/mo\n\nDeductible: $1,700 / $3,400 · Coinsurance: 10%\n\nOOP Max: $3,400 / $6,800\n\nCompany HSA: $900/$1,800/yr · Limits: $4,400/$8,750")
        st.markdown("## Dental — Guardian")
        st.markdown("**Base:** $6.78/mo · **High:** $10.66/mo · Preventive 100% · Basic 80%/100% · Major 50% (12-mo wait) · Annual Max $1,500/$3,000")
        st.markdown("## Vision — Guardian (Davis Vision)")
        st.markdown("Employee $6.93/mo · Exams/lenses every 12 months · Frames every 24 months · $130 allowance")
        st.markdown("## Life & Disability")
        st.markdown("**Basic Life/AD&D:** Free — annual earnings up to $270K\n\n**STD:** 60% weekly (max $1,250), employee-paid, 7-day elimination\n\n**LTD:** 60% monthly (max $10,000), **company-paid**, 90-day wait")
        st.markdown("## Supplemental — Guardian")
        st.markdown("Accident $14.55/mo · Cancer $21.28/mo · Critical Illness $5K–$20K (age-based)")
        st.markdown("## 401(k) Retirement")
        H('<div class="info-box green"><strong>Company match:</strong> 100% of first 3% + 50% of next 2% = <strong>4% match on 5% contribution</strong>. 100% vested immediately. Eligible after 60 days.</div>')
    with pt:
        st.markdown("## Benefits for All Employees")
        st.caption("Available at no cost regardless of employment status.")
        for icon,title,desc in [("📱","Teladoc — Free Telehealth","24/7 doctor visits from your phone. General medical, mental health, therapy. Call 1-800-835-2362 or teladoc.com."),("🧠","LifeMatters EAP","Free confidential counseling, legal/financial consultation. 1-800-634-6433 or mylifematters.com (password: AAP1)."),("📚","LinkedIn Learning","Full professional development library. Activate at linkedin.com/learning with your company email."),("🎁","BenefitHub Perks","Discounts on travel, electronics, restaurants, entertainment. Register at aapperks.benefithub.com with code 9Y7G26."),("🕐","Personal Time Off","All employees earn personal leave. See Attendance & PTO module for details.")]:
            H(f'<div class="action-card"><span class="action-icon">{icon}</span><div><div class="action-title">{title}</div><div class="action-desc">{desc}</div></div></div>')
    render_quiz("benefits",[
        {"q":"When do full-time benefits become effective?","options":["Day 1","After 30 days","1st of month after 60 days","After 90 days"],"answer":2},
        {"q":"401(k) match if you contribute 5%?","options":["2%","3%","4%","5%"],"answer":2},
        {"q":"Which benefit is free for ALL employees?","options":["Dental","Short-term disability","Teladoc","Vision"],"answer":2},
        {"q":"Basic Life/AD&D is provided at:","options":["50% employer-paid","No cost to employee","Employee-paid","Enrollment required"],"answer":1}])
    render_checklist("benefits",["I understand the two medical plans.","I know the 401(k) match.","I know which benefits are free for everyone.","I know enrollment is within 30 days.","I understand supplemental options."])

def module_firststeps():
    H('<div class="mhero"><span class="mhero-num">Module 06</span><h2>First Steps</h2><p>Your action items, system access setup, and 90-day onboarding roadmap.</p></div>')
    st.markdown("## Immediate Action Items")
    st.caption("Complete these tasks as soon as possible after your start date.")
    for icon,title,desc in [("✅","Verify Account Access","Confirm you can access your AAP email, internal systems, and tools."),("📝","Sign All New Hire Documents","Complete your full onboarding packet in BambooHR — all documents must be signed."),("📚","Activate LinkedIn Learning","Go to **linkedin.com/learning** and log in with your company email."),("📄","Provide I-9 Documents","Bring acceptable ID (passport, or DL + SS card) to HR within **3 business days**."),("💰","Register for Paylocity","Set up your account for pay stubs, tax documents, and payroll."),("📱","Download BambooHR App","Install the mobile app to access your profile, time off, and documents.")]:
        H(f'<div class="action-card"><span class="action-icon">{icon}</span><div><div class="action-title">{title}</div><div class="action-desc">{desc}</div></div></div>')
    st.markdown("---")
    st.markdown("## Your 90-Day Roadmap")
    H("""<div class="timeline-item"><p class="tl-title">Days 1–30 &nbsp;·&nbsp; Orientation & Foundation</p><div class="tl-body"><ul><li>Complete all orientation and training modules</li><li>Sign required paperwork and provide I-9 documentation</li><li>Get access to all systems and tools</li><li>Meet your team and key contacts</li><li>Shadow key processes and learn daily workflows</li><li>Complete the <strong>30-Day Survey</strong></li></ul></div></div>
    <div class="timeline-item"><p class="tl-title">Days 31–60 &nbsp;·&nbsp; Building Independence</p><div class="tl-body"><ul><li>Begin independently executing core responsibilities</li><li>Complete the <strong>60-Day Survey</strong></li><li>Become eligible for <strong>PTO and holiday pay</strong></li><li><strong>End of probationary period</strong></li><li>Set a personal goal for the next 30 days with your supervisor</li></ul></div></div>
    <div class="timeline-item"><p class="tl-title">Days 61–90 &nbsp;·&nbsp; Growth & Review</p><div class="tl-body"><ul><li>Build confidence and consistency in your role</li><li>Identify opportunities for improvement</li><li>Have your <strong>first performance review</strong></li><li><strong>Full benefits eligibility</strong> — coverage begins 1st of month after 60 days</li></ul></div></div>""")
    render_quiz("firststeps",[
        {"q":"I-9 documents must be provided within?","options":["1 day","3 business days","5 days","10 days"],"answer":1},
        {"q":"Probationary period ends at?","options":["30 days","60 days","90 days","120 days"],"answer":1},
        {"q":"PTO eligibility begins after?","options":["Day 1","30 days","60 days","90 days"],"answer":2},
        {"q":"Which app for your employee profile?","options":["Workday","BambooHR","ADP","Gusto"],"answer":1}])
    render_checklist("firststeps",["I will verify access and sign all documents.","I will activate LinkedIn Learning.","I will provide I-9 within 3 business days.","I will register for Paylocity and download BambooHR.","I understand the 90-day timeline.","I know who to contact in HR."])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ROUTER & MAIN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
_FN={"welcome":module_welcome,"conduct":module_conduct,"attendance":module_attendance,"workplace":module_workplace,"benefits":module_benefits,"firststeps":module_firststeps}
def show_module(m):
    if st.button("← Back to Dashboard",key="back"):
        st.session_state["current_page"]="home"; st.session_state["current_module"]=None; st.rerun()
    _FN[m]()
    st.markdown("---")
    ix=MK.index(m); c1,c2=st.columns(2)
    if ix>0:
        with c1:
            if st.button(f"← {MNAME[MK[ix-1]]}",key="prev"): st.session_state["current_module"]=MK[ix-1]; st.rerun()
    if ix<len(MK)-1:
        with c2:
            if st.button(f"{MNAME[MK[ix+1]]} →",key="next"): st.session_state["current_module"]=MK[ix+1]; st.rerun()

def main():
    if not st.session_state["logged_in"]: show_login()
    else:
        show_sidebar()
        if st.session_state["current_page"]=="module" and st.session_state["current_module"]: show_module(st.session_state["current_module"])
        else: show_home()

if __name__=="__main__": main()
