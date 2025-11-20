import customtkinter as ctk
from constants import COLOR_TEXT, COLOR_BG_CARD, COLOR_ACCENT
from ui_components import AccountFrame

class MainListScreen:
    def __init__(self, container, app):
        self.container = container
        self.app = app
        self.account_frames = []
        self.is_edit_mode = False

    def show(self):
        self.is_edit_mode = False
        
        # Header
        header = ctk.CTkFrame(self.container, height=60, corner_radius=0, fg_color="transparent")
        header.pack(fill="x", side="top")
        
        # Hamburger Menu Button
        self.btn_menu = ctk.CTkButton(header, text="☰", width=40, font=("Roboto", 24), fg_color="transparent", text_color=COLOR_TEXT, command=self.show_menu, hover=False)
        self.btn_menu.pack(side="left", padx=20, pady=15)
        
        self.btn_add = ctk.CTkButton(header, text="+", width=40, command=self.app.show_add_account_screen)
        self.btn_add.pack(side="right", padx=(10, 20), pady=15)
        
        self.btn_edit = ctk.CTkButton(header, text="Edit", width=60, fg_color="transparent", border_width=1, text_color=COLOR_TEXT, command=self.toggle_edit_mode)
        self.btn_edit.pack(side="right", padx=0, pady=15)

        # Scrollable Account List
        self.scroll_frame = ctk.CTkScrollableFrame(self.container, width=380)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_account_list()

    def update(self):
        """Called by App timer loop"""
        try:
            for frame in self.account_frames:
                if frame.winfo_exists():
                    frame.update_code()
        except Exception as e:
            print(f"Timer Error: {e}")

    def show_menu(self):
        """Show context menu with options"""
        # Create menu window
        menu = ctk.CTkToplevel(self.container)
        menu.overrideredirect(True)
        menu.attributes("-topmost", True)
        
        # Position near hamburger button
        x = self.btn_menu.winfo_rootx()
        y = self.btn_menu.winfo_rooty() + self.btn_menu.winfo_height() + 5
        menu.geometry(f"+{x}+{y}")
        
        # Menu items
        ctk.CTkButton(menu, text="Change Password", width=200, height=30, fg_color=COLOR_BG_CARD, hover_color=COLOR_ACCENT, text_color=COLOR_TEXT, command=lambda: [menu.destroy(), self.app.show_change_password_dialog()]).pack(pady=2)
        ctk.CTkButton(menu, text="Import Accounts", width=200, height=30, fg_color=COLOR_BG_CARD, hover_color=COLOR_ACCENT, text_color=COLOR_TEXT, command=lambda: [menu.destroy(), self.import_accounts()]).pack(pady=2)
        ctk.CTkButton(menu, text="Export Accounts", width=200, height=30, fg_color=COLOR_BG_CARD, hover_color=COLOR_ACCENT, text_color=COLOR_TEXT, command=lambda: [menu.destroy(), self.export_accounts()]).pack(pady=2)
        
        # Close menu when clicking outside or window moves
        def close_menu(event=None):
            if menu.winfo_exists():
                menu.destroy()
                # Unbind the configure event
                self.app.unbind("<Configure>")
        
        # Bind to main window click and window move
        # Note: self.app is the main window
        self.app.bind("<Button-1>", close_menu, add="+")
        self.app.bind("<Configure>", close_menu)  # Close when window moves/resizes
        menu.bind("<FocusOut>", lambda e: close_menu())

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

    def refresh_account_list(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.account_frames = []
        
        # Empty State
        if not self.app.accounts:
            frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            frame.pack(expand=True, pady=50)
            
            ctk.CTkLabel(frame, text="No accounts yet", font=("Roboto", 16), text_color=COLOR_TEXT).pack(pady=10)
            ctk.CTkButton(frame, text="Import Accounts", command=self.import_accounts).pack(pady=10)
            return

        callbacks = {
            'delete': self.delete_account,
            'move_up': self.move_up,
            'move_down': self.move_down,
            'update_settings': self.update_account_settings
        }
        
        for acc in self.app.accounts:
            # Pass the full account dict to AccountFrame
            frame = AccountFrame(self.scroll_frame, acc, self.app.auth_engine, callbacks)
            frame.pack(fill="x", pady=5)
            self.account_frames.append(frame)

    def import_accounts(self):
        from tkinter import filedialog, messagebox
        filepath = filedialog.askopenfilename(
            title="Import Accounts",
            filetypes=[("JSON/CSV Files", "*.json *.csv"), ("All Files", "*.*")]
        )
        
        if filepath:
            new_accounts = self.app.storage.import_accounts(filepath)
            if new_accounts:
                # Merge accounts (append)
                count = 0
                for acc in new_accounts:
                    # Simple duplicate check by secret
                    if not any(a['secret'] == acc['secret'] for a in self.app.accounts):
                        self.app.accounts.append(acc)
                        count += 1
                
                if count > 0:
                    self.app.storage.save_accounts(self.app.accounts, self.app.password)
                    self.refresh_account_list()
                    messagebox.showinfo("Success", f"Imported {count} accounts.")
                else:
                    messagebox.showinfo("Info", "No new accounts found (duplicates skipped).")
            else:
                messagebox.showerror("Error", "Failed to import accounts. Check file format.")

    def export_accounts(self):
        from dialogs.export_dialog import ExportDialog
        dialog = ExportDialog(self.container, self.app)
        dialog.show()

    def delete_account(self, account_frame):
        try:
            index = self.account_frames.index(account_frame)
            self.app.accounts.pop(index)
            self.app.storage.save_accounts(self.app.accounts, self.app.password)
            self.refresh_account_list()
            
            # Restore edit mode state for the new frames
            if self.is_edit_mode:
                for frame in self.account_frames:
                    frame.set_edit_mode(True)
        except ValueError:
            print("Error: Account frame not found for deletion")

    def move_up(self, account_frame):
        try:
            index = self.account_frames.index(account_frame)
            if index > 0:
                # Swap with previous item
                self.app.accounts[index], self.app.accounts[index - 1] = self.app.accounts[index - 1], self.app.accounts[index]
                self.app.storage.save_accounts(self.app.accounts, self.app.password)
                self.refresh_account_list()
                
                # Restore edit mode
                if self.is_edit_mode:
                    for f in self.account_frames:
                        f.set_edit_mode(True)
        except ValueError:
            print("Error: Account frame not found")

    def move_down(self, account_frame):
        try:
            index = self.account_frames.index(account_frame)
            if index < len(self.account_frames) - 1:
                # Swap with next item
                self.app.accounts[index], self.app.accounts[index + 1] = self.app.accounts[index + 1], self.app.accounts[index]
                self.app.storage.save_accounts(self.app.accounts, self.app.password)
                self.refresh_account_list()
                
                # Restore edit mode
                if self.is_edit_mode:
                    for f in self.account_frames:
                        f.set_edit_mode(True)
        except ValueError:
            print("Error: Account frame not found")

    def update_account_settings(self, account_frame, digits, period, algorithm):
        """Update TOTP settings for an existing account"""
        try:
            index = self.account_frames.index(account_frame)
            # Update account settings
            self.app.accounts[index]['digits'] = digits
            self.app.accounts[index]['interval'] = period
            self.app.accounts[index]['algorithm'] = algorithm
            # Save changes
            self.app.storage.save_accounts(self.app.accounts, self.app.password)
            # Update the frame's settings
            account_frame.digits = digits
            account_frame.interval = period
            account_frame.algorithm = algorithm
            # Force code to regenerate with new settings
            account_frame.update_code()
        except ValueError:
            print("Error: Account frame not found for settings update")
