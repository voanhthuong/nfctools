import tkinter as ttk
from tkinter import messagebox

def add_numbers():
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        result = num1 + num2
        result_entry.delete(0, ttk.END)  # Xóa nội dung cũ của ô kết quả
        result_entry.insert(0, str(result))  # Hiển thị kết quả trong ô kết quả
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")

# Tạo cửa sổ chính
window = ttk.Tk()
window.title("Máy tính cộng đơn giản")

# Nhãn và ô nhập cho số thứ nhất
label1 = ttk.Label(window, text="Số thứ nhất:")
label1.pack()
entry1 = ttk.Entry(window)
entry1.pack()

# Nhãn và ô nhập cho số thứ hai
label2 = ttk.Label(window, text="Số thứ hai:")
label2.pack()
entry2 = ttk.Entry(window)
entry2.pack()

# Nút để tính phép cộng
button_add = ttk.Button(window, text="Cộng", command=add_numbers)
button_add.pack()

# Nhãn và ô trống để hiển thị kết quả
label_result = ttk.Label(window, text="Kết quả:")
label_result.pack()
result_entry = ttk.Entry(window)
result_entry.pack()

# Chạy vòng lặp chính của giao diện
window.mainloop()
