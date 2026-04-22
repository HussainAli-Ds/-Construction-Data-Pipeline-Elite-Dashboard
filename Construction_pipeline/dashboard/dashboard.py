import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import plotly.graph_objects as go
import os
from dotenv import load_dotenv
from datetime import datetime, date

# ─────────────────────────────────────────────────────────────────
# ENV & PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
}

st.set_page_config(
    page_title="Elite Dashboard ⚡",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────
# NEON GLASSY CSS
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');

/* ─── Global ─── */
html, body, .stApp {
    background: #03030f !important;
    color: #ccd6f6 !important;
    font-family: 'Rajdhani', sans-serif;
}

/* animated starfield bg */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background:
        radial-gradient(ellipse at 20% 20%, rgba(0,245,255,0.04) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 80%, rgba(160,80,255,0.04) 0%, transparent 60%),
        radial-gradient(ellipse at 50% 50%, rgba(0,255,136,0.02) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* ─── Sidebar ─── */
[data-testid="stSidebar"] {
    background: rgba(3,3,15,0.97) !important;
    border-right: 1px solid rgba(0,245,255,0.2) !important;
}
[data-testid="stSidebar"]::before {
    content:'';
    position:absolute;
    top:0;left:0;right:0;bottom:0;
    background: linear-gradient(180deg, rgba(0,245,255,0.03) 0%, transparent 40%, rgba(160,80,255,0.03) 100%);
    pointer-events:none;
}

/* Sidebar nav buttons */
section[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(0,245,255,0.18) !important;
    border-radius: 10px !important;
    color: #8899bb !important;
    text-align: left !important;
    padding: 11px 16px !important;
    width: 100% !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    transition: all 0.25s ease !important;
    margin-bottom: 5px !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(0,245,255,0.08) !important;
    border-color: rgba(0,245,255,0.5) !important;
    color: #00f5ff !important;
    box-shadow: 0 0 14px rgba(0,245,255,0.15), inset 0 0 10px rgba(0,245,255,0.03) !important;
    transform: translateX(3px) !important;
}
section[data-testid="stSidebar"] .stButton > button:focus {
    border-color: #00f5ff !important;
    color: #00f5ff !important;
    box-shadow: 0 0 14px rgba(0,245,255,0.25) !important;
}

/* Sidebar collapse arrow button */
button[data-testid="collapsedControl"] {
    background: rgba(0,245,255,0.12) !important;
    border: 1px solid rgba(0,245,255,0.4) !important;
    color: #00f5ff !important;
    border-radius: 50% !important;
    box-shadow: 0 0 16px rgba(0,245,255,0.3) !important;
    transition: all 0.3s !important;
}
button[data-testid="collapsedControl"]:hover {
    background: rgba(0,245,255,0.25) !important;
    box-shadow: 0 0 24px rgba(0,245,255,0.5) !important;
}

/* ─── Top Bar ─── */
.top-bar {
    background: rgba(6,6,22,0.92);
    border: 1px solid rgba(0,245,255,0.18);
    border-radius: 14px;
    padding: 13px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 22px;
    backdrop-filter: blur(20px);
    box-shadow: 0 4px 30px rgba(0,0,0,0.4), 0 0 1px rgba(0,245,255,0.2);
}
.top-bar-center {
    font-family: 'Orbitron', monospace;
    font-size: 15px;
    font-weight: 700;
    color: #00f5ff;
    letter-spacing: 3px;
    text-shadow: 0 0 12px rgba(0,245,255,0.5);
}
.top-bar-left { color: #667799; font-size: 13px; font-weight: 500; }
.top-bar-right { color: #00f5ff; font-size: 13px; font-weight: 700; text-align:right; }

/* ─── Big Page Title ─── */
.big-title {
    font-family: 'Orbitron', monospace;
    text-align: center;
    font-size: 36px;
    font-weight: 900;
    background: linear-gradient(90deg, #00f5ff 0%, #a050ff 50%, #00f5ff 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 4s linear infinite;
    margin-bottom: 4px;
    letter-spacing: 3px;
}
.big-title-urdu {
    text-align: center;
    font-size: 20px;
    color: #556688;
    font-weight: 400;
    direction: rtl;
    margin-bottom: 24px;
}
@keyframes shimmer { 0%{background-position:0%} 100%{background-position:200%} }

/* ─── KPI Cards ─── */
.kpi-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(0,245,255,0.2);
    border-radius: 16px;
    padding: 20px 16px;
    text-align: center;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 20px rgba(0,245,255,0.06), inset 0 1px 0 rgba(255,255,255,0.05);
    transition: all 0.3s ease;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content:'';
    position:absolute;
    top:0;left:0;right:0;height:1px;
    background: linear-gradient(90deg,transparent,rgba(0,245,255,0.4),transparent);
}
.kpi-card:hover {
    border-color: rgba(0,245,255,0.5);
    box-shadow: 0 0 30px rgba(0,245,255,0.15);
    transform: translateY(-2px);
}
.kpi-label {
    font-size: 11px;
    color: #556677;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 10px;
    font-weight: 600;
}
.kpi-urdu { font-size: 11px; color: #445566; display:block; margin-top:2px; direction:rtl; }
.kpi-value {
    font-family: 'Orbitron', monospace;
    font-size: 24px;
    font-weight: 700;
    color: #00f5ff;
    text-shadow: 0 0 12px rgba(0,245,255,0.5);
    word-break: break-all;
}

/* Color variants */
.kpi-purple { border-color: rgba(160,80,255,0.25) !important; }
.kpi-purple::before { background: linear-gradient(90deg,transparent,rgba(160,80,255,0.4),transparent) !important; }
.kpi-purple .kpi-value { color: #b45fff; text-shadow: 0 0 12px rgba(180,95,255,0.5); }
.kpi-purple:hover { border-color: rgba(160,80,255,0.6) !important; box-shadow: 0 0 30px rgba(160,80,255,0.15) !important; }

.kpi-green { border-color: rgba(0,255,136,0.22) !important; }
.kpi-green::before { background: linear-gradient(90deg,transparent,rgba(0,255,136,0.4),transparent) !important; }
.kpi-green .kpi-value { color: #00ff88; text-shadow: 0 0 12px rgba(0,255,136,0.5); }
.kpi-green:hover { border-color: rgba(0,255,136,0.5) !important; box-shadow: 0 0 30px rgba(0,255,136,0.12) !important; }

.kpi-pink { border-color: rgba(255,80,150,0.22) !important; }
.kpi-pink::before { background: linear-gradient(90deg,transparent,rgba(255,80,150,0.4),transparent) !important; }
.kpi-pink .kpi-value { color: #ff5fa0; text-shadow: 0 0 12px rgba(255,80,150,0.5); }
.kpi-pink:hover { border-color: rgba(255,80,150,0.5) !important; box-shadow: 0 0 30px rgba(255,80,150,0.12) !important; }

.kpi-yellow { border-color: rgba(255,220,60,0.22) !important; }
.kpi-yellow::before { background: linear-gradient(90deg,transparent,rgba(255,220,60,0.4),transparent) !important; }
.kpi-yellow .kpi-value { color: #ffd84a; text-shadow: 0 0 12px rgba(255,220,60,0.5); }
.kpi-yellow:hover { border-color: rgba(255,220,60,0.5) !important; box-shadow: 0 0 30px rgba(255,220,60,0.12) !important; }

/* Mega KPI */
.kpi-mega {
    background: rgba(0,245,255,0.04) !important;
    border: 2px solid rgba(0,245,255,0.4) !important;
    box-shadow: 0 0 50px rgba(0,245,255,0.15), inset 0 0 30px rgba(0,245,255,0.04) !important;
    padding: 28px !important;
}
.kpi-mega::before { background: linear-gradient(90deg,transparent,rgba(0,245,255,0.6),transparent) !important; }
.kpi-mega .kpi-value { font-size: 36px !important; text-shadow: 0 0 20px rgba(0,245,255,0.7) !important; }

/* ─── Section Titles ─── */
.sec-title {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 28px 0 14px 0;
}
.sec-title-en {
    font-family: 'Orbitron', monospace;
    font-size: 16px;
    font-weight: 700;
    color: #00f5ff;
    text-shadow: 0 0 10px rgba(0,245,255,0.4);
    padding-left: 14px;
    border-left: 3px solid #00f5ff;
    box-shadow: -4px 0 12px rgba(0,245,255,0.3);
}
.sec-title-ur {
    font-size: 13px;
    color: #445566;
    direction: rtl;
}

/* ─── Table Header ─── */
.tbl-header {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: 'Rajdhani', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: #b45fff;
    text-shadow: 0 0 8px rgba(180,95,255,0.4);
    padding: 6px 14px;
    border-left: 3px solid #b45fff;
    margin: 16px 0 8px 0;
    letter-spacing: 1px;
}

/* ─── Neon Divider ─── */
.ndiv {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,245,255,0.3), rgba(160,80,255,0.3), transparent);
    margin: 22px 0;
}

/* ─── Dataframe (table) ─── */
.stDataFrame { border-radius: 12px; overflow: hidden; }
[data-testid="stDataFrame"] > div {
    border: 1px solid rgba(0,245,255,0.12) !important;
    border-radius: 12px !important;
    background: rgba(6,6,22,0.6) !important;
}

/* ─── st.metric overrides ─── */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(0,245,255,0.18) !important;
    border-radius: 12px !important;
    padding: 16px !important;
}
[data-testid="stMetricLabel"] p { color: #667799 !important; font-family: 'Rajdhani',sans-serif !important; text-transform: uppercase; font-size: 11px !important; letter-spacing: 1.5px; }
[data-testid="stMetricValue"] { color: #00f5ff !important; font-family: 'Orbitron',monospace !important; font-size: 22px !important; }

/* ─── Tabs ─── */
[data-baseweb="tab-list"] { background: rgba(6,6,22,0.9) !important; border-radius: 10px; }
[data-baseweb="tab"] { color: #667799 !important; font-family: 'Rajdhani',sans-serif !important; font-weight: 600 !important; }
[aria-selected="true"][data-baseweb="tab"] { color: #00f5ff !important; }

/* ─── Expander ─── */
[data-testid="stExpander"] {
    background: rgba(6,6,22,0.7) !important;
    border: 1px solid rgba(0,245,255,0.15) !important;
    border-radius: 12px !important;
}

/* ─── Radio ─── */
.stRadio label { color: #8899bb !important; font-family: 'Rajdhani',sans-serif !important; }
.stRadio [data-testid="stMarkdownContainer"] p { color: #8899bb !important; }

/* ─── Scrollbar ─── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #03030f; }
::-webkit-scrollbar-thumb { background: rgba(0,245,255,0.25); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: rgba(0,245,255,0.45); }

/* ─── Alert boxes ─── */
.alert-danger {
    background: rgba(255,50,80,0.08);
    border: 1px solid rgba(255,50,80,0.35);
    border-radius: 12px;
    padding: 14px 18px;
    color: #ff8899;
    margin: 8px 0;
}
.alert-success {
    background: rgba(0,255,136,0.06);
    border: 1px solid rgba(0,255,136,0.28);
    border-radius: 12px;
    padding: 14px 18px;
    color: #55ffaa;
    margin: 8px 0;
}

/* ─── Multiselect ─── */
[data-baseweb="select"] {
    background: rgba(6,6,22,0.8) !important;
    border-color: rgba(0,245,255,0.2) !important;
}

/* ─── Date input ─── */
.stDateInput input {
    background: rgba(6,6,22,0.8) !important;
    border-color: rgba(0,245,255,0.2) !important;
    color: #aaccee !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def load_table(table_name):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()

@st.cache_data(ttl=300, show_spinner=False)
def load_all_data():
    return {
        "material":    load_table("material_data"),
        "labour":      load_table("labours_data"),
        "machines":    load_table("machines_data"),
        "maintenance": load_table("machines_maintenance"),
        "progress":    load_table("progress_data"),
        "sites":       load_table("site_data"),
    }

# ─────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────
def fmt(df):
    """Format numeric columns with commas."""
    num_cols = df.select_dtypes(include="number").columns
    return df.style.format({col: "{:,.0f}" for col in num_cols})

def kpi_card(label, value, urdu="", variant=""):
    return f"""
    <div class="kpi-card {variant}">
        <div class="kpi-label">{label}<span class="kpi-urdu">{urdu}</span></div>
        <div class="kpi-value">{value}</div>
    </div>"""

def section(en, ur=""):
    return f"""<div class="sec-title">
        <span class="sec-title-en">{en}</span>
        <span class="sec-title-ur">{ur}</span>
    </div>"""

def tbl_header(label):
    return f'<div class="tbl-header">{label}</div>'

def ndiv():
    return '<div class="ndiv"></div>'

NEON_COLORS = ["#00f5ff","#b45fff","#00ff88","#ff5fa0","#ffd84a","#ff9933","#33ddff","#88ffcc"]

def neon_fig(fig, height=380):
    """Apply unified neon theme to any plotly figure."""
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(6,6,22,0.6)",
        font=dict(color="#8899bb", family="Rajdhani, sans-serif", size=12),
        title_font=dict(color="#00f5ff", family="Orbitron, monospace", size=14),
        legend=dict(
            bgcolor="rgba(6,6,22,0.85)",
            bordercolor="rgba(0,245,255,0.2)",
            borderwidth=1,
            font=dict(color="#8899bb"),
        ),
        xaxis=dict(
            gridcolor="rgba(0,245,255,0.07)",
            tickcolor="#00f5ff",
            linecolor="rgba(0,245,255,0.2)",
            tickfont=dict(color="#667799"),
            title_font=dict(color="#00f5ff"),
        ),
        yaxis=dict(
            gridcolor="rgba(0,245,255,0.07)",
            tickcolor="#00f5ff",
            linecolor="rgba(0,245,255,0.2)",
            tickfont=dict(color="#667799"),
            title_font=dict(color="#00f5ff"),
        ),
        margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig

# ─────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"

# ─────────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────────
with st.spinner("⚡ Connecting to database..."):
    DATA = load_all_data()

# ─────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:24px 0 16px 0;">
        <div style="font-family:'Orbitron',monospace;font-size:13px;color:rgba(0,245,255,0.4);
                    letter-spacing:4px;margin-bottom:6px;">ELITE</div>
        <div style="font-family:'Orbitron',monospace;font-size:22px;font-weight:900;
                    color:#00f5ff;text-shadow:0 0 20px rgba(0,245,255,0.6);letter-spacing:2px;">
            ⚡ DASHBOARD
        </div>
        <div style="font-size:13px;color:#334455;margin-top:6px;direction:rtl;">
            الیٹ ڈیش بورڈ
        </div>
    </div>
    <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(0,245,255,0.25),transparent);
                margin:0 0 16px 0;"></div>
    """, unsafe_allow_html=True)

    nav_items = [
        ("🏠", "Home",     "ہوم",       "home"),
        ("📦", "Material", "مواد",      "material"),
        ("👷", "Labour",   "مزدور",     "labour"),
        ("🚜", "Machines", "مشینیں",    "machines"),
        ("📈", "Progress", "پیشرفت",    "progress"),
        ("🏗", "Sites",    "سائٹس",     "sites"),
    ]

    for icon, name, urdu, key in nav_items:
        label = f"{icon}  {name}  ·  {urdu}"
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.rerun()

    st.markdown("""
    <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(160,80,255,0.2),transparent);
                margin:14px 0;"></div>
    """, unsafe_allow_html=True)

    if st.button("❓  How to Use  ·  استعمال کا طریقہ", key="nav_howto", use_container_width=True):
        st.session_state.page = "howto"
        st.rerun()

    st.markdown("""
    <div style="margin-top:30px;padding:14px;background:rgba(0,245,255,0.03);
                border:1px solid rgba(0,245,255,0.1);border-radius:10px;text-align:center;">
        <div style="font-size:11px;color:#334455;margin-bottom:4px;">CREATED BY</div>
        <div style="font-size:13px;color:#445566;font-weight:600;">Hussain-Ali</div>
        <div style="font-size:11px;color:#2d3d4d;margin-top:4px;">ha780383@gmail.com</div>
        <div style="font-size:11px;color:#2d3d4d;">0335-7897412 | 0331-8782469</div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# TOP BAR
# ─────────────────────────────────────────────────────────────────
def show_topbar():
    total_records = sum(len(df) for df in DATA.values())
    last_updated  = datetime.now().strftime("%d %b %Y · %H:%M")
    st.markdown(f"""
    <div class="top-bar">
        <div class="top-bar-left">
            🕐 &nbsp;<b style="color:#8899bb">Last Updated</b>&nbsp; · &nbsp;{last_updated}
        </div>
        <div class="top-bar-center">⚡ ELITE DASHBOARD</div>
        <div class="top-bar-right">
            📊 Total Records &nbsp;·&nbsp; <b style="color:#00f5ff;font-family:'Orbitron',monospace">{total_records:,}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# PAGE: HOME
# ─────────────────────────────────────────────────────────────────
def page_home():
    show_topbar()
    st.markdown("""
    <div class="big-title">⚡ MAIN DASHBOARD</div>
    <div class="big-title-urdu">مرکزی ڈیش بورڈ · پروجیکٹ مانیٹرنگ سسٹم</div>
    """, unsafe_allow_html=True)

    lab = DATA.get("labour",      pd.DataFrame())
    mac = DATA.get("machines",    pd.DataFrame())
    mat = DATA.get("material",    pd.DataFrame())
    mnt = DATA.get("maintenance", pd.DataFrame())

    # ── Compute values ──
    total_labours  = lab["labour_id"].nunique()  if not lab.empty and "labour_id"  in lab.columns else 0
    total_machines = mac["machine_id"].nunique() if not mac.empty and "machine_id" in mac.columns else 0
    total_mat_types = mat["material"].nunique()  if not mat.empty and "material"   in mat.columns else 0

    lab_cost  = lab["total_cost"].sum()  if not lab.empty and "total_cost" in lab.columns else 0
    mnt_cost  = mnt["total_cost"].sum()  if not mnt.empty and "total_cost" in mnt.columns else 0
    mat_cost  = mat["total_cost"].sum()  if not mat.empty and "total_cost" in mat.columns else 0
    total_cost = lab_cost + mnt_cost + mat_cost

    # ── Row 1: Count KPIs ──
    st.markdown(section("📊 Key Indicators", "اہم کارکردگی اشارے"), unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(kpi_card("👷 Total Labours",       f"{total_labours:,}",   "کل مزدور"),     unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("🚜 Total Machines",      f"{total_machines:,}",  "کل مشینیں",    "kpi-purple"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("📦 Material Types Used", f"{total_mat_types:,}", "مواد کی اقسام","kpi-green"),  unsafe_allow_html=True)

    # ── Row 2: Cost KPIs ──
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(kpi_card("💼 Total Labour Cost",   f"PKR {lab_cost:,.0f}", "مزدور لاگت",   "kpi-yellow"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("🔧 Total Machine Cost",  f"PKR {mnt_cost:,.0f}", "مشین لاگت",    "kpi-pink"),   unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("📦 Total Material Cost", f"PKR {mat_cost:,.0f}", "مواد لاگت",    "kpi-purple"), unsafe_allow_html=True)

    # ── Mega KPI ──
    st.markdown(kpi_card(
        "💎 TOTAL PROJECT COST · کل پروجیکٹ لاگت",
        f"PKR {total_cost:,.0f}", "", "kpi-mega"
    ), unsafe_allow_html=True)

    st.markdown(ndiv(), unsafe_allow_html=True)

    # ── Line chart – Cost over time ──
    st.markdown(section("📈 Cost Over Time", "وقت کے ساتھ لاگت"), unsafe_allow_html=True)

    time_col1, time_col2 = st.columns([3, 1])
    with time_col2:
        grp = st.radio("Group By · گروپ", ["Day", "Month", "Year"],
                       horizontal=False, key="home_grp")

    cost_dfs = []
    for df_name, label in [("labour","Labour"), ("maintenance","Machine"), ("material","Material")]:
        df_ = DATA.get(df_name, pd.DataFrame())
        if not df_.empty and "date" in df_.columns and "total_cost" in df_.columns:
            tmp = df_[["date","total_cost"]].copy()
            tmp["date"] = pd.to_datetime(tmp["date"], errors="coerce")
            tmp["Category"] = label
            cost_dfs.append(tmp)

    with time_col1:
        if cost_dfs:
            combined = pd.concat(cost_dfs).dropna(subset=["date"])
            if grp == "Month":
                combined["date"] = combined["date"].dt.to_period("M").dt.to_timestamp()
            elif grp == "Year":
                combined["date"] = combined["date"].dt.to_period("Y").dt.to_timestamp()
            trend = combined.groupby(["date","Category"])["total_cost"].sum().reset_index()
            fig = px.line(trend, x="date", y="total_cost", color="Category",
                          color_discrete_map={"Labour":"#00f5ff","Machine":"#b45fff","Material":"#00ff88"},
                          markers=True, title="Total Cost Trend by Category",
                          labels={"total_cost":"Cost (PKR)","date":"Date"})
            fig.update_traces(line_width=2.5)
            st.plotly_chart(neon_fig(fig), use_container_width=True)
        else:
            st.info("No time-series cost data found.")

    # ── Column chart – Cost comparison ──
    st.markdown(section("📊 Cost Comparison by Category", "لاگت کا موازنہ"), unsafe_allow_html=True)
    comp = pd.DataFrame({
        "Category": ["Labour", "Machine/Maint.", "Material"],
        "Cost (PKR)": [lab_cost, mnt_cost, mat_cost],
    })
    fig2 = px.bar(comp, x="Category", y="Cost (PKR)", color="Category",
                  color_discrete_map={"Labour":"#00f5ff","Machine/Maint.":"#b45fff","Material":"#00ff88"},
                  title="Project Cost Breakdown", text_auto=True)
    fig2.update_traces(marker_line_width=0, textfont_color="white")
    st.plotly_chart(neon_fig(fig2, height=360), use_container_width=True)


# ─────────────────────────────────────────────────────────────────
# PAGE: MATERIAL
# ─────────────────────────────────────────────────────────────────
def page_material():
    show_topbar()
    st.markdown("""
    <div class="big-title">📦 MATERIAL ANALYTICS</div>
    <div class="big-title-urdu">مواد کا تجزیہ</div>
    """, unsafe_allow_html=True)

    df = DATA.get("material", pd.DataFrame()).copy()
    if df.empty:
        st.warning("⚠️ No material data found."); return

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # ── Filters ──
    with st.expander("🔍 Filters · فلٹر", expanded=False):
        fc1, fc2, fc3 = st.columns(3)
        if "date" in df.columns and df["date"].notna().any():
            s = fc1.date_input("Start · شروع", df["date"].dropna().min().date(), key="mat_s")
            e = fc2.date_input("End · اختتام",  df["date"].dropna().max().date(), key="mat_e")
            df = df[(df["date"] >= pd.Timestamp(s)) & (df["date"] <= pd.Timestamp(e))]
        if "material" in df.columns:
            sel = fc3.multiselect("Material Type", df["material"].dropna().unique(), key="mat_sel")
            if sel: df = df[df["material"].isin(sel)]

    # ── KPIs ──
    tot_types = df["material"].nunique() if "material" in df.columns else 0
    tot_tons  = df["tons"].sum()         if "tons"     in df.columns else 0
    tot_cost  = df["total_cost"].sum()   if "total_cost" in df.columns else 0

    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(kpi_card("📦 Types Used",   f"{tot_types}",          "مواد کی اقسام"),             unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("⚖️ Total Tons",   f"{tot_tons:,.1f} T",    "کل ٹن",        "kpi-green"),  unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("💰 Total Cost",   f"PKR {tot_cost:,.0f}",  "کل لاگت",      "kpi-yellow"), unsafe_allow_html=True)

    st.markdown(ndiv(), unsafe_allow_html=True)

    # ── Summary Table ──
    st.markdown(tbl_header("📋 Summary · خلاصہ"), unsafe_allow_html=True)
    if "material" in df.columns:
        agg = {c: "sum" for c in ["tons","total_cost","trips"] if c in df.columns}
        if agg:
            summ = df.groupby("material").agg(agg).reset_index().sort_values(list(agg.keys())[-1], ascending=False)
            summ.columns = ["Material"] + [c.replace("total_cost","Cost (PKR)").replace("tons","Tons").replace("trips","Trips") for c in agg]
            summ.insert(0,"#", range(1, len(summ)+1))
            st.dataframe(fmt(summ.reset_index(drop=True)), use_container_width=True)

    # ── Transporter Table ──
    st.markdown(tbl_header("🚛 Transporter · ٹرانسپورٹر"), unsafe_allow_html=True)
    trans_cols = ["transporter_name","material","tons","trips","phone_number"]
    avail = [c for c in trans_cols if c in df.columns]
    if "transporter_name" in avail and len(avail) > 1:
        grp_c = [c for c in ["transporter_name","material"] if c in avail]
        a2 = {c:"sum" for c in ["tons","trips"] if c in avail}
        if "phone_number" in avail: a2["phone_number"] = "first"
        t2 = df.groupby(grp_c).agg(a2).reset_index()
        t2.rename(columns={"transporter_name":"Transporter","material":"Material","tons":"Tons",
                             "trips":"Trips","phone_number":"Phone"}, inplace=True)
        t2.insert(0,"#", range(1, len(t2)+1))
        st.dataframe(fmt(t2.reset_index(drop=True)), use_container_width=True)
    else:
        st.info("ℹ️ Transporter columns not found in dataset (expected: transporter_name, phone_number).")

    # ── Used in Days Table ──
    st.markdown(tbl_header("📅 Used in Days · یومیہ استعمال"), unsafe_allow_html=True)
    if "date" in df.columns and "material" in df.columns:
        day_a = {c:"sum" for c in ["tons","trips","total_cost"] if c in df.columns}
        day_df = df.groupby(["date","material"]).agg(day_a).reset_index().sort_values("date",ascending=False)
        day_df.rename(columns={"date":"Date","material":"Material","tons":"Tons",
                                "trips":"Trips","total_cost":"Cost (PKR)"}, inplace=True)
        day_df.insert(0,"#", range(1, len(day_df)+1))
        st.dataframe(fmt(day_df.reset_index(drop=True)), use_container_width=True)

    st.markdown(ndiv(), unsafe_allow_html=True)

    # ── Charts ──
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(section("📈 Cost Over Time", "وقت کے ساتھ لاگت"), unsafe_allow_html=True)
        if "date" in df.columns and "total_cost" in df.columns and "material" in df.columns:
            ld = df.groupby(["date","material"])["total_cost"].sum().reset_index()
            fig = px.line(ld, x="date", y="total_cost", color="material",
                          color_discrete_sequence=NEON_COLORS, markers=True,
                          title="Material Cost Trend",
                          labels={"total_cost":"Cost (PKR)","date":"Date","material":"Material"})
            fig.update_traces(line_width=2)
            st.plotly_chart(neon_fig(fig), use_container_width=True)

    with c2:
        st.markdown(section("🥧 Tons Distribution", "ٹن کی تقسیم"), unsafe_allow_html=True)
        if "material" in df.columns and "tons" in df.columns:
            pie_d = df.groupby("material")["tons"].sum().reset_index()
            fig2 = px.pie(pie_d, names="material", values="tons",
                          color_discrete_sequence=NEON_COLORS,
                          title="Material Tons Distribution",
                          hole=0.45)
            fig2.update_traces(textfont_color="white", pull=[0.03]*len(pie_d))
            st.plotly_chart(neon_fig(fig2), use_container_width=True)


# ─────────────────────────────────────────────────────────────────
# PAGE: LABOUR
# ─────────────────────────────────────────────────────────────────
def page_labour():
    show_topbar()
    st.markdown("""
    <div class="big-title">👷 LABOUR ANALYTICS</div>
    <div class="big-title-urdu">مزدوروں کا تجزیہ</div>
    """, unsafe_allow_html=True)

    df = DATA.get("labour", pd.DataFrame()).copy()
    if df.empty:
        st.warning("⚠️ No labour data found."); return

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # ── Filters ──
    with st.expander("🔍 Filters · فلٹر", expanded=False):
        fc1, fc2, fc3 = st.columns(3)
        if "date" in df.columns and df["date"].notna().any():
            s = fc1.date_input("Start", df["date"].dropna().min().date(), key="lab_s")
            e = fc2.date_input("End",   df["date"].dropna().max().date(), key="lab_e")
            df = df[(df["date"] >= pd.Timestamp(s)) & (df["date"] <= pd.Timestamp(e))]
        if "labour_name" in df.columns:
            sel = fc3.multiselect("Labour", df["labour_name"].dropna().unique(), key="lab_sel")
            if sel: df = df[df["labour_name"].isin(sel)]

    # ── KPIs ──
    tot_lab  = df["labour_id"].nunique()    if "labour_id"    in df.columns else 0
    tot_days = df["working_days"].sum()     if "working_days" in df.columns else 0
    tot_cost = df["total_cost"].sum()       if "total_cost"   in df.columns else 0

    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(kpi_card("👷 Total Labours",  f"{tot_lab:,}",          "کل مزدور"),              unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("📅 Working Days",   f"{tot_days:,}",         "کام کے دن",  "kpi-green"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("💰 Total Cost",     f"PKR {tot_cost:,.0f}",  "کل لاگت",    "kpi-yellow"),unsafe_allow_html=True)

    st.markdown(ndiv(), unsafe_allow_html=True)

    # ── Build worker summary ──
    workers = pd.DataFrame()
    if "labour_name" in df.columns:
        agg = {}
        if "working_days"   in df.columns: agg["working_days"]   = "sum"
        if "total_cost"     in df.columns: agg["total_cost"]     = "sum"
        if "labour_rating"  in df.columns: agg["labour_rating"]  = "mean"
        if "labour_number"  in df.columns: agg["labour_number"]  = "first"
        workers = df.groupby("labour_name").agg(agg).reset_index()
        workers.rename(columns={"labour_name":"Name","working_days":"Working Days",
                                 "total_cost":"Total Cost","labour_rating":"Rating (Avg)",
                                 "labour_number":"Phone"}, inplace=True)

    # ── Best Workers ──
    st.markdown(tbl_header("🏆 Best Workers (by Rating) · بہترین مزدور"), unsafe_allow_html=True)
    if not workers.empty:
        best = workers.sort_values("Rating (Avg)", ascending=False) if "Rating (Avg)" in workers.columns else workers
        best = best.reset_index(drop=True)
        best.insert(0,"#", range(1, len(best)+1))
        st.dataframe(fmt(best), use_container_width=True)

    # ── Days & Workers ──
    st.markdown(tbl_header("📅 Days & Workers · یومیہ مزدور"), unsafe_allow_html=True)
    days_df = pd.DataFrame()
    if "date" in df.columns:
        da = {}
        if "labour_id"   in df.columns: da["labour_id"]   = "nunique"
        if "total_cost"  in df.columns: da["total_cost"]   = "sum"
        days_df = df.groupby("date").agg(da).reset_index()
        days_df.rename(columns={"date":"Date","labour_id":"Total Workers","total_cost":"Total Cost"}, inplace=True)
        days_df.sort_values("Date", ascending=False, inplace=True)
        days_df.insert(0,"#", range(1, len(days_df)+1))
        st.dataframe(fmt(days_df.reset_index(drop=True)), use_container_width=True)

    # ── Bad Workers ──
    st.markdown(tbl_header("⚠️ Underperforming Workers (Low Rating) · کم کارکردگی"), unsafe_allow_html=True)
    if not workers.empty and "Rating (Avg)" in workers.columns:
        bad = workers.sort_values("Rating (Avg)", ascending=True).reset_index(drop=True)
        bad.insert(0,"#", range(1, len(bad)+1))
        st.dataframe(fmt(bad), use_container_width=True)

    st.markdown(ndiv(), unsafe_allow_html=True)

    # ── Bubble Chart ──
    st.markdown(section("🫧 Rating Distribution", "ریٹنگ تقسیم"), unsafe_allow_html=True)
    if "labour_rating" in df.columns:
        bub_agg = {"labour_name": "count"} if "labour_name" in df.columns else {}
        if "total_cost" in df.columns: bub_agg["total_cost"] = "sum"
        bub = df.groupby("labour_rating").agg(bub_agg).reset_index()
        bub.rename(columns={"labour_name":"Workers","total_cost":"Total Cost"}, inplace=True)
        size_col = "Total Cost" if "Total Cost" in bub.columns else "Workers"
        fig = px.scatter(bub, x="labour_rating", y="Workers" if "Workers" in bub.columns else bub.columns[1],
                         size=size_col, color="labour_rating",
                         color_continuous_scale=["#ff5fa0","#ffd84a","#00f5ff","#00ff88","#b45fff"],
                         title="Workers by Rating Group",
                         labels={"labour_rating":"Rating (1–5)"})
        fig.update_traces(marker_line_color="rgba(0,0,0,0)")
        st.plotly_chart(neon_fig(fig), use_container_width=True)

    # ── Line charts ──
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(section("👷 Workers Per Day", "یومیہ مزدور"), unsafe_allow_html=True)
        if not days_df.empty and "Total Workers" in days_df.columns:
            f2 = px.line(days_df, x="Date", y="Total Workers", markers=True,
                         title="Daily Worker Count", line_shape="spline")
            f2.update_traces(line_color="#00f5ff", line_width=2.5,
                              fill="tozeroy", fillcolor="rgba(0,245,255,0.04)")
            st.plotly_chart(neon_fig(f2), use_container_width=True)
    with c2:
        st.markdown(section("💰 Labour Cost Per Day", "یومیہ مزدور لاگت"), unsafe_allow_html=True)
        if not days_df.empty and "Total Cost" in days_df.columns:
            f3 = px.line(days_df, x="Date", y="Total Cost", markers=True,
                         title="Daily Labour Cost", line_shape="spline")
            f3.update_traces(line_color="#00ff88", line_width=2.5,
                              fill="tozeroy", fillcolor="rgba(0,255,136,0.04)")
            st.plotly_chart(neon_fig(f3), use_container_width=True)


# ─────────────────────────────────────────────────────────────────
# PAGE: MACHINES
# ─────────────────────────────────────────────────────────────────
def page_machines():
    show_topbar()
    st.markdown("""
    <div class="big-title">🚜 MACHINE ANALYTICS</div>
    <div class="big-title-urdu">مشینوں کا تجزیہ</div>
    """, unsafe_allow_html=True)

    df  = DATA.get("machines",    pd.DataFrame()).copy()
    mnt = DATA.get("maintenance", pd.DataFrame()).copy()
    if df.empty:
        st.warning("⚠️ No machine data found."); return

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # ── KPIs ──
    tot_mac   = df["machine_id"].nunique()   if "machine_id"   in df.columns else 0
    tot_work  = df["working_time"].sum()     if "working_time" in df.columns else 0
    mnt_cost  = mnt["total_cost"].sum()      if not mnt.empty and "total_cost" in mnt.columns else 0
    fuel_used = df["fuel_used"].sum()        if "fuel_used"    in df.columns else 0
    fuel_cost = df["fuel_cost"].sum()        if "fuel_cost"    in df.columns else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.markdown(kpi_card("🚜 Total Machines",    f"{tot_mac}",                "کل مشینیں"),                   unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("⏱ Working Time",       f"{tot_work:,.0f} h",        "کام کا وقت",    "kpi-green"),  unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("🔧 Maintenance Cost",  f"PKR {mnt_cost:,.0f}",      "مرمت لاگت",     "kpi-pink"),   unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("⛽ Fuel Used",          f"{fuel_used:,.0f} L",       "ایندھن",        "kpi-purple"), unsafe_allow_html=True)
    with c5: st.markdown(kpi_card("💰 Fuel Cost",          f"PKR {fuel_cost:,.0f}",    "ایندھن لاگت",   "kpi-yellow"), unsafe_allow_html=True)

    st.markdown(ndiv(), unsafe_allow_html=True)

    # ── Most Working Machines ──
    st.markdown(tbl_header("🏆 Most Working Machines · سب سے زیادہ کام"), unsafe_allow_html=True)
    grp_c = ["machine_id"] + (["machine_name"] if "machine_name" in df.columns else [])
    ma = {c:"sum" for c in ["working_time","idle_time","fuel_used","fuel_cost"] if c in df.columns}
    mac_summ = df.groupby(grp_c).agg(ma).reset_index() if ma else df[grp_c].drop_duplicates()

    if not mnt.empty and "machine_id" in mnt.columns:
        mnt_g = {}
        if "total_cost"    in mnt.columns: mnt_g["total_cost"]    = "sum"
        if "repair_cost"   in mnt.columns: mnt_g["repair_cost"]   = "sum"
        if "machine_fault" in mnt.columns: mnt_g["machine_fault"] = "count"
        if mnt_g:
            m_agg = mnt.groupby("machine_id").agg(mnt_g).reset_index()
            m_agg.rename(columns={"total_cost":"Maint. Cost","repair_cost":"Repair Cost",
                                   "machine_fault":"Faults"}, inplace=True)
            mac_summ = mac_summ.merge(m_agg, on="machine_id", how="left")

    mac_summ.rename(columns={"machine_id":"ID","machine_name":"Name","working_time":"Working Time",
                               "idle_time":"Idle Time","fuel_used":"Fuel Used","fuel_cost":"Fuel Cost"},
                    inplace=True)
    if "Working Time" in mac_summ.columns:
        mac_summ.sort_values("Working Time", ascending=False, inplace=True)
    mac_summ.insert(0,"#", range(1, len(mac_summ)+1))
    st.dataframe(fmt(mac_summ.reset_index(drop=True)), use_container_width=True)

    # ── Days & Machines ──
    st.markdown(tbl_header("📅 Days & Machines · یومیہ مشینیں"), unsafe_allow_html=True)
    days_mac = pd.DataFrame()
    if "date" in df.columns:
        df["_idle_flag"] = (df["idle_time"] > 0).astype(int) if "idle_time" in df.columns else 0
        dm = {"machine_id": "nunique", "_idle_flag": "sum"}
        for c in ["fuel_used","fuel_cost"]:
            if c in df.columns: dm[c] = "sum"
        days_mac = df.groupby("date").agg(dm).reset_index()
        days_mac.rename(columns={"date":"Date","machine_id":"Working Machines",
                                  "_idle_flag":"Idle Machines","fuel_used":"Fuel Used",
                                  "fuel_cost":"Fuel Cost"}, inplace=True)
        days_mac.sort_values("Date", ascending=False, inplace=True)
        days_mac.insert(0,"#", range(1, len(days_mac)+1))
        st.dataframe(fmt(days_mac.reset_index(drop=True)), use_container_width=True)

    st.markdown(ndiv(), unsafe_allow_html=True)

    # ── Charts ──
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(section("📈 Working vs Idle Machines", "فعال بمقابلہ بے کار مشینیں"), unsafe_allow_html=True)
        if not days_mac.empty and "Working Machines" in days_mac.columns:
            y_cols = ["Working Machines"]
            if "Idle Machines" in days_mac.columns: y_cols.append("Idle Machines")
            fig = px.line(days_mac, x="Date", y=y_cols,
                          color_discrete_map={"Working Machines":"#00ff88","Idle Machines":"#ff5fa0"},
                          markers=True, title="Daily Machine Activity")
            fig.update_traces(line_width=2.5)
            st.plotly_chart(neon_fig(fig), use_container_width=True)
    with c2:
        st.markdown(section("⛽ Daily Fuel Cost", "یومیہ ایندھن لاگت"), unsafe_allow_html=True)
        if not days_mac.empty and "Fuel Cost" in days_mac.columns:
            fig2 = px.line(days_mac, x="Date", y="Fuel Cost", markers=True,
                           title="Fuel Cost Trend", line_shape="spline")
            fig2.update_traces(line_color="#ffd84a", line_width=2.5,
                                fill="tozeroy", fillcolor="rgba(255,216,74,0.04)")
            st.plotly_chart(neon_fig(fig2), use_container_width=True)

    # ── Idle ratio alert ──
    st.markdown(section("🚨 Smart Alerts", "ذہین الرٹ"), unsafe_allow_html=True)
    if "working_time" in df.columns and "idle_time" in df.columns:
        w = df["working_time"].sum(); i = df["idle_time"].sum()
        ratio = i / (w + 1)
        if ratio > 0.5:
            st.markdown(f"""<div class="alert-danger">
                🚨 <b>High Machine Idle Time!</b><br>
                Idle time is <b>{ratio:.1%}</b> of working time — machines are underutilised.<br>
                <b>Solution:</b> Improve scheduling or reallocate machines to active sites.
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-success">✅ Machines are being utilised efficiently.</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# PAGE: PROGRESS & SITES
# ─────────────────────────────────────────────────────────────────
def page_progress_sites():
    show_topbar()
    st.markdown("""
    <div class="big-title">📈 PROGRESS & SITES</div>
    <div class="big-title-urdu">پیشرفت اور سائٹس</div>
    """, unsafe_allow_html=True)

    prog  = DATA.get("progress", pd.DataFrame())
    sites = DATA.get("sites",    pd.DataFrame())

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(section("📈 Progress Data", "پیشرفت ڈیٹا"), unsafe_allow_html=True)
        if not prog.empty:
            st.markdown(tbl_header("📊 Progress Summary · پیشرفت خلاصہ"), unsafe_allow_html=True)
            st.dataframe(fmt(prog.reset_index(drop=True)), use_container_width=True)

            # KPI
            if "progress_percent" in prog.columns:
                avg_prog = prog["progress_percent"].mean()
                st.markdown(kpi_card("📈 Avg Progress", f"{avg_prog:.1f}%", "اوسط پیشرفت","kpi-green"), unsafe_allow_html=True)

            # Chart if date column exists
            if "date" in prog.columns and prog["date"].notna().any():
                prog2 = prog.copy()
                prog2["date"] = pd.to_datetime(prog2["date"], errors="coerce")
                num_c = prog2.select_dtypes("number").columns
                if len(num_c):
                    fig = px.line(prog2, x="date", y=num_c[0],
                                  title="Progress Over Time", markers=True, line_shape="spline")
                    fig.update_traces(line_color="#00f5ff", line_width=2.5,
                                      fill="tozeroy", fillcolor="rgba(0,245,255,0.04)")
                    st.plotly_chart(neon_fig(fig), use_container_width=True)
        else:
            st.info("ℹ️ No progress data available.")

    with c2:
        st.markdown(section("🏗 Sites Data", "سائٹس ڈیٹا"), unsafe_allow_html=True)
        if not sites.empty:
            st.markdown(tbl_header("🏗 Sites Summary · سائٹ خلاصہ"), unsafe_allow_html=True)
            st.dataframe(fmt(sites.reset_index(drop=True)), use_container_width=True)

            # site count KPI
            n_sites = len(sites)
            st.markdown(kpi_card("🏗 Total Sites", f"{n_sites}", "کل سائٹس","kpi-purple"), unsafe_allow_html=True)

            # bar chart if numeric
            num_s = sites.select_dtypes("number").columns
            if len(num_s) and sites.shape[0] > 1:
                id_col = sites.select_dtypes("object").columns
                if len(id_col):
                    fig2 = px.bar(sites, x=id_col[0], y=num_s[0],
                                  color_discrete_sequence=NEON_COLORS,
                                  title=f"Sites by {num_s[0]}")
                    fig2.update_traces(marker_line_width=0)
                    st.plotly_chart(neon_fig(fig2), use_container_width=True)
        else:
            st.info("ℹ️ No sites data available.")


# ─────────────────────────────────────────────────────────────────
# PAGE: HOW TO USE
# ─────────────────────────────────────────────────────────────────
def page_howto():
    show_topbar()
    st.markdown("""
    <div class="big-title">📘 HOW TO USE</div>
    <div class="big-title-urdu">استعمال کا مکمل طریقہ</div>
    """, unsafe_allow_html=True)

    st.markdown(section("🇬🇧 English Guide", "انگریزی رہنمائی"), unsafe_allow_html=True)
    st.markdown("""
    <div style="background:rgba(6,6,22,0.7);border:1px solid rgba(0,245,255,0.15);border-radius:14px;padding:24px;line-height:1.9;color:#99aabb;font-size:15px;">

    <h4 style="color:#00f5ff;font-family:'Orbitron',monospace;font-size:14px;letter-spacing:2px;">⚡ GETTING STARTED</h4>
    <p>This dashboard connects to your PostgreSQL database and provides real-time monitoring of your construction project.
    Set your database credentials in the <b style="color:#aaccee">.env</b> file before launching.</p>

    <h4 style="color:#00f5ff;font-family:'Orbitron',monospace;font-size:14px;letter-spacing:2px;">🔀 SIDEBAR NAVIGATION</h4>
    <ul>
        <li><b style="color:#aaccee">🏠 Home</b> – Overview with total KPIs, cost trends, and category comparison charts.</li>
        <li><b style="color:#aaccee">📦 Material</b> – Material usage, transporter details, and daily consumption breakdown.</li>
        <li><b style="color:#aaccee">👷 Labour</b> – Worker performance rankings, daily attendance, and cost trends.</li>
        <li><b style="color:#aaccee">🚜 Machines</b> – Machine activity, fuel tracking, maintenance costs, idle-time alerts.</li>
        <li><b style="color:#aaccee">📈 Progress</b> – Project progress percentages and site-level summaries.</li>
        <li><b style="color:#aaccee">🏗 Sites</b> – Site-level data view and charts.</li>
    </ul>
    <p>Click the <b style="color:#00f5ff">▶ arrow button</b> at the top-right of the screen to collapse or expand the sidebar.</p>

    <h4 style="color:#00f5ff;font-family:'Orbitron',monospace;font-size:14px;letter-spacing:2px;">🔍 FILTERS</h4>
    <p>Each page has an expandable <b style="color:#aaccee">Filters</b> section at the top. Use it to:</p>
    <ul>
        <li>Select a <b style="color:#aaccee">date range</b> to narrow data to a specific period.</li>
        <li>Use the <b style="color:#aaccee">dropdown</b> to focus on specific materials, workers, or machines.</li>
    </ul>
    <p>All tables, KPIs, and charts update automatically when you apply a filter.</p>

    <h4 style="color:#00f5ff;font-family:'Orbitron',monospace;font-size:14px;letter-spacing:2px;">📊 TOP BAR</h4>
    <ul>
        <li><b style="color:#aaccee">Left side</b> – Shows when the data was last fetched from the database.</li>
        <li><b style="color:#aaccee">Right side</b> – Shows total number of records across all tables.</li>
    </ul>

    <h4 style="color:#00f5ff;font-family:'Orbitron',monospace;font-size:14px;letter-spacing:2px;">📈 CHARTS</h4>
    <ul>
        <li><b>Line Charts</b> – Show trends over time (day/month/year toggleable on Home).</li>
        <li><b>Bar Charts</b> – Compare costs or quantities across categories.</li>
        <li><b>Pie / Donut Charts</b> – Show proportional distribution (e.g. tons by material).</li>
        <li><b>Bubble Charts</b> – Display labour rating groups with cost magnitude as bubble size.</li>
    </ul>
    <p>All charts are interactive — hover for exact values, click legend items to toggle series, zoom in by dragging.</p>

    <h4 style="color:#00f5ff;font-family:'Orbitron',monospace;font-size:14px;letter-spacing:2px;">🚨 SMART ALERTS</h4>
    <ul>
        <li><span style="color:#ff8899">🔴 Red Alert</span> – A problem has been detected (e.g. high idle time, low worker ratings). It explains what the issue is and how to fix it.</li>
        <li><span style="color:#55ffaa">🟢 Green Alert</span> – Everything is working efficiently. No action required.</li>
    </ul>

    <h4 style="color:#00f5ff;font-family:'Orbitron',monospace;font-size:14px;letter-spacing:2px;">💾 DATABASE</h4>
    <p>Data is cached for <b style="color:#aaccee">5 minutes</b> to avoid repeated database calls. To force a refresh, reload the page.</p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(section("🇵🇰 اردو رہنمائی", "Urdu Guide"), unsafe_allow_html=True)
    st.markdown("""
    <div style="background:rgba(6,6,22,0.7);border:1px solid rgba(160,80,255,0.15);border-radius:14px;
                padding:24px;line-height:2.2;color:#99aabb;font-size:15px;direction:rtl;text-align:right;">

    <h4 style="color:#b45fff;font-family:'Rajdhani',sans-serif;font-size:16px;">⚡ شروعات</h4>
    <p>یہ ڈیش بورڈ آپ کے PostgreSQL ڈیٹا بیس سے جڑتا ہے اور آپ کے تعمیراتی پروجیکٹ کی
    ریئل ٹائم نگرانی فراہم کرتا ہے۔ شروع کرنے سے پہلے <b style="color:#aaccee">.env</b> فائل میں
    اپنی ڈیٹا بیس معلومات درج کریں۔</p>

    <h4 style="color:#b45fff;font-family:'Rajdhani',sans-serif;font-size:16px;">🔀 سائیڈ بار نیویگیشن</h4>
    <ul>
        <li><b style="color:#aaccee">🏠 ہوم</b> – مجموعی KPIs، لاگت کا رجحان اور موازنہ چارٹ۔</li>
        <li><b style="color:#aaccee">📦 مواد</b> – مواد کا استعمال، ٹرانسپورٹر تفصیل، یومیہ استعمال۔</li>
        <li><b style="color:#aaccee">👷 مزدور</b> – مزدوروں کی کارکردگی، یومیہ حاضری، لاگت رجحان۔</li>
        <li><b style="color:#aaccee">🚜 مشینیں</b> – مشینوں کی سرگرمی، ایندھن، مرمت لاگت، بے کار وقت الرٹ۔</li>
        <li><b style="color:#aaccee">📈 پیشرفت</b> – پروجیکٹ کی پیشرفت فیصد اور سائٹ کا خلاصہ۔</li>
        <li><b style="color:#aaccee">🏗 سائٹس</b> – سائٹ کی سطح پر ڈیٹا اور چارٹ۔</li>
    </ul>
    <p>سائیڈ بار کو بند یا کھولنے کے لیے اسکرین کے اوپری دائیں کونے میں <b style="color:#b45fff">▶ تیر کا بٹن</b> دبائیں۔</p>

    <h4 style="color:#b45fff;font-family:'Rajdhani',sans-serif;font-size:16px;">🔍 فلٹر</h4>
    <p>ہر صفحے پر اوپر ایک <b style="color:#aaccee">فلٹر</b> سیکشن ہے۔ اسے استعمال کریں:</p>
    <ul>
        <li>مخصوص عرصے کے لیے <b style="color:#aaccee">تاریخ کی حد</b> منتخب کریں۔</li>
        <li>مخصوص مواد، مزدور یا مشین دیکھنے کے لیے <b style="color:#aaccee">ڈراپ ڈاؤن</b> استعمال کریں۔</li>
    </ul>

    <h4 style="color:#b45fff;font-family:'Rajdhani',sans-serif;font-size:16px;">📊 ٹاپ بار</h4>
    <ul>
        <li><b style="color:#aaccee">بائیں طرف</b> – ڈیٹا بیس سے آخری بار ڈیٹا لانے کا وقت۔</li>
        <li><b style="color:#aaccee">دائیں طرف</b> – تمام ٹیبلز میں ریکارڈ کی کل تعداد۔</li>
    </ul>

    <h4 style="color:#b45fff;font-family:'Rajdhani',sans-serif;font-size:16px;">🚨 ذہین الرٹ</h4>
    <ul>
        <li><span style="color:#ff8899">🔴 سرخ الرٹ</span> – مسئلہ پایا گیا ہے۔ مسئلہ کیا ہے اور کیسے حل کریں یہ بھی بتایا گیا ہے۔</li>
        <li><span style="color:#55ffaa">🟢 سبز الرٹ</span> – سب کچھ ٹھیک چل رہا ہے۔ کوئی کارروائی ضروری نہیں۔</li>
    </ul>

    <h4 style="color:#b45fff;font-family:'Rajdhani',sans-serif;font-size:16px;">💾 ڈیٹا بیس</h4>
    <p>ڈیٹا <b style="color:#aaccee">5 منٹ</b> کے لیے محفوظ رہتا ہے تاکہ بار بار ڈیٹا بیس سے ڈیٹا نہ لیا جائے۔
    تازہ ڈیٹا کے لیے صفحہ ریفریش کریں۔</p>

    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# MAIN ROUTER
# ─────────────────────────────────────────────────────────────────
page = st.session_state.page

if page == "home":
    page_home()
elif page == "material":
    page_material()
elif page == "labour":
    page_labour()
elif page == "machines":
    page_machines()
elif page in ("progress", "sites"):
    page_progress_sites()
elif page == "howto":
    page_howto()
else:
    page_home()