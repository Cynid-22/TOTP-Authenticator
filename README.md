# TOTP Authenticator

**A secure, modern, and highly customizable TOTP authenticator built for power users.**

Most 2FA apps lock you into the standard 6-digit, 30-second SHA1 default. **TOTP Authenticator is different.** This give you full control over your security parameters, making it one of the few authenticators that supports custom digits, periods, and algorithms for every single account.

## Why TOTP Authenticator?

### 🔧 Unmatched Customization
Don't settle for defaults. Configure every aspect of your TOTP codes:
- **Custom Digits**: Support for anywhere from **1 to 9 digits**.
- **Flexible Periods**: Set custom rotation periods from **1 to 120 seconds**.
- **Algorithm Choice**: Full support for **SHA1, SHA256, and SHA512**.

### 🔒 Enterprise-Grade Security
- **AES-256-GCM Encryption**: Your secrets are encrypted with industry-standard authenticated encryption.
- **Argon2id Key Derivation**: Your master password is protected by the winner of the Password Hashing Competition.
- **Zero Knowledge**: We never see your password or keys. Everything stays local on your device.

### ✨ Modern Experience
- **Sleek Dark Mode**: A beautiful, modern interface built with CustomTkinter.
- **Smart Formatting**: Codes are automatically formatted for readability based on their length.
- **Import/Export**: Full control over your data with JSON and CSV support.

## Features at a Glance
- **Circular Progress Timer**: Visual countdown for code expiration.
- **One-Click Copy**: Click any code to copy it instantly.
- **Drag & Drop Reordering**: Organize your accounts exactly how you want them.
- **Secure Export**: Backup your accounts (with a clear warning about unencrypted data).

## Download
**No installation required!** Just download the latest version and run it.

1. Go to the [Releases](../../releases) page.
2. Download `TOTP-Authenticator.exe`.
3. Double-click to run.

## Development

### Prerequisites
- Python 3.7+

### Setup
1. Install dependencies:
   ```bash
   pip install customtkinter pyotp cryptography pyperclip pillow pyinstaller
   ```
2. Run the application:
   ```bash
   python app.py
   ```

## Getting Started

1. **Create a Master Password**: On first run, set a strong password. This encrypts your entire vault.
2. **Add an Account**: Click the **+** button.
3. **Customize**: Click "Advanced Options" to tweak the digits, period, and algorithm to match your specific security requirements.

## Security & Privacy
- **Local Only**: No cloud sync, no external servers.
- **Encrypted Storage**: Your account data is stored in `%LOCALAPPDATA%\TOTP-Authenticator\DO_NOT_DELETE_accounts.json` and is fully encrypted using AES-256-GCM.
- **Memory Protection**: Sensitive data is handled with care in memory.

## Uninstallation

To completely remove TOTP Authenticator from your system:

1. Delete the `TOTP-Authenticator.exe` file.
2. **(Optional)** To permanently delete your encrypted account data, navigate to `%LOCALAPPDATA%\TOTP-Authenticator` and delete the `DO_NOT_DELETE_accounts.json` file.
   - **Note**: This file contains your encrypted 2FA secrets. Only delete it if you no longer need access to these accounts or have backed them up elsewhere.

---
*Built with Python & CustomTkinter*
