import streamlit as st
from features.face_dataset import main as face_dataset_main
from features.image_processing import main as processing_main
from features.image_analysis import main as analysis_main
from features.image_compression import main as compression_main
from features.color_conversion import main as color_space_main
from style import inject_custom_css, render_header, render_sidebar_content, render_page_header, render_footer

# Page configuration
st.set_page_config(
    page_title="Image Processing", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.streamlit.io/community',
        'Report a bug': "https://github.com/streamlit/streamlit/issues",
        'About': "# Pengolahan Citra Digital\n*Created by Dwika Ali Ramdhan*"
    }
)

inject_custom_css()

render_header()

with st.sidebar:
    page = render_sidebar_content()

st.markdown("<br>", unsafe_allow_html=True)

# Content container
with st.container():
    if page == "Face Dataset Addition":
        render_page_header(
            "Face Dataset Addition",
            "Modul untuk menambahkan dan mengelola dataset wajah dengan mudah dan efisien. "
            "Fitur ini memungkinkan Anda untuk mengorganisir dan memproses data wajah untuk berbagai keperluan analisis."
        )
        face_dataset_main()

    elif page == "Image Processing Techniques":
        render_page_header(
            "Image Processing Techniques",
            "Berbagai teknik pemrosesan gambar untuk filtering, enhancement, dan transformasi. "
            "Eksplorasi metode-metode canggih dalam manipulasi dan perbaikan kualitas gambar digital."
        )
        processing_main()

    elif page == "Image Analysis":
        render_page_header(
            "Image Analysis",
            "Analisis mendalam terhadap karakteristik dan properti gambar digital. "
            "Dapatkan insight tentang histogram, statistik, dan fitur-fitur penting dari gambar Anda."
        )
        analysis_main()

    elif page == "Image Compression Analysis":
        render_page_header(
            "Image Compression Analysis",
            "Analisis berbagai metode kompresi gambar dan perbandingan kualitas. "
            "Evaluasi trade-off antara ukuran file dan kualitas gambar dengan berbagai algoritma kompresi."
        )
        compression_main()

    elif page == "Color Space Conversion":
        render_page_header(
            "Color Space Conversion",
            "Konversi antara berbagai ruang warna seperti RGB, HSV, LAB dengan visualisasi interaktif. "
            "Pahami karakteristik setiap ruang warna dan aplikasinya dalam pemrosesan gambar."
        )
        color_space_main()

render_footer()