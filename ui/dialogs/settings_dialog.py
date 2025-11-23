import customtkinter as ctk
from core.constants import COLOR_TEXT

class SettingsDialog:
    def __init__(self, parent, title, initial_digits, initial_period, initial_algorithm, on_save):
        self.parent = parent
        self.title_text = title
        self.initial_digits = initial_digits
        self.initial_period = initial_period
        self.initial_algorithm = initial_algorithm
        self.on_save = on_save # callback(digits, period, algorithm)

    def show(self):
        # Create dialog
        dialog = ctk.CTkToplevel(self.parent)
        dialog.iconbitmap("assets/icon.ico")
        # Delay setting icon to prevent override
        dialog.after(200, dialog.iconbitmap, "assets/icon.ico")
        dialog.title(self.title_text)
        dialog.geometry("350x320")
        dialog.resizable(False, False)
        dialog.attributes("-topmost", True)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (350 // 2)
        y = (dialog.winfo_screenheight() // 2) - (320 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        frame = ctk.CTkFrame(dialog, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Digits
        ctk.CTkLabel(frame, text="Digits:", text_color=COLOR_TEXT).grid(row=0, column=0, sticky="w", pady=10)
        entry_digits = ctk.CTkEntry(frame, width=80)
        entry_digits.insert(0, str(self.initial_digits))
        entry_digits.grid(row=0, column=1, sticky="w", pady=10)
        ctk.CTkLabel(frame, text="(1-9)", text_color="#888888", font=("Roboto", 10)).grid(row=0, column=2, sticky="w", padx=5, pady=10)
        
        # Period
        ctk.CTkLabel(frame, text="Period:", text_color=COLOR_TEXT).grid(row=1, column=0, sticky="w", pady=10)
        entry_period = ctk.CTkEntry(frame, width=80)
        entry_period.insert(0, str(self.initial_period))
        entry_period.grid(row=1, column=1, sticky="w", pady=10)
        ctk.CTkLabel(frame, text="(1-120)", text_color="#888888", font=("Roboto", 10)).grid(row=1, column=2, sticky="w", padx=5, pady=10)
        
        # Algorithm
        ctk.CTkLabel(frame, text="Algorithm:", text_color=COLOR_TEXT).grid(row=2, column=0, sticky="w", pady=10)
        combo_algorithm = ctk.CTkComboBox(frame, values=["SHA1", "SHA256", "SHA512"], width=120)
        combo_algorithm.set(self.initial_algorithm)
        combo_algorithm.grid(row=2, column=1, columnspan=2, sticky="w", pady=10)
        
        # Error label
        lbl_error = ctk.CTkLabel(frame, text="", text_color="red")
        lbl_error.grid(row=3, column=0, columnspan=3, pady=5)
        
        def save_settings():
            try:
                digits = int(entry_digits.get())
                if not (1 <= digits <= 9):
                    lbl_error.configure(text="Digits must be 1-9")
                    return
            except ValueError:
                lbl_error.configure(text="Digits must be a number")
                return
            
            try:
                period = int(entry_period.get())
                if not (1 <= period <= 120):
                    lbl_error.configure(text="Period must be 1-120")
                    return
            except ValueError:
                lbl_error.configure(text="Period must be a number")
                return
            
            algorithm = combo_algorithm.get()
            
            # Update via callback
            self.on_save(digits, period, algorithm)
            
            dialog.destroy()
        
        # Buttons
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        ctk.CTkButton(btn_frame, text="Save", width=100, command=save_settings).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Cancel", width=100, fg_color="transparent", border_width=1, command=dialog.destroy).pack(side="left", padx=5)
