import customtkinter as ctk
from core.constants import COLOR_TEXT

class AddAccountScreen:
    def __init__(self, container, app):
        self.container = container
        self.app = app

    def show(self):
        frame = ctk.CTkFrame(self.container, fg_color="transparent")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="Add Account", font=("Roboto", 24, "bold"), text_color=COLOR_TEXT).pack(pady=20)
        
        self.entry_name = ctk.CTkEntry(frame, width=220, placeholder_text="Account Name (e.g. Google)")
        self.entry_name.pack(pady=10)
        
        self.entry_secret = ctk.CTkEntry(frame, width=220, placeholder_text="Secret Key")
        self.entry_secret.pack(pady=10)
        
        ctk.CTkButton(frame, text="Add", width=220, command=self.add_account).pack(pady=10)
        ctk.CTkButton(frame, text="Cancel", width=220, fg_color="transparent", border_width=1, text_color=COLOR_TEXT, command=self.app.show_main_screen).pack(pady=10)
        
        # Advanced Options Toggle Button
        self.advanced_expanded = False
        self.btn_advanced = ctk.CTkButton(frame, text="∨ Advanced Options", width=220, fg_color="transparent", text_color=COLOR_TEXT, command=self.toggle_advanced_options, hover=False)
        self.btn_advanced.pack(pady=(5, 0))
        
        # Advanced Options Frame (Hidden by default)
        self.frame_advanced = ctk.CTkFrame(frame, fg_color="transparent")
        
        ctk.CTkLabel(self.frame_advanced, text="Digits:", text_color=COLOR_TEXT).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=5)
        self.entry_digits = ctk.CTkEntry(self.frame_advanced, width=60)
        self.entry_digits.insert(0, "6")
        self.entry_digits.grid(row=0, column=1, sticky="w", pady=5)
        ctk.CTkLabel(self.frame_advanced, text="(1-9)", text_color="#888888", font=("Roboto", 10)).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        
        ctk.CTkLabel(self.frame_advanced, text="Period:", text_color=COLOR_TEXT).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)
        self.entry_period = ctk.CTkEntry(self.frame_advanced, width=60)
        self.entry_period.insert(0, "30")
        self.entry_period.grid(row=1, column=1, sticky="w", pady=5)
        ctk.CTkLabel(self.frame_advanced, text="(1-120)", text_color="#888888", font=("Roboto", 10)).grid(row=1, column=2, sticky="w", padx=5, pady=5)
        
        ctk.CTkLabel(self.frame_advanced, text="Algorithm:", text_color=COLOR_TEXT).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=5)
        self.combo_algorithm = ctk.CTkComboBox(self.frame_advanced, values=["SHA1", "SHA256", "SHA512"], width=120)
        self.combo_algorithm.set("SHA1")
        self.combo_algorithm.grid(row=2, column=1, columnspan=2, sticky="w", pady=5)
        
        self.lbl_error = ctk.CTkLabel(frame, text="", text_color="red")
        self.lbl_error.pack(pady=5)

    def toggle_advanced_options(self):
        self.advanced_expanded = not self.advanced_expanded
        if self.advanced_expanded:
            self.btn_advanced.configure(text="∧ Advanced Options")
            self.frame_advanced.pack(pady=10)
        else:
            self.btn_advanced.configure(text="∨ Advanced Options")
            self.frame_advanced.pack_forget()

    def add_account(self):
        name = self.entry_name.get()
        secret = self.entry_secret.get()
        
        if not name or not secret:
            self.lbl_error.configure(text="Fields cannot be empty")
            return

        # Validate Secret
        secret = secret.replace(" ", "").upper()
        if not self.app.auth_engine.validate_secret(secret):
            self.lbl_error.configure(text="Invalid Secret Key")
            return
        
        # Get advanced settings (if expanded)
        if self.advanced_expanded:
            try:
                digits = int(self.entry_digits.get())
                if not (1 <= digits <= 9):
                    self.lbl_error.configure(text="Digits must be 1-9")
                    return
            except ValueError:
                self.lbl_error.configure(text="Digits must be a number")
                return
            
            try:
                period = int(self.entry_period.get())
                if not (1 <= period <= 120):
                    self.lbl_error.configure(text="Period must be 1-120")
                    return
            except ValueError:
                self.lbl_error.configure(text="Period must be a number")
                return
            
            algorithm = self.combo_algorithm.get()
        else:
            # Use defaults
            digits = 6
            period = 30
            algorithm = "SHA1"
        
        # Create account with all settings
        account = {
            'name': name,
            'secret': secret,
            'digits': digits,
            'interval': period,
            'algorithm': algorithm
        }
        
        self.app.accounts.append(account)
        self.app.storage.save_accounts(self.app.accounts, self.app.password)
        self.app.show_main_screen()
