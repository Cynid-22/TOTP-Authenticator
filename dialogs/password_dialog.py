import customtkinter as ctk
from constants import COLOR_TEXT, COLOR_BG_CARD, COLOR_ACCENT

class ChangePasswordDialog:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

    def show(self):
        # Create dialog
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Change Password")
        dialog.geometry("350x450")
        dialog.resizable(False, False)
        dialog.attributes("-topmost", True)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (350 // 2)
        y = (dialog.winfo_screenheight() // 2) - (450 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        frame = ctk.CTkFrame(dialog, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="Change Master Password", font=("Roboto", 16, "bold"), text_color=COLOR_TEXT).pack(pady=(0, 20))
        
        # Current Password
        ctk.CTkLabel(frame, text="Current Password:", text_color=COLOR_TEXT).pack(anchor="w", pady=(0, 5))
        entry_current = ctk.CTkEntry(frame, width=300, show="*")
        entry_current.pack(pady=(0, 15))
        
        # New Password
        ctk.CTkLabel(frame, text="New Password:", text_color=COLOR_TEXT).pack(anchor="w", pady=(0, 5))
        entry_new = ctk.CTkEntry(frame, width=300, show="*")
        entry_new.pack(pady=(0, 15))
        
        # Repeat New Password
        ctk.CTkLabel(frame, text="Repeat New Password:", text_color=COLOR_TEXT).pack(anchor="w", pady=(0, 5))
        entry_repeat = ctk.CTkEntry(frame, width=300, show="*")
        entry_repeat.pack(pady=(0, 15))
        
        # Message label (for errors and success)
        lbl_message = ctk.CTkLabel(frame, text="", text_color="red")
        lbl_message.pack(pady=5)
        
        # Buttons frame and buttons (created before function so we can modify them)
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        btn_change = ctk.CTkButton(btn_frame, text="Change Password", width=140, height=36)
        btn_change.pack(side="left", padx=5)
        
        btn_cancel = ctk.CTkButton(btn_frame, text="Cancel", width=140, height=36, fg_color="transparent", border_width=1, command=dialog.destroy)
        btn_cancel.pack(side="left", padx=5)
        
        def change_password():
            current = entry_current.get()
            new = entry_new.get()
            repeat = entry_repeat.get()
            
            # Validate current password
            if not self.app.storage.unlock(current):
                lbl_message.configure(text="Current password is incorrect", text_color="red")
                return
            
            # Validate new password
            if not new:
                lbl_message.configure(text="New password cannot be empty", text_color="red")
                return
            
            if new != repeat:
                lbl_message.configure(text="New passwords do not match", text_color="red")
                return
            
            # Change password
            try:
                # Load current accounts
                accounts = self.app.storage.load_accounts()
                
                # Re-encrypt with new password
                self.app.storage.unlock(new)
                self.app.storage.save_accounts(accounts, new)
                
                # Update current password
                self.app.password = new
                
                # Show success state inline
                # Disable all input fields
                entry_current.configure(state="disabled")
                entry_new.configure(state="disabled")
                entry_repeat.configure(state="disabled")
                
                # Show success message
                lbl_message.configure(text="Password changed successfully!", text_color="#00ff00")
                
                # Grey out cancel button
                btn_cancel.configure(state="disabled", fg_color="gray40", border_color="gray40")
                
                # Change the "Change Password" button to "OK" and make it close the dialog
                btn_change.configure(text="OK", command=dialog.destroy)
                
            except Exception as e:
                lbl_message.configure(text=f"Error: {str(e)}", text_color="red")
        
        # Configure the change button command
        btn_change.configure(command=change_password)
