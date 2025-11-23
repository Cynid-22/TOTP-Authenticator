import os
import sys

def get_asset_path(filename):
    """
    Get the absolute path to an asset file.
    Handles both development (running from source) and PyInstaller (running as exe).
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled exe
        base_path = sys._MEIPASS
    else:
        # Running from source
        # core/utils.py -> core/ -> root
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_path, "assets", filename)
