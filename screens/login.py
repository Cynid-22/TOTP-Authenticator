import customtkinter as ctk
from constants import COLOR_TEXT

class LoginScreen:
    def __init__(self, container, storage, on_success):
        self.container = container
        self.storage = storage
        self.on_success = on_success # callback(password, accounts)

    def show(self):
        frame = ctk.CTkFrame(self.container, fg_color="transparent")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="Welcome Back", font=("Roboto", 24, "bold"), text_color=COLOR_TEXT).pack(pady=20)
        
        self.entry_password = ctk.CTkEntry(frame, show="*", width=220, placeholder_text="Enter Password")
        self.entry_password.pack(pady=10)
        self.entry_password.bind("<Return>", self.login)
        
        ctk.CTkButton(frame, text="Unlock", width=220, command=self.login).pack(pady=10)
        
        self.lbl_error = ctk.CTkLabel(frame, text="", text_color="red")
        self.lbl_error.pack(pady=5)

    def login(self, event=None):
        password = self.entry_password.get()
        if self.storage.unlock(password):
            accounts = self.storage.load_accounts()
            self.on_success(password, accounts)
        else:
            self.lbl_error.configure(text="Incorrect password")
