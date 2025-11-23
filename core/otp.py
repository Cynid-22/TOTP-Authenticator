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
        
        # Ensure secret is string for pyotp
        if isinstance(secret, (bytes, bytearray)):
            try:
                secret_str = secret.decode('utf-8')
            except AttributeError:
                secret_str = str(secret)
        else:
            secret_str = secret

        totp = pyotp.TOTP(secret_str, digits=digits, interval=interval, digest=digest_name)
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
            pyotp.TOTP(secret).now()
            return True
        except Exception:
            return False
