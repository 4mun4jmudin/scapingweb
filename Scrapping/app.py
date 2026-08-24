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

# Theme Selector in Sidebar
theme = st.sidebar.select_slider(
    "🌓 Tema Aplikasi",
    options=["Dark Mode", "Light Mode"],
    value="Dark Mode"
)

# Custom CSS with Smooth Transitions, Glassmorphism, and Interactive Sidebar tabs
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
    
    /* Interactive Sidebar Navigation Tabs */
    div[data-testid="stRadio"] [role="radiogroup"] label span:first-child {
        display: none !important; /* Hide radio circles */
    }
    div[data-testid="stRadio"] [role="radiogroup"] {
        gap: 10px !important;
        padding-top: 10px !important;
    }
    div[data-testid="stRadio"] [role="radiogroup"] label {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 12px 18px !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        width: 100% !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
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
    
    /* Interactive Sidebar Navigation Tabs */
    div[data-testid="stRadio"] [role="radiogroup"] label span:first-child {
        display: none !important; /* Hide radio circles */
    }
    div[data-testid="stRadio"] [role="radiogroup"] {
        gap: 10px !important;
        padding-top: 10px !important;
    }
    div[data-testid="stRadio"] [role="radiogroup"] label {
        background-color: #f1f5f9 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 12px 18px !important;
        color: #64748b !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
        width: 100% !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
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
st.sidebar.image(
    "https://img.icons8.com/color/96/qris.png", width=80
)  # Logo Opsional
st.sidebar.title("📌 Navigasi Menu")
page = st.sidebar.radio(
    "Pilih Halaman:",
    [
        "📊 Ringkasan Dataset",
        "🤖 Evaluasi & Performa Model",
        "🔮 Simulator Prediksi Live",
    ],
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
if page == "📊 Ringkasan Dataset":
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
elif page == "🤖 Evaluasi & Performa Model":
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
        * **Kelemahan:** Memiliki *independency assumption* yang menganggap setiap kata berdiri sendiri. Mudah terkecoh oleh kalimat panjang yang mengandung banyak kata netral/pendukung.
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
elif page == "🔮 Simulator Prediksi Live":
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