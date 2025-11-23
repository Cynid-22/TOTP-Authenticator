# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| Older   | :x:                |

## Reporting a Vulnerability

I take security seriously. If you discover a vulnerability, please report it responsibly.

### How to Report

**Option 1: GitHub Security Advisory** (Preferred)
1. Go to the [Security tab](../../security/advisories)
2. Click "Report a vulnerability"
3. Provide detailed information

**Option 2: Public Issue**
- For **non-critical** issues only

### What to Include

- Detailed description and steps to reproduce
- Potential impact (data leak, encryption bypass, etc.)
- Suggested fixes (if you have any)

### Security Notes

This application follows OWASP/NIST best practices but **has not been professionally audited**. See the [Security Disclaimer](README.md#-security-disclaimer) in the README.

**Key security areas:**
- AES-256-GCM encryption with Argon2id
- Secure memory wiping
- Local-only encrypted storage
- Unencrypted exports (by design)

Thank you for helping keep TOTP-Authenticator secure!
