import sys
import os

print("Checking imports...")
try:
    import constants
    print("constants imported")
    import ui_components
    print("ui_components imported")
    from screens.login import LoginScreen
    print("LoginScreen imported")
    from screens.setup import SetupScreen
    print("SetupScreen imported")
    from screens.main_list import MainListScreen
    print("MainListScreen imported")
    from screens.add_account import AddAccountScreen
    print("AddAccountScreen imported")
    from dialogs.password_dialog import ChangePasswordDialog
    print("ChangePasswordDialog imported")
    import main
    print("main imported")
    print("All imports successful")
except Exception as e:
    print(f"Import Error: {e}")
    import traceback
    traceback.print_exc()
