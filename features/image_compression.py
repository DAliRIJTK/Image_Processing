import streamlit as st
import cv2
import os
import numpy as np
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
import io
import tempfile
import subprocess

@st.cache_data
def process_jpeg_compression(img, is_color, original_size_bytes, output_dir, base_filename):
    jpeg_qualities = [95, 75, 50, 25, 10]
    results = []
    min_dim = min(img.shape[:2])
    win_size = min(7, min_dim if min_dim % 2 == 1 else min_dim - 1)
    if win_size < 3:
        win_size = 3

    os.makedirs(output_dir, exist_ok=True)

    for quality in jpeg_qualities:
        jpeg_filename = f'{base_filename}_jpeg_{quality}.jpg'
        jpeg_path = os.path.join(output_dir, jpeg_filename)
        
        img_to_save = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) if is_color else img
        cv2.imwrite(jpeg_path, img_to_save, [cv2.IMWRITE_JPEG_QUALITY, quality])
        compressed_size_bytes = os.path.getsize(jpeg_path)

        img_compressed_bgr = cv2.imread(jpeg_path)
        if img_compressed_bgr is None:
            continue

        img_compressed_cv = cv2.cvtColor(img_compressed_bgr, cv2.COLOR_BGR2RGB) if is_color else cv2.imread(jpeg_path, cv2.IMREAD_GRAYSCALE)
        if img_compressed_cv is None:
            continue

        if img.shape != img_compressed_cv.shape:
            continue

        psnr_value = cv2.PSNR(img, img_compressed_cv)
        try:
            ssim_value = ssim(
                img, img_compressed_cv,
                channel_axis=2 if is_color else None,
                win_size=win_size,
                data_range=img.max() - img.min()
            )
        except ValueError:
            ssim_value = None

        identical = np.array_equal(img, img_compressed_cv)
        results.append({
            'Method': 'JPEG',
            'Quality': quality,
            'FileSize (KB)': compressed_size_bytes / 1024,
            'FileSize Opt (KB)': compressed_size_bytes / 1024,
            'CompressionRatio': original_size_bytes / compressed_size_bytes if compressed_size_bytes > 0 else float('inf'),
            'PSNR (dB)': psnr_value,
            'PSNR Manual': float('inf') if identical else psnr_value,
            'SSIM': ssim_value,
            'Identical': identical
        })

    df_results = pd.DataFrame(results)
    
    cmap_val = None if is_color else 'gray'
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].imshow(img, cmap=cmap_val)
    axes[0].set_title(f'Original ({original_size_bytes / 1024:.2f} KB)')
    axes[0].axis('off')

    img_q95_path = os.path.join(output_dir, f'{base_filename}_jpeg_95.jpg')
    img_q95_bgr = cv2.imread(img_q95_path)
    if img_q95_bgr is not None:
        img_q95_vis = cv2.cvtColor(img_q95_bgr, cv2.COLOR_BGR2RGB) if is_color else cv2.imread(img_q95_path, cv2.IMREAD_GRAYSCALE)
        q95_size = os.path.getsize(img_q95_path)
        axes[1].imshow(img_q95_vis, cmap=cmap_val)
        axes[1].set_title(f'JPEG Q95 ({q95_size / 1024:.2f} KB)')
    else:
        axes[1].set_title('JPEG Q95 (Error)')
    axes[1].axis('off')

    img_q10_path = os.path.join(output_dir, f'{base_filename}_jpeg_10.jpg')
    img_q10_bgr = cv2.imread(img_q10_path)
    if img_q10_bgr is not None:
        img_q10_vis = cv2.cvtColor(img_q10_bgr, cv2.COLOR_BGR2RGB) if is_color else cv2.imread(img_q10_path, cv2.IMREAD_GRAYSCALE)
        q10_size = os.path.getsize(img_q10_path)
        axes[2].imshow(img_q10_vis, cmap=cmap_val)
        axes[2].set_title(f'JPEG Q10 ({q10_size / 1024:.2f} KB)')
    else:
        axes[2].set_title('JPEG Q10 (Error)')
    axes[2].axis('off')

    plt.tight_layout()
    
    graf_dir = os.path.join(output_dir, 'grafik')
    os.makedirs(graf_dir, exist_ok=True)
    
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.set_xlabel('JPEG Quality')
    ax1.set_ylabel('File Size (KB)', color='tab:blue')
    ax1.plot(df_results['Quality'], df_results['FileSize (KB)'], marker='o', label='File Size', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    
    ax2 = ax1.twinx()
    ax2.set_ylabel('PSNR / SSIM', color='tab:green')
    ax2.plot(df_results['Quality'], df_results['PSNR (dB)'], marker='s', label='PSNR', color='tab:green')
    ax2.plot(df_results['Quality'], df_results['SSIM'], marker='^', label='SSIM', color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:green')
    
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    plt.title('JPEG Quality vs File Size, PSNR, and SSIM')
    plt.grid(True)
    
    labels = ['Original'] + [f'JPEG Q{q}' for q in df_results['Quality']]
    file_sizes_kb = [original_size_bytes / 1024] + df_results['FileSize (KB)'].tolist()
    
    fig2, ax3 = plt.subplots(figsize=(10, 6))
    bars = ax3.bar(labels, file_sizes_kb, color='skyblue')
    ax3.set_ylabel('File Size (KB)')
    ax3.set_title('File Size Comparison: Original vs JPEG')
    ax3.set_xticklabels(labels, rotation=45, ha='right')
    
    for bar in bars:
        height = bar.get_height()
        ax3.annotate(f'{height:.1f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
    
    plt.tight_layout()
    
    return df_results, fig, fig1, fig2

@st.cache_data
def process_png_compression(img, is_color, original_size_bytes, output_dir, base_filename):
    png_compression_levels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    results = []
    min_dim = min(img.shape[:2])
    win_size = min(7, min_dim if min_dim % 2 == 1 else min_dim - 1)
    if win_size < 3:
        win_size = 3

    os.makedirs(output_dir, exist_ok=True)

    for level in png_compression_levels:
        png_filename = f'{base_filename}_compressed_level{level}.png'
        png_path = os.path.join(output_dir, png_filename)
        
        img_to_save = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) if is_color else img
        cv2.imwrite(png_path, img_to_save, [cv2.IMWRITE_PNG_COMPRESSION, level])
        png_size_bytes = os.path.getsize(png_path)
        
        try:
            subprocess.run(['optipng', '-o7', png_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            png_size_bytes_opt = os.path.getsize(png_path)
        except (subprocess.CalledProcessError, FileNotFoundError):
            png_size_bytes_opt = png_size_bytes

        img_png_compressed_bgr = cv2.imread(png_path)
        if img_png_compressed_bgr is None:
            continue

        img_png_compressed_cv = cv2.cvtColor(img_png_compressed_bgr, cv2.COLOR_BGR2RGB) if is_color else cv2.imread(png_path, cv2.IMREAD_GRAYSCALE)
        if img_png_compressed_cv is None:
            continue

        psnr_png = cv2.PSNR(img, img_png_compressed_cv)
        mse = np.mean((img.astype(float) - img_png_compressed_cv.astype(float)) ** 2)
        psnr_manual = float('inf') if mse == 0 else 20 * np.log10(255.0 / np.sqrt(mse))

        try:
            ssim_png = ssim(
                img, img_png_compressed_cv,
                channel_axis=2 if is_color else None,
                win_size=win_size,
                data_range=img.max() - img.min()
            )
        except ValueError:
            ssim_png = None

        is_identical = np.array_equal(img, img_png_compressed_cv)
        results.append({
            'Method': f'PNG (Level {level})',
            'Quality': 'Lossless',
            'FileSize (KB)': png_size_bytes / 1024,
            'FileSize Opt (KB)': png_size_bytes_opt / 1024,
            'CompressionRatio': original_size_bytes / png_size_bytes if png_size_bytes > 0 else float('inf'),
            'PSNR (dB)': psnr_png if psnr_png != float('inf') else 'Infinity',
            'PSNR Manual': psnr_manual if psnr_manual != float('inf') else 'Infinity',
            'SSIM': ssim_png,
            'Identical': is_identical
        })

    df_results = pd.DataFrame(results)
    df_png = df_results[df_results['Method'].str.contains('PNG')].copy()
    df_png['Level'] = df_png['Method'].str.extract(r'Level (\d)').astype(int)
    df_png.sort_values('Level', inplace=True)

    cmap_val = None if is_color else 'gray'

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].imshow(img, cmap=cmap_val)
    axes[0].set_title(f'Original ({original_size_bytes / 1024:.2f} KB)')
    axes[0].axis('off')

    png_path_vis = os.path.join(output_dir, f'{base_filename}_compressed_level9.png')
    img_png_vis = cv2.imread(png_path_vis)
    img_png_vis = cv2.cvtColor(img_png_vis, cv2.COLOR_BGR2RGB) if is_color else cv2.imread(png_path_vis, cv2.IMREAD_GRAYSCALE)
    if img_png_vis is not None:
        png_size_vis = os.path.getsize(png_path_vis)
        axes[1].imshow(img_png_vis, cmap=cmap_val)
        axes[1].set_title(f'PNG Level 9 ({png_size_vis / 1024:.2f} KB)')
    else:
        axes[1].set_title('PNG Level 9 (Error)')
    axes[1].axis('off')

    plt.tight_layout()

    graf_dir = os.path.join(output_dir, 'grafik')
    os.makedirs(graf_dir, exist_ok=True)

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.set_xlabel('PNG Compression Level')
    ax1.set_ylabel('File Size (KB)', color='tab:blue')
    ax1.plot(df_png['Level'], df_png['FileSize Opt (KB)'], marker='o', label='File Size', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel('PSNR (dB)', color='tab:red')
    ax2.plot(df_png['Level'], df_png['PSNR (dB)'].replace('Infinity', 100).astype(float), marker='s', linestyle='--', color='tab:red', label='PSNR')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    plt.title('PNG Compression vs File Size and PSNR')
    plt.grid(True)

    labels = [f'PNG {int(l)}' for l in df_png['Level']]
    file_sizes = df_png['FileSize Opt (KB)'].tolist()
    labels.insert(0, 'Original')
    file_sizes.insert(0, original_size_bytes / 1024)

    fig2, ax3 = plt.subplots(figsize=(12, 6))
    bars = ax3.bar(labels, file_sizes, color='skyblue')
    ax3.set_ylabel('File Size (KB)')
    ax3.set_title('File Size Comparison')
    ax3.set_xticklabels(labels, rotation=45, ha='right')

    for bar in bars:
        yval = bar.get_height()
        ax3.annotate(f'{yval:.1f}', xy=(bar.get_x() + bar.get_width() / 2, yval),
                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

    plt.tight_layout()

    return df_results, fig, fig1, fig2

def main():
    st.title("Image Compression Analysis")
    st.write("Upload an image to analyze JPEG and PNG compression effects on file size, PSNR, and SSIM.")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])

    if uploaded_file is not None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_img_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_img_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            
            original_size_bytes = os.path.getsize(temp_img_path)
            base_filename = os.path.splitext(os.path.basename(temp_img_path))[0]
            
            img_bgr = cv2.imread(temp_img_path)
            if img_bgr is None:
                st.error(f"Error: Cannot load image from {temp_img_path}")
                return

            is_color = len(img_bgr.shape) == 3
            img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB) if is_color else img_bgr

            st.header("JPEG Compression Analysis")
            jpeg_dir = os.path.join(temp_dir, 'Image_jpeg')
            df_jpeg, jpeg_comp_fig, jpeg_graph1, jpeg_graph2 = process_jpeg_compression(img, is_color, original_size_bytes, jpeg_dir, base_filename)
            
            st.subheader("Comparison Images")
            st.pyplot(jpeg_comp_fig)
            
            st.subheader("Results Table")
            st.dataframe(df_jpeg.style.format({
                'FileSize (KB)': '{:.2f}',
                'FileSize Opt (KB)': '{:.2f}',
                'CompressionRatio': '{:.2f}',
                'PSNR (dB)': '{:.2f}',
                'PSNR Manual': '{:.2f}',
                'SSIM': '{:.4f}'
            }))
            
            st.subheader("Quality vs File Size, PSNR, SSIM")
            st.pyplot(jpeg_graph1)
            
            st.subheader("File Size Comparison")
            st.pyplot(jpeg_graph2)

            st.header("PNG Compression Analysis")
            png_dir = os.path.join(temp_dir, 'Image_png')
            df_png, png_comp_fig, png_graph1, png_graph2 = process_png_compression(img, is_color, original_size_bytes, png_dir, base_filename)
            
            st.subheader("Comparison Images")
            st.pyplot(png_comp_fig)
            
            st.subheader("Results Table")
            st.dataframe(df_png.style.format({
                'FileSize (KB)': '{:.2f}',
                'FileSize Opt (KB)': '{:.2f}',
                'CompressionRatio': '{:.2f}',
                'PSNR (dB)': '{}',
                'PSNR Manual': '{}',
                'SSIM': '{:.4f}'
            }))
            
            st.subheader("Compression Level vs File Size and PSNR")
            st.pyplot(png_graph1)
            
            st.subheader("File Size Comparison")
            st.pyplot(png_graph2)

if __name__ == "__main__":
    main()
