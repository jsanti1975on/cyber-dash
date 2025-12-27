# 2026_Server.py

## Purpose
This project is a lightweight, **intentionally insecure HTTP server** designed for use in a cyber range or home training lab. Security controls are deliberately relaxed to support hands-on learning, source code review, and exploitation exercises. The code has evolved through multiple iterations since 2024.

## Core Feature: File Routing by Prefix
The primary training feature of this server is **moving uploaded files into specific directories based on filename prefix or extension**. This simulates weak business-rule logic commonly found in internal tools and misconfigured services, where user-controlled filenames influence server-side behavior.

### File Routing Rules
- `*.mp3`, `*.wav` → `Music-files/`
- `scripts_*` → `scripts/`
- `cyberoperations_*` → `CyberOperations/`
- `vSphere_*` → `vSphere/`

This behavior is intentional and meant to demonstrate how improper trust in filenames can lead to security issues.

## Additional Behavior
- Accepts `multipart/form-data` file uploads
- Minimal filename sanitization (training-focused, not production-safe)
- Redirects users to `/upload` after submission  
  - `/upload` may resolve to a directory listing or an `index.html`
  - This ambiguity is intentional to encourage inspection and confusion during labs
- Includes a simple success page and an RSS-to-JSON endpoint for additional exercises

## Usage
Run locally from the project directory:
