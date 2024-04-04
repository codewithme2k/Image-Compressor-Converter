import tkinter as tk
from tkinter import filedialog, messagebox, Label, simpledialog
from PIL import Image
import os
import threading

def compress_image(image_path, output_path, quality=20):
    img = Image.open(image_path)
    img.save(output_path, quality=quality)

def convert_to_webp(image_path, output_path):
    img = Image.open(image_path)
    img.save(output_path, 'webp')

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def compress_images_in_folder(folder_path, output_folder="compressed", quality=20):
    output_dir = os.path.join(folder_path, output_folder)
    ensure_dir(output_dir)
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                original_image_path = os.path.join(root, file)
                compressed_image_path = os.path.join(output_dir, file)
                compress_image(original_image_path, compressed_image_path, quality=quality)

def convert_images_in_folder_to_webp(folder_path, output_folder="webp_converted"):
    output_dir = os.path.join(folder_path, output_folder)
    ensure_dir(output_dir)
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                original_image_path = os.path.join(root, file)
                file_without_extension, _ = os.path.splitext(file)
                webp_image_path = os.path.join(output_dir, file_without_extension + '.webp')
                convert_to_webp(original_image_path, webp_image_path)

def process_images(folder_path, quality, update_status):
    try:
        update_status("Đang nén ảnh...")
        compress_images_in_folder(folder_path, quality=quality)
        update_status("Đang chuyển đổi sang WebP...")
        convert_images_in_folder_to_webp(folder_path)
        update_status("Hoàn thành!")
    finally:
        messagebox.showinfo("Hoàn thành", "Tất cả ảnh đã được nén và chuyển đổi.")
        update_status("")

def start_processing(folder_path, quality, status_label):
    update_status = lambda text: status_label.config(text=text)
    threading.Thread(target=process_images, args=(folder_path, quality, update_status), daemon=True).start()

def select_folder_and_process():
    folder_path = filedialog.askdirectory()
    if folder_path:
        quality = simpledialog.askinteger("Chất lượng nén", "Nhập chất lượng nén (1-100):", minvalue=1, maxvalue=100)
        if quality is not None:  # Kiểm tra xem người dùng đã nhập chất lượng hay không
            start_processing(folder_path, quality, status_label)

app = tk.Tk()
app.title("Image Compressor & Converter")
app.geometry("400x200")

frame = tk.Frame(app)
frame.pack(padx=10, pady=10)

btn_select_folder = tk.Button(frame, text="Chọn thư mục và xử lý", command=select_folder_and_process)
btn_select_folder.pack(side=tk.TOP, pady=5)

status_label = Label(frame, text="")
status_label.pack(side=tk.TOP, pady=5)

app.mainloop()
