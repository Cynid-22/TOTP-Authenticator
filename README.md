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
- **Auto-Lock**: Configurable timeout with secure memory wiping.

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

### 🔐 Security Architecture

TOTP Authenticator implements security best practices in accordance with **OWASP** (Open Web Application Security Project) and **NIST** (National Institute of Standards and Technology) guidelines:

#### Encryption Standards
- **AES-256-GCM**: Industry-standard Authenticated Encryption with Associated Data (AEAD)
  - Provides both confidentiality and authenticity
  - NIST-approved cipher (FIPS 197)
  - Fresh 12-byte nonce for every encryption operation
  - Fresh 16-byte salt generated on every save

#### Password Security
- **Argon2id Key Derivation**: Winner of the Password Hashing Competition
  - OWASP recommended for password storage
  - Resistant to GPU/ASIC attacks
  - Parameters: 6 iterations, 64MB memory, 4 parallelism lanes
  - No password ever stored in plaintext

#### Data Protection
- **Local-Only Storage**: No cloud sync, no external servers, fully offline
- **Encrypted at Rest**: All account data encrypted in `%LOCALAPPDATA%\TOTP-Authenticator`
- **Secure Memory Management**: Sensitive data wiped from memory on app lock
- **Auto-Lock**: Configurable timeout (default: 5 minutes) with automatic memory cleanup
- **Zero Logging**: No debug logs or error messages that could leak sensitive data

#### Export Security
- **Unencrypted Exports**: CSV/JSON exports are NOT encrypted
  - 5-second warning countdown before export
  - Clear security warnings displayed to users
  - Users must secure exported files themselves

### ⚠️ Security Disclaimer

> **IMPORTANT**: While TOTP Authenticator follows industry best practices and implements security measures in accordance with OWASP and NIST guidelines, this software:
> 
> - **Has not been audited** by third-party security professionals
> - **Has no official certifications** (e.g., Common Criteria, FIPS 140-2)
> - Is provided **as-is** without warranty of any kind
> 
> Use this application at your own risk. For mission-critical or high-security environments, consider professionally audited alternatives with official certifications.

### Privacy Guarantees
- **Zero Knowledge**: Your master password and TOTP secrets never leave your device
- **No Telemetry**: No analytics, tracking, or data collection of any kind
- **No Network Calls**: Application is 100% offline

## Uninstallation

To completely remove TOTP Authenticator from your system:

1. Delete the `TOTP-Authenticator.exe` file.
2. **(Optional)** To permanently delete your encrypted account data, navigate to `%LOCALAPPDATA%\TOTP-Authenticator` and delete the `DO_NOT_DELETE_accounts.json` file.
   - **Note**: This file contains your encrypted 2FA secrets. Only delete it if you no longer need access to these accounts or have backed them up elsewhere.

---
*Built with Python & CustomTkinter*
