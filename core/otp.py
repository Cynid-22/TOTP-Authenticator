import pyotp
import time

class AuthEngine:
    def __init__(self):
        pass

    def generate_totp(self, secret, digits=6, interval=30, algorithm='SHA1'):
        """
        Generate a TOTP code with custom parameters.
        
        Args:
            secret: Base32 encoded secret key
            digits: Number of digits in the TOTP code (1-9, default 6)
            interval: Time step in seconds (default 30)
            algorithm: Hash algorithm - 'SHA1', 'SHA256', or 'SHA512' (default 'SHA1')
        """
        # Map algorithm names to hashlib names
        algorithm_map = {
            'SHA1': 'sha1',
            'SHA-1': 'sha1',
            'SHA256': 'sha256',
            'SHA-256': 'sha256',
            'SHA512': 'sha512',
            'SHA-512': 'sha512'
        }
        
        digest_name = algorithm_map.get(algorithm.upper().replace('-', ''), 'sha1')
        
        # Ensure secret is string for pyotp (pyotp requires string)
        # We decode only at the last moment to minimize string lifetime
        if isinstance(secret, (bytes, bytearray)):
            try:
                # Create a temporary string just for pyotp
                secret_str = secret.decode('utf-8')
                totp = pyotp.TOTP(secret_str, digits=digits, interval=interval, digest=digest_name)
                code = totp.now()
                
                # Attempt to clear the string from memory (best effort)
                del secret_str
                return code
            except Exception:
                return "000000"
        else:
            totp = pyotp.TOTP(secret, digits=digits, interval=interval, digest=digest_name)
            return totp.now()

    def get_remaining_time(self, interval=30):
        """
        Calculate remaining time until next TOTP code.
        
        Args:
            interval: Time step in seconds (default 30)
        
        Returns:
            Remaining seconds in current interval
        """
        return interval - (int(time.time()) % interval)

    def validate_secret(self, secret):
        """Validate if secret is a valid base32 string"""
        try:
            if isinstance(secret, (bytes, bytearray)):
                secret_str = secret.decode('utf-8')
                pyotp.TOTP(secret_str).now()
                del secret_str
            else:
                pyotp.TOTP(secret).now()
            return True
        except Exception:
            return False
