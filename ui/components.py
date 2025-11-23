import customtkinter as ctk
import tkinter as tk
import math
import pyperclip
from PIL import Image, ImageDraw
import os

from core.constants import COLOR_TEXT, COLOR_ACCENT, COLOR_BG_CARD

from core.utils import get_asset_path

def create_trashcan_icon(size=23):
    """Load trashcan icon from assets folder"""
    try:
        icon_path = get_asset_path("trash.ico")
        
        if os.path.exists(icon_path):
            img = Image.open(icon_path)
            return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))
    except Exception:
        pass
    
    # Fallback: return None or create a simple placeholder
    return None

def create_settings_icon(size=23):
    """Load settings icon from assets folder and recolor to light cream"""
    try:
        icon_path = get_asset_path("setting.ico")
        
        if os.path.exists(icon_path):
            img = Image.open(icon_path).convert("RGBA")
            
            # Recolor to light cream (#FFFDD0)
            # Convert RGB values from hex
            cream_color = (255, 253, 208)  # #FFFDD0
            
            # Create a new image with the same size
            data = img.getdata()
            new_data = []
            
            for item in data:
                # If pixel is not transparent
                if item[3] > 0:
                    # Replace with cream color, keep alpha
                    new_data.append((*cream_color, item[3]))
                else:
                    new_data.append(item)
            
            img.putdata(new_data)
            return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))
    except Exception:
        pass
    
    # Fallback: return None or create a simple placeholder
    return None

class CircularProgress(tk.Canvas):
    def __init__(self, master, size=60, color=COLOR_TEXT, **kwargs):
        super().__init__(master, width=size, height=size, bg=master.cget("fg_color"), highlightthickness=0, **kwargs)
        self.size = size
        self.color = color
        self.angle = 360
        self.text_id = self.create_text(size/2, size/2, text="30", fill=color, font=("Roboto", 15, "bold"))
        self.draw()

    def set_progress(self, progress, remaining_seconds):
        # progress is 0.0 to 1.0
        self.angle = 360 * progress
        self.itemconfigure(self.text_id, text=str(int(remaining_seconds)))
        self.draw()

    def draw(self):
        # Clear only arcs, keep text
        self.delete("arc")
        self.delete("bg_circle")
        
        # Draw background circle (faint)
        self.create_oval(2, 2, self.size-2, self.size-2, outline="#444444", width=2, tags="bg_circle")
        # Draw progress arc
        if self.angle > 0:
            self.create_arc(2, 2, self.size-2, self.size-2, start=90, extent=self.angle, outline=self.color, width=3, style="arc", tags="arc")
        
        # Ensure text is on top
        self.tag_raise(self.text_id)

class AccountFrame(ctk.CTkFrame):
    def __init__(self, master, account, auth_engine, callbacks, **kwargs):
        super().__init__(master, fg_color=COLOR_BG_CARD, corner_radius=10, **kwargs)
        
        # Extract account data (support both old dict format and new)
        if isinstance(account, dict):
            self.name = account.get('name', 'Unknown')
            self.secret = account.get('secret', '')
            self.digits = account.get('digits', 6)
            self.interval = account.get('interval', 30)
            self.algorithm = account.get('algorithm', 'SHA1')
        else:
            # Backwards compatibility if someone passes individual args
            self.name = account
            self.secret = auth_engine
            self.digits = 6
            self.interval = 30
            self.algorithm = 'SHA1'
            auth_engine = callbacks
            
        self.auth_engine = auth_engine
        self.callbacks = callbacks # dict of callbacks: delete, move_up, move_down

        # Layout
        self.grid_columnconfigure(1, weight=1)

        # Account Name
        self.label_name = ctk.CTkLabel(self, text=self.name, font=("Roboto", 14), text_color=COLOR_TEXT)
        self.label_name.grid(row=0, column=0, padx=15, pady=(10, 0), sticky="w")

        # TOTP Code
        self.label_code = ctk.CTkLabel(self, text="--- ---", font=("Roboto", 28, "bold"), text_color=COLOR_TEXT)
        self.label_code.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="w")

        # Circular Progress
        self.progress = CircularProgress(self, size=45, color=COLOR_TEXT)
        self.progress.grid(row=0, column=2, rowspan=2, padx=10)

        # --- Normal Mode Widgets ---
        self.btn_copy = ctk.CTkButton(self, text="Copy", width=50, height=25, fg_color=COLOR_ACCENT, text_color=COLOR_TEXT, command=self.copy_code)
        self.btn_copy.grid(row=0, column=3, rowspan=2, padx=10)
        
        # --- Edit Mode Widgets (Hidden by default) ---
        # Up/Down Arrow Buttons
        self.btn_up = ctk.CTkButton(self, text="▲", width=30, height=30, fg_color="transparent", hover_color="#1f6aa5", font=("Roboto", 16), command=lambda: self.callbacks['move_up'](self))
        self.btn_up.grid(row=0, column=3, padx=2)
        self.btn_down = ctk.CTkButton(self, text="▼", width=30, height=30, fg_color="transparent", hover_color="#1f6aa5", font=("Roboto", 16), command=lambda: self.callbacks['move_down'](self))
        self.btn_down.grid(row=0, column=4, padx=5)

        # Trashcan Icon
        self.trash_icon = create_trashcan_icon()
        self.btn_delete = ctk.CTkButton(self, text="", image=self.trash_icon, width=30, height=30, fg_color="transparent", hover_color="#550000", command=self.show_delete_confirmation)

        # Settings Icon
        self.settings_icon = create_settings_icon()
        self.btn_settings = ctk.CTkButton(self, text="", image=self.settings_icon, width=30, height=30, fg_color="transparent", hover_color="#1f6aa5", command=self.show_settings_dialog)

        self.update_code()
        
        # Initially hide edit buttons
        self.btn_up.grid_remove()
        self.btn_down.grid_remove()
        self.btn_delete.grid_remove()
        self.btn_settings.grid_remove()

    def show_delete_confirmation(self):
        if hasattr(self, 'confirm_popup') and self.confirm_popup and self.confirm_popup.winfo_exists():
            self.confirm_popup.lift()
            return

        # Create Popup
        self.confirm_popup = ctk.CTkToplevel(self)
        self.confirm_popup.overrideredirect(True)
        self.confirm_popup.attributes("-topmost", True)
        self.confirm_popup.configure(fg_color="#333333") # Slightly lighter than card
        
        # Position near the delete button
        x = self.btn_delete.winfo_rootx() + 35
        y = self.btn_delete.winfo_rooty()
        self.confirm_popup.geometry(f"+{x}+{y}")
        
        # Content
        lbl = ctk.CTkLabel(self.confirm_popup, text="Delete?", font=("Roboto", 12), text_color=COLOR_TEXT)
        lbl.pack(side="left", padx=(10, 5), pady=5)
        
        btn_yes = ctk.CTkButton(self.confirm_popup, text="Yes", width=40, height=20, fg_color="#ff5555", hover_color="#aa0000", font=("Roboto", 12), command=self.confirm_delete)
        btn_yes.pack(side="left", padx=5, pady=5)
        
        btn_no = ctk.CTkButton(self.confirm_popup, text="No", width=40, height=20, fg_color="transparent", border_width=1, border_color="#666666", text_color=COLOR_TEXT, font=("Roboto", 12), command=self.close_popup)
        btn_no.pack(side="left", padx=(0, 10), pady=5)
        
        # Auto-close on focus loss (optional, but good for UX)
        self.confirm_popup.bind("<FocusOut>", lambda e: self.close_popup())
        self.confirm_popup.focus_force()

    def confirm_delete(self):
        self.callbacks['delete'](self)
        self.close_popup()

    def close_popup(self):
        if hasattr(self, 'confirm_popup') and self.confirm_popup:
            self.confirm_popup.destroy()
            self.confirm_popup = None

    def set_edit_mode(self, is_edit):
        if is_edit:
            self.btn_copy.grid_remove()
            self.label_code.grid_remove()
            self.progress.grid_remove()
            
            # Edit Layout: [Trash] [Settings] [Name (Expanded)] [Up] [Down]
            self.btn_delete.grid(row=0, column=0, padx=5)
            self.btn_settings.grid(row=0, column=1, padx=5)
            
            # Truncate name if too long
            display_name = self.name
            if len(display_name) > 15:
                display_name = display_name[:12] + "..."
            
            self.label_name.configure(text=display_name, font=("Roboto", 20, "bold"), anchor="w")
            self.label_name.grid(row=0, column=2, sticky="ew", pady=10, padx=(5, 0))
            
            self.btn_up.grid(row=0, column=3, padx=2)
            self.btn_down.grid(row=0, column=4, padx=5)
            
            # Adjust column weights for edit mode
            self.grid_columnconfigure(0, weight=0)
            self.grid_columnconfigure(1, weight=0)
            self.grid_columnconfigure(2, weight=1)
            self.grid_columnconfigure(3, weight=0)
            self.grid_columnconfigure(4, weight=0)
            
        else:
            self.btn_delete.grid_remove()
            self.btn_settings.grid_remove()
            self.btn_up.grid_remove()
            self.btn_down.grid_remove()
            
            self.label_name.configure(text=self.name, font=("Roboto", 14), anchor="center")
            # Restore original layout
            self.label_name.grid(row=0, column=0, columnspan=1, sticky="w", pady=(10, 0), padx=15)
            
            self.label_code.grid()
            self.progress.grid()
            self.btn_copy.grid()
            
            # Restore column weights for normal mode
            self.grid_columnconfigure(0, weight=0)
            self.grid_columnconfigure(1, weight=1) # Space between code and progress
            self.grid_columnconfigure(2, weight=0)
            self.grid_columnconfigure(3, weight=0)

    def show_settings_dialog(self):
        from ui.dialogs.settings_dialog import SettingsDialog
        
        def on_save(digits, period, algorithm):
            if 'update_settings' in self.callbacks:
                self.callbacks['update_settings'](self, digits, period, algorithm)

        dialog = SettingsDialog(
            parent=self,
            title=f"Settings - {self.name}",
            initial_digits=self.digits,
            initial_period=self.interval,
            initial_algorithm=self.algorithm,
            on_save=on_save
        )
        dialog.show()

    def update_code(self):
        code = self.auth_engine.generate_totp(
            self.secret, 
            digits=self.digits, 
            interval=self.interval, 
            algorithm=self.algorithm
        )
        
        # Format code based on number of digits
        if len(code) <= 4:
            # 1-4 digits: just show it
            formatted_code = code
        elif len(code) == 5:
            # 5 digits: xxx xx
            formatted_code = f"{code[:3]} {code[3:]}"
        elif len(code) == 6:
            # 6 digits: xxx xxx
            formatted_code = f"{code[:3]} {code[3:]}"
        elif len(code) == 7:
            # 7 digits: xxx xxxx
            formatted_code = f"{code[:3]} {code[3:]}"
        elif len(code) == 8:
            # 8 digits: xxxx xxxx
            formatted_code = f"{code[:4]} {code[4:]}"
        elif len(code) == 9:
            # 9 digits: xxx xxx xxx
            formatted_code = f"{code[:3]} {code[3:6]} {code[6:]}"
        else:
            # Fallback for any other length
            formatted_code = code
            
        self.label_code.configure(text=formatted_code)
        
        # Update progress
        remaining = self.auth_engine.get_remaining_time(interval=self.interval)
        self.progress.set_progress(remaining / self.interval, remaining)

    def copy_code(self):
        code = self.label_code.cget("text").replace(" ", "")
        pyperclip.copy(code)
        
        # Visual feedback
        original_text = self.btn_copy.cget("text")
        self.btn_copy.configure(text="Copied!")
        self.after(1000, lambda: self.btn_copy.configure(text=original_text))
