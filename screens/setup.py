import customtkinter as ctk
from constants import COLOR_TEXT

class SetupScreen:
    def __init__(self, container, storage, on_success):
        self.container = container
        self.storage = storage
        self.on_success = on_success # callback(password, accounts)

    def show(self):
        frame = ctk.CTkFrame(self.container, fg_color="transparent")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="Create Vault", font=("Roboto", 24, "bold"), text_color=COLOR_TEXT).pack(pady=20)
        ctk.CTkLabel(frame, text="Set a secure password", text_color=COLOR_TEXT).pack(pady=(0, 20))
        
        self.entry_password = ctk.CTkEntry(frame, show="*", width=220, placeholder_text="New Password")
        self.entry_password.pack(pady=10)
        
        self.entry_confirm = ctk.CTkEntry(frame, show="*", width=220, placeholder_text="Confirm Password")
        self.entry_confirm.pack(pady=10)
        self.entry_confirm.bind("<Return>", self.setup_vault)
        
        ctk.CTkButton(frame, text="Create Vault", width=220, command=self.setup_vault).pack(pady=10)
        
        self.lbl_error = ctk.CTkLabel(frame, text="", text_color="red")
        self.lbl_error.pack(pady=5)

    def setup_vault(self, event=None):
        password = self.entry_password.get()
        confirm = self.entry_confirm.get()
        
        if not password:
            self.lbl_error.configure(text="Password cannot be empty")
            return
            
        if password != confirm:
            self.lbl_error.configure(text="Passwords do not match")
            return
        
        if self.storage.unlock(password):
            accounts = []
            self.storage.save_accounts(accounts, password)
            self.on_success(password, accounts)
