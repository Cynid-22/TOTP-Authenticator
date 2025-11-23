import json
import os
import base64
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class Storage:
    def __init__(self, filepath="accounts.json"):
        self.filepath = filepath
        self.key = None

    def derive_key(self, password, salt=None, iterations=6, memory_cost=65536, lanes=4):
        """
        Derives a 32-byte AES-256 key from the password using Argon2id.
        If salt is None, generates a new 16-byte salt.
        Returns (key, salt)
        """
        if salt is None:
            salt = os.urandom(16)
        
        # Argon2id parameters
        kdf = Argon2id(
            salt=salt,
            length=32,
            iterations=iterations,
            lanes=lanes,
            memory_cost=memory_cost,
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
            # New file, just derive a key to be ready (using new defaults)
            key, _ = self.derive_key(password)
            self.key = key
            return True

        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
            
            salt = base64.b64decode(data['salt'])
            
            # Get KDF params from file, or use legacy defaults
            kdf_params = data.get('kdf_params', {})
            iterations = kdf_params.get('iterations', 2) # Legacy default: 2
            memory_cost = kdf_params.get('memory_cost', 65536)
            lanes = kdf_params.get('lanes', 4)
            
            key, _ = self.derive_key(password, salt, iterations, memory_cost, lanes)
            
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
        Uses upgraded security parameters (iterations=6).
        """
        try:
            # New security defaults
            iterations = 6
            memory_cost = 65536
            lanes = 4
            
            # Generate new salt and key for every save
            key, salt = self.derive_key(password, salt=None, iterations=iterations, memory_cost=memory_cost, lanes=lanes)
            
            aesgcm = AESGCM(key)
            nonce = os.urandom(12) # NIST recommended nonce size for GCM - ALWAYS FRESH
            
            data_json = json.dumps(accounts).encode()
            encrypted_data = aesgcm.encrypt(nonce, data_json, None)
            
            storage_data = {
                "salt": base64.b64encode(salt).decode(),
                "nonce": base64.b64encode(nonce).decode(),
                "data": base64.b64encode(encrypted_data).decode(),
                "kdf_params": {
                    "iterations": iterations,
                    "memory_cost": memory_cost,
                    "lanes": lanes
                }
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

    def export_accounts(self, accounts, format, filepath):
        """
        Exports accounts to a file in the specified format (json or csv).
        WARNING: The exported file is NOT encrypted.
        """
        try:
            if format.lower() == 'json':
                with open(filepath, 'w') as f:
                    json.dump(accounts, f, indent=4)
            elif format.lower() == 'csv':
                import csv
                with open(filepath, 'w', newline='') as f:
                    fieldnames = ['name', 'secret', 'digits', 'interval', 'algorithm']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    for acc in accounts:
                        # Ensure we only write the fields we expect
                        row = {k: acc.get(k) for k in fieldnames}
                        writer.writerow(row)
            else:
                raise ValueError("Unsupported format")
            return True
        except Exception as e:
            print(f"Export error: {e}")
            return False

    def import_accounts(self, filepath):
        """
        Imports accounts from a file (json or csv).
        Automatically detects format.
        Returns a list of account dicts.
        """
        try:
            # Try JSON first
            try:
                with open(filepath, 'r') as f:
                    accounts = json.load(f)
                if isinstance(accounts, list):
                    # Validate basic structure
                    valid_accounts = []
                    for acc in accounts:
                        if 'name' in acc and 'secret' in acc:
                             # Set defaults if missing
                            acc.setdefault('digits', 6)
                            acc.setdefault('interval', 30)
                            acc.setdefault('algorithm', 'SHA1')
                            valid_accounts.append(acc)
                    return valid_accounts
            except json.JSONDecodeError:
                pass # Not JSON, try CSV

            # Try CSV
            import csv
            accounts = []
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if 'name' in row and 'secret' in row:
                        # Convert types
                        try:
                            row['digits'] = int(row.get('digits', 6))
                            row['interval'] = int(row.get('interval', 30))
                        except ValueError:
                            row['digits'] = 6
                            row['interval'] = 30
                        
                        row.setdefault('algorithm', 'SHA1')
                        accounts.append(row)
            return accounts

        except Exception as e:
            print(f"Import error: {e}")
            return []
