import customtkinter as ctk
from tkinter import filedialog, messagebox
from constants import COLOR_TEXT, COLOR_BG_CARD, COLOR_ACCENT

class ExportDialog:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

    def show(self):
        # Create dialog
        dialog = ctk.CTkToplevel(self.parent)
        dialog.iconbitmap("assets/icon.ico")
        # Delay setting icon to prevent override
        dialog.after(200, dialog.iconbitmap, "assets/icon.ico")
        dialog.title("Export Accounts")
        dialog.geometry("350x250")
        dialog.resizable(False, False)
        dialog.attributes("-topmost", True)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (350 // 2)
        y = (dialog.winfo_screenheight() // 2) - (250 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        frame = ctk.CTkFrame(dialog, fg_color="transparent")
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
                parent=dialog
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
                defaultextension=def_ext,
                filetypes=filetypes,
                parent=dialog
            )
            
            if not filepath:
                return
                
            # Perform Export
            if self.app.storage.export_accounts(self.app.accounts, format_type, filepath):
                messagebox.showinfo("Success", "Accounts exported successfully!", parent=dialog)
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to export accounts.", parent=dialog)

        ctk.CTkButton(btn_frame, text="Export", width=140, height=36, fg_color="#ff5555", hover_color="#aa0000", command=export).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Cancel", width=140, height=36, fg_color="transparent", border_width=1, command=dialog.destroy).pack(side="left", padx=5)
