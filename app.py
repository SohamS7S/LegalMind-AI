
# app.py

import streamlit as st

# Safe imports
try:
    from legalmind_core import run_legalmind
except ImportError:
    st.error("LegalMind core module not found. Please ensure 'legalmind_core.py' exists.")
    st.stop()

try:
    from pdf_utils import extract_pdf_text
except ImportError:
    st.error("PDF utilities module not found. Please ensure 'pdf_utils.py' exists.")
    st.stop()

st.set_page_config(
    page_title="LegalMind AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",  # clean, minimal sidebar
)

# =========================
#  PREMIUM LUXURY CSS
# =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global reset */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #F0F0F0;
    }

    /* Animated background with moving gold gradient */
    .stApp {
        background: #080808;
        background-image:
            radial-gradient(ellipse at 30% 20%, rgba(212, 175, 55, 0.06) 0%, transparent 60%),
            radial-gradient(ellipse at 70% 80%, rgba(212, 175, 55, 0.04) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 50%, rgba(20, 20, 20, 0.9) 0%, transparent 70%);
        background-size: 200% 200%;
        animation: ambientShift 25s ease-in-out infinite alternate;
    }

    @keyframes ambientShift {
        0% { background-position: 0% 0%; }
        100% { background-position: 100% 100%; }
    }

    /* Main container */
    .main .block-container {
        max-width: 1100px;
        padding: 2rem 2rem 3rem;
        margin: 0 auto;
    }

    /* Title with gold gradient + glow animation */
    .premium-title {
        text-align: center;
        font-size: 58px;
        font-weight: 700;
        letter-spacing: -1px;
        background: linear-gradient(135deg, #D4AF37 0%, #F5E7A0 40%, #B8960C 70%, #E5D37C 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: titleGlow 4s ease-in-out infinite alternate;
        margin-bottom: 0.25rem;
        filter: drop-shadow(0 0 20px rgba(212, 175, 55, 0.3));
    }

    @keyframes titleGlow {
        0% { filter: drop-shadow(0 0 15px rgba(212, 175, 55, 0.25)); }
        100% { filter: drop-shadow(0 0 30px rgba(212, 175, 55, 0.5)); }
    }

    .premium-subtitle {
        text-align: center;
        font-size: 18px;
        font-weight: 400;
        color: #B8A880;
        letter-spacing: 0.5px;
        margin-bottom: 2.5rem;
    }

    /* Glass card with gold edge */
    .glass-card {
        background: rgba(18, 18, 18, 0.65);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(212, 175, 55, 0.15);
        border-radius: 22px;
        padding: 28px;
        box-shadow: 0 25px 50px -10px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.03);
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(212, 175, 55, 0.3);
        box-shadow: 0 25px 50px -10px rgba(0,0,0,0.6), 0 0 30px rgba(212, 175, 55, 0.08);
    }

    /* Premium button with gold shimmer */
    .stButton > button {
        background: linear-gradient(135deg, #1C1C1C 0%, #0E0E0E 100%);
        border: 1px solid #D4AF37;
        border-radius: 14px;
        color: #D4AF37;
        font-weight: 600;
        font-size: 16px;
        padding: 0.8rem 2rem;
        letter-spacing: 0.5px;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1.2);
        box-shadow: 0 4px 18px rgba(0,0,0,0.5);
    }
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -75%;
        width: 50%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.2), transparent);
        transform: skewX(-25deg);
        transition: left 0.7s;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #2A2410 0%, #1C1A10 100%);
        border-color: #F5E7A0;
        color: #FFFFFF;
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.3);
        transform: translateY(-2px);
    }
    .stButton > button:hover::before {
        left: 125%;
    }
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 8px rgba(0,0,0,0.7);
    }

    /* Input fields */
    .stTextArea textarea, .stFileUploader {
        background: rgba(20, 20, 20, 0.8) !important;
        border: 1px solid rgba(212, 175, 55, 0.2) !important;
        border-radius: 16px !important;
        color: #F0F0F0 !important;
        font-size: 15px !important;
        transition: all 0.3s ease;
    }
    .stTextArea textarea:focus, .stFileUploader:focus-within {
        border-color: #D4AF37 !important;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.2) !important;
        outline: none !important;
    }
    .stFileUploader {
        padding: 14px !important;
        border-style: dashed !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(25, 25, 25, 0.6);
        border-radius: 12px;
        border: 1px solid rgba(212, 175, 55, 0.2);
        font-weight: 500;
    }
    .streamlit-expanderContent {
        background: rgba(18, 18, 18, 0.5);
        border-radius: 0 0 12px 12px;
        padding: 20px;
        border: 1px solid rgba(212, 175, 55, 0.1);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
        border-bottom: 1px solid rgba(212, 175, 55, 0.2);
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px 12px 0 0;
        padding: 12px 24px;
        font-weight: 500;
        color: #B8A880;
        border: 1px solid transparent;
        margin-right: 4px;
        transition: all 0.3s;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #D4AF37;
        background: rgba(212, 175, 55, 0.05);
        border-color: rgba(212, 175, 55, 0.3);
    }
    .stTabs [aria-selected="true"] {
        background: rgba(212, 175, 55, 0.08) !important;
        color: #D4AF37 !important;
        border-color: rgba(212, 175, 55, 0.4) !important;
        box-shadow: inset 0 -2px 0 #D4AF37;
    }

    /* Divider */
    .premium-divider {
        border: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.4), transparent);
        margin: 2.2rem 0;
    }

    /* Disclaimer */
    .disclaimer-text {
        color: #7A7A7A;
        font-size: 13px;
        text-align: center;
        margin-top: 2.5rem;
        letter-spacing: 0.2px;
        border-top: 1px solid rgba(212, 175, 55, 0.15);
        padding-top: 2rem;
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: #D4AF37 !important;
    }

    /* Sidebar (minimal) */
    [data-testid="stSidebar"] {
        background: rgba(8, 8, 8, 0.95);
        backdrop-filter: blur(25px);
        border-right: 1px solid rgba(212, 175, 55, 0.2);
    }
    .sidebar-brand {
        text-align: center;
        font-size: 24px;
        font-weight: 700;
        letter-spacing: -0.3px;
        color: #D4AF37;
        margin-top: 2rem;
    }

    /* Alerts */
    .stAlert {
        border-radius: 14px;
        border: 1px solid rgba(212, 175, 55, 0.25);
        background: rgba(20, 20, 20, 0.8);
    }
</style>
""", unsafe_allow_html=True)

# =========================
#  HEADER
# =========================
st.markdown("""
<div class="premium-title">
    ⚖️ LegalMind AI
</div>
<div class="premium-subtitle">
    Intelligent Legal Reasoning · Multi‑Agent Analysis · Automated Verification
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='premium-divider'></div>", unsafe_allow_html=True)

# =========================
#  SIDEBAR (minimal)
# =========================
with st.sidebar:
    st.markdown("<div class='sidebar-brand'>LEGALMIND</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; color:#B8A880; font-size:13px;'>Premium Legal Intelligence</div>", unsafe_allow_html=True)
    st.markdown("---")
    # No tech stack – pure, clean

# =========================
#  PDF UPLOAD
# =========================
uploaded_file = st.file_uploader(
    "📄 Upload Legal Document (PDF)",
    type=["pdf"],
    help="Max file size: 200MB"
)

document_text = ""

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")
    try:
        document_text = extract_pdf_text(uploaded_file)

        with st.expander("📑 Extracted Document Preview", expanded=False):
            st.text_area("Preview", document_text[:3000], height=280)

        st.info(f"Extracted {len(document_text)} characters.")
    except Exception as e:
        st.error(f"PDF extraction failed: {str(e)}")

# =========================
#  QUESTION INPUT
# =========================
st.markdown("---")
question = st.text_area(
    "💬 Enter your legal query",
    height=150,
    placeholder="e.g., A startup founder claims a former employee copied proprietary source code and joined a competitor. Identify potential civil, criminal, contractual and IP issues.",
    help="Describe the legal scenario in detail for best results."
)

# =========================
#  ANALYZE BUTTON
# =========================
if st.button("⚖️ Analyze Legal Matter", use_container_width=True):
    if not question.strip():
        st.warning("Please enter a legal question.")
    else:
        try:
            with st.spinner("LegalMind is reasoning through legal materials..."):
                result = run_legalmind(question)

            if not isinstance(result, dict) or "final" not in result:
                st.error("Unexpected response format from LegalMind engine. Please try again.")
            else:
                st.markdown("## ⚖️ Final Legal Opinion")
                st.markdown(f"""
                <div class="glass-card">
                    {result["final"]}
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<div class='premium-divider'></div>", unsafe_allow_html=True)

                tab1, tab2, tab3 = st.tabs([
                    "📚 Retrieved Context",
                    "🧠 Lawyer Analysis",
                    "🔍 Verification Report"
                ])

                with tab1:
                    st.write(result.get("context", "No context retrieved."))
                with tab2:
                    st.write(result.get("lawyer", "No lawyer analysis available."))
                with tab3:
                    st.write(result.get("verifier", "No verification report available."))

                st.markdown("<div class='premium-divider'></div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An unexpected error occurred during analysis: {str(e)}")
            st.info("Please check your input or try again later.")

# =========================
#  DISCLAIMER
# =========================
st.markdown("""
<div class="disclaimer-text">
    LegalMind provides AI‑assisted legal analysis based on retrieved materials and multi‑agent reasoning.
    It is not a substitute for professional legal advice.
</div>
""", unsafe_allow_html=True)
