import json
import os
from core.utils import get_storage_path

class Config:
    """Manages application configuration settings"""
    
    def __init__(self):
        self.config_path = get_storage_path("config.json")
        self.auto_lock_minutes = 5  # Default: 5 minutes
        self.load()
        
        # Create config file with defaults if it doesn't exist
        if not os.path.exists(self.config_path):
            self.save()
    
    def load(self):
        """Load configuration from file"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                    self.auto_lock_minutes = data.get('auto_lock_minutes', 5)
            except Exception:
                # Use defaults if load fails
                pass
    
    def save(self):
        """Save configuration to file"""
        try:
            data = {
                'auto_lock_minutes': self.auto_lock_minutes
            }
            with open(self.config_path, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception:
            pass
