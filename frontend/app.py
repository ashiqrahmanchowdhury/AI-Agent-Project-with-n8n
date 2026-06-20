import streamlit as st
import requests

st.set_page_config(
    page_title="Article Analyzer",
    page_icon="📄",
    layout="centered"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    [data-testid="stHeader"] { background: transparent; }
    
    .hero {
        text-align: center;
        padding: 2.5rem 0 1.5rem 0;
    }
    
    .hero-badge {
        display: inline-block;
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        color: #2563eb;
        font-size: 12px;
        font-weight: 600;
        padding: 4px 14px;
        border-radius: 999px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    
    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0f172a;
        letter-spacing: -0.03em;
        margin: 0;
    }
    
    .hero-title span { color: #2563eb; }
    
    .hero-sub {
        color: #64748b;
        font-size: 1rem;
        margin-top: 0.5rem;
    }
    
    .stTextInput > label {
        font-size: 13px !important;
        font-weight: 600 !important;
        color: #475569 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 8px !important;
    }

    [data-testid="stTextInput"] div[data-baseweb="input"] {
        background-color: #ffffff !important; 
        border: 2px solid #334155 !important; 
        border-radius: 8px !important;
        transition: all 0.2s ease-in-out;
    }

    [data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
        border-color: #2563eb !important; 
        box-shadow: 0 0 0 2px rgba(37,99,235,0.2) !important;
        background-color: #ffffff !important;
    }

    [data-testid="stTextInput"] input {
        color: #0f172a !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        background-color: #ffffff !important;
        border-radius: 8px !important;
    }

    [data-testid="stTextInput"] input::placeholder {
        color: #94a3b8 !important;
        font-style: italic;
    }
    /* -------------------------------------- */
    
    .stButton > button {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.2s !important;
        box-shadow: 0 4px 12px rgba(37,99,235,0.3) !important;
    }
    
    .stButton > button:hover {
        opacity: 0.88 !important;
        box-shadow: 0 6px 20px rgba(37,99,235,0.4) !important;
    }
    
    .steps-row {
        display: flex;
        gap: 8px;
        margin-top: 1.2rem;
    }
    
    .step-card {
        flex: 1;
        background: #ffffff;
        border: 1.5px solid #dbeafe;
        border-radius: 12px;
        padding: 12px 6px;
        text-align: center;
        font-size: 11px;
        color: #2563eb;
        font-weight: 600;
        box-shadow: 0 2px 6px rgba(37,99,235,0.08);
    }
    
    .step-card .ico { font-size: 22px; display: block; margin-bottom: 4px; }
    
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
        margin-top: 1.5rem;
        padding-bottom: 1rem;
    }
    
    .sid-text {
        font-family: monospace;
        font-size: 11px;
        color: #94a3b8;
        margin-top: 4px;
    }

    div[data-testid="stVerticalBlock"] > div:has(> div.stTextInput) {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 24px rgba(0,0,0,0.06);
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

BACKEND_URL = "http://localhost:8000"

st.markdown("""
<div class="hero">
    <div class="hero-badge">⚡ Powered by Gemini AI · n8n · FastAPI</div>
    <h1 class="hero-title">Article <span>Analyzer</span></h1>
    <p class="hero-sub">Enter any article URL and get AI-powered summary & insights delivered to your inbox.</p>
</div>
""", unsafe_allow_html=True)

email = st.text_input("📧 Email Address", placeholder="your@email.com")
article_url = st.text_input("🔗 Article URL", placeholder="https://example.com/article...")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 Analyze Article", use_container_width=True):
    if not email or not article_url:
        st.error("⚠️ Please fill in both fields.")
    elif not article_url.startswith("http"):
        st.error("⚠️ URL must start with http:// or https://")
    else:
        with st.spinner("Processing your article..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/analyze",
                    json={"email": email, "article_url": article_url},
                    timeout=120
                )
                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ Article is being analyzed! Check your email shortly.")
                    st.markdown(f'<div class="sid-text">Session ID: {data["session_id"]}</div>', unsafe_allow_html=True)
                else:
                    detail = response.json().get("detail", "Something went wrong.")
                    st.error(f"❌ {detail}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Make sure FastAPI is running.")
            except requests.exceptions.Timeout:
                st.warning("⏳ Request sent! The analysis may take a moment. Check your email.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

st.markdown("""
<div class="steps-row">
    <div class="step-card"><span class="ico">🌐</span>Scrape</div>
    <div class="step-card"><span class="ico">✍️</span>Summarize</div>
    <div class="step-card"><span class="ico">💡</span>Insights</div>
    <div class="step-card"><span class="ico">📊</span>Sheets</div>
    <div class="step-card"><span class="ico">📧</span>Email</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="footer">Module 21 · AI Agent Project with n8n · Ashiq Rahman Chowdhury</div>', unsafe_allow_html=True)