# Contributing to TOTP Authenticator

First off, thanks for taking the time to contribute! 🎉

The following is a set of guidelines for contributing to TOTP Authenticator. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

-   **Use a clear and descriptive title** for the issue to identify the problem.
-   **Describe the exact steps to reproduce the problem** in as many details as possible.
-   **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
-   **Explain which behavior you expected to see instead and why.**
-   **Include screenshots** if the problem is related to the UI.

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion, including completely new features and minor improvements to existing functionality.

-   **Use a clear and descriptive title** for the issue.
-   **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
-   **Explain why this enhancement would be useful** to most users.

## Pull Request Process

1.  **Fork the repository** and create your branch from `main`.
2.  **Install dependencies** (`pip install -r requirements.txt`) and ensure the application runs (`python app.py`).
3.  **Make your changes**. If you added code, make sure it adheres to the existing style (Python, CustomTkinter).
4.  **Test your changes**. Ensure the app still locks correctly and encrypts data as expected.
5.  **Submit a Pull Request**. Describe your changes and reference any related issues.

## Development Setup

Refer to the [README](README.md#development) for detailed setup instructions.

### Quick Start

```bash
# Install dependencies
pip install customtkinter pyotp cryptography pyperclip pillow pyinstaller

# Run the app
python app.py
```

## Security

If you discover a potential security issue, please do **not** post it as a public issue. Instead, please follow the guidelines in [SECURITY.md](SECURITY.md) (if available) or contact the maintainers directly.

Thank you for contributing!
