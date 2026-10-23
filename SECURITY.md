# Security Policy

## Supported Versions

Security fixes are released for the latest published minor version only. Older
versions are not backported — please upgrade to the latest release.

| Version | Supported          |
| ------- | ------------------ |
| 0.8.x   | :white_check_mark: |
| < 0.8   | :x:                |

The current release is published on [PyPI](https://pypi.org/project/whatstk/).

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Report them privately through
[GitHub Security Advisories](https://github.com/lucasrodes/whatstk/security/advisories/new).
If that is unavailable to you, [contact the maintainer directly](https://lcsrg.me/pages/contact).

Please include:

- The affected version of whatstk and your Python version.
- A description of the issue and its impact.
- A minimal reproduction — ideally a short chat snippet or script. Redact any
  personal data; a synthetic chat generated with `whatstk-generate-chat` is
  preferred over a real export.

You can expect an initial response within 14 days. If the issue is confirmed, a
patch release will follow and you will be credited in the advisory unless you
prefer otherwise.

## Scope

whatstk parses untrusted input: WhatsApp export files (`.txt`, `.zip`) supplied
by the user, and optionally files fetched over HTTP or from Google Drive. The
following are in scope:

- Arbitrary file write or path traversal when extracting `.zip` exports.
- Code execution or resource exhaustion (e.g. catastrophic regex backtracking)
  triggered by a crafted chat file.
- Unintended network access or credential exposure in the `gdrive` extra.

The following are generally **not** in scope:

- Vulnerabilities in third-party dependencies — report those upstream, though
  we welcome a heads-up so we can pin or bump.
- Crashes or parse failures that only produce an exception or an incorrect
  DataFrame. These are correctness bugs — please open a regular
  [issue](https://github.com/lucasrodes/whatstk/issues).
