import streamlit as st
import replicate
import os
import time

st.set_page_config(page_title="SamuderaKepri AI Video", page_icon="🎬")

# --- SIDEBAR UNTUK KONFIGURASI ---
with st.sidebar:
    st.title("⚙️ Pengaturan API")
    # Bapak bisa mendapatkan API Key di replicate.com
    replicate_api = st.text_input("Masukkan Replicate API Token:", type="password")
    st.info("Dapatkan token di [replicate.com/account](https://replicate.com/account)")
    st.markdown("---")
    st.write("User: **Ronny Paslan**")

# --- HALAMAN UTAMA ---
st.title("🎬 AI Video Generator Pro")
st.caption("Alat Bantu Produksi Konten SamuderaKepriTV")

# Input Gambar (SVD bekerja lebih baik dengan Image-to-Video)
uploaded_file = st.file_uploader("Upload Foto Berita (PNG/JPG):", type=["jpg", "png", "jpeg"])

if st.button("Generate Video Sekarang"):
    if not replicate_api:
        st.error("Silakan masukkan API Token di sidebar terlebih dahulu!")
    elif not uploaded_file:
        st.warning("Mohon upload foto berita yang ingin dianimasikan.")
    else:
        try:
            # Set API Key ke environment
            os.environ["REPLICATE_API_TOKEN"] = replicate_api
            
            with st.status("Sedang memproses video... Mohon tunggu.", expanded=True) as status:
                st.write("Mengirim data ke model Stable Video Diffusion...")
                
                # Menjalankan Model SVD di Replicate
                output = replicate.run(
                    "stability-ai/stable-video-diffusion:3f04571b066757116e39748fa091919864205574f8845e2da04b338ba4a3b7d1",
                    input={
                        "input_image": uploaded_file,
                        "video_length": "14_frames_with_svd",
                        "sizing_strategy": "maintain_aspect_ratio"
                    }
                )
                
                status.update(label="Proses Selesai!", state="complete", expanded=False)
            
            # Tampilkan Hasil Video
            if output:
                st.video(output[0])
                st.success("Video berhasil dibuat! Silakan klik kanan untuk download.")
                
        except Exception as e:
            st.error(f"Terjadi kesalahan: {str(e)}")

# --- FOOTER ---
st.markdown("---")
st.markdown("© 2026 **SamuderaKepri.co.id** - Inovasi Digital Kepulauan Riau")
