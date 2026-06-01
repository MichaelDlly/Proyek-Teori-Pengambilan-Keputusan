# app.py
# Dashboard utama Streamlit

import streamlit as st
from pathlib import Path
import pandas as pd
import io

# Import modul custom
from style import apply_custom_css, set_background_image
from analysis import (
    load_dataset, analysis_certainty, analysis_risk, 
    analysis_uncertainty, analysis_probabilistic, 
    analysis_utility, analysis_sensitivity
)

# Konfigurasi halaman
st.set_page_config(
    page_title="Bank Marketing Analytics Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load dataset
df = load_dataset()

# Apply CSS
apply_custom_css()

# ========== SETUP BACKGROUND ==========
# Opsi background dari file lokal
bg_image_path_abs = r"C:\Users\user\Downloads\projek 2 tpk bu dian\Gambar Bank.jpeg"
bg_image_path_rel = "Gambar Bank.jpeg"

if Path(bg_image_path_abs).exists():
    default_path = bg_image_path_abs
elif Path(bg_image_path_rel).exists():
    default_path = bg_image_path_rel
else:
    default_path = ""

# Set background jika file ditemukan
if default_path and Path(default_path).exists():
    set_background_image(default_path)
else:
    # Background gradient default
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #FDF8F0 0%, #F9F1E6 100%);
    }
    </style>
    """, unsafe_allow_html=True)

# ========== HEADER COVER ==========
col1, col2, col3 = st.columns([0.2, 9.6, 0.2])
with col2:
    st.markdown('<div class="cover-container">', unsafe_allow_html=True)

    # Judul
    st.markdown("""
    <div class="title-container">
        <p class="main-title">BANK MARKETING ANALYTICS</p>
        <p class="sub-title">Framework Decision Intelligence Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    
    # ========== DESKRIPSI DATASET ==========
    col_desc1, col_desc2 = st.columns([2.5, 1])

    with col_desc1:
        st.markdown("""
        <div class="dataset-box" style="text-align: justify;">
            <span style="font-size:1.2rem; font-weight:700; color:#FFE4A0;">DESKRIPSI DATASET</span><br><br>
            <span style="color:#F0E6D2; line-height: 1.5;">
            Dataset yang digunakan merupakan Bank Marketing Dataset yang terdiri atas 17 variabel, yaitu age, job, marital, education, default, balance, housing, loan, contact, day, month, duration, campaign, pdays, previous, poutcome, dan deposit. Variabel-variabel tersebut mencakup informasi demografis nasabah, kondisi keuangan, serta riwayat interaksi dan kampanye pemasaran yang dilakukan oleh pihak bank.<BR><br>
            Variabel target dalam dataset ini adalah deposit, yang menunjukkan keputusan nasabah terhadap penawaran deposito berjangka. Variabel ini memiliki dua kategori, yaitu yes untuk nasabah yang menerima penawaran deposito dan no untuk nasabah yang menolak. Keberadaan variabel target memungkinkan analisis faktor-faktor yang memengaruhi keputusan nasabah dalam memilih produk deposito.<br><br>
            Dalam mata kuliah Teori Pengambilan Keputusan, dataset ini digunakan untuk menerapkan konsep Decision Under Certainty, Decision Under Risk (Expected Value), Probabilistic Modeling, Decision Under Uncertainty, Utility and Risk Preference, serta Sensitivity Analysis and Simulation. Melalui penerapan konsep-konsep tersebut, data dapat dimanfaatkan untuk menganalisis dan mengevaluasi berbagai alternatif strategi pemasaran bank berdasarkan tingkat kepastian, risiko, probabilitas, preferensi risiko, dan perubahan kondisi yang mungkin terjadi.<br><br>
            </span>
        </div>
        """, unsafe_allow_html=True)
        
    with col_desc2:
        st.markdown("""
        <div style="background:rgba(0,0,0,0.6); backdrop-filter:blur(2px); border-radius:14px; padding:1.2rem;">
            <span style="font-size:0.9rem; font-weight:700; color:#FFE4A0;">VARIABEL LAPORAN:</span><br>
            <div style="max-height: 400px; overflow-y: auto; margin-top: 10px;">
                <table style="width:100%; color:#D4C4A8; font-size:0.75rem; border-collapse: collapse; text-align: center;">
                    <thead>
                        <tr style="background: rgba(218,165,32,0.25);">
                            <th style="padding:10px 6px; text-align:center; color:#FFE4A0; font-weight:600; border-bottom:2px solid rgba(218,165,32,0.5);">No</th>
                            <th style="padding:10px 6px; text-align:center; color:#FFE4A0; font-weight:600; border-bottom:2px solid rgba(218,165,32,0.5);">Variabel</th>
                            <th style="padding:10px 6px; text-align:center; color:#FFE4A0; font-weight:600; border-bottom:2px solid rgba(218,165,32,0.5);">Keterangan</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">1</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">age</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">Usia nasabah</td></tr>
                        <tr><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">2</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">job</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">Jenis pekerjaan</td></tr>
                        <tr><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">3</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">marital</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">Status pernikahan</td></tr>
                        <tr><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">4</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">education</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">Tingkat pendidikan</td></tr>
                        <tr><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">5</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">default</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">Gagal bayar kredit</td></tr>
                        <tr><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">6</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">balance</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">Saldo rekening</td></tr>
                        <tr><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">7</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">housing</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">Pinjaman rumah</td></tr>
                        <tr><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">8</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">loan</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">Pinjaman pribadi</td></tr>
                        <tr><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">9</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">contact</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">Jenis komunikasi</td></tr>
                        <tr><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">10</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">day</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">Hari kontak terakhir</td></tr>
                        <tr><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">11</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">month</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">Bulan kontak terakhir</td></tr>
                        <tr><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">12</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">duration</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">Durasi panggilan</td></tr>
                        <tr><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">13</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">campaign</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">Jumlah kontak</td></tr>
                        <tr><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">14</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">pdays</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">Hari sejak kontak sebelumnya</td></tr>
                        <tr><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">15</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">previous</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">Jumlah kontak sebelumnya</td></tr>
                        <tr><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">16</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">poutcome</td><td style="padding:8px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.15);">Hasil kampanye sebelumnya</td></tr>
                        <tr style="background: rgba(218,165,32,0.12);">
                            <td style="padding:10px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.4); font-weight:700; color:#FFD700;">17</td>
                            <td style="padding:10px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.4); font-weight:700; color:#FFD700;">deposit</td>
                            <td style="padding:10px 6px; text-align:center; border-bottom:1px solid rgba(218,165,32,0.4); font-weight:700; color:#FFD700;">TARGET (yes/no)</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ========== STATISTIK CEPAT ==========
    
    # CSS untuk styling preview dataset
    st.markdown("""
    <style>
    /* Styling untuk judul PREVIEW DATASET */
    .preview-title {
        text-align: center;
        font-family: 'Georgia', 'Playfair Display', serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #FFE4A0;
        margin-bottom: 0.25rem;
        letter-spacing: 2px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .preview-subtitle {
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: #D4C4A8;
        margin-bottom: 1.5rem;
        letter-spacing: 1px;
    }
    
    /* Styling untuk tabel dataframe agar teks di tengah */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    
    .stDataFrame thead th {
        text-align: center !important;
        background: linear-gradient(135deg, #DAA520 0%, #B8860B 100%) !important;
        color: #1a1a2e !important;
        font-weight: 700 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        padding: 12px 8px !important;
        text-align: center !important;
    }
    
    .stDataFrame tbody td {
        text-align: center !important;
        font-size: 0.75rem !important;
        padding: 8px 6px !important;
        color: #E8E0D0 !important;
        vertical-align: middle !important;
    }
    
    /* Styling untuk tombol download */
    .download-bar {
        background: rgba(0, 0, 0, 0.4);
        border-radius: 12px;
        padding: 0.6rem 1rem;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        border: 1px solid rgba(218,165,32,0.25);
        display: flex;
        justify-content: flex-end;
        align-items: center;
    }
    
    .download-bar button {
        background: linear-gradient(135deg, rgba(218,165,32,0.15) 0%, rgba(218,165,32,0.05) 100%);
        color: #FFE4A0;
        border: 1px solid rgba(218,165,32,0.4);
        border-radius: 30px;
        padding: 0.35rem 1.2rem;
        font-size: 0.75rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
    }
    
    .download-bar button:hover {
        background: rgba(218,165,32,0.25);
        border-color: rgba(218,165,32,0.7);
        transform: translateY(-1px);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Judul PREVIEW DATASET dengan font lebih besar dan profesional
    st.markdown("""
    <div class="preview-title">PREVIEW DATASET</div>
    <div class="preview-subtitle">11.000 Records | 17 Variabel | Bank Marketing Dataset</div>
    """, unsafe_allow_html=True)
    
    # Card statistik
    col1, col2, col3, col4 = st.columns(4)
    
    total_rows = len(df)
    total_cols = len(df.columns)
    
    deposit_col = 'deposit' if 'deposit' in df.columns else None
    if deposit_col:
        deposit_yes = (df[deposit_col] == 'yes').sum()
        deposit_pct = (deposit_yes / total_rows) * 100
    
    with col1:
        st.markdown(f"""
        <div class="info-card-modern">
            <div class="info-content">
                <div class="info-value">{total_rows:,}</div>
                <div class="info-label">Total Records</div>
                <div class="info-separator"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="info-card-modern">
            <div class="info-content">
                <div class="info-value">{total_cols}</div>
                <div class="info-label">Total Features</div>
                <div class="info-separator"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="info-card-modern">
            <div class="info-content">
                <div class="info-value">{df['age'].mean():.0f}</div>
                <div class="info-label">Rata-rata Usia</div>
                <div class="info-separator"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="info-card-modern">
            <div class="info-content">
                <div class="info-value">{deposit_pct:.1f}%</div>
                <div class="info-label">Success Rate</div>
                <div class="info-separator"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
 
    # ========== DATA PREVIEW ==========
   
    # Konfigurasi kolom untuk tampilan tabel dengan teks di tengah
    column_config = {}
    
    for col in df.columns:
        if col == 'deposit':
            column_config[col] = st.column_config.TextColumn(
                col.upper(),
                help=f"Target variable: yes/no",
                width="small"
            )
        elif df[col].dtype in ['int64', 'float64']:
            if col in ['age', 'balance', 'duration', 'campaign', 'previous', 'pdays', 'day']:
                column_config[col] = st.column_config.NumberColumn(
                    col.upper(),
                    help=f"Kolom: {col}",
                    format="%d" if df[col].dtype == 'int64' else "%.2f"
                )
            else:
                column_config[col] = st.column_config.NumberColumn(
                    col.upper(),
                    help=f"Kolom: {col}",
                    format="%d"
                )
        else:
            column_config[col] = st.column_config.TextColumn(
                col.upper(),
                help=f"Kolom: {col}"
            )
    
    # Tampilkan dataframe
    st.dataframe(
        df.head(100),
        use_container_width=True,
        height=450,
        column_config=column_config,
        hide_index=True
    )
    
    # Tombol download CSV di bawah tabel (persegi panjang dari ujung ke ujung margin)
    csv_data = df.to_csv(index=False).encode('utf-8')
    
    st.markdown(f"""
    <div class="download-bar">
        <div style="flex-grow: 1;"></div>
        <div>
            <button onclick="document.getElementById('downloadBtn').click()" style="background: none; border: none; padding: 0;">
                📥 Export to CSV
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Download button yang tersembunyi (tetap menggunakan st.download_button)
    st.download_button(
        label="📥 Export to CSV",
        data=csv_data,
        file_name='bank_marketing_dataset.csv',
        mime='text/csv',
        key="download_dataset_preview",
        help="Download dataset lengkap dalam format CSV",
        use_container_width=False
    )
    
    # CSS untuk menyembunyikan tombol default Streamlit dan membuatnya lebih rapi
    st.markdown("""
    <style>
    /* Menyembunyikan teks default pada tombol download */
    div[data-testid="stDownloadButton"] button {
        display: none;
    }
    
    /* Tombol download custom yang terlihat */
    .download-bar button {
        background: linear-gradient(135deg, rgba(218,165,32,0.15) 0%, rgba(218,165,32,0.05) 100%);
        color: #FFE4A0;
        border: 1px solid rgba(218,165,32,0.4);
        border-radius: 30px;
        padding: 0.45rem 1.5rem;
        font-size: 0.8rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .download-bar button:hover {
        background: rgba(218,165,32,0.25);
        border-color: rgba(218,165,32,0.7);
        transform: translateY(-1px);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Menampilkan tombol download dengan JavaScript trigger
    # Alternative: Menggunakan st.columns untuk menempatkan tombol
    download_container = st.container()
    with download_container:
        col_download1, col_download2, col_download3 = st.columns([8, 1.5, 1])
        with col_download3:
            st.download_button(
                label="📥 Export to CSV",
                data=csv_data,
                file_name='bank_marketing_dataset.csv',
                mime='text/csv',
                key="download_dataset_final",
                help="Download dataset lengkap (11.000 records) dalam format CSV",
                use_container_width=True
            )
    
    st.markdown("---")


    # ========== 6 TAB ANALISIS ==========
    
    # CSS untuk styling judul dan tab yang lebih elegan
    st.markdown("""
    <style>
    /* Styling judul FRAMEWORK DECISION ANALYSIS - SAMA DENGAN PREVIEW DATASET */
    .framework-container {
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
    }
    
    .framework-title {
        font-family: 'Georgia', 'Playfair Display', serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #FFE4A0;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
        display: inline-block;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .framework-underline {
        width: 800px;
        height: 3px;
        background: linear-gradient(90deg, transparent, #DAA520, #FFE4A0, #DAA520, transparent);
        margin: 0.5rem auto 0;
        border-radius: 3px;
    }
    
    .framework-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: #A8885A;
        letter-spacing: 2px;
        margin-top: 0.75rem;
        text-transform: uppercase;
    }
    
    /* Styling tab yang lebih minimalis dan elegan */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.2rem;
        background-color: transparent;
        border-bottom: 1px solid rgba(218,165,32,0.3);
        padding: 0;
        margin-bottom: 1.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3.2rem;
        border-radius: 0;
        background-color: transparent;
        color: #A8885A;
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        font-weight: 500;
        letter-spacing: 0.8px;
        transition: all 0.3s ease;
        border: none;
        border-bottom: 2px solid transparent;
        margin: 0;
        padding: 0 1.2rem;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: transparent;
        color: #FFE4A0;
        border-bottom-color: rgba(218,165,32,0.5);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: transparent !important;
        color: #DAA520 !important;
        border-bottom: 2px solid #DAA520 !important;
    }
    
    /* Styling container tab content */
    .stTabs [data-baseweb="tab-panel"] {
        background-color: rgba(0, 0, 0, 0.25);
        border-radius: 12px;
        padding: 1.25rem;
        margin-top: 0;
        border: 1px solid rgba(218,165,32,0.15);
    }
    
    /* Card header untuk setiap tab */
    .tab-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(218,165,32,0.2);
    }
    
    .tab-icon {
        font-size: 2rem;
    }
    
    .tab-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        font-weight: 600;
        color: #FFE4A0;
        letter-spacing: 1px;
    }
    
    .tab-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        color: #A8885A;
        margin-top: 2px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Judul Framework Decision Analysis dengan font dan size sama seperti PREVIEW DATASET
    st.markdown("""
    <div class="framework-container">
        <div class="framework-title">FRAMEWORK DECISION ANALYSIS</div>
        <div class="framework-underline"></div>
        <div class="framework-subtitle">Bank Marketing Analytics</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Membuat 6 tab
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "CERTAINTY",
        "RISK (EV)",
        "UNCERTAINTY",
        "PROBABILISTIC",
        "UTILITY",
        "SENSITIVITY"
    ])
    
    with tab1:
        st.markdown("""
        <div class="tab-header">
            <span class="tab-icon">🎯</span>
            <div>
                <div class="tab-title">Decision Under Certainty</div>
                <div class="tab-subtitle">Analisis keputusan dengan informasi pasti</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        analysis_certainty(df)
    
    with tab2:
        st.markdown("""
        <div class="tab-header">
            <span class="tab-icon">⚖️</span>
            <div>
                <div class="tab-title">Decision Under Risk (Expected Value)</div>
                <div class="tab-subtitle">Analisis keputusan dengan probabilitas diketahui</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        analysis_risk(df)
    
    with tab3:
        st.markdown("""
        <div class="tab-header">
            <span class="tab-icon">🎲</span>
            <div>
                <div class="tab-title">Decision Under Uncertainty</div>
                <div class="tab-subtitle">Analisis keputusan tanpa probabilitas</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        analysis_uncertainty(df)
    
    with tab4:
        st.markdown("""
        <div class="tab-header">
            <span class="tab-icon">📐</span>
            <div>
                <div class="tab-title">Probabilistic Modeling</div>
                <div class="tab-subtitle">Pemodelan probabilitas dan distribusi data</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        analysis_probabilistic(df)
    
    with tab5:
        st.markdown("""
        <div class="tab-header">
            <span class="tab-icon">🎭</span>
            <div>
                <div class="tab-title">Utility & Risk Preference</div>
                <div class="tab-subtitle">Preferensi risiko dan fungsi utilitas</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        analysis_utility(df)
    
    with tab6:
        st.markdown("""
        <div class="tab-header">
            <span class="tab-icon">🔄</span>
            <div>
                <div class="tab-title">Sensitivity & Simulation</div>
                <div class="tab-subtitle">Analisis sensitivitas dan simulasi Monte Carlo</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        analysis_sensitivity(df)
    
    
    # ========== FOOTER ==========
    st.markdown("""
    <div class="footer">
        Dashboard Interaktif dengan Streamlit | Michael Dolly Sianturi | 4233260010 | 2026<br>
        6 Framework Decision Analysis: Certainty | Risk (EV) | Uncertainty | Probabilistic | Utility | Simulation
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)