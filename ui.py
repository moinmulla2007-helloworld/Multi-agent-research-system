import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dossier · Research Agent",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,400;0,500;0,600;1,400&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Newsreader', Georgia, serif;
    color: #2b271f;
}

.stApp {
    background: #f6f2e9;
    background-image:
        repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(43,39,31,0.035) 40px);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.2rem 3.5rem 5rem; max-width: 1100px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #eee7d6;
    border-right: 2px solid #2b271f;
}
section[data-testid="stSidebar"] .block-container { padding-top: 2.4rem; }

.brand {
    font-family: 'Space Mono', monospace;
    font-size: 1.05rem;
    font-weight: 700;
    color: #2b271f;
    letter-spacing: 0.02em;
    text-transform: uppercase;
    border-bottom: 3px solid #b5482a;
    display: inline-block;
    padding-bottom: 0.2rem;
    margin-bottom: 0.4rem;
}
.brand-tag {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #7a725e;
    margin-bottom: 2.2rem;
}

.sidebar-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #b5482a;
    margin: 1.8rem 0 0.6rem;
}
.sidebar-label::before { content: "§ "; }

section[data-testid="stSidebar"] .stTextArea textarea {
    background: #f6f2e9 !important;
    border: 1.5px solid #2b271f !important;
    border-radius: 0px !important;
    color: #2b271f !important;
    font-family: 'Newsreader', serif !important;
    font-size: 0.98rem !important;
    box-shadow: 3px 3px 0px rgba(43,39,31,0.15) !important;
}
section[data-testid="stSidebar"] .stTextArea textarea:focus {
    border-color: #b5482a !important;
    box-shadow: 3px 3px 0px rgba(181,72,42,0.25) !important;
}

section[data-testid="stSidebar"] .stButton > button {
    background: #2b271f !important;
    color: #f6f2e9 !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border: 1.5px solid #2b271f !important;
    border-radius: 0px !important;
    padding: 0.7rem 1rem !important;
    width: 100%;
    transition: all 0.12s !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: #b5482a !important;
    border-color: #b5482a !important;
    transform: translate(-2px, -2px) !important;
    box-shadow: 3px 3px 0px #2b271f !important;
}

.chip-row { display:flex; flex-direction: column; gap:0.5rem; margin-top:0.6rem; }
.chip {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #4a4536;
    background: transparent;
    border-left: 2px solid #b5482a;
    padding: 0.2rem 0 0.2rem 0.6rem;
}

.pipeline-list {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #4a4536;
    line-height: 2.1;
}
.pipeline-list b { color: #2b271f; }

/* ── Main header ── */
.masthead {
    border-bottom: 3px double #2b271f;
    padding-bottom: 0.9rem;
    margin-bottom: 1.6rem;
}
.masthead-top {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #7a725e;
    margin-bottom: 0.5rem;
}
.main-title {
    font-family: 'Newsreader', serif;
    font-size: 2.6rem;
    font-weight: 600;
    font-style: italic;
    color: #2b271f;
    line-height: 1.1;
}
.main-topic {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    color: #b5482a;
    margin-top: 0.5rem;
}
.main-sub {
    font-size: 1rem;
    color: #5c563f;
    font-style: italic;
    margin-top: 0.4rem;
}

/* ── Ledger-style pipeline tracker ── */
.log-line {
    display: flex;
    align-items: baseline;
    gap: 1rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    padding: 0.65rem 0.1rem;
    border-bottom: 1px dashed #cfc6ac;
}
.log-marker {
    width: 16px; text-align: center; flex-shrink: 0;
    font-size: 0.9rem;
    color: #cfc6ac;
}
.log-line.running .log-marker { color: #b5482a; animation: blink 1s infinite; }
.log-line.done .log-marker { color: #2b271f; }
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.25;} }

.log-step { color: #a89f84; min-width: 22px; }
.log-name { color: #2b271f; min-width: 150px; font-weight: 700; }
.log-detail { color: #7a725e; flex: 1; font-style: italic; }
.log-status { min-width: 75px; text-align: right; letter-spacing: 0.06em; text-transform: uppercase; font-size: 0.7rem; }
.log-line.waiting .log-status { color: #cfc6ac; }
.log-line.running .log-status { color: #b5482a; }
.log-line.done .log-status { color: #2b271f; }

/* ── Result tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: transparent;
    border-bottom: 2px solid #2b271f;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Space Mono', monospace;
    font-size: 0.74rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #7a725e;
    background: transparent;
    border: none;
    padding: 0.7rem 1.4rem;
}
.stTabs [aria-selected="true"] {
    color: #f6f2e9 !important;
    background: #2b271f !important;
}

.content-block {
    background: #fffdf6;
    border: 1.5px solid #2b271f;
    padding: 2rem 2.4rem;
    margin-top: 1.4rem;
    font-size: 1.02rem;
    line-height: 1.8;
    color: #2b271f;
    box-shadow: 5px 5px 0px rgba(43,39,31,0.08);
}
.content-block.accent-rust { border-left: 5px solid #b5482a; }
.content-block.accent-ink { border-left: 5px solid #2b271f; }

.raw-block {
    background: #eee7d6;
    border: 1px solid #cfc6ac;
    padding: 1.5rem 1.7rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.76rem;
    line-height: 1.75;
    color: #4a4536;
    white-space: pre-wrap;
    max-height: 440px;
    overflow-y: auto;
}

.empty-state {
    text-align: center;
    padding: 5.5rem 2rem;
    color: #a89f84;
    border: 1.5px dashed #cfc6ac;
    margin-top: 1rem;
}
.empty-state .glyph { font-size: 2rem; margin-bottom: 1rem; color: #b5482a; }
.empty-state .msg { font-family: 'Space Mono', monospace; font-size: 0.82rem; letter-spacing: 0.03em; }

.stSpinner > div { color: #b5482a !important; }

.footer-note {
    font-family: 'Space Mono', monospace;
    font-size: 0.66rem;
    color: #a89f84;
    text-align: center;
    margin-top: 3.5rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    border-top: 1px solid #cfc6ac;
    padding-top: 1.2rem;
}

[data-testid="stDownloadButton"] button {
    background: #fffdf6 !important;
    color: #2b271f !important;
    border: 1.5px solid #2b271f !important;
    border-radius: 0 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.74rem !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
[data-testid="stDownloadButton"] button:hover {
    background: #b5482a !important;
    border-color: #b5482a !important;
    color: #fffdf6 !important;
}
</style>
""", unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key, default in (("results", {}), ("running", False), ("done", False), ("topic_run", "")):
    if key not in st.session_state:
        st.session_state[key] = default


# ── Sidebar: input ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="brand">Dossier</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-tag">Field Notes from Four Agents</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">Research Topic</div>', unsafe_allow_html=True)
    topic = st.text_area(
        "Research Topic",
        placeholder="e.g. Fusion energy breakthroughs in 2026",
        height=90,
        label_visibility="collapsed",
        key="topic_input",
    )
    run_btn = st.button("Open the case →", use_container_width=True)

    st.markdown('<div class="sidebar-label">Try instead</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="chip-row">
        <span class="chip">LLM agents 2026</span>
        <span class="chip">CRISPR ethics</span>
        <span class="chip">EV battery costs</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">The Process</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="pipeline-list">
        <b>I.</b>&nbsp; Search Agent<br>
        <b>II.</b>&nbsp; Reader Agent<br>
        <b>III.</b>&nbsp; Writer Chain<br>
        <b>IV.</b>&nbsp; Critic Chain
    </div>
    """, unsafe_allow_html=True)


# ── Main header ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="masthead">
    <div class="masthead-top">
        <span>Vol. I — The Research Desk</span>
        <span>{time.strftime("%d %b %Y")}</span>
    </div>
    <div class="main-title">Research Console</div>
    {'<div class="main-topic">ON THE SUBJECT OF: ' + st.session_state.topic_run.upper() + '</div>' if st.session_state.topic_run else ''}
    <div class="main-sub">Four correspondents, one dispatch: search, read, write, critique.</div>
</div>
""", unsafe_allow_html=True)


# ── Trigger run ───────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.session_state.topic_run = topic.strip()
        st.rerun()


# ── Pipeline log tracker ─────────────────────────────────────────────────────
steps = [
    ("I", "search", "Search Agent", "gathering recent web sources"),
    ("II", "reader", "Reader Agent", "scraping top result for depth"),
    ("III", "writer", "Writer Chain", "drafting structured report"),
    ("IV", "critic", "Critic Chain", "scoring and reviewing"),
]

def step_state(key):
    r = st.session_state.results
    if key in r:
        return "done"
    if st.session_state.running:
        for _, k, _, _ in steps:
            if k not in r:
                return "running" if k == key else "waiting"
    return "waiting"

log_placeholder = st.empty()

def render_log():
    rows = []
    for num, key, name, detail in steps:
        state = step_state(key)
        marker = {"waiting": "○", "running": "●", "done": "✦"}[state]
        label = {"waiting": "pending", "running": "in progress", "done": "filed"}[state]
        rows.append(f"""
        <div class="log-line {state}">
            <span class="log-marker">{marker}</span>
            <span class="log-step">{num}.</span>
            <span class="log-name">{name}</span>
            <span class="log-detail">{detail}</span>
            <span class="log-status">{label}</span>
        </div>
        """)
    log_placeholder.markdown("".join(rows), unsafe_allow_html=True)

render_log()


# ── Run pipeline ──────────────────────────────────────────────────────────────
if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_run

    with st.spinner("Search Agent is working…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)
        render_log()

    with st.spinner("Reader Agent is scraping top resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)
        render_log()

    with st.spinner("Writer Chain is drafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)
        render_log()

    with st.spinner("Critic Chain is reviewing the report…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)
        render_log()

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results ───────────────────────────────────────────────────────────────────
r = st.session_state.results

if r and "writer" in r:
    tab_report, tab_critic, tab_raw = st.tabs(["The Report", "Editor's Notes", "Correspondence"])

    with tab_report:
        st.markdown('<div class="content-block accent-rust">', unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown('</div>', unsafe_allow_html=True)
        st.download_button(
            label="Download report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    with tab_critic:
        if "critic" in r:
            st.markdown('<div class="content-block accent-ink">', unsafe_allow_html=True)
            st.markdown(r["critic"])
            st.markdown('</div>', unsafe_allow_html=True)

    with tab_raw:
        if "search" in r:
            st.markdown('<div class="sidebar-label">Search Agent Output</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="raw-block">{r["search"]}</div>', unsafe_allow_html=True)
        if "reader" in r:
            st.markdown('<div class="sidebar-label">Reader Agent Output</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="raw-block">{r["reader"]}</div>', unsafe_allow_html=True)

elif not st.session_state.running:
    st.markdown("""
    <div class="empty-state">
        <div class="glyph">✦</div>
        <div class="msg">Enter a topic in the margin and open the case to see the dossier here.</div>
    </div>
    """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-note">Dossier · Langchain Multi-Agent Pipeline · Streamlit</div>
""", unsafe_allow_html=True)