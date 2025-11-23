import customtkinter as ctk
from core.constants import COLOR_TEXT
from ui.dialogs.base_dialog import BaseDialog

class AutoLockDialog(BaseDialog):
    def __init__(self, parent, config):
        super().__init__(parent, "Auto-Lock Settings", width=400, height=280)
        self.config = config

    def setup_ui(self):
        frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="Auto-Lock Settings", font=("Roboto", 16, "bold"), text_color=COLOR_TEXT).pack(pady=(0, 10))
        
        info_text = "The app will automatically lock after being inactive for the specified time."
        ctk.CTkLabel(frame, text=info_text, font=("Roboto", 12), text_color=COLOR_TEXT, wraplength=360).pack(pady=(0, 20))
        
        # Minutes setting
        setting_frame = ctk.CTkFrame(frame, fg_color="transparent")
        setting_frame.pack(pady=10)
        
        ctk.CTkLabel(setting_frame, text="Lock after (minutes):", text_color=COLOR_TEXT).grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        self.entry_minutes = ctk.CTkEntry(setting_frame, width=80)
        self.entry_minutes.insert(0, str(self.config.auto_lock_minutes))
        self.entry_minutes.grid(row=0, column=1, sticky="w")
        
        ctk.CTkLabel(setting_frame, text="(0 = disabled)", text_color="#888888", font=("Roboto", 10)).grid(row=0, column=2, sticky="w", padx=5)
        
        # Error label
        self.lbl_error = ctk.CTkLabel(frame, text="", text_color="red")
        self.lbl_error.pack(pady=5)
        
        # Buttons
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(btn_frame, text="Save", width=100, command=self.save_settings).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Cancel", width=100, fg_color="transparent", border_width=1, command=self.destroy).pack(side="left", padx=5)

    def save_settings(self):
        try:
            minutes = int(self.entry_minutes.get())
            if minutes < 0:
                self.lbl_error.configure(text="Minutes cannot be negative")
                return
            
            self.config.auto_lock_minutes = minutes
            self.config.save()
            self.destroy()
        except ValueError:
            self.lbl_error.configure(text="Please enter a valid number")
