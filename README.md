# TOTP Authenticator

A simple, secure, and modern TOTP (Time-based One-Time Password) authenticator for Windows, built with Python and CustomTkinter.

## Features
- **Secure Storage**: Accounts are encrypted using `cryptography` (Fernet).
- **Modern UI**: Dark mode interface using `customtkinter`.
- **Standard TOTP**: Compatible with Google Authenticator (SHA1, 30s interval).
- **Clipboard Support**: One-click copy for codes.

## Installation

1.  **Prerequisites**: Ensure Python is installed.
2.  **Install Dependencies**:
    ```bash
    pip install customtkinter pyotp cryptography pyperclip
    ```

## Usage

### Running the App
Run the `main.py` script:
```bash
python main.py
```

### First Run (Setup)
1.  You will be prompted to **Set a Password**.
2.  This password will be used to encrypt your accounts. **Do not forget it!**

### Subsequent Runs (Login)
1.  Enter your password to unlock the application.
2.  If you enter the wrong password, the app will not open.

### Adding an Account
1.  Click the **+** button.
2.  Enter a name (e.g., "Google", "GitHub").
3.  Enter the **Secret Key** provided by the service (e.g., `JBSWY3DPEHPK3PXP`).
    *Note: If the service provides a QR code, look for a "setup key" or "manual entry" option to get the text code.*

## Troubleshooting
- **"Module not found"**: Run the installation command again.
- **"Invalid Secret"**: Ensure you copied the secret key correctly. It should be a Base32 string (letters A-Z and numbers 2-7).
