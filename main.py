import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class SteganographyApp:
    """
    Ứng dụng giấu và trích xuất dữ liệu trong ảnh sử dụng Steghide.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Giấu tin an toàn trong ảnh")

        # Khởi tạo các biến đường dẫn
        self.image_path = ""
        self.data_path = ""
        self.output_path = ""

        # GUI thành phần
        self.create_widgets()

    def create_widgets(self):
        # Chọn ảnh gốc
        tk.Button(self.root, text="Chọn ảnh", command=self.select_image).grid(row=0, column=0, padx=10, pady=10)
        self.image_label = tk.Label(self.root, text="Chưa chọn ảnh")
        self.image_label.grid(row=0, column=1)

        # Chọn file dữ liệu
        tk.Button(self.root, text="Chọn file cần giấu", command=self.select_data).grid(row=1, column=0, padx=10, pady=10)
        self.data_label = tk.Label(self.root, text="Chưa chọn file")
        self.data_label.grid(row=1, column=1)

        # Nhập mật khẩu
        tk.Label(self.root, text="Mật khẩu:").grid(row=2, column=0)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=2, column=1)

        # Nút thực hiện giấu dữ liệu
        tk.Button(self.root, text="Nhúng dữ liệu", command=self.embed_data).grid(row=3, column=0, pady=10)

        # Nút thực hiện trích xuất
        tk.Button(self.root, text="Trích xuất dữ liệu", command=self.extract_data).grid(row=3, column=1, pady=10)

        # Hiển thị ảnh nhúng
        self.image_preview = tk.Label(self.root)
        self.image_preview.grid(row=4, column=0, columnspan=2, pady=10)

    def select_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.bmp *.png")])
        if path:
            self.image_path = path
            self.image_label.config(text=os.path.basename(path))
            self.show_image(path)

    def select_data(self):
        path = filedialog.askopenfilename()
        if path:
            self.data_path = path
            self.data_label.config(text=os.path.basename(path))

    def show_image(self, path):
        try:
            img = Image.open(path)
            img = img.resize((300, 300))
            img = ImageTk.PhotoImage(img)
            self.image_preview.configure(image=img)
            self.image_preview.image = img
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi hiển thị ảnh: {e}")

    def embed_data(self):
        if not self.image_path or not self.data_path:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn ảnh và file dữ liệu.")
            return

        password = self.password_entry.get()
        out_path = os.path.splitext(self.image_path)[0] + "_output.jpg"

        try:
            shutil.copy2(self.image_path, out_path)  # copy ảnh để giữ ảnh gốc

            command = ["steghide", "embed", "-cf", out_path, "-ef", self.data_path]
            if password:
                command += ["-p", password]
            else:
                command += ["-p", ""]  # bắt buộc có -p dù rỗng

            subprocess.run(command, check=True)
            self.show_image(out_path)
            messagebox.showinfo("Thành công", f"Đã nhúng dữ liệu vào ảnh:\n{out_path}")
        except subprocess.CalledProcessError:
            messagebox.showerror("Lỗi", "Không thể nhúng dữ liệu. Kiểm tra mật khẩu hoặc định dạng ảnh.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khác: {e}")

    def extract_data(self):
        if not self.image_path:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn ảnh đã giấu tin.")
            return

        password = self.password_entry.get()
        output_file = filedialog.asksaveasfilename(title="Lưu file trích xuất")

        if not output_file:
            return

        try:
            command = ["steghide", "extract", "-sf", self.image_path, "-xf", output_file]
            if password:
                command += ["-p", password]
            else:
                command += ["-p", ""]

            subprocess.run(command, check=True)
            messagebox.showinfo("Thành công", f"Đã trích xuất dữ liệu:\n{output_file}")
        except subprocess.CalledProcessError:
            messagebox.showerror("Lỗi", "Không thể trích xuất. Sai mật khẩu hoặc ảnh không chứa dữ liệu.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khác: {e}")

# Chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
