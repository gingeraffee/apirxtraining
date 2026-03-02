# onboarding_app.py
# Canonical UI/theme: training_app.py (single source of truth)

import os
import re
import json
import hmac
import sqlite3
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

import streamlit as st


# -----------------------------------------------------------------------------
# Page config (keep conservative for older Streamlit)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Onboarding Portal",
    page_icon="✅",
    layout="wide",
)


# -----------------------------------------------------------------------------
# Paths / app constants
# -----------------------------------------------------------------------------
APP_DIR = Path(__file__).resolve().parent
TRAINING_APP_PATH = APP_DIR / "training_app.py"
DATA_DIR = APP_DIR / ".data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "onboarding.db"

APP_VERSION = "onboarding_app_template_v1"


# -----------------------------------------------------------------------------
# Session state contract
# -----------------------------------------------------------------------------
def ensure_session_defaults() -> None:
    defaults = {
        # auth/session
        "auth_ok": False,
        "username": "",
        "profile": None,  # dict
        # app routing
        "nav": "Home",
        "track": "Administrative",  # "Administrative" | "Warehouse"
        # persisted data
        "progress": {},  # dict: module_key -> list/obj
        "notes": {},     # dict: module_key -> str
        # ui messages
        "flash": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# -----------------------------------------------------------------------------
# Database / data layer
# -----------------------------------------------------------------------------
def _db() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def _ensure_schema(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            display_name TEXT,
            role TEXT,
            track TEXT,
            created_at TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS progress (
            username TEXT NOT NULL,
            module_key TEXT NOT NULL,
            payload TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            PRIMARY KEY (username, module_key)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            username TEXT NOT NULL,
            module_key TEXT NOT NULL,
            note TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            PRIMARY KEY (username, module_key)
        )
        """
    )
    conn.commit()


def _now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _hash_password(password: str) -> str:
    """
    Lightweight hash (HMAC-SHA256) to avoid extra deps.
    For production: use bcrypt/argon2. Kept simple for portability.
    """
    secret = os.environ.get("ONBOARDING_SECRET", "dev-secret-change-me")
    return hmac.new(secret.encode("utf-8"), password.encode("utf-8"), digestmod="sha256").hexdigest()


def authenticate(username: str, password: str) -> bool:
    username = (username or "").strip().lower()
    if not username or not password:
        return False

    conn = _db()
    _ensure_schema(conn)

    row = conn.execute("SELECT username, password_hash FROM users WHERE username = ?", (username,)).fetchone()
    if not row:
        return False

    return hmac.compare_digest(row["password_hash"], _hash_password(password))


def get_profile(username: str) -> Optional[Dict[str, Any]]:
    username = (username or "").strip().lower()
    if not username:
        return None

    conn = _db()
    _ensure_schema(conn)

    row = conn.execute(
        "SELECT username, display_name, role, track, created_at FROM users WHERE username = ?",
        (username,),
    ).fetchone()
    if not row:
        return None
    return dict(row)


def load_progress(username: str) -> Dict[str, Any]:
    username = (username or "").strip().lower()
    if not username:
        return {}

    conn = _db()
    _ensure_schema(conn)

    rows = conn.execute(
        "SELECT module_key, payload FROM progress WHERE username = ?",
        (username,),
    ).fetchall()

    out: Dict[str, Any] = {}
    for r in rows:
        try:
            out[r["module_key"]] = json.loads(r["payload"])
        except Exception:
            # fallback if corrupted
            out[r["module_key"]] = r["payload"]
    return out


def save_progress(username: str, module_key: str, payload: Any) -> None:
    username = (username or "").strip().lower()
    module_key = (module_key or "").strip()
    if not username or not module_key:
        return

    conn = _db()
    _ensure_schema(conn)

    conn.execute(
        """
        INSERT INTO progress(username, module_key, payload, updated_at)
        VALUES(?,?,?,?)
        ON CONFLICT(username, module_key)
        DO UPDATE SET payload=excluded.payload, updated_at=excluded.updated_at
        """,
        (username, module_key, json.dumps(payload), _now_iso()),
    )
    conn.commit()


def load_notes(username: str) -> Dict[str, str]:
    username = (username or "").strip().lower()
    if not username:
        return {}

    conn = _db()
    _ensure_schema(conn)

    rows = conn.execute(
        "SELECT module_key, note FROM notes WHERE username = ?",
        (username,),
    ).fetchall()

    return {r["module_key"]: (r["note"] or "") for r in rows}


def save_notes(username: str, module_key: str, note: str) -> None:
    username = (username or "").strip().lower()
    module_key = (module_key or "").strip()
    if not username or not module_key:
        return

    conn = _db()
    _ensure_schema(conn)

    conn.execute(
        """
        INSERT INTO notes(username, module_key, note, updated_at)
        VALUES(?,?,?,?)
        ON CONFLICT(username, module_key)
        DO UPDATE SET note=excluded.note, updated_at=excluded.updated_at
        """,
        (username, module_key, note or "", _now_iso()),
    )
    conn.commit()


# -----------------------------------------------------------------------------
# Training theme: import or extract verbatim CSS from training_app.py
# -----------------------------------------------------------------------------
def _extract_training_css_from_file(py_path: Path) -> str:
    '''
    Extracts *verbatim* CSS blocks from training_app.py.
    Strategy:
      - If training_app defines TRAINING_THEME_CSS or THEME_CSS as triple-quoted string, use it.
      - Else, collect any st.markdown("""<style> ... </style>""", unsafe_allow_html=True) blocks.
    '''
    if not py_path.exists():
        return ""

    text = py_path.read_text(encoding="utf-8", errors="ignore")

    # 1) Named CSS variables
    for var_name in ("TRAINING_THEME_CSS", "THEME_CSS", "APP_CSS", "CSS"):
        m = re.search(rf"{var_name}\s*=\s*([\"']{{3}})(.*?)(\1)", text, flags=re.DOTALL)
        if m and m.group(2).strip():
            return m.group(2)

    # 2) st.markdown(<style>...</style>) blocks
    style_blocks = re.findall(r"(<style.*?>.*?</style>)", text, flags=re.DOTALL | re.IGNORECASE)
    if style_blocks:
        # Return exactly what was in training_app, preserving order
        return "\n\n".join(style_blocks)

    return ""


def apply_training_theme() -> None:
    """
    Applies training_app.py theme *without duplicating CSS*.
    Preferred:
      - from training_app import apply_theme (or similar) and call it.
    Fallback:
      - extract CSS verbatim from training_app.py and inject.
    """
    # Try to import and call canonical theme function(s)
    try:
        import training_app  # type: ignore

        # Common patterns: apply_theme(), inject_css(), load_theme()
        for fn_name in ("apply_theme", "inject_css", "load_theme", "apply_app_theme"):
            fn = getattr(training_app, fn_name, None)
            if callable(fn):
                fn()
                return

        # Or a canonical CSS string
        for var in ("TRAINING_THEME_CSS", "THEME_CSS", "APP_CSS", "CSS"):
            css = getattr(training_app, var, None)
            if isinstance(css, str) and css.strip():
                st.markdown(css, unsafe_allow_html=True)
                return

    except Exception:
        pass

    # Fallback: extract from file verbatim
    css = _extract_training_css_from_file(TRAINING_APP_PATH)
    if css.strip():
        st.markdown(css, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# UI helpers (use training_app helpers if present; otherwise safe fallbacks)
# -----------------------------------------------------------------------------
def _training_ui():
    """
    Returns (module, None) if import works, else (None, error_str).
    """
    try:
        import training_app  # type: ignore
        return training_app, None
    except Exception as e:
        return None, str(e)


def render_header(title: str, subtitle: str = "") -> None:
    training_app, _ = _training_ui()

    # Use canonical training header renderer if it exists
    if training_app:
        for fn_name in ("render_header", "header", "_render_header"):
            fn = getattr(training_app, fn_name, None)
            if callable(fn):
                try:
                    fn(title, subtitle)  # common signature
                    return
                except TypeError:
                    fn(title)
                    if subtitle:
                        st.caption(subtitle)
                    return

    # Fallback header (should still look fine under training CSS)
    st.markdown(f"## {title}")
    if subtitle:
        st.caption(subtitle)


def render_card(title: str, body_fn, right_fn=None) -> None:
    """
    body_fn(): renders main card body
    right_fn(): optional right-side content in card
    """
    training_app, _ = _training_ui()

    # Prefer training card renderer
    if training_app:
        for fn_name in ("render_card", "_render_card", "card"):
            fn = getattr(training_app, fn_name, None)
            if callable(fn):
                try:
                    # Some training apps accept (doc) dicts. Provide a compatible shape.
                    doc = {"title": title, "desc": "", "id": title}
                    fn(doc, body_fn=body_fn, right_fn=right_fn)  # if supported
                    return
                except TypeError:
                    # Try a simpler call pattern
                    try:
                        fn(title, body_fn)
                        return
                    except TypeError:
                        # Last attempt: call and let body render after
                        fn(title)
                        body_fn()
                        if right_fn:
                            right_fn()
                        return

    # Fallback: HTML-ish card wrapper (CSS should style .card/.card-title if present)
    st.markdown(f"<div class='card'><div class='card-title'>{title}</div>", unsafe_allow_html=True)
    if right_fn:
        left, right = st.columns([3, 1])
        with left:
            body_fn()
        with right:
            right_fn()
    else:
        body_fn()
    st.markdown("</div>", unsafe_allow_html=True)


def sidebar_nav(pages: List[str]) -> str:
    """
    Training-style sidebar navigation if available; fallback to radio.
    """
    training_app, _ = _training_ui()

    if training_app:
        for fn_name in ("sidebar_nav", "render_sidebar", "_sidebar_nav"):
            fn = getattr(training_app, fn_name, None)
            if callable(fn):
                try:
                    return fn(pages, default=st.session_state.get("nav", pages[0]))
                except TypeError:
                    return fn(pages)

    # Fallback nav
    st.sidebar.markdown("### Navigation")
    choice = st.sidebar.radio("Go to", pages, index=pages.index(st.session_state.get("nav", pages[0])))
    return choice


# -----------------------------------------------------------------------------
# Module catalog + tracks
# -----------------------------------------------------------------------------
@dataclass(frozen=True)
class ModuleDef:
    key: str
    title: str
    desc: str
    track: str  # "Administrative" | "Warehouse" | "Both"


# IMPORTANT: preserve your onboarding content/logic here.
# Replace these placeholders with your real modules/steps from the current onboarding_app.py.
MODULES: List[ModuleDef] = [
    ModuleDef("start_here", "Start Here", "How this onboarding portal works.", "Both"),
    ModuleDef("bamboo_packet", "Complete New Hire Packet (BambooHR)", "Required for all new hires.", "Both"),
    ModuleDef("admin_tools", "Admin Tools & Systems", "Email, calendar, files, internal tools.", "Administrative"),
    ModuleDef("warehouse_safety", "Warehouse Safety Basics", "PPE, traffic lanes, reporting, drills.", "Warehouse"),
    ModuleDef("policies", "Policies & Acknowledgements", "Handbook, attendance, conduct, safety policies.", "Both"),
]


def visible_modules(track: str) -> List[ModuleDef]:
    """
    Non-recursive. Deterministic. No calling itself. No side effects.
    """
    t = (track or "Administrative").strip()
    out = []
    for m in MODULES:
        if m.track == "Both" or m.track == t:
            out.append(m)
    return out


# -----------------------------------------------------------------------------
# Onboarding rendering (progress + notes)
# -----------------------------------------------------------------------------
def _progress_key(module_key: str) -> str:
    return f"progress::{module_key}"


def _notes_key(module_key: str) -> str:
    return f"notes::{module_key}"


def render_module(m: ModuleDef) -> None:
    """
    Renders a module inside a training-style card, with progress + notes persistence.
    """
    username = st.session_state["username"]

    def body():
        st.markdown(m.desc)

        # --- Progress controls (simple + robust) ---
        done = bool(st.session_state["progress"].get(m.key, {}).get("done", False))
        new_done = st.checkbox("Mark complete", value=done, key=_progress_key(m.key))
        if new_done != done:
            st.session_state["progress"][m.key] = {"done": new_done, "updated_at": _now_iso()}
            save_progress(username, m.key, st.session_state["progress"][m.key])

        # --- Notes ---
        existing_note = st.session_state["notes"].get(m.key, "")
        new_note = st.text_area("Notes", value=existing_note, height=140, key=_notes_key(m.key))
        if new_note != existing_note:
            st.session_state["notes"][m.key] = new_note
            save_notes(username, m.key, new_note)

    def right():
        # Status pill / meta
        p = st.session_state["progress"].get(m.key, {})
        is_done = bool(p.get("done", False))
        st.markdown("**Status**")
        st.write("✅ Complete" if is_done else "⬜ Not complete")
        if p.get("updated_at"):
            st.caption(f"Updated: {p['updated_at']}")

    render_card(m.title, body_fn=body, right_fn=right)


# -----------------------------------------------------------------------------
# Login screen (stable, self-contained)
# -----------------------------------------------------------------------------
def _show_login_screen() -> None:
    render_header("Onboarding Portal", "Sign in to continue")

    # Keep this screen extremely stable: no cross-calls, no hidden dependencies.
    with st.container():
        st.markdown("### Login")

        u = st.text_input("Username", value=st.session_state.get("username", ""), key="login_user")
        p = st.text_input("Password", type="password", key="login_pass")

        cols = st.columns([1, 3])
        with cols[0]:
            clicked = st.button("Sign in", use_container_width=True)
        with cols[1]:
            if st.session_state.get("flash"):
                st.warning(st.session_state["flash"])

        if clicked:
            ok = authenticate(u, p)
            if not ok:
                st.session_state["flash"] = "Invalid username or password."
                st.session_state["auth_ok"] = False
                return

            st.session_state["username"] = (u or "").strip().lower()
            st.session_state["auth_ok"] = True
            st.session_state["flash"] = ""

            prof = get_profile(st.session_state["username"]) or {}
            st.session_state["profile"] = prof

            # Track comes from profile if available, else keep default
            prof_track = (prof.get("track") or "").strip()
            if prof_track in ("Administrative", "Warehouse"):
                st.session_state["track"] = prof_track

            # Hydrate persisted data
            st.session_state["progress"] = load_progress(st.session_state["username"])
            st.session_state["notes"] = load_notes(st.session_state["username"])

            # Move into app
            st.rerun()


# -----------------------------------------------------------------------------
# Main app shell (theme + sidebar + pages)
# -----------------------------------------------------------------------------
def _show_app_shell() -> None:
    prof = st.session_state.get("profile") or {}
    display_name = prof.get("display_name") or st.session_state["username"]

    pages = ["Home", "Modules", "Profile"]
    st.sidebar.markdown("")

    # Track selector in sidebar (training-style layout should style this)
    st.sidebar.markdown("### Track")
    track = st.sidebar.selectbox(
        "Choose training path",
        ["Administrative", "Warehouse"],
        index=0 if st.session_state["track"] == "Administrative" else 1,
    )
    if track != st.session_state["track"]:
        st.session_state["track"] = track
        # No recursion: visible_modules reads this cleanly

    st.sidebar.markdown("---")
    st.session_state["nav"] = sidebar_nav(pages)

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Signed in as:** {display_name}")
    if st.sidebar.button("Sign out"):
        # deterministic reset
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        ensure_session_defaults()
        st.rerun()

    # --- Pages ---
    nav = st.session_state["nav"]

    if nav == "Home":
        render_header("Home", f"Track: {st.session_state['track']}")
        st.markdown(
            "Welcome! This portal uses the same layout/theme as the HR Training app so it feels identical."
        )

        mods = visible_modules(st.session_state["track"])
        done_count = sum(1 for m in mods if st.session_state["progress"].get(m.key, {}).get("done"))
        st.metric("Modules completed", f"{done_count} / {len(mods)}")

        # Quick view cards
        for m in mods[:3]:
            render_module(m)

    elif nav == "Modules":
        render_header("Onboarding Modules", f"Track: {st.session_state['track']}")
        mods = visible_modules(st.session_state["track"])
        for m in mods:
            render_module(m)

    elif nav == "Profile":
        render_header("Profile", "Your onboarding profile")
        st.markdown("### Details")
        st.write(prof if prof else {"username": st.session_state["username"]})
        st.markdown("### Data health")
        st.write(
            {
                "progress_keys": len(st.session_state.get("progress") or {}),
                "notes_keys": len(st.session_state.get("notes") or {}),
                "db_path": str(DB_PATH),
                "app_version": APP_VERSION,
            }
        )


# -----------------------------------------------------------------------------
# Boot
# -----------------------------------------------------------------------------
def main() -> None:
    ensure_session_defaults()
    apply_training_theme()

    if not st.session_state["auth_ok"]:
        _show_login_screen()
        return

    _show_app_shell()


if __name__ == "__main__":
    main()
