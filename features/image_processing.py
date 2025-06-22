import streamlit as st
import cv2
import numpy as np
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

def apply_convolution(image, kernel_type="average"):
    if kernel_type == "average":
        kernel = np.ones((3, 3), np.float32) / 9
    elif kernel_type == "sharpen":
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    elif kernel_type == "edge":
        kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    output_img = cv2.filter2D(image, -1, kernel)
    return output_img

def apply_zero_padding(image, padding_size=10):
    padded_img = cv2.copyMakeBorder(image, padding_size, padding_size, padding_size, padding_size, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    return padded_img

def apply_filter(image, filter_type="low"):
    if filter_type == "low":
        filtered_img = cv2.GaussianBlur(image, (5, 5), 0)
    elif filter_type == "high":
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        filtered_img = cv2.filter2D(image, -1, kernel)
    elif filter_type == "band":
        low_pass = cv2.GaussianBlur(image, (9, 9), 0)
        high_pass = image - low_pass
        filtered_img = low_pass + high_pass
    return filtered_img

def apply_fourier_transform(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift))
    return magnitude_spectrum

def reduce_periodic_noise(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)
    rows, cols = gray.shape
    crow, ccol = rows // 2, cols // 2
    mask = np.ones((rows, cols), np.uint8)
    r = 30
    mask[crow-r:crow+r, ccol-r:ccol+r] = 0
    fshift = fshift * mask
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    return img_back

def main():
    st.title("Image Processing with Streamlit")
    st.write("Upload an image and apply various image processing techniques.")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        img = read_image(uploaded_file)
        st.subheader("Original Image")
        st.image(opencv_to_pil(img), use_column_width=True)

        st.subheader("Select Processing Technique")
        process_type = st.radio(
            "Choose a technique:",
            ("Convolution", "Zero Padding", "Filter", "Fourier Transform", "Reduce Periodic Noise")
        )

        if process_type == "Convolution":
            kernel_type = st.selectbox("Select kernel type:", ["average", "sharpen", "edge"])
            if st.button("Apply Convolution"):
                result = apply_convolution(img, kernel_type)
                st.subheader("Convolution Result")
                st.image(opencv_to_pil(result), use_column_width=True)

        elif process_type == "Zero Padding":
            padding_size = st.slider("Select padding size:", 10, 50, 20)
            if st.button("Apply Zero Padding"):
                result = apply_zero_padding(img, padding_size)
                st.subheader("Zero Padding Result")
                st.image(opencv_to_pil(result), use_column_width=True)

        elif process_type == "Filter":
            filter_type = st.selectbox("Select filter type:", ["low", "high", "band"])
            if st.button("Apply Filter"):
                result = apply_filter(img, filter_type)
                st.subheader("Filter Result")
                st.image(opencv_to_pil(result), use_column_width=True)

        elif process_type == "Fourier Transform":
            if st.button("Apply Fourier Transform"):
                result = apply_fourier_transform(img)
                st.subheader("Fourier Transform Result")
                st.image(opencv_to_pil(result), use_column_width=True)

        elif process_type == "Reduce Periodic Noise":
            if st.button("Reduce Periodic Noise"):
                result = reduce_periodic_noise(img)
                st.subheader("Noise Reduction Result")
                st.image(opencv_to_pil(result), use_column_width=True)

if __name__ == "__main__":
    main()