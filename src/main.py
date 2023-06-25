import tkinter as tk
from tkinter import ttk
import utils, re

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.app_name = "Password Manager"

        self.SCR_WIDTH= self.winfo_screenwidth()
        self.SCR_HEIGHT= self.winfo_screenheight()
        self.geometry(f"300x300")
        self.title(self.app_name)
        self.grid_columnconfigure(0, weight=1)
        
        self.create_user = CreateUser(self)
        self.forgot_password = ForgotPassword(self)
        self.login = LogInFrame(self)
        self.add_account = AddAccount(self)
        self.remove_account = RemoveAccount(self)
        self.reveal_account = RevealAccount(self)
        self.manager = PasswordManager(self)
        self.login.show()
        # self.wm_attributes("-topmost", 1)
        # self.grid_rowconfigure(3, weight=1)

    def change_frame(self, frame):
        frame.show()
        print(self.grid_slaves())
        for slaves in self.grid_slaves():
            if slaves != frame:
                slaves.grid_forget()

        print(self.grid_slaves())

class LogInFrame(ttk.Frame):
    def __init__(self, master, **options):
        super().__init__(master, **options)
        self.y_padding, self.x_padding = 30, 15
        self.reveal_password = False

        self.title = tk.Label(self, text="LOG IN", font=("bold", 15))
        self.user_name_label = tk.Label(self, text="User Name")
        self.user_name = tk.StringVar()
        self.name = tk.Entry(self, textvariable=self.user_name)
        self.user_password = tk.StringVar()
        self.password_label = tk.Label(self, text="Password")
        self.password = tk.Entry(self, textvariable=self.user_password, show="•", name="password")
        self.show_password_button = tk.Button(self, text="👁", font=("bold", 7))
        self.button = tk.Button(self, text="Log In", command=self.validate)
        self.forgot_password = tk.Label(self, text="Forgot Password", font=('Helvetica 7 underline'))
        self.create_user = tk.Label(self, text="Create User", font=('Helvetica 7 underline'))

        utils.show_password(self.show_password_button, self.password)
        self.forgot_password.bind("<Button>", lambda e, f=self.master.forgot_password: self.master.change_frame(f))
        self.create_user.bind("<Button>", lambda e, f=self.master.create_user:self.master.change_frame(f))

    def show(self):
        self.grid(row=0, column=0, sticky="nsew", padx=self.x_padding, pady=self.y_padding)
        self.grid_columnconfigure(0, weight=1)

        self.title.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/6)
        self.user_name_label.grid(row=1, columnspan=3, column=0, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/6)
        self.password_label.grid(row=3, columnspan=3, column=0, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/6)
        self.name.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/6)
        self.password.grid(row=4, column=0, columnspan=2, sticky="nsew",padx=self.x_padding/3, pady=self.y_padding/6)
        self.show_password_button.grid(row=4, column=2, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/6)
        self.button.grid(row=5, column=0, columnspan=3, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/6 )
        self.create_user.grid(row=6, column=0, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/6)
        self.forgot_password.grid(row=6, column=1, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/6)

    def validate(self):
        print(self.user_name.get(), self.user_password.get())
        self.master.change_frame(self.master.manager)

    def grid_forget(self):
        super().grid_forget()
        for slave in self.grid_slaves():
            if isinstance(slave, tk.Entry):
                slave.delete(0, tk.END)
                if slave._name == "password":
                    slave.config(show="•")
            elif isinstance(slave, tk.Button):
                slave.config(relief="raised")

class CreateUser(ttk.Frame):
    def __init__(self, master, **options):
        super().__init__(master, **options)
        self.y_padding, self.x_padding = 15, 15
        self.reveal_password = False

        self.title = tk.Label(self, text="Create User", font=("bold", 15))
        self.username_label = tk.Label(self, text="User Name")
        self.password_label = tk.Label(self, text="Password")
        self.confirm_password_label = tk.Label(self, text="Confirm Password")
        self.username_text_variable = tk.StringVar()
        self.password_text_variable = tk.StringVar()
        self.confirm_password_text_variable = tk.StringVar()
        self.username = tk.Entry(self, textvariable=self.username_text_variable)
        self.password = tk.Entry(self, textvariable=self.password_text_variable, show="•", name="password1")
        self.confirm_password = tk.Entry(self, textvariable=self.confirm_password_text_variable, show="•", name="password")
        self.show_password_button_0 = tk.Button(self, text="👁", font=("bold", 7))
        self.show_password_button_1 = tk.Button(self, text="👁", font=("bold", 7))
        self.confirm = tk.Button(self, text="Confirm")
        self.back = tk.Button(self, text="🡨 Return", command=self.back)

        utils.show_password(self.show_password_button_0, self.password)
        utils.show_password(self.show_password_button_1, self.confirm_password)

    def show(self):
        self.grid(row=0, column=0, sticky="nsew", padx=self.x_padding, pady=self.y_padding)
        self.columnconfigure(0, weight=1)

        self.title.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.username_label.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.username.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.password_label.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.password.grid(row=4, column=0, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.show_password_button_0.grid(row=4, column=1, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.confirm_password_label.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.confirm_password.grid(row=6, column=0, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.show_password_button_1.grid(row=6, column=1, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.confirm.grid(row=7, column=0, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.back.grid(row=7, column=1, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)

    def back(self):
        self.master.change_frame(self.master.login)

    def grid_forget(self):
        super().grid_forget()
        for slave in self.grid_slaves():
            if isinstance(slave, tk.Entry):
                slave.delete(0, tk.END)
                if re.search("^password", str(slave._name)):
                    print(slave)
                    slave.config(show="•")
            elif isinstance(slave, tk.Button):
                slave.config(relief="raised")

class ForgotPassword(CreateUser):
    def __init__(self, master, **options):
        super().__init__(master, **options)
        self.title = tk.Label(self, text="Password Reset", font=("bold", 15))
        self.username_label = tk.Label(self, text="User Name")
        self.password_label = tk.Label(self, text="New Password")

class PasswordManager(ttk.Frame):
    def __init__(self, master, **options):
        super().__init__(master, **options)
        self.y_padding, self.x_padding = 60, 15

        self.title = tk.Label(self, text="PASSWORD MANAGER", font=("bold", 15))
        self.add = tk.Button(self, text="Add Account", command=lambda frame=self.master.add_account: self.master.change_frame(frame))
        self.recover = tk.Button(self, text="Reveal Account", command=lambda frame=self.master.reveal_account: self.master.change_frame(frame))
        self.remove = tk.Button(self, text="Remove Account", command=lambda frame=self.master.remove_account: self.master.change_frame(frame))
        self.back = tk.Button(self, text="🡨 Return", command=self.back)

    def show(self):
        self.grid(row=0, column=0, sticky="nsew", padx=self.x_padding, pady=self.y_padding)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.title.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.add.grid(row=1, column=0, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.recover.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.back.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.remove.grid(row=1, column=1, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)

    def back(self):
        self.master.change_frame(self.master.login)

class AddAccount(ttk.Frame):
    def __init__(self, master, **options):
        super().__init__(master, **options)
        self.y_padding, self.x_padding = 15, 15
        self.reveal_password = False

        self.title = tk.Label(self, text="Add Account", font=("bold", 15))
        self.appname_label = tk.Label(self, text="App Name")
        self.username_label = tk.Label(self, text="User Name")
        self.password_label = tk.Label(self, text="Password")
        self.confirm_password_label = tk.Label(self, text="Confirm Password")
        self.appname_text_variable = tk.StringVar()
        self.username_text_variable = tk.StringVar()
        self.password_text_variable = tk.StringVar()
        self.confirm_password_text_variable = tk.StringVar()
        self.appname = tk.Entry(self, textvariable=self.appname_text_variable)
        self.username = tk.Entry(self, textvariable=self.username_text_variable)
        self.password = tk.Entry(self, textvariable=self.password_text_variable, show="•", name="password1")
        self.confirm_password = tk.Entry(self, textvariable=self.confirm_password_text_variable, show="•", name="password")
        self.show_password_button_0 = tk.Button(self, text="👁", font=("bold", 7))
        self.show_password_button_1 = tk.Button(self, text="👁", font=("bold", 7))
        self.confirm = tk.Button(self, text="Confirm")
        self.back = tk.Button(self, text="🡨 Return", command=self.back)

        utils.show_password(self.show_password_button_0, self.password)
        utils.show_password(self.show_password_button_1, self.confirm_password)

    def show(self):
        self.grid(row=0, column=0, sticky="nsew", padx=self.x_padding, pady=self.y_padding)
        self.columnconfigure(0, weight=1)

        self.title.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.appname_label.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.appname.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.username_label.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.username.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.password_label.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.password.grid(row=6, column=0, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.show_password_button_0.grid(row=6, column=1, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.confirm_password_label.grid(row=7, column=0, columnspan=2, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.confirm_password.grid(row=8, column=0, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.show_password_button_1.grid(row=8, column=1, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.confirm.grid(row=9, column=0, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)
        self.back.grid(row=9, column=1, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/7)

    def back(self):
        self.master.change_frame(self.master.manager)

    def grid_forget(self):
        super().grid_forget()
        for slave in self.grid_slaves():
            if isinstance(slave, tk.Entry):
                slave.delete(0, tk.END)
                if re.search("^password", str(slave._name)):
                    slave.config(show="•")
            elif isinstance(slave, tk.Button):
                slave.config(relief="raised")

class RemoveAccount(ttk.Frame):
    def __init__(self, master, **options):
        super().__init__(master, **options)
        self.y_padding, self.x_padding = 15, 15

        self.title = tk.Label(self, text="Remove Account", font=("bold", 15))
        self.appname_label = tk.Label(self, text="App Name")
        self.username_label = tk.Label(self, text="User Name")
        self.password_label = tk.Label(self, text="Password")
        self.app_text_variable = tk.StringVar()
        self.app = ttk.Combobox(self, textvariable=self.app_text_variable, state="readonly")
        self.username_text_variable = tk.StringVar()
        self.username = ttk.Combobox(self, textvariable=self.username_text_variable, state="readonly")
        self.password_text_variable = tk.StringVar()
        self.password = tk.Entry(self, textvariable=self.password_text_variable, show="•", name="password")
        self.show_password_button = tk.Button(self, text="👁", font=("bold", 7))
        self.confirm = tk.Button(self, text="Confirm")
        self.back = tk.Button(self, text="🡨 Return", command=self.back)

        utils.show_password(self.show_password_button, self.password)
    
    def show(self):
        self.grid(row=0, column=0, sticky="nsew", padx=self.x_padding, pady=self.y_padding)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.app_text_variable.set("-")
        self.username_text_variable.set("-")

        self.title.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/4)
        self.appname_label.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/4)
        self.app.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/4)
        self.username_label.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/4)
        self.username.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/4)
        self.password_label.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/4)
        self.password.grid(row=6, column=0, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/4)
        self.show_password_button.grid(row=6, column=1, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/4)
        self.confirm.grid(row=7, column=0, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/4)
        self.back.grid(row=7, column=1, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/4)

    def back(self):
        self.master.change_frame(self.master.manager)

    def validate(self):
        print("DELETED!")

    def grid_forget(self):
        super().grid_forget()
        for slave in self.grid_slaves():
            if isinstance(slave, tk.Entry):
                slave.delete(0, tk.END)
                if re.search("^password", str(slave._name)):
                    slave.config(show="•")
            elif isinstance(slave, tk.Button):
                slave.config(relief="raised")

class RevealAccount(ttk.Frame):
    def __init__(self, master, **options):
        super().__init__(master, **options)
        self.y_padding, self.x_padding = 15, 15
        self.reveal_password = False

        self.title = tk.Label(self, text="Reveal Account", font=("bold", 15))
        self.appname_label = tk.Label(self, text="App Name")
        self.username_label = tk.Label(self, text="User Name")
        self.password_label = tk.Label(self, text="Password")
        self.app_text_variable = tk.StringVar()
        self.app = ttk.Combobox(self, textvariable=self.app_text_variable, state="readonly")
        self.username_text_variable = tk.StringVar()
        self.username = ttk.Combobox(self, textvariable=self.username_text_variable, state="readonly")
        self.password_text_variable = tk.StringVar()
        self.password = tk.Entry(self, textvariable=self.password_text_variable, state="readonly", name="password")
        self.show_password_button = tk.Button(self, text="👁", font=("bold", 7))
        self.copy_password_button = tk.Button(self, text="Copy", height=1)
        self.back_button = tk.Button(self, text="🡨 Return", command=self.back)

        utils.show_password(self.show_password_button, self.password)
    
    def show(self):
        self.grid(row=0, column=0, sticky="nsew", padx=self.x_padding, pady=self.y_padding)
        self.grid_columnconfigure(0, weight=1)

        self.app_text_variable.set("-")
        self.username_text_variable.set("-")

        self.title.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/5)
        self.appname_label.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/5)
        self.app.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/5)
        self.username_label.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/5)
        self.username.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/5)
        self.password_label.grid(row=5, column=0, columnspan=3, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/5)
        self.password.grid(row=6, column=0, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/5)
        self.show_password_button.grid(row=6, column=1, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/5)
        self.copy_password_button.grid(row=6, column=2, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/5)
        self.back_button.grid(row=7, column=0, columnspan=3, sticky="nsew", padx=self.x_padding/3, pady=self.y_padding/5)

    def back(self):
        self.master.change_frame(self.master.manager)

    def grid_forget(self):
        super().grid_forget()
        for slave in self.grid_slaves():
            if isinstance(slave, tk.Entry):
                slave.delete(0, tk.END)
                if re.search("^password", str(slave._name)):
                    slave.config(show="•")
            elif isinstance(slave, tk.Button):
                slave.config(relief="raised")

def start():
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    start()