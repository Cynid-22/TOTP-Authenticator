import json
import os
import base64
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class Storage:
    def __init__(self, filepath="accounts.json"):
        self.filepath = filepath
        self.key = None

    def derive_key(self, password, salt=None):
        """
        Derives a 32-byte AES-256 key from the password using Argon2id.
        If salt is None, generates a new 16-byte salt.
        Returns (key, salt)
        """
        if salt is None:
            salt = os.urandom(16)
        
        # Argon2id parameters (OWASP recommendations or standard secure defaults)
        kdf = Argon2id(
            salt=salt,
            length=32,
            iterations=2,
            lanes=4,
            memory_cost=65536, # 64 MB
            ad=None,
            secret=None
        )
        key = kdf.derive(password.encode())
        return key, salt

    def unlock(self, password):
        """
        Attempts to unlock the storage with the provided password.
        Returns True if successful (or if file doesn't exist yet), False otherwise.
        """
        if not os.path.exists(self.filepath):
            # New file, just derive a key to be ready
            key, _ = self.derive_key(password)
            self.key = key
            return True

        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
            
            salt = base64.b64decode(data['salt'])
            key, _ = self.derive_key(password, salt)
            
            # Verify by attempting to decrypt
            nonce = base64.b64decode(data['nonce'])
            encrypted_data = base64.b64decode(data['data'])
            
            aesgcm = AESGCM(key)
            aesgcm.decrypt(nonce, encrypted_data, None)
            
            self.key = key
            return True
        except Exception as e:
            print(f"Unlock failed: {e}")
            return False

    def save_accounts(self, accounts, password):
        """
        Encrypts and saves the accounts using AES-256-GCM.
        """
        try:
            # Generate new salt and key for every save
            key, salt = self.derive_key(password)
            
            aesgcm = AESGCM(key)
            nonce = os.urandom(12) # NIST recommended nonce size for GCM
            
            data_json = json.dumps(accounts).encode()
            encrypted_data = aesgcm.encrypt(nonce, data_json, None)
            
            storage_data = {
                "salt": base64.b64encode(salt).decode(),
                "nonce": base64.b64encode(nonce).decode(),
                "data": base64.b64encode(encrypted_data).decode()
            }
            
            with open(self.filepath, "w") as f:
                json.dump(storage_data, f)
            
            self.key = key # Update current key
            return True
        except Exception as e:
            print(f"Error saving accounts: {e}")
            return False

    def load_accounts(self):
        """
        Loads accounts using the unlocked key.
        """
        if not self.key:
            raise Exception("Storage not unlocked")
            
        if not os.path.exists(self.filepath):
            return []
        
        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
            
            nonce = base64.b64decode(data['nonce'])
            encrypted_data = base64.b64decode(data['data'])
            
            aesgcm = AESGCM(self.key)
            decrypted_data = aesgcm.decrypt(nonce, encrypted_data, None)
            return json.loads(decrypted_data.decode())
        except Exception as e:
            print(f"Error loading accounts: {e}")
            return []
