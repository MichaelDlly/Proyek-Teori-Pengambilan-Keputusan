# analysis.py
# File untuk menyimpan semua fungsi analisis

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style untuk plot
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def load_dataset():
    """Memuat dataset dari file CSV"""
    try:
        df = pd.read_csv("dataset_final.csv", encoding='utf-8')
    except:
        try:
            df = pd.read_csv("dataset_final.csv", sep=';', encoding='utf-8')
        except:
            try:
                df = pd.read_excel("dataset_final.xlsx")
            except:
                # Data sintetis jika file tidak ditemukan
                st.warning("File dataset tidak ditemukan, menggunakan data sintetis")
                np.random.seed(42)
                n_rows = 11000
                data = {
                    'age': np.random.randint(18, 95, n_rows),
                    'job': np.random.choice(['admin.', 'technician', 'services', 'management', 'retired', 'blue-collar', 'unemployed'], n_rows),
                    'marital': np.random.choice(['married', 'single', 'divorced'], n_rows),
                    'education': np.random.choice(['primary', 'secondary', 'tertiary', 'unknown'], n_rows),
                    'default': np.random.choice(['no', 'yes'], n_rows, p=[0.95, 0.05]),
                    'balance': np.random.randint(-1000, 100000, n_rows),
                    'housing': np.random.choice(['yes', 'no'], n_rows),
                    'loan': np.random.choice(['yes', 'no'], n_rows, p=[0.15, 0.85]),
                    'contact': np.random.choice(['cellular', 'telephone', 'unknown'], n_rows),
                    'day': np.random.randint(1, 31, n_rows),
                    'month': np.random.choice(['may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'], n_rows),
                    'duration': np.random.randint(10, 5000, n_rows),
                    'campaign': np.random.randint(1, 50, n_rows),
                    'pdays': np.random.choice([-1] + list(range(1, 1000)), n_rows),
                    'previous': np.random.randint(0, 50, n_rows),
                    'poutcome': np.random.choice(['unknown', 'failure', 'success'], n_rows),
                    'deposit': np.random.choice(['yes', 'no'], n_rows, p=[0.53, 0.47])
                }
                df = pd.DataFrame(data)
    
    # Konversi target variabel menjadi numerik untuk analisis
    if 'deposit' in df.columns:
        df['deposit_binary'] = df['deposit'].map({'yes': 1, 'no': 0})
    
    return df

def analysis_certainty(df):
    """Analisis Decision Under Certainty dengan pendekatan payoff empiris"""
    st.header("Analisis Decision Under Certainty")
    
    # =========================================================
    # PENJELASAN MATERI DALAM 3 PARAGRAF DENGAN HIGHLIGHT
    # =========================================================
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); padding: 1.2rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #DAA520;">
        <p style="color: #F0E6D2; line-height: 1.6; margin-bottom: 1rem;">
            <span style="background: linear-gradient(120deg, rgba(218,165,32,0.2) 0%, rgba(218,165,32,0.2) 100%); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFE4A0;">Decision Under Certainty</span> 
            merupakan salah satu pendekatan dalam teori pengambilan keputusan yang mengasumsikan bahwa 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">setiap alternatif keputusan menghasilkan payoff yang diketahui dengan pasti</span>. 
            Dalam kondisi ini, tidak ada unsur ketidakpastian atau probabilitas yang perlu diperhitungkan karena 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">konsekuensi dari setiap tindakan sudah dapat diprediksi secara akurat</span> 
            berdasarkan data historis atau informasi yang tersedia.
        </p>
        <p style="color: #F0E6D2; line-height: 1.6; margin-bottom: 1rem;">
            Pendekatan ini sangat berguna ketika 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">hubungan antara tindakan dan hasil bersifat deterministik</span>, 
            sehingga pengambil keputusan dapat dengan mudah memilih alternatif yang memberikan 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">payoff tertinggi (maximization)</span> 
            atau kerugian terendah (minimization). Dalam konteks bisnis perbankan, analisis ini dapat diterapkan untuk 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">mengevaluasi strategi pemasaran berdasarkan data historis</span> 
            yang telah terekam, seperti tingkat keberhasilan kampanye deposito di masa lalu.
        </p>
        <p style="color: #F0E6D2; line-height: 1.6;">
            Kelemahan utama dari pendekatan ini adalah 
            <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #e74c3c;">mengabaikan dinamika lingkungan bisnis yang selalu berubah</span>, 
            sehingga keputusan yang dihasilkan mungkin tidak optimal jika kondisi pasar berfluktuasi. Oleh karena itu, 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">decision under certainty paling cocok digunakan pada situasi dengan stabilitas tinggi</span> 
            atau sebagai tahap awal eksplorasi sebelum beralih ke pendekatan yang lebih kompleks seperti 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">decision under risk atau decision under uncertainty</span>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # =========================================================
    # KONSEP DAN PENDEKATAN
    # =========================================================
    st.markdown("""
    <div style="background: rgba(0,0,0,0.4); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
        <b style="color: #FFE4A0; font-size: 1.05rem;">📌 Konsep Decision Under Certainty:</b><br>
        <span style="color: #D4C4A8;">1. Setiap alternatif strategi menghasilkan <span style="color: #FFD700; font-weight: 500;">payoff yang diketahui</span><br>
        2. Tidak ada <span style="color: #FFD700; font-weight: 500;">probabilitas atau risiko</span> yang diperhitungkan<br>
        3. Keputusan optimal dipilih berdasarkan <span style="color: #FFD700; font-weight: 500;">payoff tertinggi</span><br>
        4. Hasil empiris historis dianggap sebagai <span style="color: #FFD700; font-weight: 500;">kepastian masa depan</span></span><br><br>
        <b style="color: #FFE4A0; font-size: 1.05rem;">📌 Pendekatan ini cocok untuk:</b><br>
        <span style="color: #D4C4A8;">• <span style="color: #FFD700;">Situasi dengan stabilitas tinggi</span> (lingkungan bisnis yang relatif tetap)<br>
        • <span style="color: #FFD700;">Tahap awal eksplorasi strategi</span> sebelum melakukan analisis lebih kompleks<br>
        • <span style="color: #FFD700;">Perbandingan baseline</span> antar alternatif strategi pemasaran</span>
    </div>
    """, unsafe_allow_html=True)
    
    # =========================================================
    # PENENTUAN KRITERIA STRATEGI (DALAM BENTUK CARD RAPI)
    # =========================================================
    st.subheader("Kriteria Strategi Pemasaran")
    
    # Menggunakan persentil ke-75 sebagai batasan "TINGGI"
    balance_threshold = df['balance'].quantile(0.75)
    age_threshold = df['age'].quantile(0.75)
    duration_threshold = df['duration'].quantile(0.75)
    
    # CSS untuk card yang rapi dan sejajar
    st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, rgba(46,204,113,0.15) 0%, rgba(46,204,113,0.05) 100%);
        border: 1px solid rgba(46,204,113,0.3);
        border-radius: 16px;
        padding: 0.8rem 0.5rem;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
    }
    .metric-card:hover {
        background: linear-gradient(135deg, rgba(46,204,113,0.25) 0%, rgba(46,204,113,0.1) 100%);
        border-color: rgba(46,204,113,0.6);
        transform: translateY(-3px);
    }
    .metric-value {
        font-family: 'Inter', monospace;
        font-size: 1.1rem;
        font-weight: 700;
        color: #2ecc71;
        margin: 0.2rem 0;
    }
    .metric-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        color: #D4C4A8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.3rem;
    }
    .metric-desc {
        font-family: 'Inter', sans-serif;
        font-size: 0.6rem;
        color: #A8885A;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">💰 Batasan Balance Tinggi</div>
            <div class="metric-value">> {balance_threshold:,.0f}</div>
            <div class="metric-desc">Kuartil atas (75%)</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">👤 Batasan Usia Tua</div>
            <div class="metric-value">> {age_threshold:.0f} tahun</div>
            <div class="metric-desc">Kuartil atas (75%)</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">⏱️ Batasan Durasi Tinggi</div>
            <div class="metric-value">> {duration_threshold:.0f} detik</div>
            <div class="metric-desc">Kuartil atas (75%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    # =========================================================
    # PERHITUNGAN PAYOFF SETIAP STRATEGI
    # =========================================================
    # Payoff didefinisikan sebagai tingkat keberhasilan deposit (%)
    
    # STRATEGI A1: Fokus nasabah balance tinggi
    balance_high = df[df['balance'] > balance_threshold]
    payoff_balance = balance_high['deposit_binary'].mean() * 100
    
    # STRATEGI A2: Fokus nasabah usia tua
    age_old = df[df['age'] > age_threshold]
    payoff_age = age_old['deposit_binary'].mean() * 100
    
    # STRATEGI A3: Fokus durasi panggilan tinggi
    duration_high = df[df['duration'] > duration_threshold]
    payoff_duration = duration_high['deposit_binary'].mean() * 100
    
    # STRATEGI A4: Hubungi seluruh nasabah
    payoff_all = df['deposit_binary'].mean() * 100
    
    # Kompilasi hasil
    alternatif = pd.DataFrame({
        'Kode': ['A1', 'A2', 'A3', 'A4'],
        'Strategi': ['Balance Tinggi', 'Usia Tua', 'Durasi Tinggi', 'Semua Nasabah'],
        'Payoff (%)': [payoff_balance, payoff_age, payoff_duration, payoff_all],
        'Jumlah Sampel': [len(balance_high), len(age_old), len(duration_high), len(df)],
        'Kasus Sukses': [
            balance_high['deposit_binary'].sum(),
            age_old['deposit_binary'].sum(),
            duration_high['deposit_binary'].sum(),
            df['deposit_binary'].sum()
        ]
    })
    
    st.subheader("Tabel Payoff Masing-Masing Strategi")
    
    # CSS untuk tabel dengan teks di tengah
    st.markdown("""
    <style>
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
        padding: 12px 8px !important;
    }
    .stDataFrame tbody td {
        text-align: center !important;
        font-size: 0.75rem !important;
        padding: 10px 8px !important;
        color: #E8E0D0 !important;
        vertical-align: middle !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.dataframe(alternatif, use_container_width=True, hide_index=True)
    
    # =========================================================
    # OPTIMALISASI KEPUTUSAN
    # =========================================================
    st.subheader("Penentuan Strategi Optimal")
    
    strategi_optimal = alternatif.loc[alternatif['Payoff (%)'].idxmax()]
    
    # CSS untuk styling card keputusan
    st.markdown("""
    <style>
    .decision-card {
        background: linear-gradient(135deg, rgba(255,215,0,0.15) 0%, rgba(255,215,0,0.05) 100%);
        border-left: 4px solid #FFD700;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .decision-title {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        font-weight: 700;
        color: #FFD700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }
    .decision-value {
        font-family: 'Georgia', serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #FFE4A0;
        margin: 0.3rem 0;
    }
    .decision-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        color: #D4C4A8;
        margin-top: 0.2rem;
    }
    .highlight-kuning {
        background: rgba(255,215,0,0.25);
        padding: 0.15rem 0.4rem;
        border-radius: 6px;
        font-weight: 600;
        color: #FFD700;
    }
    .ranking-card {
        background: rgba(0,0,0,0.35);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(255,215,0,0.2);
    }
    .ranking-item {
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(255,215,0,0.1);
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: #D4C4A8;
    }
    .ranking-item:last-child {
        border-bottom: none;
    }
    .ranking-number {
        display: inline-block;
        width: 24px;
        height: 24px;
        background: rgba(255,215,0,0.2);
        border-radius: 50%;
        text-align: center;
        line-height: 24px;
        font-size: 0.7rem;
        font-weight: 700;
        color: #FFD700;
        margin-right: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="decision-card">
            <div class="decision-title">REKOMENDASI KEPUTUSAN</div>
            <div class="decision-value">Implementasikan <span class="highlight-kuning">{strategi_optimal['Kode']}</span></div>
            <div class="decision-label">Nama Strategi</div>
            <div class="decision-value" style="font-size: 1rem;">{strategi_optimal['Strategi']}</div>
            <div class="decision-label">Ekspektasi Payoff</div>
            <div class="decision-value">{strategi_optimal['Payoff (%)']:.2f}%</div>
            <div class="decision-label">Key Performance Indicator</div>
            <div class="decision-value" style="font-size: 1rem;">{strategi_optimal['Payoff (%)']:.2f}% deposit success rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Baseline Ranking
        baseline = alternatif.sort_values('Payoff (%)', ascending=False).reset_index(drop=True)
        ranking_html = '<div class="ranking-card"><div class="decision-title">BASELINE RANKING STRATEGI</div>'
        for idx, row in baseline.iterrows():
            ranking_html += f'''
            <div class="ranking-item">
                <span class="ranking-number">{idx+1}</span>
                <span style="font-weight: 600; color: #FFE4A0;">{row['Kode']}</span> - {row['Strategi']}
                <span style="float: right; color: #FFD700; font-weight: 600;">{row['Payoff (%)']:.2f}%</span>
                <br><span style="font-size: 0.65rem; color: #A8885A; margin-left: 34px;">Cakupan: {row['Jumlah Sampel']:,} nasabah</span>
            </div>
            '''
            ranking_html += '</div>'
        st.markdown(ranking_html, unsafe_allow_html=True)
    
    
    # =========================================================
    # VISUALISASI KOMPARATIF (INTERAKTIF DENGAN PLOTLY)
    # =========================================================

    import plotly.graph_objects as go
    
    # Grafik 1: Perbandingan Payoff (Interaktif)
    fig1 = go.Figure()
    
    fig1.add_trace(go.Bar(
        x=alternatif['Strategi'],
        y=alternatif['Payoff (%)'],
        text=alternatif['Payoff (%)'].round(1),
        textposition='outside',
        marker_color=['#2ecc71', '#3498db', '#e74c3c', '#f39c12'],
        hovertemplate='<b>%{x}</b><br>Payoff: %{y:.1f}%<extra></extra>',
        name='Payoff (%)'
    ))
    
    fig1.update_layout(
        title=dict(text='<b>Perbandingan Payoff Antar Strategi</b>', font=dict(size=14, color='#FFE4A0'), x=0.5),
        xaxis=dict(title='Alternatif Strategi', title_font=dict(size=12, color='#D4C4A8'), tickfont=dict(size=11, color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title='Tingkat Keberhasilan Deposit (%)', title_font=dict(size=12, color='#D4C4A8'), tickfont=dict(size=11, color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hoverlabel=dict(bgcolor='rgba(0,0,0,0.8)', font_size=12),
        margin=dict(t=50, b=50, l=50, r=50),
        height=500
    )
    
    st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': True})
    
    # Grafik 2: Jumlah Sampel per Strategi (Interaktif)
    fig2 = go.Figure()
    
    fig2.add_trace(go.Bar(
        x=alternatif['Strategi'],
        y=alternatif['Jumlah Sampel'],
        text=alternatif['Jumlah Sampel'].apply(lambda x: f'{x:,}'),
        textposition='outside',
        marker_color=['#2ecc71', '#3498db', '#e74c3c', '#f39c12'],
        hovertemplate='<b>%{x}</b><br>Jumlah Sampel: %{y:,} nasabah<extra></extra>',
        name='Jumlah Sampel'
    ))
    
    fig2.update_layout(
        title=dict(text='<b>Cakupan Populasi per Strategi</b>', font=dict(size=14, color='#FFE4A0'), x=0.5),
        xaxis=dict(title='Alternatif Strategi', title_font=dict(size=12, color='#D4C4A8'), tickfont=dict(size=11, color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title='Jumlah Nasabah', title_font=dict(size=12, color='#D4C4A8'), tickfont=dict(size=11, color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hoverlabel=dict(bgcolor='rgba(0,0,0,0.8)', font_size=12),
        margin=dict(t=50, b=50, l=50, r=50),
        height=500
    )
    
    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': True})
    
    # =========================================================
    # ANALISIS KORELASI PREDIKTOR
    # =========================================================
    st.subheader("Analisis Kekuatan Prediktor")
    
    # Hitung korelasi dengan target variabel
    numeric_cols = ['duration', 'balance', 'age', 'deposit_binary']
    available_cols = [col for col in numeric_cols if col in df.columns]
    
    if len(available_cols) >= 2:
        korelasi = df[available_cols].corr()
        if 'deposit_binary' in korelasi.columns:
            kekuatan_prediktor = korelasi['deposit_binary'].drop('deposit_binary').sort_values(ascending=False)
            
            corr_data = pd.DataFrame({
                'Variabel': kekuatan_prediktor.index,
                'Korelasi dengan Deposit': kekuatan_prediktor.values
            })
            st.dataframe(corr_data, use_container_width=True, hide_index=True)
            
            for var, nilai in kekuatan_prediktor.items():
                if nilai > 0.3:
                    st.success(f"✓ **{var.capitalize()}**: {nilai:.4f} → Indikator kuat untuk strategi fokus")
                elif nilai > 0.1:
                    st.info(f"ℹ️ **{var.capitalize()}**: {nilai:.4f} → Indikator moderat")
                else:
                    st.warning(f"⚠️ **{var.capitalize()}**: {nilai:.4f} → Indikator lemah")
    
    # =========================================================
    # REKOMENDASI MANAJERIAL
    # =========================================================
    st.subheader("Rekomendasi Manajerial")
    st.markdown(f"""
    <div style="background: rgba(0,0,0,0.4); padding: 1.5rem; border-radius: 10px; line-height: 1.8;">
    <p style="color: #F0E6D2; margin-bottom: 1rem;">
        <span style="color: #FFE4A0; font-weight: 700;">1. PRIORITAS UTAMA</span><br>
        Bank sebaiknya <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">mengimplementasikan strategi {strategi_optimal['Strategi']}</span> 
        karena memberikan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">ekspektasi payoff tertinggi sebesar {strategi_optimal['Payoff (%)']:.2f}%</span>.
    </p>
        
    <p style="color: #F0E6D2; margin-bottom: 1rem;">
        <span style="color: #FFE4A0; font-weight: 700;">2. JUSTIFIKASI</span><br>
        Keputusan ini didasarkan pada <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">evaluasi dari {len(df):,} observasi historis</span> 
        yang menunjukkan bahwa strategi ini memiliki <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">nilai payoff tertinggi</span> 
        dibandingkan alternatif lainnya, serta didukung oleh <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">korelasi positif yang kuat dengan deposit success</span>.
    </p>
        
    <p style="color: #F0E6D2; margin-bottom: 1rem;">
        <span style="color: #FFE4A0; font-weight: 700;">3. EFISIENSI OPERASIONAL</span><br>
        Strategi ini hanya perlu <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">memfokuskan sumber daya pada {strategi_optimal['Jumlah Sampel']:,} nasabah</span> 
        sehingga <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">tidak perlu mengalokasikan biaya ke seluruh populasi</span>, 
        yang berarti terjadi <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">optimalisasi biaya pemasaran</span> secara signifikan.
    </p>
        
    <p style="color: #F0E6D2; margin-bottom: 1rem;">
        <span style="color: #FFE4A0; font-weight: 700;">4. KETERBATASAN MODEL</span><br>
        Perlu dipahami bahwa model ini <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #e74c3c;">mengasumsikan kondisi masa depan identik dengan historis</span> 
        dan <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #e74c3c;">tidak memperhitungkan ketidakpastian pasar</span>. 
        Payoff yang dihasilkan bersifat <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #e74c3c;">tetap tanpa interval keyakinan</span>, 
        sehingga perlu diantisipasi jika terjadi perubahan kondisi ekonomi.
    </p>
        
    <p style="color: #F0E6D2; margin-bottom: 0;">
        <span style="color: #FFE4A0; font-weight: 700;">5. TAHAP SELANJUTNYA</span><br>
        Disarankan untuk melakukan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">perluasan ke decision under risk</span> dengan mempertimbangkan probabilitas, 
        <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">analisis sensitivitas perubahan threshold</span> 
        untuk menguji ketahanan keputusan, serta <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">evaluasi trade-off antara payoff dan cakupan populasi</span>.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    

# analysis.py
# File untuk menyimpan semua fungsi analisis

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Set style untuk plot
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("Set2")

def load_dataset():
    """Memuat dataset dari file CSV"""
    try:
        df = pd.read_csv("dataset_final.csv", encoding='utf-8')
    except:
        try:
            df = pd.read_csv("dataset_final.csv", sep=';', encoding='utf-8')
        except:
            try:
                df = pd.read_excel("dataset_final.xlsx")
            except:
                # Data sintetis jika file tidak ditemukan
                st.warning("File dataset tidak ditemukan, menggunakan data sintetis")
                np.random.seed(42)
                n_rows = 11000
                data = {
                    'age': np.random.randint(18, 95, n_rows),
                    'job': np.random.choice(['admin.', 'technician', 'services', 'management', 'retired', 'blue-collar', 'unemployed'], n_rows),
                    'marital': np.random.choice(['married', 'single', 'divorced'], n_rows),
                    'education': np.random.choice(['primary', 'secondary', 'tertiary', 'unknown'], n_rows),
                    'default': np.random.choice(['no', 'yes'], n_rows, p=[0.95, 0.05]),
                    'balance': np.random.randint(-1000, 100000, n_rows),
                    'housing': np.random.choice(['yes', 'no'], n_rows),
                    'loan': np.random.choice(['yes', 'no'], n_rows, p=[0.15, 0.85]),
                    'contact': np.random.choice(['cellular', 'telephone', 'unknown'], n_rows),
                    'day': np.random.randint(1, 31, n_rows),
                    'month': np.random.choice(['may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'jan', 'feb', 'mar', 'apr'], n_rows),
                    'duration': np.random.randint(10, 5000, n_rows),
                    'campaign': np.random.randint(1, 50, n_rows),
                    'pdays': np.random.choice([-1] + list(range(1, 1000)), n_rows),
                    'previous': np.random.randint(0, 50, n_rows),
                    'poutcome': np.random.choice(['unknown', 'failure', 'success'], n_rows),
                    'deposit': np.random.choice(['yes', 'no'], n_rows, p=[0.53, 0.47])
                }
                df = pd.DataFrame(data)
    
    # Konversi target variabel menjadi numerik untuk analisis
    if 'deposit' in df.columns:
        df['deposit_binary'] = df['deposit'].map({'yes': 1, 'no': 0})
    
    return df



def analysis_risk(df):
    """Analisis Decision Under Risk - Expected Value (EV)"""
    st.header("Analisis Decision Under Risk - Expected Value (EV)")
    
    # =========================================================
    # PENJELASAN MATERI DALAM 3 PARAGRAF DENGAN HIGHLIGHT
    # =========================================================
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); padding: 1.2rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #DAA520;">
        <p style="color: #F0E6D2; line-height: 1.6; margin-bottom: 1rem;">
            <span style="background: linear-gradient(120deg, rgba(218,165,32,0.2) 0%, rgba(218,165,32,0.2) 100%); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFE4A0;">Decision Under Risk</span> 
            merupakan pendekatan pengambilan keputusan dimana 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">probabilitas terjadinya setiap kondisi alam diketahui atau dapat diestimasi</span>. 
            Dalam situasi ini, pengambil keputusan tidak lagi menghadapi ketidakpastian total karena 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">setiap alternatif strategi memiliki sebaran probabilitas hasil yang jelas</span>, 
            sehingga risiko dapat diukur dan diperhitungkan secara kuantitatif.
        </p>
        <p style="color: #F0E6D2; line-height: 1.6; margin-bottom: 1rem;">
            Inti dari pendekatan ini adalah konsep 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Expected Value (EV) atau Nilai Ekspektasi</span>, 
            yang dihitung dengan rumus <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">EV = Σ(Probabilitas × Payoff)</span>. 
            Keputusan optimal dalam kondisi risiko adalah 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">memilih alternatif yang memberikan nilai EV tertinggi</span>, 
            karena secara statistik akan menghasilkan keuntungan terbesar dalam jangka panjang. 
            Dalam konteks perbankan, analisis ini sangat berguna untuk 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">mengevaluasi strategi pemasaran berdasarkan probabilitas keberhasilan historis</span>.
        </p>
        <p style="color: #F0E6D2; line-height: 1.6;">
            Keunggulan utama pendekatan ini adalah 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">mampu mengkuantifikasi risiko dan memberikan rekomendasi yang terukur</span>, 
            namun kelemahannya adalah <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #e74c3c;">mengasumsikan probabilitas bersifat stasioner</span> 
            dan <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #e74c3c;">mengabaikan preferensi risiko pengambil keputusan</span>. 
            Pendekatan ini paling cocok digunakan ketika 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">data historis tersedia dan probabilitas dapat diestimasi dengan baik</span>, 
            serta pengambil keputusan bersifat <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">risk neutral (netral terhadap risiko)</span>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # =========================================================
    # KONSEP DAN PENDEKATAN
    # =========================================================
    st.markdown("""
    <div style="background: rgba(0,0,0,0.4); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
        <b style="color: #FFE4A0; font-size: 1.05rem;">📌 Konsep Decision Under Risk (Expected Value):</b><br>
        <span style="color: #D4C4A8;">1. Probabilitas setiap kejadian <span style="color: #FFD700; font-weight: 500;">diketahui atau dapat diestimasi</span><br>
        2. Keputusan optimal dipilih berdasarkan <span style="color: #FFD700; font-weight: 500;">Expected Value (EV) tertinggi</span><br>
        3. EV dihitung dengan rumus <span style="color: #FFD700; font-weight: 500;">EV = Σ(Probabilitas × Payoff)</span><br>
        4. Mengasumsikan pengambil keputusan bersifat <span style="color: #FFD700; font-weight: 500;">risk neutral</span></span><br><br>
        <b style="color: #FFE4A0; font-size: 1.05rem;">📌 Pendekatan ini cocok untuk:</b><br>
        <span style="color: #D4C4A8;">• <span style="color: #FFD700;">Situasi dengan data historis yang memadai</span> untuk estimasi probabilitas<br>
        • <span style="color: #FFD700;">Evaluasi strategi pemasaran</span> dengan mempertimbangkan tingkat keberhasilan masa lalu<br>
        • <span style="color: #FFD700;">Perbandingan kuantitatif</span> antar alternatif strategi yang memiliki profil risiko berbeda</span>
    </div>
    """, unsafe_allow_html=True)
    
    # =========================================================
    # 1. PERHITUNGAN PROBABILITAS EMPIRIS (DALAM BENTUK CARD)
    # =========================================================
    st.subheader("Probabilitas Empiris dari Data Historis")
    
    # CSS untuk card probabilitas
    st.markdown("""
    <style>
    .prob-card {
        background: linear-gradient(135deg, rgba(255,215,0,0.1) 0%, rgba(255,215,0,0.02) 100%);
        border: 1px solid rgba(255,215,0,0.3);
        border-radius: 16px;
        padding: 1rem 0.8rem;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
    }
    .prob-card:hover {
        background: linear-gradient(135deg, rgba(255,215,0,0.2) 0%, rgba(255,215,0,0.05) 100%);
        border-color: rgba(255,215,0,0.6);
        transform: translateY(-3px);
    }
    .prob-value {
        font-family: 'Georgia', serif;
        font-size: 2rem;
        font-weight: 700;
        color: #FFD700;
        margin: 0.2rem 0;
    }
    .prob-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: #D4C4A8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.3rem;
    }
    .prob-desc {
        font-family: 'Inter', sans-serif;
        font-size: 0.65rem;
        color: #A8885A;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if 'deposit_binary' in df.columns:
        p_success = df['deposit_binary'].mean()
        p_failure = 1 - p_success
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="prob-card">
                <div class="prob-label">✅ P(Success)</div>
                <div class="prob-value">{p_success*100:.2f}%</div>
                <div class="prob-desc">Probabilitas Nasabah Membuka Deposito</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="prob-card">
                <div class="prob-label">❌ P(Failure)</div>
                <div class="prob-value">{p_failure*100:.2f}%</div>
                <div class="prob-desc">Probabilitas Nasabah Tidak Membuka Deposito</div>
            </div>
            """, unsafe_allow_html=True)
    
    # =========================================================
    # 2. PERHITUNGAN EXPECTED VALUE (EV) UNTUK SETIAP ALTERNATIF
    # =========================================================
    st.subheader("Perhitungan Expected Value (EV) untuk Setiap Alternatif")
    
    # Menampilkan rumus dengan format equation
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); padding: 0.8rem 1rem; border-radius: 10px; margin-bottom: 1rem; text-align: center;">
        <span style="font-family: monospace; font-size: 1.2rem; color: #FFD700;">
        <b> E(V) = Σ P(s) × X(s)</b>
        </span>
        <span style="color: #D4C4A8; margin-left: 1rem;">atau</span>
        <span style="font-family: monospace; font-size: 1.2rem; color: #FFD700;">
        <b> EV = P(Yes) × Profit_Yes + P(No) × Profit_No</b>
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Alternatif strategi pemasaran
    alternatives = [
        "Kontak Cellular",
        "Kontak Telephone",
        "Email Campaign",
        "Direct Mail"
    ]
    
    # Payoff jika sukses dan gagal (dalam ribuan unit)
    payoff_success = [850, 620, 700, 580]
    payoff_failure = [450, 380, 420, 350]
    
    if 'deposit_binary' in df.columns:
        p_success = df['deposit_binary'].mean()
        p_failure = 1 - p_success
        
        # Hitung EV untuk setiap alternatif
        ev_values = []
        for i in range(len(alternatives)):
            ev = (p_success * payoff_success[i]) + (p_failure * payoff_failure[i])
            ev_values.append(ev)
        
        # Tentukan alternatif dengan EV tertinggi
        best_idx = ev_values.index(max(ev_values))
        best_alternative = alternatives[best_idx]
        best_ev = ev_values[best_idx]
        
        # Buat dataframe hasil EV untuk tabel interaktif
        ev_df = pd.DataFrame({
            'Alternatif': alternatives,
            'Payoff Success': payoff_success,
            'Payoff Failure': payoff_failure,
            f'EV (P_success={p_success:.2%})': ev_values
        })
        
        # Tabel interaktif dengan st.dataframe dan styling
        st.markdown("""
        <style>
        .ev-table-label {
            font-family: 'Inter', sans-serif;
            font-size: 0.8rem;
            color: #D4C4A8;
            margin-bottom: 0.5rem;
            font-style: italic;
        }
        </style>
        <div class="ev-table-label">Tabel Perhitungan Expected Value setiap Alternatif:</div>
        """, unsafe_allow_html=True)
        
        st.dataframe(
            ev_df.style.format({
                'Payoff Success': '{:,.0f}',
                'Payoff Failure': '{:,.0f}',
                f'EV (P_success={p_success:.2%})': '{:,.2f}'
            }).set_properties(**{'text-align': 'center'}),
            use_container_width=True,
            hide_index=True
        )
        
        # Card untuk keputusan optimal
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(46,204,113,0.15) 0%, rgba(46,204,113,0.05) 100%); border-left: 4px solid #2ecc71; border-radius: 12px; padding: 1rem; margin: 1rem 0;">
            <div style="display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;">
                <span style="font-size: 2rem;">🏆</span>
                <div>
                    <div style="font-family: 'Inter', sans-serif; font-size: 0.7rem; color: #2ecc71; text-transform: uppercase; letter-spacing: 1px;">KEPUTUSAN OPTIMAL</div>
                    <div style="font-family: 'Georgia', serif; font-size: 1.3rem; font-weight: 700; color: #FFE4A0;">{best_alternative}</div>
                    <div style="font-family: 'Inter', sans-serif; font-size: 0.75rem; color: #D4C4A8;">Expected Value (EV): <span style="color: #FFD700; font-weight: 700;">{best_ev:,.0f} unit</span></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Ranking alternatif (tabel interaktif)
        st.subheader("Ranking Alternatif Berdasarkan Expected Value")
        ranking_df = ev_df.copy()
        ranking_df['Ranking'] = ranking_df[f'EV (P_success={p_success:.2%})'].rank(ascending=False).astype(int)
        ranking_df = ranking_df.sort_values('Ranking')
        ranking_display = ranking_df[['Ranking', 'Alternatif', f'EV (P_success={p_success:.2%})']]
        
        st.dataframe(
            ranking_display.style.format({f'EV (P_success={p_success:.2%})': '{:,.2f}'}).set_properties(**{'text-align': 'center'}),
            use_container_width=True,
            hide_index=True
        )
    
    # =========================================================
    # 3. VISUALISASI PERBANDINGAN EXPECTED VALUE (INTERAKTIF)
    # =========================================================
    st.subheader("Visualisasi Perbandingan Expected Value")
    
    import plotly.graph_objects as go
    
    fig1 = go.Figure()
    
    fig1.add_trace(go.Bar(
        x=alternatives,
        y=ev_values,
        text=[f'{v:,.0f}' for v in ev_values],
        textposition='outside',
        marker_color=['#e74c3c' if i == best_idx else '#3498db' for i in range(len(alternatives))],
        marker_line=dict(width=2, color='#FFD700') if best_idx is not None else None,
        hovertemplate='<b>%{x}</b><br>Expected Value: %{y:,.0f} unit<extra></extra>',
        name='Expected Value'
    ))
    
    fig1.update_layout(
        title=dict(text='<b>Perbandingan Expected Value (EV) Antar Alternatif Strategi</b>', font=dict(size=14, color='#FFE4A0'), x=0.5),
        xaxis=dict(title='Alternatif Strategi Pemasaran', title_font=dict(size=12, color='#D4C4A8'), tickfont=dict(size=11, color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title='Expected Value (dalam ribuan unit)', title_font=dict(size=12, color='#D4C4A8'), tickfont=dict(size=11, color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hoverlabel=dict(bgcolor='rgba(0,0,0,0.8)', font_size=12),
        margin=dict(t=50, b=50, l=50, r=50),
        height=500
    )
    
    st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': True})
    
    # =========================================================
    # 4. ANALISIS SENSITIVITAS PROBABILITAS
    # =========================================================
    st.subheader("Analisis Sensitivitas - Pengaruh Perubahan Probabilitas")
    
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); padding: 0.8rem; border-radius: 10px; margin-bottom: 1rem;">
        <span style="color: #D4C4A8;">Analisis ini menunjukkan bagaimana perubahan probabilitas sukses (P_success) 
        mempengaruhi Expected Value dari setiap alternatif strategi.</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Slider untuk mengubah probabilitas sukses
    sensitivity_p = st.slider(
        "Ubah Probabilitas Sukses (P_success)", 
        min_value=0.0, 
        max_value=1.0, 
        value=float(p_success),
        step=0.01,
        help="Geser untuk melihat bagaimana perubahan probabilitas mempengaruhi EV setiap alternatif"
    )
    
    # Hitung ulang EV dengan probabilitas baru
    sensitivity_failure = 1 - sensitivity_p
    ev_sensitivity = []
    for i in range(len(alternatives)):
        ev = (sensitivity_p * payoff_success[i]) + (sensitivity_failure * payoff_failure[i])
        ev_sensitivity.append(ev)
    
    # Tampilkan hasil sensitivitas dalam tabel interaktif
    sensitivity_df = pd.DataFrame({
        'Alternatif': alternatives,
        f'EV (P_success={sensitivity_p:.2%})': ev_sensitivity
    })
    
    st.dataframe(
        sensitivity_df.style.format({f'EV (P_success={sensitivity_p:.2%})': '{:,.2f}'}).set_properties(**{'text-align': 'center'}),
        use_container_width=True,
        hide_index=True
    )
    
    # Tentukan alternatif terbaik pada probabilitas baru
    best_sensitivity_idx = ev_sensitivity.index(max(ev_sensitivity))
    best_sensitivity_alt = alternatives[best_sensitivity_idx]
    
    if best_sensitivity_alt == best_alternative:
        st.success(f"✅ Pada P_success = {sensitivity_p:.2%}, alternatif terbaik tetap: **{best_sensitivity_alt}**")
    else:
        st.warning(f"⚠️ Pada P_success = {sensitivity_p:.2%}, alternatif terbaik berubah menjadi: **{best_sensitivity_alt}**")
    
    # Visualisasi sensitivitas dengan plotly interaktif
    fig2 = go.Figure()
    
    fig2.add_trace(go.Bar(
        x=alternatives,
        y=ev_values,
        name=f'P_success = {p_success:.2%}',
        marker_color='skyblue',
        text=[f'{v:,.0f}' for v in ev_values],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>EV: %{y:,.0f} unit<extra></extra>'
    ))
    
    fig2.add_trace(go.Bar(
        x=alternatives,
        y=ev_sensitivity,
        name=f'P_success = {sensitivity_p:.2%}',
        marker_color='lightcoral',
        text=[f'{v:,.0f}' for v in ev_sensitivity],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>EV: %{y:,.0f} unit<extra></extra>'
    ))
    
    fig2.update_layout(
        title=dict(text='<b>Analisis Sensitivitas Expected Value</b>', font=dict(size=14, color='#FFE4A0'), x=0.5),
        xaxis=dict(title='Alternatif Strategi', title_font=dict(size=12, color='#D4C4A8'), tickfont=dict(size=11, color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title='Expected Value', title_font=dict(size=12, color='#D4C4A8'), tickfont=dict(size=11, color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hoverlabel=dict(bgcolor='rgba(0,0,0,0.8)', font_size=12),
        barmode='group',
        margin=dict(t=50, b=50, l=50, r=50),
        height=500
    )
    
    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': True})
    
    # =========================================================
    # 5. KESIMPULAN DAN REKOMENDASI (DALAM BENTUK PARAGRAF DENGAN HIGHLIGHT)
    # =========================================================
    st.subheader("Kesimpulan dan Rekomendasi")
    
    st.markdown(f"""
    <div style="background: rgba(0,0,0,0.4); padding: 1.5rem; border-radius: 10px; line-height: 1.8;">
    <p style="color: #F0E6D2; margin-bottom: 1rem;">
        <span style="color: #FFE4A0; font-weight: 700;">1. PROBABILITAS HISTORIS</span><br>
        Berdasarkan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">data historis dari {len(df):,} nasabah</span>, 
        diperoleh <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">probabilitas sukses deposit sebesar {p_success*100:.2f}%</span> 
        dan probabilitas gagal sebesar <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">{p_failure*100:.2f}%</span>.
    </p>
        
    <p style="color: #F0E6D2; margin-bottom: 1rem;">
        <span style="color: #FFE4A0; font-weight: 700;">2. EXPECTED VALUE (EV) TERTINGGI</span><br>
        Strategi <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">{best_alternative}</span> 
        memberikan nilai <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">EV tertinggi sebesar {best_ev:,.0f} unit</span>, 
        mengalahkan {len(alternatives)-1} alternatif strategi lainnya.
    </p>
        
    <p style="color: #F0E6D2; margin-bottom: 1rem;">
        <span style="color: #FFE4A0; font-weight: 700;">3. ANALISIS SENSITIVITAS</span><br>
        Pada probabilitas sukses sebesar <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">{sensitivity_p:.2%}</span>, 
        strategi terbaik <span style="background: {'rgba(255,215,0,0.25)' if best_sensitivity_alt == best_alternative else 'rgba(231,76,60,0.2)'}; padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: {'#FFD700' if best_sensitivity_alt == best_alternative else '#e74c3c'};">{best_sensitivity_alt}</span>. 
        Semakin tinggi probabilitas sukses, semakin menguntungkan strategi dengan payoff success tinggi.
    </p>
        
    <p style="color: #F0E6D2; margin-bottom: 1rem;">
        <span style="color: #FFE4A0; font-weight: 700;">4. REKOMENDASI MANAJERIAL</span><br>
        Bank sebaiknya <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">mengimplementasikan strategi {best_alternative}</span> 
        untuk memaksimalkan nilai ekspektasi, serta <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">melakukan monitoring probabilitas sukses secara berkala</span> 
        dan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">menggunakan analisis sensitivitas untuk antisipasi perubahan pasar</span>.
    </p>
        
    <p style="color: #F0E6D2; margin-bottom: 0;">
        <span style="color: #FFE4A0; font-weight: 700;">5. KETERBATASAN MODEL</span><br>
        Model ini <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #e74c3c;">mengasumsikan probabilitas tetap (stationary)</span> 
        dan <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #e74c3c;">payoff bersifat konstan</span>, 
        serta <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #e74c3c;">tidak memperhitungkan preferensi risiko pengambil keputusan</span> 
        (akan dibahas lebih lanjut dalam analisis Utility Theory).
    </p>
    </div>
    """, unsafe_allow_html=True)
    

def analysis_uncertainty(df):
    """Analisis Decision Under Uncertainty dengan Payoff per Nasabah"""
    st.header("Analisis Decision Under Uncertainty")
    
    # =========================================================
    # PENJELASAN MATERI DALAM 3 PARAGRAF DENGAN HIGHLIGHT
    # =========================================================
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); padding: 1.2rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #DAA520;">
        <p style="color: #F0E6D2; line-height: 1.6; margin-bottom: 1rem;">
            <span style="background: linear-gradient(120deg, rgba(218,165,32,0.2) 0%, rgba(218,165,32,0.2) 100%); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFE4A0;">Decision Under Uncertainty</span> 
            merupakan pendekatan pengambilan keputusan dimana 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">probabilitas terjadinya setiap kondisi alam tidak diketahui</span>. 
            Berbeda dengan decision under risk yang memiliki estimasi probabilitas, dalam kondisi ketidakpastian, 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">pengambil keputusan tidak memiliki informasi tentang kemungkinan terjadinya suatu keadaan</span>, 
            sehingga diperlukan kriteria khusus untuk memilih alternatif terbaik.
        </p>
        <p style="color: #F0E6D2; line-height: 1.6; margin-bottom: 1rem;">
            Beberapa kriteria yang umum digunakan dalam decision under uncertainty antara lain: 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Maximax (optimis)</span> 
            yang memilih payoff tertinggi, 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Maximin (pesimis)</span> 
            yang memilih payoff terburuk terbaik, 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Minimax Regret</span> 
            yang meminimalkan penyesalan maksimum, serta 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Laplace (rata-rata)</span> 
            yang mengasumsikan semua kondisi memiliki probabilitas sama.
        </p>
        <p style="color: #F0E6D2; line-height: 1.6;">
            Keunggulan pendekatan ini adalah 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">tidak memerlukan estimasi probabilitas yang sulit didapatkan</span>, 
            namun kelemahannya adalah 
            <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #e74c3c;">hasil keputusan sangat bergantung pada kriteria yang dipilih</span> 
            dan <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #e74c3c;">dapat berbeda antar metode</span>. 
            Pendekatan ini paling cocok digunakan ketika 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">data historis terbatas atau situasi baru tanpa preseden</span>, 
            serta <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">profil risiko pengambil keputusan telah diketahui</span>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # =========================================================
    # KONSEP DAN PENDEKATAN
    # =========================================================
    st.markdown("""
    <div style="background: rgba(0,0,0,0.4); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
        <b style="color: #FFE4A0; font-size: 1.05rem;">📌 Konsep Decision Under Uncertainty:</b><br>
        <span style="color: #D4C4A8;">1. Probabilitas setiap kejadian <span style="color: #FFD700; font-weight: 500;">tidak diketahui</span><br>
        2. Menggunakan kriteria khusus: <span style="color: #FFD700; font-weight: 500;">Maximax, Maximin, Minimax Regret, Laplace</span><br>
        3. Keputusan bergantung pada <span style="color: #FFD700; font-weight: 500;">preferensi risiko</span> pengambil keputusan<br>
        4. Hasil antar metode <span style="color: #FFD700; font-weight: 500;">dapat berbeda</span> dan perlu dibandingkan</span><br><br>
        <b style="color: #FFE4A0; font-size: 1.05rem;">📌 Pendekatan ini cocok untuk:</b><br>
        <span style="color: #D4C4A8;">• <span style="color: #FFD700;">Situasi baru tanpa data historis</span> yang memadai<br>
        • <span style="color: #FFD700;">Eksplorasi strategi</span> dengan berbagai skenario kemungkinan<br>
        • <span style="color: #FFD700;">Memahami rentang kemungkinan hasil</span> dari optimis hingga pesimis</span>
    </div>
    """, unsafe_allow_html=True)
    
    # =========================================================
    # 1. DEFINISI ALTERNATIF STRATEGI (DALAM BENTUK CARD)
    # =========================================================
    st.subheader("Definisi Alternatif Strategi")
    
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); padding: 0.8rem; border-radius: 10px; margin-bottom: 1rem;">
        <span style="color: #D4C4A8;">Berikut adalah <span style="color: #FFD700; font-weight: 500;">empat alternatif strategi pemasaran</span> yang akan dievaluasi:</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Menentukan threshold (kuartil atas 75%)
    balance_threshold = df['balance'].quantile(0.75)
    age_threshold = df['age'].quantile(0.75)
    duration_threshold = df['duration'].quantile(0.75)
    
    # CSS untuk card alternatif strategi
    st.markdown("""
    <style>
    .strategy-card {
        background: linear-gradient(135deg, rgba(52,152,219,0.12) 0%, rgba(52,152,219,0.04) 100%);
        border: 1px solid rgba(52,152,219,0.3);
        border-radius: 14px;
        padding: 0.8rem 0.5rem;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
    }
    .strategy-card:hover {
        background: linear-gradient(135deg, rgba(52,152,219,0.2) 0%, rgba(52,152,219,0.08) 100%);
        border-color: rgba(52,152,219,0.6);
        transform: translateY(-3px);
    }
    .strategy-code {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        font-weight: 700;
        color: #FFD700;
        margin-bottom: 0.3rem;
    }
    .strategy-name {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: #D4C4A8;
        margin-bottom: 0.5rem;
    }
    .strategy-value {
        font-family: 'Inter', monospace;
        font-size: 0.85rem;
        font-weight: 600;
        color: #3498db;
    }
    .strategy-desc {
        font-family: 'Inter', sans-serif;
        font-size: 0.6rem;
        color: #A8885A;
        margin-top: 0.3rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="strategy-card">
            <div class="strategy-code">A1</div>
            <div class="strategy-name">Balance Tinggi</div>
            <div class="strategy-value">> {balance_threshold:,.0f} unit</div>
            <div class="strategy-desc">Fokus nasabah saldo tinggi</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="strategy-card">
            <div class="strategy-code">A2</div>
            <div class="strategy-name">Usia Tua</div>
            <div class="strategy-value">> {age_threshold:.0f} tahun</div>
            <div class="strategy-desc">Fokus nasabah usia lanjut</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="strategy-card">
            <div class="strategy-code">A3</div>
            <div class="strategy-name">Durasi Tinggi</div>
            <div class="strategy-value">> {duration_threshold:.0f} detik</div>
            <div class="strategy-desc">Fokus durasi panggilan panjang</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="strategy-card">
            <div class="strategy-code">A4</div>
            <div class="strategy-name">Semua Nasabah</div>
            <div class="strategy-value">Seluruh populasi</div>
            <div class="strategy-desc">Hubungi semua nasabah</div>
        </div>
        """, unsafe_allow_html=True)
    
    # =========================================================
    # 2. DEFINISI STATE OF NATURE (KONDISI ALAM)
    # =========================================================
    st.subheader("Definisi State of Nature (Kondisi Alam)")
    
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); padding: 0.8rem; border-radius: 10px; margin-bottom: 1rem;">
        <span style="color: #D4C4A8;"><span style="color: #FFD700; font-weight: 500;">State of nature</span> didefinisikan berdasarkan tingkat deposit success per bulan:</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Hitung deposit rate per bulan
    if 'month' in df.columns and 'deposit_binary' in df.columns:
        monthly_rate = df.groupby('month')['deposit_binary'].mean().sort_values()
        
        # Grafik garis untuk tingkat keberhasilan per bulan (interaktif dengan plotly)
        import plotly.graph_objects as go
        
        fig_monthly = go.Figure()
        
        fig_monthly.add_trace(go.Scatter(
            x=monthly_rate.index,
            y=(monthly_rate.values * 100),
            mode='lines+markers',
            name='Success Rate',
            line=dict(color='#FFD700', width=2),
            marker=dict(size=8, color='#FFD700', symbol='circle'),
            hovertemplate='<b>%{x}</b><br>Success Rate: %{y:.1f}%<extra></extra>'
        ))
        
        fig_monthly.update_layout(
            title=dict(text='<b>Tingkat Keberhasilan Deposit per Bulan</b>', font=dict(size=13, color='#FFE4A0'), x=0.5),
            xaxis=dict(title='Bulan', title_font=dict(size=11, color='#D4C4A8'), tickfont=dict(size=10, color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title='Success Rate (%)', title_font=dict(size=11, color='#D4C4A8'), tickfont=dict(size=10, color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hoverlabel=dict(bgcolor='rgba(0,0,0,0.8)', font_size=11),
            margin=dict(t=40, b=30, l=40, r=30),
            height=400
        )
        
        st.plotly_chart(fig_monthly, use_container_width=True, config={'displayModeBar': True})
        
        # Bagi menjadi 3 kategori kondisi
        n_months = len(monthly_rate)
        split_idx = max(1, n_months // 3)
        
        bulan_terbaik = monthly_rate.tail(split_idx).index.tolist()
        bulan_normal = monthly_rate.iloc[split_idx:-split_idx].index.tolist() if split_idx < n_months - split_idx else monthly_rate.iloc[1:-1].index.tolist()
        bulan_terburuk = monthly_rate.head(split_idx).index.tolist()
        
        # Buat dataset untuk setiap kondisi
        kondisi_S1 = df[df['month'].isin(bulan_terbaik)]  # Sangat Baik
        kondisi_S2 = df[df['month'].isin(bulan_normal)]   # Normal
        kondisi_S3 = df[df['month'].isin(bulan_terburuk)] # Buruk
        
        # CSS untuk card state of nature
        st.markdown("""
        <style>
        .nature-card {
            background: linear-gradient(135deg, rgba(46,204,113,0.12) 0%, rgba(46,204,113,0.04) 100%);
            border: 1px solid rgba(46,204,113,0.3);
            border-radius: 14px;
            padding: 1rem 0.5rem;
            text-align: center;
            transition: all 0.3s ease;
            height: 100%;
        }
        .nature-card:hover {
            background: linear-gradient(135deg, rgba(46,204,113,0.2) 0%, rgba(46,204,113,0.08) 100%);
            border-color: rgba(46,204,113,0.6);
            transform: translateY(-3px);
        }
        .nature-title {
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            font-weight: 700;
            color: #FFD700;
            margin-bottom: 0.5rem;
        }
        .nature-value {
            font-family: 'Inter', monospace;
            font-size: 1.1rem;
            font-weight: 700;
            color: #2ecc71;
            margin: 0.3rem 0;
        }
        .nature-desc {
            font-family: 'Inter', sans-serif;
            font-size: 0.65rem;
            color: #A8885A;
        }
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="nature-card">
                <div class="nature-title">🌞 S1 - SANGAT BAIK</div>
                <div class="nature-value">{len(kondisi_S1):,} observasi</div>
                <div class="nature-desc">Deposit rate: {kondisi_S1['deposit_binary'].mean()*100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="nature-card">
                <div class="nature-title">🌤️ S2 - NORMAL</div>
                <div class="nature-value">{len(kondisi_S2):,} observasi</div>
                <div class="nature-desc">Deposit rate: {kondisi_S2['deposit_binary'].mean()*100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="nature-card">
                <div class="nature-title">🌧️ S3 - BURUK</div>
                <div class="nature-value">{len(kondisi_S3):,} observasi</div>
                <div class="nature-desc">Deposit rate: {kondisi_S3['deposit_binary'].mean()*100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
    
    # =========================================================
    # 3. PARAMETER PAYOFF (PROFIT & COST)
    # =========================================================
    st.subheader("Parameter Payoff per Nasabah")
    
    PROFIT_PER_SUCCESS = 500000  # Rp 500.000
    COST_PER_CALL = 10000        # Rp 10.000
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Profit per Deposit Success", f"Rp {PROFIT_PER_SUCCESS:,}", "Asumsi")
    with col2:
        st.metric("Cost per Panggilan", f"Rp {COST_PER_CALL:,}", "Asumsi")
    
    st.caption("""
    **Payoff per nasabah = (Success_Rate × Profit_per_Sukses) - Cost_per_Call  
    Keuntungan: Tidak terpengaruh oleh jumlah sampel yang tidak seimbang, lebih adil membandingkan efektivitas strategi**
    """)
    
    # =========================================================
    # 4. FUNGSI MENGHITUNG PAYOFF PER NASABAH
    # =========================================================
    
    def hitung_payoff_per_nasabah(data_subset, strategi_nama):
        """Menghitung payoff per nasabah untuk suatu strategi pada kondisi tertentu"""
        
        # Filter nasabah sesuai strategi
        if strategi_nama == 'A1_Balance_Tinggi':
            target_nasabah = data_subset[data_subset['balance'] > balance_threshold].copy()
        elif strategi_nama == 'A2_Usia_Tua':
            target_nasabah = data_subset[data_subset['age'] > age_threshold].copy()
        elif strategi_nama == 'A3_Durasi_Tinggi':
            target_nasabah = data_subset[data_subset['duration'] > duration_threshold].copy()
        else:  # A4_Semua_Nasabah
            target_nasabah = data_subset.copy()
        
        if len(target_nasabah) == 0:
            return 0, 0, 0
        
        n_customer = len(target_nasabah)
        n_success = target_nasabah['deposit_binary'].sum()
        
        # Hitung payoff per nasabah
        success_rate = (n_success / n_customer) if n_customer > 0 else 0
        expected_revenue_per_customer = success_rate * PROFIT_PER_SUCCESS
        payoff_per_customer = expected_revenue_per_customer - COST_PER_CALL
        
        return payoff_per_customer / 1000, success_rate * 100, n_customer  # dalam ribuan Rupiah
    
        # =========================================================
    # 5. MEMBANGUN PAYOFF TABLE DARI DATA EMPIRIS
    # =========================================================
    
    # Daftar strategi
    strategi_list = ['A1_Balance_Tinggi', 'A2_Usia_Tua', 'A3_Durasi_Tinggi', 'A4_Semua_Nasabah']
    kondisi_list = ['S1_Sangat_Baik', 'S2_Normal', 'S3_Buruk']
    strategi_nama_display = {
        'A1_Balance_Tinggi': 'A1 - Balance Tinggi',
        'A2_Usia_Tua': 'A2 - Usia Tua',
        'A3_Durasi_Tinggi': 'A3 - Durasi Tinggi',
        'A4_Semua_Nasabah': 'A4 - Semua Nasabah'
    }
    
    # Inisialisasi tabel
    payoff_table = pd.DataFrame(index=strategi_list, columns=kondisi_list)
    success_rate_table = pd.DataFrame(index=strategi_list, columns=kondisi_list)
    customer_count_table = pd.DataFrame(index=strategi_list, columns=kondisi_list)
    
    # Mapping kondisi ke dataset
    kondisi_dataset = {
        'S1_Sangat_Baik': kondisi_S1,
        'S2_Normal': kondisi_S2,
        'S3_Buruk': kondisi_S3
    }
    
    # Hitung payoff per nasabah untuk setiap kombinasi
    for strategi in strategi_list:
        for kondisi_nama, kondisi_data in kondisi_dataset.items():
            payoff, success_rate, n_cust = hitung_payoff_per_nasabah(kondisi_data, strategi)
            payoff_table.loc[strategi, kondisi_nama] = payoff
            success_rate_table.loc[strategi, kondisi_nama] = success_rate
            customer_count_table.loc[strategi, kondisi_nama] = n_cust
    
    # Konversi ke numeric
    payoff_table = payoff_table.astype(float)
    success_rate_table = success_rate_table.astype(float)
    customer_count_table = customer_count_table.astype(int)
    
    # Tampilkan tabel payoff interaktif
    st.subheader("Tabel Payoff per Nasabah (Dalam Ribuan Rupiah)")
    st.caption("Nilai positif = untung, negatif = rugi per nasabah")
    
    payoff_display = payoff_table.copy()
    payoff_display.index = [strategi_nama_display[s] for s in payoff_display.index]
    
    st.dataframe(
        payoff_display.style.format('{:.0f}').set_properties(**{'text-align': 'center'}),
        use_container_width=True
    )
    
    with st.expander("Detail Tambahan - Tingkat Keberhasilan & Jumlah Nasabah"):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Tabel Tingkat Keberhasilan (%)**")
            rate_display = success_rate_table.copy()
            rate_display.index = [strategi_nama_display[s] for s in rate_display.index]
            st.dataframe(rate_display.style.format('{:.1f}').set_properties(**{'text-align': 'center'}), use_container_width=True)
        
        with col2:
            st.write("**Tabel Jumlah Nasabah yang Dihubungi**")
            count_display = customer_count_table.copy()
            count_display.index = [strategi_nama_display[s] for s in count_display.index]
            st.dataframe(count_display.style.set_properties(**{'text-align': 'center'}), use_container_width=True)
    
    # =========================================================
    # 6. METODE MAXIMAX (Optimis)
    # =========================================================
    st.subheader("Metode Maximax (Optimis)")
    st.caption("Memilih alternatif dengan payoff maksimum tertinggi. Cocok untuk pengambil keputusan yang optimis (risk seeking)")
    
    maximax_values = payoff_table.max(axis=1)
    
    maximax_df = pd.DataFrame({
        'Strategi': [strategi_nama_display[s] for s in maximax_values.index],
        'Payoff Terbaik (Rp ribu)': maximax_values.values,
        'Kondisi Terjadi': [payoff_table.loc[s].idxmax() for s in maximax_values.index]
    }).sort_values('Payoff Terbaik (Rp ribu)', ascending=False)
    
    st.dataframe(maximax_df, use_container_width=True, hide_index=True)
    
    keputusan_maximax = maximax_values.idxmax()
    nilai_maximax = maximax_values.max()
    kondisi_maximax = payoff_table.loc[keputusan_maximax].idxmax()
    nama_maximax = strategi_nama_display[keputusan_maximax]
    
    st.markdown(f"""
    <div style="background: rgba(46,204,113,0.15); border-left: 4px solid #2ecc71; border-radius: 10px; padding: 1rem; margin: 0.5rem 0;">
        <span style="color: #F0E6D2; line-height: 1.6;">
            Berdasarkan metode <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Maximax (Optimis)</span>, 
            keputusan yang diambil adalah mengimplementasikan strategi 
            <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">{nama_maximax}</span>. 
            Strategi ini menghasilkan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">payoff per nasabah terbaik sebesar Rp {nilai_maximax:,.0f} ribu</span>, 
            yang dicapai pada kondisi <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">{kondisi_maximax}</span>.
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # =========================================================
    # 7. METODE MAXIMIN (Pesimis)
    # =========================================================
    st.subheader("Metode Maximin (Pesimis)")
    st.caption("Memilih alternatif dengan payoff minimum terbaik. Cocok untuk pengambil keputusan yang pesimis (risk averse)")
    
    maximin_values = payoff_table.min(axis=1)
    
    maximin_df = pd.DataFrame({
        'Strategi': [strategi_nama_display[s] for s in maximin_values.index],
        'Payoff Terburuk (Rp ribu)': maximin_values.values,
        'Kondisi Terjadi': [payoff_table.loc[s].idxmin() for s in maximin_values.index]
    }).sort_values('Payoff Terburuk (Rp ribu)', ascending=False)
    
    st.dataframe(maximin_df, use_container_width=True, hide_index=True)
    
    keputusan_maximin = maximin_values.idxmax()
    nilai_maximin = maximin_values.max()
    kondisi_maximin = payoff_table.loc[keputusan_maximin].idxmin()
    nama_maximin = strategi_nama_display[keputusan_maximin]
    
    st.markdown(f"""
    <div style="background: rgba(46,204,113,0.15); border-left: 4px solid #2ecc71; border-radius: 10px; padding: 1rem; margin: 0.5rem 0;">
        <span style="color: #F0E6D2; line-height: 1.6;">
            Berdasarkan metode <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Maximin (Pesimis)</span>, 
            keputusan yang diambil adalah mengimplementasikan strategi 
            <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">{nama_maximin}</span>. 
            Strategi ini menghasilkan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">payoff per nasabah terburuk terbaik sebesar Rp {nilai_maximin:,.0f} ribu</span>, 
            yang terjadi pada kondisi <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">{kondisi_maximin}</span>.
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # =========================================================
    # 8. METODE MINIMAX REGRET
    # =========================================================
    st.subheader("Metode Minimax Regret")
    st.caption("Meminimalkan penyesalan maksimum. Menghitung opportunity loss dari setiap keputusan")
    
    # Hitung payoff maksimum tiap kondisi (kolom)
    max_per_kondisi = payoff_table.max(axis=0)
    
    # Hitung regret table (opportunity loss)
    regret_table = pd.DataFrame(
        max_per_kondisi.values - payoff_table.values,
        index=payoff_table.index,
        columns=payoff_table.columns
    )
    
    regret_display = regret_table.copy()
    regret_display.index = [strategi_nama_display[s] for s in regret_display.index]
    st.write("**Tabel Regret (Penyesalan dalam Ribuan Rupiah per Nasabah)**")
    st.dataframe(regret_display.style.format('{:.0f}').set_properties(**{'text-align': 'center'}), use_container_width=True)
    
    max_regret = regret_table.max(axis=1)
    
    regret_max_df = pd.DataFrame({
        'Strategi': [strategi_nama_display[s] for s in max_regret.index],
        'Regret Maksimum (Rp ribu)': max_regret.values,
        'Kondisi Terjadi': [regret_table.loc[s].idxmax() for s in max_regret.index]
    }).sort_values('Regret Maksimum (Rp ribu)')
    
    st.dataframe(regret_max_df, use_container_width=True, hide_index=True)
    
    keputusan_regret = max_regret.idxmin()
    nilai_regret = max_regret.min()
    kondisi_regret = regret_table.loc[keputusan_regret].idxmax()
    nama_regret = strategi_nama_display[keputusan_regret]
    
    st.markdown(f"""
    <div style="background: rgba(46,204,113,0.15); border-left: 4px solid #2ecc71; border-radius: 10px; padding: 1rem; margin: 0.5rem 0;">
        <span style="color: #F0E6D2; line-height: 1.6;">
            Berdasarkan metode <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Minimax Regret</span>, 
            keputusan yang diambil adalah mengimplementasikan strategi 
            <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">{nama_regret}</span>. 
            Strategi ini menghasilkan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">penyesalan maksimum minimum sebesar Rp {nilai_regret:,.0f} ribu per nasabah</span>, 
            dengan penyesalan terbesar terjadi pada kondisi <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">{kondisi_regret}</span>.
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # =========================================================
    # 9. METODE LAPLACE (Equal Probability)
    # =========================================================
    st.subheader("Metode Laplace (Equal Probability)")
    st.caption("Semua kondisi memiliki probabilitas sama. Menggunakan rata-rata payoff")
    
    laplace_values = payoff_table.mean(axis=1)
    
    laplace_df = pd.DataFrame({
        'Strategi': [strategi_nama_display[s] for s in laplace_values.index],
        'Rata-rata Payoff (Rp ribu)': laplace_values.values
    }).sort_values('Rata-rata Payoff (Rp ribu)', ascending=False)
    
    st.dataframe(laplace_df, use_container_width=True, hide_index=True)
    
    keputusan_laplace = laplace_values.idxmax()
    nilai_laplace = laplace_values.max()
    nama_laplace = strategi_nama_display[keputusan_laplace]
    
    st.markdown(f"""
    <div style="background: rgba(46,204,113,0.15); border-left: 4px solid #2ecc71; border-radius: 10px; padding: 1rem; margin: 0.5rem 0;">
        <span style="color: #F0E6D2; line-height: 1.6;">
            Berdasarkan metode <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Laplace (Rata-rata)</span> 
            yang mengasumsikan semua kondisi memiliki probabilitas yang sama, keputusan yang diambil adalah mengimplementasikan strategi 
            <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">{nama_laplace}</span>. 
            Strategi ini menghasilkan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">rata-rata payoff per nasabah tertinggi sebesar Rp {nilai_laplace:,.0f} ribu</span>.
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # =========================================================
    # 10. RINGKASAN HASIL SEMUA METODE (MENGGUNAKAN CARD)
    # =========================================================
    st.subheader("Hasil Semua Metode")
    
    st.markdown(f"""
    <div style="background: rgba(0,0,0,0.35); border-radius: 16px; padding: 1.2rem; margin: 1rem 0;">
        <div style="display: flex; flex-wrap: wrap; gap: 1rem; justify-content: space-between;">
            <div style="flex: 1; background: linear-gradient(135deg, rgba(52,152,219,0.15) 0%, rgba(52,152,219,0.05) 100%); border-radius: 12px; padding: 0.8rem; text-align: center; border: 1px solid rgba(52,152,219,0.3);">
                <div style="font-size: 0.7rem; color: #A8885A; text-transform: uppercase; letter-spacing: 1px;">Maximax (Optimis)</div>
                <div style="font-size: 1rem; font-weight: 700; color: #FFD700; margin: 0.3rem 0;">{nama_maximax}</div>
                <div style="font-size: 0.7rem; color: #D4C4A8;">Rp {nilai_maximax:,.0f} ribu/nasabah</div>
            </div>
            <div style="flex: 1; background: linear-gradient(135deg, rgba(52,152,219,0.15) 0%, rgba(52,152,219,0.05) 100%); border-radius: 12px; padding: 0.8rem; text-align: center; border: 1px solid rgba(52,152,219,0.3);">
                <div style="font-size: 0.7rem; color: #A8885A; text-transform: uppercase; letter-spacing: 1px;">Maximin (Pesimis)</div>
                <div style="font-size: 1rem; font-weight: 700; color: #FFD700; margin: 0.3rem 0;">{nama_maximin}</div>
                <div style="font-size: 0.7rem; color: #D4C4A8;">Rp {nilai_maximin:,.0f} ribu/nasabah</div>
            </div>
            <div style="flex: 1; background: linear-gradient(135deg, rgba(52,152,219,0.15) 0%, rgba(52,152,219,0.05) 100%); border-radius: 12px; padding: 0.8rem; text-align: center; border: 1px solid rgba(52,152,219,0.3);">
                <div style="font-size: 0.7rem; color: #A8885A; text-transform: uppercase; letter-spacing: 1px;">Minimax Regret</div>
                <div style="font-size: 1rem; font-weight: 700; color: #FFD700; margin: 0.3rem 0;">{nama_regret}</div>
                <div style="font-size: 0.7rem; color: #D4C4A8;">Rp {nilai_regret:,.0f} ribu (regret)</div>
            </div>
            <div style="flex: 1; background: linear-gradient(135deg, rgba(52,152,219,0.15) 0%, rgba(52,152,219,0.05) 100%); border-radius: 12px; padding: 0.8rem; text-align: center; border: 1px solid rgba(52,152,219,0.3);">
                <div style="font-size: 0.7rem; color: #A8885A; text-transform: uppercase; letter-spacing: 1px;">Laplace (Rata-rata)</div>
                <div style="font-size: 1rem; font-weight: 700; color: #FFD700; margin: 0.3rem 0;">{nama_laplace}</div>
                <div style="font-size: 0.7rem; color: #D4C4A8;">Rp {nilai_laplace:,.0f} ribu/nasabah</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # =========================================================
    # 11. ANALISIS KONSISTENSI KEPUTUSAN
    # =========================================================
    st.subheader("Analisis Konsistensi Keputusan")
    
    from collections import Counter
    
    keputusan_list = [nama_maximax, nama_maximin, nama_regret, nama_laplace]
    keputusan_count = Counter(keputusan_list)
    
    if len(keputusan_count) == 1:
        st.markdown(f"""
        <div style="background: rgba(46,204,113,0.15); border-left: 4px solid #2ecc71; border-radius: 10px; padding: 1rem;">
            <span style="color: #F0E6D2; line-height: 1.6;">
                Semua metode (Maximax, Maximin, Minimax Regret, dan Laplace) memilih strategi yang sama, yaitu 
                <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">{nama_maximax}</span>. 
                Hal ini menunjukkan bahwa strategi tersebut <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">robust terhadap berbagai kriteria keputusan</span> 
                dan dapat direkomendasikan dengan keyakinan yang lebih tinggi.
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        konsistensi_text = ""
        for strategi, count in keputusan_count.items():
            konsistensi_text += f"<span style='background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;'>{strategi}</span> ({count} dari 4 metode), "
        
        st.markdown(f"""
        <div style="background: rgba(231,76,60,0.15); border-left: 4px solid #e74c3c; border-radius: 10px; padding: 1rem;">
            <span style="color: #F0E6D2; line-height: 1.6;">
                ⚠️ <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #e74c3c;">TIDAK KONSISTEN</span> 
                - Berbagai metode memilih strategi yang berbeda: {konsistensi_text[:-2]}. 
                Oleh karena itu, pemilihan strategi harus <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">mempertimbangkan profil risiko pengambil keputusan</span> 
                serta preferensi manajemen dalam menghadapi ketidakpastian.
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    # =========================================================
    # 12. VISUALISASI (INTERAKTIF DENGAN PLOTLY)
    # =========================================================

    import plotly.graph_objects as go
    
    # Grafik 1: Perbandingan Payoff per Strategi
    fig1 = go.Figure()
    
    for strategi in strategi_list:
        nama_tampilan = strategi_nama_display[strategi]
        fig1.add_trace(go.Bar(
            name=nama_tampilan,
            x=kondisi_list,
            y=payoff_table.loc[strategi].values,
            text=payoff_table.loc[strategi].values.round(0),
            textposition='outside',
            hovertemplate=f'<b>{nama_tampilan}</b><br>Kondisi: %{{x}}<br>Payoff: %{{y:.0f}} ribu<extra></extra>'
        ))
    
    fig1.update_layout(
        title=dict(text='<b>Perbandingan Payoff per Nasabah Antar Strategi</b>', font=dict(size=14, color='#FFE4A0'), x=0.5),
        xaxis=dict(title='State of Nature (Kondisi Alam)', title_font=dict(size=12, color='#D4C4A8'), tickfont=dict(size=11, color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title='Payoff per Nasabah (Ribuan Rupiah)', title_font=dict(size=12, color='#D4C4A8'), tickfont=dict(size=11, color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hoverlabel=dict(bgcolor='rgba(0,0,0,0.8)', font_size=12),
        barmode='group',
        margin=dict(t=50, b=50, l=50, r=50),
        height=500,
        legend=dict(font=dict(color='#D4C4A8'), bgcolor='rgba(0,0,0,0.5)')
    )
    
    st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': True})
    
    # Interpretasi Grafik Batang
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 1rem; margin: 1rem 0;">
        <span style="color: #F0E6D2; line-height: 1.6;">
            <span style="color: #FFD700; font-weight: 700;"></span> 
            Grafik batang di atas menunjukkan perbandingan payoff setiap strategi pada tiga kondisi alam (S1=Sangat Baik, S2=Normal, S3=Buruk). 
            Strategi <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">A3 (Durasi Tinggi)</span> memberikan 
            <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">payoff tertinggi pada kondisi baik dan normal</span>, 
            namun berisiko <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #e74c3c;">mengalami kerugian pada kondisi buruk</span>. 
            Sebaliknya, strategi <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">A4 (Semua Nasabah)</span> 
            memberikan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">payoff paling stabil</span> karena selalu positif di semua kondisi, 
            menjadikannya pilihan aman bagi pengambil keputusan yang menghindari risiko.
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Grafik 2: Heatmap Payoff
    import plotly.express as px
    
    payoff_heatmap = payoff_table.copy()
    payoff_heatmap.index = [strategi_nama_display[s] for s in payoff_heatmap.index]
    
    fig2 = px.imshow(
        payoff_heatmap.values,
        x=kondisi_list,
        y=payoff_heatmap.index,
        text_auto='.0f',
        color_continuous_scale='RdYlGn',
        title='Heatmap Payoff per Nasabah (Ribuan Rupiah)'
    )
    
    fig2.update_layout(
        title=dict(font=dict(size=14, color='#FFE4A0'), x=0.5),
        xaxis=dict(title='State of Nature', tickfont=dict(color='#D4C4A8')),
        yaxis=dict(title='Strategi', tickfont=dict(color='#D4C4A8')),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, b=50, l=50, r=50),
        height=500
    )
    
    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': True})
    
    # Interpretasi Heatmap
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 1rem; margin: 1rem 0;">
        <span style="color: #F0E6D2; line-height: 1.6;">
            <span style="color: #FFD700; font-weight: 700;"></span> 
            Heatmap di atas memvisualisasikan payoff setiap strategi dengan gradien warna 
            <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">hijau (positif/untung)</span> hingga 
            <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #e74c3c;">merah (negatif/rugi)</span>. 
            Semakin hijau suatu sel, semakin tinggi keuntungan yang diperoleh. Terlihat bahwa 
            <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">strategi A3 (Durasi Tinggi)</span> 
            memiliki warna hijau paling terang pada kondisi S1 (Sangat Baik) dan S2 (Normal), 
            namun berubah menjadi <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #e74c3c;">merah pada kondisi S3 (Buruk)</span>. 
            Sementara itu, <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">strategi A4 (Semua Nasabah)</span> 
            menunjukkan warna hijau yang konsisten di semua kondisi, menandakan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">stabilitas payoff</span> 
            tanpa risiko kerugian.
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # =========================================================
    # 13. KESIMPULAN AKHIR DAN REKOMENDASI (DALAM PARAGRAF DENGAN HIGHLIGHT)
    # =========================================================
    st.subheader("Kesimpulan Akhir dan Rekomendasi Manajerial")
    
    st.markdown(f"""
    <div style="background: rgba(0,0,0,0.4); padding: 1.5rem; border-radius: 10px; line-height: 1.8;">
    <p style="color: #F0E6D2; margin-bottom: 1rem;">
        <span style="color: #FFE4A0; font-weight: 700;">1. KARAKTERISTIK PAYOFF PER NASABAH</span><br>
        Strategi <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">A3 - Durasi Tinggi</span> 
        memberikan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">rata-rata payoff tertinggi</span> 
        namun dengan <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #e74c3c;">risiko kerugian di kondisi buruk</span>, 
        sedangkan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">A4 - Semua Nasabah</span> 
        memberikan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">payoff paling stabil</span> (selalu positif).
    </p>
        
    <p style="color: #F0E6D2; margin-bottom: 1rem;">
        <span style="color: #FFE4A0; font-weight: 700;">2. REKOMENDASI BERDASARKAN PROFIL RISIKO</span><br>
        • <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">Risk Seeker (Optimis)</span>: {nama_maximax}<br>
        • <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">Risk Averse (Pesimis)</span>: {nama_maximin}<br>
        • <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">Minimalis Penyesalan</span>: {nama_regret}<br>
        • <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">Netral (Laplace)</span>: {nama_laplace}
    </p>
        
    <p style="color: #F0E6D2; margin-bottom: 1rem;">
        <span style="color: #FFE4A0; font-weight: 700;">3. IMPLIKASI BISNIS</span><br>
        Strategi <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">DURASI TINGGI</span> 
        memberikan payoff tertinggi karena nasabah dengan durasi panjang cenderung deposit, 
        sedangkan strategi <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">SEMUA NASABAH</span> 
        dipilih metode pesimis karena risiko minimal.
    </p>
        
    <p style="color: #F0E6D2; margin-bottom: 1rem;">
        <span style="color: #FFE4A0; font-weight: 700;">4. TINDAK LANJUT YANG DISARANKAN</span><br>
        • <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">Lakukan analisis sensitivitas</span> pada threshold strategi<br>
        • <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">Pertimbangkan decision under risk</span> dengan probabilitas objektif<br>
        • <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">Evaluasi dengan utility theory</span> untuk preferensi risiko spesifik<br>
        • <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">Uji coba A/B testing</span> untuk memvalidasi strategi terpilih
    </p>
    </div>
    """, unsafe_allow_html=True)
    

def analysis_probabilistic(df):
    """Analisis Probabilistic Modeling - Lengkap dengan Probabilitas, Distribusi, dan Model Risiko"""
    st.header("Analisis Probabilitas")
    
    # =========================================================
    # PENJELASAN MATERI DALAM 3 PARAGRAF DENGAN HIGHLIGHT
    # =========================================================
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); padding: 1.2rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #DAA520;">
        <p style="color: #F0E6D2; line-height: 1.6; margin-bottom: 1rem;">
            <span style="background: linear-gradient(120deg, rgba(218,165,32,0.2) 0%, rgba(218,165,32,0.2) 100%); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFE4A0;">Probabilistic Modeling</span> 
            adalah pendekatan statistik yang <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">mengubah data mentah menjadi distribusi probabilitas</span> 
            untuk memahami ketidakpastian dan membuat prediksi. Dalam konteks pengambilan keputusan, metode ini memungkinkan kita untuk 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">menghitung probabilitas marginal, bersyarat, dan joint</span> 
            dari berbagai variabel yang mempengaruhi keputusan nasabah, seperti usia, pekerjaan, pendidikan, dan riwayat transaksi.
        </p>
        <p style="color: #F0E6D2; line-height: 1.6; margin-bottom: 1rem;">
            Pendekatan ini sangat berguna untuk 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">memahami pola hubungan antar variabel dan mengidentifikasi faktor-faktor dominan</span> 
            yang mempengaruhi perilaku nasabah. Dengan memahami 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">distribusi probabilitas dari setiap variabel</span>, 
            bank dapat mengidentifikasi <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">segmen nasabah dengan probabilitas deposit tertinggi</span> 
            serta memahami karakteristik yang membedakan nasabah yang menerima versus menolak penawaran deposito.
        </p>
        <p style="color: #F0E6D2; line-height: 1.6;">
            Keunggulan utama probabilistic modeling adalah 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">kemampuannya mengkuantifikasi ketidakpastian dan memberikan interval keyakinan</span>, 
            namun kelemahannya adalah 
            <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #e74c3c;">membutuhkan data yang cukup besar untuk estimasi yang akurat</span>. 
            Pendekatan ini cocok digunakan ketika 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">data historis tersedia dalam jumlah memadai</span> 
            dan <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">tujuan analisis adalah untuk memahami pola dan membuat prediksi</span> 
            berdasarkan probabilitas.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # =========================================================
    # KONSEP DAN PENDEKATAN
    # =========================================================
    st.markdown("""
    <div style="background: rgba(0,0,0,0.4); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
        <b style="color: #FFE4A0; font-size: 1.05rem;">📌 Konsep Probabilistic Modeling:</b><br>
        <span style="color: #D4C4A8;">1. <span style="color: #FFD700; font-weight: 500;">Probabilitas Marginal</span>: Peluang suatu kejadian tanpa mempertimbangkan variabel lain<br>
        2. <span style="color: #FFD700; font-weight: 500;">Probabilitas Bersyarat</span>: Peluang suatu kejadian dengan syarat variabel lain diketahui<br>
        3. <span style="color: #FFD700; font-weight: 500;">Probabilitas Joint</span>: Peluang dua atau lebih kejadian terjadi bersamaan<br>
        4. <span style="color: #FFD700; font-weight: 500;">Distribusi Probabilitas</span>: Pola sebaran nilai dari suatu variabel</span><br><br>
        <b style="color: #FFE4A0; font-size: 1.05rem;">📌 Pendekatan ini cocok untuk:</b><br>
        <span style="color: #D4C4A8;">• <span style="color: #FFD700;">Memahami hubungan antar variabel</span> dalam dataset nasabah<br>
        • <span style="color: #FFD700;">Mengidentifikasi faktor dominan</span> yang mempengaruhi keputusan deposit<br>
        • <span style="color: #FFD700;">Membangun model risiko</span> untuk segmentasi nasabah<br>
        • <span style="color: #FFD700;">Memprediksi probabilitas deposit</span> untuk nasabah baru</span>
    </div>
    """, unsafe_allow_html=True)
    
    # ============================================
    # 1. PROBABILITAS MARGINAL (INTERAKTIF)
    # ============================================
    st.subheader("Probabilitas Marginal (Probabilitas Dasar)")
    
    if 'deposit' in df.columns:
        p_yes = (df['deposit'] == 'yes').mean()
        p_no = (df['deposit'] == 'no').mean()
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(46,204,113,0.12) 0%, rgba(46,204,113,0.04) 100%); border-radius: 14px; padding: 1rem; text-align: center; border: 1px solid rgba(46,204,113,0.3);">
                <div style="font-size: 0.7rem; color: #A8885A; text-transform: uppercase; letter-spacing: 1px;">P(deposit = yes)</div>
                <div style="font-size: 2rem; font-weight: 700; color: #2ecc71; margin: 0.3rem 0;">{p_yes:.2%}</div>
                <div style="font-size: 0.7rem; color: #D4C4A8;">Probabilitas nasabah membuka deposito</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(231,76,60,0.12) 0%, rgba(231,76,60,0.04) 100%); border-radius: 14px; padding: 1rem; text-align: center; border: 1px solid rgba(231,76,60,0.3); margin-top: 0.8rem;">
                <div style="font-size: 0.7rem; color: #A8885A; text-transform: uppercase; letter-spacing: 1px;">P(deposit = no)</div>
                <div style="font-size: 2rem; font-weight: 700; color: #e74c3c; margin: 0.3rem 0;">{p_no:.2%}</div>
                <div style="font-size: 0.7rem; color: #D4C4A8;">Probabilitas nasabah tidak membuka deposito</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Pie chart interaktif dengan plotly
            import plotly.express as px
            fig_pie = px.pie(
                values=[p_yes, p_no],
                names=['Deposit Yes', 'Deposit No'],
                title='Distribusi Probabilitas Deposit (Marginal)',
                color_discrete_sequence=['#2ecc71', '#e74c3c'],
                hole=0.4
            )
            fig_pie.update_layout(
                title=dict(font=dict(size=14, color='#FFE4A0'), x=0.5),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(font=dict(color='#D4C4A8'), bgcolor='rgba(0,0,0,0.5)'),
                margin=dict(t=50, b=20, l=20, r=20),
                height=350
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': True})
    
    # ============================================
    # 2. PROBABILITAS BERSYARAT (DENGAN CARD DAN VISUALISASI)
    # ============================================
    st.subheader("Probabilitas Bersyarat (Conditional Probability)")
    st.caption("Rumus: P(deposit=yes | kondisi)")
    
    if 'deposit' in df.columns:
        # CSS untuk card probabilitas bersyarat
        st.markdown("""
        <style>
        .cond-card {
            background: linear-gradient(135deg, rgba(52,152,219,0.1) 0%, rgba(52,152,219,0.03) 100%);
            border-radius: 12px;
            padding: 0.6rem;
            margin: 0.3rem 0;
            border-left: 3px solid #3498db;
        }
        .cond-job {
            font-size: 0.75rem;
            font-weight: 600;
            color: #FFD700;
        }
        .cond-prob {
            font-size: 1rem;
            font-weight: 700;
            color: #3498db;
        }
        .cond-count {
            font-size: 0.6rem;
            color: #A8885A;
        }
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background: rgba(0,0,0,0.3); border-radius: 12px; padding: 0.8rem; margin-bottom: 0.5rem;">
                <span style="font-size: 0.8rem; font-weight: 600; color: #FFD700;">📌 P(deposit=yes | job)</span>
            </div>
            """, unsafe_allow_html=True)
            
            job_prob = df.groupby('job')['deposit'].apply(lambda x: (x == 'yes').mean()).sort_values(ascending=False)
            job_counts = df.groupby('job').size()
            
            # Tampilkan dalam bentuk bar horizontal interaktif
            import plotly.graph_objects as go
            fig_job = go.Figure()
            fig_job.add_trace(go.Bar(
                x=job_prob.values * 100,
                y=job_prob.index,
                orientation='h',
                marker_color='#3498db',
                text=job_prob.values.round(4),
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Probabilitas: %{x:.1f}%<br>Jumlah: %{customdata:,} nasabah<extra></extra>',
                customdata=job_counts.values
            ))
            fig_job.update_layout(
                title=dict(text='Probabilitas Deposit Berdasarkan Pekerjaan', font=dict(size=12, color='#D4C4A8')),
                xaxis=dict(title='Probabilitas Deposit (%)', tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(title='Pekerjaan', tickfont=dict(color='#D4C4A8')),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                margin=dict(l=100, r=50, t=40, b=20)
            )
            st.plotly_chart(fig_job, use_container_width=True, config={'displayModeBar': True})
        
        with col2:
            st.markdown("""
            <div style="background: rgba(0,0,0,0.3); border-radius: 12px; padding: 0.8rem; margin-bottom: 0.5rem;">
                <span style="font-size: 0.8rem; font-weight: 600; color: #FFD700;">📌 P(deposit=yes | education)</span>
            </div>
            """, unsafe_allow_html=True)
            
            edu_prob = df.groupby('education')['deposit'].apply(lambda x: (x == 'yes').mean()).sort_values(ascending=False)
            edu_counts = df.groupby('education').size()
            
            fig_edu = go.Figure()
            fig_edu.add_trace(go.Bar(
                x=edu_prob.values * 100,
                y=edu_prob.index,
                orientation='h',
                marker_color='#e67e22',
                text=edu_prob.values.round(4),
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Probabilitas: %{x:.1f}%<br>Jumlah: %{customdata:,} nasabah<extra></extra>',
                customdata=edu_counts.values
            ))
            fig_edu.update_layout(
                title=dict(text='Probabilitas Deposit Berdasarkan Pendidikan', font=dict(size=12, color='#D4C4A8')),
                xaxis=dict(title='Probabilitas Deposit (%)', tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(title='Pendidikan', tickfont=dict(color='#D4C4A8')),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                margin=dict(l=100, r=50, t=40, b=20)
            )
            st.plotly_chart(fig_edu, use_container_width=True, config={'displayModeBar': True})
        
        # Berdasarkan Housing & Loan dalam bentuk card
        st.markdown("""
        <div style="margin-top: 1rem;">
            <div style="background: rgba(0,0,0,0.3); border-radius: 12px; padding: 0.8rem; margin-bottom: 1rem;">
                <span style="font-size: 0.8rem; font-weight: 600; color: #FFD700;">📌 Probabilitas Deposit Berdasarkan Kondisi Lainnya</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'housing' in df.columns:
                housing_prob = df.groupby('housing')['deposit'].apply(lambda x: (x == 'yes').mean())
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(46,204,113,0.1) 0%, rgba(46,204,113,0.03) 100%); border-radius: 12px; padding: 0.8rem; border: 1px solid rgba(46,204,113,0.3);">
                    <div style="font-size: 0.65rem; color: #A8885A; text-transform: uppercase;">Pinjaman Rumah (Housing)</div>
                    <div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">
                        <div><span style="color: #FFD700;">Yes:</span> <span style="color: #2ecc71; font-weight: 700;">{housing_prob.get('yes', 0):.2%}</span></div>
                        <div><span style="color: #FFD700;">No:</span> <span style="color: #e74c3c; font-weight: 700;">{housing_prob.get('no', 0):.2%}</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            if 'loan' in df.columns:
                loan_prob = df.groupby('loan')['deposit'].apply(lambda x: (x == 'yes').mean())
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(46,204,113,0.1) 0%, rgba(46,204,113,0.03) 100%); border-radius: 12px; padding: 0.8rem; border: 1px solid rgba(46,204,113,0.3);">
                    <div style="font-size: 0.65rem; color: #A8885A; text-transform: uppercase;">Pinjaman Pribadi (Loan)</div>
                    <div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">
                        <div><span style="color: #FFD700;">Yes:</span> <span style="color: #2ecc71; font-weight: 700;">{loan_prob.get('yes', 0):.2%}</span></div>
                        <div><span style="color: #FFD700;">No:</span> <span style="color: #e74c3c; font-weight: 700;">{loan_prob.get('no', 0):.2%}</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
        # ============================================
    # 3. PROBABILITAS JOINT
    # ============================================
    st.subheader("Probabilitas Joint (Probabilitas Bersama)")
    st.caption("Rumus: P(deposit=yes ∩ kondisi)")
    
    if 'deposit' in df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Joint Probability: Deposit vs Job**")
            joint_job = pd.crosstab(df['job'], df['deposit'], normalize='all')
            
            # Buat bar chart untuk joint probability
            joint_job_melted = joint_job.reset_index().melt(id_vars='job', var_name='deposit', value_name='probabilitas')
            
            fig_joint_job = px.bar(
                joint_job_melted,
                x='job',
                y='probabilitas',
                color='deposit',
                barmode='group',
                text=joint_job_melted['probabilitas'].apply(lambda x: f'{x:.2%}'),
                title='Joint Probability: Job vs Deposit',
                color_discrete_map={'yes': '#2ecc71', 'no': '#e74c3c'}
            )
            fig_joint_job.update_layout(
                title=dict(font=dict(size=12, color='#D4C4A8')),
                xaxis=dict(title='Job', tickfont=dict(color='#D4C4A8'), tickangle=45),
                yaxis=dict(title='Probabilitas Joint', tickfont=dict(color='#D4C4A8'), tickformat='.0%', gridcolor='rgba(255,255,255,0.1)'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(title='Deposit', font=dict(color='#D4C4A8')),
                height=500
            )
            fig_joint_job.update_traces(textposition='outside')
            st.plotly_chart(fig_joint_job, use_container_width=True, config={'displayModeBar': True})
        
        with col2:
            st.write("**Joint Probability: Deposit vs Education**")
            joint_edu = pd.crosstab(df['education'], df['deposit'], normalize='all')
            
            joint_edu_melted = joint_edu.reset_index().melt(id_vars='education', var_name='deposit', value_name='probabilitas')
            
            fig_joint_edu = px.bar(
                joint_edu_melted,
                x='education',
                y='probabilitas',
                color='deposit',
                barmode='group',
                text=joint_edu_melted['probabilitas'].apply(lambda x: f'{x:.2%}'),
                title='Joint Probability: Education vs Deposit',
                color_discrete_map={'yes': '#2ecc71', 'no': '#e74c3c'}
            )
            fig_joint_edu.update_layout(
                title=dict(font=dict(size=12, color='#D4C4A8')),
                xaxis=dict(title='Education', tickfont=dict(color='#D4C4A8'), tickangle=45),
                yaxis=dict(title='Probabilitas Joint', tickfont=dict(color='#D4C4A8'), tickformat='.0%', gridcolor='rgba(255,255,255,0.1)'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(title='Deposit', font=dict(color='#D4C4A8')),
                height=500
            )
            fig_joint_edu.update_traces(textposition='outside')
            st.plotly_chart(fig_joint_edu, use_container_width=True, config={'displayModeBar': True})
        
        # Interpretasi Probabilitas Joint
        st.markdown("""
        <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 0.8rem; margin-top: 1rem;">
            <span style="color: #F0E6D2; line-height: 1.6; font-size: 0.85rem;">
                Grafik menunjukkan bahwa probabilitas joint tertinggi untuk deposit yes terjadi pada kombinasi 
                <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">job 'retired' dengan deposit yes</span> 
                dan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">education 'tertiary' dengan deposit yes</span>. 
                Sebaliknya, probabilitas joint terendah terjadi pada <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #e74c3c;">job 'blue-collar' dan education 'primary' dengan deposit no</span>.
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    # ============================================
    # 4. DISTRIBUSI PROBABILITAS (KONTINU)
    # ============================================
    st.subheader("Distribusi Probabilitas (Variabel Kontinu)")
    
    continuous_vars = ['age', 'balance', 'duration']
    available_cont = [var for var in continuous_vars if var in df.columns]
    
    if available_cont:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        
        # Buat subplot untuk histogram
        fig_hist = make_subplots(rows=1, cols=len(available_cont), subplot_titles=[var.capitalize() for var in available_cont])
        
        for idx, var in enumerate(available_cont):
            mu = df[var].mean()
            std = df[var].std()
            
            fig_hist.add_trace(
                go.Histogram(x=df[var], nbinsx=50, name=var, histnorm='probability density',
                            marker_color='steelblue', opacity=0.6),
                row=1, col=idx+1
            )
            
            # Tambahkan garis distribusi normal
            x_norm = np.linspace(df[var].min(), df[var].max(), 100)
            def normal_pdf(x, mu, sigma):
                return (1/(sigma * np.sqrt(2*np.pi))) * np.exp(-0.5*((x-mu)/sigma)**2)
            y_norm = normal_pdf(x_norm, mu, std)
            
            fig_hist.add_trace(
                go.Scatter(x=x_norm, y=y_norm, mode='lines', name=f'N(μ={mu:.0f}, σ={std:.0f})',
                          line=dict(color='red', width=2)),
                row=1, col=idx+1
            )
        
        fig_hist.update_layout(
            title=dict(text='<b>Distribusi Probabilitas Variabel Kontinu</b>', font=dict(size=14, color='#FFE4A0'), x=0.5),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            height=500
        )
        fig_hist.update_xaxes(title_font=dict(color='#D4C4A8'), tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)')
        fig_hist.update_yaxes(title_font=dict(color='#D4C4A8'), tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)')
        
        st.plotly_chart(fig_hist, use_container_width=True, config={'displayModeBar': True})
        
        # Interpretasi Distribusi Kontinu
        st.markdown("""
        <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 0.8rem; margin-top: 0.5rem;">
            <span style="color: #F0E6D2; line-height: 1.6; font-size: 0.85rem;">
                Distribusi <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">usia (age)</span> cenderung mendekati normal dengan puncak di sekitar 40-50 tahun. 
                Distribusi <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">balance</span> menunjukkan skewness positif dengan mayoritas nasabah memiliki saldo rendah. 
                Distribusi <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">duration</span> juga skewness positif, artinya sebagian besar panggilan berdurasi pendek hingga sedang.
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Statistik distribusi
        with st.expander("Statistik Distribusi Variabel Kontinu"):
            for var in available_cont:
                st.markdown(f"""
                <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 0.8rem; margin: 0.5rem 0;">
                    <span style="color: #FFD700; font-weight: 700;">{var.upper()}</span>
                    <div style="display: flex; flex-wrap: wrap; gap: 1rem; margin-top: 0.5rem;">
                        <div><span style="color: #A8885A;">Mean (μ):</span> <span style="color: #D4C4A8;">{df[var].mean():.2f}</span></div>
                        <div><span style="color: #A8885A;">Median:</span> <span style="color: #D4C4A8;">{df[var].median():.2f}</span></div>
                        <div><span style="color: #A8885A;">Std Dev (σ):</span> <span style="color: #D4C4A8;">{df[var].std():.2f}</span></div>
                        <div><span style="color: #A8885A;">Skewness:</span> <span style="color: #D4C4A8;">{df[var].skew():.3f}</span></div>
                        <div><span style="color: #A8885A;">Kurtosis:</span> <span style="color: #D4C4A8;">{df[var].kurtosis():.3f}</span></div>
                        <div><span style="color: #A8885A;">Range:</span> <span style="color: #D4C4A8;">{df[var].min():.2f} - {df[var].max():.2f}</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # ============================================
    # 5. DISTRIBUSI PROBABILITAS (DISKRIT)
    # ============================================
    st.subheader("Distribusi Probabilitas (Variabel Diskrit)")
    
    discrete_vars = ['job', 'education', 'marital', 'housing', 'loan']
    available_disc = [var for var in discrete_vars if var in df.columns]
    
    if available_disc:
        # Gunakan plotly pie chart untuk variabel diskrit
        import plotly.express as px
        
        disc_cols = st.columns(min(3, len(available_disc)))
        for idx, var in enumerate(available_disc[:3]):
            dist = df[var].value_counts(normalize=True).reset_index()
            dist.columns = [var, 'probabilitas']
            
            fig_disc = px.pie(
                dist, 
                names=var, 
                values='probabilitas',
                title=f'Distribusi {var.capitalize()}',
                hole=0.3,
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            fig_disc.update_layout(
                title=dict(font=dict(size=12, color='#D4C4A8')),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(font=dict(color='#D4C4A8'), bgcolor='rgba(0,0,0,0.5)'),
                height=350
            )
            with disc_cols[idx]:
                st.plotly_chart(fig_disc, use_container_width=True, config={'displayModeBar': True})
        
        # Interpretasi Distribusi Diskrit
        st.markdown("""
        <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 0.8rem; margin-top: 0.5rem;">
            <span style="color: #F0E6D2; line-height: 1.6; font-size: 0.85rem;"> 
                Sebagian besar nasabah memiliki pekerjaan sebagai <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">'blue-collar' dan 'management'</span>. 
                Tingkat pendidikan didominasi oleh <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">'secondary' dan 'tertiary'</span>. 
                Status <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">'married'</span> merupakan proporsi tertinggi pada status pernikahan nasabah.
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    # ============================================
    # 6. MODEL RISIKO (RISK PROFILE)
    # ============================================
    st.subheader("Model Risiko (Risk Profile Berdasarkan Probabilitas)")
    
    if 'deposit' in df.columns and 'job' in df.columns and 'education' in df.columns:
        
        def risk_category(p):
            if p < 0.3:
                return 'Sangat Tinggi (P<30%)'
            elif p < 0.45:
                return 'Tinggi (30-45%)'
            elif p < 0.55:
                return 'Sedang (45-55%)'
            elif p < 0.7:
                return 'Rendah (55-70%)'
            else:
                return 'Sangat Rendah (≥70%)'
        
        # Hitung P(yes) untuk setiap kombinasi job & education
        risk_model = df.groupby(['job', 'education']).agg({
            'deposit': lambda x: (x == 'yes').mean(),
        }).reset_index()
        risk_model.columns = ['job', 'education', 'p_deposit_yes']
        risk_model['risk_level'] = risk_model['p_deposit_yes'].apply(risk_category)
        risk_model['risk_score'] = 1 - risk_model['p_deposit_yes']
        
        st.write("**Model Risiko (berdasarkan Job & Education):**")
        st.dataframe(risk_model.sort_values('p_deposit_yes', ascending=False), use_container_width=True, hide_index=True)
        
        # Distribusi kategori risiko dengan plotly
        risk_counts = risk_model['risk_level'].value_counts().reset_index()
        risk_counts.columns = ['Kategori Risiko', 'Jumlah Segment']
        
        colors_risk = {
            'Sangat Rendah (≥70%)': '#2ecc71',
            'Rendah (55-70%)': '#3498db',
            'Sedang (45-55%)': '#f39c12',
            'Tinggi (30-45%)': '#e67e22',
            'Sangat Tinggi (P<30%)': '#e74c3c'
        }
        
        fig_risk = px.bar(
            risk_counts,
            x='Kategori Risiko',
            y='Jumlah Segment',
            color='Kategori Risiko',
            color_discrete_map=colors_risk,
            title='Distribusi Kategori Risiko'
        )
        fig_risk.update_layout(
            title=dict(font=dict(size=14, color='#FFE4A0'), x=0.5),
            xaxis=dict(title='Kategori Risiko', tickfont=dict(color='#D4C4A8'), tickangle=45),
            yaxis=dict(title='Jumlah Segment', tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            height=450
        )
        fig_risk.update_traces(texttemplate='%{y}', textposition='outside')
        st.plotly_chart(fig_risk, use_container_width=True, config={'displayModeBar': True})
    
        # ============================================
    # 7. APLIKASI: PREDIKSI PROBABILITAS
    # ============================================
    st.subheader("Aplikasi: Prediksi Probabilitas untuk Nasabah Baru")
    
    if 'deposit' in df.columns:
        # Buat dictionary probabilitas dari data
        job_prob_dict = df.groupby('job')['deposit'].apply(lambda x: (x == 'yes').mean()).to_dict()
        edu_prob_dict = df.groupby('education')['deposit'].apply(lambda x: (x == 'yes').mean()).to_dict()
        base_prob = (df['deposit'] == 'yes').mean()
        
        # Fungsi prediksi
        def predict_deposit_probability(job, education, balance=0, housing='no'):
            job_p = job_prob_dict.get(job, base_prob)
            edu_p = edu_prob_dict.get(education, base_prob)
            final_prob = (job_p * 0.5 + edu_p * 0.5)
            return final_prob
        
        # CSS untuk styling input dan hasil prediksi
        st.markdown("""
        <style>
        .prediction-container {
            background: rgba(0,0,0,0.25);
            border-radius: 16px;
            padding: 1.2rem;
            margin: 0.5rem 0;
        }
        .prediction-result {
            background: linear-gradient(135deg, rgba(255,215,0,0.1) 0%, rgba(255,215,0,0.02) 100%);
            border-radius: 14px;
            padding: 1rem;
            text-align: center;
            border: 1px solid rgba(255,215,0,0.3);
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .result-label {
            font-size: 0.7rem;
            color: #A8885A;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .result-value {
            font-size: 2.2rem;
            font-weight: 700;
            margin: 0.3rem 0;
        }
        .result-risk {
            font-size: 0.8rem;
            margin-top: 0.3rem;
        }
        .prediction-placeholder {
            background: rgba(0,0,0,0.3);
            border-radius: 14px;
            padding: 1rem;
            text-align: center;
            border: 1px solid rgba(255,215,0,0.15);
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="prediction-container">', unsafe_allow_html=True)
        
        # Layout dengan 3 kolom yang lebih rapi
        col_left, col_mid, col_right = st.columns([1.2, 1.2, 1.2])
        
        with col_left:
            selected_job = st.selectbox(
                "Pilih Pekerjaan", 
                list(job_prob_dict.keys()),
                help="Pilih jenis pekerjaan nasabah"
            )
        
        with col_mid:
            selected_education = st.selectbox(
                "Pilih Pendidikan", 
                list(edu_prob_dict.keys()),
                help="Pilih tingkat pendidikan nasabah"
            )
        
        with col_right:
            st.markdown('<div style="margin-top: 1.8rem;">', unsafe_allow_html=True)
            predict_clicked = st.button(
                "Prediksi Probabilitas", 
                use_container_width=True,
                type="primary"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Hasil Prediksi
        if predict_clicked:
            prob = predict_deposit_probability(selected_job, selected_education)
            
            # Kategorisasi risiko
            if prob < 0.3:
                risk_level = "Sangat Tinggi"
                risk_icon = "🔴"
                color = "#e74c3c"
                bg_color = "rgba(231,76,60,0.15)"
            elif prob < 0.45:
                risk_level = "Tinggi"
                risk_icon = "🟠"
                color = "#e67e22"
                bg_color = "rgba(230,126,34,0.15)"
            elif prob < 0.55:
                risk_level = "Sedang"
                risk_icon = "🟡"
                color = "#f39c12"
                bg_color = "rgba(243,156,18,0.15)"
            elif prob < 0.7:
                risk_level = "Rendah"
                risk_icon = "🟢"
                color = "#2ecc71"
                bg_color = "rgba(46,204,113,0.15)"
            else:
                risk_level = "Sangat Rendah"
                risk_icon = "✅"
                color = "#27ae60"
                bg_color = "rgba(39,174,96,0.15)"
            
            st.markdown(f"""
            <div style="margin-top: 1rem;">
                <div style="background: {bg_color}; border-radius: 16px; padding: 1.2rem; text-align: center; border: 1px solid {color}40;">
                    <div style="display: flex; align-items: center; justify-content: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                        <span style="font-size: 0.75rem; color: #A8885A; text-transform: uppercase; letter-spacing: 1px;">Hasil Prediksi Probabilitas Deposit</span>
                    </div>
                    <div style="font-size: 2.8rem; font-weight: 800; color: {color}; margin: 0.3rem 0;">{prob:.2%}</div>
                    <div style="display: flex; align-items: center; justify-content: center; gap: 0.3rem; margin-top: 0.3rem;">
                        <span style="font-size: 1rem;">{risk_icon}</span>
                        <span style="font-size: 0.85rem; color: #D4C4A8;">Kategori Risiko: <strong style="color: {color};">{risk_level}</strong></span>
                    </div>
                    <div style="margin-top: 0.8rem; padding-top: 0.5rem; border-top: 1px solid rgba(255,215,0,0.2);">
                        <span style="font-size: 0.7rem; color: #A8885A;">
                            💼 {selected_job} | 🎓 {selected_education}
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="margin-top: 1rem;">
                <div style="background: rgba(0,0,0,0.25); border-radius: 16px; padding: 1.2rem; text-align: center; border: 1px dashed rgba(255,215,0,0.3);">
                    <div style="display: flex; align-items: center; justify-content: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                        <span style="font-size: 0.75rem; color: #A8885A; text-transform: uppercase; letter-spacing: 1px;">Hasil Prediksi</span>
                    </div>
                    <div style="font-size: 2rem; font-weight: 700; color: #A8885A; margin: 0.5rem 0;">---</div>
                    <div style="font-size: 0.7rem; color: #A8885A;">Silakan pilih pekerjaan dan pendidikan, lalu klik tombol prediksi</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ============================================
    # 8. OUTPUT UNTUK DSS
    # ============================================
    st.subheader("Output untuk Decision Support System (DSS)")
    
    if 'deposit' in df.columns and all(col in df.columns for col in ['job', 'education']):
        
        def risk_category_dss(p):
            if p < 0.3:
                return 'Sangat Tinggi'
            elif p < 0.45:
                return 'Tinggi'
            elif p < 0.55:
                return 'Sedang'
            elif p < 0.7:
                return 'Rendah'
            else:
                return 'Sangat Rendah'
        
        # Buat dataframe probabilitas untuk semua nasabah
        df_prob = df.copy()
        df_prob['p_deposit_pred'] = df_prob.apply(
            lambda x: predict_deposit_probability(x['job'], x['education']),
            axis=1
        )
        df_prob['risk_category'] = df_prob['p_deposit_pred'].apply(risk_category_dss)
        df_prob['recommendation'] = df_prob['p_deposit_pred'].apply(
            lambda x: 'PRIORITAS' if x > 0.6 else ('TARGET' if x > 0.45 else 'KURANG PRIORITAS')
        )
        
        st.write("**Contoh Output DSS (10 nasabah pertama):**")
        display_cols = ['age', 'job', 'education', 'balance', 'p_deposit_pred', 'risk_category', 'recommendation']
        available_cols = [col for col in display_cols if col in df_prob.columns]
        st.dataframe(df_prob[available_cols].head(10), use_container_width=True, hide_index=True)
        
        # Statistik rekomendasi dalam bentuk card
        rec_stats = df_prob['recommendation'].value_counts()
        
        st.markdown("""
        <div style="margin-top: 1rem;">
            <div style="background: rgba(0,0,0,0.3); border-radius: 12px; padding: 0.8rem; margin-bottom: 0.8rem;">
                <span style="font-size: 0.8rem; font-weight: 600; color: #FFD700;">Statistik Rekomendasi DSS</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        rec_cols = st.columns(3)
        colors_rec = {'PRIORITAS': '#2ecc71', 'TARGET': '#f39c12', 'KURANG PRIORITAS': '#e74c3c'}
        for idx, (rec, count) in enumerate(rec_stats.items()):
            with rec_cols[idx % 3]:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {colors_rec.get(rec, '#3498db')}15 0%, {colors_rec.get(rec, '#3498db')}05 100%); border-radius: 12px; padding: 0.8rem; text-align: center; border: 1px solid {colors_rec.get(rec, '#3498db')}40;">
                    <div style="font-size: 0.7rem; color: #A8885A; text-transform: uppercase;">{rec}</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: {colors_rec.get(rec, '#3498db')};">{count:,}</div>
                    <div style="font-size: 0.65rem; color: #D4C4A8;">({count/len(df_prob)*100:.1f}%)</div>
                </div>
                """, unsafe_allow_html=True)
    
    # ============================================
    # 9. RINGKASAN AKHIR (DALAM BENTUK PARAGRAF DENGAN HIGHLIGHT)
    # ============================================
    st.subheader("Ringkasan Analisis Probabilistic Modeling")
    
    if 'deposit' in df.columns:
        p_yes = (df['deposit'] == 'yes').mean()
        yes_count = (df['deposit'] == 'yes').sum()
        no_count = (df['deposit'] == 'no').sum()
        
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.4); padding: 1.5rem; border-radius: 10px; line-height: 1.8;">
        <p style="color: #F0E6D2; margin-bottom: 1rem;">
            <span style="color: #FFE4A0; font-weight: 700;">Tujuan 1: Mengubah data menjadi probabilitas</span><br>
            Berdasarkan analisis, diperoleh <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">probabilitas marginal P(yes) = {p_yes:.2%}</span> 
            dan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">P(no) = {(1-p_yes):.2%}</span>. 
            Probabilitas bersyarat menunjukkan bahwa faktor <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">pekerjaan (job) dan pendidikan (education)</span> 
            memiliki pengaruh signifikan terhadap keputusan deposit, dengan nilai probabilitas tertinggi pada kategori tertentu.
        </p>
            
        <p style="color: #F0E6D2; margin-bottom: 1rem;">
            <span style="color: #FFE4A0; font-weight: 700;">Tujuan 2: Memahami distribusi peluang</span><br>
            Distribusi variabel kontinu seperti <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">age, balance, dan duration</span> 
            telah diidentifikasi beserta parameter statistiknya (mean, median, skewness, kurtosis). 
            Sementara itu, distribusi variabel diskrit seperti <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">job, education, marital, housing, dan loan</span> 
            memberikan gambaran tentang komposisi nasabah berdasarkan karakteristik demografis dan keuangannya.
        </p>
            
        <p style="color: #F0E6D2; margin-bottom: 0;">
            <span style="color: #FFE4A0; font-weight: 700;">Tujuan 3: Membangun model risiko</span><br>
            Model risiko berhasil dibangun dengan menghasilkan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">risk matrix dan kategori risiko</span> 
            berdasarkan kombinasi job dan education. <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Prediksi probabilitas untuk nasabah baru</span> 
            dapat dilakukan secara interaktif, dan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">output siap pakai untuk Decision Support System (DSS)</span> 
            dengan rekomendasi PRIORITAS, TARGET, atau KURANG PRIORITAS. 
            Total nasabah sebanyak <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">{len(df):,}</span>, 
            dengan deposit yes sebanyak <span style="background: rgba(46,204,113,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #2ecc71;">{yes_count:,} ({p_yes:.2%})</span> 
            dan deposit no sebanyak <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #e74c3c;">{no_count:,} ({(1-p_yes):.2%})</span>.
        </p>
        </div>
        """, unsafe_allow_html=True)
    


def analysis_sensitivity(df):
    """Analisis Sensitivity & Simulation"""
    st.header("🔄 Analisis Sensitivity & Simulation")
    
    st.markdown("""
    <div style="background: rgba(0,0,0,0.4); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
    <b>Konsep:</b> Sensitivity Analysis menguji bagaimana perubahan parameter input mempengaruhi 
    hasil keputusan. Simulation menggunakan Monte Carlo untuk memodelkan berbagai skenario.
    </div>
    """, unsafe_allow_html=True)
    
    if 'duration' in df.columns and 'deposit_binary' in df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Sensitivity: Pengaruh Durasi Panggilan")
            
            # Bins durasi
            df['duration_group'] = pd.cut(df['duration'], bins=[0, 100, 300, 600, 1000, 5000], 
                                           labels=['<100', '100-300', '300-600', '600-1000', '>1000'])
            duration_success = df.groupby('duration_group')['deposit_binary'].mean() * 100
            
            fig, ax = plt.subplots(figsize=(10, 6))
            duration_success.plot(kind='bar', ax=ax, color='purple')
            ax.set_xlabel('Durasi Panggilan (detik)')
            ax.set_ylabel('Keberhasilan Deposit (%)')
            ax.set_title('Sensitivity: Durasi vs Keberhasilan')
            plt.xticks(rotation=0)
            st.pyplot(fig)
            plt.close()
        
        with col2:
            st.subheader("Sensitivity: Pengaruh Jumlah Kontak")
            
            if 'campaign' in df.columns:
                df['campaign_group'] = pd.cut(df['campaign'], bins=[0, 2, 4, 6, 10, 50],
                                               labels=['1-2', '3-4', '5-6', '7-10', '>10'])
                campaign_success = df.groupby('campaign_group')['deposit_binary'].mean() * 100
                
                fig, ax = plt.subplots(figsize=(10, 6))
                campaign_success.plot(kind='bar', ax=ax, color='olive')
                ax.set_xlabel('Jumlah Kontak per Kampanye')
                ax.set_ylabel('Keberhasilan Deposit (%)')
                ax.set_title('Sensitivity: Jumlah Kontak vs Keberhasilan')
                plt.xticks(rotation=0)
                st.pyplot(fig)
                plt.close()
    
    # Monte Carlo Simulation
    if 'deposit_binary' in df.columns:
        st.subheader("🎲 Monte Carlo Simulation")
        
        n_simulations = st.slider("Jumlah Simulasi", 100, 10000, 1000, step=100)
        
        # Simulasi
        np.random.seed(42)
        base_rate = df['deposit_binary'].mean()
        simulated_rates = np.random.binomial(n=n_simulations, p=base_rate, size=1000) / n_simulations * 100
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(simulated_rates, bins=30, color='goldenrod', edgecolor='black', alpha=0.7)
        ax.axvline(base_rate * 100, color='red', linestyle='--', linewidth=2, label=f'Base Rate: {base_rate*100:.1f}%')
        ax.set_xlabel('Tingkat Keberhasilan (%)')
        ax.set_ylabel('Frekuensi')
        ax.set_title(f'Monte Carlo Simulation - Distribusi Tingkat Keberhasilan ({n_simulations} iterasi)')
        ax.legend()
        st.pyplot(fig)
        plt.close()
        
        # Confidence interval
        lower_bound = np.percentile(simulated_rates, 2.5)
        upper_bound = np.percentile(simulated_rates, 97.5)
        
        st.info(f"""
        **Hasil Simulasi ({n_simulations:,} iterasi):**
        - Rata-rata keberhasilan: {simulated_rates.mean():.1f}%
        - Confidence Interval 95%: [{lower_bound:.1f}% - {upper_bound:.1f}%]
        - Base rate aktual: {base_rate*100:.1f}%
        
        Dengan tingkat keyakinan 95%, keberhasilan kampanye diperkirakan 
        berada dalam rentang {lower_bound:.1f}% hingga {upper_bound:.1f}%.
        """)


def analysis_utility(df):
    """Analisis Utility & Risk Preference - dengan Logistic Regression dan Expected Value"""
    st.header("Analisis Utility & Risk Preference")
    
    # =========================================================
    # PENJELASAN MATERI DALAM 3 PARAGRAF DENGAN HIGHLIGHT
    # =========================================================
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); padding: 1.2rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #DAA520;">
        <p style="color: #F0E6D2; line-height: 1.6; margin-bottom: 1rem;">
            <span style="background: linear-gradient(120deg, rgba(218,165,32,0.2) 0%, rgba(218,165,32,0.2) 100%); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFE4A0;">Utility Theory</span> 
            merupakan konsep dalam pengambilan keputusan yang <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">mempertimbangkan preferensi risiko pengambil keputusan</span>, 
            berbeda dengan Expected Value (EV) yang hanya fokus pada keuntungan rata-rata. 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Utility function mengkonversi payoff menjadi nilai utilitas</span> 
            berdasarkan tingkat toleransi risiko, sehingga dua keputusan dengan EV yang sama dapat memiliki nilai utility yang berbeda tergantung profil risiko pengambil keputusan.
        </p>
        <p style="color: #F0E6D2; line-height: 1.6; margin-bottom: 1rem;">
            Terdapat <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">tiga tipe risk preference</span> yang umum dikenal: 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Risk Averse (menghindari risiko)</span> dengan fungsi utility cekung (concave) seperti U = √x, 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Risk Neutral (netral risiko)</span> dengan fungsi utility linear U = x, 
            dan <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Risk Seeking (menyukai risiko)</span> dengan fungsi utility cembung (convex) seperti U = x².
            Pemilihan tipe risk preference sangat bergantung pada <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">karakteristik dan tujuan organisasi</span>.
        </p>
        <p style="color: #F0E6D2; line-height: 1.6;">
            Keunggulan pendekatan ini adalah <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">mampu mengakomodasi preferensi risiko yang berbeda</span>, 
            namun kelemahannya adalah <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #e74c3c;">memerlukan penentuan fungsi utility yang subjektif</span>. 
            Pendekatan ini paling cocok digunakan ketika <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">profil risiko pengambil keputusan telah diketahui</span> 
            dan <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">keputusan perlu disesuaikan dengan toleransi risiko organisasi</span>, 
            seperti dalam konteks perbankan yang umumnya cenderung <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Risk Averse</span>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # =========================================================
    # KONSEP DAN PENDEKATAN
    # =========================================================
    st.markdown("""
    <div style="background: rgba(0,0,0,0.4); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
        <b style="color: #FFE4A0; font-size: 1.05rem;">📌 Konsep Utility & Risk Preference:</b><br>
        <span style="color: #D4C4A8;">1. <span style="color: #FFD700; font-weight: 500;">Expected Value (EV)</span>: Keuntungan rata-rata tanpa mempertimbangkan risiko<br>
        2. <span style="color: #FFD700; font-weight: 500;">Utility Function</span>: Mengkonversi payoff menjadi nilai kepuasan subjektif<br>
        3. <span style="color: #FFD700; font-weight: 500;">Risk Averse</span>: Menghindari risiko (utility cekung/concave)<br>
        4. <span style="color: #FFD700; font-weight: 500;">Risk Neutral</span>: Netral risiko (utility linear)<br>
        5. <span style="color: #FFD700; font-weight: 500;">Risk Seeking</span>: Menyukai risiko (utility cembung/convex)</span><br><br>
        <b style="color: #FFE4A0; font-size: 1.05rem;">📌 Pendekatan ini cocok untuk:</b><br>
        <span style="color: #D4C4A8;">• <span style="color: #FFD700;">Situasi dengan preferensi risiko yang jelas</span> dari pengambil keputusan<br>
        • <span style="color: #FFD700;">Evaluasi strategi</span> dengan mempertimbangkan toleransi risiko bank<br>
        • <span style="color: #FFD700;">Perbandingan keputusan</span> antara EV dan utility untuk melihat pengaruh preferensi risiko</span>
    </div>
    """, unsafe_allow_html=True)
    
        # =========================================================
    # 1. ANALISIS TARGET (DEPOSIT) - GRAFIK BATANG & CARD
    # =========================================================
    st.subheader("Distribusi Target Deposit")
    
    if 'deposit' in df.columns:
        deposit_counts = df['deposit'].value_counts()
        yes_count = deposit_counts.get('yes', 0)
        no_count = deposit_counts.get('no', 0)
        yes_pct = (yes_count / len(df)) * 100
        no_pct = (no_count / len(df)) * 100
        
        # Row untuk 2 card (Deposit Yes dan No)
        st.markdown(f"""
        <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
            <div style="flex: 1; background: linear-gradient(135deg, rgba(46,204,113,0.15) 0%, rgba(46,204,113,0.05) 100%); border-radius: 14px; padding: 1rem; text-align: center; border: 1px solid rgba(46,204,113,0.3);">
                <div style="font-size: 0.7rem; color: #A8885A; text-transform: uppercase;">Deposit Yes</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #2ecc71;">{yes_count:,}</div>
                <div style="font-size: 0.8rem; color: #D4C4A8;">({yes_pct:.1f}%)</div>
            </div>
            <div style="flex: 1; background: linear-gradient(135deg, rgba(231,76,60,0.15) 0%, rgba(231,76,60,0.05) 100%); border-radius: 14px; padding: 1rem; text-align: center; border: 1px solid rgba(231,76,60,0.3);">
                <div style="font-size: 0.7rem; color: #A8885A; text-transform: uppercase;">Deposit No</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #e74c3c;">{no_count:,}</div>
                <div style="font-size: 0.8rem; color: #D4C4A8;">({no_pct:.1f}%)</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Bar chart horizontal di bawah kedua card
        import plotly.express as px
        fig_target = px.bar(
            x=[yes_count, no_count],
            y=['Deposit Yes', 'Deposit No'],
            orientation='h',
            color=['Deposit Yes', 'Deposit No'],
            color_discrete_map={'Deposit Yes': '#2ecc71', 'Deposit No': '#e74c3c'},
            text=[f'{yes_count:,} ({yes_pct:.1f}%)', f'{no_count:,} ({no_pct:.1f}%)'],
            title='Distribusi Target Deposit'
        )
        fig_target.update_layout(
            title=dict(font=dict(size=13, color='#FFE4A0'), x=0.5),
            xaxis=dict(title='Jumlah Nasabah', tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title='', tickfont=dict(color='#D4C4A8')),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            height=200,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        fig_target.update_traces(textposition='outside', textfont=dict(color='#D4C4A8', size=11))
        st.plotly_chart(fig_target, use_container_width=True, config={'displayModeBar': False})
    
    # =========================================================
    # 2. ANALISIS BERDASARKAN BALANCE (BOXPLOT INTERAKTIF)
    # =========================================================
    st.subheader("Analisis Balance vs Deposit")
    
    if 'balance' in df.columns and 'deposit' in df.columns:
        import plotly.graph_objects as go
        
        fig_balance = go.Figure()
        
        # Boxplot untuk Deposit Yes
        fig_balance.add_trace(go.Box(
            y=df[df['deposit'] == 'yes']['balance'],
            name='Deposit Yes',
            marker_color='#2ecc71',
            boxmean='sd',
            boxpoints='outliers'
        ))
        
        # Boxplot untuk Deposit No
        fig_balance.add_trace(go.Box(
            y=df[df['deposit'] == 'no']['balance'],
            name='Deposit No',
            marker_color='#e74c3c',
            boxmean='sd',
            boxpoints='outliers'
        ))
        
        fig_balance.update_layout(
            title=dict(text='<b>Distribusi Balance berdasarkan Status Deposit</b>', font=dict(size=14, color='#FFE4A0'), x=0.5),
            xaxis=dict(title='Status Deposit', tickfont=dict(color='#D4C4A8')),
            yaxis=dict(title='Balance', tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(font=dict(color='#D4C4A8'), bgcolor='rgba(0,0,0,0.5)'),
            height=450
        )
        
        st.plotly_chart(fig_balance, use_container_width=True, config={'displayModeBar': True})
        
        st.markdown("""
        <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 0.8rem; margin-top: 0.5rem;">
            <span style="color: #F0E6D2; line-height: 1.6; font-size: 0.85rem;">
                Nasabah dengan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">deposit yes memiliki median balance yang lebih tinggi</span> 
                dibandingkan deposit no. Hal ini mengindikasikan bahwa <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">nasabah dengan saldo lebih besar cenderung lebih menerima penawaran deposito</span>, 
                sehingga bank sebaiknya memprioritaskan nasabah dengan balance tinggi.
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    # =========================================================
    # 3. ANALISIS BERDASARKAN DURATION (BOXPLOT INTERAKTIF)
    # =========================================================
    st.subheader("Analisis Duration vs Deposit")
    
    if 'duration' in df.columns and 'deposit' in df.columns:
        fig_duration = go.Figure()
        
        fig_duration.add_trace(go.Box(
            y=df[df['deposit'] == 'yes']['duration'],
            name='Deposit Yes',
            marker_color='#2ecc71',
            boxmean='sd',
            boxpoints='outliers'
        ))
        
        fig_duration.add_trace(go.Box(
            y=df[df['deposit'] == 'no']['duration'],
            name='Deposit No',
            marker_color='#e74c3c',
            boxmean='sd',
            boxpoints='outliers'
        ))
        
        fig_duration.update_layout(
            title=dict(text='<b>Distribusi Duration berdasarkan Status Deposit</b>', font=dict(size=14, color='#FFE4A0'), x=0.5),
            xaxis=dict(title='Status Deposit', tickfont=dict(color='#D4C4A8')),
            yaxis=dict(title='Duration (detik)', tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(font=dict(color='#D4C4A8'), bgcolor='rgba(0,0,0,0.5)'),
            height=450
        )
        
        st.plotly_chart(fig_duration, use_container_width=True, config={'displayModeBar': True})
        
        st.markdown("""
        <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 0.8rem; margin-top: 0.5rem;">
            <span style="color: #F0E6D2; line-height: 1.6; font-size: 0.85rem;">
                Terlihat bahwa <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">nasabah dengan deposit yes memiliki durasi panggilan yang lebih panjang</span> 
                dibandingkan deposit no. Hal ini menunjukkan bahwa <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">semakin lama durasi telepon, semakin tinggi peluang nasabah menerima penawaran deposito</span>, 
                sehingga durasi panggilan dapat menjadi indikator penting dalam strategi pemasaran.
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    # =========================================================
    # 4. ENCODING & PREPARASI DATA
    # =========================================================
    st.subheader("Persiapan Data untuk Modeling")
    
    # Copy data
    data = df.copy()
    
    # Label encoding untuk kolom kategorik
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    
    cat_cols = data.select_dtypes(include='object').columns
    
    for col in cat_cols:
        if col != 'deposit':
            data[col] = le.fit_transform(data[col].astype(str))
    
    # Pisahkan fitur dan target
    if 'deposit' in data.columns:
        data['deposit'] = le.fit_transform(data['deposit'])
        
        X = data.drop('deposit', axis=1)
        y = data['deposit']
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style="background: rgba(52,152,219,0.1); border-radius: 12px; padding: 0.8rem; text-align: center; border: 1px solid rgba(52,152,219,0.3);">
                <div style="font-size: 0.7rem; color: #A8885A;">Jumlah Fitur</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #3498db;">{X.shape[1]}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="background: rgba(52,152,219,0.1); border-radius: 12px; padding: 0.8rem; text-align: center; border: 1px solid rgba(52,152,219,0.3);">
                <div style="font-size: 0.7rem; color: #A8885A;">Target</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #FFD700;">deposit (0=no, 1=yes)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("Lihat hasil encoding (5 data pertama)"):
            st.dataframe(data.head(), use_container_width=True)
    
    # =========================================================
    # 5. SPLIT DATA TRAIN-TEST (DALAM BENTUK CARD)
    # =========================================================
    st.subheader("Split Data Training & Testing")
    
    from sklearn.model_selection import train_test_split
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(46,204,113,0.1) 0%, rgba(46,204,113,0.03) 100%); border-radius: 14px; padding: 1rem; text-align: center; border: 1px solid rgba(46,204,113,0.3);">
            <div style="font-size: 0.7rem; color: #A8885A; text-transform: uppercase;">Data Training</div>
            <div style="font-size: 1.6rem; font-weight: 700; color: #2ecc71;">{X_train.shape[0]:,}</div>
            <div style="font-size: 0.7rem; color: #D4C4A8;">nasabah ({X_train.shape[0]/len(X)*100:.0f}%)</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(231,76,60,0.1) 0%, rgba(231,76,60,0.03) 100%); border-radius: 14px; padding: 1rem; text-align: center; border: 1px solid rgba(231,76,60,0.3);">
            <div style="font-size: 0.7rem; color: #A8885A; text-transform: uppercase;">Data Testing</div>
            <div style="font-size: 1.6rem; font-weight: 700; color: #e74c3c;">{X_test.shape[0]:,}</div>
            <div style="font-size: 0.7rem; color: #D4C4A8;">nasabah ({X_test.shape[0]/len(X)*100:.0f}%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    # =========================================================
    # 6. LOGISTIC REGRESSION MODEL
    # =========================================================
    st.subheader("Logistic Regression Model")
    
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
    
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)
    
    # Prediksi
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)
    
    akurasi = accuracy_score(y_test, y_pred) * 100
    
    # Layout: Heatmap di tengah, akurasi di bawah
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Confusion Matrix Heatmap dengan plotly
        cm = confusion_matrix(y_test, y_pred)
        import plotly.express as px
        
        fig_cm = px.imshow(
            cm,
            text_auto=True,
            x=['No Deposit', 'Deposit'],
            y=['No Deposit', 'Deposit'],
            color_continuous_scale='Blues',
            title='Confusion Matrix'
        )
        fig_cm.update_layout(
            title=dict(font=dict(size=14, color='#FFE4A0'), x=0.5),
            xaxis=dict(title='Predicted', tickfont=dict(color='#D4C4A8')),
            yaxis=dict(title='Actual', tickfont=dict(color='#D4C4A8')),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        st.plotly_chart(fig_cm, use_container_width=True, config={'displayModeBar': True})
    
    # Akurasi Model dalam card yang menarik
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(255,215,0,0.15) 0%, rgba(255,215,0,0.05) 100%); border-radius: 16px; padding: 1.2rem; text-align: center; border: 1px solid rgba(255,215,0,0.4); margin: 1rem 0;">
        <div style="display: flex; align-items: center; justify-content: center; gap: 0.8rem;">
            <div>
                <div style="font-size: 0.7rem; color: #A8885A; text-transform: uppercase; letter-spacing: 1px;">Akurasi Model</div>
                <div style="font-size: 2.2rem; font-weight: 800; color: #FFD700;">{akurasi:.2f}%</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Classification Report dalam bentuk card metrics (bukan tabel)
    st.markdown("""
    <div style="margin-top: 1rem;">
        <div style="background: rgba(0,0,0,0.3); border-radius: 12px; padding: 0.8rem; margin-bottom: 1rem;">
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hitung metrics dari classification report
    report = classification_report(y_test, y_pred, output_dict=True)
    
    # Ambil metrics untuk class 0 (No Deposit) dan class 1 (Deposit)
    precision_0 = report['0']['precision']
    recall_0 = report['0']['recall']
    f1_0 = report['0']['f1-score']
    
    precision_1 = report['1']['precision']
    recall_1 = report['1']['recall']
    f1_1 = report['1']['f1-score']
    
    # Tampilkan metrics dalam bentuk card yang rapi
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(231,76,60,0.1) 0%, rgba(231,76,60,0.03) 100%); border-radius: 14px; padding: 0.8rem; text-align: center; border: 1px solid rgba(231,76,60,0.3); margin-bottom: 0.5rem;">
            <div style="font-size: 0.65rem; color: #A8885A; text-transform: uppercase;">No Deposit (Class 0)</div>
            <div style="display: flex; justify-content: space-around; margin-top: 0.5rem;">
                <div><span style="font-size: 0.6rem; color: #A8885A;">Precision</span><br><span style="font-size: 1.1rem; font-weight: 700; color: #e74c3c;">{precision_0:.3f}</span></div>
                <div><span style="font-size: 0.6rem; color: #A8885A;">Recall</span><br><span style="font-size: 1.1rem; font-weight: 700; color: #e74c3c;">{recall_0:.3f}</span></div>
                <div><span style="font-size: 0.6rem; color: #A8885A;">F1-Score</span><br><span style="font-size: 1.1rem; font-weight: 700; color: #e74c3c;">{f1_0:.3f}</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(46,204,113,0.1) 0%, rgba(46,204,113,0.03) 100%); border-radius: 14px; padding: 0.8rem; text-align: center; border: 1px solid rgba(46,204,113,0.3); margin-bottom: 0.5rem;">
            <div style="font-size: 0.65rem; color: #A8885A; text-transform: uppercase;">Deposit (Class 1)</div>
            <div style="display: flex; justify-content: space-around; margin-top: 0.5rem;">
                <div><span style="font-size: 0.6rem; color: #A8885A;">Precision</span><br><span style="font-size: 1.1rem; font-weight: 700; color: #2ecc71;">{precision_1:.3f}</span></div>
                <div><span style="font-size: 0.6rem; color: #A8885A;">Recall</span><br><span style="font-size: 1.1rem; font-weight: 700; color: #2ecc71;">{recall_1:.3f}</span></div>
                <div><span style="font-size: 0.6rem; color: #A8885A;">F1-Score</span><br><span style="font-size: 1.1rem; font-weight: 700; color: #2ecc71;">{f1_1:.3f}</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Interpretasi Classification Report
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 0.8rem; margin-top: 0.5rem;">
        <span style="color: #F0E6D2; line-height: 1.6; font-size: 0.85rem;">
            Model memiliki <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">precision untuk kelas Deposit sebesar 0.999</span>, 
            artinya <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">99.9% dari prediksi deposit adalah benar</span>. 
            Nilai <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">recall sebesar 0.998</span> menunjukkan bahwa model mampu menangkap 
            <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">99.8% dari seluruh nasabah yang benar-benar deposit</span>. 
            Secara keseluruhan, <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">F1-Score sebesar 0.999</span> mengindikasikan performa model yang cukup baik dalam memprediksi keputusan deposit.
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # =========================================================
    # 7. ANALISIS EXPECTED VALUE (EV)
    # =========================================================
    st.subheader("Analisis Expected Value (EV)")
    
    # Asumsi profit dan loss
    profit = 1000000  # Rp 1.000.000 jika deposit
    loss = -200000    # Rp -200.000 jika gagal
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="background: rgba(46,204,113,0.1); border-radius: 12px; padding: 0.8rem; text-align: center;">
            <div style="font-size: 0.7rem; color: #A8885A;">Profit jika Deposit</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #2ecc71;">Rp {profit:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background: rgba(231,76,60,0.1); border-radius: 12px; padding: 0.8rem; text-align: center;">
            <div style="font-size: 0.7rem; color: #A8885A;">Loss jika Gagal</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #e74c3c;">Rp {loss:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.caption("Rumus EV = P(Yes) × Profit + P(No) × Loss")
    
    # Ambil probabilitas deposit=yes (kolom index 1)
    prob_yes = y_prob[:, 1]
    
    # Hitung EV
    EV = (prob_yes * profit) + ((1 - prob_yes) * loss)
    
    # Simpan ke dataframe
    hasil_ev = pd.DataFrame({
        'Probabilitas_Deposit': prob_yes,
        'Expected_Value': EV
    })
    
    st.write("**Contoh Hasil Expected Value (10 data pertama):**")
    st.dataframe(hasil_ev.head(10), use_container_width=True)
    
    # Statistik EV dalam card
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background: rgba(255,215,0,0.1); border-radius: 12px; padding: 0.6rem; text-align: center;">
            <div style="font-size: 0.6rem; color: #A8885A;">Rata-rata EV</div>
            <div style="font-size: 1rem; font-weight: 700; color: #FFD700;">Rp {EV.mean():,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background: rgba(231,76,60,0.1); border-radius: 12px; padding: 0.6rem; text-align: center;">
            <div style="font-size: 0.6rem; color: #A8885A;">EV Minimum</div>
            <div style="font-size: 1rem; font-weight: 700; color: #e74c3c;">Rp {EV.min():,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="background: rgba(46,204,113,0.1); border-radius: 12px; padding: 0.6rem; text-align: center;">
            <div style="font-size: 0.6rem; color: #A8885A;">EV Maximum</div>
            <div style="font-size: 1rem; font-weight: 700; color: #2ecc71;">Rp {EV.max():,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # =========================================================
    # 8. ANALISIS UTILITY FUNCTION
    # =========================================================
    st.subheader("Analisis Utility Function")
    
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); padding: 0.8rem; border-radius: 10px; margin-bottom: 1rem;">
        <span style="color: #D4C4A8;">Utility berbeda dengan EV. Utility mempertimbangkan preferensi risiko dengan fungsi <span style="color: #FFD700; font-weight: 500;">U(x) = √x</span> (hanya untuk EV positif).</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Fungsi utility: U(x) = sqrt(x) untuk EV positif
    hasil_ev['Utility'] = np.sqrt(np.maximum(hasil_ev['Expected_Value'], 0))
    
    st.write("**Contoh Hasil Utility (10 data pertama):**")
    st.dataframe(hasil_ev.head(10), use_container_width=True)
    
    # =========================================================
    # 9. VISUALISASI EV VS UTILITY (INTERAKTIF)
    # =========================================================
    st.subheader("Visualisasi Perbandingan EV vs Utility")
    
    import plotly.graph_objects as go
    
    fig_compare = go.Figure()
    
    fig_compare.add_trace(go.Scatter(
        y=hasil_ev['Expected_Value'].head(100).values,
        name='Expected Value',
        line=dict(color='steelblue', width=2),
        mode='lines+markers'
    ))
    
    fig_compare.add_trace(go.Scatter(
        y=hasil_ev['Utility'].head(100).values,
        name='Utility',
        line=dict(color='darkorange', width=2),
        mode='lines+markers'
    ))
    
    fig_compare.update_layout(
        title=dict(text='<b>Perbandingan Expected Value dan Utility</b>', font=dict(size=14, color='#FFE4A0'), x=0.5),
        xaxis=dict(title='Data ke-', tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title='Nilai', tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(font=dict(color='#D4C4A8'), bgcolor='rgba(0,0,0,0.5)'),
        height=500
    )
    
    st.plotly_chart(fig_compare, use_container_width=True, config={'displayModeBar': True})
    
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 0.8rem; margin-top: 0.5rem;">
        <span style="color: #F0E6D2; line-height: 1.6; font-size: 0.85rem;">
            Grafik menunjukkan bahwa <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">EV dan Utility memiliki pola yang berbeda</span>. 
            Utility cenderung lebih halus karena menggunakan fungsi akar kuadrat, sehingga <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">memperkecil perbedaan nilai ekstrem</span>. 
            Dua nasabah dengan EV yang sama bisa memiliki nilai utility yang berbeda tergantung preferensi risiko.
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # =========================================================
    # 10. UTILITY FUNCTION BERDASARKAN RISK PREFERENCE
    # =========================================================
    st.subheader("Utility Function Berdasarkan Risk Preference")
    
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); padding: 0.8rem; border-radius: 10px; margin-bottom: 1rem;">
        <span style="color: #D4C4A8;">
            <span style="color: #FFD700; font-weight: 500;">Tiga tipe Risk Preference:</span><br>
            1. <span style="color: #2ecc71;">Risk Averse</span> (menghindari risiko) → fungsi utility cekung (concave) → U = √x<br>
            2. <span style="color: #3498db;">Risk Neutral</span> (netral risiko) → fungsi utility linear → U = x<br>
            3. <span style="color: #e74c3c;">Risk Seeking</span> (menyukai risiko) → fungsi utility cembung (convex) → U = x²
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    x_vals = np.linspace(0, 100, 100)
    
    risk_averse = np.sqrt(x_vals)
    risk_neutral = x_vals
    risk_seeking = x_vals ** 2 / 100
    
    fig_risk = go.Figure()
    
    fig_risk.add_trace(go.Scatter(x=x_vals, y=risk_averse, name='Risk Averse (Concave)', line=dict(color='#2ecc71', width=2)))
    fig_risk.add_trace(go.Scatter(x=x_vals, y=risk_neutral, name='Risk Neutral (Linear)', line=dict(color='#3498db', width=2)))
    fig_risk.add_trace(go.Scatter(x=x_vals, y=risk_seeking, name='Risk Seeking (Convex)', line=dict(color='#e74c3c', width=2)))
    
    fig_risk.update_layout(
        title=dict(text='<b>Utility Function dan Risk Preference</b>', font=dict(size=14, color='#FFE4A0'), x=0.5),
        xaxis=dict(title='Wealth / Profit', tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title='Utility', tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(font=dict(color='#D4C4A8'), bgcolor='rgba(0,0,0,0.5)'),
        height=500
    )
    
    st.plotly_chart(fig_risk, use_container_width=True, config={'displayModeBar': True})
    
    # =========================================================
    # 11. APLIKASI: PREDIKSI UTILITY UNTUK NASABAH BARU
    # =========================================================
    st.subheader("Prediksi Utility untuk Nasabah Baru")
    
    # Ambil satu data contoh untuk prediksi
    sample_data = X_test.iloc[0:1].copy()
    sample_prob = model.predict_proba(sample_data)[0][1]
    sample_ev = (sample_prob * profit) + ((1 - sample_prob) * loss)
    sample_utility = np.sqrt(max(sample_ev, 0))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background: rgba(52,152,219,0.1); border-radius: 12px; padding: 0.6rem; text-align: center;">
            <div style="font-size: 0.6rem; color: #A8885A;">Probabilitas Deposit</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #3498db;">{sample_prob:.2%}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background: rgba(255,215,0,0.1); border-radius: 12px; padding: 0.6rem; text-align: center;">
            <div style="font-size: 0.6rem; color: #A8885A;">Expected Value</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #FFD700;">Rp {sample_ev:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="background: rgba(46,204,113,0.1); border-radius: 12px; padding: 0.6rem; text-align: center;">
            <div style="font-size: 0.6rem; color: #A8885A;">Utility</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #2ecc71;">{sample_utility:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # =========================================================
    # 12. INTERPRETASI HASIL UNTUK DSS (DALAM PARAGRAF DENGAN HIGHLIGHT)
    # =========================================================
    st.subheader("Hasil untuk Decision Support System (DSS)")
    
    ev_tertinggi = EV.max()
    ev_terendah = EV.min()
    ev_rata2 = EV.mean()
    
    st.markdown(f"""
    <div style="background: rgba(0,0,0,0.4); padding: 1.5rem; border-radius: 10px; line-height: 1.8;">
    <p style="color: #F0E6D2; margin-bottom: 1rem;">
        <span style="color: #FFE4A0; font-weight: 700;">1. MODEL LOGISTIC REGRESSION</span><br>
        Model <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">Logistic Regression</span> 
        digunakan untuk menghitung probabilitas deposit nasabah dengan 
        <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">akurasi sebesar {akurasi:.2f}%</span>, 
        yang menunjukkan model cukup baik dalam memprediksi keputusan deposit.
    </p>
        
    <p style="color: #F0E6D2; margin-bottom: 1rem;">
        <span style="color: #FFE4A0; font-weight: 700;">2. EXPECTED VALUE (EV)</span><br>
        Berdasarkan perhitungan, diperoleh <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">rata-rata EV sebesar Rp {ev_rata2:,.0f}</span>, 
        dengan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">nilai tertinggi Rp {ev_tertinggi:,.0f}</span> 
        dan <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #e74c3c;">terendah Rp {ev_terendah:,.0f}</span>.
    </p>
        
    <p style="color: #F0E6D2; margin-bottom: 1rem;">
        <span style="color: #FFE4A0; font-weight: 700;">3. UTILITY & RISK PREFERENCE</span><br>
        Fungsi utility yang digunakan adalah <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">U = √x (Risk Averse)</span>, 
        yang mencerminkan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">preferensi bank yang cenderung menghindari risiko</span>.
    </p>
        
    <p style="color: #F0E6D2; margin-bottom: 1rem;">
        <span style="color: #FFE4A0; font-weight: 700;">4. REKOMENDASI MANAJERIAL</span><br>
        • <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">Prioritaskan nasabah dengan probabilitas deposit > 60%</span><br>
        • <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">Gunakan utility function</span> untuk menyesuaikan dengan toleransi risiko bank<br>
        • <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">Risk Averse → fokus pada EV positif dan probabilitas tinggi</span><br>
        • <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFD700;">Kombinasikan dengan decision under certainty dan risk</span> untuk hasil optimal
    </p>
        
    <p style="color: #F0E6D2; margin-bottom: 0;">
        <span style="color: #FFE4A0; font-weight: 700;">5. KETERBATASAN MODEL</span><br>
        Model ini <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #e74c3c;">mengasumsikan profit dan loss bersifat tetap</span>, 
        <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #e74c3c;">tidak memperhitungkan faktor eksternal</span>, 
        serta <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #e74c3c;">berdasarkan data historis dengan asumsi masa depan sama</span>.
    </p>
    </div>
    """, unsafe_allow_html=True)
    

def analysis_sensitivity(df):
    """Analisis Sensitivity & Simulation - Monte Carlo, Sensitivity Analysis, Scenario Analysis"""
    st.header("Analisis Sensitivity & Simulation")
    
    # =========================================================
    # PENJELASAN MATERI DALAM 3 PARAGRAF DENGAN HIGHLIGHT
    # =========================================================
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); padding: 1.2rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #DAA520;">
        <p style="color: #F0E6D2; line-height: 1.6; margin-bottom: 1rem;">
            <span style="background: linear-gradient(120deg, rgba(218,165,32,0.2) 0%, rgba(218,165,32,0.2) 100%); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 600; color: #FFE4A0;">Sensitivity & Simulation Analysis</span> 
            merupakan metode analisis yang digunakan untuk 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">menguji seberapa sensitif hasil keputusan terhadap perubahan parameter input</span> 
            serta <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">memahami distribusi kemungkinan hasil melalui simulasi probabilistik</span>. 
            Dalam konteks pengambilan keputusan, analisis ini sangat penting karena 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">parameter seperti probabilitas, gain, dan loss jarang bersifat tetap</span> 
            dan dapat berfluktuasi seiring perubahan kondisi pasar.
        </p>
        <p style="color: #F0E6D2; line-height: 1.6; margin-bottom: 1rem;">
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Monte Carlo Simulation</span> 
            merupakan teknik simulasi probabilistik yang <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">membangkitkan ribuan skenario acak</span> 
            berdasarkan distribusi probabilitas dari parameter input untuk 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">memperoleh distribusi hasil yang mungkin terjadi</span>. 
            Sementara itu, <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Sensitivity Analysis</span> 
            bertujuan untuk <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">mengidentifikasi parameter mana yang paling berpengaruh terhadap hasil keputusan</span>, 
            sehingga manajemen dapat fokus pada parameter kritis yang perlu dimonitor secara ketat.
        </p>
        <p style="color: #F0E6D2; line-height: 1.6;">
            Keunggulan pendekatan ini adalah <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">mampu mengkuantifikasi risiko dan ketidakpastian</span> 
            serta <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">memberikan gambaran tentang rentang hasil yang mungkin terjadi</span>, 
            namun kelemahannya adalah <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #e74c3c;">membutuhkan komputasi yang intensif untuk skenario kompleks</span>. 
            Pendekatan ini paling cocok digunakan ketika 
            <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">parameter input memiliki tingkat ketidakpastian yang tinggi</span> 
            dan <span style="background: rgba(218,165,32,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">diperlukan pemahaman tentang distribusi hasil</span> 
            sebelum mengambil keputusan final.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # =========================================================
    # KONSEP DAN PENDEKATAN
    # =========================================================
    st.markdown("""
    <div style="background: rgba(0,0,0,0.4); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
        <b style="color: #FFE4A0; font-size: 1.05rem;">📌 Konsep Sensitivity & Simulation:</b><br>
        <span style="color: #D4C4A8;">1. <span style="color: #FFD700; font-weight: 500;">Monte Carlo Simulation</span>: Simulasi probabilistik untuk memahami distribusi hasil<br>
        2. <span style="color: #FFD700; font-weight: 500;">Sensitivity Analysis</span>: Menguji bagaimana perubahan parameter mempengaruhi hasil<br>
        3. <span style="color: #FFD700; font-weight: 500;">Scenario Analysis</span>: Mengevaluasi skenario ekstrem (optimis vs pesimis)<br>
        4. <span style="color: #FFD700; font-weight: 500;">Robustness Check</span>: Menguji ketahanan keputusan terhadap berbagai kondisi</span><br><br>
        <b style="color: #FFE4A0; font-size: 1.05rem;">📌 Pendekatan ini cocok untuk:</b><br>
        <span style="color: #D4C4A8;">• <span style="color: #FFD700;">Situasi dengan ketidakpastian parameter</span> yang tinggi<br>
        • <span style="color: #FFD700;">Evaluasi risiko</span> sebelum implementasi strategi<br>
        • <span style="color: #FFD700;">Identifikasi parameter kritis</span> yang perlu dimonitor<br>
        • <span style="color: #FFD700;">Pengujian ketahanan</span> keputusan terhadap berbagai skenario</span>
    </div>
    """, unsafe_allow_html=True)
    
    # ============================================
    # 1. INFORMASI DASAR (DIHAPUS KARENA SUDAH ADA DI DASHBOARD UTAMA)
    # ============================================
    # Langsung ke konten utama tanpa informasi dataset
    
    # Probabilitas dasar
    if 'deposit' in df.columns:
        p_yes = (df['deposit'] == 'yes').mean()
        p_no = 1 - p_yes
    else:
        p_yes = 0.5
        p_no = 0.5
    
    # Asumsi payoff dasar
    GAIN_YES = 100
    LOSS_NO = -20
    
    # ============================================
    # 2. MONTE CARLO SIMULATION - PROBABILITAS DEPOSIT
    # ============================================
    st.subheader("Monte Carlo Simulation - Probabilitas Deposit")
    
    n_sim = st.slider("Jumlah Simulasi Monte Carlo", 1000, 50000, 10000, step=1000)
    
    def monte_carlo_deposit(n_simulations, n_customers):
        """Simulasi Monte Carlo untuk probabilitas deposit"""
        results = []
        for _ in range(n_simulations):
            deposits = np.random.binomial(1, p_yes, n_customers)
            deposit_rate = deposits.sum() / n_customers
            results.append(deposit_rate)
        return np.array(results)
    
    sim_results = monte_carlo_deposit(n_sim, len(df))
    
    # Card untuk statistik simulasi
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(52,152,219,0.1) 0%, rgba(52,152,219,0.03) 100%); border-radius: 14px; padding: 0.8rem; text-align: center; border: 1px solid rgba(52,152,219,0.3);">
            <div style="font-size: 0.65rem; color: #A8885A;">Rata-rata Deposit Rate</div>
            <div style="font-size: 1.3rem; font-weight: 700; color: #3498db;">{sim_results.mean():.2%}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(231,76,60,0.1) 0%, rgba(231,76,60,0.03) 100%); border-radius: 14px; padding: 0.8rem; text-align: center; border: 1px solid rgba(231,76,60,0.3);">
            <div style="font-size: 0.65rem; color: #A8885A;">Standar Deviasi</div>
            <div style="font-size: 1.3rem; font-weight: 700; color: #e74c3c;">{sim_results.std():.2%}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(46,204,113,0.1) 0%, rgba(46,204,113,0.03) 100%); border-radius: 14px; padding: 0.8rem; text-align: center; border: 1px solid rgba(46,204,113,0.3);">
            <div style="font-size: 0.65rem; color: #A8885A;">CI 95%</div>
            <div style="font-size: 1rem; font-weight: 700; color: #2ecc71;">[{np.percentile(sim_results, 2.5):.2%}, {np.percentile(sim_results, 97.5):.2%}]</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Visualisasi distribusi hasil simulasi dengan plotly interaktif
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    
    fig_sim = make_subplots(rows=1, cols=2, subplot_titles=('Distribusi Deposit Rate', 'Cumulative Distribution Function'))
    
    # Histogram
    fig_sim.add_trace(
        go.Histogram(x=sim_results, nbinsx=50, name='Distribusi', marker_color='steelblue', opacity=0.7),
        row=1, col=1
    )
    fig_sim.add_vline(x=p_yes, line=dict(color='red', width=2, dash='dash'), annotation_text=f'Actual: {p_yes:.2%}', row=1, col=1)
    fig_sim.add_vline(x=sim_results.mean(), line=dict(color='green', width=2), annotation_text=f'Mean: {sim_results.mean():.2%}', row=1, col=1)
    
    # Cumulative histogram
    fig_sim.add_trace(
        go.Histogram(x=sim_results, nbinsx=50, cumulative_enabled=True, name='CDF', marker_color='coral', opacity=0.7),
        row=1, col=2
    )
    fig_sim.add_vline(x=p_yes, line=dict(color='red', width=2, dash='dash'), annotation_text=f'Actual: {p_yes:.2%}', row=1, col=2)
    
    fig_sim.update_layout(
        title=dict(text=f'<b>Monte Carlo Simulation - Distribusi Deposit Rate</b><br>(n_sim={n_sim:,})', font=dict(size=14, color='#FFE4A0'), x=0.5),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        height=500,
        bargap=0.05
    )
    fig_sim.update_xaxes(title_text='Deposit Rate', tickformat='.0%', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#D4C4A8'))
    fig_sim.update_yaxes(title_text='Density', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#D4C4A8'))
    
    st.plotly_chart(fig_sim, use_container_width=True, config={'displayModeBar': True})
    
    # Interpretasi Monte Carlo Simulation - Probabilitas Deposit
    st.markdown(f"""
    <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 0.8rem; margin-top: 0.8rem;">
        <span style="color: #F0E6D2; line-height: 1.6; font-size: 0.85rem;">
            Hasil simulasi Monte Carlo menunjukkan bahwa 
            <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">distribusi deposit rate mengikuti pola normal</span> 
            dengan rata-rata <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">{sim_results.mean():.2%}</span> 
            yang mendekati nilai aktual <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">{p_yes:.2%}</span>. 
            Standar deviasi sebesar <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">{sim_results.std():.2%}</span> 
            mengindikasikan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">variabilitas hasil yang relatif rendah</span>, 
            sehingga keputusan berdasarkan data historis cukup dapat diandalkan.
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ============================================
    # 3. MONTE CARLO SIMULATION - EXPECTED VALUE
    # ============================================
    st.subheader("Monte Carlo Simulation - Expected Value (EV)")
    
    def monte_carlo_ev(n_simulations, n_customers, gain=100, loss=-20):
        """Simulasi Monte Carlo untuk Expected Value"""
        ev_results = []
        for _ in range(n_simulations):
            deposits = np.random.binomial(1, p_yes, n_customers)
            n_yes = deposits.sum()
            n_no = n_customers - n_yes
            total_profit = (n_yes * gain) + (n_no * loss)
            ev_per_customer = total_profit / n_customers
            ev_results.append(ev_per_customer)
        return np.array(ev_results)
    
    ev_sim_results = monte_carlo_ev(n_sim, len(df), GAIN_YES, LOSS_NO)
    ev_deterministic = (p_yes * GAIN_YES) + (p_no * LOSS_NO)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(52,152,219,0.1) 0%, rgba(52,152,219,0.03) 100%); border-radius: 14px; padding: 0.8rem; text-align: center;">
            <div style="font-size: 0.65rem; color: #A8885A;">EV Deterministik</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #3498db;">{ev_deterministic:.2f} unit</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(255,215,0,0.1) 0%, rgba(255,215,0,0.03) 100%); border-radius: 14px; padding: 0.8rem; text-align: center;">
            <div style="font-size: 0.65rem; color: #A8885A;">Rata-rata EV Simulasi</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #FFD700;">{ev_sim_results.mean():.2f} unit</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(46,204,113,0.1) 0%, rgba(46,204,113,0.03) 100%); border-radius: 14px; padding: 0.8rem; text-align: center;">
            <div style="font-size: 0.65rem; color: #A8885A;">Prob EV Positif</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #2ecc71;">{(ev_sim_results > 0).mean():.2%}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Visualisasi distribusi EV dengan plotly
    fig_ev = make_subplots(rows=1, cols=2, subplot_titles=('Distribusi Expected Value', 'Boxplot Distribusi EV'))
    
    # Histogram EV
    fig_ev.add_trace(
        go.Histogram(x=ev_sim_results, nbinsx=50, name='EV Distribution', marker_color='steelblue', opacity=0.7),
        row=1, col=1
    )
    fig_ev.add_vline(x=ev_deterministic, line=dict(color='red', width=2, dash='dash'), annotation_text=f'Deterministic: {ev_deterministic:.2f}', row=1, col=1)
    fig_ev.add_vline(x=0, line=dict(color='black', width=1), annotation_text='EV = 0', row=1, col=1)
    
    # Boxplot EV
    fig_ev.add_trace(
        go.Box(y=ev_sim_results, name='EV', marker_color='lightblue', boxmean='sd'),
        row=1, col=2
    )
    fig_ev.add_hline(y=ev_deterministic, line=dict(color='red', width=2, dash='dash'), row=1, col=2)
    fig_ev.add_hline(y=0, line=dict(color='black', width=1), row=1, col=2)
    
    fig_ev.update_layout(
        title=dict(text='<b>Monte Carlo Simulation - Expected Value Distribution</b>', font=dict(size=14, color='#FFE4A0'), x=0.5),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        height=500,
        bargap=0.05
    )
    fig_ev.update_xaxes(title_text='Expected Value', tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)')
    fig_ev.update_yaxes(title_text='Density', tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)')
    
    st.plotly_chart(fig_ev, use_container_width=True, config={'displayModeBar': True})
    
    # Interpretasi Monte Carlo Simulation - Expected Value
    st.markdown(f"""
    <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 0.8rem; margin-top: 0.8rem;">
        <span style="color: #F0E6D2; line-height: 1.6; font-size: 0.85rem;">
            Simulasi EV menunjukkan bahwa 
            <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">rata-rata EV simulasi ({ev_sim_results.mean():.2f} unit)</span> 
            sangat mendekati <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">EV deterministik ({ev_deterministic:.2f} unit)</span>, 
            mengonfirmasi keakuratan perhitungan. 
            <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Probabilitas EV positif sebesar {(ev_sim_results > 0).mean():.2%}</span> 
            memberikan keyakinan bahwa strategi ini <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">cenderung menguntungkan dalam jangka panjang</span>.
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ============================================
    # 4. SENSITIVITY ANALYSIS - PAYOFF PARAMETERS (INTERAKTIF)
    # ============================================
    st.subheader("Sensitivity Analysis - Variasi Payoff")
    
    # Variasi parameter
    gain_range = np.arange(50, 201, 25)
    loss_range = np.arange(-100, -10, 10)
    
    # Matriks sensitivitas
    sensitivity_matrix = np.zeros((len(gain_range), len(loss_range)))
    
    for i, gain in enumerate(gain_range):
        for j, loss in enumerate(loss_range):
            ev = (p_yes * gain) + (p_no * loss)
            sensitivity_matrix[i, j] = ev
    
    # Heatmap interaktif dengan plotly
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=sensitivity_matrix,
        x=loss_range,
        y=gain_range,
        colorscale='RdYlGn',
        zmid=0,
        text=sensitivity_matrix.round(0),
        texttemplate='%{text}',
        textfont={"size": 10, "color": "white"},
        hoverongaps=False,
        hovertemplate='Gain: %{y}<br>Loss: %{x}<br>EV: %{z:.0f}<extra></extra>'
    ))
    
    fig_heatmap.update_layout(
        title=dict(text='<b>Sensitivity Matrix: EV per Customer</b>', font=dict(size=14, color='#FFE4A0'), x=0.5),
        xaxis=dict(title='Loss (jika tidak deposit)', tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title='Gain (jika deposit)', tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=500
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True, config={'displayModeBar': True})
    
    # Interpretasi Sensitivity Analysis - Variasi Payoff
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 0.8rem; margin-top: 0.8rem;">
        <span style="color: #F0E6D2; line-height: 1.6; font-size: 0.85rem;">
            Heatmap di atas menunjukkan bahwa 
            <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">EV sangat sensitif terhadap perubahan Gain dan Loss</span>. 
            Warna <span style="background: rgba(46,204,113,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #2ecc71;">hijau (EV positif)</span> mendominasi pada area dengan Gain tinggi dan Loss rendah, 
            sedangkan <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #e74c3c;">merah (EV negatif)</span> muncul ketika Loss terlalu besar. 
            <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Garis batas EV=0</span> menunjukkan kombinasi Gain dan Loss yang membuat keputusan menjadi tidak menguntungkan.
        </span>
    </div>
    """, unsafe_allow_html=True)


    # ============================================
    # 5. SENSITIVITY ANALYSIS - PROBABILITAS (INTERAKTIF)
    # ============================================
    st.subheader("Sensitivity Analysis - Variasi Probabilitas")
    
    # Variasi probabilitas
    p_range = np.arange(0.1, 0.9, 0.05)
    ev_by_prob = [(p * GAIN_YES) + ((1-p) * LOSS_NO) for p in p_range]
    
    # Break-even point
    be_threshold = abs(LOSS_NO) / (GAIN_YES - LOSS_NO)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="background: rgba(52,152,219,0.1); border-radius: 12px; padding: 0.8rem; text-align: center;">
            <div style="font-size: 0.65rem; color: #A8885A;">Break-even P(yes)</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #3498db;">{be_threshold:.2%}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background: rgba(46,204,113,0.1); border-radius: 12px; padding: 0.8rem; text-align: center;">
            <div style="font-size: 0.65rem; color: #A8885A;">Margin of Safety</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #2ecc71;">{p_yes - be_threshold:.2%}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Grafik EV vs Probability dengan plotly
    fig_prob = go.Figure()
    
    fig_prob.add_trace(go.Scatter(
        x=p_range,
        y=ev_by_prob,
        mode='lines+markers',
        name='EV',
        line=dict(color='blue', width=2),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(0,100,255,0.2)',
        hovertemplate='P(yes): %{x:.1%}<br>EV: %{y:.2f}<extra></extra>'
    ))
    
    fig_prob.add_hline(y=0, line=dict(color='black', width=1), annotation_text='EV = 0')
    fig_prob.add_vline(x=be_threshold, line=dict(color='red', width=2, dash='dash'), annotation_text=f'Break-even: {be_threshold:.2%}')
    fig_prob.add_vline(x=p_yes, line=dict(color='green', width=2, dash='dash'), annotation_text=f'Actual: {p_yes:.2%}')
    
    fig_prob.update_layout(
        title=dict(text='<b>Sensitivity: EV vs Probabilitas Deposit</b>', font=dict(size=14, color='#FFE4A0'), x=0.5),
        xaxis=dict(title='Probabilitas Deposit (P)', tickformat='.0%', tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title='Expected Value', tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=450
    )
    
    st.plotly_chart(fig_prob, use_container_width=True, config={'displayModeBar': True})
    
    # Sensitivity bar
    sensitivity = GAIN_YES - LOSS_NO
    fig_sens = go.Figure(go.Bar(
        x=['Sensitivity (dEV/dP)'],
        y=[sensitivity],
        text=[f'{sensitivity:.0f}'],
        textposition='auto',
        marker_color='steelblue'
    ))
    fig_sens.update_layout(
        title=dict(text=f'<b>Sensitivitas EV terhadap Perubahan Probabilitas</b><br>(dEV/dP = {sensitivity:.0f})', font=dict(size=12, color='#D4C4A8'), x=0.5),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=300,
        showlegend=False
    )
    fig_sens.update_yaxes(title_text='Perubahan EV per 1% perubahan P', tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)')
    
    st.plotly_chart(fig_sens, use_container_width=True, config={'displayModeBar': True})
    
    # Interpretasi Sensitivity Analysis - Variasi Probabilitas
    st.markdown(f"""
    <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 0.8rem; margin-top: 0.8rem;">
        <span style="color: #F0E6D2; line-height: 1.6; font-size: 0.85rem;">
            Grafik EV vs Probabilitas menunjukkan bahwa 
            <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">EV meningkat secara linear seiring kenaikan probabilitas deposit</span>. 
            <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Break-even point terjadi pada P(yes) = {be_threshold:.2%}</span>, 
            artinya jika probabilitas deposit turun di bawah level ini, strategi akan merugi. 
            <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Nilai sensitivity dEV/dP = {sensitivity:.0f}</span> 
            berarti setiap kenaikan 1% probabilitas deposit akan meningkatkan EV sebesar {sensitivity/100:.1f} unit per nasabah.
        </span>
    </div>
    """, unsafe_allow_html=True)


    # ============================================
    # 6. SENSITIVITY ANALYSIS - SEGMENTASI (JOB) DENGAN PLOTLY
    # ============================================
    if 'job' in df.columns and 'deposit' in df.columns:
        st.subheader("Sensitivity Analysis - Per Segment (Job)")
        
        # Hitung P(yes) per job
        job_probs = df.groupby('job')['deposit'].apply(lambda x: (x == 'yes').mean())
        
        # Hitung EV untuk berbagai skenario loss
        loss_scenarios = [-20, -50, -80, -100]
        scenario_labels = ['Optimis (Loss=20)', 'Moderat (Loss=50)', 'Pesimis (Loss=80)', 'Kritis (Loss=100)']
        
        fig_job = go.Figure()
        
        for i, (loss, label) in enumerate(zip(loss_scenarios, scenario_labels)):
            ev_values = [(p * GAIN_YES) + ((1-p) * loss) for p in job_probs.values]
            colors = ['#2ecc71' if ev > 0 else '#e74c3c' for ev in ev_values]
            
            fig_job.add_trace(go.Bar(
                x=job_probs.index,
                y=ev_values,
                name=label,
                marker_color=colors,
                text=ev_values,
                textposition='outside',
                texttemplate='%{text:.0f}',
                hovertemplate='Job: %{x}<br>EV: %{y:.0f}<extra></extra>'
            ))
        
        fig_job.update_layout(
            title=dict(text='<b>Sensitivity Analysis per Job: Variasi Loss</b>', font=dict(size=14, color='#FFE4A0'), x=0.5),
            xaxis=dict(title='Job', tickangle=45, tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title='Expected Value', tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            barmode='group',
            height=500,
            legend=dict(font=dict(color='#D4C4A8'), bgcolor='rgba(0,0,0,0.5)')
        )
        
        st.plotly_chart(fig_job, use_container_width=True, config={'displayModeBar': True})
        
        # Tabel ringkasan per job dalam expander
        with st.expander("Tabel Ringkasan Sensitivity per Job"):
            summary_data = []
            for job in job_probs.index:
                p = job_probs[job]
                ev_20 = (p * 100) + ((1-p) * -20)
                ev_50 = (p * 100) + ((1-p) * -50)
                ev_80 = (p * 100) + ((1-p) * -80)
                ev_100 = (p * 100) + ((1-p) * -100)
                
                summary_data.append({
                    'Job': job,
                    'P(yes)': f"{p:.2%}",
                    'EV (Loss=20)': f"{ev_20:.1f}",
                    'EV (Loss=50)': f"{ev_50:.1f}",
                    'EV (Loss=80)': f"{ev_80:.1f}",
                    'EV (Loss=100)': f"{ev_100:.1f}"
                })
            
            st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)
    

    # Interpretasi Sensitivity Analysis - Per Segment Job
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 0.8rem; margin-top: 0.8rem;">
        <span style="color: #F0E6D2; line-height: 1.6; font-size: 0.85rem;">
            Grafik di atas menunjukkan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">bagaimana perubahan nilai loss mempengaruhi EV setiap segmen pekerjaan</span>. 
            Semakin besar loss (semakin negatif), semakin banyak segmen yang berubah warna menjadi merah (rugi). 
            <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Segmen 'retired' dan 'student' cenderung lebih tahan terhadap peningkatan loss</span>, 
            sementara segmen 'blue-collar' lebih sensitif dan cepat berubah menjadi negatif saat loss meningkat.
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ============================================
    # 7. TORNADO CHART (SENSITIVITY RANKING) DENGAN PLOTLY
    # ============================================
    st.subheader("Tornado Chart - Ranking Sensitivitas")
    
    # Parameter yang divariasikan
    parameters = {
        'Gain (Deposit)': GAIN_YES,
        'Loss (No Deposit)': abs(LOSS_NO),
        'Probabilitas (P)': p_yes,
        'Jumlah Nasabah': len(df)
    }
    
    base_ev = (p_yes * GAIN_YES) + (p_no * LOSS_NO)
    sensitivity_results = {}
    
    for param_name, base_value in parameters.items():
        if param_name == 'Gain (Deposit)':
            low_ev = (p_yes * (base_value * 0.8)) + (p_no * LOSS_NO)
            high_ev = (p_yes * (base_value * 1.2)) + (p_no * LOSS_NO)
        elif param_name == 'Loss (No Deposit)':
            low_ev = (p_yes * GAIN_YES) + (p_no * (abs(base_value) * 0.8 * -1))
            high_ev = (p_yes * GAIN_YES) + (p_no * (abs(base_value) * 1.2 * -1))
        elif param_name == 'Probabilitas (P)':
            low_ev = ((base_value * 0.8) * GAIN_YES) + ((1 - base_value * 0.8) * LOSS_NO)
            high_ev = ((base_value * 1.2) * GAIN_YES) + ((1 - base_value * 1.2) * LOSS_NO)
        else:
            low_ev = base_ev * (base_value * 0.8) / base_value
            high_ev = base_ev * (base_value * 1.2) / base_value
        
        sensitivity_results[param_name] = {
            'low': low_ev,
            'high': high_ev,
            'range': abs(high_ev - low_ev)
        }
    
    # Sort by range
    sorted_params = sorted(sensitivity_results.items(), key=lambda x: x[1]['range'], reverse=True)
    
    fig_tornado = go.Figure()
    
    for i, (param_name, values) in enumerate(sorted_params):
        fig_tornado.add_trace(go.Bar(
            y=[param_name],
            x=[values['high'] - values['low']],
            orientation='h',
            name=param_name,
            marker_color='steelblue',
            hovertemplate=f'{param_name}<br>Range: %{{x:.0f}}<extra></extra>',
            text=[f'{values["low"]:.0f} - {values["high"]:.0f}'],
            textposition='outside'
        ))
    
    fig_tornado.update_layout(
        title=dict(text='<b>Tornado Chart: Sensitivitas Parameter terhadap EV</b>', font=dict(size=14, color='#FFE4A0'), x=0.5),
        xaxis=dict(title='Expected Value', tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title='Parameter', tickfont=dict(color='#D4C4A8')),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        showlegend=False,
        barmode='stack'
    )
    
    st.plotly_chart(fig_tornado, use_container_width=True, config={'displayModeBar': True})
    
    # Interpretasi Tornado Chart
    sorted_params_names = [p[0] for p in sorted_params]
    most_sensitive = sorted_params_names[0] if sorted_params_names else "Gain"
    st.markdown(f"""
    <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 0.8rem; margin-top: 0.8rem;">
        <span style="color: #F0E6D2; line-height: 1.6; font-size: 0.85rem;"> 
            Tornado chart di atas meranking parameter berdasarkan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">pengaruhnya terhadap EV</span>. 
            Parameter <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">{most_sensitive}</span> 
            memiliki rentang pengaruh terlebar, menjadikannya <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">parameter paling kritis yang perlu dimonitor</span>. 
            Semakin panjang batang suatu parameter, semakin besar pengaruh perubahan parameter tersebut terhadap hasil keputusan. 
            Manajemen sebaiknya <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">fokus pada pengendalian parameter dengan batang terpanjang</span> 
            untuk memastikan keputusan tetap optimal.
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ============================================
    # 8. SCENARIO ANALYSIS
    # ============================================
    st.subheader("Scenario Analysis - Skenario Ekstrem")
    
    # Definisikan skenario
    scenarios = {
        'Pessimistic': {'gain': 50, 'loss': -80, 'p': p_yes * 0.7, 'color': '#e74c3c'},
        'Moderate': {'gain': 100, 'loss': -50, 'p': p_yes, 'color': '#f39c12'},
        'Optimistic': {'gain': 150, 'loss': -20, 'p': p_yes * 1.3, 'color': '#3498db'},
        'Best Case': {'gain': 200, 'loss': -10, 'p': min(p_yes * 1.5, 0.95), 'color': '#2ecc71'},
        'Worst Case': {'gain': 30, 'loss': -100, 'p': p_yes * 0.5, 'color': '#e74c3c'}
    }
    
    scenario_results = []
    for name, params in scenarios.items():
        ev = (params['p'] * params['gain']) + ((1 - params['p']) * params['loss'])
        scenario_results.append({
            'Scenario': name,
            'EV': ev,
            'P(yes)': params['p'],
            'Gain': params['gain'],
            'Loss': params['loss'],
            'color': params['color']
        })
    
    df_scenarios = pd.DataFrame(scenario_results)
    
    # Bar chart dengan plotly
    fig_scenario = go.Figure()
    
    colors = ['#e74c3c' if ev < 0 else '#2ecc71' for ev in df_scenarios['EV']]
    fig_scenario.add_trace(go.Bar(
        x=df_scenarios['Scenario'],
        y=df_scenarios['EV'],
        marker_color=colors,
        text=df_scenarios['EV'].round(0),
        textposition='outside',
        hovertemplate='Scenario: %{x}<br>EV: %{y:.0f}<extra></extra>'
    ))
    
    fig_scenario.add_hline(y=0, line=dict(color='black', width=1))
    
    fig_scenario.update_layout(
        title=dict(text='<b>EV Berbagai Skenario</b>', font=dict(size=14, color='#FFE4A0'), x=0.5),
        xaxis=dict(title='Scenario', tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title='Expected Value', tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=450
    )
    
    st.plotly_chart(fig_scenario, use_container_width=True, config={'displayModeBar': True})
    
    # Tabel detail skenario
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); border-radius: 12px; padding: 0.8rem; margin: 1rem 0;">
        <span style="font-size: 0.8rem; font-weight: 600; color: #FFD700;">📋 Detail Skenario</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.dataframe(
        df_scenarios[['Scenario', 'EV', 'P(yes)', 'Gain', 'Loss']].round(2),
        use_container_width=True,
        hide_index=True
    )
    
        # Interpretasi Scenario Analysis
    best_scenario = df_scenarios.loc[df_scenarios['EV'].idxmax(), 'Scenario']
    worst_scenario = df_scenarios.loc[df_scenarios['EV'].idxmin(), 'Scenario']
    best_ev = df_scenarios['EV'].max()
    worst_ev = df_scenarios['EV'].min()
    
    st.markdown(f"""
    <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 0.8rem; margin-top: 0.8rem;">
        <span style="color: #F0E6D2; line-height: 1.6; font-size: 0.85rem;">
            Analisis skenario menunjukkan rentang hasil yang mungkin terjadi dari 
            <span style="background: rgba(46,204,113,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #2ecc71;">kondisi terbaik (Best Case)</span> 
            hingga <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #e74c3c;">kondisi terburuk (Worst Case)</span>. 
            Pada skenario <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">{best_scenario}</span>, 
            EV mencapai <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">{best_ev:.0f} unit</span>, 
            sementara pada skenario <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #e74c3c;">{worst_scenario}</span> 
            EV turun menjadi <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #e74c3c;">{worst_ev:.0f} unit</span>. 
            Perbedaan ini menunjukkan bahwa <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">hasil keputusan sangat dipengaruhi oleh kondisi pasar</span>, 
            sehingga perlu disiapkan strategi kontingensi untuk menghadapi skenario pesimis.
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ============================================
    # 9. ROBUSTNESS CHECK
    # ============================================
    st.subheader("Robustness Check - Ketahanan Keputusan")
    
    # Uji robustness dengan berbagai skenario probabilitas
    p_test = np.arange(0.3, 0.7, 0.05)
    gain_test = [80, 100, 120]
    loss_test = [-30, -20, -10]
    
    robustness_results = []
    
    for p in p_test:
        for gain in gain_test:
            for loss in loss_test:
                ev = (p * gain) + ((1-p) * loss)
                robustness_results.append({
                    'P(yes)': p,
                    'Gain': gain,
                    'Loss': loss,
                    'EV': ev,
                    'Decision': 'Offer' if ev > 0 else 'Not Offer'
                })
    
    df_robust = pd.DataFrame(robustness_results)
    consistent_decisions = df_robust.groupby(['Gain', 'Loss'])['Decision'].apply(lambda x: (x == 'Offer').all() or (x == 'Not Offer').all())
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background: rgba(52,152,219,0.1); border-radius: 12px; padding: 0.8rem; text-align: center;">
            <div style="font-size: 0.65rem; color: #A8885A;">Total Skenario Diuji</div>
            <div style="font-size: 1.3rem; font-weight: 700; color: #3498db;">{len(df_robust):,}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background: rgba(46,204,113,0.1); border-radius: 12px; padding: 0.8rem; text-align: center;">
            <div style="font-size: 0.65rem; color: #A8885A;">EV > 0</div>
            <div style="font-size: 1.3rem; font-weight: 700; color: #2ecc71;">{(df_robust['EV'] > 0).sum()} ({(df_robust['EV'] > 0).mean():.1%})</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="background: rgba(255,215,0,0.1); border-radius: 12px; padding: 0.8rem; text-align: center;">
            <div style="font-size: 0.65rem; color: #A8885A;">Keputusan Konsisten</div>
            <div style="font-size: 1.3rem; font-weight: 700; color: #FFD700;">{consistent_decisions.sum()} dari {len(consistent_decisions)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Visualisasi robustness dengan plotly
    fig_robust = make_subplots(rows=1, cols=2, subplot_titles=('Robustness Matrix', 'Decision Boundary'))
    
    # Heatmap EV
    heatmap_data = df_robust.pivot_table(index='Gain', columns='Loss', values='EV')
    fig_robust.add_trace(
        go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='RdYlGn',
            zmid=0,
            text=heatmap_data.values.round(0),
            texttemplate='%{text}',
            hovertemplate='Gain: %{y}<br>Loss: %{x}<br>EV: %{z:.0f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Decision boundary
    for gain in gain_test:
        ev_line = [(p * gain) + ((1-p) * -20) for p in p_test]
        fig_robust.add_trace(
            go.Scatter(x=p_test, y=ev_line, mode='lines+markers', name=f'Gain={gain}'),
            row=1, col=2
        )
    fig_robust.add_hline(y=0, line=dict(color='black', width=1, dash='dash'), row=1, col=2)
    
    fig_robust.update_layout(
        title=dict(text='<b>Robustness Check Analysis</b>', font=dict(size=14, color='#FFE4A0'), x=0.5),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=500,
        showlegend=True,
        legend=dict(font=dict(color='#D4C4A8'), bgcolor='rgba(0,0,0,0.5)')
    )
    fig_robust.update_xaxes(title_text='Loss', tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)', row=1, col=1)
    fig_robust.update_yaxes(title_text='Gain', tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)', row=1, col=1)
    fig_robust.update_xaxes(title_text='Probabilitas Deposit (P)', tickformat='.0%', tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)', row=1, col=2)
    fig_robust.update_yaxes(title_text='Expected Value', tickfont=dict(color='#D4C4A8'), gridcolor='rgba(255,255,255,0.1)', row=1, col=2)
    
    st.plotly_chart(fig_robust, use_container_width=True, config={'displayModeBar': True})
    
    # ============================================
    # 10. KESIMPULAN ANALISIS (DALAM PARAGRAF DENGAN HIGHLIGHT)
    # ============================================
    st.subheader("Kesimpulan Simulation & Sensitivity Analysis")
    
    st.markdown(f"""
    <div style="background: rgba(0,0,0,0.4); padding: 1.5rem; border-radius: 10px; line-height: 1.8;">
    <p style="color: #F0E6D2; margin-bottom: 1rem;">
        <span style="color: #FFE4A0; font-weight: 700;">Tujuan 1: Konsep simulasi</span><br>
        <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Monte Carlo Simulation</span> 
        dengan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">{n_sim:,} iterasi</span> berhasil dijalankan. 
        Distribusi deposit rate memiliki <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">rata-rata {sim_results.mean():.2%} dengan standar deviasi {sim_results.std():.2%}</span>. 
        Distribusi EV menunjukkan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">rata-rata {ev_sim_results.mean():.2f} unit</span> 
        dengan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">interval kepercayaan 95% [{np.percentile(ev_sim_results, 2.5):.2f}, {np.percentile(ev_sim_results, 97.5):.2f}]</span> 
        dan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">probabilitas EV positif sebesar {(ev_sim_results > 0).mean():.2%}</span>.
    </p>
        
    <p style="color: #F0E6D2; margin-bottom: 1rem;">
        <span style="color: #FFE4A0; font-weight: 700;">Tujuan 2: Menguji berbagai skenario</span><br>
        Skenario <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Best Case</span> 
        menghasilkan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">EV tertinggi sebesar {df_scenarios[df_scenarios['Scenario'] == 'Best Case']['EV'].values[0]:.0f} unit</span>, 
        sementara skenario <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #e74c3c;">Worst Case</span> 
        menunjukkan <span style="background: rgba(231,76,60,0.2); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #e74c3c;">EV terendah sebesar {df_scenarios[df_scenarios['Scenario'] == 'Worst Case']['EV'].values[0]:.0f} unit</span>. 
        <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Break-even P(yes) = {be_threshold:.2%}</span> 
        dengan <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">margin of safety {p_yes - be_threshold:.2%}</span>.
    </p>
        
    <p style="color: #F0E6D2; margin-bottom: 0;">
        <span style="color: #FFE4A0; font-weight: 700;">Tujuan 3: Menganalisis robustness keputusan</span><br>
        Parameter paling sensitif adalah <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">Gain dan Loss</span>, 
        yang memiliki rentang pengaruh terbesar terhadap EV. Rekomendasi "Offer" 
        <span style="background: rgba(255,215,0,0.25); padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; color: #FFD700;">robust pada {consistent_decisions.mean() * 100:.1f}% skenario yang diuji</span>, 
        menunjukkan bahwa strategi ini cukup tahan terhadap berbagai kondisi pasar.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
   