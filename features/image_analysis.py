import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt

def generate_freeman_chain_code(contour):
    chain_code = []
    if len(contour) < 2:
        return chain_code
    directions = {
        (1, 0): 0, (1, 1): 1, (0, 1): 2, (-1, 1): 3,
        (-1, 0): 4, (-1, -1): 5, (0, -1): 6, (1, -1): 7
    }
    for i in range(len(contour)):
        p1 = contour[i][0]
        p2 = contour[(i + 1) % len(contour)][0]
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        norm_dx = np.sign(dx)
        norm_dy = np.sign(dy)
        code = directions.get((norm_dx, norm_dy))
        if code is not None:
            chain_code.append(code)
    return chain_code

def process_edge_detection(img, low_threshold, high_threshold):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, low_threshold, high_threshold)
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    ax1.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    ax1.set_title('Original Image')
    ax1.axis('off')
    
    ax2.imshow(blurred, cmap='gray')
    ax2.set_title('Grayscale + Gaussian Blur')
    ax2.axis('off')
    
    ax3.imshow(edges, cmap='gray')
    ax3.set_title(f'Canny Edges (Th={low_threshold},{high_threshold})')
    ax3.axis('off')
    
    plt.tight_layout()
    return fig

def process_freeman_chain(img_path):
    gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    _, binary_img = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    chain_code_str = "No contours found."
    
    axs[0, 0].imshow(gray, cmap='gray')
    axs[0, 0].set_title('Grayscale Image')
    axs[0, 0].axis('off')
    
    axs[0, 1].imshow(binary_img, cmap='gray')
    axs[0, 1].set_title('Binary Image')
    axs[0, 1].axis('off')
    
    img_contour_display = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(img_contour_display, [largest_contour], -1, (0, 255, 0), 1)
        chain_code_result = generate_freeman_chain_code(largest_contour)
        
        max_line_len = 70
        wrapped_code = ""
        current_line_len = 0
        for i, code_str in enumerate(map(str, chain_code_result)):
            item = code_str + (", " if i < len(chain_code_result) - 1 else "")
            if current_line_len + len(item) > max_line_len:
                wrapped_code += "\n"
                current_line_len = 0
            wrapped_code += item
            current_line_len += len(item)
        
        chain_code_str = (
            f"Total Contours: {len(contours)}\n"
            f"Chain Code Length: {len(chain_code_result)}\n"
            f"{wrapped_code}"
        )
    
    img_rgb_display = cv2.cvtColor(img_contour_display, cv2.COLOR_BGR2RGB)
    axs[1, 0].imshow(img_rgb_display)
    axs[1, 0].set_title('Largest Contour')
    axs[1, 0].axis('off')
    
    axs[1, 1].axis('off')
    axs[1, 1].text(0.05, 0.95, chain_code_str, ha='left', va='top', fontsize=9, wrap=True)
    axs[1, 1].set_title('Freeman Chain Code')
    
    plt.tight_layout(pad=1.5)
    plt.suptitle("Freeman Chain Code Analysis", fontsize=16)
    plt.subplots_adjust(top=0.92)
    
    return fig

def process_integral_projection(img_path):
    gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    _, binary_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    binary_norm = binary_img / 255.0
    horizontal_projection = np.sum(binary_norm, axis=0)
    vertical_projection = np.sum(binary_norm, axis=1)
    
    height, width = binary_norm.shape
    fig = plt.figure(figsize=(10, 8))
    gs = fig.add_gridspec(2, 2, width_ratios=(4, 1), height_ratios=(1, 4),
                          left=0.1, right=0.9, bottom=0.1, top=0.9,
                          wspace=0.05, hspace=0.05)
    
    ax_img = fig.add_subplot(gs[1, 0])
    ax_img.imshow(binary_norm, cmap='gray')
    ax_img.set_title('Binary Image')
    ax_img.set_xlabel('Column Index')
    ax_img.set_ylabel('Row Index')
    
    ax_hproj = fig.add_subplot(gs[0, 0], sharex=ax_img)
    ax_hproj.plot(np.arange(width), horizontal_projection)
    ax_hproj.set_title('Horizontal Projection')
    ax_hproj.set_ylabel('Pixel Sum')
    plt.setp(ax_hproj.get_xticklabels(), visible=False)
    
    ax_vproj = fig.add_subplot(gs[1, 1], sharey=ax_img)
    ax_vproj.plot(vertical_projection, np.arange(height))
    ax_vproj.set_title('Vertical Projection')
    ax_vproj.set_xlabel('Pixel Sum')
    ax_vproj.invert_yaxis()
    plt.setp(ax_vproj.get_yticklabels(), visible=False)
    
    plt.suptitle("Integral Projection Analysis", fontsize=14)
    
    return fig

def main():
    st.title("Image Processing Analysis")
    st.write("Upload an image to perform Edge Detection, Freeman Chain Code Analysis, and Integral Projection.")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])

    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        temp_img_path = "temp_image.png"
        cv2.imwrite(temp_img_path, img)
        
        st.header("Edge Detection")
        low_threshold = st.slider("Low Threshold", 0, 255, 50)
        high_threshold = st.slider("High Threshold", 0, 255, 150)
        edge_fig = process_edge_detection(img, low_threshold, high_threshold)
        st.pyplot(edge_fig)
        
        st.header("Freeman Chain Code Analysis")
        freeman_fig = process_freeman_chain(temp_img_path)
        st.pyplot(freeman_fig)
        
        st.header("Integral Projection Analysis")
        proj_fig = process_integral_projection(temp_img_path)
        st.pyplot(proj_fig)

if __name__ == "__main__":
    main()