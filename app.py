import streamlit as st
import replicate
import os

# Konfigurasi Tampilan
st.set_page_config(page_title="SamuderaKepri AI Video", page_icon="🎬")

# --- SIDEBAR UNTUK KONFIGURASI ---
with st.sidebar:
    st.title("⚙️ Pengaturan API")
    replicate_api = st.text_input("Masukkan Replicate API Token:", type="password", help="Masukkan token r8_...")
    st.info("Dapatkan token di [replicate.com/account](https://replicate.com/account)")
    st.markdown("---")
    st.write("User Logged in: **Ronny Paslan**")
    st.write("Role: **CEO SamuderaKepri.co.id**")

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
            # Set API Key ke environment
            os.environ["REPLICATE_API_TOKEN"] = replicate_api
            
            with st.status("Sedang memproses video... Mohon tunggu.", expanded=True) as status:
                st.write("Menghubungkan ke model AI (Stable Video Diffusion)...")
                
                # --- SOLUSI FIX 422: MEMANGGIL MODEL TANPA ID VERSI PANJANG ---
                # Ini akan otomatis mengambil versi terbaru yang diizinkan
                model = replicate.models.get("stability-ai/svd")
                version = model.versions.list()[0] # Mengambil versi paling atas (terbaru)
                
                output = replicate.run(
                    f"{model.owner}/{model.name}:{version.id}",
                    input={
                        "input_image": uploaded_file,
                        "video_length": "14_frames_with_svd",
                        "sizing_strategy": "maintain_aspect_ratio",
                        "frames_per_second": 6,
                        "motion_bucket_id": 127
                    }
                )
                
                status.update(label="Proses Selesai!", state="complete", expanded=False)
            
            # Tampilkan Hasil Video
            if output:
                video_url = output[0] if isinstance(output, list) else output
                st.video(video_url)
                st.success("Video berhasil dibuat untuk SamuderaKepriTV!")
                st.balloons()
                
        except Exception as e:
            error_msg = str(e)
            if "422" in error_msg:
                st.error("Izin Ditolak: Bapak perlu membuka https://replicate.com/stability-ai/svd di browser, lalu klik 'Run' sekali saja untuk menyetujui syarat penggunaan (Terms).")
            elif "401" in error_msg:
                st.error("Token API tidak valid. Pastikan r8_... sudah benar.")
            else:
                st.error(f"Terjadi kesalahan teknis: {error_msg}")

# --- FOOTER ---
st.markdown("---")
st.markdown("© 2026 **SamuderaKepri.co.id** - Inovasi Media Digital Kepulauan Riau")
