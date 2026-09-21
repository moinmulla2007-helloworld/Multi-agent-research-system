import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multiagent · Research Agent",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@300;400;500;600&family=Inter:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #dcd9f0;
}

.stApp {
    background: #08080c;
    background-image:
        radial-gradient(ellipse 70% 50% at 85% -5%, rgba(120,90,255,0.14) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 5% 100%, rgba(40,220,190,0.08) 0%, transparent 55%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 3rem 4rem; max-width: 1180px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0c0c13;
    border-right: 1px solid rgba(140,120,255,0.12);
}
section[data-testid="stSidebar"] .block-container { padding-top: 2rem; }

.brand {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #f2f0fa;
    letter-spacing: -0.01em;
    margin-bottom: 0.1rem;
}
.brand span { color: #8b7bff; }
.brand-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #5a5670;
    margin-bottom: 2rem;
}

.sidebar-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #8b7bff;
    margin: 1.6rem 0 0.6rem;
}

section[data-testid="stSidebar"] .stTextArea textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(140,120,255,0.2) !important;
    border-radius: 8px !important;
    color: #f2f0fa !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
}
section[data-testid="stSidebar"] .stTextArea textarea:focus {
    border-color: #8b7bff !important;
    box-shadow: 0 0 0 3px rgba(139,123,255,0.15) !important;
}

section[data-testid="stSidebar"] .stButton > button {
    background: #8b7bff !important;
    color: #08080c !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.65rem 1rem !important;
    width: 100%;
    transition: background 0.15s, transform 0.15s !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: #a094ff !important;
    transform: translateY(-1px) !important;
}

.chip-row { display:flex; flex-wrap:wrap; gap:0.4rem; margin-top:0.8rem; }
.chip {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: #9490b0;
    background: rgba(140,120,255,0.08);
    border: 1px solid rgba(140,120,255,0.15);
    border-radius: 20px;
    padding: 0.3rem 0.75rem;
}

/* ── Main header ── */
.main-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.3rem;
}
.main-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: #f2f0fa;
}
.main-topic {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #6ee7c9;
}
.main-sub {
    font-size: 0.92rem;
    color: #75718f;
    margin-bottom: 1.8rem;
}

/* ── Log-style pipeline tracker ── */
.log-line {
    display: flex;
    align-items: center;
    gap: 0.9rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    padding: 0.55rem 0.2rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.log-dot {
    width: 8px; height: 8px; border-radius: 50%;
    flex-shrink: 0;
    background: #333047;
}
.log-line.running .log-dot { background: #8b7bff; box-shadow: 0 0 8px rgba(139,123,255,0.7); animation: pulse 1.2s infinite; }
.log-line.done .log-dot { background: #6ee7c9; }
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.35;} }

.log-step { color: #5a5670; min-width: 20px; }
.log-name { color: #cbc8e0; min-width: 150px; }
.log-detail { color: #55516c; flex: 1; }
.log-status { min-width: 70px; text-align: right; }
.log-line.waiting .log-status { color: #3c3950; }
.log-line.running .log-status { color: #8b7bff; }
.log-line.done .log-status { color: #6ee7c9; }

/* ── Result tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.3rem;
    background: transparent;
    border-bottom: 1px solid rgba(140,120,255,0.15);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.05em;
    color: #75718f;
    background: transparent;
    border-radius: 6px 6px 0 0;
    padding: 0.6rem 1.2rem;
}
.stTabs [aria-selected="true"] {
    color: #8b7bff !important;
    background: rgba(139,123,255,0.08) !important;
}

.content-block {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 1.8rem 2rem;
    margin-top: 1.2rem;
    font-size: 0.92rem;
    line-height: 1.75;
    color: #cbc8e0;
}
.content-block.accent-violet { border-color: rgba(139,123,255,0.25); }
.content-block.accent-teal { border-color: rgba(110,231,201,0.25); }
.raw-block {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    line-height: 1.7;
    color: #9490b0;
    white-space: pre-wrap;
    max-height: 420px;
    overflow-y: auto;
}

.empty-state {
    text-align: center;
    padding: 5rem 2rem;
    color: #454258;
}
.empty-state .glyph { font-size: 2.2rem; margin-bottom: 1rem; color: #8b7bff; opacity: 0.6; }
.empty-state .msg { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; }

.stSpinner > div { color: #8b7bff !important; }

.footer-note {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: #3c3950;
    text-align: center;
    margin-top: 3.5rem;
    letter-spacing: 0.1em;
}
</style>
""", unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key, default in (("results", {}), ("running", False), ("done", False), ("topic_run", "")):
    if key not in st.session_state:
        st.session_state[key] = default


# ── Sidebar: input ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="brand">Multiagent<span>.</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-tag">Multi-Agent Research Console</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">Research Topic</div>', unsafe_allow_html=True)
    topic = st.text_area(
        "Research Topic",
        placeholder="e.g. Fusion energy breakthroughs in 2026",
        height=90,
        label_visibility="collapsed",
        key="topic_input",
    )
    run_btn = st.button("Run pipeline →", use_container_width=True)

    st.markdown('<div class="sidebar-label">Try instead</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="chip-row">
        <span class="chip">LLM agents 2026</span>
        <span class="chip">CRISPR ethics</span>
        <span class="chip">EV battery costs</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">Pipeline</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#5a5670; line-height:2;">
        01 · search agent<br>
        02 · reader agent<br>
        03 · writer chain<br>
        04 · critic chain
    </div>
    """, unsafe_allow_html=True)


# ── Main header ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="main-header">
    <div class="main-title">Research Console</div>
    {'<div class="main-topic">' + st.session_state.topic_run + '</div>' if st.session_state.topic_run else ''}
</div>
<div class="main-sub">Four agents run in sequence: search → read → write → critique.</div>
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
    ("01", "search", "Search Agent", "gathering recent web sources"),
    ("02", "reader", "Reader Agent", "scraping top result for depth"),
    ("03", "writer", "Writer Chain", "drafting structured report"),
    ("04", "critic", "Critic Chain", "scoring and reviewing"),
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
        label = {"waiting": "waiting", "running": "running…", "done": "done"}[state]
        rows.append(f"""
        <div class="log-line {state}">
            <span class="log-dot"></span>
            <span class="log-step">{num}</span>
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
    tab_report, tab_critic, tab_raw = st.tabs(["◆ Report", "◇ Critic Feedback", "⌁ Raw Agent Output"])

    with tab_report:
        st.markdown('<div class="content-block accent-violet">', unsafe_allow_html=True)
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
            st.markdown('<div class="content-block accent-teal">', unsafe_allow_html=True)
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
        <div class="glyph">◆</div>
        <div class="msg">Enter a topic in the sidebar and run the pipeline to see results here.</div>
    </div>
    """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-note">NYRA · LANGCHAIN MULTI-AGENT PIPELINE · STREAMLIT</div>
""", unsafe_allow_html=True)