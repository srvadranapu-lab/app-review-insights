import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from app.ingestion import fetch_all_reviews
from app.database import db
from app.processing import load_reviews, filter_reviews, prepare_llm_input, save_processed_reviews
from app.summarize import generate_summary
from app.render import load_summary, generate_report, generate_email, save_report, save_email
from app.publish_docs import publish_to_docs
from app.publish_email import publish_email

st.set_page_config(
    page_title="Groww · Review Insights",
    page_icon="📊",
    layout="wide"
)

# ─── Global Styles ────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

  /* ── Base reset ── */
  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
  }

  /* ── App background ── */
  .stApp {
    background: #f7f9f7;
  }

  /* ── Hide default Streamlit header chrome ── */
  #MainMenu, footer, header { visibility: hidden; }

  /* ── Custom top navbar ── */
  .groww-navbar {
    background: #fff;
    border-bottom: 1.5px solid #e6ede6;
    padding: 18px 36px;
    display: flex;
    align-items: center;
    gap: 14px;
    position: sticky;
    top: 0;
    z-index: 100;
    margin: -1rem -1rem 2rem -1rem;
  }
  .groww-logo-mark {
    width: 36px;
    height: 36px;
    background: #00d09c;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    font-weight: 700;
    color: #fff;
    letter-spacing: -1px;
    flex-shrink: 0;
  }
  .groww-title {
    font-size: 20px;
    font-weight: 700;
    color: #0d1117;
    letter-spacing: -0.4px;
  }
  .groww-subtitle {
    font-size: 13px;
    font-weight: 500;
    color: #7a8b7a;
    letter-spacing: 0.2px;
    margin-top: 1px;
  }
  .groww-badge {
    margin-left: auto;
    background: #e8faf4;
    color: #00b386;
    border: 1.5px solid #b3edd9;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.3px;
  }

  /* ── Section labels ── */
  .section-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #7a8b7a;
    margin-bottom: 14px;
    margin-top: 8px;
  }

  /* ── Pipeline cards ── */
  .pipeline-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 28px;
  }
  .pipeline-card {
    background: #fff;
    border: 1.5px solid #e6ede6;
    border-radius: 16px;
    padding: 22px 20px 18px;
    transition: box-shadow 0.2s, border-color 0.2s;
    cursor: default;
  }
  .pipeline-card:hover {
    box-shadow: 0 4px 24px rgba(0, 208, 156, 0.10);
    border-color: #b3edd9;
  }
  .card-step-num {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #00b386;
    margin-bottom: 4px;
  }
  .card-title {
    font-size: 15px;
    font-weight: 700;
    color: #0d1117;
    margin-bottom: 4px;
    letter-spacing: -0.2px;
  }
  .card-desc {
    font-size: 12.5px;
    color: #7a8b7a;
    line-height: 1.5;
  }

  /* ── Streamlit button override ── */
  div.stButton > button {
    background: #00d09c !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 22px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    letter-spacing: 0.1px !important;
    transition: background 0.18s, transform 0.12s, box-shadow 0.18s !important;
    box-shadow: 0 2px 10px rgba(0, 208, 156, 0.25) !important;
    width: 100% !important;
    margin-top: 10px !important;
  }
  div.stButton > button:hover {
    background: #00b386 !important;
    box-shadow: 0 4px 18px rgba(0, 208, 156, 0.35) !important;
    transform: translateY(-1px) !important;
  }
  div.stButton > button:active {
    transform: translateY(0px) !important;
    background: #009e78 !important;
  }

  /* ── Danger / secondary buttons (Send Email) ── */
  div[data-testid="column"]:last-child div.stButton > button {
    background: #fff !important;
    color: #00b386 !important;
    border: 1.5px solid #00d09c !important;
    box-shadow: none !important;
  }
  div[data-testid="column"]:last-child div.stButton > button:hover {
    background: #e8faf4 !important;
  }

  /* ── Output panels ── */
  .output-panel {
    background: #fff;
    border: 1.5px solid #e6ede6;
    border-radius: 16px;
    padding: 24px 26px;
    margin-bottom: 18px;
  }
  .output-panel-title {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.3px;
    color: #0d1117;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1.5px solid #f0f5f0;
  }
  .output-icon {
    width: 28px;
    height: 28px;
    background: #e8faf4;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
  }

  /* ── Spinner override ── */
  .stSpinner > div {
    border-top-color: #00d09c !important;
  }

  /* ── Success / info / error messages ── */
  .stSuccess {
    background: #e8faf4 !important;
    border-left: 3px solid #00d09c !important;
    border-radius: 8px !important;
    color: #006b55 !important;
    font-weight: 500 !important;
  }
  .stInfo {
    background: #f7f9f7 !important;
    border-left: 3px solid #b3edd9 !important;
    border-radius: 8px !important;
    color: #5a6e5a !important;
  }

  /* ── Divider ── */
  .custom-divider {
    height: 1.5px;
    background: linear-gradient(90deg, #e6ede6 0%, #b3edd9 50%, #e6ede6 100%);
    border: none;
    margin: 28px 0;
    border-radius: 2px;
  }

  /* ── Text area (report) ── */
  .stTextArea textarea, pre {
    font-family: 'DM Mono', monospace !important;
    font-size: 12.5px !important;
    background: #f7f9f7 !important;
    border-radius: 10px !important;
    border-color: #e6ede6 !important;
    color: #2c3e2c !important;
  }
</style>
""", unsafe_allow_html=True)

# ─── Navbar ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="groww-navbar">
  <div class="groww-logo-mark">G</div>
  <div>
    <div class="groww-title">Groww</div>
    <div class="groww-subtitle">Review Insights Analyser</div>
  </div>
  <div class="groww-badge">📊 Analytics Pipeline</div>
</div>
""", unsafe_allow_html=True)

# ─── Session State ─────────────────────────────────────────────────────────────
if "render_success" not in st.session_state:
    st.session_state.render_success = False

# ─── Pipeline Step Cards ───────────────────────────────────────────────────────
st.markdown('<div class="section-label">Pipeline Steps</div>', unsafe_allow_html=True)

st.markdown("""
<div class="pipeline-grid">
  <div class="pipeline-card">
    <div class="card-step-num">Step 01</div>
    <div class="card-title">Ingest Reviews</div>
    <div class="card-desc">Fetch latest Groww app reviews and store them in the database.</div>
  </div>
  <div class="pipeline-card">
    <div class="card-step-num">Step 02</div>
    <div class="card-title">Process Reviews</div>
    <div class="card-desc">Filter, clean, and prepare reviews for LLM summarisation.</div>
  </div>
  <div class="pipeline-card">
    <div class="card-step-num">Step 03</div>
    <div class="card-title">Generate Insights</div>
    <div class="card-desc">Run the LLM to extract themes, quotes, and action items.</div>
  </div>
  <div class="pipeline-card">
    <div class="card-step-num">Step 04</div>
    <div class="card-title">Generate Report</div>
    <div class="card-desc">Produce a formatted report and ready-to-send email draft.</div>
  </div>
  <div class="pipeline-card">
    <div class="card-step-num">Step 05</div>
    <div class="card-title">Publish to Docs</div>
    <div class="card-desc">Push the report to a Google Doc and get a shareable link.</div>
  </div>
  <div class="pipeline-card">
    <div class="card-step-num">Step 06</div>
    <div class="card-title">Send Email</div>
    <div class="card-desc">Open Gmail with a pre-composed insights email ready to send.</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Action Buttons (2 rows × 3 columns) ─────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⬇️  Run Ingestion"):
        with st.spinner("Fetching reviews..."):
            reviews = fetch_all_reviews("groww")
            st.success(f"✓ Fetched {len(reviews)} reviews")
        with st.spinner("Inserting into database..."):
            inserted_count = db.insert_reviews(reviews)
            st.success(f"✓ Inserted {inserted_count} new reviews")

with col2:
    if st.button("⚙️  Process Reviews"):
        with st.spinner("Loading reviews..."):
            reviews = load_reviews("groww")
            st.success(f"✓ Loaded {len(reviews)} reviews")
        with st.spinner("Filtering..."):
            filtered_reviews = filter_reviews(reviews)
            st.success(f"✓ After filtering: {len(filtered_reviews)} reviews")
        with st.spinner("Preparing LLM input..."):
            llm_input = prepare_llm_input(filtered_reviews)
            st.success(f"✓ Prepared {len(llm_input)} reviews for LLM")
        with st.spinner("Saving..."):
            save_processed_reviews(llm_input)
            st.success("✓ Saved to data/processed_reviews.json")

with col3:
    if st.button("🧠  Generate Insights"):
        with st.spinner("Generating insights with LLM..."):
            result = generate_summary()
            if result:
                st.success(f"✓ {len(result.get('themes', []))} themes identified")
                st.success(f"✓ {len(result.get('quotes', []))} valid quotes found")
                st.success(f"✓ {len(result.get('actions', []))} action ideas created")

col4, col5, col6 = st.columns(3)

with col4:
    if st.button("📄  Generate Report"):
        with st.spinner("Loading summary..."):
            summary = load_summary()
            if not summary:
                st.error("No summary found. Run 'Generate Insights' first.")
                st.session_state.render_success = False
            else:
                st.success("✓ Summary loaded")
        if summary:
            with st.spinner("Building report..."):
                report = generate_report(summary, "Groww")
                save_report(report)
                st.success("✓ Report saved to data/report.txt")
            with st.spinner("Drafting email..."):
                subject, body = generate_email(summary, "Groww")
                save_email(subject, body)
                st.success("✓ Email saved to data/email.html")
            st.session_state.render_success = True

with col5:
    if st.button("☁️  Publish to Google Docs"):
        with st.spinner("Publishing..."):
            doc_link = publish_to_docs()
            if doc_link:
                st.success(f"✓ Published to Google Docs")
                st.markdown(f"[Open Document →]({doc_link})")
            else:
                st.error("Failed to publish to Google Docs")

with col6:
    if st.button("✉️  Send Email"):
        with st.spinner("Generating Gmail link..."):
            gmail_url = publish_email()
            if gmail_url:
                st.success("✓ Gmail compose link ready!")
                st.markdown(f"[Open Gmail Compose →]({gmail_url})")
            else:
                st.error("Failed to generate Gmail compose link")

# ─── Divider ──────────────────────────────────────────────────────────────────
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ─── Outputs ──────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Outputs</div>', unsafe_allow_html=True)

out_col1, out_col2 = st.columns([3, 2])

with out_col1:
    st.markdown("""
    <div class="output-panel">
      <div class="output-panel-title">
        <div class="output-icon">📋</div>
        Insights Report
      </div>
    </div>
    """, unsafe_allow_html=True)
    if st.session_state.render_success and os.path.exists("data/report.txt"):
        with open("data/report.txt", 'r', encoding='utf-8') as f:
            st.text(f.read())
    else:
        st.info("Run the pipeline to generate a report.")

with out_col2:
    st.markdown("""
    <div class="output-panel">
      <div class="output-panel-title">
        <div class="output-icon">📧</div>
        Email Preview
      </div>
    </div>
    """, unsafe_allow_html=True)
    if st.session_state.render_success and os.path.exists("data/email.html"):
        with open("data/email.html", 'r', encoding='utf-8') as f:
            st.markdown(f.read(), unsafe_allow_html=True)
    else:
        st.info("Email will appear here after report generation.")

    st.markdown("""
    <div class="output-panel" style="margin-top:14px;">
      <div class="output-panel-title">
        <div class="output-icon">🔗</div>
        Google Doc
      </div>
    </div>
    """, unsafe_allow_html=True)
    if os.path.exists("data/doc_link.txt"):
        with open("data/doc_link.txt", 'r', encoding='utf-8') as f:
            doc_link = f.read().strip()
            st.markdown(f"[Open Google Doc →]({doc_link})")
    else:
        st.info("Publish the report to get a Google Doc link.")
