# style.py
# File untuk menyimpan semua konfigurasi CSS dashboard

import streamlit as st

def apply_custom_css():
    """Menerapkan CSS kustom untuk dashboard"""
    
    # CSS Utama dengan Font Profesional
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@700;800&display=swap');
    
    /* Font dasar untuk seluruh dashboard */
    * {
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    /* Container utama cover */
    .cover-container {
        background-color: rgba(0, 0, 0, 0.55);
        backdrop-filter: blur(3px);
        border-radius: 28px;
        padding-top: 0.5rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        margin-top: 0rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        border: 1px solid rgba(255, 215, 0, 0.3);
    }
    
    .block-container {
        padding-top: 1rem !important;
    }
    
    /* Container judul - center sempurna */
    .title-container {
        text-align: center;
        width: 100%;
        margin-top: 0rem;
        padding-top: 0rem;
        margin-bottom: 0.5rem;
    }
    
    /* JUDUL UTAMA - Font Elegan */
    .main-title {
        font-family: 'Georgia', 'Georgia', serif;
        font-size: 8rem;
        font-weight: 900;
        letter-spacing: 6px;
        text-align: center;
        line-height: 1;
        margin: 0;
        padding: 0;
        text-transform: uppercase;
        background: linear-gradient(135deg, #FFFFFF 0%, #FFE4A0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 5px 5px 18px rgba(0,0,0,0.9);
        width: 100%;
    }
    
    /* SUB JUDUL - Font Modern */
    .sub-title {
        font-family: 'Inter', 'Segoe UI', sans-serif;
        font-size: 0.8rem;
        font-weight: 600;
        color: #FFE4B5;
        text-align: center;
        margin-top: 0.8rem;
        margin-bottom: 0;
        letter-spacing: 1.5px;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.4);
        border-bottom: 2px solid rgba(255, 215, 0, 0.6);
        display: inline-block;
        padding-bottom: 12px;
    }
    
    /* Kartu statistik */
    .stat-card {
        background-color: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(2px);
        border-radius: 20px;
        padding: 1rem 1.2rem;
        text-align: center;
        transition: all 0.2s ease;
        border: 1px solid rgba(255, 215, 0, 0.3);
    }
    
    .stat-number {
        font-family: 'Inter', monospace;
        font-size: 2rem;
        font-weight: 800;
        color: #FFE4A0;
        margin: 0;
    }
    
    .stat-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: #D4C4A8;
        font-weight: 500;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Tombol navigasi */
    .stButton > button {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        background-color: rgba(0, 0, 0, 0.7);
        color: #FFE4A0;
        border-radius: 40px;
        border: 1px solid rgba(255, 215, 0, 0.5);
    }
    
    /* Footer */
    .footer {
        font-family: 'Inter', sans-serif;
        text-align: center;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 215, 0, 0.3);
        font-size: 0.7rem;
        color: #D4C4A8;
    }
    
    /* Hilangkan space/header atas streamlit */
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
        height: 0px;
    }
    
    /* Hilangkan padding atas halaman */
    .block-container {
        padding-top: 0rem !important;
        margin-top: 0rem !important;
    }
    
    /* Hilangkan jarak default */
    .main {
        padding-top: 0rem !important;
    }
    
    /* Rapatkan container utama */
    section.main > div {
        padding-top: 0rem !important;
    }
    
    /* Card Info Modern */
    .info-card-modern {
        background: linear-gradient(135deg, rgba(0,0,0,0.75) 0%, rgba(30,30,50,0.8) 100%);
        backdrop-filter: blur(8px);
        border-radius: 20px;
        padding: 1.2rem 0.8rem;
        text-align: center;
        border: 1px solid rgba(255,215,0,0.3);
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .info-card-modern:hover {
        transform: translateY(-5px);
        border-color: rgba(255,215,0,0.7);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    .info-content {
        position: relative;
        z-index: 1;
    }
    
    .info-value {
        font-family: 'Inter', monospace;
        font-size: 2rem;
        font-weight: 800;
        color: #FFE4A0;
        margin: 0.2rem 0;
        letter-spacing: 1px;
    }
    
    .info-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: #D4C4A8;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 500;
    }
    
    .info-sub {
        font-family: 'Inter', sans-serif;
        font-size: 0.65rem;
        color: #A8885A;
        margin-top: 0.3rem;
    }
    
    .info-separator {
        width: 30px;
        height: 2px;
        background: rgba(255,215,0,0.4);
        margin: 8px auto 0 auto;
        border-radius: 2px;
    }
    
    /* Container tabel */
    .dataframe-container {
        background: rgba(0,0,0,0.4);
        border-radius: 20px;
        padding: 0.8rem;
        border: 1px solid rgba(255,215,0,0.25);
        margin-bottom: 1rem;
    }
    
    /* Header tabel */
    .dataframe-header {
        background: linear-gradient(135deg, rgba(255,215,0,0.2) 0%, rgba(255,215,0,0.08) 100%);
        border-radius: 14px;
        padding: 0.7rem 1rem;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid rgba(255,215,0,0.2);
    }
    
    .dataframe-title {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        color: #FFE4A0;
        letter-spacing: 1px;
    }
    
    .dataframe-stats {
        font-family: 'Inter', monospace;
        font-size: 0.7rem;
        color: #D4C4A8;
        background: rgba(0,0,0,0.4);
        padding: 0.25rem 0.8rem;
        border-radius: 20px;
    }
    
    /* Styling tabel Streamlit */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    
    .stDataFrame thead th {
        background: linear-gradient(135deg, #DAA520 0%, #B8860B 100%) !important;
        color: #1a1a2e !important;
        font-weight: 700 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        padding: 10px 8px !important;
        border-bottom: 2px solid rgba(255,215,0,0.5) !important;
    }
    
    .stDataFrame tbody tr {
        border-bottom: 1px solid rgba(255,215,0,0.08) !important;
        transition: all 0.15s ease !important;
    }
    
    .stDataFrame tbody tr:hover {
        background-color: rgba(255,215,0,0.08) !important;
        cursor: pointer !important;
    }
    
    .stDataFrame tbody tr:nth-child(even) {
        background-color: rgba(255,255,255,0.02) !important;
    }
    
    .stDataFrame tbody td {
        font-size: 0.7rem !important;
        padding: 8px 6px !important;
        color: #E8E0D0 !important;
    }
    
    .stDataFrame td:last-child {
        font-weight: 600 !important;
    }
    
    .stDataFrame tbody tr td:last-child {
        background-color: rgba(255,215,0,0.05) !important;
        border-left: 2px solid rgba(255,215,0,0.3) !important;
    }
    
    /* Scrollbar */
    .stDataFrame::-webkit-scrollbar {
        height: 6px;
        width: 6px;
    }
    
    .stDataFrame::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.3);
        border-radius: 10px;
    }
    
    .stDataFrame::-webkit-scrollbar-thumb {
        background: rgba(255,215,0,0.4);
        border-radius: 10px;
    }
    
    .stDataFrame::-webkit-scrollbar-thumb:hover {
        background: rgba(255,215,0,0.6);
    }
    
    /* Download button styling */
    div.stDownloadButton > button {
        background: linear-gradient(135deg, rgba(255,215,0,0.15) 0%, rgba(255,215,0,0.05) 100%);
        color: #FFE4A0;
        border: 1px solid rgba(255,215,0,0.3);
        border-radius: 40px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    div.stDownloadButton > button:hover {
        background: linear-gradient(135deg, rgba(255,215,0,0.25) 0%, rgba(255,215,0,0.15) 100%);
        border-color: rgba(255,215,0,0.6);
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)


def set_background_image(image_path):
    """Mengatur background website dengan gambar"""
    import base64
    from pathlib import Path
    
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        # Deteksi tipe file
        if image_path.lower().endswith('.jpg') or image_path.lower().endswith('.jpeg'):
            mime_type = "image/jpeg"
        elif image_path.lower().endswith('.png'):
            mime_type = "image/png"
        else:
            mime_type = "image/jpeg"
        
        background_css = f"""
        <style>
        .stApp {{
            background-image: url("data:{mime_type};base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}
        
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.7);
            z-index: 0;
            pointer-events: none;
        }}
        
        .main .block-container {{
            position: relative;
            z-index: 1;
        }}
        
        [data-testid="stSidebar"] {{
            background-color: rgba(253, 248, 240, 0.85);
        }}
        </style>
        """
        st.markdown(background_css, unsafe_allow_html=True)
        return True
    except Exception as e:
        st.error(f"Gagal memuat background: {e}")
        return False