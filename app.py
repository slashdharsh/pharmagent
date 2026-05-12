import streamlit as st
import time
import os
from pharmagent import research_drug
from brief_writer import write_marketing_brief

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="PharmAgent · AI Pharma Intelligence",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="auto"
)

# ─────────────────────────────────────────
# SESSION STATE
# Streamlit Cloud has no persistent disk.
# st.session_state is an in-memory dictionary
# that lives as long as the browser tab is open.
# All generated briefs are stored here.
# ─────────────────────────────────────────
if "saved_briefs" not in st.session_state:
    st.session_state.saved_briefs = {}  # { "Ozempic": "brief text..." }


# ─────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=DM+Mono:wght@300;400;500&display=swap');

:root {
    --bg:       #05080f;
    --surface:  #090e18;
    --card:     #0d1420;
    --card2:    #101828;
    --border:   #1a2535;
    --border2:  #243040;
    --accent:   #00c8ff;
    --accent2:  #6c5ce7;
    --accent3:  #00e5a0;
    --text:     #dce8f5;
    --muted:    #4e6070;
    --muted2:   #7a8fa0;
    --danger:   #ff4f6a;
    --gold:     #f5c842;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}
#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton, [data-testid="stToolbar"] { display: none !important; }
.stApp { background-color: var(--bg) !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 99px; }

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
    min-width: 260px !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--accent) !important;
}
.sidebar-inner { padding: 1.75rem 1.5rem 2rem; }
.logo-wrap { display: flex; align-items: center; gap: 12px; margin-bottom: 2rem; }
.logo-icon { width: 42px; height: 42px; background: linear-gradient(135deg, var(--accent), var(--accent2)); border-radius: 12px; font-size: 1.3rem; box-shadow: 0 0 20px rgba(0,200,255,0.3); flex-shrink: 0; }
.logo-name { font-size: 1.15rem; font-weight: 800; letter-spacing: -0.3px; color: var(--text); line-height: 1; }
.logo-sub { font-family: 'DM Mono', monospace; font-size: 0.62rem; color: var(--muted); text-transform: uppercase; letter-spacing: 2px; margin-top: 3px; }
.live-badge { display: inline-flex; align-items: center; gap: 6px; background: rgba(0,229,160,0.1); border: 1px solid rgba(0,229,160,0.25); border-radius: 20px; padding: 5px 12px; font-family: 'DM Mono', monospace; font-size: 0.68rem; color: var(--accent3); margin-bottom: 1.75rem; width: fit-content; }
.live-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--accent3); animation: blink 2s ease-in-out infinite; flex-shrink: 0; }
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.2;} }
.nav-label { font-family: 'DM Mono', monospace; font-size: 0.62rem; text-transform: uppercase; letter-spacing: 2.5px; color: var(--muted); margin-bottom: 0.6rem; padding-left: 4px; }
div[data-testid="stRadio"] > div { gap: 2px !important; flex-direction: column !important; }
div[data-testid="stRadio"] label { background: transparent !important; border: 1px solid transparent !important; border-radius: 10px !important; padding: 0.65rem 1rem !important; cursor: pointer !important; transition: all 0.18s ease !important; color: var(--muted2) !important; font-size: 0.9rem !important; font-weight: 500 !important; }
div[data-testid="stRadio"] label:hover { background: rgba(0,200,255,0.06) !important; border-color: var(--border) !important; color: var(--text) !important; }
div[data-testid="stRadio"] > label { display: none !important; }
.stack-wrap { margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid var(--border); }
.stack-label { font-family: 'DM Mono', monospace; font-size: 0.62rem; text-transform: uppercase; letter-spacing: 2px; color: var(--muted); margin-bottom: 0.7rem; }
.stack-pill { display: inline-flex; align-items: center; gap: 5px; background: rgba(108,92,231,0.1); border: 1px solid rgba(108,92,231,0.25); border-radius: 6px; padding: 3px 9px; font-family: 'DM Mono', monospace; font-size: 0.7rem; color: #a390f5; margin: 2px 2px 2px 0; }
.footer-note { margin-top: 2rem; font-family: 'DM Mono', monospace; font-size: 0.62rem; color: var(--muted); line-height: 1.9; text-transform: uppercase; letter-spacing: 1.5px; }

.block-container { padding: 0 !important; max-width: 100% !important; }

.hero-banner { position: relative; width: 100%; min-height: 340px; overflow: hidden; display: flex; align-items: flex-end; padding: 2.5rem 3rem; margin-bottom: 0; }
.hero-bg { position: absolute; inset: 0; background: linear-gradient(to right, rgba(5,8,15,0.97) 35%, rgba(5,8,15,0.7) 65%, rgba(5,8,15,0.4) 100%), url('https://images.unsplash.com/photo-1576671081837-49000212a370?w=1600&q=80&auto=format&fit=crop'); background-size: cover; background-position: center right; }
.hero-content { position: relative; z-index: 2; max-width: 680px; }
.hero-eyebrow { font-family: 'DM Mono', monospace; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 3.5px; color: var(--accent); margin-bottom: 1rem; display: flex; align-items: center; gap: 10px; }
.hero-eyebrow::before { content: ''; display: inline-block; width: 30px; height: 1px; background: var(--accent); }
.hero-h1 { font-size: 3rem; font-weight: 900; line-height: 1.05; letter-spacing: -1.5px; color: #fff; margin-bottom: 1rem; }
.hero-h1 span { background: linear-gradient(90deg, var(--accent), var(--accent2)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.hero-p { font-size: 1rem; font-weight: 300; color: rgba(255,255,255,0.55); line-height: 1.65; max-width: 500px; margin-bottom: 1.75rem; }
.hero-stats { display: flex; gap: 2rem; margin-top: 0.5rem; }
.hero-stat-val { font-size: 1.6rem; font-weight: 800; color: #fff; line-height: 1; }
.hero-stat-val span { color: var(--accent); }
.hero-stat-lbl { font-family: 'DM Mono', monospace; font-size: 0.62rem; text-transform: uppercase; letter-spacing: 2px; color: rgba(255,255,255,0.35); margin-top: 4px; }
.molecule-wrap { position: absolute; right: 2rem; top: 50%; transform: translateY(-50%); opacity: 0.18; z-index: 1; animation: rotate-slow 30s linear infinite; }
@keyframes rotate-slow { from{transform:translateY(-50%) rotate(0deg);} to{transform:translateY(-50%) rotate(360deg);} }

.content-area { padding: 2.5rem 3rem; }
.pg-eyebrow { font-family: 'DM Mono', monospace; font-size: 0.68rem; text-transform: uppercase; letter-spacing: 3px; color: var(--accent); margin-bottom: 0.6rem; }

.search-card { background: var(--card); border: 1px solid var(--border); border-radius: 20px; padding: 2rem; position: relative; overflow: hidden; margin-bottom: 2rem; }
.search-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, var(--accent), var(--accent2), transparent 80%); }
.search-card-label { font-family: 'DM Mono', monospace; font-size: 0.68rem; text-transform: uppercase; letter-spacing: 2.5px; color: var(--muted); margin-bottom: 1rem; }

.stTextInput > div > div > input { background: var(--card2) !important; border: 1px solid var(--border2) !important; border-radius: 12px !important; color: var(--text) !important; font-family: 'Outfit', sans-serif !important; font-size: 1rem !important; padding: 0.8rem 1.1rem !important; height: 48px !important; transition: border-color 0.2s, box-shadow 0.2s !important; }
.stTextInput > div > div > input:focus { border-color: var(--accent) !important; box-shadow: 0 0 0 3px rgba(0,200,255,0.1) !important; }
.stTextInput > div > div > input::placeholder { color: var(--muted) !important; }
.stTextInput label { display: none !important; }
.stTextArea > div > div > textarea { background: var(--card2) !important; border: 1px solid var(--border) !important; border-radius: 14px !important; color: var(--text) !important; font-family: 'DM Mono', monospace !important; font-size: 0.83rem !important; line-height: 1.75 !important; padding: 1.25rem !important; }
.stTextArea > div > div > textarea:focus { border-color: var(--accent) !important; box-shadow: 0 0 0 3px rgba(0,200,255,0.08) !important; }

.stButton > button { font-family: 'Outfit', sans-serif !important; font-weight: 700 !important; font-size: 0.9rem !important; border-radius: 12px !important; border: none !important; padding: 0 1.5rem !important; height: 48px !important; cursor: pointer !important; transition: all 0.2s ease !important; }
.stButton > button[kind="primary"] { background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%) !important; color: #05080f !important; box-shadow: 0 4px 20px rgba(0,200,255,0.3) !important; }
.stButton > button[kind="primary"]:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 30px rgba(0,200,255,0.4) !important; }
.stButton > button:not([kind="primary"]) { background: var(--card2) !important; color: var(--text) !important; border: 1px solid var(--border2) !important; }
.stButton > button:not([kind="primary"]):hover { border-color: var(--accent) !important; color: var(--accent) !important; }
.stDownloadButton > button { font-family: 'Outfit', sans-serif !important; font-weight: 600 !important; font-size: 0.85rem !important; background: var(--card2) !important; border: 1px solid var(--border2) !important; border-radius: 10px !important; color: var(--muted2) !important; height: 42px !important; transition: all 0.2s !important; }
.stDownloadButton > button:hover { border-color: var(--accent) !important; color: var(--accent) !important; }

[data-testid="stStatus"] { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: 14px !important; }
.stAlert { border-radius: 12px !important; font-size: 0.88rem !important; }

.chip { display: inline-flex; align-items: center; gap: 5px; background: rgba(0,200,255,0.08); border: 1px solid rgba(0,200,255,0.2); border-radius: 6px; padding: 3px 10px; font-family: 'DM Mono', monospace; font-size: 0.72rem; color: var(--accent); }
.chip-green { background: rgba(0,229,160,0.08); border-color: rgba(0,229,160,0.2); color: var(--accent3); }
.chip-purple { background: rgba(108,92,231,0.1); border-color: rgba(108,92,231,0.25); color: #a390f5; }

[data-testid="stMetric"] { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: 16px !important; padding: 1.5rem !important; position: relative !important; overflow: hidden !important; }
[data-testid="stMetric"]::before { content: '' !important; position: absolute !important; top: 0; left: 0; right: 0 !important; height: 2px !important; background: linear-gradient(90deg, var(--accent), var(--accent2)) !important; }
[data-testid="stMetricLabel"] > div { font-family: 'DM Mono', monospace !important; font-size: 0.65rem !important; text-transform: uppercase !important; letter-spacing: 2px !important; color: var(--muted) !important; }
[data-testid="stMetricValue"] > div { font-size: 2.2rem !important; font-weight: 800 !important; color: var(--text) !important; letter-spacing: -1px !important; }

.stProgress > div > div > div > div { background: linear-gradient(90deg, var(--accent), var(--accent2)) !important; border-radius: 99px !important; }
.stProgress > div > div { background: var(--card2) !important; border-radius: 99px !important; height: 6px !important; }

.stSelectbox > div > div { background: var(--card2) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; color: var(--text) !important; }
hr { border-color: var(--border) !important; }

.feature-row { display: flex; gap: 1rem; margin-bottom: 2.5rem; flex-wrap: wrap; }
.feature-card { flex: 1; min-width: 180px; background: var(--card); border: 1px solid var(--border); border-radius: 16px; padding: 1.25rem 1.5rem; position: relative; overflow: hidden; transition: border-color 0.2s, transform 0.2s; }
.feature-card:hover { border-color: var(--border2); transform: translateY(-2px); }
.feature-icon { font-size: 1.4rem; margin-bottom: 0.6rem; }
.feature-title { font-size: 0.88rem; font-weight: 700; color: var(--text); margin-bottom: 0.3rem; }
.feature-desc { font-size: 0.78rem; font-weight: 300; color: var(--muted2); line-height: 1.55; }
.feature-card.cyan::after { content: ''; position: absolute; top: -20px; right: -20px; width: 80px; height: 80px; background: radial-gradient(circle, rgba(0,200,255,0.15), transparent 70%); border-radius: 50%; }
.feature-card.purple::after { content: ''; position: absolute; top: -20px; right: -20px; width: 80px; height: 80px; background: radial-gradient(circle, rgba(108,92,231,0.15), transparent 70%); border-radius: 50%; }
.feature-card.green::after { content: ''; position: absolute; top: -20px; right: -20px; width: 80px; height: 80px; background: radial-gradient(circle, rgba(0,229,160,0.15), transparent 70%); border-radius: 50%; }

.queue-panel { background: var(--card); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; height: 100%; min-height: 280px; }
.queue-panel-label { font-family: 'DM Mono', monospace; font-size: 0.62rem; text-transform: uppercase; letter-spacing: 2.5px; color: var(--muted); margin-bottom: 1rem; }
.queue-count { font-size: 2.2rem; font-weight: 800; color: var(--accent); letter-spacing: -1px; margin-top: 1.25rem; line-height: 1; }
.queue-count-lbl { font-family: 'DM Mono', monospace; font-size: 0.62rem; text-transform: uppercase; letter-spacing: 2px; color: var(--muted); margin-top: 4px; }

.library-banner { position: relative; width: 100%; height: 160px; border-radius: 20px; overflow: hidden; margin-bottom: 2rem; }
.library-banner-bg { position: absolute; inset: 0; background: linear-gradient(90deg, rgba(5,8,15,0.92) 40%, rgba(5,8,15,0.6) 100%), url('https://images.unsplash.com/photo-1587854692152-cbe660dbde88?w=1200&q=80&auto=format&fit=crop'); background-size: cover; background-position: center; }
.library-banner-content { position: relative; z-index: 2; padding: 1.75rem 2rem; }
.library-banner-title { font-size: 1.5rem; font-weight: 800; color: #fff; letter-spacing: -0.5px; margin-bottom: 0.3rem; }
.library-banner-sub { font-size: 0.85rem; font-weight: 300; color: rgba(255,255,255,0.5); }

.stat-strip { display: flex; gap: 1px; background: var(--border); border: 1px solid var(--border); border-radius: 16px; overflow: hidden; margin-bottom: 2rem; }
.stat-block { flex: 1; background: var(--card); padding: 1.25rem 1.5rem; }
.stat-val { font-size: 1.8rem; font-weight: 800; color: var(--accent); letter-spacing: -1px; line-height: 1; }
.stat-lbl { font-family: 'DM Mono', monospace; font-size: 0.62rem; text-transform: uppercase; letter-spacing: 2px; color: var(--muted); margin-top: 5px; }

.brief-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 0.9rem 1.1rem; margin-bottom: 0.4rem; }
.brief-card-name { font-weight: 600; font-size: 0.88rem; color: var(--text); }
.brief-card-meta { font-family: 'DM Mono', monospace; font-size: 0.62rem; color: var(--muted); margin-top: 2px; }

.upload-zone { background: var(--card); border: 1px dashed var(--border2); border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem; }
.upload-zone-label { font-family: 'DM Mono', monospace; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 2px; color: var(--muted); margin-bottom: 0.75rem; }

.empty-state { background: var(--card); border: 1px dashed var(--border2); border-radius: 20px; padding: 4rem 2rem; text-align: center; }
.empty-icon { font-size: 2.5rem; margin-bottom: 1rem; opacity: 0.4; }
.empty-title { font-size: 1.1rem; font-weight: 700; color: var(--muted2); margin-bottom: 0.4rem; }
.empty-desc { font-size: 0.85rem; color: var(--muted); font-weight: 300; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# MOLECULE SVG
# ─────────────────────────────────────────
MOLECULE_SVG = """
<svg width="280" height="280" viewBox="0 0 280 280" fill="none" xmlns="http://www.w3.org/2000/svg">
  <line x1="140" y1="60"  x2="210" y2="110" stroke="white" stroke-width="1.5"/>
  <line x1="210" y1="110" x2="210" y2="180" stroke="white" stroke-width="1.5"/>
  <line x1="210" y1="180" x2="140" y2="220" stroke="white" stroke-width="1.5"/>
  <line x1="140" y1="220" x2="70"  y2="180" stroke="white" stroke-width="1.5"/>
  <line x1="70"  y1="180" x2="70"  y2="110" stroke="white" stroke-width="1.5"/>
  <line x1="70"  y1="110" x2="140" y2="60"  stroke="white" stroke-width="1.5"/>
  <line x1="140" y1="60"  x2="140" y2="140" stroke="white" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="210" y1="110" x2="140" y2="140" stroke="white" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="210" y1="180" x2="140" y2="140" stroke="white" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="140" y1="220" x2="140" y2="140" stroke="white" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="70"  y1="180" x2="140" y2="140" stroke="white" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="70"  y1="110" x2="140" y2="140" stroke="white" stroke-width="1" stroke-dasharray="3 3"/>
  <circle cx="140" cy="60"  r="14" fill="white" fill-opacity="0.9"/>
  <circle cx="210" cy="110" r="11" fill="white" fill-opacity="0.7"/>
  <circle cx="210" cy="180" r="16" fill="white" fill-opacity="0.9"/>
  <circle cx="140" cy="220" r="11" fill="white" fill-opacity="0.7"/>
  <circle cx="70"  cy="180" r="13" fill="white" fill-opacity="0.85"/>
  <circle cx="70"  cy="110" r="11" fill="white" fill-opacity="0.7"/>
  <circle cx="140" cy="140" r="18" fill="white" fill-opacity="0.95"/>
  <text x="140" y="64"  text-anchor="middle" dominant-baseline="middle" fill="#05080f" font-size="9" font-weight="800" font-family="monospace">C</text>
  <text x="210" y="114" text-anchor="middle" dominant-baseline="middle" fill="#05080f" font-size="8" font-weight="800" font-family="monospace">N</text>
  <text x="210" y="184" text-anchor="middle" dominant-baseline="middle" fill="#05080f" font-size="9" font-weight="800" font-family="monospace">O</text>
  <text x="140" y="224" text-anchor="middle" dominant-baseline="middle" fill="#05080f" font-size="8" font-weight="800" font-family="monospace">H</text>
  <text x="70"  y="184" text-anchor="middle" dominant-baseline="middle" fill="#05080f" font-size="9" font-weight="800" font-family="monospace">C</text>
  <text x="70"  y="114" text-anchor="middle" dominant-baseline="middle" fill="#05080f" font-size="8" font-weight="800" font-family="monospace">N</text>
  <text x="140" y="144" text-anchor="middle" dominant-baseline="middle" fill="#05080f" font-size="11" font-weight="800" font-family="monospace">Rx</text>
</svg>
"""


# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-inner">
        <div class="logo-wrap">
            <div class="logo-icon">⬡</div>
            <div>
                <div class="logo-name">PharmAgent</div>
                <div class="logo-sub">AI Intelligence</div>
            </div>
        </div>
        <div class="live-badge">
            <div class="live-dot"></div>
            System Online
        </div>
        <div class="nav-label">Navigation</div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "nav",
        ["🔬  Generate Brief", "⚡  Batch Run", "📁  Saved Briefs"],
        label_visibility="collapsed"
    )

    brief_count = len(st.session_state.saved_briefs)
    st.markdown(f"""
        <div class="stack-wrap">
            <div class="stack-label">Session Library</div>
            <div style="font-size:1.8rem; font-weight:800; color:var(--accent); letter-spacing:-1px;">{brief_count}</div>
            <div style="font-family:'DM Mono',monospace; font-size:0.62rem; text-transform:uppercase; letter-spacing:2px; color:var(--muted); margin-bottom:1.25rem;">Briefs saved</div>
            <div class="stack-label">Powered by</div>
            <div class="stack-pill">⚡ Groq LLaMA 3.3</div>
            <div class="stack-pill">🔎 Tavily Search</div>
            <div class="stack-pill">🧠 RAG Pipeline</div>
        </div>
        <div class="footer-note">
            v1.0.0 · May 2026<br>
            Research use only
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# PAGE 1: GENERATE BRIEF
# Auto-saves every generated brief to session
# ─────────────────────────────────────────
if "Generate Brief" in page:

    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-bg"></div>
        <div class="molecule-wrap">{MOLECULE_SVG}</div>
        <div class="hero-content">
            <div class="hero-eyebrow">AI-Powered Pharma Intelligence</div>
            <h1 class="hero-h1">Competitive briefs,<br><span>generated instantly.</span></h1>
            <p class="hero-p">PharmAgent searches the web in real time, analyzes competitive landscapes, and writes strategic marketing briefs — in seconds, not days.</p>
            <div class="hero-stats">
                <div><div class="hero-stat-val">20<span>+</span></div><div class="hero-stat-lbl">Drugs analyzed</div></div>
                <div><div class="hero-stat-val">&lt;30<span>s</span></div><div class="hero-stat-lbl">Per brief</div></div>
                <div><div class="hero-stat-val">100<span>%</span></div><div class="hero-stat-lbl">AI-generated</div></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="content-area">
        <div class="feature-row">
            <div class="feature-card cyan"><div class="feature-icon">🔎</div><div class="feature-title">Live Web Research</div><div class="feature-desc">Searches the web in real time for pricing, positioning, and competitor moves.</div></div>
            <div class="feature-card purple"><div class="feature-icon">🧠</div><div class="feature-title">LLM Synthesis</div><div class="feature-desc">Groq LLaMA 3.3 processes raw data into structured, actionable strategy briefs.</div></div>
            <div class="feature-card green"><div class="feature-icon">📄</div><div class="feature-title">Export Ready</div><div class="feature-desc">Download as .txt — every brief is also auto-saved to your session library.</div></div>
        </div>
        <div class="search-card">
            <div class="search-card-label">Enter drug name to analyze</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1])
    with col1:
        drug_name = st.text_input(
            "drug",
            placeholder="e.g. Ozempic, Keytruda, Humira, Jardiance, Wegovy...",
            label_visibility="collapsed"
        )
    with col2:
        generate = st.button("Generate →", use_container_width=True, type="primary")

    st.markdown("</div>", unsafe_allow_html=True)

    if generate and drug_name:
        start = time.time()
        with st.status(f"⬡  Analyzing {drug_name}...", expanded=True) as status:
            st.write("🔎  Scanning the web for competitive intelligence...")
            summary, raw_search = research_drug(drug_name)
            st.write("🧠  Writing your strategic marketing brief...")
            brief = write_marketing_brief(drug_name, raw_search)
            elapsed = round(time.time() - start, 1)
            status.update(label=f"✓  Brief ready · {elapsed}s", state="complete")

        # AUTO-SAVE to session state
        st.session_state.saved_briefs[drug_name.title()] = brief
        st.success(f"✓ Brief auto-saved to library — {len(st.session_state.saved_briefs)} brief(s) total. View them in 'Saved Briefs'.")

        word_count = len(brief.split())
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:0.5rem; margin-top:1rem; margin-bottom:0.75rem; flex-wrap:wrap;">
            <span style="font-size:1rem; font-weight:700; color:var(--text); margin-right:0.5rem;">{drug_name} — Strategic Brief</span>
            <span class="chip">{word_count} words</span>
            <span class="chip chip-green">✓ Saved</span>
            <span class="chip chip-purple">{elapsed}s</span>
        </div>
        """, unsafe_allow_html=True)

        st.text_area("brief", value=brief, height=500, label_visibility="collapsed")

        col_dl, _ = st.columns([2, 5])
        with col_dl:
            st.download_button(
                label="⬇  Download .txt",
                data=brief.encode("utf-8"),
                file_name=f"{drug_name.lower().replace(' ', '_')}_brief.txt",
                mime="text/plain",
                use_container_width=True
            )

    elif generate and not drug_name:
        st.warning("Please enter a drug name to continue.")

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────
# PAGE 2: BATCH RUN
# Empty by default — user types their own list
# All generated briefs auto-saved to session
# ─────────────────────────────────────────
elif "Batch Run" in page:

    st.markdown("""
    <div class="hero-banner" style="min-height:220px;">
        <div class="hero-bg" style="background: linear-gradient(to right, rgba(5,8,15,0.97) 35%, rgba(5,8,15,0.7) 100%), url('https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=1600&q=80&auto=format&fit=crop'); background-size:cover; background-position:center;"></div>
        <div class="hero-content">
            <div class="hero-eyebrow">Portfolio Engine</div>
            <h1 class="hero-h1" style="font-size:2.2rem;">Batch generate<br><span>your brief library</span></h1>
            <p class="hero-p" style="margin-bottom:0;">All generated briefs are automatically saved to your session library.</p>
        </div>
    </div>
    <div class="content-area">
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('<div class="pg-eyebrow">Drug Queue</div>', unsafe_allow_html=True)
        drug_input = st.text_area(
            "Enter one drug per line",
            value="",   # EMPTY — no pre-filled defaults
            placeholder="Xarelto\nStelara\nSkyrizi\nTremfya\nTaltz\nCosentyx\n...",
            height=290
        )
    with col2:
        drug_list = [d.strip() for d in drug_input.strip().split("\n") if d.strip()]
        chips = "".join(f'<span class="chip" style="margin:2px;">{d}</span>' for d in drug_list[:20]) if drug_list else '<span style="color:var(--muted); font-size:0.8rem;">Type drugs on the left to preview</span>'
        st.markdown(f"""
        <div class="queue-panel">
            <div class="queue-panel-label">⬡ Queue Preview</div>
            {chips}
            <div class="queue-count">{len(drug_list)}</div>
            <div class="queue-count-lbl">Drugs queued</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚡  Run Batch Pipeline", type="primary"):
        if not drug_list:
            st.warning("Please enter at least one drug name above.")
        else:
            results = []
            progress = st.progress(0, text="Initializing batch pipeline...")
            log = st.empty()

            for i, drug in enumerate(drug_list):
                log.info(f"Processing {drug}  ({i+1} of {len(drug_list)})...")
                try:
                    summary, raw_search = research_drug(drug)
                    brief = write_marketing_brief(drug, raw_search)

                    # AUTO-SAVE each brief to session
                    st.session_state.saved_briefs[drug.title()] = brief

                    results.append({"drug": drug, "status": "success"})
                    log.success(f"✓  {drug} — saved to library")
                except Exception as e:
                    results.append({"drug": drug, "status": "failed", "error": str(e)})
                    log.error(f"✗  {drug} failed — {str(e)[:80]}")

                progress.progress((i + 1) / len(drug_list), text=f"{i+1} / {len(drug_list)} complete")
                time.sleep(2)

            st.divider()
            successful = [r for r in results if r["status"] == "success"]
            failed = [r for r in results if r["status"] == "failed"]
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Queued", len(drug_list))
            col2.metric("Saved to Library", len(successful))
            col3.metric("Failed", len(failed))
            if successful:
                st.success(f"✓ {len(successful)} briefs saved — go to 'Saved Briefs' to view them")
            if failed:
                st.error("Failed (likely rate limit — try tomorrow): " + "  ·  ".join(r["drug"] for r in failed))

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────
# PAGE 3: SAVED BRIEFS
# Shows all session briefs
# Upload your local 7 .txt files here too
# ─────────────────────────────────────────
elif "Saved Briefs" in page:

    st.markdown('<div class="content-area">', unsafe_allow_html=True)

    st.markdown("""
    <div class="library-banner">
        <div class="library-banner-bg"></div>
        <div class="library-banner-content">
            <div class="library-banner-title">📁 Brief Library</div>
            <div class="library-banner-sub">Your competitive intelligence portfolio — current session</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # UPLOAD ZONE — paste your 7 local .txt briefs here
    st.markdown("""
    <div class="upload-zone">
        <div class="upload-zone-label">📂 Upload your existing brief files — drag your 7 local .txt files here to add them to this session</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Upload .txt brief files",
        type=["txt"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    if uploaded_files:
        newly_added = []
        for uf in uploaded_files:
            drug_label = uf.name.replace("_brief.txt", "").replace("_", " ").title()
            content = uf.read().decode("utf-8")
            if drug_label not in st.session_state.saved_briefs:
                st.session_state.saved_briefs[drug_label] = content
                newly_added.append(drug_label)
        if newly_added:
            st.success(f"✓ Added {len(newly_added)} brief(s) to library: {', '.join(newly_added)}")

    st.divider()

    briefs = st.session_state.saved_briefs

    if not briefs:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🗂️</div>
            <div class="empty-title">No briefs in the library yet</div>
            <div class="empty-desc">Generate a brief, run a batch, or upload your 7 existing .txt files above.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        total_words = sum(len(v.split()) for v in briefs.values())
        avg_words = total_words // len(briefs)

        st.markdown(f"""
        <div class="stat-strip">
            <div class="stat-block"><div class="stat-val">{len(briefs)}</div><div class="stat-lbl">Briefs in library</div></div>
            <div class="stat-block"><div class="stat-val">{total_words:,}</div><div class="stat-lbl">Total words</div></div>
            <div class="stat-block"><div class="stat-val">{avg_words}</div><div class="stat-lbl">Avg words / brief</div></div>
        </div>
        """, unsafe_allow_html=True)

        selected = st.selectbox(
            "Choose a brief to view",
            options=list(briefs.keys()),
        )

        if selected:
            content = briefs[selected]
            word_count = len(content.split())

            st.markdown(f"""
            <div style="display:flex; gap:0.4rem; margin:1rem 0 0.75rem; flex-wrap:wrap;">
                <span class="chip">{selected}</span>
                <span class="chip chip-green">{word_count} words</span>
                <span class="chip chip-purple">✓ In library</span>
            </div>
            """, unsafe_allow_html=True)

            st.text_area("content", value=content, height=500, label_visibility="collapsed")

            col1, col2 = st.columns([2, 5])
            with col1:
                st.download_button(
                    label="⬇  Download this brief",
                    data=content.encode("utf-8"),
                    file_name=f"{selected.lower().replace(' ', '_')}_brief.txt",
                    mime="text/plain",
                    use_container_width=True
                )

        # Grid of all briefs
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<div class="pg-eyebrow">All {len(briefs)} briefs in library</div>', unsafe_allow_html=True)
        cols = st.columns(4)
        for i, name in enumerate(sorted(briefs.keys())):
            with cols[i % 4]:
                st.markdown(f"""
                <div class="brief-card">
                    <div class="brief-card-name">{name}</div>
                    <div class="brief-card-meta">{len(briefs[name].split())} words</div>
                </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)