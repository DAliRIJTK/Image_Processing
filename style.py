# style.py
import streamlit as st

def inject_custom_css():
    """
    Inject custom CSS styling for the Image Processing Suite application.
    This function contains all the modern styling and theme configurations.
    """
    st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Source+Code+Pro:wght@400;500;600&display=swap');
        
        /* Modern Theme Variables */
        :root {
            --primary-bg: #ffffff;
            --secondary-bg: #f8fafc;
            --card-bg: #ffffff;
            --sidebar-bg: #f1f5f9;
            --accent-color: #3b82f6;
            --accent-hover: #2563eb;
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --border-color: #e2e8f0;
            --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --gradient-accent: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            --shadow-light: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            --shadow-medium: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-large: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }
        
        /* Main App Background */
        .stApp {
            background: var(--primary-bg);
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
        }
        
        /* Main Content Area */
        .main .block-container {
            background: var(--primary-bg);
            padding: 2rem 3rem;
            max-width: 1200px;
        }
        
        /* Sidebar Styling */
        .css-1d391kg {
            background: var(--sidebar-bg);
            border-right: 1px solid var(--border-color);
        }
        
        .css-1lcbmhc {
            background: var(--sidebar-bg);
        }
        
        /* Header Styling */
        .header-container {
            background: var(--gradient-primary);
            padding: 4rem 2rem;
            margin: -2rem -3rem 3rem -3rem;
            border-radius: 0 0 24px 24px;
            text-align: center;
            position: relative;
            overflow: hidden;
            box-shadow: var(--shadow-large);
        }
        
        .header-container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: rotate 30s linear infinite;
        }
        
        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .header-title {
            color: white;
            font-size: 3.2rem;
            font-weight: 700;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            position: relative;
            z-index: 1;
            letter-spacing: -0.025em;
        }
        
        .header-subtitle {
            color: rgba(255,255,255,0.95);
            font-size: 1.25rem;
            font-weight: 500;
            margin: 1rem 0 0 0;
            position: relative;
            z-index: 1;
        }
        
        /* Content Cards */
        .content-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 2rem;
            margin: 2rem 0;
            box-shadow: var(--shadow-light);
            transition: all 0.3s ease;
        }
        
        .content-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-medium);
            border-color: var(--accent-color);
        }
        
        /* Sidebar Navigation */
        .stRadio > div {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid var(--border-color);
            box-shadow: var(--shadow-light);
        }
        
        .stRadio > div > label {
            color: var(--text-primary) !important;
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 1rem;
        }
        
        .stRadio > div > div {
            gap: 0.75rem;
        }
        
        .stRadio > div > div > div {
            background: var(--secondary-bg);
            border: 2px solid var(--border-color);
            border-radius: 10px;
            padding: 1rem 1.25rem;
            margin: 0.5rem 0;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        
        .stRadio > div > div > div:hover {
            border-color: var(--accent-color);
            background: rgba(59, 130, 246, 0.05);
            transform: translateX(4px);
        }
        
        .stRadio > div > div > div[data-checked="true"] {
            background: var(--gradient-accent);
            border-color: var(--accent-color);
            color: white;
            box-shadow: var(--shadow-medium);
            transform: translateX(4px);
        }
        
        /* Buttons */
        .stButton > button {
            background: var(--gradient-accent);
            color: white;
            font-weight: 600;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: var(--shadow-light);
            font-family: 'Inter', sans-serif;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-medium);
            background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        }
        
        .stButton > button:active {
            transform: translateY(0px);
            box-shadow: var(--shadow-light);
        }
        
        /* Sidebar Title */
        .css-1lcbmhc h1 {
            color: var(--accent-color);
            font-size: 1.5rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid var(--border-color);
        }
        
        /* Content Subheaders */
        .stApp h2, .stApp h3 {
            color: var(--accent-color);
            font-weight: 700;
            margin-bottom: 1.5rem;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid var(--border-color);
            font-size: 2rem;
        }
        
        /* Markdown and Text */
        .stMarkdown {
            color: var(--text-primary);
        }
        
        .stMarkdown p {
            color: var(--text-secondary);
            line-height: 1.7;
            font-size: 1.05rem;
        }
        
        /* File Uploader */
        .stFileUploader > div {
            background: var(--secondary-bg);
            border: 2px dashed var(--border-color);
            border-radius: 12px;
            transition: all 0.3s ease;
            padding: 2rem;
        }
        
        .stFileUploader > div:hover {
            border-color: var(--accent-color);
            background: rgba(59, 130, 246, 0.02);
        }
        
        /* Selectbox and other inputs */
        .stSelectbox > div > div {
            background: var(--card-bg);
            border: 2px solid var(--border-color);
            border-radius: 10px;
            color: var(--text-primary);
            transition: all 0.3s ease;
        }
        
        .stSelectbox > div > div:focus-within {
            border-color: var(--accent-color);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        .stSelectbox > div > div > div {
            color: var(--text-primary);
        }
        
        /* Text Input */
        .stTextInput > div > div > input {
            background: var(--card-bg);
            border: 2px solid var(--border-color);
            border-radius: 10px;
            color: var(--text-primary);
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: var(--accent-color);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        /* Slider */
        .stSlider > div > div > div > div {
            background: var(--accent-color);
        }
        
        .stSlider > div > div > div {
            background: var(--border-color);
        }
        
        /* Divider */
        hr {
            border-color: var(--border-color);
            margin: 3rem 0;
            border-width: 1px;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background: var(--secondary-bg);
            border-radius: 12px;
            padding: 0.5rem;
            border: 1px solid var(--border-color);
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            color: var(--text-secondary);
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background: var(--gradient-accent);
            color: white;
            box-shadow: var(--shadow-light);
        }
        
        /* Metrics */
        .stMetric {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: var(--shadow-light);
            transition: all 0.3s ease;
        }
        
        .stMetric:hover {
            box-shadow: var(--shadow-medium);
            border-color: var(--accent-color);
        }
        
        /* Progress Bar */
        .stProgress > div > div > div > div {
            background: var(--gradient-accent);
        }
        
        /* Success/Error Messages */
        .stSuccess {
            background: rgba(34, 197, 94, 0.1);
            border: 1px solid rgba(34, 197, 94, 0.2);
            border-radius: 12px;
            color: rgb(21, 128, 61);
        }
        
        .stError {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            border-radius: 12px;
            color: rgb(185, 28, 28);
        }
        
        .stWarning {
            background: rgba(245, 158, 11, 0.1);
            border: 1px solid rgba(245, 158, 11, 0.2);
            border-radius: 12px;
            color: rgb(180, 83, 9);
        }
        
        .stInfo {
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 12px;
            color: rgb(29, 78, 216);
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--secondary-bg);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--border-color);
            border-radius: 4px;
            transition: all 0.3s ease;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent-color);
        }
        
        /* Feature Description Box */
        .feature-description {
            background: rgba(59, 130, 246, 0.05);
            border: 1px solid rgba(59, 130, 246, 0.1);
            border-radius: 12px;
            padding: 1.25rem;
            margin-top: 1rem;
            text-align: center;
        }
        
        .feature-description p {
            color: var(--text-secondary);
            margin: 0;
            font-size: 0.95rem;
            font-weight: 500;
        }
        
        /* Loading animation */
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .loading {
            animation: pulse 2s infinite;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .header-title {
                font-size: 2.5rem;
            }
            
            .main .block-container {
                padding: 1rem 2rem;
            }
            
            .header-container {
                margin: -1rem -2rem 2rem -2rem;
                padding: 3rem 1rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)

def render_header():
    """
    Render the application header with title and subtitle.
    """
    st.markdown("""
        <div class="header-container">
            <h1 class="header-title">Pengolahan Citra Digital</h1>
            <p class="header-subtitle" style ="color: #FFF">Dwika Ali Ramdhan - 231511042</p>
        </div>
    """, unsafe_allow_html=True)

def render_sidebar_content():
    """
    Render the sidebar navigation and feature descriptions.
    Returns the selected page.
    """
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #3b82f6; font-size: 1.8rem; margin: 0;">
                Navigation Menu
            </h1>
            <p style="color: #64748b; margin: 0.5rem 0 0 0; font-weight: 500;">Pilih fitur yang ingin dijalankan</p>
        </div>
    """, unsafe_allow_html=True)
    
    features = {
        "Face Dataset Addition": "Menambah dan mengelola dataset wajah",
        "Image Processing Techniques": "Teknik pemrosesan gambar lanjutan",
        "Image Analysis": "Analisis karakteristik gambar",
        "Image Compression Analysis": "Analisis kompresi dan kualitas",
        "Color Space Conversion": "Konversi ruang warna"
    }
    
    page = st.radio(
        "Modul Fitur",
        list(features.keys())
    )
    
    if page in features:
        st.markdown(f"""
            <div class="feature-description">
                <p>{features[page]}</p>
            </div>
        """, unsafe_allow_html=True)
    
    return page

def render_page_header(title, description):
    """
    Render a page header with title and description.
    
    Args:
        title (str): The page title
        description (str): The page description
    """
    st.markdown(f"""
        <div style="margin-bottom: 2rem;">
            <h2 style="color: #3b82f6;">{title}</h2>
            <p style="color: #64748b; font-size: 1.1rem; margin-bottom: 2rem; line-height: 1.6;">
                {description}
            </p>
        </div>
    """, unsafe_allow_html=True)

def render_footer():
    """
    Render the application footer.
    """
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="
            text-align: center; 
            padding: 2.5rem; 
            border-top: 1px solid #e2e8f0; 
            margin-top: 4rem;
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.03) 0%, rgba(102, 126, 234, 0.03) 100%);
            border-radius: 16px;
            border: 1px solid #e2e8f0;
        ">
            <p style="color: #64748b; margin: 0; font-size: 1rem; font-weight: 500;">
                <strong>Image Processing</strong>
            </p>
            <p style="color: #94a3b8; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                2024 Dwika Ali Ramdhan | Tugas Pengolahan Citra Digital
            </p>
        </div>
    """, unsafe_allow_html=True)