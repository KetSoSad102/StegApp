# Ứng dụng Giấu Tin An Toàn Trong Ảnh

## Thông tin sinh viên

- Họ tên: Phan Lâm Dũng  
- MSSV: 24520349

## Mô tả

Đây là ứng dụng giúp nhúng dữ liệu vào ảnh và trích xuất dữ liệu từ ảnh, sử dụng công cụ `steghide` và xây dựng giao diện người dùng với `tkinter`.

## Tính năng

- Nhúng dữ liệu vào ảnh (hỗ trợ định dạng JPG, BMP)
- Trích xuất dữ liệu từ ảnh đã nhúng
- Nhập mật khẩu tùy chọn
- Hiển thị ảnh gốc và ảnh sau khi giấu tin
- Xử lý các lỗi: thiếu file, sai mật khẩu, file không hợp lệ

## Công nghệ sử dụng

| Thư viện / Công cụ | Chức năng |
|--------------------|-----------|
| **Python 3**     | Ngôn ngữ lập trình chính |
| **steghide**       | Công cụ giấu và trích xuất dữ liệu trong ảnh qua dòng lệnh |
| **tkinter**        | Tạo giao diện đồ họa (GUI) cho người dùng |
| **subprocess**     | Chạy lệnh hệ thống (ví dụ: gọi lệnh steghide từ Python) |
| **os**             | Kiểm tra sự tồn tại của file, xử lý đường dẫn |
| **shutil**         | Sao chép file ảnh trước khi nhúng dữ liệu |
| **Pillow (PIL)**   | Xử lý và hiển thị ảnh trong giao diện (resize, preview ảnh) |

## Hướng dẫn cài đặt

### Cài đặt thư viện Python
```bash
pip install pillow
```

### Cài đặt steghide
- Ubuntu/Debian:
```bash
sudo apt install steghide
```

- Windows: tải tại https://steghide.sourceforge.net/

## Cách sử dụng

### Chạy chương trình:
```bash
python main.py
```

### Thao tác:

1. Chọn ảnh
2. Chọn file cần giấu
3. Nhập mật khẩu (nếu có)
4. Bấm "Nhúng dữ liệu"
5. Xem kết quả
6. Để trích xuất: chọn ảnh + mật khẩu và chọn nơi lưu file

### Hình ảnh

![image](https://hackmd.io/_uploads/S1zXkUdZxe.png)
![image](https://hackmd.io/_uploads/Skbzl8_Wgl.png)
![image](https://hackmd.io/_uploads/H1rmx8dbgg.png)
