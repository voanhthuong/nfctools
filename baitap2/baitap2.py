import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import psycopg2
from psycopg2 import sql

class ThuVienTruyen:
    def __init__(self, root):
        self.root = root
        self.root.title("Thư viện truyện")

    
        # Biến kết nối cơ sở dữ liệu
        self.db_name = tk.StringVar(value='baitap2')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='171104')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='danhsachtruyen')

        # Biến tìm kiếm
        self.search_keyword = tk.StringVar()

        # Tạo nút đăng nhập ban đầu
        self.login_button = tk.Button(self.root, text="Đăng nhập", command=self.show_connection_frame, bg='green', fg='white')
        self.login_button.pack(pady=100)
        

    def show_connection_frame(self):
        """Ẩn nút đăng nhập và hiện khung kết nối."""
        self.login_button.pack_forget()  # Ẩn nút đăng nhập

        # Tạo khung kết nối
        self.connection_frame = tk.Frame(self.root, bg='white')
        self.connection_frame.pack(pady=10)

        tk.Label(self.connection_frame, text="DB Name:", bg='yellow', fg='black').grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(self.connection_frame, textvariable=self.db_name, bg='white').grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self.connection_frame, text="User:", bg='yellow', fg='black').grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(self.connection_frame, textvariable=self.user, bg='white').grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.connection_frame, text="Password:", bg='yellow', fg='black').grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(self.connection_frame, textvariable=self.password, show="*", bg='white').grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.connection_frame, text="Host:", bg='yellow', fg='black').grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(self.connection_frame, textvariable=self.host, bg='white').grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.connection_frame, text="Port:", bg='yellow', fg='black').grid(row=4, column=0, padx=5, pady=5)
        tk.Entry(self.connection_frame, textvariable=self.port, bg='white').grid(row=4, column=1, padx=5, pady=5)

        tk.Button(self.connection_frame, text="Connect", command=self.connect_db, bg='green', fg='white').grid(row=5, columnspan=2, pady=10)

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Success", "Connected to the database successfully!")
            self.connection_frame.pack_forget()  # Ẩn khung kết nối sau khi kết nối thành công
            self.create_widgets()  # Hiển thị các chức năng chính
        except Exception as e:
            messagebox.showerror("Error", f"Error connecting to the database: {e}")

    def create_widgets(self):
        """Tạo các phần tử GUI sau khi kết nối thành công."""
        self.tentruyen = tk.StringVar()
        self.taptruyen = tk.StringVar()
        self.sotrang = tk.StringVar()
        self.theloai = tk.StringVar()

        # Khung chính chứa input_frame và query_frame
        self.main_frame = tk.Frame(self.root, bg='white')
        self.main_frame.pack(pady=10)

        # Khung nhập liệu cho insert dữ liệu
        self.input_frame = tk.Frame(self.main_frame, bg='white')
        self.input_frame.grid(row=0, column=0, padx=10)  # Đặt ở cột đầu tiên của main_frame

        tk.Label(self.input_frame, text="Tên truyện:", bg='yellow', fg='black').grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(self.input_frame, textvariable=self.tentruyen, bg='white').grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.input_frame, text="Tập truyện:", bg='yellow', fg='black').grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(self.input_frame, textvariable=self.taptruyen, bg='white').grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.input_frame, text="Số trang:", bg='yellow', fg='black').grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(self.input_frame, textvariable=self.sotrang, bg='white').grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.input_frame, text="Thể loại:", bg='yellow', fg='black').grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(self.input_frame, textvariable=self.theloai, bg='white').grid(row=3, column=1, padx=5, pady=5)

        tk.Button(self.input_frame, text="Insert Data", command=self.insert_data, bg='blue', fg='white').grid(row=4, columnspan=2, pady=10)
        
        # Khung truy vấn
        self.query_frame = tk.Frame(self.main_frame, bg='white')
        self.query_frame.grid(row=0, column=1, padx=10)  # Đặt ở cột thứ hai của main_frame

        tk.Label(self.query_frame, text="Thư viện:", bg='yellow', fg='black').grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(self.query_frame, textvariable=self.table_name, bg='white').grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.query_frame, text="Load Data", command=self.load_data, bg='green', fg='white').grid(row=1, columnspan=2, pady=10)

        tk.Label(self.query_frame, text="Search by tên truyện:", bg='yellow', fg='black').grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(self.query_frame, textvariable=self.search_keyword, bg='white').grid(row=2, column=1, padx=5, pady=5)
        tk.Button(self.query_frame, text="Search", command=self.search_data, bg='blue', fg='white').grid(row=3, columnspan=2, pady=10)

        # Khu vực hiển thị dữ liệu
        self.data_display = tk.Text(self.root, height=10, width=100, bg='lightyellow')
        self.data_display.pack(pady=10)

        # Nút đăng xuất
        self.logout_button = tk.Button(self.root, text="Đăng xuất", command=self.logout, bg='red', fg='white')
        self.logout_button.pack(pady=10)



    def load_data(self):
        """Tải dữ liệu từ bảng vào GUI và hiển thị theo cột."""



        try:
            self.data_display.config(state='normal')  # Đặt về trạng thái bình thường
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(query)
            rows = self.cur.fetchall()
            
            # Xóa dữ liệu cũ
            self.data_display.delete(1.0, tk.END)
            
            # Kiểm tra số lượng cột trả về
            if self.cur.description:
                column_count = len(self.cur.description)
                column_names = [desc[0] for desc in self.cur.description]  # Lấy tên cột từ con trỏ
                
                # Độ rộng cố định cho mỗi cột 
                col_width = 20
                
                # Hiển thị tiêu đề các cột với căn giữa
                header = " | ".join(name.center(col_width) for name in column_names) + "\n"
                self.data_display.insert(tk.END, header)
                self.data_display.insert(tk.END, "-" * (len(header) - 1) + "\n")  # Dòng gạch ngang
                
                # Hiển thị dữ liệu với độ rộng cố định cho mỗi cột
                for row in rows:
                    row_data = " | ".join(
                        str(row[i]).rjust(col_width) if i > 0 else str(row[i]).ljust(col_width) 
                        for i in range(column_count)
                    ) + "\n"
                    self.data_display.insert(tk.END, row_data)
            else:
                self.data_display.insert(tk.END, "No data found.\n")
                self.data_display.config(state='disabled')
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")  # Hiển thị thông báo lỗi




    def search_data(self):
        """Tìm kiếm dữ liệu trong bảng theo từ khóa."""
        try:
            search_query = self.search_keyword.get()  # Lấy từ khóa tìm kiếm từ người dùng
            
            if not search_query:  # Kiểm tra nếu từ khóa tìm kiếm trống
                messagebox.showwarning("Warning", "Please enter a search keyword.")
                return
                
            # Truy vấn tìm kiếm trong cơ sở dữ liệu
            query = sql.SQL("SELECT * FROM {} WHERE tentruyen ILIKE %s OR taptruyen ILIKE %s").format(
                sql.Identifier(self.table_name.get())
            )
            self.cur.execute(query, (f"%{search_query}%", f"%{search_query}%"))
            rows = self.cur.fetchall()
            
            # Xóa dữ liệu cũ trong giao diện
            self.data_display.delete(1.0, tk.END)  # Xóa tất cả dữ liệu hiện tại
            
            # Kiểm tra số lượng cột trả về
            if self.cur.description:
                column_count = len(self.cur.description)
                column_names = [desc[0] for desc in self.cur.description]  # Lấy tên cột
                
                # Độ rộng cố định cho mỗi cột (có thể điều chỉnh theo nhu cầu)
                col_width = 20
                
                # Hiển thị tiêu đề cột
                header = " | ".join(name.ljust(col_width) for name in column_names) + "\n"
                self.data_display.insert(tk.END, header)
                self.data_display.insert(tk.END, "-" * (col_width * column_count) + "\n")  # Dòng gạch ngang
                
                # Hiển thị kết quả tìm kiếm
                if rows:  # Kiểm tra nếu có kết quả
                    for row in rows:
                        row_data = " | ".join(str(row[i]).ljust(col_width) for i in range(column_count)) + "\n"
                        self.data_display.insert(tk.END, row_data)
                else:
                    self.data_display.insert(tk.END, "No results found.\n")
            else:
                self.data_display.insert(tk.END, "No results found.\n")  # Không có cột trả về

        except Exception as e:
            messagebox.showerror("Error", f"Error searching data: {e}")  # Hiển thị thông báo lỗi




    def insert_data(self):
        """Chèn dữ liệu vào bảng trong cơ sở dữ liệu."""
        try:
            insert_query = sql.SQL("INSERT INTO {} (tentruyen, taptruyen, sotrang, theloai) VALUES (%s, %s, %s, %s)").format(sql.Identifier(self.table_name.get()))
            data_to_insert = (self.tentruyen.get(), self.taptruyen.get(), self.sotrang.get(), self.theloai.get())
            self.cur.execute(insert_query, data_to_insert)
            self.conn.commit()
            
            messagebox.showinfo("Success", "Data inserted successfully!")  # Hiển thị thông báo thành công
            self.clear_fields()  # Xóa các trường sau khi chèn dữ liệu thành công
            
            self.load_data()  # Gọi hàm load_data để cập nhật hiển thị
        except Exception as e:
            self.conn.rollback()  # Rollback lại giao dịch khi có lỗi
            messagebox.showerror("Error", f"Error inserting data: {e}")  # Hiển thị thông báo lỗi

    def clear_fields(self):
        """Xóa tất cả các trường nhập liệu sau khi chèn dữ liệu."""
        self.tentruyen.set('')
        self.taptruyen.set('')
        self.sotrang.set('')
        self.theloai.set('')

    def on_exit(self):
        """Dọn dẹp trước khi thoát ứng dụng."""
        if self.cur:
            self.cur.close()  # Đóng con trỏ dữ liệu
        if self.conn:
            self.conn.close()   
            
        self.root.quit()  
    def logout(self):
        """Đăng xuất khỏi giao diện chính và quay lại màn hình đăng nhập."""
        # Ẩn tất cả các khung và nút đăng xuất
        if hasattr(self, 'main_frame'):
            self.main_frame.pack_forget()
        if hasattr(self, 'input_frame'):
            self.input_frame.grid_forget()
        if hasattr(self, 'query_frame'):
            self.query_frame.grid_forget()
        if hasattr(self, 'data_display'):
            self.data_display.pack_forget()
        if hasattr(self, 'logout_button'):
            self.logout_button.pack_forget()
        
        # Xóa các trường nhập liệu và từ khóa tìm kiếm
        self.tentruyen.set('')
        self.taptruyen.set('')
        self.sotrang.set('')
        self.theloai.set('')
        self.search_keyword.set('')
        
        # Hiển thị lại nút đăng nhập
        self.login_button.pack(pady=100)


if __name__ == "__main__":
    root = tk.Tk()
    app = ThuVienTruyen(root)
    root.mainloop()
