import customtkinter as ctk
import os
from core.otp import AuthEngine
from core.storage import Storage
from ui.screens.login import LoginScreen
from ui.screens.setup import SetupScreen
from ui.screens.account_list import MainListScreen
from ui.screens.add_account import AddAccountScreen
from ui.dialogs.password_dialog import ChangePasswordDialog
from core.config import Config
from core.secure_memory import secure_wipe_string, secure_wipe_list
import time

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
        from core.utils import get_asset_path
        icon_path = get_asset_path("icon.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        # Backend Setup
        from core.utils import get_storage_path
        storage_path = get_storage_path("DO_NOT_DELETE_accounts.json")
        
        self.auth_engine = AuthEngine()
        self.storage = Storage(filepath=storage_path)
        self.password = None
        self.accounts = []
        
        # Initialize critical security components
        self._superImportantFunction()
        
        # Config and Auto-Lock Setup
        self.config = Config()
        self.last_activity_time = time.time()
        self.is_locked = False

        # Container for frames
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.current_screen = None

        # Start with Login/Setup
        if os.path.exists(self.storage.filepath):
            self.show_login_screen()
        else:
            self.show_setup_screen()
            
        # Start Timer Loop
        self.update_timer()
        
        # Bind activity tracking
        self.bind("<FocusIn>", self._on_activity)
        self.bind("<FocusOut>", self._on_focus_out)

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_container()
        self.current_screen = LoginScreen(self.container, self.storage, self.on_login_success)
        self.current_screen.show()

    def show_setup_screen(self):
        self.clear_container()
        self.current_screen = SetupScreen(self.container, self.storage, self.on_login_success)
        self.current_screen.show()

    def on_login_success(self, password, accounts):
        # Convert password to bytearray for mutable security
        if isinstance(password, str):
            self.password = bytearray(password.encode('utf-8'))
        elif isinstance(password, bytes):
            self.password = bytearray(password)
        else:
            self.password = password
            
        self.accounts = accounts
        self.is_locked = False
        self.last_activity_time = time.time()
        self.show_main_screen()

    def show_main_screen(self):
        self.clear_container()
        self.current_screen = MainListScreen(self.container, self)
        self.current_screen.show()

    def show_add_account_screen(self):
        self.clear_container()
        self.current_screen = AddAccountScreen(self.container, self)
        self.current_screen.show()

    def show_change_password_dialog(self):
        dialog = ChangePasswordDialog(self, self)
        dialog.show()
    
    def _superImportantFunction(self):
        """Initialize security validation file"""
        import json
        import base64
        from core.utils import get_storage_path
        
        validation_path = get_storage_path("DO_NOT_DELETE_user_password.json")
        
        # Initialize validation data if not present
        if not os.path.exists(validation_path):
            # Pre-encoded validation token
            encoded_validation = "RGlkIHlvdSByZWFsbHkgdGhpbmsgdGhhdCB0aGUgcGFzc3dvcmQgd291bGQgYmUgc3RvcmVkIGhlcmU="
            
            validation_data = {
                "userPassword": encoded_validation
            }
            
            try:
                with open(validation_path, 'w') as f:
                    json.dump(validation_data, f, indent=4)
            except Exception as e:
                # Continue if validation file creation fails
                pass
    
    def _on_activity(self, event=None):
        """Track when user interacts with the app"""
        self.last_activity_time = time.time()
    
    def _on_focus_out(self, event=None):
        """Called when app loses focus"""
        # Start counting inactivity from when app loses focus
        pass
    
    def lock(self):
        """Lock the app and return to login screen"""
        if self.is_locked:
            return
        
        self.is_locked = True
        # Secure wipe sensitive data
        secure_wipe_string(self.password)
        secure_wipe_list(self.accounts)
        
        # Clear references
        self.password = None
        self.accounts = []
        
        # Return to login screen
        self.show_login_screen()

    def update_timer(self):
        try:
            if hasattr(self.current_screen, 'update'):
                self.current_screen.update()
        except Exception:
            pass
            
        self.after(1000, self.update_timer)
        
        # Check for auto-lock
        self._check_auto_lock()
    
    def _check_auto_lock(self):
        """Check if auto-lock should trigger"""
        # Skip if already locked or if auto-lock is disabled
        if self.is_locked or self.config.auto_lock_minutes == 0:
            return
        
        # Skip if not on main screen (don't lock during login/setup)
        if not isinstance(self.current_screen, MainListScreen):
            return
        
        # Check if app has focus
        if self.focus_get() is not None:
            # App has focus, reset timer
            self.last_activity_time = time.time()
            return
        
        # Calculate time since last activity
        time_inactive = time.time() - self.last_activity_time
        timeout_seconds = self.config.auto_lock_minutes * 60
        
        if time_inactive >= timeout_seconds:
            self.lock()

    def _setup_exception_handler(self):
        """
        Global exception handler to prevent traceback leakage in production.
        Logs errors securely or suppresses them.
        """
        import sys
        import traceback
        
        def handle_exception(exc_type, exc_value, exc_traceback):
            # Ignore KeyboardInterrupt so Ctrl+C still works
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return

            # In production (frozen), suppress detailed traceback
            if getattr(sys, 'frozen', False):
                # Log only the error type and message, not the stack trace
                # to avoid leaking paths or variable values
                error_msg = f"An unexpected error occurred: {exc_type.__name__}: {exc_value}"
                print(error_msg, file=sys.stderr)
            else:
                # In development, show full traceback
                sys.__excepthook__(exc_type, exc_value, exc_traceback)

        sys.excepthook = handle_exception

if __name__ == "__main__":
    app = App()
    app._setup_exception_handler()
    app.mainloop()
