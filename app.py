import customtkinter as ctk
import os
from core.otp import AuthEngine
from core.storage import Storage
from ui.screens.login import LoginScreen
from ui.screens.setup import SetupScreen
from ui.screens.account_list import MainListScreen
from ui.screens.add_account import AddAccountScreen
from ui.dialogs.password_dialog import ChangePasswordDialog

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

        self.current_screen = None

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
        self.current_screen = LoginScreen(self.container, self.storage, self.on_login_success)
        self.current_screen.show()

    def show_setup_screen(self):
        self.clear_container()
        self.current_screen = SetupScreen(self.container, self.storage, self.on_login_success)
        self.current_screen.show()

    def on_login_success(self, password, accounts):
        self.password = password
        self.accounts = accounts
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

    def update_timer(self):
        try:
            if hasattr(self.current_screen, 'update'):
                self.current_screen.update()
        except Exception as e:
            print(f"Timer Error: {e}")
            
        self.after(1000, self.update_timer)

if __name__ == "__main__":
    app = App()
    app.mainloop()
