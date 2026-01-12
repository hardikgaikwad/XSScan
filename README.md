# XSScan

XSScan is a lightweight, context-aware reflected XSS scanner written in Python.

The tool focuses on detecting server-side reflected Cross-Site Scripting (XSS) vulnerabilities by injecting context-specific payloads into URL parameters and analyzing reflected responses.

XSScan is intended for educational and authorized security testing purposes.

---

## Features

- Reflected XSS detection
- Context-specific payloads (HTML, attribute, JavaScript, SVG)
- Parameter-based URL fuzzing
- Clean and deterministic CLI output
- Tested against OWASP Mutillidae II

---

## Usage

```bash
python main.py --url "http://target-url" --depth 0
