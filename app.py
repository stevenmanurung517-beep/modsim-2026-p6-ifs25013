import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.markdown("""
<style>

/* Background utama */
.stApp {
    background: linear-gradient(135deg, #eef2ff, #f0fdf4);
}

/* Judul */
h1 {
    font-weight: 800 !important;
    letter-spacing: 1px;
}

/* Card style */
.block-container {
    padding-top: 2rem;
}

/* Metric box */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #ffffff, #f1f5f9);
    border: 1px solid #e2e8f0;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
}

/* Hover effect */
[data-testid="metric-container"]:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0,0,0,0.15);
}

/* Tombol */
.stButton>button {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    color: white;
    border-radius: 12px;
    font-weight: bold;
    padding: 10px 20px;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    background: linear-gradient(135deg, #16a34a, #15803d);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e293b, #0f172a);
    color: white;
}

/* Text sidebar */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Slider */
.stSlider > div > div {
    color: #22c55e !important;
}

/* Dataframe */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
}

/* Success box */
.stAlert {
    border-radius: 12px;
}

/* Divider */
hr {
    border: none;
    height: 2px;
    background: linear-gradient(to right, #22c55e, #3b82f6);
}

</style>
""", unsafe_allow_html=True)
# ================================
# CONFIG HALAMAN
# ================================
st.set_page_config(
    page_title="Simulasi Antrian Mahasiswa",
    page_icon="📊",
    layout="wide"
)

# ================================
# HEADER
# ================================
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>
    📊 Simulasi Pembagian Lembar Jawaban
    </h1>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center'>
Simulasi sistem antrian <b>single server (FIFO)</b> untuk pembagian lembar jawaban ujian
</div>
""", unsafe_allow_html=True)

st.divider()

# ================================
# FUNGSI SIMULASI
# ================================
def simulasi_antrian(jumlah_mahasiswa, min_waktu=1, max_waktu=3, seed=None):
    
    if seed is not None:
        np.random.seed(seed)

    # Generate waktu pelayanan
    service_time = np.random.uniform(min_waktu, max_waktu, jumlah_mahasiswa)

    start_time = []
    finish_time = []
    waiting_time = []

    current_time = 0

    # Proses simulasi
    for i in range(jumlah_mahasiswa):
        start = current_time
        finish = start + service_time[i]

        start_time.append(start)
        finish_time.append(finish)
        waiting_time.append(start)

        current_time = finish

    # Dataframe
    df = pd.DataFrame({
        "Mahasiswa": range(1, jumlah_mahasiswa + 1),
        "Waktu Pelayanan (menit)": service_time,
        "Mulai Dilayani": start_time,
        "Selesai Dilayani": finish_time,
        "Waktu Tunggu": waiting_time
    })

    # Statistik
    total_waktu = finish_time[-1]
    rata_tunggu = np.mean(waiting_time)
    utilisasi = (sum(service_time) / total_waktu) * 100

    return df, total_waktu, rata_tunggu, utilisasi, finish_time


# ================================
# SIDEBAR INPUT
# ================================
st.sidebar.header("⚙️ Pengaturan Simulasi")

jumlah = st.sidebar.slider("Jumlah Mahasiswa", 10, 100, 30)
min_waktu = st.sidebar.slider("Waktu Minimum (menit)", 1, 5, 1)
max_waktu = st.sidebar.slider("Waktu Maksimum (menit)", 2, 10, 3)
seed = st.sidebar.number_input("Random Seed (opsional)", value=42)

run = st.sidebar.button("🚀 Jalankan Simulasi")

# ================================
# JIKA BELUM DIJALANKAN
# ================================
if not run:
    st.info("Silakan atur parameter di sidebar lalu klik **Jalankan Simulasi** 👈")

# ================================
# JALANKAN SIMULASI
# ================================
if run:

    df, total, rata, util, finish_time = simulasi_antrian(
        jumlah, min_waktu, max_waktu, seed
    )

    st.success("✅ Simulasi berhasil dijalankan!")

    # ================================
    # METRIC (STATISTIK UTAMA)
    # ================================
    st.subheader("📊 Statistik Utama")

    col1, col2, col3 = st.columns(3)

    col1.metric("⏱ Total Waktu", f"{total:.2f} menit")
    col2.metric("⌛ Rata-rata Tunggu", f"{rata:.2f} menit")
    col3.metric("📈 Utilisasi Server", f"{util:.2f}%")

    st.divider()

    # ================================
    # INTERPRETASI HASIL
    # ================================
    st.subheader("🧠 Analisis Singkat")

    if util > 90:
        st.warning("⚠️ Utilisasi sangat tinggi → sistem padat, antrian panjang")
    else:
        st.success("✅ Utilisasi normal → sistem cukup efisien")

    if rata > total / 2:
        st.warning("⚠️ Waktu tunggu cukup lama untuk mahasiswa akhir")
    else:
        st.info("ℹ️ Waktu tunggu masih dalam batas wajar")

    st.divider()

    # ================================
    # DATA TABEL
    # ================================
    st.subheader("📋 Data Simulasi Mahasiswa")

    st.dataframe(df, use_container_width=True)

    st.divider()

    # ================================
    # GRAFIK 1
    # ================================
    st.subheader("📈 Grafik Waktu Selesai")

    fig1, ax1 = plt.subplots()
    ax1.plot(df["Mahasiswa"], finish_time, marker='o')
    ax1.set_title("Waktu Selesai Setiap Mahasiswa")
    ax1.set_xlabel("Mahasiswa")
    ax1.set_ylabel("Waktu (menit)")
    ax1.grid(True)

    st.pyplot(fig1)

    # ================================
    # GRAFIK 2
    # ================================
    st.subheader("📊 Distribusi Waktu Pelayanan")

    fig2, ax2 = plt.subplots()
    ax2.hist(df["Waktu Pelayanan (menit)"], bins=10)
    ax2.set_title("Distribusi Waktu Pelayanan")
    ax2.set_xlabel("Waktu (menit)")
    ax2.set_ylabel("Frekuensi")

    st.pyplot(fig2)

    st.divider()

    # ================================
    # DOWNLOAD DATA
    # ================================
    st.subheader("⬇️ Download Hasil")

    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download Data CSV",
        data=csv,
        file_name="hasil_simulasi.csv",
        mime="text/csv"
    )

    # ================================
    # FOOTER
    # ================================
    st.markdown("""
    ---
    👨‍💻 Dibuat untuk Praktikum Pemodelan & Simulasi  
    Sistem: Single Server Queue (FIFO)  
    """)