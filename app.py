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
                st.write("Menghubungkan ke server AI...")
                
                # PERBAIKAN: Menggunakan model 'stability-ai/svd' versi terbaru yang aktif
                # Ini adalah ID versi yang paling stabil saat ini
                model_version = "stability-ai/svd:3f04571b066757116e39748fa091919864205574f8845e2da04b338ba4a3b7d1"
                
                # Eksekusi Model
                output = replicate.run(
                    model_version,
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
                # Jika output berupa list, ambil yang pertama
                video_url = output[0] if isinstance(output, list) else output
                st.video(video_url)
                st.success("Video berhasil dibuat untuk SamuderaKepriTV!")
                st.balloons()
                
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg:
                st.error("Error 404: Alamat model tidak ditemukan. Saya akan coba gunakan metode alternatif...")
                # Metode Cadangan (Tanpa ID Versi)
                try:
                    output = replicate.run("stability-ai/svd", input={"input_image": uploaded_file})
                    st.video(output[0])
                except:
                    st.error("Gagal terhubung. Pastikan akun Replicate Bapak sudah aktif.")
            else:
                st.error(f"Terjadi kesalahan teknis: {error_msg}")

# --- FOOTER ---
st.markdown("---")
st.markdown("© 2026 **SamuderaKepri.co.id** - Inovasi Media Digital Kepulauan Riau")
