import streamlit as st
import json, os, base64, gspread

st.set_page_config(page_title="AAP Onboarding", page_icon="💊", layout="wide", initial_sidebar_state="expanded")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  CONSTANTS & STATE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MK = ["welcome","conduct","attendance","workplace","benefits","firststeps"]
MNAME = {"welcome":"Welcome to AAP","conduct":"Code of Conduct & Ethics","attendance":"Attendance & PTO Policies","workplace":"Workplace Policies","benefits":"Benefits Overview","firststeps":"First Steps"}
MICON = {"welcome":"01","conduct":"02","attendance":"03","workplace":"04","benefits":"05","firststeps":"06"}
MDESC = {"welcome":"Company history, mission, vision & guiding principles","conduct":"Ethics, confidentiality & professional conduct standards","attendance":"PTO accruals, point system, holidays & leave policies","workplace":"Safety, dress code, technology, harassment & conduct","benefits":"Medical, dental, vision, 401(k) & supplemental coverage","firststeps":"System access, onboarding checklist & 90-day roadmap"}
MCLCOUNT = {"welcome":4,"conduct":4,"attendance":5,"workplace":5,"benefits":5,"firststeps":6}

for _k, _v in {"logged_in":False,"emp_name":"","emp_number":"","emp_department":"","emp_position":"","emp_start_date":"","emp_track":"general","current_page":"home","current_module":None}.items():
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
        ct=MCLCOUNT[m]; t+=ct; d+=sum(1 for v in st.session_state.get(f"checklist_{m}",{}).values() if v)
    return d,t
def done(m):
    p=st.session_state.get(f"quiz_{m}_passed",False)
    c=st.session_state.get(f"checklist_{m}",{})
    return p and sum(1 for v in c.values() if v)>=MCLCOUNT[m]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  AUTH (unchanged logic, same secrets format)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def get_gsheet_client():
    try:
        cd=dict(st.secrets["gcp_service_account"])
        return gspread.service_account_from_dict(cd,scopes=["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"])
    except: return None

def validate_login(ac,eid,fn):
    try: cc=st.secrets["orientation_access_code"]
    except:
        st.error("Access code not configured."); return False
    if ac.strip()!=cc.strip():
        st.error("Incorrect access code."); return False
    cl=get_gsheet_client()
    if not cl:
        st.error("Cannot connect to Google Sheets."); return False
    try: es=cl.open("AAP New Hire Orientation Progress").worksheet("Employee Roster")
    except:
        st.error("Cannot open Employee Roster tab."); return False
    try:
        for r in es.get_all_records():
            if str(r.get("Employee ID","")).strip().lower()==eid.strip().lower():
                if str(r.get("Full Name","")).strip().lower()==fn.strip().lower():
                    st.session_state["emp_track"]="warehouse" if str(r.get("Track","")).strip().lower()=="warehouse" else "general"
                    st.session_state["emp_department"]=str(r.get("Department",""))
                    st.session_state["emp_position"]=str(r.get("Position",""))
                    st.session_state["emp_start_date"]=str(r.get("Start Date",""))
                    return True
                else: st.error("Name does not match our records for this Employee ID."); return False
        st.error("Employee ID not found."); return False
    except Exception as e: st.error(f"Error: {e}"); return False


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  DESIGN SYSTEM — AAP Brand: Navy #003087 / Red #CC1B33
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def inject_css():
    H("""<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800&display=swap');

    :root {
        --navy: #003087;
        --navy-deep: #001E54;
        --navy-light: #0047BA;
        --red: #CC1B33;
        --red-soft: rgba(204,27,51,0.07);
        --red-glow: rgba(204,27,51,0.15);
        --slate-50: #F8FAFC;
        --slate-100: #F1F5F9;
        --slate-200: #E2E8F0;
        --slate-300: #CBD5E1;
        --slate-400: #94A3B8;
        --slate-500: #64748B;
        --slate-600: #475569;
        --slate-700: #334155;
        --slate-800: #1E293B;
        --slate-900: #0F172A;
        --white: #FFFFFF;
        --success: #059669;
        --success-soft: rgba(5,150,105,0.08);
        --warning-soft: rgba(217,119,6,0.08);
        --r-xl: 20px; --r-lg: 16px; --r-md: 12px; --r-sm: 8px;
        --sh-sm: 0 1px 2px rgba(0,0,0,0.05);
        --sh-md: 0 4px 12px rgba(0,0,0,0.06);
        --sh-lg: 0 12px 40px rgba(0,0,0,0.08);
        --sh-xl: 0 20px 60px rgba(0,0,0,0.10);
        --ease: all .25s cubic-bezier(.4,0,.2,1);
    }

    html,body,[class*="css"]{font-family:'DM Sans',-apple-system,BlinkMacSystemFont,sans-serif!important;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
    .stApp{background:var(--slate-50)!important}
    h1{font-weight:800!important;color:var(--slate-900)!important;letter-spacing:-.03em;line-height:1.1}
    h2{font-weight:700!important;color:var(--slate-800)!important;letter-spacing:-.02em;line-height:1.2}
    h3{font-weight:600!important;color:var(--slate-700)!important;letter-spacing:-.01em}
    p,li{color:var(--slate-600);line-height:1.75}
    strong{color:var(--slate-800)}
    hr{border:none;border-top:1px solid var(--slate-200);margin:32px 0}

    /* ── SIDEBAR ── */
    [data-testid="stSidebar"]{
        background:linear-gradient(180deg,var(--navy-deep) 0%,var(--navy) 50%,#003D99 100%)!important;
        border-right:none!important;
        box-shadow:4px 0 24px rgba(0,30,84,0.20);
    }
    [data-testid="stSidebar"] .block-container{padding:1.25rem 1rem!important}
    [data-testid="stSidebar"] .stButton>button{
        width:100%!important;border-radius:var(--r-md)!important;
        border:1px solid rgba(255,255,255,0.08)!important;
        background:rgba(255,255,255,0.04)!important;
        color:rgba(255,255,255,0.80)!important;
        font-size:.84rem!important;font-weight:500!important;
        transition:var(--ease)!important;text-align:left!important;
        padding:10px 14px!important;
    }
    [data-testid="stSidebar"] .stButton>button:hover{
        background:rgba(255,255,255,0.10)!important;
        color:#fff!important;
        border-color:rgba(255,255,255,0.15)!important;
        transform:translateX(3px)!important;
    }
    [data-testid="stSidebar"] [data-testid="stBaseButton-primary"]{
        background:var(--red)!important;border:none!important;color:#fff!important;
        box-shadow:0 4px 14px rgba(204,27,51,0.35)!important;
    }

    .sb-brand{padding:8px 0 20px;text-align:center;border-bottom:1px solid rgba(255,255,255,0.08);margin-bottom:20px}
    .sb-card{background:rgba(255,255,255,0.06);border-radius:var(--r-md);padding:16px;margin-bottom:8px;border:1px solid rgba(255,255,255,0.06)}
    .sb-lbl{font-size:.58rem;text-transform:uppercase;letter-spacing:.16em;color:rgba(255,255,255,0.35);font-weight:600;margin-bottom:2px}
    .sb-val{font-size:.88rem;font-weight:600;color:#fff}
    .sb-section{font-size:.58rem;text-transform:uppercase;letter-spacing:.16em;color:rgba(255,255,255,0.30);font-weight:700;margin:20px 0 10px 4px}
    .sb-prog-bg{width:100%;height:5px;border-radius:99px;background:rgba(255,255,255,0.08);overflow:hidden;margin-top:6px}
    .sb-prog-fill{height:100%;border-radius:99px;background:linear-gradient(90deg,#CC1B33,#E8435A);transition:width .5s ease}
    .sb-hr{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.05);border-radius:var(--r-md);padding:14px;margin-top:auto}
    .sb-hr *{color:rgba(255,255,255,0.45)!important;font-size:.76rem;line-height:1.7}
    .sb-hr strong{color:rgba(255,255,255,0.65)!important}

    /* ── HERO (Home) ── */
    .hero{
        background:linear-gradient(135deg,var(--navy-deep) 0%,var(--navy) 40%,var(--navy-light) 100%);
        border-radius:var(--r-xl);padding:44px 48px;position:relative;overflow:hidden;
        margin-bottom:32px;box-shadow:var(--sh-xl);
    }
    .hero::before{content:"";position:absolute;width:600px;height:600px;right:-200px;top:-250px;
        background:radial-gradient(circle,rgba(204,27,51,0.20) 0%,transparent 60%);pointer-events:none}
    .hero::after{content:"";position:absolute;width:400px;height:400px;left:-100px;bottom:-200px;
        background:radial-gradient(circle,rgba(255,255,255,0.04) 0%,transparent 70%);pointer-events:none}
    .hero *{position:relative;z-index:1}
    .hero-tag{display:inline-block;background:rgba(204,27,51,0.20);color:#FF6B7F;font-size:.65rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase;padding:5px 14px;border-radius:99px;margin-bottom:16px}
    .hero h1{color:#fff!important;font-size:2.4rem!important;margin:0 0 12px!important;font-weight:800!important}
    .hero p{color:rgba(255,255,255,0.60)!important;font-size:1.05rem;max-width:700px;margin:0!important;line-height:1.75}

    /* ── STAT CARDS ── */
    .stat{background:var(--white);border:1px solid var(--slate-200);border-radius:var(--r-lg);padding:22px 24px;transition:var(--ease)}
    .stat:hover{box-shadow:var(--sh-md);transform:translateY(-2px)}
    .stat-n{font-size:2rem;font-weight:800;color:var(--navy);letter-spacing:-.03em;line-height:1}
    .stat-l{font-size:.68rem;color:var(--slate-400);text-transform:uppercase;letter-spacing:.10em;font-weight:600;margin-top:6px}
    .stat-bar{height:4px;background:var(--slate-100);border-radius:99px;margin-top:12px;overflow:hidden}
    .stat-bar-fill{height:100%;border-radius:99px;background:linear-gradient(90deg,var(--navy),var(--navy-light));transition:width .5s ease}

    /* ── MODULE CARDS ── */
    .mc{background:var(--white);border:1px solid var(--slate-200);border-radius:var(--r-lg);padding:0;overflow:hidden;transition:var(--ease);margin-bottom:16px}
    .mc:hover{box-shadow:var(--sh-lg);transform:translateY(-3px);border-color:var(--slate-300)}
    .mc-top{display:flex;align-items:start;gap:16px;padding:24px 24px 0}
    .mc-num{width:40px;height:40px;border-radius:var(--r-md);display:flex;align-items:center;justify-content:center;font-size:.72rem;font-weight:800;letter-spacing:.04em;flex-shrink:0}
    .mc-num.todo{background:var(--slate-100);color:var(--slate-400)}
    .mc-num.active{background:var(--red-soft);color:var(--red)}
    .mc-num.done{background:var(--success-soft);color:var(--success)}
    .mc-body{flex:1;min-width:0}
    .mc-title{font-weight:700;color:var(--slate-800);font-size:.95rem;margin:0 0 4px;letter-spacing:-.01em}
    .mc-desc{color:var(--slate-500);font-size:.82rem;line-height:1.6;margin:0}
    .mc-footer{display:flex;align-items:center;justify-content:space-between;padding:16px 24px;margin-top:16px;border-top:1px solid var(--slate-100)}
    .mc-pill{font-size:.62rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:4px 12px;border-radius:99px}
    .mc-pill.todo{background:var(--slate-100);color:var(--slate-500)}
    .mc-pill.active{background:var(--warning-soft);color:#B45309}
    .mc-pill.done{background:var(--success-soft);color:var(--success)}

    /* ── MODULE PAGE HERO ── */
    .mhero{background:linear-gradient(135deg,var(--navy-deep),var(--navy) 60%,var(--navy-light));
        border-radius:var(--r-xl);padding:36px 40px;margin-bottom:28px;position:relative;overflow:hidden;box-shadow:var(--sh-lg)}
    .mhero::after{content:"";position:absolute;width:500px;height:500px;right:-200px;top:-220px;
        background:radial-gradient(circle,rgba(204,27,51,0.18) 0%,transparent 65%);pointer-events:none}
    .mhero *{position:relative;z-index:1}
    .mhero-tag{display:inline-block;background:rgba(255,255,255,0.10);color:rgba(255,255,255,0.70);font-size:.62rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;padding:4px 12px;border-radius:99px;margin-bottom:12px}
    .mhero h2{color:#fff!important;font-size:1.6rem!important;margin:0 0 8px!important}
    .mhero p{color:rgba(255,255,255,0.55);font-size:.92rem;margin:0;line-height:1.6}

    /* ── CONTENT STYLING ── */
    .info-box{background:var(--red-soft);border-left:3px solid var(--red);border-radius:0 var(--r-sm) var(--r-sm) 0;padding:16px 20px;margin:20px 0;font-size:.9rem;line-height:1.7;color:var(--slate-700)}
    .info-box.green{background:var(--success-soft);border-left-color:var(--success)}
    .info-box.blue{background:rgba(0,48,135,0.05);border-left-color:var(--navy)}

    .styled-table{width:100%;border-collapse:separate;border-spacing:0;font-size:.86rem;margin:16px 0;border-radius:var(--r-md);overflow:hidden;border:1px solid var(--slate-200)}
    .styled-table th{background:var(--navy);color:#fff;padding:11px 16px;text-align:left;font-weight:600;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase}
    .styled-table td{padding:11px 16px;border-bottom:1px solid var(--slate-100);color:var(--slate-600);background:var(--white)}
    .styled-table tr:nth-child(even) td{background:var(--slate-50)}
    .styled-table tr:last-child td{border-bottom:none}

    .timeline-item{border-left:3px solid var(--navy);padding:0 0 24px 24px;margin-left:12px;position:relative}
    .timeline-item::before{content:'';width:13px;height:13px;background:var(--navy);border:3px solid var(--slate-50);border-radius:50%;position:absolute;left:-8px;top:2px;box-shadow:0 0 0 3px rgba(0,48,135,0.15)}
    .timeline-item:last-child{border-left-color:transparent}
    .tl-title{font-weight:700;color:var(--slate-800);font-size:.95rem;margin:0 0 8px}
    .tl-body{color:var(--slate-500);font-size:.86rem;line-height:1.8}
    .tl-body li{margin-bottom:2px}

    /* ── QUIZ ── */
    .quiz-pass{background:var(--success-soft);border:1px solid rgba(5,150,105,0.20);color:var(--success);padding:20px;border-radius:var(--r-md);text-align:center;font-weight:700;font-size:.95rem}
    .quiz-fail{background:var(--red-soft);border:1px solid rgba(204,27,51,0.15);color:var(--red);padding:20px;border-radius:var(--r-md);text-align:center;font-weight:700;font-size:.95rem}

    /* ── BUTTONS ── */
    [data-testid="stBaseButton-primary"]{background:var(--red)!important;color:#fff!important;border:none!important;border-radius:var(--r-md)!important;font-weight:700!important;font-size:.86rem!important;box-shadow:0 4px 14px rgba(204,27,51,0.25)!important;transition:var(--ease)!important}
    [data-testid="stBaseButton-primary"]:hover{box-shadow:0 8px 24px rgba(204,27,51,0.35)!important;transform:translateY(-2px)!important}
    [data-testid="stBaseButton-secondary"]{border-radius:var(--r-md)!important;font-weight:600!important;border-color:var(--slate-300)!important;color:var(--slate-600)!important}
    div[data-testid="stFormSubmitButton"] button{background:var(--navy)!important;color:#fff!important;border:none!important;border-radius:var(--r-md)!important;font-weight:700!important;font-size:.88rem!important;padding:12px 24px!important;box-shadow:0 4px 14px rgba(0,48,135,0.25)!important;letter-spacing:.01em!important;transition:var(--ease)!important}
    div[data-testid="stFormSubmitButton"] button:hover{box-shadow:0 8px 24px rgba(0,48,135,0.35)!important;transform:translateY(-2px)!important}

    /* ── TABS ── */
    .stTabs [data-baseweb="tab-list"]{gap:2px;background:var(--slate-100);border-radius:var(--r-md);padding:4px}
    .stTabs [data-baseweb="tab"]{border-radius:var(--r-sm)!important;font-weight:600!important;font-size:.80rem!important;color:var(--slate-500)!important;padding:8px 16px!important;transition:var(--ease)!important}
    .stTabs [aria-selected="true"]{background:var(--white)!important;color:var(--navy)!important;box-shadow:var(--sh-sm)!important;font-weight:700!important}
    .stTabs [data-baseweb="tab-highlight"],.stTabs [data-baseweb="tab-border"]{display:none!important}

    /* ── INPUTS ── */
    .stTextInput label p{font-size:.72rem!important;font-weight:700!important;color:var(--slate-400)!important;text-transform:uppercase!important;letter-spacing:.10em!important}
    .stTextInput input{border-radius:var(--r-md)!important;border:1.5px solid var(--slate-200)!important;font-size:.92rem!important;padding:12px 16px!important;background:var(--white)!important;transition:var(--ease)!important}
    .stTextInput input:focus{border-color:var(--navy)!important;box-shadow:0 0 0 3px rgba(0,48,135,0.08)!important}
    [data-testid="stForm"]{background:var(--white);border-radius:var(--r-xl);padding:40px 36px 32px!important;box-shadow:var(--sh-xl);border:1px solid var(--slate-200)}

    /* ── CHECKBOXES ── */
    .stCheckbox label span{font-size:.88rem!important;color:var(--slate-600)!important}

    #MainMenu{visibility:hidden}footer{visibility:hidden}
    [data-testid="stHeader"]{background:transparent!important}
    </style>""")

inject_css()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  LOGIN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def show_login():
    H("<style>.stApp{background:linear-gradient(135deg,#001E54 0%,#003087 50%,#0047BA 100%)!important}</style>")
    st.markdown("")
    _,center,_=st.columns([1,1.6,1])
    with center:
        logo=_logo()
        if logo:
            H(f'<div style="text-align:center;margin:40px 0 32px"><img src="data:image/png;base64,{logo}" style="height:72px;max-width:320px;object-fit:contain;filter:brightness(1.15) drop-shadow(0 4px 12px rgba(0,0,0,0.25))"></div>')
        with st.form("login_form"):
            H('<p style="font-size:1.3rem;font-weight:800;color:var(--slate-900);margin:0 0 2px;letter-spacing:-.02em">Employee Sign In</p>')
            H('<p style="color:var(--slate-400);font-size:.86rem;margin:0 0 24px;line-height:1.6">Enter your onboarding credentials to continue.</p>')
            ac=st.text_input("Access Code",placeholder="Enter the code from HR",type="password")
            eid=st.text_input("Employee ID",placeholder="e.g. 10042")
            fn=st.text_input("Full Name",placeholder="As shown in your HR paperwork")
            H("<div style='height:8px'></div>")
            sub=st.form_submit_button("Sign In",use_container_width=True)
            if sub:
                if not ac or not eid or not fn: st.error("Please complete all fields.")
                else:
                    with st.spinner("Verifying..."):
                        if validate_login(ac,eid,fn):
                            st.session_state["logged_in"]=True
                            st.session_state["emp_name"]=fn.strip().title()
                            st.session_state["emp_number"]=eid.strip()
                            st.rerun()
        H('<div style="text-align:center;margin-top:28px"><p style="color:rgba(255,255,255,0.45);font-size:.78rem;line-height:2">Need help? &nbsp;<strong style="color:rgba(255,255,255,0.70)">Nicole Thornton</strong>&nbsp; · &nbsp;nicole.thornton@apirx.com&nbsp; · &nbsp;256-574-7528</p></div>')


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SIDEBAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def show_sidebar():
    with st.sidebar:
        logo=_logo()
        if logo:
            H(f'<div class="sb-brand"><img src="data:image/png;base64,{logo}" style="height:52px;width:auto;opacity:.95"></div>')
        d,t=prog(); pct=int((d/t)*100) if t>0 else 0
        nm=st.session_state["emp_name"]
        H(f'<div class="sb-card"><div class="sb-lbl">Signed in as</div><div class="sb-val">{nm}</div></div>')
        if st.session_state.get("emp_position"):
            H(f'<div class="sb-card"><div class="sb-lbl">Position</div><div class="sb-val">{st.session_state["emp_position"]}</div></div>')
        H(f'<div class="sb-card"><div class="sb-lbl">Progress</div><div class="sb-val">{pct}%</div><div class="sb-prog-bg"><div class="sb-prog-fill" style="width:{pct}%"></div></div></div>')
        H('<div class="sb-section">Modules</div>')
        if st.button("🏠  Dashboard",use_container_width=True,key="nav_home"):
            st.session_state["current_page"]="home"; st.session_state["current_module"]=None; st.rerun()
        for m in MK:
            dn=done(m)
            ck=" ✓" if dn else ""
            if st.button(f"{MICON[m]}  {MNAME[m]}{ck}",use_container_width=True,key=f"nav_{m}"):
                st.session_state["current_page"]="module"; st.session_state["current_module"]=m; st.rerun()
        H("<div style='height:12px'></div>")
        H('<div class="sb-hr"><strong>HR Contact</strong><br>Nicole Thornton · HR Manager<br>256-574-7528<br>nicole.thornton@apirx.com</div>')
        st.markdown("")
        if st.button("Sign Out",use_container_width=True,key="logout"):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  HOME
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def show_home():
    first=st.session_state["emp_name"].split()[0] if st.session_state["emp_name"] else "there"
    d,t=prog(); pct=int((d/t)*100) if t>0 else 0
    cdone=sum(1 for m in MK if done(m))
    H(f'<div class="hero"><span class="hero-tag">New Hire Onboarding</span><h1>Welcome, {first}</h1><p>Complete each module below to finish your orientation. Track your progress and confirm your understanding along the way.</p></div>')
    c1,c2,c3=st.columns(3)
    with c1: H(f'<div class="stat"><div class="stat-n">{pct}%</div><div class="stat-l">Overall Progress</div><div class="stat-bar"><div class="stat-bar-fill" style="width:{pct}%"></div></div></div>')
    with c2: H(f'<div class="stat"><div class="stat-n">{cdone}<span style="font-size:1rem;color:var(--slate-400);font-weight:500">/{len(MK)}</span></div><div class="stat-l">Modules Complete</div></div>')
    with c3: H(f'<div class="stat"><div class="stat-n">{d}<span style="font-size:1rem;color:var(--slate-400);font-weight:500">/{t}</span></div><div class="stat-l">Items Completed</div></div>')
    H("<div style='height:12px'></div>")
    cols=st.columns(2)
    for i,m in enumerate(MK):
        dn=done(m); p=st.session_state.get(f"quiz_{m}_passed",False); ch=st.session_state.get(f"checklist_{m}",{}); dc=sum(1 for v in ch.values() if v)
        if dn: pcls="done"; ptxt="Complete"
        elif p or dc>0: pcls="active"; ptxt="In Progress"
        else: pcls="todo"; ptxt="Not Started"
        with cols[i%2]:
            H(f'<div class="mc"><div class="mc-top"><div class="mc-num {pcls}">{MICON[m]}</div><div class="mc-body"><p class="mc-title">{MNAME[m]}</p><p class="mc-desc">{MDESC[m]}</p></div></div><div class="mc-footer"><span class="mc-pill {pcls}">{ptxt}</span></div></div>')
            if st.button("Open Module",key=f"open_{m}",use_container_width=True):
                st.session_state["current_page"]="module"; st.session_state["current_module"]=m; st.rerun()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  QUIZ & CHECKLIST
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_quiz(mk,questions):
    st.markdown("---")
    st.markdown("### Module Assessment")
    if st.session_state.get(f"quiz_{mk}_passed"):
        H('<div class="quiz-pass">✓ &nbsp;Assessment complete — all answers correct.</div>'); return
    st.caption("Answer all questions correctly to pass. You may retake as needed.")
    ans={}
    for i,q in enumerate(questions):
        ans[i]=st.radio(f"**Q{i+1}.** {q['q']}",options=q["options"],index=None,key=f"quiz_{mk}_q{i}")
    if st.button("Submit",key=f"submit_{mk}",type="primary"):
        c=sum(1 for i,q in enumerate(questions) if ans[i]==q["options"][q["answer"]])
        if c==len(questions):
            st.session_state[f"quiz_{mk}_passed"]=True
            H('<div class="quiz-pass">✓ &nbsp;All correct — assessment passed!</div>'); st.rerun()
        else:
            H(f'<div class="quiz-fail">{c}/{len(questions)} correct — please review and retry.</div>')

def render_checklist(mk,items):
    st.markdown("---")
    st.markdown("### Confirmation Checklist")
    st.caption("Confirm your understanding of each item:")
    ch=st.session_state.get(f"checklist_{mk}",{})
    for i,item in enumerate(items):
        k=f"cl_{mk}_{i}"; ch[k]=st.checkbox(item,value=ch.get(k,False),key=k)
    st.session_state[f"checklist_{mk}"]=ch
    dn=sum(1 for v in ch.values() if v)
    if dn==len(items): st.success(f"All {len(items)} items confirmed.")
    else: st.info(f"{dn} of {len(items)} confirmed.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  MODULES 1–6 (rich content, same quiz/checklist logic)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def module_welcome():
    H('<div class="mhero"><span class="mhero-tag">Module 01</span><h2>Welcome to AAP</h2><p>Learn about our history, mission, vision, and the values that guide everything we do.</p></div>')
    st.markdown("## Who We Are")
    st.markdown("""American Associated Pharmacies (AAP) is a national cooperative of more than **2,000 independent pharmacies**. Founded in 2009 when **United Drugs** (Phoenix, AZ) and **Associated Pharmacies, Inc. (API)** (Scottsboro, AL) merged to form one of the largest independent pharmacy organizations in America.

Today, AAP operates API with two U.S. warehouse locations, providing member-focused support, innovative programs, and significant cost savings through its Prime Vendor Agreement with a national wholesaler.""")
    H('<div class="info-box blue"><strong>Did you know?</strong> AAP saves its member pharmacies millions in operating and acquisition costs every year.</div>')
    st.markdown("## Our Mission")
    st.markdown("AAP provides support and customized solutions for independent community pharmacies to enhance their profitability, streamline their operations, and improve the quality of patient care.")
    st.markdown("## Our Vision")
    st.markdown("*Helping independent pharmacies thrive in a competitive healthcare market.*")
    st.markdown("## Our Core Values")
    for icon,title,desc in [("🎯","Customer Focus","Our primary focus is meeting and exceeding customer expectations. Customer service is not just a department — it's an attitude."),("⚖️","Integrity","We act with honesty without compromising truth. We build trust through consistency in our words and actions."),("🤝","Respect","We treat others with dignity, recognize the power of teamwork, and encourage open, honest communication."),("⭐","Excellence","We strive for the highest quality in everything we do and pursue continuous improvement and innovation."),("🔑","Ownership","We seek responsibility, hold ourselves accountable, and take ownership when things go wrong.")]:
        st.markdown(f"**{icon} {title}**")
        st.caption(desc)
    render_quiz("welcome",[
        {"q":"When was AAP formed?","options":["2001","2005","2009","2012"],"answer":2},
        {"q":"AAP is a cooperative of approximately how many pharmacies?","options":["500","1,000","2,000","5,000"],"answer":2},
        {"q":"Which is NOT one of AAP's five core values?","options":["Customer Focus","Integrity","Profitability","Ownership"],"answer":2},
        {"q":"What is AAP's vision statement?","options":["To be the largest pharmacy chain","Helping independent pharmacies thrive in a competitive healthcare market","Maximizing shareholder value","Providing the lowest drug prices"],"answer":1}])
    render_checklist("welcome",["I understand AAP's history and formation.","I can identify the mission and vision statements.","I know the five core values and what they mean.","I understand that AAP is a cooperative serving independent pharmacies."])

def module_conduct():
    H('<div class="mhero"><span class="mhero-tag">Module 02</span><h2>Code of Conduct & Ethics</h2><p>Professional standards, ethical behavior, and workplace expectations.</p></div>')
    st.markdown("## Business Ethics & Conduct")
    st.markdown("The success of AAP depends on our customers' trust. Every employee must act with honesty and integrity, comply with all applicable laws, and refrain from any illegal, dishonest, or unethical conduct. Failure to comply leads to disciplinary action, up to and including termination.")
    st.markdown("## Key Policies")
    tab1,tab2,tab3,tab4=st.tabs(["Conflicts of Interest","Confidentiality","Outside Employment","Equal Opportunity"])
    with tab1: st.markdown("Employees must avoid actual or potential conflicts of interest in all business dealings. Contact HR with any questions.")
    with tab2: st.markdown("All employees sign a **confidentiality and non-disclosure agreement** upon hire. Refusal is grounds for immediate termination. Personnel files are company property with restricted access. All electronic systems may be monitored.")
    with tab3: st.markdown("Outside employment is permitted as long as you satisfactorily perform your AAP responsibilities. If outside work creates a conflict or interferes with performance, you may be asked to choose.")
    with tab4: st.markdown("All employment decisions are based on merit, qualifications, and abilities. AAP does not discriminate on the basis of race, color, religion, sex, national origin, age, disability, or any other protected characteristic. Report concerns to your supervisor or HR without fear of reprisal.")
    st.markdown("## Problem Resolution Process")
    st.markdown("1. Present concerns to your **immediate supervisor** (or HR if inappropriate)\n2. If unresolved, escalate: **VP → President → CEO**\n3. CEO has full authority to resolve\n4. Board of Directors review available as final step\n\nNo employee will be penalized for voicing a complaint in a reasonable, professional manner.")
    render_quiz("conduct",[
        {"q":"What must all employees sign upon hire?","options":["Non-compete agreement","Confidentiality and non-disclosure agreement","Social media policy","Union membership form"],"answer":1},
        {"q":"What system does AAP use to verify work authorization?","options":["HIPAA","E-Verify","ADP Screening","LinkedIn"],"answer":1},
        {"q":"Who should you approach first with a workplace concern?","options":["CEO","A coworker","Your immediate supervisor or HR","An attorney"],"answer":2},
        {"q":"Outside employment is allowed as long as:","options":["You work under 20 hours elsewhere","You satisfactorily perform your AAP responsibilities","Your manager gives verbal approval","It is in a different industry"],"answer":1}])
    render_checklist("conduct",["I understand AAP's ethics expectations and my responsibility.","I understand the confidentiality and NDA requirements.","I know the problem resolution steps for workplace concerns.","I understand the equal employment opportunity policy."])

def module_attendance():
    H('<div class="mhero"><span class="mhero-tag">Module 03</span><h2>Attendance & PTO Policies</h2><p>Vacation accruals, personal leave, holidays, and the point system.</p></div>')
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
    H('<div class="info-box">Vacation cannot be taken before accrual. Requests for 5+ consecutive days require written approval from the Company President. Bank up to 19 days (152 hrs). Accrued vacation is paid out at termination.</div>')
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
    H('<div class="info-box blue">Saturday holidays are observed on Friday. Sunday holidays are observed on Monday. Employees who work on a holiday receive a floating holiday to use within 90 days.</div>')
    st.markdown("## Attendance Point System")
    st.caption("No-fault basis for non-exempt employees")
    H("""<table class="styled-table"><tr><th>Event</th><th>Points</th></tr>
    <tr><td>Tardy up to 5 minutes (grace period)</td><td>0</td></tr>
    <tr><td>Tardy or early leave (less than 4 hours)</td><td>½</td></tr>
    <tr><td>Full shift absence, tardy or early leave (4+ hours)</td><td>1</td></tr>
    <tr><td>No-call absence (15+ min after start)</td><td>1½</td></tr></table>""")
    st.markdown("### Corrective Action Thresholds")
    H("""<table class="styled-table"><tr><th>Points (rolling 12 months)</th><th>Action Taken</th></tr>
    <tr><td>5 points</td><td>Coaching Session</td></tr>
    <tr><td>6 points</td><td>Verbal Warning</td></tr>
    <tr><td>7 points</td><td>Written Warning</td></tr>
    <tr><td>8 points</td><td>Termination</td></tr></table>""")
    H('<div class="info-box green"><strong>Perfect attendance rewards:</strong> 2 consecutive months of perfect attendance removes 1 point. 3 consecutive months earns a <strong>$75 bonus</strong>.</div>')
    st.warning("Two consecutive days absent without reporting in is considered **voluntary resignation**.")
    render_quiz("attendance",[
        {"q":"What is the minimum increment for vacation time?","options":["1 hour","2 hours","4 hours","8 hours"],"answer":1},
        {"q":"What is the minimum increment for personal leave?","options":["1 hour","2 hours","4 hours","8 hours"],"answer":0},
        {"q":"How many points does a no-call absence carry?","options":["½ point","1 point","1½ points","2 points"],"answer":2},
        {"q":"At how many points does termination occur?","options":["6","7","8","10"],"answer":2},
        {"q":"How many consecutive no-call days equals voluntary resignation?","options":["1","2","3","5"],"answer":1}])
    render_checklist("attendance",["I understand the vacation accrual schedule and the 2-hour minimum.","I understand personal leave uses 1-hour increments and forfeits at year-end.","I know the 8 company holidays and the floating holiday rules.","I understand the attendance point system and corrective action thresholds.","I understand that 2 consecutive no-call days is considered voluntary resignation."])

def module_workplace():
    H('<div class="mhero"><span class="mhero-tag">Module 04</span><h2>Workplace Policies</h2><p>Safety, dress code, technology, harassment prevention, and conduct.</p></div>')
    tabs=st.tabs(["Dress Code","Safety","Drug & Alcohol","Computer & Email","Harassment","Other Policies"])
    with tabs[0]:
        st.markdown("### Personal Appearance")
        st.markdown("A neat, clean, and well-groomed appearance is required. Dress requirements vary by department, but these rules are universal:\n- All clothing must be work-appropriate — nothing too revealing or offensive\n- Avoid clothing with offensive or inappropriate stamps/messages\n- Due to allergies and asthma among staff, avoid strong perfumes and scented products\n\nNon-compliance means being sent home to change (clocked out).")
    with tabs[1]:
        st.markdown("### Workplace Safety")
        st.markdown("- **Immediately report** any unsafe conditions to your supervisor\n- **Immediately report** all work-related injuries to HR, no matter how minor\n- All work-related accidents require **immediate drug and alcohol testing**\n- Safety violations may result in disciplinary action up to termination")
    with tabs[2]:
        st.markdown("### Drug & Alcohol Policy")
        st.markdown("AAP maintains a **zero-tolerance** drug and alcohol-free workplace.\n- Being under the influence at work is strictly prohibited\n- Employees may be subject to **random drug testing** at any time\n- Violations may result in **immediate termination**\n- The Employee Assistance Program (EAP) is available for support")
    with tabs[3]:
        st.markdown("### Computer & Email Usage")
        st.markdown("All computers, files, email, and software are **AAP property** for business use.\n- Usage **may be monitored** at any time\n- Prohibited: sexually explicit content, ethnic slurs, off-color jokes, or anything constituting harassment\n- Illegal duplication of software is prohibited\n- Violations result in disciplinary action up to termination")
    with tabs[4]:
        st.markdown("### Harassment Prevention")
        st.markdown("AAP has **zero tolerance** for discrimination and unlawful harassment of any kind.\n\n**If you experience or witness harassment:**\n1. Tell the offender their conduct must stop (if comfortable)\n2. Report to your supervisor or HR\n3. If your supervisor is involved, contact the VP of Human Resources\n\n**No retaliation** will occur for good-faith complaints. Violators face discipline up to and including termination.")
    with tabs[5]:
        st.markdown("### Overtime & Schedules\nAll overtime requires **prior supervisor approval**. Non-exempt employees receive OT pay per federal/state law.")
        st.markdown("### Workplace Violence\nZero tolerance for threats, assaults, or intimidating behavior. All incidents must be reported within 24 hours.")
        st.markdown("### Business Travel\nReasonable expenses are reimbursed per policy. Falsifying expense reports is grounds for termination.")
    render_quiz("workplace",[
        {"q":"What happens after a work-related accident?","options":["Nothing unless serious","An incident report is filed","Immediate drug and alcohol testing","The employee goes home"],"answer":2},
        {"q":"AAP's computer and email systems are:","options":["Personal employee property","Company property that may be monitored","Available for personal use","Only monitored during investigations"],"answer":1},
        {"q":"If you experience harassment, what should you do first?","options":["Post about it online","Ignore it","Tell the offender to stop or report to supervisor/HR","Confront them publicly"],"answer":2},
        {"q":"Overtime must be:","options":["Approved by a coworker","Approved by your supervisor in advance","Reported after the fact","Self-authorized if needed"],"answer":1}])
    render_checklist("workplace",["I understand dress code expectations and consequences of non-compliance.","I understand safety reporting requirements and my responsibilities.","I understand the drug and alcohol policy, including random testing.","I understand that computer and email usage is monitored.","I know how to report harassment and understand the no-retaliation policy."])

def module_benefits():
    H('<div class="mhero"><span class="mhero-tag">Module 05</span><h2>Benefits Overview</h2><p>Medical, dental, vision, retirement, and supplemental coverage options.</p></div>')
    H('<div class="info-box blue"><strong>Eligibility:</strong> Full-time employees (30+ hours/week) must enroll within 30 days of hire. Benefits become effective the <strong>1st of the month following 60 days</strong> of employment. Dependent children up to age 26 may be covered.</div>')
    ft,pt=st.tabs(["Full-Time Employee Benefits","Benefits for All Employees"])
    with ft:
        st.markdown("## Medical Insurance — BlueCross BlueShield of Alabama")
        c1,c2=st.columns(2)
        with c1:
            st.markdown("### Option 1: PPO Plan")
            st.markdown("**Monthly Premiums:** Employee $157.20 · Family $678.62")
            st.markdown("Deductible: $500 / $1,000 · Coinsurance: 20%\n\nOut-of-Pocket Max: $2,250 / $4,500\n\nPCP: $30 copay · Specialist: $45 copay\n\nRx: $10 generic · $30 preferred · $50 non-preferred")
        with c2:
            st.markdown("### Option 2: HDHP with HSA")
            st.markdown("**Monthly Premiums:** Employee $136.34 · Family $581.72")
            st.markdown("Deductible: $1,700 / $3,400 · Coinsurance: 10%\n\nOut-of-Pocket Max: $3,400 / $6,800\n\nCompany HSA Contribution: $900 / $1,800 per year\n\n2026 HSA Limits: $4,400 single · $8,750 family")
        st.markdown("## Dental Insurance — Guardian")
        st.markdown("**Base Plan:** Employee $6.78/mo · **High Plan:** $10.66/mo\n\nPreventive (Coverage A): 100% both plans · Basic (Coverage B): 80% Base / 100% High\n\nMajor (Coverage C): 50% both plans (12-month waiting period) · Annual Max: $1,500 Base / $3,000 High")
        st.markdown("## Vision Insurance — Guardian (Davis Vision)")
        st.markdown("Employee $6.93/mo · Exams and lenses every 12 months · Frames every 24 months · $130 frame allowance")
        st.markdown("## Life Insurance & Disability")
        st.markdown("**Basic Life & AD&D:** Provided at **no cost** — equal to annual earnings up to $270,000\n\n**Short-Term Disability:** 60% of weekly earnings (max $1,250/wk) · Employee-paid · 7-day elimination\n\n**Long-Term Disability:** 60% of monthly earnings (max $10,000/mo) · **Company-paid** · 90-day waiting period")
        st.markdown("## Supplemental Coverage — Guardian")
        st.markdown("**Accident:** $14.55/mo employee · **Cancer:** $21.28/mo employee · **Critical Illness:** $5,000–$20,000 (age-based rates)")
        st.markdown("## 401(k) Retirement Plan")
        H('<div class="info-box green"><strong>Company Match:</strong> AAP matches 100% of the first 3% you contribute, plus 50% of the next 2% — that\'s a <strong>4% match when you contribute 5%</strong>. Company match is <strong>100% vested immediately</strong>. Eligible after 60 days.</div>')
    with pt:
        st.markdown("## Benefits Available to ALL Employees")
        st.caption("These benefits are provided at no cost regardless of employment status.")
        st.markdown("### 📱 Teladoc — Free Telehealth\nSee a doctor 24/7 from your phone or computer. General medical, mental health, and therapy — all at no cost. Call **1-800-835-2362** or visit **teladoc.com**.")
        st.markdown("### 🧠 LifeMatters EAP\nFree, confidential counseling for stress, depression, family concerns, legal and financial consultation, and more. Available 24/7 at **1-800-634-6433** or **mylifematters.com** (password: **AAP1**).")
        st.markdown("### 📚 LinkedIn Learning\nFull access to LinkedIn Learning's professional development library. Activate at **linkedin.com/learning** with your company email.")
        st.markdown("### 🎁 BenefitHub Employee Perks\nDiscounts on travel, electronics, restaurants, entertainment, and more. Register at **aapperks.benefithub.com** with referral code **9Y7G26**.")
        st.markdown("### 🕐 Personal Time Off\nAll employees — full-time and part-time — earn personal leave. See the Attendance & PTO module for full details.")
    render_quiz("benefits",[
        {"q":"When do full-time benefits become effective?","options":["Day 1","After 30 days","1st of the month following 60 days","After 90 days"],"answer":2},
        {"q":"What is the 401(k) match if you contribute 5%?","options":["2%","3%","4%","5%"],"answer":2},
        {"q":"Which benefit is provided at no cost to ALL employees?","options":["Dental insurance","Short-term disability","Teladoc telehealth","Vision insurance"],"answer":2},
        {"q":"Basic Life and AD&D coverage is provided at:","options":["50% employer-paid","No cost to the employee","Employee-paid via payroll","Only during open enrollment"],"answer":1}])
    render_checklist("benefits",["I understand the two medical plan options (PPO vs HDHP/HSA) and cost differences.","I know the 401(k) match structure (4% on 5%) and when I become eligible.","I understand which benefits are free for all employees.","I know that enrollment must happen within 30 days of hire.","I understand the supplemental coverage options available."])

def module_firststeps():
    H('<div class="mhero"><span class="mhero-tag">Module 06</span><h2>First Steps</h2><p>Your action items, system access setup, and 90-day onboarding roadmap.</p></div>')
    st.markdown("## Immediate Action Items")
    st.caption("Complete these tasks as soon as possible after your start date.")
    for icon,title,desc in [("✅","Verify Account Access","Confirm you can access your AAP email, internal systems, and tools."),("📝","Sign All New Hire Documents","Complete your full onboarding packet in BambooHR — all documents must be signed."),("📚","Activate LinkedIn Learning","Go to **linkedin.com/learning** and log in with your company email to activate your account."),("📄","Provide I-9 Documents","Bring acceptable I-9 identification (e.g., passport, or driver's license + Social Security card) to HR within **3 business days** of your start date."),("💰","Register for Paylocity","Set up your Paylocity account to access pay stubs, tax documents, and payroll information."),("📱","Download BambooHR App","Install the BambooHR mobile app and log in to access your employee profile, time off requests, and documents.")]:
        H(f'<div style="background:var(--white);border:1px solid var(--slate-200);border-radius:var(--r-md);padding:16px 20px;margin-bottom:8px;display:flex;align-items:start;gap:14px"><span style="font-size:1.2rem;flex-shrink:0;margin-top:2px">{icon}</span><div><strong style="color:var(--slate-800);font-size:.92rem">{title}</strong><br><span style="color:var(--slate-500);font-size:.86rem;line-height:1.6">{desc}</span></div></div>')
    st.markdown("---")
    st.markdown("## Your 90-Day Roadmap")
    H("""<div class="timeline-item"><p class="tl-title">Days 1–30 &nbsp;·&nbsp; Orientation & Foundation</p><div class="tl-body"><ul><li>Complete all orientation and training modules</li><li>Sign required paperwork and provide I-9 documentation</li><li>Get access to all systems and tools</li><li>Meet your team and key contacts</li><li>Shadow key processes and learn daily workflows</li><li>Complete the <strong>30-Day Survey</strong></li></ul></div></div>
    <div class="timeline-item"><p class="tl-title">Days 31–60 &nbsp;·&nbsp; Building Independence</p><div class="tl-body"><ul><li>Begin independently executing core responsibilities</li><li>Complete the <strong>60-Day Survey</strong></li><li>Become eligible for <strong>PTO and holiday pay</strong></li><li><strong>End of probationary period</strong></li><li>Set a personal goal for the next 30 days with your supervisor</li></ul></div></div>
    <div class="timeline-item"><p class="tl-title">Days 61–90 &nbsp;·&nbsp; Growth & Review</p><div class="tl-body"><ul><li>Build confidence and consistency in your role</li><li>Identify opportunities for improvement</li><li>Have your <strong>first performance review</strong></li><li><strong>Full benefits eligibility</strong> — coverage effective 1st of month after 60 days</li></ul></div></div>""")
    render_quiz("firststeps",[
        {"q":"Within how many business days must you provide I-9 documents?","options":["1 day","3 business days","5 days","10 days"],"answer":1},
        {"q":"When does the probationary period end?","options":["30 days","60 days","90 days","120 days"],"answer":1},
        {"q":"When do you become eligible for PTO and holiday pay?","options":["Day 1","After 30 days","After 60 days","After 90 days"],"answer":2},
        {"q":"Which app should you download for your employee profile?","options":["Workday","BambooHR","ADP","Gusto"],"answer":1}])
    render_checklist("firststeps",["I will verify my account access and sign all onboarding documents.","I will activate my LinkedIn Learning account with my company email.","I understand I must provide I-9 documents within 3 business days.","I will register for Paylocity and download the BambooHR app.","I understand the 90-day onboarding timeline and milestones.","I know who to contact in HR if I have questions."])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ROUTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
_FN={"welcome":module_welcome,"conduct":module_conduct,"attendance":module_attendance,"workplace":module_workplace,"benefits":module_benefits,"firststeps":module_firststeps}
def show_module(m):
    if st.button("← Back to Dashboard",key="back"):
        st.session_state["current_page"]="home"; st.session_state["current_module"]=None; st.rerun()
    _FN[m]()
    st.markdown("---")
    ix=MK.index(m)
    c1,c2=st.columns(2)
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
