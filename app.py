import streamlit as st
import requests
import json
import pandas as pd
import altair as alt
from pypdf import PdfReader

# ======================================================
# ✅ CONFIGURATION
# ======================================================
REAL_API_KEY = "DlsN6zvlNDvx4MIIiAgj5RiGqAO09AUhazmS4MQNsvkx"
DEPLOYMENT_ID = "e77ce284-a5fa-4dd0-a891-528ee92080e4"

# ======================================================
# 🎨 PROFESSIONAL ENTERPRISE THEME
# ======================================================
st.set_page_config(page_title="Sovereign Enterprise", layout="wide", page_icon="🏢")

st.markdown("""
<style>
    /* PROFESSIONAL DARK MODE */
    .stApp { background-color: #0e1117; color: #fff; }
    
    /* CARD STYLING */
    .metric-card {
        background-color: #1e2130;
        border: 1px solid #30334e;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        min-height: 200px;
    }
    
    /* AGENT COLORS */
    .arch-border { border-top: 5px solid #00d4ff; }
    .cfo-border { border-top: 5px solid #ffaa00; }
    .coo-border { border-top: 5px solid #00ff41; }
    
    /* UPLOAD BOX */
    .stFileUploader {
        border: 1px dashed #00ff41;
        padding: 10px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ======================================================
# ⚙️ LOGIC ENGINE (PDF + AI)
# ======================================================
def get_token(api_key):
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={api_key}"
    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200: return response.json()["access_token"]
    except: pass
    return None

def extract_text_from_pdf(uploaded_file):
    try:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text[:3000] # Limit to 3000 chars to avoid token limits
    except:
        return None

def call_watsonx(token, persona, prompt, temp=0.7):
    url = f"https://us-south.ml.cloud.ibm.com/ml/v1/deployments/{DEPLOYMENT_ID}/text/chat?version=2023-05-29"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Accept": "application/json"}
    
    payload = {
        "messages": [{"role": "user", "content": f"{persona}\nTASK: {prompt}"}],
        "parameters": {
            "temperature": temp,
            "decoding_method": "sample",
            "max_new_tokens": 500,
            "repetition_penalty": 1.1
        }
    }
    try:
        res = requests.post(url, json=payload, headers=headers)
        if res.status_code == 200: return res.json()['choices'][0]['message']['content']
        return f"Error: {res.text}"
    except Exception as e: return f"Error: {str(e)}"

# ======================================================
# 🖥️ MAIN APPLICATION
# ======================================================
st.title("🏢 SOVEREIGN ENTERPRISE PLATFORM")
st.markdown("**Autonomous Supply Chain Orchestration & Document Analysis**")

if 'token' not in st.session_state:
    st.session_state['token'] = get_token(REAL_API_KEY)
    st.session_state['history'] = {}

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("⚙️ Input Source")
    
    # NEW: DOCUMENT UPLOADER (RAG)
    uploaded_file = st.file_uploader("📂 Upload Vendor Proposal (PDF)", type="pdf")
    
    st.divider()
    
    # MANUAL FALLBACK
    scenario = st.selectbox("Or Select Scenario", ["None", "Budget Risk", "Automation"])
    if "Budget" in scenario: txt = "Proposal: Spend $85k on AI immediately."
    elif "Automation" in scenario: txt = "Proposal: Create Python script for inventory."
    else: txt = ""
    
    manual_topic = st.text_area("Manual Input", txt, height=100)
    
    run_btn = st.button("▶️ ANALYZE & DECIDE", type="primary")

# --- MAIN LOGIC ---
if run_btn:
    token = st.session_state['token']
    
    # DETERMINE SOURCE (PDF vs Text)
    if uploaded_file:
        with st.spinner("📄 Reading Document content..."):
            pdf_text = extract_text_from_pdf(uploaded_file)
            if pdf_text:
                topic = f"ANALYZING UPLOADED DOCUMENT CONTENT:\n{pdf_text}"
                st.info("✅ Document Extracted Successfully. Agents are reviewing file contents.")
            else:
                st.error("❌ Failed to read PDF.")
                st.stop()
    else:
        topic = manual_topic
        if not topic:
            st.error("Please Upload a PDF or Enter Text.")
            st.stop()

    st.session_state['topic'] = topic

    # --- TABS ---
    tab1, tab2, tab3 = st.tabs(["🏛️ BOARDROOM", "🛠️ THE FORGE", "📊 WATCHTOWER"])

    # 1. BOARDROOM
    with tab1:
        col1, col2, col3 = st.columns(3)
        
        # ARCHITECT
        with col1:
            st.markdown('<div class="metric-card arch-border"><h4>👨‍💻 ARCHITECT</h4></div>', unsafe_allow_html=True)
            with st.spinner("Analyzing Risks..."):
                r1 = call_watsonx(token, "You are a Paranoid Architect. Analyze technical risk in this text.", f"Review: {topic}")
                st.markdown(f'<div class="metric-card arch-border"><h4>👨‍💻 ARCHITECT</h4><p>{r1}</p></div>', unsafe_allow_html=True)

        # CFO
        with col2:
            st.markdown('<div class="metric-card cfo-border"><h4>💰 CFO</h4></div>', unsafe_allow_html=True)
            with st.spinner("Checking Budget..."):
                r2 = call_watsonx(token, "You are a Stingy CFO. Extract costs and complain.", f"Review: {topic}")
                st.markdown(f'<div class="metric-card cfo-border"><h4>💰 CFO</h4><p>{r2}</p></div>', unsafe_allow_html=True)

        # COO
        with col3:
            st.markdown('<div class="metric-card coo-border"><h4>🚚 COO</h4></div>', unsafe_allow_html=True)
            with st.spinner("Checking Speed..."):
                r3 = call_watsonx(token, "You are an Impatient COO. Look for timelines.", f"Review: {topic}")
                st.markdown(f'<div class="metric-card coo-border"><h4>🚚 COO</h4><p>{r3}</p></div>', unsafe_allow_html=True)

        st.divider()
        
        # CEO
        verdict = call_watsonx(token, "You are the CEO. Decide APPROVED or REJECTED.", f"Feedback: {r1} {r2} {r3}. Decision on: {topic}")
        st.session_state['verdict'] = verdict
        
        c = "#ff4b4b" if "REJECTED" in verdict.upper() else "#00ff41"
        st.markdown(f"<div style='text-align:center; padding:20px; border:2px solid {c}; border-radius:10px;'><h2 style='color:{c}'>{verdict}</h2></div>", unsafe_allow_html=True)

    # 2. FORGE
    with tab2:
        st.header("🛠️ Code Generator")
        if "APPROVED" in st.session_state.get('verdict', '').upper():
            if st.button("Generate Implementation Code"):
                with st.spinner("Coding..."):
                    code = call_watsonx(token, "You are a Python Dev. Write code to solve this.", st.session_state['topic'])
                    st.code(code)
        else:
            st.warning("⚠️ Proposal Rejected. Code generation locked.")

    # 3. WATCHTOWER
    with tab3:
        st.header("📊 Analytics")
        st.caption("Simulated Risk Metrics based on Agent Debate")
        data = pd.DataFrame({'Metric': ['Risk', 'Cost', 'Speed'], 'Score': [30, 85, 60]})
        st.bar_chart(data.set_index('Metric'))