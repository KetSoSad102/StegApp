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

        # Khởi tạo các biến để lưu đường dẫn ảnh, file dữ liệu và ảnh đầu ra
        self.image_path = ""
        self.data_path = ""
        self.output_path = ""

        # Tạo giao diện người dùng
        self.create_widgets()

    def create_widgets(self):
        # Nút chọn ảnh gốc
        tk.Button(self.root, text="Chọn ảnh", command=self.select_image).grid(row=0, column=0, padx=10, pady=10)
        self.image_label = tk.Label(self.root, text="Chưa chọn ảnh")
        self.image_label.grid(row=0, column=1)

        # Nút chọn file dữ liệu để giấu
        tk.Button(self.root, text="Chọn file cần giấu", command=self.select_data).grid(row=1, column=0, padx=10, pady=10)
        self.data_label = tk.Label(self.root, text="Chưa chọn file")
        self.data_label.grid(row=1, column=1)

        # Trường nhập mật khẩu
        tk.Label(self.root, text="Mật khẩu:").grid(row=2, column=0)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=2, column=1)

        # Nút để thực hiện giấu dữ liệu
        tk.Button(self.root, text="Nhúng dữ liệu", command=self.embed_data).grid(row=3, column=0, pady=10)

        # Nút để trích xuất dữ liệu
        tk.Button(self.root, text="Trích xuất dữ liệu", command=self.extract_data).grid(row=3, column=1, pady=10)

        # Vùng hiển thị ảnh sau khi nhúng hoặc đã chọn
        self.image_preview = tk.Label(self.root)
        self.image_preview.grid(row=4, column=0, columnspan=2, pady=10)

    def select_image(self):
        # Mở hộp thoại để chọn file ảnh
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.bmp *.png")])
        if path:
            self.image_path = path
            self.image_label.config(text=os.path.basename(path))  # Cập nhật nhãn
            self.show_image(path)  # Hiển thị ảnh xem trước

    def select_data(self):
        # Mở hộp thoại để chọn file dữ liệu cần giấu
        path = filedialog.askopenfilename()
        if path:
            self.data_path = path
            self.data_label.config(text=os.path.basename(path))

    def show_image(self, path):
        try:
            # Hiển thị ảnh kích thước nhỏ 300x300 trong giao diện
            img = Image.open(path)
            img = img.resize((300, 300))
            img = ImageTk.PhotoImage(img)
            self.image_preview.configure(image=img)
            self.image_preview.image = img
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi hiển thị ảnh: {e}")

    def embed_data(self):
        # Kiểm tra xem đã chọn đủ ảnh và file dữ liệu chưa
        if not self.image_path or not self.data_path:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn ảnh và file dữ liệu.")
            return

        password = self.password_entry.get()
        # Tạo tên file đầu ra (copy từ ảnh gốc)
        out_path = os.path.splitext(self.image_path)[0] + "_output.jpg"

        try:
            # Sao chép ảnh gốc để giữ nguyên ảnh ban đầu
            shutil.copy2(self.image_path, out_path)

            # Lệnh steghide để nhúng file
            command = ["steghide", "embed", "-cf", out_path, "-ef", self.data_path]
            if password:
                command += ["-p", password]
            else:
                command += ["-p", ""]  # steghide yêu cầu có -p, kể cả khi rỗng

            # Thực thi lệnh
            subprocess.run(command, check=True)
            self.show_image(out_path)  # Hiển thị ảnh mới sau khi nhúng
            messagebox.showinfo("Thành công", f"Đã nhúng dữ liệu vào ảnh:\n{out_path}")
        except subprocess.CalledProcessError:
            messagebox.showerror("Lỗi", "Không thể nhúng dữ liệu. Kiểm tra mật khẩu hoặc định dạng ảnh.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khác: {e}")

    def extract_data(self):
        # Kiểm tra đã chọn ảnh chứa dữ liệu chưa
        if not self.image_path:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn ảnh đã giấu tin.")
            return

        password = self.password_entry.get()
        # Hộp thoại để chọn vị trí lưu file trích xuất
        output_file = filedialog.asksaveasfilename(title="Lưu file trích xuất")

        if not output_file:
            return  # Người dùng bấm cancel

        try:
            # Lệnh steghide để trích xuất
            command = ["steghide", "extract", "-sf", self.image_path, "-xf", output_file]
            if password:
                command += ["-p", password]
            else:
                command += ["-p", ""]

            # Thực thi lệnh
            subprocess.run(command, check=True)
            messagebox.showinfo("Thành công", f"Đã trích xuất dữ liệu:\n{output_file}")
        except subprocess.CalledProcessError:
            messagebox.showerror("Lỗi", "Không thể trích xuất. Sai mật khẩu hoặc ảnh không chứa dữ liệu.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khác: {e}")

# Khởi chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
