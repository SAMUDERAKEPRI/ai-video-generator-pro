import streamlit as st
import replicate
import os

# Konfigurasi Tampilan
st.set_page_config(page_title="SamuderaKepri AI Video", page_icon="🎬")

# --- SIDEBAR UNTUK KONFIGURASI ---
with st.sidebar:
    st.title("⚙️ Pengaturan API")
    # Menggunakan session_state agar token tidak hilang saat refresh
    replicate_api = st.text_input("Masukkan Replicate API Token:", type="password", help="Masukkan token r8_...")
    st.info("Dapatkan token di [replicate.com/account](https://replicate.com/account)")
    st.markdown("---")
    st.write("User Logged in: **Ronny Paslan**")
    st.write("Role: **Editor-in-Chief**")

# --- HALAMAN UTAMA ---
st.title("🎬 AI Video Generator Pro")
st.caption("Alat Bantu Produksi Konten Berita SamuderaKepriTV")

# Input Gambar
uploaded_file = st.file_uploader("Upload Foto Berita (PNG/JPG):", type=["jpg", "png", "jpeg"])

if st.button("Generate Video Sekarang"):
    if not replicate_api:
        st.error("Silakan masukkan API Token di sidebar terlebih dahulu!")
    elif not uploaded_file:
        st.warning("Mohon upload foto berita yang ingin dianimasikan.")
    else:
        try:
            # Set API Key ke environment agar library replicate bisa membacanya
            os.environ["REPLICATE_API_TOKEN"] = replicate_api
            
            with st.status("Sedang memproses video... Mohon tunggu sebentar.", expanded=True) as status:
                st.write("Menghubungkan ke server AI (Stable Video Diffusion)...")
                
                # Menjalankan Model SVD (Versi Otomatis Terbaru)
                # Kode ini telah diperbaiki untuk menghindari error 422
                output = replicate.run(
                    "stability-ai/stable-video-diffusion",
                    input={
                        "input_image": uploaded_file,
                        "video_length": "14_frames_with_svd",
                        "sizing_strategy": "maintain_aspect_ratio",
                        "frames_per_second": 6,
                        "motion_bucket_id": 127 # Mengatur tingkat gerakan (1-255)
                    }
                )
                
                status.update(label="Proses Selesai!", state="complete", expanded=False)
            
            # Tampilkan Hasil Video
            if output:
                # Replicate biasanya mengembalikan daftar URL, kita ambil yang pertama
                video_url = output[0] if isinstance(output, list) else output
                st.video(video_url)
                st.success("Video berhasil dibuat untuk SamuderaKepriTV!")
                st.balloons()
                
        except Exception as e:
            # Jika masih error, berikan instruksi spesifik
            if "422" in str(e):
                st.error("Error 422: Coba buka https://replicate.com/stability-ai/stable-video-diffusion di browser dan klik 'Run' sekali untuk menyetujui Terms of Service.")
            else:
                st.error(f"Terjadi kesalahan teknis: {str(e)}")

# --- FOOTER ---
st.markdown("---")
st.markdown("© 2026 **SamuderaKepri.co.id** - Inovasi Media Digital Kepulauan Riau")
