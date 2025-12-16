import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter
from rembg import remove

st.set_page_config(page_title="AI Matrix Transformation", layout="wide")

st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at 10% 20%, rgba(255,255,255,0.06), transparent 30%),
                radial-gradient(circle at 90% 80%, rgba(255,255,255,0.04), transparent 35%),
                linear-gradient(135deg, #1f3a2e, #2e4f3e);
    background-size: 400% 400%;
    animation: gradientShift 10s ease infinite;
    color: #eef4f1;
    font-family: 'Segoe UI', sans-serif;
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.block-container { padding-top: 2.5rem; }
p, label { color: #e5efe9; }
.team-card {
    background: linear-gradient(180deg, #ffffff, #eef4ff);
    padding: 20px 18px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    margin: 20px auto;
    max-width: 380px;
    animation: fadeUp 0.6s ease both;
}
.profile-pic {
    display: block;
    margin: 0 auto 10px;
    border-radius: 50%;
    border: 3px solid rgba(0,102,204,0.25);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.profile-pic:hover {
    transform: scale(1.05);
    box-shadow: 0 0 0 5px rgba(0,102,204,0.25);
}
.team-name { color: #1a1a1a; font-size: 16px; font-weight: 700; }
.team-nim { color: #000000; font-size: 12px; margin-top: 3px; }
.team-role {
    display: inline-block;
    margin-top: 6px;
    padding: 5px 12px;
    border-radius: 15px;
    background: rgba(0, 102, 204, 0.2);
    color: #003366;
    font-size: 12px;
    font-weight: 600;
}
.team-card p { color: #000000 !important; font-size: 13px; margin-top: 10px; line-height: 1.4; opacity: 1 !important; }
.team-card * { opacity: 1 !important; }
@keyframes fadeUp { from { transform: translateY(15px); } to { transform: translateY(0); } }
</style>
""", unsafe_allow_html=True)

lang = st.sidebar.radio("🌐 Language / Bahasa", ["English", "Indonesia"])

def L(en, id):
    return en if lang == "English" else id

page = st.sidebar.radio(
    L("Navigation", "Navigasi"),
    [L("Home", "Beranda"), L("AI Matrix Transformation", "Transformasi Matriks AI"), L("Developer Team", "Tim Pengembang")]
)

if page == L("Home", "Beranda"):
    st.title("🏠 " + L("Home", "Beranda"))
    st.write(L(
        "Welcome to AI Matrix Transformation! 🚀 This app allows you to apply geometric transformations, filters, and visualize matrix operations on images. Let's dive into the world of image processing! ✨",
        "Selamat datang di Transformasi Matriks AI! 🚀 Aplikasi ini memungkinkan Anda menerapkan transformasi geometri, filter, dan memvisualisasikan operasi matriks pada gambar. Mari jelajahi dunia pemrosesan gambar! ✨"
    ))
    st.subheader(L("Features", "Fitur") + " 🌟")
    st.write(L(
        "- **Geometric Transformations** 🔄: Translate, scale, rotate, shear, and reflect images.\n"
        "- **Image Filters** 🎨: Apply blur, sharpen, or remove backgrounds.\n"
        "- **Matrix Visualization** 📊: See how transformations affect points in a matrix.\n"
        "- **Multi-language Support** 🌍: Switch between English and Indonesian.",
        "- **Transformasi Geometri** 🔄: Translasi, skala, rotasi, geser, dan refleksi gambar.\n"
        "- **Filter Gambar** 🎨: Terapkan blur, sharpen, atau hapus latar belakang.\n"
        "- **Visualisasi Matriks** 📊: Lihat bagaimana transformasi memengaruhi titik dalam matriks.\n"
        "- **Dukungan Multi-bahasa** 🌍: Beralih antara Bahasa Inggris dan Indonesia."
    ))
    st.subheader(L("About Us", "Tentang Kami") + " 👥")
    st.write(L(
        "Developed by Group 4, Class 2. 🌟 Explore the power of matrix transformations in image processing! Ready to transform your images? 🎉",
        "Dikembangkan oleh Kelompok 4, Kelas 2. 🌟 Jelajahi kekuatan transformasi matriks dalam pemrosesan gambar! Siap untuk mentransformasi gambar Anda? 🎉"
    ))

elif page == L("AI Matrix Transformation", "Transformasi Matriks AI"):
    st.title("🧮 AI Matrix Transformation")
    st.caption(L("Geometric Transformations, Filters & Matrix Visualization", "Transformasi Geometri, Filter & Visualisasi Matriks") + " ✨")
    st.divider()
    st.subheader(L("📤 Upload Image", "📤 Unggah Gambar") + " 🖼️")
    file = st.file_uploader(L("Upload image (JPG / PNG)", "Unggah gambar (JPG / PNG)"), ["jpg", "png", "jpeg"])
    point = np.array([[1], [1]])
    if file:
        img = Image.open(file).convert("RGBA")
        st.image(img, caption=L("Original Image", "Gambar Asli") + " 📸", width=300)
        st.divider()
        st.subheader(L("📐 Geometric Transformations", "📐 Transformasi Geometri") + " 🔄")
        col1, col2 = st.columns(2)
        with col1:
            use_translation = st.checkbox(L("Translation", "Translasi") + " 📍")
            use_scaling = st.checkbox(L("Scaling", "Skala") + " 📏")
            use_shearing = st.checkbox(L("Shearing", "Geser (Shear)") + " ✂️")
        with col2:
            use_rotation = st.checkbox(L("Rotation", "Rotasi") + " 🔄")
            use_reflection = st.checkbox(L("Reflection", "Refleksi") + " 🪞")
        if use_translation:
            dx = st.slider("dx", -200, 200, 0)
            dy = st.slider("dy", -200, 200, 0)
        if use_scaling:
            sx = st.slider(L("Scale X", "Skala X"), 0.1, 3.0, 1.0)
            sy = st.slider(L("Scale Y", "Skala Y"), 0.1, 3.0, 1.0)
        if use_rotation:
            angle = st.slider(L("Rotation Angle (°)", "Sudut Rotasi (°)"), -180, 180, 0)
        if use_shearing:
            shx = st.slider(L("Shear X", "Geser X"), -2.0, 2.0, 0.0)
            shy = st.slider(L("Shear Y", "Geser Y"), -2.0, 2.0, 0.0)
        if use_reflection:
            axis = st.radio(L("Reflection Axis", "Sumbu Refleksi"), [L("Horizontal", "Horizontal"), L("Vertical", "Vertikal")])
        st.divider()
        st.subheader(L("🎨 Image Filters", "🎨 Filter Gambar") + " 🖌️")
        filter_blur = st.checkbox(L("Blur Image", "Kaburkan Gambar") + " 🌫️")
        filter_sharpen = st.checkbox(L("Sharpen Image", "Pertajam Gambar") + " ⚡")
        filter_remove_bg = st.checkbox(L("Remove Background", "Hapus Latar Belakang") + " 🗑️")
        st.divider()
        if st.button(L("🚀 Process Image", "🚀 Proses Gambar") + " ✨"):
            result = img.copy()
            w, h = result.size
            if use_scaling:
                result = result.resize((int(w * sx), int(h * sy)))
            if use_rotation:
                result = result.rotate(angle, expand=True)
            if use_shearing:
                shear_matrix = (1, shx, 0, shy, 1, 0)
                result = result.transform(result.size, Image.AFFINE, shear_matrix)
            if use_translation:
                canvas = Image.new("RGBA", (w + abs(dx), h + abs(dy)), (0, 0, 0, 0))
                canvas.paste(result, (max(dx, 0), max(dy, 0)))
                result = canvas
            if use_reflection:
                if axis == L("Horizontal", "Horizontal"):
                    result = result.transpose(Image.FLIP_TOP_BOTTOM)
                else:
                    result = result.transpose(Image.FLIP_LEFT_RIGHT)
            if filter_blur:
                result = result.filter(ImageFilter.BLUR)
            if filter_sharpen:
                result = result.filter(ImageFilter.SHARPEN)
            if filter_remove_bg:
                result = remove(result)
            st.subheader(L("📤 Output", "📤 Hasil") + " 🎯")
            colA, colB = st.columns(2)
            with colA:
                st.image(img, caption=L("Original Image", "Gambar Asli") + " 📸")
            with colB:
                st.image(result, caption=L("Processed Image", "Gambar Hasil") + " 🖼️")
            st.divider()
            st.subheader(L("📊 Matrix Visualization", "📊 Visualisasi Matriks") + " 🔍")
            transformed_point = point.copy()
            if use_scaling:
                S = np.array([[sx, 0], [0, sy]])
                transformed_point = S @ transformed_point
            if use_rotation:
                r = np.radians(angle)
                R = np.array([[np.cos(r), -np.sin(r)], [np.sin(r), np.cos(r)]])
                transformed_point = R @ transformed_point
            if use_shearing:
                Sh = np.array([[1, shx], [shy, 1]])
                transformed_point = Sh @ transformed_point
            if use_translation:
                transformed_point += np.array([[dx / 100], [dy / 100]])
            if use_reflection:
                Ref = np.array([[1, 0], [0, -1]]) if axis == L("Horizontal", "Horizontal") else np.array([[-1, 0], [0, 1]])
                transformed_point = Ref @ transformed_point
            fig, ax = plt.subplots()
            ax.scatter(point[0], point[1], s=100, label=L("Original Point", "Titik Awal") + " 🔵")
            ax.scatter(transformed_point[0], transformed_point[1], s=100, label=L("Transformed Point", "Titik Transformasi") + " 🔴")
            ax.axhline(0)
            ax.axvline(0)
            ax.grid(True)
            ax.legend()
            st.pyplot(fig)
    else:
        st.info(L("Please upload an image to start.", "Silakan unggah gambar untuk memulai.") + " 📤")

elif page == L("Developer Team", "Tim Pengembang"):
    st.title("👨‍💻 " + L("Developer Team", "Tim Pengembang") + " 🌟")
    st.caption(L("Group 4 – Class 2", "Kelompok 4 – Kelas 2") + " 👥")
    members = [
        ("Fazayya Syauqi Wardani", "004202400072", "Team Leader", "Ketua Tim",
         "Project coordination & matrix logic design", "Koordinasi proyek & logika matriks", "assets/member1.jpeg"),
        ("Lulu Zenover", "004202400081", "Deployment Engineer", "Deploy & Integrasi",
         "Application deployment & integration", "Deploy aplikasi & integrasi", "assets/member2.jpeg"),
        ("Nazwa Safa Davina", "004202400074", "UI/UX Designer", "Desain UI/UX",
         "Interface design & documentation", "Desain antarmuka & dokumentasi", "assets/member3.jpeg"),
        ("Raisyah Aditya Sufah", "004202400082", "Image Processing Engineer", "Pemrosesan Citra",
         "Image transformation logic", "Logika transformasi citra", "assets/member4.jpeg")
    ]
    for m in members:
        try:
            profile_img = Image.open(m[6])
            st.image(profile_img, width=150, caption="")
        except FileNotFoundError:
            st.warning(f"Image {m[6]} not found. Please ensure the image file exists in the 'assets' folder.")
            st.image("https://via.placeholder.com/150", width=150, caption="Placeholder")
        st.markdown(f"""
        <div class="team-card">
            <div class="team-name">{m[0]} 👩‍💻</div>
            <div class="team-nim">{m[1]}</div>
            <div class="team-role">{L(m[2], m[3])} 🏆</div>
            <p>{L(m[4], m[5])} 🚀</p>
        </div>
        """, unsafe_allow_html=True)



