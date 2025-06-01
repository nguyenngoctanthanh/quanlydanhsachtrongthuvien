import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import requests
import json
import os
from datetime import datetime


USERS_FILE = "users.json"
BOOKS_FILE = "books.json"
READERS_FILE = "readers.json"
BORROW_FILE = "borrow.json"


def load_data():
    data = {
        "users": {},
        "books": [],
        "readers": [],
        "borrows": []
    }
    
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            data["users"] = json.load(f)
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, "r") as f:
            data["books"] = json.load(f)
    if os.path.exists(READERS_FILE):
        with open(READERS_FILE, "r") as f:
            data["readers"] = json.load(f)
    if os.path.exists(BORROW_FILE):
        with open(BORROW_FILE, "r") as f:
            data["borrows"] = json.load(f)
    
    return data


def save_data(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data["users"], f, indent=4)
    with open(BOOKS_FILE, "w") as f:
        json.dump(data["books"], f, indent=4)
    with open(READERS_FILE, "w") as f:
        json.dump(data["readers"], f, indent=4)
    with open(BORROW_FILE, "w") as f:
        json.dump(data["borrows"], f, indent=4)

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Danh Sách Sách Thư viện")
        self.root.geometry("1000x700")
        
        self.data = load_data()
        self.current_user = None
        
        self.setup_login_screen()
    
    
    def setup_login_screen(self):
        self.clear_screen()
        
        
        try:
            self.bg_image = Image.open("bg3.jpg")
            self.bg_image = self.bg_image.resize((1300, 800), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            tk.Label(self.root, image=self.bg_photo).place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            messagebox.showerror("Error", "Không tìm thấy hình nền bg3.jpg")
        
        
        login_frame = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        login_frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=400)
        
        tk.Label(login_frame, text="ĐĂNG NHẬP", font=("Arial", 16, "bold"), bg="white").pack(pady=15)
        
        
        tk.Label(login_frame, text="Mã số:", font=("Arial", 12), bg="white").pack()
        self.username_entry = tk.Entry(login_frame, font=("Arial", 12))
        self.username_entry.pack(pady=5)
        
        
        tk.Label(login_frame, text="Mật khẩu:", font=("Arial", 12), bg="white").pack()
        self.password_entry = tk.Entry(login_frame, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5)
        
        
        self.show_pass_var = tk.BooleanVar()
        tk.Checkbutton(login_frame, text="Hiển thị mật khẩu", variable=self.show_pass_var, 
                      command=self.toggle_password, bg="white").pack()
        
        
        tk.Label(login_frame, text="Vai trò:", font=("Arial", 12), bg="white").pack(pady=5)
        self.role_var = tk.StringVar()
        ttk.Combobox(login_frame, textvariable=self.role_var, 
                    values=["Admin", "Thủ thư", "Độc giả"], state="readonly").pack()
        self.role_var.set("Thủ thư")
        
        
        tk.Button(login_frame, text="Đăng nhập", bg="#4CAF50", fg="white", 
                 font=("Arial", 12), command=self.handle_login).pack(pady=15)
        
        # Register button
        tk.Button(login_frame, text="Đăng ký", bg="#2196F3", fg="white", 
                 font=("Arial", 10), command=self.show_register_window).pack()
    
    def toggle_password(self):
        if self.show_pass_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
    
    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()
        
        if username in self.data["users"]:
            user = self.data["users"][username]
            if user["password"] == password and user["role"] == role.lower():
                self.current_user = user
                messagebox.showinfo("Thành công", "Đăng nhập thành công!")
                
                if role == "Admin":
                    self.show_admin_dashboard()
                elif role == "Thủ thư":
                    self.show_librarian_dashboard()
                else:
                    self.show_reader_dashboard()
            else:
                messagebox.showerror("Lỗi", "Sai mật khẩu hoặc vai trò!")
        else:
            messagebox.showerror("Lỗi", "Người dùng không tồn tại!")

    def show_register_window(self):
        register_window = tk.Toplevel(self.root)
        register_window.title("Đăng ký tài khoản")
        register_window.geometry("1300x600")
        register_window.configure(bg="#E3F2FD")

    
        try:
            bg_image = Image.open("bg3.jpg")
            bg_image = bg_image.resize((1300, 600), Image.Resampling.LANCZOS)
            bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(register_window, image=bg_photo)
            bg_label.image = bg_photo
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print("Không tìm thấy ảnh nền 'bg3.jpg'. Bỏ qua hình nền.")

        
        register_frame = tk.Frame(register_window, bg="white", bd=2, relief="groove")
        register_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=500)

        tk.Label(register_frame, text="ĐĂNG KÝ TÀI KHOẢN", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        
        tk.Label(register_frame, text="Mã số:", font=("Arial", 12), bg="white").pack()
        username_entry = tk.Entry(register_frame, font=("Arial", 12))
        username_entry.pack(pady=5)

        
        tk.Label(register_frame, text="Mật khẩu:", font=("Arial", 12), bg="white").pack()
        password_entry = tk.Entry(register_frame, font=("Arial", 12), show="*")
        password_entry.pack(pady=5)

        
        tk.Label(register_frame, text="Họ tên:", font=("Arial", 12), bg="white").pack()
        fullname_entry = tk.Entry(register_frame, font=("Arial", 12))
        fullname_entry.pack(pady=5)

        
        tk.Label(register_frame, text="Email:", font=("Arial", 12), bg="white").pack()
        email_entry = tk.Entry(register_frame, font=("Arial", 12))
        email_entry.pack(pady=5)

        
        tk.Label(register_frame, text="Số ĐT:", font=("Arial", 12), bg="white").pack()
        phone_entry = tk.Entry(register_frame, font=("Arial", 12))
        phone_entry.pack(pady=5)

        
        tk.Label(register_frame, text="Địa chỉ:", font=("Arial", 12), bg="white").pack()
        address_entry = tk.Entry(register_frame, font=("Arial", 12))
        address_entry.pack(pady=5)

        
        tk.Label(register_frame, text="Vai trò:", font=("Arial", 12), bg="white").pack(pady=5)
        role_var = tk.StringVar()
        role_combo = ttk.Combobox(register_frame, textvariable=role_var, 
                                values=["Admin", "Thủ thư", "Độc giả"], state="readonly")
        role_combo.pack()
        role_var.set("Thủ thư")

        
        def register():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            fullname = fullname_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()
            address = address_entry.get().strip()
            role = role_var.get().lower()

            if not username or not password or not fullname or not email or not phone or not address:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
                return

            if username in self.data["users"]:
                messagebox.showerror("Lỗi", "Tài khoản đã tồn tại!")
                return

            self.data["users"][username] = {
                "password": password,
                "role": role,
                "fullname": fullname,
                "email": email,
                "phone": phone
            }

            if role == "độc giả":
                self.data["readers"].append({
                    "id": username,
                    "fullname": fullname,
                    "email": email,
                    "phone": phone,
                    "address": address,
                    "borrowed_books": []
                })

            save_data(self.data)
            messagebox.showinfo("Thành công", "Đăng ký thành công!")
            register_window.destroy()

        tk.Button(register_frame, text="Đăng ký", bg="#4CAF50", fg="white", 
                font=("Arial", 12), command=register).pack(pady=15)


    
    
    def show_admin_dashboard(self):
        self.clear_screen()
        
        # Header
        header_frame = tk.Frame(self.root, bg="#333", height=50)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text="QUẢN LÝ THƯ VIỆN - ADMIN", fg="white", bg="#333", 
               font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=20)
        
        tk.Button(header_frame, text="Đăng xuất", bg="#f44336", fg="white", 
                command=self.setup_login_screen).pack(side=tk.RIGHT, padx=20)
        
        
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        
        sidebar = tk.Frame(main_frame, bg="#f1f1f1", width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        buttons = [
            ("Quản lý sách", self.show_book_management),
            ("Quản lý độc giả", self.show_reader_management),
            ("Quản lý mượn/trả", self.show_borrow_management),
            ("Thống kê báo cáo", self.show_statistics),
            ("Quản lý tài khoản", self.show_account_management)
        ]
        
        for text, command in buttons:
            tk.Button(sidebar, text=text, width=20, anchor="w", 
                    command=command).pack(pady=5, padx=5, ipady=5)
        
        
        self.content_frame = tk.Frame(main_frame, bg="white")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        
        self.show_book_management()
    
    def show_book_management(self):
        self.clear_content()
        
        
        search_frame = tk.Frame(self.content_frame)
        search_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(search_frame, text="Tìm kiếm sách:").pack(side=tk.LEFT)
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        search_by = ttk.Combobox(search_frame, values=["Tên sách", "Tác giả", "Thể loại", "Nhà xuất bản"], width=15)
        search_by.pack(side=tk.LEFT, padx=5)
        search_by.set("Tên sách")
        
        def search_books():
            keyword = search_entry.get().lower()
            search_type = search_by.get()
            
            filtered_books = []
            for book in self.data["books"]:
                if search_type == "Tên sách" and keyword in book["title"].lower():
                    filtered_books.append(book)
                elif search_type == "Tác giả" and keyword in book["author"].lower():
                    filtered_books.append(book)
                elif search_type == "Thể loại" and keyword in book["category"].lower():
                    filtered_books.append(book)
                elif search_type == "Nhà xuất bản" and keyword in book["publisher"].lower():
                    filtered_books.append(book)
            
            
            for item in tree.get_children():
                tree.delete(item)
            
            for book in filtered_books:
                tree.insert("", tk.END, values=(
                    book["id"], book["title"], book["author"], 
                    book["category"], book["quantity"], 
                    book["year"], book["publisher"]
                ))
        
        tk.Button(search_frame, text="Tìm kiếm", command=search_books).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Làm mới", command=lambda: self.update_book_tree(tree)).pack(side=tk.LEFT)
        
        
        tk.Button(search_frame, text="+ Thêm sách", bg="#4CAF50", fg="white", 
                command=self.show_add_book_window).pack(side=tk.RIGHT)
        
        
        columns = ("ID", "Tên sách", "Tác giả", "Thể loại", "Số lượng", "Năm XB", "Nhà XB")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        
        self.update_book_tree(tree)
        
        
        btn_frame = tk.Frame(self.content_frame)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Sửa thông tin", bg="#2196F3", fg="white", 
                command=lambda: self.show_edit_book_window(tree)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Xóa sách", bg="#f44336", fg="white", 
                command=lambda: self.delete_book(tree)).pack(side=tk.LEFT, padx=5)
    
    def update_book_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        
        for book in self.data["books"]:
            tree.insert("", tk.END, values=(
                book["id"], book["title"], book["author"], 
                book["category"], book["quantity"], 
                book["year"], book["publisher"]
            ))
    
    def show_add_book_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Thêm sách mới")
        add_window.geometry("400x500")
        
        tk.Label(add_window, text="THÊM SÁCH MỚI", font=("Arial", 14, "bold")).pack(pady=10)
        
        fields = [
            ("Mã sách:", "id"),
            ("Tên sách:", "title"),
            ("Tác giả:", "author"),
            ("Thể loại:", "category"),
            ("Số lượng:", "quantity"),
            ("Năm xuất bản:", "year"),
            ("Nhà xuất bản:", "publisher")
        ]
        
        entries = {}
        for text, field in fields:
            frame = tk.Frame(add_window)
            frame.pack(pady=5)
            
            tk.Label(frame, text=text, width=15, anchor="w").pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=30)
            entry.pack(side=tk.LEFT)
            entries[field] = entry
        
        def add_book():
            new_book = {}
            for field, entry in entries.items():
                value = entry.get()
                if field == "quantity":
                    try:
                        value = int(value)
                    except ValueError:
                        messagebox.showerror("Lỗi", "Số lượng phải là số!")
                        return
                new_book[field] = value
            
            
            for book in self.data["books"]:
                if book["id"] == new_book["id"]:
                    messagebox.showerror("Lỗi", "Mã sách đã tồn tại!")
                    return
            
            self.data["books"].append(new_book)
            save_data(self.data)
            messagebox.showinfo("Thành công", "Thêm sách thành công!")
            add_window.destroy()
        
        tk.Button(add_window, text="Thêm sách", bg="#4CAF50", fg="white", 
                command=add_book).pack(pady=20)
    
    def show_edit_book_window(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Lỗi", "Vui lòng chọn sách cần sửa!")
            return
        
        book_id = tree.item(selected[0])["values"][0]
        book = next((b for b in self.data["books"] if b["id"] == book_id), None)
        
        if not book:
            messagebox.showerror("Lỗi", "Không tìm thấy sách!")
            return
        
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Sửa thông tin sách")
        edit_window.geometry("400x500")
        
        tk.Label(edit_window, text="SỬA THÔNG TIN SÁCH", font=("Arial", 14, "bold")).pack(pady=10)
        
        fields = [
            ("Mã sách:", "id", False),
            ("Tên sách:", "title", True),
            ("Tác giả:", "author", True),
            ("Thể loại:", "category", True),
            ("Số lượng:", "quantity", True),
            ("Năm xuất bản:", "year", True),
            ("Nhà xuất bản:", "publisher", True)
        ]
        
        entries = {}
        for text, field, editable in fields:
            frame = tk.Frame(edit_window)
            frame.pack(pady=5)
            
            tk.Label(frame, text=text, width=15, anchor="w").pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=30)
            entry.insert(0, book[field])
            if not editable:
                entry.config(state="readonly")
            entry.pack(side=tk.LEFT)
            entries[field] = entry
        
        def update_book():
            updated_book = book.copy()
            for field, entry in entries.items():
                value = entry.get()
                if field == "quantity":
                    try:
                        value = int(value)
                    except ValueError:
                        messagebox.showerror("Lỗi", "Số lượng phải là số!")
                        return
                updated_book[field] = value
            
            # Update book in data
            for i, b in enumerate(self.data["books"]):
                if b["id"] == book["id"]:
                    self.data["books"][i] = updated_book
                    break
            
            save_data(self.data)
            messagebox.showinfo("Thành công", "Cập nhật sách thành công!")
            edit_window.destroy()
            self.update_book_tree(tree)
        
        tk.Button(edit_window, text="Cập nhật", bg="#4CAF50", fg="white", 
                command=update_book).pack(pady=20)
    
    def delete_book(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Lỗi", "Vui lòng chọn sách cần xóa!")
            return
        
        book_id = tree.item(selected[0])["values"][0]
        
        
        for borrow in self.data["borrows"]:
            if borrow["book_id"] == book_id and borrow["return_date"] == "":
                messagebox.showerror("Lỗi", "Sách đang được mượn, không thể xóa!")
                return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa sách này?"):
            self.data["books"] = [b for b in self.data["books"] if b["id"] != book_id]
            save_data(self.data)
            messagebox.showinfo("Thành công", "Xóa sách thành công!")
            self.update_book_tree(tree)
    
    
    def show_reader_management(self):
        self.clear_content()
        
        # Search frame
        search_frame = tk.Frame(self.content_frame)
        search_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(search_frame, text="Tìm kiếm độc giả:").pack(side=tk.LEFT)
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        search_by = ttk.Combobox(search_frame, values=["Mã số", "Họ tên", "Email", "SĐT"], width=15)
        search_by.pack(side=tk.LEFT, padx=5)
        search_by.set("Mã số")
        
        def search_readers():
            keyword = search_entry.get().lower()
            search_type = search_by.get()
            
            filtered_readers = []
            for reader in self.data["readers"]:
                if search_type == "Mã số" and keyword in reader["id"].lower():
                    filtered_readers.append(reader)
                elif search_type == "Họ tên" and keyword in reader["fullname"].lower():
                    filtered_readers.append(reader)
                elif search_type == "Email" and keyword in reader["email"].lower():
                    filtered_readers.append(reader)
                elif search_type == "SĐT" and keyword in reader["phone"].lower():
                    filtered_readers.append(reader)
            
            # Update treeview
            for item in tree.get_children():
                tree.delete(item)
            
            for reader in filtered_readers:
                tree.insert("", tk.END, values=(
                    reader["id"], reader["fullname"], reader["email"], 
                    reader["phone"], reader["address"], len(reader["borrowed_books"])
                ))
        
        tk.Button(search_frame, text="Tìm kiếm", command=search_readers).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Làm mới", command=lambda: self.update_reader_tree(tree)).pack(side=tk.LEFT)
        
        # Add reader button
        tk.Button(search_frame, text="+ Thêm độc giả", bg="#4CAF50", fg="white", 
                command=self.show_add_reader_window).pack(side=tk.RIGHT)
        
        # Reader list
        columns = ("Mã số", "Họ tên", "Email", "Số ĐT", "Địa chỉ", "Số sách đang mượn")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        
        self.update_reader_tree(tree)
        
        
        btn_frame = tk.Frame(self.content_frame)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Sửa thông tin", bg="#2196F3", fg="white", 
                command=lambda: self.show_edit_reader_window(tree)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Xóa độc giả", bg="#f44336", fg="white", 
                command=lambda: self.delete_reader(tree)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Xem sách đang mượn", bg="#FF9800", fg="white", 
                command=lambda: self.show_reader_books(tree)).pack(side=tk.LEFT, padx=5)
    
    def update_reader_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        
        for reader in self.data["readers"]:
            tree.insert("", tk.END, values=(
                reader["id"], reader["fullname"], reader["email"], 
                reader["phone"], reader["address"], len(reader["borrowed_books"])
            ))
    
    def show_add_reader_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Thêm độc giả mới")
        add_window.geometry("400x500")
        
        tk.Label(add_window, text="THÊM ĐỘC GIẢ MỚI", font=("Arial", 14, "bold")).pack(pady=10)
        
        fields = [
            ("Mã số:", "id"),
            ("Họ tên:", "fullname"),
            ("Email:", "email"),
            ("Số ĐT:", "phone"),
            ("Địa chỉ:", "address")
        ]
        
        entries = {}
        for text, field in fields:
            frame = tk.Frame(add_window)
            frame.pack(pady=5)
            
            tk.Label(frame, text=text, width=15, anchor="w").pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=30)
            entry.pack(side=tk.LEFT)
            entries[field] = entry
        
        def add_reader():
            new_reader = {
                "id": entries["id"].get(),
                "fullname": entries["fullname"].get(),
                "email": entries["email"].get(),
                "phone": entries["phone"].get(),
                "address": entries["address"].get(),
                "borrowed_books": []
            }
            
            
            for reader in self.data["readers"]:
                if reader["id"] == new_reader["id"]:
                    messagebox.showerror("Lỗi", "Mã số độc giả đã tồn tại!")
                    return
            
            self.data["readers"].append(new_reader)
            
            
            if new_reader["id"] not in self.data["users"]:
                self.data["users"][new_reader["id"]] = {
                    "password": "123456",  
                    "role": "độc giả",
                    "fullname": new_reader["fullname"],
                    "email": new_reader["email"],
                    "phone": new_reader["phone"]
                }
            
            save_data(self.data)
            messagebox.showinfo("Thành công", "Thêm độc giả thành công!")
            add_window.destroy()
        
        tk.Button(add_window, text="Thêm độc giả", bg="#4CAF50", fg="white", 
                command=add_reader).pack(pady=20)
    
    def show_edit_reader_window(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Lỗi", "Vui lòng chọn độc giả cần sửa!")
            return
        
        reader_id = tree.item(selected[0])["values"][0]
        reader = next((r for r in self.data["readers"] if r["id"] == reader_id), None)
        
        if not reader:
            messagebox.showerror("Lỗi", "Không tìm thấy độc giả!")
            return
        
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Sửa thông tin độc giả")
        edit_window.geometry("400x500")
        
        tk.Label(edit_window, text="SỬA THÔNG TIN ĐỘC GIẢ", font=("Arial", 14, "bold")).pack(pady=10)
        
        fields = [
            ("Mã số:", "id", False),
            ("Họ tên:", "fullname", True),
            ("Email:", "email", True),
            ("Số ĐT:", "phone", True),
            ("Địa chỉ:", "address", True)
        ]
        
        entries = {}
        for text, field, editable in fields:
            frame = tk.Frame(edit_window)
            frame.pack(pady=5)
            
            tk.Label(frame, text=text, width=15, anchor="w").pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=30)
            entry.insert(0, reader[field])
            if not editable:
                entry.config(state="readonly")
            entry.pack(side=tk.LEFT)
            entries[field] = entry
        
        def update_reader():
            updated_reader = reader.copy()
            for field, entry in entries.items():
                updated_reader[field] = entry.get()
            
            # Update reader in data
            for i, r in enumerate(self.data["readers"]):
                if r["id"] == reader["id"]:
                    self.data["readers"][i] = updated_reader
                    break
            
            # Also update user info
            if reader["id"] in self.data["users"]:
                self.data["users"][reader["id"]]["fullname"] = updated_reader["fullname"]
                self.data["users"][reader["id"]]["email"] = updated_reader["email"]
                self.data["users"][reader["id"]]["phone"] = updated_reader["phone"]
            
            save_data(self.data)
            messagebox.showinfo("Thành công", "Cập nhật độc giả thành công!")
            edit_window.destroy()
            self.update_reader_tree(tree)
        
        tk.Button(edit_window, text="Cập nhật", bg="#4CAF50", fg="white", 
                command=update_reader).pack(pady=20)
    
    def delete_reader(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Lỗi", "Vui lòng chọn độc giả cần xóa!")
            return
        
        reader_id = tree.item(selected[0])["values"][0]
        
        
        reader = next((r for r in self.data["readers"] if r["id"] == reader_id), None)
        if reader and len(reader["borrowed_books"]) > 0:
            messagebox.showerror("Lỗi", "Độc giả đang mượn sách, không thể xóa!")
            return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa độc giả này?"):
            self.data["readers"] = [r for r in self.data["readers"] if r["id"] != reader_id]
            
            
            if reader_id in self.data["users"] and self.data["users"][reader_id]["role"] == "độc giả":
                del self.data["users"][reader_id]
            
            save_data(self.data)
            messagebox.showinfo("Thành công", "Xóa độc giả thành công!")
            self.update_reader_tree(tree)
    
    def show_reader_books(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Lỗi", "Vui lòng chọn độc giả!")
            return
        
        reader_id = tree.item(selected[0])["values"][0]
        reader = next((r for r in self.data["readers"] if r["id"] == reader_id), None)
        
        if not reader:
            messagebox.showerror("Lỗi", "Không tìm thấy độc giả!")
            return
        
        books_window = tk.Toplevel(self.root)
        books_window.title(f"Sách đang mượn - {reader['fullname']}")
        books_window.geometry("800x400")
        
        # Book list
        columns = ("Mã sách", "Tên sách", "Ngày mượn", "Hạn trả")
        book_tree = ttk.Treeview(books_window, columns=columns, show="headings", height=15)
        
        for col in columns:
            book_tree.heading(col, text=col)
            book_tree.column(col, width=150)
        
        book_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add borrowed books to treeview
        for borrow_id in reader["borrowed_books"]:
            borrow = next((b for b in self.data["borrows"] if b["id"] == borrow_id), None)
            if borrow and borrow["return_date"] == "":
                book = next((b for b in self.data["books"] if b["id"] == borrow["book_id"]), None)
                if book:
                    book_tree.insert("", tk.END, values=(
                        book["id"], book["title"], 
                        borrow["borrow_date"], borrow["due_date"]
                    ))
        
        
        def return_book():
            selected_book = book_tree.selection()
            if not selected_book:
                messagebox.showerror("Lỗi", "Vui lòng chọn sách cần trả!")
                return
            
            book_id = book_tree.item(selected_book[0])["values"][0]
            
            
            for borrow in self.data["borrows"]:
                if borrow["book_id"] == book_id and borrow["return_date"] == "":
                    borrow["return_date"] = datetime.now().strftime("%d/%m/%Y")
                    
                    
                    for book in self.data["books"]:
                        if book["id"] == book_id:
                            book["quantity"] += 1
                            break
                    
                    
                    reader["borrowed_books"].remove(borrow["id"])
                    
                    save_data(self.data)
                    messagebox.showinfo("Thành công", "Ghi nhận trả sách thành công!")
                    books_window.destroy()
                    return
            
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin mượn sách!")
        
        tk.Button(books_window, text="Ghi nhận trả sách", bg="#4CAF50", fg="white", 
                command=return_book).pack(pady=10)
    

    def show_borrow_management(self):
        self.clear_content()
        
        # Search frame
        search_frame = tk.Frame(self.content_frame)
        search_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(search_frame, text="Tìm kiếm phiếu mượn:").pack(side=tk.LEFT)
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        search_by = ttk.Combobox(search_frame, values=["Mã phiếu", "Mã sách", "Mã độc giả"], width=15)
        search_by.pack(side=tk.LEFT, padx=5)
        search_by.set("Mã phiếu")
        
        def search_borrows():
            keyword = search_entry.get().lower()
            search_type = search_by.get()
            
            filtered_borrows = []
            for borrow in self.data["borrows"]:
                if search_type == "Mã phiếu" and keyword in borrow["id"].lower():
                    filtered_borrows.append(borrow)
                elif search_type == "Mã sách" and keyword in borrow["book_id"].lower():
                    filtered_borrows.append(borrow)
                elif search_type == "Mã độc giả" and keyword in borrow["reader_id"].lower():
                    filtered_borrows.append(borrow)
            
            
            for item in tree.get_children():
                tree.delete(item)
            
            for borrow in filtered_borrows:
                reader = next((r for r in self.data["readers"] if r["id"] == borrow["reader_id"]), None)
                book = next((b for b in self.data["books"] if b["id"] == borrow["book_id"]), None)
                
                reader_name = reader["fullname"] if reader else "Unknown"
                book_title = book["title"] if book else "Unknown"
                
                tree.insert("", tk.END, values=(
                    borrow["id"], borrow["reader_id"], reader_name,
                    borrow["book_id"], book_title,
                    borrow["borrow_date"], borrow["due_date"], 
                    borrow["return_date"] if borrow["return_date"] else "Chưa trả"
                ))
        
        tk.Button(search_frame, text="Tìm kiếm", command=search_borrows).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Làm mới", command=lambda: self.update_borrow_tree(tree)).pack(side=tk.LEFT)
        
        # Add borrow button
        tk.Button(search_frame, text="+ Tạo phiếu mượn", bg="#4CAF50", fg="white", 
                command=self.show_add_borrow_window).pack(side=tk.RIGHT)
        
        
        columns = ("Mã phiếu", "Mã ĐG", "Tên ĐG", "Mã sách", "Tên sách", "Ngày mượn", "Hạn trả", "Ngày trả")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        
        self.update_borrow_tree(tree)
    
    def update_borrow_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        
        for borrow in self.data["borrows"]:
            reader = next((r for r in self.data["readers"] if r["id"] == borrow["reader_id"]), None)
            book = next((b for b in self.data["books"] if b["id"] == borrow["book_id"]), None)
            
            reader_name = reader["fullname"] if reader else "Unknown"
            book_title = book["title"] if book else "Unknown"
            
            tree.insert("", tk.END, values=(
                borrow["id"], borrow["reader_id"], reader_name,
                borrow["book_id"], book_title,
                borrow["borrow_date"], borrow["due_date"], 
                borrow["return_date"] if borrow["return_date"] else "Chưa trả"
            ))
    
    def show_add_borrow_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Tạo phiếu mượn sách")
        add_window.geometry("500x400")
        
        tk.Label(add_window, text="TẠO PHIẾU MƯỢN SÁCH", font=("Arial", 14, "bold")).pack(pady=10)
        
        
        tk.Label(add_window, text="Độc giả:", font=("Arial", 12)).pack()
        reader_var = tk.StringVar()
        readers = [f"{r['id']} - {r['fullname']}" for r in self.data["readers"]]
        reader_combo = ttk.Combobox(add_window, textvariable=reader_var, values=readers, state="readonly")
        reader_combo.pack(pady=5)
        
    
        tk.Label(add_window, text="Sách:", font=("Arial", 12)).pack()
        book_var = tk.StringVar()
        available_books = [f"{b['id']} - {b['title']}" for b in self.data["books"] if b["quantity"] > 0]
        book_combo = ttk.Combobox(add_window, textvariable=book_var, values=available_books, state="readonly")
        book_combo.pack(pady=5)
        
        
        tk.Label(add_window, text="Hạn trả (ngày):", font=("Arial", 12)).pack()
        due_days_var = tk.IntVar(value=7)
        tk.Entry(add_window, textvariable=due_days_var, width=10).pack()
        
        def create_borrow():
            if not reader_var.get() or not book_var.get():
                messagebox.showerror("Lỗi", "Vui lòng chọn độc giả và sách!")
                return
            
            reader_id = reader_var.get().split(" - ")[0]
            book_id = book_var.get().split(" - ")[0]
            
            
            reader = next((r for r in self.data["readers"] if r["id"] == reader_id), None)
            if not reader:
                messagebox.showerror("Lỗi", "Không tìm thấy độc giả!")
                return
            
            
            book = next((b for b in self.data["books"] if b["id"] == book_id), None)
            if not book:
                messagebox.showerror("Lỗi", "Không tìm thấy sách!")
                return
            
            if book["quantity"] <= 0:
                messagebox.showerror("Lỗi", "Sách đã hết, không thể mượn!")
                return
            
            
            borrow_id = f"BORROW-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            borrow_date = datetime.now().strftime("%d/%m/%Y")
            due_date = (datetime.now() + timedelta(days=due_days_var.get())).strftime("%d/%m/%Y")
            
            new_borrow = {
                "id": borrow_id,
                "reader_id": reader_id,
                "book_id": book_id,
                "borrow_date": borrow_date,
                "due_date": due_date,
                "return_date": ""
            }
            
            
            book["quantity"] -= 1
            
            
            reader["borrowed_books"].append(borrow_id)
            
            
            self.data["borrows"].append(new_borrow)
            
            save_data(self.data)
            messagebox.showinfo("Thành công", "Tạo phiếu mượn thành công!")
            add_window.destroy()
        
        tk.Button(add_window, text="Tạo phiếu mượn", bg="#4CAF50", fg="white", 
                command=create_borrow).pack(pady=20)
    
    
    def show_statistics(self):
        self.clear_content()
        
        
        tab_control = ttk.Notebook(self.content_frame)
        
        
        tab1 = ttk.Frame(tab_control)
        tab_control.add(tab1, text="Thống kê sách")
        
        
        tk.Label(tab1, text="Số lượng sách theo thể loại", font=("Arial", 12, "bold")).pack(pady=10)
        
        category_frame = tk.Frame(tab1)
        category_frame.pack(fill=tk.X, padx=10, pady=5)
        
        categories = {}
        for book in self.data["books"]:
            for category in book["category"].split(", "):
                categories[category] = categories.get(category, 0) + 1
        
        for category, count in categories.items():
            tk.Label(category_frame, text=f"{category}: {count}").pack(anchor="w")
        
        
        tk.Label(tab1, text="Số lượng sách theo nhà xuất bản", font=("Arial", 12, "bold")).pack(pady=10)
        
        publisher_frame = tk.Frame(tab1)
        publisher_frame.pack(fill=tk.X, padx=10, pady=5)
        
        publishers = {}
        for book in self.data["books"]:
            publishers[book["publisher"]] = publishers.get(book["publisher"], 0) + 1
        
        for publisher, count in publishers.items():
            tk.Label(publisher_frame, text=f"{publisher}: {count}").pack(anchor="w")
        
        
        tab2 = ttk.Frame(tab_control)
        tab_control.add(tab2, text="Thống kê mượn/trả")
        
        
        tk.Label(tab2, text="Số lượt mượn theo tháng", font=("Arial", 12, "bold")).pack(pady=10)
        
        monthly_borrows = {}
        for borrow in self.data["borrows"]:
            month = borrow["borrow_date"].split("/")[1] + "/" + borrow["borrow_date"].split("/")[2]
            monthly_borrows[month] = monthly_borrows.get(month, 0) + 1
        
        for month, count in monthly_borrows.items():
            tk.Label(tab2, text=f"Tháng {month}: {count} lượt mượn").pack(anchor="w")
        
        
        tk.Label(tab2, text="Sách trả muộn", font=("Arial", 12, "bold")).pack(pady=10)
        
        late_returns = []
        for borrow in self.data["borrows"]:
            if borrow["return_date"]:
                due_date = datetime.strptime(borrow["due_date"], "%d/%m/%Y")
                return_date = datetime.strptime(borrow["return_date"], "%d/%m/%Y")
                if return_date > due_date:
                    late_returns.append(borrow)
        
        tk.Label(tab2, text=f"Tổng số: {len(late_returns)}").pack(anchor="w")
        
        
        tab3 = ttk.Frame(tab_control)
        tab_control.add(tab3, text="Thống kê độc giả")
        
        
        tk.Label(tab3, text="Độc giả mượn nhiều nhất", font=("Arial", 12, "bold")).pack(pady=10)
        
        reader_borrows = {}
        for borrow in self.data["borrows"]:
            reader_borrows[borrow["reader_id"]] = reader_borrows.get(borrow["reader_id"], 0) + 1
        
        sorted_readers = sorted(reader_borrows.items(), key=lambda x: x[1], reverse=True)[:5]
        
        for reader_id, count in sorted_readers:
            reader = next((r for r in self.data["readers"] if r["id"] == reader_id), None)
            if reader:
                tk.Label(tab3, text=f"{reader['fullname']}: {count} lượt mượn").pack(anchor="w")
        
    
        tab_control.pack(fill=tk.BOTH, expand=True)
    
    
    def show_account_management(self):
        self.clear_content()
        
        
        columns = ("Username", "Role", "Fullname", "Email", "Phone")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        
        for username, user in self.data["users"].items():
            tree.insert("", tk.END, values=(
                username, user["role"], user["fullname"], 
                user["email"], user["phone"]
            ))
        
        
        btn_frame = tk.Frame(self.content_frame)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Sửa thông tin", bg="#2196F3", fg="white", 
                command=lambda: self.show_edit_account_window(tree)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Xóa tài khoản", bg="#f44336", fg="white", 
                command=lambda: self.delete_account(tree)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Đổi mật khẩu", bg="#FF9800", fg="white", 
                command=lambda: self.show_change_password_window(tree)).pack(side=tk.LEFT, padx=5)
    
    def show_edit_account_window(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Lỗi", "Vui lòng chọn tài khoản cần sửa!")
            return
        
        username = tree.item(selected[0])["values"][0]
        user = self.data["users"][username]
        
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Sửa thông tin tài khoản")
        edit_window.geometry("400x400")
        
        tk.Label(edit_window, text="SỬA THÔNG TIN TÀI KHOẢN", font=("Arial", 14, "bold")).pack(pady=10)
        
        fields = [
            ("Username:", "username", False),
            ("Vai trò:", "role", False),
            ("Họ tên:", "fullname", True),
            ("Email:", "email", True),
            ("Số ĐT:", "phone", True)
        ]
        
        entries = {}
        for text, field, editable in fields:
            frame = tk.Frame(edit_window)
            frame.pack(pady=5)
            
            tk.Label(frame, text=text, width=15, anchor="w").pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=30)
            entry.insert(0, user[field])
            if not editable:
                entry.config(state="readonly")
            entry.pack(side=tk.LEFT)
            entries[field] = entry
        
        def update_account():
            updated_user = user.copy()
            for field, entry in entries.items():
                if field != "username" and field != "role":
                    updated_user[field] = entry.get()
            
            
            self.data["users"][username] = updated_user
            
            
            if username in [r["id"] for r in self.data["readers"]]:
                for i, reader in enumerate(self.data["readers"]):
                    if reader["id"] == username:
                        self.data["readers"][i]["fullname"] = updated_user["fullname"]
                        self.data["readers"][i]["email"] = updated_user["email"]
                        self.data["readers"][i]["phone"] = updated_user["phone"]
                        break
            
            save_data(self.data)
            messagebox.showinfo("Thành công", "Cập nhật tài khoản thành công!")
            edit_window.destroy()
            
            
            for item in tree.get_children():
                tree.delete(item)
            
            for username, user in self.data["users"].items():
                tree.insert("", tk.END, values=(
                    username, user["role"], user["fullname"], 
                    user["email"], user["phone"]
                ))
        
        tk.Button(edit_window, text="Cập nhật", bg="#4CAF50", fg="white", 
                command=update_account).pack(pady=20)
    
    def delete_account(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Lỗi", "Vui lòng chọn tài khoản cần xóa!")
            return
        
        username = tree.item(selected[0])["values"][0]
        role = tree.item(selected[0])["values"][1]
        
        
        if username == self.current_user["username"]:
            messagebox.showerror("Lỗi", "Không thể xóa tài khoản đang đăng nhập!")
            return
        
        
        if role == "độc giả":
            reader = next((r for r in self.data["readers"] if r["id"] == username), None)
            if reader and len(reader["borrowed_books"]) > 0:
                messagebox.showerror("Lỗi", "Độc giả đang mượn sách, không thể xóa!")
                return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa tài khoản này?"):
            del self.data["users"][username]
            
            
            if role == "độc giả":
                self.data["readers"] = [r for r in self.data["readers"] if r["id"] != username]
            
            save_data(self.data)
            messagebox.showinfo("Thành công", "Xóa tài khoản thành công!")
            
            
            for item in tree.get_children():
                tree.delete(item)
            
            for username, user in self.data["users"].items():
                tree.insert("", tk.END, values=(
                    username, user["role"], user["fullname"], 
                    user["email"], user["phone"]
                ))
    
    def show_change_password_window(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Lỗi", "Vui lòng chọn tài khoản cần đổi mật khẩu!")
            return
        
        username = tree.item(selected[0])["values"][0]
        
        pass_window = tk.Toplevel(self.root)
        pass_window.title("Đổi mật khẩu")
        pass_window.geometry("300x200")
        
        tk.Label(pass_window, text="ĐỔI MẬT KHẨU", font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(pass_window, text="Mật khẩu mới:").pack()
        new_pass_entry = tk.Entry(pass_window, show="*")
        new_pass_entry.pack(pady=5)
        
        tk.Label(pass_window, text="Nhập lại mật khẩu:").pack()
        confirm_pass_entry = tk.Entry(pass_window, show="*")
        confirm_pass_entry.pack(pady=5)
        
        def change_password():
            new_pass = new_pass_entry.get()
            confirm_pass = confirm_pass_entry.get()
            
            if not new_pass or not confirm_pass:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ mật khẩu!")
                return
            
            if new_pass != confirm_pass:
                messagebox.showerror("Lỗi", "Mật khẩu không khớp!")
                return
            
            self.data["users"][username]["password"] = new_pass
            save_data(self.data)
            messagebox.showinfo("Thành công", "Đổi mật khẩu thành công!")
            pass_window.destroy()
        
        tk.Button(pass_window, text="Đổi mật khẩu", bg="#4CAF50", fg="white", 
                command=change_password).pack(pady=10)
    
    
    def show_librarian_dashboard(self):
        self.clear_screen()
        
        
        header_frame = tk.Frame(self.root, bg="#333", height=50)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text="QUẢN LÝ THƯ VIỆN - THỦ THƯ", fg="white", bg="#333", 
               font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=20)
        
        tk.Button(header_frame, text="Đăng xuất", bg="#f44336", fg="white", 
                command=self.setup_login_screen).pack(side=tk.RIGHT, padx=20)
        
        
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        
        sidebar = tk.Frame(main_frame, bg="#f1f1f1", width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        buttons = [
            ("Quản lý mượn/trả", self.show_borrow_management),
            ("Quản lý độc giả", self.show_reader_management),
            ("Danh sách sách", self.show_book_list)
        ]
        
        for text, command in buttons:
            tk.Button(sidebar, text=text, width=20, anchor="w", 
                    command=command).pack(pady=5, padx=5, ipady=5)
        
        
        self.content_frame = tk.Frame(main_frame, bg="white")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    
        self.show_borrow_management()
    
    def show_book_list(self):
        self.clear_content()
        
        
        columns = ("ID", "Tên sách", "Tác giả", "Thể loại", "Số lượng", "Năm XB", "Nhà XB")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        
        for book in self.data["books"]:
            tree.insert("", tk.END, values=(
                book["id"], book["title"], book["author"], 
                book["category"], book["quantity"], 
                book["year"], book["publisher"]
            ))
    
    
    def show_reader_dashboard(self):
        self.clear_screen()
        
        # Header
        header_frame = tk.Frame(self.root, bg="#333", height=50)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text="QUẢN LÝ THƯ VIỆN - ĐỘC GIẢ", fg="white", bg="#333", 
               font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=20)
        
        tk.Button(header_frame, text="Đăng xuất", bg="#f44336", fg="white", 
                command=self.setup_login_screen).pack(side=tk.RIGHT, padx=20)
        
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        
        sidebar = tk.Frame(main_frame, bg="#f1f1f1", width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        buttons = [
            ("Sách đang mượn", self.show_my_borrowed_books),
            ("Danh sách sách", self.show_all_books),
            ("Thông tin cá nhân", self.show_my_profile)
        ]
        
        for text, command in buttons:
            tk.Button(sidebar, text=text, width=20, anchor="w", 
                    command=command).pack(pady=5, padx=5, ipady=5)
        
        
        self.content_frame = tk.Frame(main_frame, bg="white")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    
        self.show_my_borrowed_books()
    
    def show_my_borrowed_books(self):
        self.clear_content()
        
        reader = next((r for r in self.data["readers"] if r["id"] == self.current_user["username"]), None)
        if not reader:
            tk.Label(self.content_frame, text="Không tìm thấy thông tin độc giả!", font=("Arial", 12)).pack(pady=20)
            return
        
        # Book list
        columns = ("Mã sách", "Tên sách", "Ngày mượn", "Hạn trả")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add borrowed books to treeview
        for borrow_id in reader["borrowed_books"]:
            borrow = next((b for b in self.data["borrows"] if b["id"] == borrow_id), None)
            if borrow and borrow["return_date"] == "":
                book = next((b for b in self.data["books"] if b["id"] == borrow["book_id"]), None)
                if book:
                    tree.insert("", tk.END, values=(
                        book["id"], book["title"], 
                        borrow["borrow_date"], borrow["due_date"]
                    ))
    
    def show_all_books(self):
        self.clear_content()
        
        # Search frame
        search_frame = tk.Frame(self.content_frame)
        search_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(search_frame, text="Tìm kiếm sách:").pack(side=tk.LEFT)
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        search_by = ttk.Combobox(search_frame, values=["Tên sách", "Tác giả", "Thể loại"], width=15)
        search_by.pack(side=tk.LEFT, padx=5)
        search_by.set("Tên sách")
        
        def search_books():
            keyword = search_entry.get().lower()
            search_type = search_by.get()
            
            filtered_books = []
            for book in self.data["books"]:
                if search_type == "Tên sách" and keyword in book["title"].lower():
                    filtered_books.append(book)
                elif search_type == "Tác giả" and keyword in book["author"].lower():
                    filtered_books.append(book)
                elif search_type == "Thể loại" and keyword in book["category"].lower():
                    filtered_books.append(book)
            
            # Update treeview
            for item in tree.get_children():
                tree.delete(item)
            
            for book in filtered_books:
                tree.insert("", tk.END, values=(
                    book["id"], book["title"], book["author"], 
                    book["category"], book["quantity"], 
                    book["year"], book["publisher"]
                ))
        
        tk.Button(search_frame, text="Tìm kiếm", command=search_books).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Làm mới", command=lambda: self.update_book_tree_for_reader(tree)).pack(side=tk.LEFT)
        
        # Book list
        columns = ("ID", "Tên sách", "Tác giả", "Thể loại", "Số lượng", "Năm XB", "Nhà XB")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Update treeview
        self.update_book_tree_for_reader(tree)
    
    def update_book_tree_for_reader(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        
        for book in self.data["books"]:
            tree.insert("", tk.END, values=(
                book["id"], book["title"], book["author"], 
                book["category"], book["quantity"], 
                book["year"], book["publisher"]
            ))
    
    def show_my_profile(self):
        self.clear_content()
        
        reader = next((r for r in self.data["readers"] if r["id"] == self.current_user["username"]), None)
        if not reader:
            tk.Label(self.content_frame, text="Không tìm thấy thông tin độc giả!", font=("Arial", 12)).pack(pady=20)
            return
        
        # Profile info
        profile_frame = tk.Frame(self.content_frame, bg="white", bd=2, relief="groove")
        profile_frame.pack(pady=20, padx=50, fill=tk.X)
        
        tk.Label(profile_frame, text="THÔNG TIN CÁ NHÂN", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        
        fields = [
            ("Mã số:", reader["id"]),
            ("Họ tên:", reader["fullname"]),
            ("Email:", reader["email"]),
            ("Số ĐT:", reader["phone"]),
            ("Địa chỉ:", reader["address"]),
            ("Số sách đang mượn:", len(reader["borrowed_books"]))
        ]
        
        for text, value in fields:
            frame = tk.Frame(profile_frame, bg="white")
            frame.pack(fill=tk.X, pady=5)
            
            tk.Label(frame, text=text, font=("Arial", 12), bg="white", width=15, anchor="w").pack(side=tk.LEFT)
            tk.Label(frame, text=value, font=("Arial", 12), bg="white").pack(side=tk.LEFT)
        
        # Edit button
        def edit_profile():
            self.show_edit_profile_window(reader)
        
        tk.Button(self.content_frame, text="Chỉnh sửa thông tin", bg="#4CAF50", fg="white", 
                command=edit_profile).pack(pady=10)
    
    def show_edit_profile_window(self, reader):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Chỉnh sửa thông tin cá nhân")
        edit_window.geometry("400x400")
        
        tk.Label(edit_window, text="CHỈNH SỬA THÔNG TIN", font=("Arial", 14, "bold")).pack(pady=10)
        
        fields = [
            ("Họ tên:", "fullname", reader["fullname"]),
            ("Email:", "email", reader["email"]),
            ("Số ĐT:", "phone", reader["phone"]),
            ("Địa chỉ:", "address", reader["address"])
        ]
        
        entries = {}
        for text, field, value in fields:
            frame = tk.Frame(edit_window)
            frame.pack(pady=5)
            
            tk.Label(frame, text=text, width=15, anchor="w").pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=30)
            entry.insert(0, value)
            entry.pack(side=tk.LEFT)
            entries[field] = entry
        
        def update_profile():
            updated_reader = reader.copy()
            for field, entry in entries.items():
                updated_reader[field] = entry.get()
            
            # Update reader in data
            for i, r in enumerate(self.data["readers"]):
                if r["id"] == reader["id"]:
                    self.data["readers"][i] = updated_reader
                    break
            
            # Also update user info
            if reader["id"] in self.data["users"]:
                self.data["users"][reader["id"]]["fullname"] = updated_reader["fullname"]
                self.data["users"][reader["id"]]["email"] = updated_reader["email"]
                self.data["users"][reader["id"]]["phone"] = updated_reader["phone"]
            
            save_data(self.data)
            messagebox.showinfo("Thành công", "Cập nhật thông tin thành công!")
            edit_window.destroy()
            self.show_my_profile()
        
        tk.Button(edit_window, text="Cập nhật", bg="#4CAF50", fg="white", 
                command=update_profile).pack(pady=20)
    
    # ========== Utility functions ==========
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()