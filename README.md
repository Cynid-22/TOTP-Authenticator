# TOTP Authenticator

A secure, modern TOTP (Time-based One-Time Password) authenticator built with Python and CustomTkinter.

## Features

### Security
- **AES-256-GCM Encryption**: All accounts are encrypted using industry-standard AES-256-GCM
- **Argon2id Key Derivation**: Password-based encryption key derivation with OWASP-recommended parameters
- **Master Password**: Single password protects all your accounts
- **Password Change**: Change your master password without losing accounts

### TOTP Configuration
- **Custom Digits**: Support for 1 to 9 digit TOTP codes
- **Custom Period**: Configurable time periods (default 30s, range 1-120s)
- **Multiple Algorithms**: SHA1, SHA256, and SHA512 support
- **Per-Account Settings**: Configure TOTP parameters individually for each account

### User Interface
- **Modern Dark Theme**: Clean, modern interface with smooth animations
- **Circular Progress Timer**: Visual countdown for code expiration
- **Smart Code Formatting**: Auto-formatted code display based on digit count
- **Arrow Button Reordering**: Use ▲▼ buttons to reorder accounts
- **Edit Mode**: Toggle edit mode to delete or reorder accounts
- **One-Click Copy**: Click any code to copy to clipboard
- **Custom Icons**: Application icon and asset support

## Installation

### Prerequisites
- Python 3.7 or higher

### Install Dependencies
```bash
pip install customtkinter pyotp cryptography pyperclip pillow
```

## Usage

### Running the App
```bash
python main.py
```

### First Run
1. You'll be prompted to create a master password
2. This password encrypts all your accounts - **don't forget it!**

### Login
Enter your master password to unlock the app

### Adding Accounts
1. Click the **+** button
2. Enter the account name (e.g., "Google", "GitHub")
3. Enter the secret key from the service
4. **(Optional)** Click "Advanced Options" to configure:
   - Number of digits (1 to 9)
   - Time period (in seconds, 1 to 120)
   - Hash algorithm (SHA1, SHA256, SHA512)

### Managing Accounts
- **Copy Code**: Click on any TOTP code to copy it
- **Edit Account Settings**: Click the ⚙️ icon on any account
- **Delete Account**: Enable edit mode (≡ menu → Edit) and click the 🗑️ icon
- **Reorder Accounts**: Enable edit mode and use ▲▼ arrow buttons to move accounts up or down
- **Change Password**: Click ≡ menu → Change Password

## Security Notes
- Account data is encrypted using AES-256-GCM with Argon2id key derivation
- The master password is never stored - only used to derive encryption keys
- Each save operation generates a new salt and nonce for security
- If you forget your master password, your accounts cannot be recovered
