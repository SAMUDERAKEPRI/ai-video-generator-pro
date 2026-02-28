import streamlit as st

st.set_page_config(page_title="SamuderaKepri AI Video Generator", page_icon="🎬")

st.title("🎬 AI Video Generator Pro")
st.subheader("Khusus Redaksi SamuderaKepri.co.id")

# Input teks berita
news_text = st.text_area("Masukkan naskah berita atau artikel:", placeholder="Contoh: Laporan dugaan korupsi di Anambas...")

# Pilihan Model AI
ai_model = st.selectbox("Pilih Mesin AI:", ["Stable Video Diffusion", "OpenAI Sora (Coming Soon)", "Runway Gen-2"])

if st.button("Generate Video"):
    if news_text:
        st.info(f"Sedang memproses video menggunakan model {ai_model}...")
        # Di sini nantinya kita hubungkan ke API Key AI
        st.warning("Fitur integrasi API sedang dikonfigurasi.")
    else:
        st.error("Silakan masukkan naskah terlebih dahulu!")

st.sidebar.markdown("---")
st.sidebar.write("Logged in as: **Ronny Paslan**")
