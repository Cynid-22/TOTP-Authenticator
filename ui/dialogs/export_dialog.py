import customtkinter as ctk
from tkinter import filedialog, messagebox
from core.constants import COLOR_TEXT
from ui.dialogs.base_dialog import BaseDialog

class ExportDialog(BaseDialog):
    def __init__(self, parent, app):
        super().__init__(parent, "Export Accounts", width=350, height=250)
        self.app = app

    def setup_ui(self):
        frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="Export Accounts", font=("Roboto", 16, "bold"), text_color=COLOR_TEXT).pack(pady=(0, 20))
        
        # Format Selection
        ctk.CTkLabel(frame, text="Select Format:", text_color=COLOR_TEXT).pack(anchor="w", pady=(0, 5))
        combo_format = ctk.CTkComboBox(frame, values=["JSON", "CSV"], width=300)
        combo_format.set("JSON")
        combo_format.pack(pady=(0, 20))
        
        # Buttons
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        def export():
            format_type = combo_format.get().lower()
            
            # WARNING PROMPT
            confirm = messagebox.askyesno(
                "WARNING: Unencrypted Export", 
                "You are about to export your accounts to an unencrypted file.\n\n"
                "ANYONE who accesses this file will be able to generate your TOTP codes.\n\n"
                "Do you want to proceed?",
                icon='warning',
                parent=self.dialog
            )
            
            if not confirm:
                return

            # File Save Dialog
            filetypes = []
            if format_type == 'json':
                filetypes = [("JSON Files", "*.json")]
                def_ext = ".json"
            else:
                filetypes = [("CSV Files", "*.csv")]
                def_ext = ".csv"
                
            filepath = filedialog.asksaveasfilename(
                title="Export Accounts",
                initialfile="TOTP_Export_DO_NOT_SHARE",
                defaultextension=def_ext,
                filetypes=filetypes,
                parent=self.dialog
            )
            
            if not filepath:
                return
                
            # Perform Export
            if self.app.storage.export_accounts(self.app.accounts, format_type, filepath):
                messagebox.showinfo("Success", "Accounts exported successfully!", parent=self.dialog)
                self.destroy()
            else:
                messagebox.showerror("Error", "Failed to export accounts.", parent=self.dialog)

        ctk.CTkButton(btn_frame, text="Export", width=140, height=36, fg_color="#ff5555", hover_color="#aa0000", command=export).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Cancel", width=140, height=36, fg_color="transparent", border_width=1, command=self.destroy).pack(side="left", padx=5)
