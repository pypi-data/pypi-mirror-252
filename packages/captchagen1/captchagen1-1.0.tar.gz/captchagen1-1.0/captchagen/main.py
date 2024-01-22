import sqlite3
import random
import string
from tkinter import *
from tkinter import messagebox
from tkinter import ttk


class Window(Tk):
    def __init__(self, title, geometry):
        super().__init__() 
        self.title(title)
        self.geometry(geometry) 
        self.resizable(False, False)
        self.create_tables()
    
    def create_tables(self):
        connection = sqlite3.connect("lab_database.db")
        cursor = connection.cursor()
        cursor.executescript('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    photo TEXT,
                    login TEXT NOT NULL,
                    password TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    user_type TEXT NOT NULL,
                    dob TEXT NOT NULL,
                    passport TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT NOT NULL,
                    insurance_number TEXT NOT NULL,
                    insurance_type TEXT NOT NULL,
                    insurance_company TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS services (
                    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    cost REAL NOT NULL,
                    service_code TEXT NOT NULL,
                    execution_time INTEGER NOT NULL,
                    deviation REAL NOT NULL
                );
                CREATE TABLE IF NOT EXISTS orders (
                    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    creation_date TEXT NOT NULL,
                    status TEXT NOT NULL,
                    completion_time INTEGER,
                    user_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                );
                CREATE TABLE IF NOT EXISTS order_services (
                    order_service_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER,
                    service_id INTEGER,
                    status TEXT NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders(order_id),
                    FOREIGN KEY (service_id) REFERENCES services(service_id)
                );
                CREATE TABLE IF NOT EXISTS invoices (
                    invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    service_id INTEGER,
                    amount REAL NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (service_id) REFERENCES services(service_id)
                );
            ''')
        connection.commit()
        connection.close()
        
    def logout(self):
        self.destroy()
        WindowAuth("Авторизация", "500x500", 0)
    
    def display_user_info(self):
        full_name, dob, photo_path = self.user_data[4], self.user_data[6], self.user_data[1] 
        if photo_path:
            photo_image = PhotoImage(file=photo_path)

            width, height = photo_image.width(), photo_image.height()
            max_size = 100, 100

            scale_w = width // max_size[0]
            scale_h = height // max_size[1]
            scale = max(scale_w, scale_h, 1)

            photo_image = photo_image.subsample(scale, scale)

            label_photo = Label(self, image=photo_image)
            label_photo.image = photo_image 
            label_photo.pack(pady=50)
        Label(self, text=f"Роль: {self.title()}", font=("Times New Roman", 20)).pack()
        Label(self, text=f"Имя: {full_name}", font=("Times New Roman", 20)).pack()
        Label(self, text=f"Дата рождения: {dob}", font=("Times New Roman", 20)).pack()
        Button(self, text="Выйти", width=15, font=("Times New Roman", 20), command=self.logout).pack(pady=20)

class WindowAuth(Window):
    def __init__(self, title, geometry, lockout_time):
        super().__init__(title, geometry)
        self.failed_attempts = 0
        self.create_login_widgets()
        self.captcha_frame = None
        if lockout_time > 0:
            self.start_lockout(lockout_time)

    def create_login_widgets(self):
        Label(self, text="Авторизация", font=("Times New Roman", 30)).pack(pady=50)
        Label(self, text="Логин:", font=("Times New Roman", 20)).pack()
        self.entry_username = Entry(self, width=20, font=("Times New Roman", 20))
        self.entry_username.pack(pady=5)
        Label(self, text="Пароль:", font=("Times New Roman", 20)).pack()
        self.entry_password = Entry(self, show="*", width=20, font=("Times New Roman", 20))
        self.entry_password.pack(pady=5)
        self.toggle_password_button = Button(self, text="Показать пароль", font=("Times New Roman", 14), command=self.toggle_password)
        self.toggle_password_button.pack(pady=5)
        self.login_button = Button(self, text="Войти", width=15, font=("Times New Roman", 20), command=self.authenticate)
        self.login_button.pack(pady=20)
        self.timer_label = Label(self, text="", font=("Times New Roman", 20))
        self.timer_label.place(x=10, y=10)

    def toggle_password(self):
        if self.entry_password.cget('show') == '*':
            self.entry_password.config(show='')
            self.toggle_password_button.config(text="Скрыть пароль")
        else:
            self.entry_password.config(show='*')
            self.toggle_password_button.config(text="Показать пароль")

    def authenticate(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if self.failed_attempts >= 1:
            entered_captcha = self.captcha_entry.get().upper()
            if entered_captcha != self.plain_captcha_code:
                messagebox.showerror("Ошибка", "Неверный код CAPTCHA")
                self.start_lockout(10)
                self.create_captcha()
                return

        user_data = self.check_credentials(username, password)
        if user_data:
            self.failed_attempts = 0
            self.destroy()
            self.open_user_window(user_data)
        else:
            self.failed_attempts += 1
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
            if self.failed_attempts >= 1:
                self.create_captcha()
        
    def start_lockout(self, lockout_time):
        self.lockout_time = lockout_time
        self.update_timer()
        self.login_button['state'] = 'disabled'

    def update_timer(self):
        if self.lockout_time > 0:
            self.timer_label.config(text=f"Блокировка: {self.lockout_time}s")
            self.lockout_time -= 1
            self.after(1000, self.update_timer)
        else:
            self.login_button['state'] = 'normal'
            self.timer_label.config(text="")
    
    def check_credentials(self, username, password):
        connection = sqlite3.connect("lab_database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE login=? AND password=?", (username, password))
        return cursor.fetchone()

    def open_user_window(self, user_data):
        user_type = user_data[5]
        if user_type == "admin":
            WindowAdmin("Администратор", "500x500", user_data)
        elif user_type == "buh":
            WindowBuh("Бухгалтер", "500x500", user_data)
        elif user_type == "lab_is":
            WindowLabIS("Лаборант-Исследователь", "1000x1000", user_data)
        elif user_type == "lab":
            WindowLab("Лаборант", "500x500", user_data)

    def create_captcha(self):
        if self.captcha_frame:
            self.captcha_frame.destroy()

        self.captcha_frame = Frame(self)
        self.captcha_frame.pack(pady=10)

        plain_captcha_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        display_captcha_code = '\u0336'.join(plain_captcha_code) + '\u0336'

        captcha_label = Label(self.captcha_frame, text=f"Код: {display_captcha_code}", font=("Times New Roman", 20))
        captcha_label.pack(side=LEFT)

        self.captcha_entry = Entry(self.captcha_frame, width=6, font=("Times New Roman", 20))
        self.captcha_entry.pack(side=LEFT)

        refresh_captcha_button = Button(self.captcha_frame, text="Обновить", command=self.create_captcha)
        refresh_captcha_button.pack(side=LEFT)

        self.plain_captcha_code = plain_captcha_code

    def validate_credentials(self):
        if self.captcha_frame:
            entered_captcha = self.captcha_entry.get().upper()

            if entered_captcha != self.plain_captcha_code:
                messagebox.showerror("Ошибка", "Неверный код CAPTCHA")
                return False

        return True

class WindowAdmin(Window):
    def __init__(self, title, geometry, user_data):
        super().__init__(title, geometry)
        self.user_data = user_data
        self.display_user_info()

class WindowBuh(Window):
    def __init__(self, title, geometry, user_data):
        super().__init__(title, geometry)
        self.user_data = user_data
        self.display_user_info()
        Button(self, text="Показать счета-фактуры", width=20, font=("Times New Roman", 20), command=self.show_table).pack(pady=10)

    def show_table(self):
        invoices_window = Toplevel(self)
        invoices_window.title("Счета-фактуры")
        invoices_window.geometry("600x400")

        tree = ttk.Treeview(invoices_window)
        tree.pack(pady=20, padx=20, expand=True, fill='both')

        tree['columns'] = ("invoice_id", "user_id", "service_id", "amount")
        tree.column("#0", width=0, stretch=NO) 
        tree.column("invoice_id", anchor=CENTER, width=80)
        tree.column("user_id", anchor=CENTER, width=80)
        tree.column("service_id", anchor=CENTER, width=80)
        tree.column("amount", anchor=CENTER, width=80)
        tree.heading("#0", text="", anchor=CENTER)
        tree.heading("invoice_id", text="ID счета", anchor=CENTER)
        tree.heading("user_id", text="ID пользователя", anchor=CENTER)
        tree.heading("service_id", text="ID услуги", anchor=CENTER)
        tree.heading("amount", text="Сумма", anchor=CENTER)

        connection = sqlite3.connect("lab_database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM invoices")
        invoices = cursor.fetchall()
        connection.close()

        for invoice in invoices:
            tree.insert("", END, values=invoice)

class WindowWithTimer(Window):
    def __init__(self, title, geometry, user_data, timer_duration=605):
        super().__init__(title, geometry)
        self.user_data = user_data
        self.display_user_info()

        self.remaining_time = timer_duration
        self.timer_label = Label(self, text=self.format_time(self.remaining_time), font=("Times New Roman", 20))
        self.timer_label.place(x=10, y=10)

        self.speed_up_button = Button(self, text="Ускорить таймер", command=self.speed_up_timer)
        self.speed_up_button.place(x=10, y=50)

        self.count = 0
        self.update_timer()
    
    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins:02d}:{secs:02d}"

    def update_timer(self):
        if self.remaining_time > 0:
            self.timer_label.config(text=self.format_time(self.remaining_time))
            self.remaining_time -= 1
            self.after(1000, self.update_timer)
        else:
            self.destroy()
            WindowAuth("Авторизация", "500x500", 60)
        
        if self.remaining_time == 300:
                messagebox.showwarning("Предупреждение", "До автоматического выхода осталось 5 минут!")
                self.after(1000, self.update_timer)

    def speed_up_timer(self):
        self.count += 1

        if self.count == 1:
            self.remaining_time = 301
        elif self.count == 2:
            self.remaining_time = 2

        self.timer_label.config(text=self.format_time(self.remaining_time))

class WindowLabIS(WindowWithTimer):
    def __init__(self, title, geometry, user_data):
        super().__init__(title, geometry, user_data)
        self.user_data = user_data
        self.create_order_widgets()

    def create_order_widgets(self):
        Label(self, text="Создать заказ", font=("Times New Roman", 20)).pack(pady=10)

        Label(self, text="ID пользователя:", font=("Times New Roman", 20)).pack()
        self.user_id_entry = Entry(self, width=20, font=("Times New Roman", 20))
        self.user_id_entry.pack(pady=5)

        Label(self, text="Выберите услугу:", font=("Times New Roman", 20)).pack()
        self.service_combobox = ttk.Combobox(self, width=18, font=("Times New Roman", 20))
        self.service_combobox.pack(pady=5)
        self.load_services()

        Button(self, text="Создать заказ", command=self.create_order).pack(pady=10)
        Button(self, text="Просмотр заказов", command=self.view_orders).pack(pady=10)

    def load_services(self):
        connection = sqlite3.connect("lab_database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM services")
        services = cursor.fetchall()
        self.service_combobox['values'] = [service[0] for service in services]
        connection.close()

    def view_orders(self):
        orders_window = Toplevel(self)
        orders_window.title("Заказы")
        orders_window.geometry("600x400")

        tree = ttk.Treeview(orders_window)
        tree.pack(pady=20, padx=20, expand=True, fill='both')

        tree['columns'] = ("order_id", "creation_date", "status", "completion_time", "user_id")
        tree.column("#0", width=0, stretch=NO)
        tree.column("order_id", anchor=CENTER, width=80)
        tree.column("creation_date", anchor=CENTER, width=120)
        tree.column("status", anchor=CENTER, width=120)
        tree.column("user_id", anchor=CENTER, width=80)
        tree.column("completion_time", anchor=CENTER, width=100)
        tree.heading("#0", text="", anchor=CENTER)
        tree.heading("order_id", text="ID заказа", anchor=CENTER)
        tree.heading("creation_date", text="Дата создания", anchor=CENTER)
        tree.heading("status", text="Статус", anchor=CENTER)
        tree.heading("user_id", text="ID пользователя", anchor=CENTER)
        tree.heading("completion_time", text="Время на работу", anchor=CENTER)

        connection = sqlite3.connect("lab_database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        connection.close()

        for order in orders:
            tree.insert("", END, values=order)

    def create_order(self):
        user_id = self.user_id_entry.get()
        if user_id:
            with sqlite3.connect("lab_database.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO orders (user_id, creation_date, status) VALUES (?, datetime('now'), 'pending')", (user_id,))
                conn.commit()
                messagebox.showinfo("Успех", "Заказ создан")
        else:
            messagebox.showwarning("Предупреждение", "ID пользователя не указан")

class WindowLab(WindowWithTimer):
    def __init__(self, title, geometry, user_data):
        super().__init__(title, geometry, user_data)
        self.show_users_button = Button(self, text="Пользователи", command=self.show_users)
        self.show_users_button.pack(pady=10)

    def show_users(self):
        users_window = Toplevel(self)
        users_window.title("Пользователи")
        users_window.geometry("800x400")

        tree = ttk.Treeview(users_window)
        tree.pack(pady=20, padx=20, expand=True, fill='both')

        columns = ("user_id", "photo", "login", "password", "full_name", "user_type", "dob", 
                   "passport", "phone", "email", "insurance_number", "insurance_type", "insurance_company")
        tree['columns'] = columns
        tree.column("#0", width=0, stretch=NO)
        for col in columns:
            tree.column(col, anchor=W, width=120)
            tree.heading(col, text=col, anchor=W)

        connection = sqlite3.connect("lab_database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        connection.close()

        for row in rows:
            tree.insert("", END, values=row)

window = WindowAuth("Авторизация", "500x500", 0)
window.mainloop()