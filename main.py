import customtkinter as ctk
import os
from auth_engine import AuthEngine
from storage import Storage
from ui_components import AccountFrame, COLOR_TEXT, COLOR_BG_CARD, COLOR_ACCENT

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("TOTP Authenticator")
        self.geometry("400x600")
        self.resizable(False, False)
        
        # Set Window Icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icon.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        # Backend Setup
        # Fix path to be relative to this script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        storage_path = os.path.join(base_dir, "accounts.json")
        
        self.auth_engine = AuthEngine()
        self.storage = Storage(filepath=storage_path)
        self.password = None
        self.accounts = []

        # Container for frames
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.current_frame = None

        self.is_edit_mode = False

        # Start with Login/Setup
        if os.path.exists(self.storage.filepath):
            self.show_login_screen()
        else:
            self.show_setup_screen()
            
        # Start Timer Loop
        self.update_timer()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_container()
        
        frame = ctk.CTkFrame(self.container, fg_color="transparent")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="Welcome Back", font=("Roboto", 24, "bold"), text_color=COLOR_TEXT).pack(pady=20)
        
        self.entry_password = ctk.CTkEntry(frame, show="*", width=220, placeholder_text="Enter Password")
        self.entry_password.pack(pady=10)
        self.entry_password.bind("<Return>", self.login)
        
        ctk.CTkButton(frame, text="Unlock", width=220, command=self.login).pack(pady=10)
        
        self.lbl_error = ctk.CTkLabel(frame, text="", text_color="red")
        self.lbl_error.pack(pady=5)

    def show_setup_screen(self):
        self.clear_container()
        
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

    def show_main_screen(self):
        self.clear_container()
        self.is_edit_mode = False
        
        # Header
        header = ctk.CTkFrame(self.container, height=60, corner_radius=0, fg_color="transparent")
        header.pack(fill="x", side="top")
        
        # Hamburger Menu Button
        self.btn_menu = ctk.CTkButton(header, text="☰", width=40, font=("Roboto", 24), fg_color="transparent", text_color=COLOR_TEXT, command=self.show_menu, hover=False)
        self.btn_menu.pack(side="left", padx=20, pady=15)
        
        self.btn_add = ctk.CTkButton(header, text="+", width=40, command=self.show_add_account_screen)
        self.btn_add.pack(side="right", padx=(10, 20), pady=15)
        
        self.btn_edit = ctk.CTkButton(header, text="Edit", width=60, fg_color="transparent", border_width=1, text_color=COLOR_TEXT, command=self.toggle_edit_mode)
        self.btn_edit.pack(side="right", padx=0, pady=15)

        # Scrollable Account List
        self.scroll_frame = ctk.CTkScrollableFrame(self.container, width=380)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_account_list()

    def show_menu(self):
        """Show context menu with options"""
        # Create menu window
        menu = ctk.CTkToplevel(self)
        menu.overrideredirect(True)
        menu.attributes("-topmost", True)
        
        # Position near hamburger button
        x = self.btn_menu.winfo_rootx()
        y = self.btn_menu.winfo_rooty() + self.btn_menu.winfo_height() + 5
        menu.geometry(f"+{x}+{y}")
        
        # Menu items
        ctk.CTkButton(menu, text="Change Password", width=200, height=30, fg_color=COLOR_BG_CARD, hover_color=COLOR_ACCENT, text_color=COLOR_TEXT, command=lambda: [menu.destroy(), self.show_change_password_dialog()]).pack(pady=2)
        
        # Close menu when clicking outside or window moves
        def close_menu(event=None):
            if menu.winfo_exists():
                menu.destroy()
                # Unbind the configure event
                self.unbind("<Configure>")
        
        # Bind to main window click and window move
        self.bind("<Button-1>", close_menu, add="+")
        self.bind("<Configure>", close_menu)  # Close when window moves/resizes
        menu.bind("<FocusOut>", lambda e: close_menu())

    def show_add_account_screen(self):
        self.clear_container()
        
        frame = ctk.CTkFrame(self.container, fg_color="transparent")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="Add Account", font=("Roboto", 24, "bold"), text_color=COLOR_TEXT).pack(pady=20)
        
        self.entry_name = ctk.CTkEntry(frame, width=220, placeholder_text="Account Name (e.g. Google)")
        self.entry_name.pack(pady=10)
        
        self.entry_secret = ctk.CTkEntry(frame, width=220, placeholder_text="Secret Key")
        self.entry_secret.pack(pady=10)
        
        ctk.CTkButton(frame, text="Add", width=220, command=self.add_account).pack(pady=10)
        ctk.CTkButton(frame, text="Cancel", width=220, fg_color="transparent", border_width=1, text_color=COLOR_TEXT, command=self.show_main_screen).pack(pady=10)
        
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
        
        ctk.CTkLabel(self.frame_advanced, text="Period (s):", text_color=COLOR_TEXT).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)
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

    # --- Actions ---

    def login(self, event=None):
        password = self.entry_password.get()
        if self.storage.unlock(password):
            self.password = password
            self.accounts = self.storage.load_accounts()
            self.show_main_screen()
        else:
            self.lbl_error.configure(text="Incorrect password")

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
            self.password = password
            self.accounts = []
            self.storage.save_accounts(self.accounts, self.password)
            self.show_main_screen()

    def show_change_password_dialog(self):
        """Show dialog to change master password"""
        # Create dialog
        dialog = ctk.CTkToplevel(self)
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
        
        # Error label
        lbl_error = ctk.CTkLabel(frame, text="", text_color="red")
        lbl_error.pack(pady=5)
        
        def change_password():
            current = entry_current.get()
            new = entry_new.get()
            repeat = entry_repeat.get()
            
            # Validate current password
            if not self.storage.unlock(current):
                lbl_error.configure(text="Current password is incorrect")
                return
            
            # Validate new password
            if not new:
                lbl_error.configure(text="New password cannot be empty")
                return
            
            if new != repeat:
                lbl_error.configure(text="New passwords do not match")
                return
            
            # Change password
            try:
                # Load current accounts
                accounts = self.storage.load_accounts()
                
                # Re-encrypt with new password
                self.storage.unlock(new)
                self.storage.save_accounts(accounts, new)
                
                # Update current password
                self.password = new
                
                dialog.destroy()
                
                # Show success message
                success_msg = ctk.CTkToplevel(self)
                success_msg.title("Success")
                success_msg.geometry("300x150")
                success_msg.attributes("-topmost", True)
                ctk.CTkLabel(success_msg, text="Password changed successfully!", text_color=COLOR_TEXT).pack(pady=30)
                ctk.CTkButton(success_msg, text="OK", command=success_msg.destroy).pack()
                
            except Exception as e:
                lbl_error.configure(text=f"Error: {str(e)}")
        
        # Buttons
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        ctk.CTkButton(btn_frame, text="Change Password", width=140, height=36, command=change_password).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Cancel", width=140, height=36, fg_color="transparent", border_width=1, command=dialog.destroy).pack(side="left", padx=5)

    def toggle_edit_mode(self):
        self.is_edit_mode = not self.is_edit_mode
        
        if self.is_edit_mode:
            self.btn_edit.configure(text="Done", fg_color="#1f6aa5") # Highlight
            self.btn_add.pack_forget() # Hide +
            # Repack Done button with padding
            self.btn_edit.pack_forget()
            self.btn_edit.pack(side="right", padx=20, pady=15)
        else:
            self.btn_edit.configure(text="Edit", fg_color="transparent")
            # Fix button order: Unpack Edit, Pack Add, Pack Edit (to ensure [Edit] [+])
            self.btn_edit.pack_forget()
            self.btn_add.pack(side="right", padx=(10, 20), pady=15) # Show +
            self.btn_edit.pack(side="right", padx=0, pady=15)
        
        for frame in self.account_frames:
            frame.set_edit_mode(self.is_edit_mode)

    def add_account(self):
        name = self.entry_name.get()
        secret = self.entry_secret.get()
        
        if not name or not secret:
            self.lbl_error.configure(text="Fields cannot be empty")
            return

        # Validate Secret
        secret = secret.replace(" ", "").upper()
        if not self.auth_engine.validate_secret(secret):
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
        
        self.accounts.append(account)
        self.storage.save_accounts(self.accounts, self.password)
        self.show_main_screen()

    def delete_account(self, account_frame):
        try:
            index = self.account_frames.index(account_frame)
            self.accounts.pop(index)
            self.storage.save_accounts(self.accounts, self.password)
            self.refresh_account_list()
            
            # Restore edit mode state for the new frames
            if self.is_edit_mode:
                for frame in self.account_frames:
                    frame.set_edit_mode(True)
        except ValueError:
            print("Error: Account frame not found for deletion")

    # --- Drag and Drop Logic ---

    def drag_start(self, event, frame):
        self.drag_data = {"frame": frame, "start_y": event.y_root, "index": self.account_frames.index(frame)}
        frame.configure(fg_color="#444444") # Visual feedback
        
        # Create Ghost Window
        self.drag_window = ctk.CTkToplevel(self)
        self.drag_window.overrideredirect(True)
        self.drag_window.attributes("-alpha", 0.8)
        self.drag_window.attributes("-topmost", True)
        
        # Position it near cursor
        self.drag_window.geometry(f"+{event.x_root + 15}+{event.y_root + 10}")
        
        # Add Label to Ghost
        lbl = ctk.CTkLabel(self.drag_window, text=frame.name, font=("Roboto", 16, "bold"), text_color=COLOR_TEXT, fg_color="#2b2b2b", corner_radius=5)
        lbl.pack(padx=10, pady=5)

    def drag_motion(self, event, frame):
        if hasattr(self, 'drag_window') and self.drag_window:
            self.drag_window.geometry(f"+{event.x_root + 15}+{event.y_root + 10}")

    def drag_end(self, event, frame):
        frame.configure(fg_color="#2b2b2b") # Reset color
        
        # Destroy Ghost Window
        if hasattr(self, 'drag_window') and self.drag_window:
            self.drag_window.destroy()
            self.drag_window = None
        
        drop_y = event.y_root
        # Find target index based on y coordinate
        target_index = -1
        
        # Simple hit testing
        for i, f in enumerate(self.account_frames):
            f_y = f.winfo_rooty()
            f_height = f.winfo_height()
            if f_y <= drop_y <= f_y + f_height:
                target_index = i
                break
        
        if target_index == -1:
            # Check if dropped at very bottom or top
            if drop_y < self.account_frames[0].winfo_rooty():
                target_index = 0
            elif drop_y > self.account_frames[-1].winfo_rooty() + self.account_frames[-1].winfo_height():
                target_index = len(self.account_frames) - 1

        if target_index != -1 and target_index != self.drag_data["index"]:
            # Reorder
            item = self.accounts.pop(self.drag_data["index"])
            self.accounts.insert(target_index, item)
            self.storage.save_accounts(self.accounts, self.password)
            
            self.refresh_account_list()
            # Restore edit mode
            self.btn_edit.configure(text="Done")
            self.is_edit_mode = True
            for f in self.account_frames:
                f.set_edit_mode(True)

    def update_account_settings(self, account_frame, digits, period, algorithm):
        """Update TOTP settings for an existing account"""
        try:
            index = self.account_frames.index(account_frame)
            # Update account settings
            self.accounts[index]['digits'] = digits
            self.accounts[index]['interval'] = period
            self.accounts[index]['algorithm'] = algorithm
            # Save changes
            self.storage.save_accounts(self.accounts, self.password)
            # Update the frame's settings
            account_frame.digits = digits
            account_frame.interval = period
            account_frame.algorithm = algorithm
            # Force code to regenerate with new settings
            account_frame.update_code()
        except ValueError:
            print("Error: Account frame not found for settings update")

    def refresh_account_list(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.account_frames = []
        callbacks = {
            'delete': self.delete_account,
            'drag_start': self.drag_start,
            'drag_motion': self.drag_motion,
            'drag_end': self.drag_end,
            'update_settings': self.update_account_settings
        }
        
        for acc in self.accounts:
            # Pass the full account dict to AccountFrame
            frame = AccountFrame(self.scroll_frame, acc, self.auth_engine, callbacks)
            frame.pack(fill="x", pady=5)
            self.account_frames.append(frame)

    def update_timer(self):
        try:
            # Only update if we are on the main screen (i.e. have account frames)
            if hasattr(self, 'account_frames'):
                for frame in self.account_frames:
                    # Check if frame still exists to avoid errors during refresh
                    if frame.winfo_exists():
                        frame.update_code()
        except Exception as e:
            print(f"Timer Error: {e}")
            
        self.after(1000, self.update_timer)

if __name__ == "__main__":
    app = App()
    app.mainloop()
