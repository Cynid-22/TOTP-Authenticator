import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from core.constants import COLOR_TEXT
from ui.dialogs.base_dialog import BaseDialog

class ExportDialog(BaseDialog):
    def __init__(self, parent, app):
        super().__init__(parent, "Export Warning", width=400, height=300)
        self.app = app
        self.countdown = 5

    def setup_ui(self):
        frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Warning Icon (using emoji for simplicity, or could load an icon)
        ctk.CTkLabel(frame, text="⚠️", font=("Roboto", 48)).pack(pady=(0, 10))
        
        ctk.CTkLabel(frame, text="WARNING: Unencrypted Export", font=("Roboto", 20, "bold"), text_color="#ff5555").pack(pady=(0, 10))
        
        warning_text = (
            "You are about to export your accounts to an unencrypted file.\n\n"
            "ANYONE who accesses this file will be able to generate your TOTP codes."
        )
        ctk.CTkLabel(frame, text=warning_text, font=("Roboto", 14), text_color=COLOR_TEXT, wraplength=360).pack(pady=(0, 20))
        
        # Buttons
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        self.btn_export = ctk.CTkButton(btn_frame, text=f"Export ({self.countdown})", width=140, height=36, fg_color="#ff5555", hover_color="#aa0000", state="disabled", command=self.export)
        self.btn_export.pack(side="left", padx=5)
        
        ctk.CTkButton(btn_frame, text="Cancel", width=140, height=36, fg_color="transparent", border_width=1, command=self.destroy).pack(side="left", padx=5)
        
        # Start countdown
        self.update_countdown()

    def update_countdown(self):
        if self.countdown > 0:
            self.btn_export.configure(text=f"Export ({self.countdown})")
            self.countdown -= 1
            self.dialog.after(1000, self.update_countdown)
        else:
            self.btn_export.configure(text="Export", state="normal")

    def export(self):
        # Open native file save dialog
        filepath = filedialog.asksaveasfilename(
            title="Export Accounts",
            initialfile="TOTP_Export_DO_NOT_SHARE",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("CSV Files", "*.csv")],
            parent=self.dialog
        )
        
        if not filepath:
            return
            
        # Determine format from extension
        _, ext = os.path.splitext(filepath)
        format_type = 'json' if ext.lower() == '.json' else 'csv'
        
        # Perform Export
        if self.app.storage.export_accounts(self.app.accounts, format_type, filepath):
            messagebox.showinfo("Success", "Accounts exported successfully!", parent=self.dialog)
            self.destroy()
        else:
            messagebox.showerror("Error", "Failed to export accounts.", parent=self.dialog)
