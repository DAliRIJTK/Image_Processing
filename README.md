# Image Processing

Aplikasi modular berbasis **Streamlit** untuk berbagai tugas pemrosesan citra, termasuk pembuatan dataset wajah, teknik pengolahan citra, analisis citra, analisis kompresi, dan konversi ruang warna.

## Daftar Isi

1. [Ringkasan](#ringkasan)
2. [Fitur](#fitur)
3. [Struktur Proyek](#struktur-proyek)
4. [Prasyarat](#prasyarat)
5. [Instalasi](#instalasi)
6. [Menjalankan Aplikasi](#menjalankan-aplikasi)
7. [Penggunaan](#penggunaan)
8. [Pemecahan Masalah](#pemecahan-masalah)

## Ringkasan

**Image Processing Suite** adalah aplikasi berbasis web menggunakan Streamlit dan OpenCV untuk melakukan berbagai tugas pengolahan citra. Antarmuka interaktif memungkinkan navigasi melalui sidebar ke lima fitur utama yang masing-masing dibangun sebagai modul terpisah.

## Fitur

1. **Penambahan Dataset Wajah**:

   * Mengambil gambar wajah dari webcam dan menyimpannya ke folder `dataset/<nama_person>`.
   * Deteksi wajah menggunakan Haar Cascade Classifier dari OpenCV.
   * Maksimal 20 gambar per orang.

2. **Teknik Pengolahan Citra**:

   * Aplikasi konvolusi (average, sharpen, edge), zero padding, filter (low-pass, high-pass, band-pass), transformasi Fourier, dan reduksi noise periodik pada gambar yang diunggah.

3. **Analisis Citra**:

   * Deteksi tepi (Canny), analisis kode rantai Freeman, dan proyeksi integral.
   * Menampilkan hasil dalam bentuk visual menggunakan Matplotlib.

4. **Analisis Kompresi Citra**:

   * Menganalisis pengaruh kompresi JPEG dan PNG terhadap ukuran file, PSNR, dan SSIM.
   * Menyediakan gambar pembanding, tabel, dan grafik.

5. **Konversi Ruang Warna**:

   * Konversi gambar ke berbagai ruang warna: RGB, XYZ, Lab, YCbCr, YIQ, YUV, HSI, Luv.
   * Menampilkan hasil konversi beserta komponen channel-nya.

## Struktur Proyek

```
image_processing_suite/
├── main.py                   # Aplikasi utama Streamlit
├── features/                 # Direktori modul fitur
│   ├── face_dataset_addition.py
│   ├── image_processing_techniques.py
│   ├── image_analysis.py
│   ├── image_compression_analysis.py
│   ├── color_space_conversion.py
├── requirements.txt          # Dependensi Python
└── dataset/                  # Folder dataset wajah (dibuat otomatis)
```

## Prasyarat

* **Python**: Versi 3.8 ke atas.
* **Webcam**: Diperlukan untuk fitur dataset wajah.
* **optipng** (opsional): Untuk optimasi kompresi PNG.
* **Dependensi Sistem**: Pastikan OpenCV dapat digunakan (contoh: `libopencv-dev` di Ubuntu).

## Instalasi

1. **Kloning atau Siapkan Proyek**:

   ```
   git clone <repository-url>
   cd image_processing_suite
   ```

2. **Aktifkan Virtual Environment** (opsional tapi disarankan):

   ```
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Instalasi Dependensi Python**:
   Isi file `requirements.txt`:

   ```
   streamlit==1.38.0
   opencv-python-headless==4.10.0.84
   numpy==1.26.4
   scikit-image==0.24.0
   matplotlib==3.9.2
   pandas==2.2.2
   pillow==10.4.0
   ```

   Lalu instal:

   ```
   pip install -r requirements.txt
   ```

4. **Instalasi Dependensi Sistem** (jika perlu):

   * **Ubuntu/Debian**:

     ```
     sudo apt-get install libopencv-dev optipng
     ```
   * **macOS**:

     ```
     brew install optipng
     ```
   * **Windows**:

     * Unduh optipng dari [http://optipng.sourceforge.net/](http://optipng.sourceforge.net/).
     * Tambahkan ke PATH sistem.
     * Verifikasi:

       ```
       optipng --version
       ```

5. **Izin Folder**:

   ```
   chmod -R u+w .
   ```

## Menjalankan Aplikasi

1. Buka terminal:

   ```
   cd image_processing_suite
   ```
2. Jalankan aplikasi Streamlit:

   ```
   streamlit run main.py
   ```
3. Akses di browser: `http://localhost:8501`

## Penggunaan

### Navigasi:

Gunakan sidebar di sisi kiri untuk memilih fitur.

### Panduan Tiap Fitur:

* **Penambahan Dataset Wajah**:

  * Masukkan nama orang.
  * Klik "Tambahkan Wajah Baru".
  * Kamera akan menangkap 20 gambar wajah ke dalam `dataset/<nama>/`.

* **Teknik Pengolahan Citra**:

  * Unggah gambar JPEG atau PNG.
  * Pilih metode dan parameter.
  * Tampilkan hasil setelah diproses.

* **Analisis Citra**:

  * Unggah gambar.
  * Atur parameter (misal Canny Threshold).
  * Lihat visualisasi hasil analisis.

* **Analisis Kompresi**:

  * Unggah gambar.
  * Bandingkan hasil kompresi JPEG vs PNG.
  * Tampilkan nilai PSNR, SSIM, dan ukuran file.

* **Konversi Warna**:

  * Unggah gambar.
  * Pilih ruang warna.
  * Lihat hasil konversi dan channel-nya.

## Pemecahan Masalah

* **Webcam Tidak Terdeteksi**:

  * Pastikan webcam tidak sedang digunakan aplikasi lain.
  * Coba ganti device index: `cv2.VideoCapture(1)`.
  * Periksa izin akses webcam di sistem Anda.

* **Haar Cascade Tidak Ditemukan**:

  * Reinstall OpenCV:

    ```
    pip uninstall opencv-python-headless
    pip install opencv-python-headless==4.10.0.84
    ```
  * Pastikan file cascade tersedia:

    ```python
    import cv2
    print(cv2.data.haarcascades)
    ```

* **optipng Tidak Ditemukan**:

  * Instal sesuai sistem operasi.

* **Error Izin (Permission Denied)**:

  ```
  chmod -R u+w .
  ```

* **Error Import atau File Tidak Ditemukan**:

  * Pastikan semua file fitur berada di folder `features`.
  * Cek ulang import di `main.py`.

* **Masalah UI Streamlit**:

  * Bersihkan cache:

    ```
    streamlit cache clear
    ```

* **Error Pemrosesan Gambar**:

  * Pastikan gambar valid (JPEG/PNG).
  * SSIM bisa gagal untuk gambar kecil – aplikasi akan menangani ini otomatis.

---

*Terakhir diperbarui: 22 Juni 2025*

---