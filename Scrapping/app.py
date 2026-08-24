import os
import pickle
import re
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from wordcloud import WordCloud

# =====================================================================
# 1. KONFIGURASI HALAMAN & THEME
# =====================================================================
st.set_page_config(
    page_title="Analytics Dashboard: Sentimen QRIS & Cashless",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize theme in session state
if "theme" not in st.session_state:
    st.session_state.theme = "Dark Mode"

# Theme Toggle Button (On/Off Icon)
toggle_icon = "☀️" if st.session_state.theme == "Dark Mode" else "🌙"
toggle_label = "Switch to Light Mode" if st.session_state.theme == "Dark Mode" else "Switch to Dark Mode"

# Custom style for toggle button in sidebar to look neat
st.sidebar.markdown(
    """
    <div style="margin-top: 10px; margin-bottom: -5px;">
        <span style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; color: #64748b; opacity: 0.85;">Tema Aplikasi</span>
    </div>
    """,
    unsafe_allow_html=True
)

if st.sidebar.button(f"{toggle_icon} {toggle_label}", use_container_width=True):
    if st.session_state.theme == "Dark Mode":
        st.session_state.theme = "Light Mode"
    else:
        st.session_state.theme = "Dark Mode"
    st.rerun()

theme = st.session_state.theme

# Custom CSS with Smooth Transitions, Glassmorphism, and Interactive Sidebar tabs with SVG Icons
if theme == "Dark Mode":
    theme_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
        transition: background-color 0.4s ease, color 0.4s ease, border-color 0.4s ease, box-shadow 0.3s ease !important;
    }
    
    /* Backgrounds & Text */
    .stApp {
        background-color: #0b0f19 !important;
        color: #f1f5f9 !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #1f2937 !important;
    }
    
    /* Interactive Sidebar Navigation Tabs with Custom SVGs */
    div[data-testid="stRadio"] [role="radiogroup"] label > div:first-child {
        display: none !important; /* Hide radio circles completely */
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    div[data-testid="stRadio"] [role="radiogroup"] {
        gap: 10px !important;
        padding-top: 10px !important;
    }
    div[data-testid="stRadio"] [role="radiogroup"] label {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 12px 18px 12px 48px !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        width: 100% !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        position: relative !important;
    }
    div[data-testid="stRadio"] [role="radiogroup"] label::before {
        content: "" !important;
        position: absolute !important;
        left: 18px !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        width: 18px !important;
        height: 18px !important;
        background-repeat: no-repeat !important;
        background-position: center !important;
        background-size: contain !important;
        transition: all 0.3s ease !important;
    }
    
    /* Assigning professional icons to menu items */
    div[data-testid="stRadio"] [role="radiogroup"] label:nth-of-type(1)::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='18' y1='20' x2='18' y2='10'%3E%3C/line%3E%3Cline x1='12' y1='20' x2='12' y2='4'%3E%3C/line%3E%3Cline x1='6' y1='20' x2='6' y2='14'%3E%3C/line%3E%3C/svg%3E") !important;
    }
    div[data-testid="stRadio"] [role="radiogroup"] label:nth-of-type(2)::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'%3E%3C/path%3E%3Cpath d='m9 11 2 2 4-4'%3E%3C/path%3E%3C/svg%3E") !important;
    }
    div[data-testid="stRadio"] [role="radiogroup"] label:nth-of-type(3)::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z'%3E%3C/path%3E%3Cpath d='m5 3 1 2.5L8.5 6 6 7 5 9.5 4 7 1.5 6 4 5.5z'%3E%3C/path%3E%3Cpath d='m19 17 1 2.5 2.5.5-2.5 1-1 2.5-1-2.5-2.5-1 2.5-1z'%3E%3C/path%3E%3C/svg%3E") !important;
    }
    
    div[data-testid="stRadio"] [role="radiogroup"] label:hover {
        background-color: #334155 !important;
        color: #ffffff !important;
        border-color: #475569 !important;
        transform: translateX(6px);
    }
    div[data-testid="stRadio"] [role="radiogroup"] label[data-checked="true"],
    div[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) {
        background: linear-gradient(135deg, #00adb5 0%, #6366f1 100%) !important;
        border-color: #00adb5 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(0, 173, 181, 0.35) !important;
    }
    div[data-testid="stRadio"] [role="radiogroup"] label[data-checked="true"]::before,
    div[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked)::before {
        filter: brightness(0) invert(1) !important; /* Turn SVG white */
    }
    div[data-testid="stRadio"] [role="radiogroup"] label[data-checked="true"] div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) div[data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
    }
    div[data-testid="stRadio"] [role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {
        margin: 0 !important;
    }
    
    /* Hero Banner Styling */
    .hero-container {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
        padding: 2.5rem;
        border-radius: 20px;
        border: 1px solid #4338ca;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px -10px rgba(67, 56, 202, 0.4);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.85);
    }
    
    /* Metrics block styling */
    div[data-testid="stMetric"] {
        background-color: #1e293b !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        border: 1px solid #334155 !important;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.2), 0 2px 4px -2px rgb(0 0 0 / 0.2) !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.3), 0 4px 6px -4px rgb(0 0 0 / 0.3) !important;
    }
    
    /* Individual Accent Borders */
    div[data-testid="stMetric"]:nth-of-type(1) { border-left: 5px solid #00adb5 !important; }
    div[data-testid="stMetric"]:nth-of-type(2) { border-left: 5px solid #10b981 !important; }
    div[data-testid="stMetric"]:nth-of-type(3) { border-left: 5px solid #ef4444 !important; }
    div[data-testid="stMetric"]:nth-of-type(4) { border-left: 5px solid #8b5cf6 !important; }
    
    div[data-testid="stMetricValue"] > div {
        color: #f1f5f9 !important;
        font-weight: 700 !important;
    }
    
    div[data-testid="stMetricLabel"] > div {
        color: #94a3b8 !important;
        font-weight: 500 !important;
    }
    
    /* Custom Streamlit Button Styling */
    div.stButton > button {
        background: linear-gradient(135deg, #00adb5 0%, #6366f1 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 173, 181, 0.25) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 173, 181, 0.4) !important;
    }
    
    /* Dataframes and Tables */
    div.stDataFrame {
        border: 1px solid #1f2937 !important;
        border-radius: 12px !important;
    }
    
    /* Custom spacing */
    .main { padding: 1.5rem 2.5rem; }
    hr { border-color: #1f2937 !important; }
    </style>
    """
else:
    theme_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
        transition: background-color 0.4s ease, color 0.4s ease, border-color 0.4s ease, box-shadow 0.3s ease !important;
    }
    
    /* Backgrounds & Text */
    .stApp {
        background-color: #f8fafc !important;
        color: #0f172a !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    
    /* Interactive Sidebar Navigation Tabs with Custom SVGs */
    div[data-testid="stRadio"] [role="radiogroup"] label > div:first-child {
        display: none !important; /* Hide radio circles completely */
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    div[data-testid="stRadio"] [role="radiogroup"] {
        gap: 10px !important;
        padding-top: 10px !important;
    }
    div[data-testid="stRadio"] [role="radiogroup"] label {
        background-color: #f1f5f9 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 12px 18px 12px 48px !important;
        color: #64748b !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
        width: 100% !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        position: relative !important;
    }
    div[data-testid="stRadio"] [role="radiogroup"] label::before {
        content: "" !important;
        position: absolute !important;
        left: 18px !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        width: 18px !important;
        height: 18px !important;
        background-repeat: no-repeat !important;
        background-position: center !important;
        background-size: contain !important;
        transition: all 0.3s ease !important;
    }
    
    /* Assigning professional icons to menu items */
    div[data-testid="stRadio"] [role="radiogroup"] label:nth-of-type(1)::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%2364748b' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='18' y1='20' x2='18' y2='10'%3E%3C/line%3E%3Cline x1='12' y1='20' x2='12' y2='4'%3E%3C/line%3E%3Cline x1='6' y1='20' x2='6' y2='14'%3E%3C/line%3E%3C/svg%3E") !important;
    }
    div[data-testid="stRadio"] [role="radiogroup"] label:nth-of-type(2)::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%2364748b' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'%3E%3C/path%3E%3Cpath d='m9 11 2 2 4-4'%3E%3C/path%3E%3C/svg%3E") !important;
    }
    div[data-testid="stRadio"] [role="radiogroup"] label:nth-of-type(3)::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%2364748b' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z'%3E%3C/path%3E%3Cpath d='m5 3 1 2.5L8.5 6 6 7 5 9.5 4 7 1.5 6 4 5.5z'%3E%3C/path%3E%3Cpath d='m19 17 1 2.5 2.5.5-2.5 1-1 2.5-1-2.5-2.5-1 2.5-1z'%3E%3C/path%3E%3C/svg%3E") !important;
    }
    
    div[data-testid="stRadio"] [role="radiogroup"] label:hover {
        background-color: #e2e8f0 !important;
        color: #0f172a !important;
        border-color: #cbd5e1 !important;
        transform: translateX(6px);
    }
    div[data-testid="stRadio"] [role="radiogroup"] label[data-checked="true"],
    div[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        border-color: #3b82f6 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
    }
    div[data-testid="stRadio"] [role="radiogroup"] label[data-checked="true"]::before,
    div[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked)::before {
        filter: brightness(0) invert(1) !important;
    }
    div[data-testid="stRadio"] [role="radiogroup"] label[data-checked="true"] div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) div[data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
    }
    div[data-testid="stRadio"] [role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {
        margin: 0 !important;
    }
    
    /* Hero Banner Styling */
    .hero-container {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        padding: 2.5rem;
        border-radius: 20px;
        border: 1px solid #bfdbfe;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -10px rgba(59, 130, 246, 0.15);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: #3b82f6;
    }
    
    /* Metrics block styling */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05), 0 2px 4px -2px rgb(0 0 0 / 0.05) !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1) !important;
    }
    
    /* Individual Accent Borders */
    div[data-testid="stMetric"]:nth-of-type(1) { border-left: 5px solid #00adb5 !important; }
    div[data-testid="stMetric"]:nth-of-type(2) { border-left: 5px solid #10b981 !important; }
    div[data-testid="stMetric"]:nth-of-type(3) { border-left: 5px solid #ef4444 !important; }
    div[data-testid="stMetric"]:nth-of-type(4) { border-left: 5px solid #8b5cf6 !important; }
    
    div[data-testid="stMetricValue"] > div {
        color: #0f172a !important;
        font-weight: 700 !important;
    }
    
    div[data-testid="stMetricLabel"] > div {
        color: #64748b !important;
        font-weight: 500 !important;
    }
    
    /* Custom Streamlit Button Styling */
    div.stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.25) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Dataframes and Tables */
    div.stDataFrame {
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
    }
    
    /* Custom spacing */
    .main { padding: 1.5rem 2.5rem; }
    hr { border-color: #e2e8f0 !important; }
    </style>
    """

st.markdown(theme_css, unsafe_allow_html=True)


# =====================================================================
# 2. LOAD DATASET & MODEL
# =====================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_data
def load_dataset():
    file_path = os.path.join(BASE_DIR, "data_twitter_terlabeli.xlsx")
    if os.path.exists(file_path):
        return pd.read_excel(file_path)
    return None


@st.cache_resource
def load_models():
    nb, svm, tfidf = None, None, None
    nb_path = os.path.join(BASE_DIR, "nb_model.pkl")
    svm_path = os.path.join(BASE_DIR, "svm_model.pkl")
    tfidf_path = os.path.join(BASE_DIR, "tfidf.pkl")
    
    if os.path.exists(nb_path):
        with open(nb_path, "rb") as f:
            nb = pickle.load(f)
    if os.path.exists(svm_path):
        with open(svm_path, "rb") as f:
            svm = pickle.load(f)
    if os.path.exists(tfidf_path):
        with open(tfidf_path, "rb") as f:
            tfidf = pickle.load(f)
    return nb, svm, tfidf


df_data = load_dataset()
nb_model, svm_model, tfidf = load_models()

# =====================================================================
# 3. SIDEBAR NAVIGATION
# =====================================================================
st.sidebar.markdown(
    """
    <div style="margin-top: 15px; margin-bottom: -5px;">
        <span style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; color: #64748b; opacity: 0.85;">Navigasi Menu</span>
    </div>
    """,
    unsafe_allow_html=True
)

page = st.sidebar.radio(
    "Navigasi Menu", # Hiding text label since category header is used
    [
        "Ringkasan Dataset",
        "Evaluasi & Performa Model",
        "Simulator Prediksi Live",
    ],
    label_visibility="collapsed"
)

st.sidebar.write("---")
st.sidebar.info(
    "**Analisis Sentimen QRIS & Cashless**\n\n"
    "Membandingkan Performa Algoritma **Naive Bayes** dan **Support Vector Machine (SVM)** "
    "berdasarkan Opini Publik di Twitter/X."
)

# =====================================================================
# HALAMAN 1: RINGKASAN DATASET
# =====================================================================
if page == "Ringkasan Dataset":
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-title">📊 Ringkasan Dataset & Analisis Opini</div>
            <div class="hero-subtitle">Overview distribusi data sentimen publik terhadap penggunaan QRIS dan pembayaran cashless.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if df_data is not None:
        total_data = len(df_data)
        pos_count = (df_data["label"] == "Positif").sum()
        neg_count = (df_data["label"] == "Negatif").sum()

        # Row 1: Key Metrics (KPIs)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Data Tweet", f"{total_data:,} tweet")
        col2.metric(
            "Sentimen Positif", f"{pos_count}", f"{pos_count/total_data:.1%}"
        )
        col3.metric(
            "Sentimen Negatif",
            f"{neg_count}",
            f"-{neg_count/total_data:.1%}",
            delta_color="inverse",
        )
        col4.metric("Model Terbaik", "SVM", "87.23% Akurasi")

        st.write("---")

        # Row 2: Charts & Visualizations
        c1, c2 = st.columns([1.2, 1])

        with c1:
            st.subheader("📈 Proporsi Sentimen")
            fig_pie = px.pie(
                df_data,
                names="label",
                hole=0.4,
                color="label",
                color_discrete_map={"Positif": "#10b981", "Negatif": "#ef4444"},
            )
            fig_pie.update_traces(
                textposition="inside", textinfo="percent+label"
            )
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_family="Plus Jakarta Sans",
                font_color="#f1f5f9" if theme == "Dark Mode" else "#0f172a",
                margin=dict(l=20, r=20, t=40, b=20),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.1,
                    xanchor="center",
                    x=0.5
                )
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with c2:
            st.subheader("☁️ Word Cloud Kata Kunci")
            sentiment_type = st.radio(
                "Tampilkan Word Cloud Untuk:",
                ["Positif", "Negatif"],
                horizontal=True,
            )

            text_subset = " ".join(
                df_data[df_data["label"] == sentiment_type][
                    "cleaned_text"
                ].astype(str)
            )
            if text_subset.strip():
                color_map = "Greens" if sentiment_type == "Positif" else "Reds"
                bg_color = "#0b0f19" if theme == "Dark Mode" else "#ffffff"
                wc = WordCloud(
                    width=600,
                    height=350,
                    background_color=bg_color,
                    colormap=color_map,
                ).generate(text_subset)

                fig_wc, ax = plt.subplots(figsize=(6, 3.5))
                ax.imshow(wc, interpolation="bilinear")
                ax.axis("off")
                fig_wc.patch.set_facecolor(bg_color)
                st.pyplot(fig_wc)

        st.write("---")

        # Row 3: Data Table View
        st.subheader("🔍 Sampel Data Tweet Terlabeli")
        st.dataframe(
            df_data[["cleaned_text", "label"]].head(10),
            use_container_width=True,
        )

    else:
        st.error(
            "File `data_twitter_terlabeli.xlsx` tidak ditemukan. Silakan jalankan `1_preprocessing.py` terlebih dahulu."
        )

# =====================================================================
# HALAMAN 2: EVALUASI & PERFORMA MODEL
# =====================================================================
elif page == "Evaluasi & Performa Model":
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-title">🤖 Perbandingan Model: Naive Bayes vs SVM</div>
            <div class="hero-subtitle">Analisis komparasi performa algoritma berdasarkan metrik klasifikasi standar.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Metrics dari hasil pengujian nyata dataset Anda
    metrics_summary = pd.DataFrame(
        {
            "Metrik Evaluasi": [
                "Accuracy",
                "Precision (Pos/Neg)",
                "Recall (Pos/Neg)",
                "F1-Score",
            ],
            "Multinomial Naive Bayes": [
                "82.98%",
                "78.13% / 93.33%",
                "96.15% / 66.67%",
                "82.00%",
            ],
            "Support Vector Machine (SVM)": [
                "87.23%",
                "83.33% / 94.12%",
                "96.15% / 76.19%",
                "86.75%",
            ],
        }
    )

    col_a, col_b = st.columns([1.2, 1])

    with col_a:
        st.subheader("📊 Bar Chart Perbandingan Akurasi")
        fig_bar = go.Figure(
            data=[
                go.Bar(
                    name="Naive Bayes",
                    x=["Akurasi"],
                    y=[0.8298],
                    text=["82.98%"],
                    textposition="auto",
                    marker_color="#FFA15A",
                ),
                go.Bar(
                    name="SVM (Linear)",
                    x=["Akurasi"],
                    y=[0.8723],
                    text=["87.23%"],
                    textposition="auto",
                    marker_color="#19D3BF",
                ),
            ]
        )
        fig_bar.update_layout(
            barmode="group",
            yaxis_range=[0, 1],
            height=350,
            margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_family="Plus Jakarta Sans",
            font_color="#f1f5f9" if theme == "Dark Mode" else "#0f172a",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#1f2937" if theme == "Dark Mode" else "#e2e8f0"),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_b:
        st.subheader("📋 Matriks Evaluasi Detail")
        st.table(metrics_summary)

    st.write("---")

    # Kelebihan & Kekurangan
    st.subheader("📌 Ringkasan Temuan Riset")
    tab1, tab2 = st.tabs(
        ["Multinomial Naive Bayes", "Support Vector Machine (SVM)"]
    )

    with tab1:
        st.write(
            """
        * **Kelebihan:** Proses komputasi/pelatihan sangat cepat, sangat efisien untuk dataset berskala besar, serta sensitif terhadap kata kunci eksplisit.
        * **Kelemahan:** Membutuhkan waktu *training* yang lebih lama dibanding Naive Bayes jika ukuran dataset meloncat hingga ratusan ribu baris.
        """
        )

    with tab2:
        st.write(
            """
        * **Kelebihan:** Sangat akurat dalam membentuk *hyperplane* pembatas pada ruang berdimensi tinggi (TF-IDF), mampu memahami konteks kalimat kompleks dan panjang secara utuh.
        * **Kelemahan:** Membutuhkan waktu *training* yang lebih lama dibanding Naive Bayes jika ukuran dataset meloncat hingga ratusan ribu baris.
        """
        )

# =====================================================================
# HALAMAN 3: SIMULATOR PREDIKSI LIVE
# =====================================================================
elif page == "Simulator Prediksi Live":
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-title">🔮 Simulator Prediksi Sentimen Real-Time</div>
            <div class="hero-subtitle">Uji coba performa model secara langsung menggunakan input teks opini baru Anda.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if nb_model is not None and svm_model is not None and tfidf is not None:
        user_input = st.text_area(
            "Masukkan Opini Publik tentang QRIS / Cashless:",
            value="pake qris gampang banget dan gak perlu nunggu uang kembalian",
            height=100,
        )

        if st.button("🚀 Analisis Sentimen Sekarang", use_container_width=True):
            with st.spinner("Memproses teks dan menghitung vektor TF-IDF..."):
                # Preprocessing Sederhana
                clean_text = user_input.lower()
                clean_text = re.sub(r"https?://\S+|www\.\S+", "", clean_text)
                clean_text = re.sub(r"@\w+", "", clean_text)
                clean_text = re.sub(r"[^\w\s]", "", clean_text)
                clean_text = re.sub(r"\d+", "", clean_text)
                clean_text = re.sub(r"\s+", " ", clean_text).strip()

                # Transform
                text_tfidf = tfidf.transform([clean_text])

                # Predict
                pred_nb = nb_model.predict(text_tfidf)[0]
                pred_svm = svm_model.predict(text_tfidf)[0]

                st.write("---")
                st.subheader("📥 Hasil Pembersihan Teks (Cleansing)")
                st.code(clean_text, language="text")

                # Display Results
                st.subheader("🎯 Hasil Prediksi Model")
                col_nb, col_svm = st.columns(2)

                with col_nb:
                    st.markdown("#### 🔸 Naive Bayes")
                    if pred_nb == "Positif":
                        st.success(f"**{pred_nb}** 🟢")
                    else:
                        st.error(f"**{pred_nb}** 🔴")

                with col_svm:
                    st.markdown("#### 🔹 Support Vector Machine (SVM)")
                    if pred_svm == "Positif":
                        st.success(f"**{pred_svm}** 🟢")
                    else:
                        st.error(f"**{pred_svm}** 🔴")

    else:
        st.error(
            "Model `.pkl` tidak ditemukan. Pastikan Anda sudah menjalankan script `2_classification.py`."
        )