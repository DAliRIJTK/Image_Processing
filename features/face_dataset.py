import streamlit as st
import cv2
import os
import numpy as np
import time

def detect_faces(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, 
        scaleFactor=1.1, 
        minNeighbors=5, 
        minSize=(30, 30)
    )
    return faces

def main():
    st.title("Tambah Wajah Baru ke Dataset")
    new_person = st.text_input("Masukkan nama orang baru:")
    capture = st.button("Tambahkan Wajah Baru")

    if capture:
        if not new_person:
            st.warning("Silakan masukkan nama orang baru.")
        else:
            save_path = os.path.join('dataset', new_person)
            
            if not os.path.exists('dataset'):
                os.makedirs('dataset')
                st.info("Folder 'dataset' telah dibuat.")
            
            if not os.path.exists(save_path):
                os.makedirs(save_path)
                st.success(f"Folder untuk {new_person} telah dibuat.")
                
                cap = cv2.VideoCapture(0)
                if not cap.isOpened():
                    st.error("Tidak dapat membuka webcam. Pastikan webcam terhubung dan tidak digunakan oleh aplikasi lain.")
                else:
                    num_images = 0
                    max_images = 20

                    frame_placeholder = st.empty()
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    try:
                        while num_images < max_images:
                            ret, frame = cap.read()
                            if not ret:
                                st.error("Error: Tidak dapat membaca frame dari webcam.")
                                break

                            faces = detect_faces(frame)

                            if len(faces) > 0:
                                for (x, y, w, h) in faces:
                                    face = frame[y:y+h, x:x+w]
                                    img_name = os.path.join(save_path, f"{new_person}_{num_images}.jpg")
                                    cv2.imwrite(img_name, face)
                                    num_images += 1

                                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                    frame_placeholder.image(frame_rgb, channels="RGB", caption=f"Gambar {num_images}/{max_images}")

                                    progress = num_images / max_images
                                    progress_bar.progress(progress)
                                    status_text.text(f"Menyimpan gambar {num_images} dari {max_images}...")

                                    break
                            else:
                                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                frame_placeholder.image(frame_rgb, channels="RGB", caption="Tidak ada wajah terdeteksi.")

                            time.sleep(0.1)

                        st.success(f"{num_images} gambar telah berhasil ditambahkan ke dataset {new_person}.")
                    finally:
                        cap.release()
                        frame_placeholder.empty()
                        progress_bar.empty()
                        status_text.empty()
            else:
                st.warning("Nama sudah ada di dataset. Silakan pilih nama lain atau tambahkan lebih banyak gambar.")

if __name__ == "__main__":
    main()