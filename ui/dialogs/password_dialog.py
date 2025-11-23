import customtkinter as ctk
from core.constants import COLOR_TEXT
from ui.dialogs.base_dialog import BaseDialog

class ChangePasswordDialog(BaseDialog):
    def __init__(self, parent, app):
        super().__init__(parent, "Change Password", width=350, height=450)
        self.app = app

    def setup_ui(self):
        frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="Change Master Password", font=("Roboto", 16, "bold"), text_color=COLOR_TEXT).pack(pady=(0, 20))
        
        # Current Password
        ctk.CTkLabel(frame, text="Current Password:", text_color=COLOR_TEXT).pack(anchor="w", pady=(0, 5))
        entry_current = ctk.CTkEntry(frame, width=300, show="*")
        entry_current.pack(pady=(0, 15))
        
        # New Password
        ctk.CTkLabel(frame, text="New Password:", text_color=COLOR_TEXT).pack(anchor="w", pady=(0, 5))
        ctk.CTkLabel(frame, text="(Recommended: 8+ characters)", text_color="#888888", font=("Roboto", 9)).pack(anchor="w", pady=(0, 5))
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
        
        btn_cancel = ctk.CTkButton(btn_frame, text="Cancel", width=140, height=36, fg_color="transparent", border_width=1, command=self.destroy)
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
                btn_change.configure(text="OK", command=self.destroy)
                
            except Exception:
                lbl_message.configure(text="Failed to change password", text_color="red")
        
        # Configure the change button command
        btn_change.configure(command=change_password)
