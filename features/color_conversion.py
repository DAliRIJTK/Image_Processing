import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io

def opencv_to_pil(image):
    if len(image.shape) == 2:
        return Image.fromarray(image.astype(np.uint8))
    else:
        return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

def read_image(uploaded_file):
    image_data = np.frombuffer(uploaded_file.read(), np.uint8)
    img = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    return img

def rgb_to_yiq(rgb):
    transform_matrix = np.array([[0.299, 0.587, 0.114],
                                [0.59590059, -0.27455667, -0.32134392],
                                [0.21153661, -0.52273617, 0.31119955]])
    yiq = np.dot(rgb, transform_matrix.T)
    yiq = (yiq - np.min(yiq)) / (np.max(yiq) - np.min(yiq))
    return yiq

def rgb_to_hsi(rgb):
    with np.errstate(divide='ignore', invalid='ignore'):
        rgb = np.float32(rgb) / 255.0
        r, g, b = cv2.split(rgb)
        intensity = np.divide(r + g + b, 3)
        minimum = np.minimum(np.minimum(r, g), b)
        saturation = 1 - 3 * np.divide(minimum, r + g + b + 1e-6)
        sqrt_calc = np.sqrt(((r - g) * (r - g)) + ((r - b) * (g - b)))
        theta = np.arccos(0.5 * ((r - g + r - b) / (sqrt_calc + 1e-6)))
        hue = np.where(b <= g, theta, 2 * np.pi - theta)
        hsi = cv2.merge((hue, saturation, intensity))
        return hsi, hue, saturation, intensity

def process_color_space(img, color_space):
    image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    if color_space == "RGB":
        st.subheader("RGB Image")
        st.image(opencv_to_pil(image_rgb), use_column_width=True)
        R, G, B = cv2.split(image_rgb)
        fig, axes = plt.subplots(1, 3, figsize=(12, 4))
        axes[0].imshow(R, cmap='gray')
        axes[0].set_title('R Channel')
        axes[1].imshow(G, cmap='gray')
        axes[1].set_title('G Channel')
        axes[2].imshow(B, cmap='gray')
        axes[2].set_title('B Channel')
        plt.tight_layout()
        st.pyplot(fig)
    
    elif color_space == "XYZ":
        image_xyz = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2XYZ)
        st.subheader("XYZ Image")
        st.image(opencv_to_pil(image_xyz), use_column_width=True)
        X, Y, Z = cv2.split(image_xyz)
        X_norm = cv2.normalize(X, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        Y_norm = cv2.normalize(Y, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        Z_norm = cv2.normalize(Z, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        fig, axes = plt.subplots(1, 3, figsize=(12, 4))
        axes[0].imshow(X_norm, cmap='gray')
        axes[0].set_title('X Component')
        axes[1].imshow(Y_norm, cmap='gray')
        axes[1].set_title('Y Component (Luminance)')
        axes[2].imshow(Z_norm, cmap='gray')
        axes[2].set_title('Z Component')
        plt.tight_layout()
        st.pyplot(fig)
    
    elif color_space == "Lab":
        image_lab = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2Lab)
        st.subheader("CIELab Image")
        st.image(opencv_to_pil(image_lab), use_column_width=True)
        L, a, b = cv2.split(image_lab)
        L_norm = cv2.normalize(L, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        a_norm = cv2.normalize(a, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        b_norm = cv2.normalize(b, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        fig, axes = plt.subplots(1, 3, figsize=(10, 3))
        axes[0].imshow(L_norm, cmap='gray')
        axes[0].set_title('L (Luminance)')
        axes[1].imshow(a_norm, cmap='gray')
        axes[1].set_title('a (Green-Red)')
        axes[2].imshow(b_norm, cmap='gray')
        axes[2].set_title('b (Blue-Yellow)')
        plt.tight_layout()
        st.pyplot(fig)
    
    elif color_space == "YCbCr":
        image_ycbcr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2YCrCb)
        st.subheader("YCbCr Image")
        st.image(opencv_to_pil(image_ycbcr), use_column_width=True)
        Y, Cb, Cr = cv2.split(image_ycbcr)
        Y_norm = cv2.normalize(Y, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        Cb_norm = cv2.normalize(Cb, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        Cr_norm = cv2.normalize(Cr, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        fig, axes = plt.subplots(1, 3, figsize=(10, 3))
        axes[0].imshow(Y_norm, cmap='gray')
        axes[0].set_title('Y (Luminance)')
        axes[1].imshow(Cb_norm, cmap='gray')
        axes[1].set_title('Cb (Blue Chrominance)')
        axes[2].imshow(Cr_norm, cmap='gray')
        axes[2].set_title('Cr (Red Chrominance)')
        plt.tight_layout()
        st.pyplot(fig)
    
    elif color_space == "YIQ":
        image_yiq = rgb_to_yiq(image_rgb / 255.0)
        st.subheader("YIQ Image")
        st.image(image_yiq, use_column_width=True)
        Y, I, Q = image_yiq[:, :, 0], image_yiq[:, :, 1], image_yiq[:, :, 2]
        I_norm = cv2.normalize(I, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        Q_norm = cv2.normalize(Q, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        fig, axes = plt.subplots(1, 3, figsize=(10, 3))
        axes[0].imshow(Y, cmap='gray')
        axes[0].set_title('Y (Luminance)')
        axes[1].imshow(I_norm, cmap='gray')
        axes[1].set_title('I (In-phase)')
        axes[2].imshow(Q_norm, cmap='gray')
        axes[2].set_title('Q (Quadrature)')
        plt.tight_layout()
        st.pyplot(fig)
    
    elif color_space == "YUV":
        image_yuv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2YUV)
        st.subheader("YUV Image")
        st.image(opencv_to_pil(image_yuv), use_column_width=True)
        Y, U, V = cv2.split(image_yuv)
        fig, axes = plt.subplots(1, 3, figsize=(10, 4))
        axes[0].imshow(Y, cmap='gray')
        axes[0].set_title('Y Channel')
        axes[1].imshow(U, cmap='gray')
        axes[1].set_title('U Channel')
        axes[2].imshow(V, cmap='gray')
        axes[2].set_title('V Channel')
        plt.tight_layout()
        st.pyplot(fig)
    
    elif color_space == "HSI":
        image_hsi, H, S, I = rgb_to_hsi(image_rgb)
        st.subheader("HSI Image")
        st.image(image_hsi, use_column_width=True)
        fig, axes = plt.subplots(1, 3, figsize=(10, 4))
        axes[0].imshow(H, cmap='hsv')
        axes[0].set_title('Hue')
        axes[1].imshow(S, cmap='gray')
        axes[1].set_title('Saturation')
        axes[2].imshow(I, cmap='gray')
        axes[2].set_title('Intensity')
        plt.tight_layout()
        st.pyplot(fig)
    
    elif color_space == "Luv":
        image_luv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2Luv)
        luv_normalized = cv2.normalize(image_luv, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        st.subheader("CIELuv Image")
        st.image(opencv_to_pil(luv_normalized), use_column_width=True)
        L, u, v = cv2.split(luv_normalized)
        fig, axes = plt.subplots(1, 3, figsize=(10, 4))
        axes[0].imshow(L, cmap='gray')
        axes[0].set_title('L Channel')
        axes[1].imshow(u, cmap='gray')
        axes[1].set_title('u Channel')
        axes[2].imshow(v, cmap='gray')
        axes[2].set_title('v Channel')
        plt.tight_layout()
        st.pyplot(fig)

def main():
    st.title("Color Space Conversion with Streamlit")
    st.write("Upload an image and select a color space to view the converted image and its components.")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        img = read_image(uploaded_file)
        st.subheader("Original Image")
        st.image(opencv_to_pil(img), use_column_width=True)

        color_space = st.selectbox("Select Color Space", 
                                  ["RGB", "XYZ", "Lab", "YCbCr", "YIQ", "YUV", "HSI", "Luv"])
        
        if st.button("Process Image"):
            process_color_space(img, color_space)

if __name__ == "__main__":
    main()