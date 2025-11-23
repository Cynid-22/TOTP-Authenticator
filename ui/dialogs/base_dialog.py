import customtkinter as ctk
from core.utils import get_asset_path

class BaseDialog:
    def __init__(self, parent, title, width=350, height=300):
        self.parent = parent
        self.title_text = title
        self.width = width
        self.height = height
        self.dialog = None

    def show(self):
        # Create dialog
        self.dialog = ctk.CTkToplevel(self.parent)
        
        # Set icon with delay to prevent override
        icon_path = get_asset_path("icon.ico")
        self.dialog.after(200, self.dialog.iconbitmap, icon_path)
        
        self.dialog.title(self.title_text)
        self.dialog.geometry(f"{self.width}x{self.height}")
        self.dialog.resizable(False, False)
        self.dialog.attributes("-topmost", True)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.height // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        self.setup_ui()

    def setup_ui(self):
        """Override this method to add widgets to the dialog"""
        pass
    
    def destroy(self):
        if self.dialog:
            self.dialog.destroy()
