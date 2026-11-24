#!/usr/bin/env python3
"""Render an HTML file to PDF with local headless Chrome/Chromium/Edge.

usage: render_pdf.py input.html output.pdf
Cross-platform: macOS, Windows and Linux install locations are all searched.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path


def _candidates():
    paths = [
        # macOS
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    ]
    # Windows: standard install locations (Edge ships with Windows 10/11)
    for root in filter(None, [
        os.environ.get("PROGRAMFILES"),
        os.environ.get("PROGRAMFILES(X86)"),
        os.environ.get("LOCALAPPDATA"),
    ]):
        paths += [
            os.path.join(root, "Google", "Chrome", "Application", "chrome.exe"),
            os.path.join(root, "Chromium", "Application", "chrome.exe"),
            os.path.join(root, "Microsoft", "Edge", "Application", "msedge.exe"),
        ]
    # Anything on PATH (Linux names; Windows too if the user added them)
    paths += [
        shutil.which(n)
        for n in ("google-chrome", "google-chrome-stable", "chromium",
                  "chromium-browser", "chrome", "msedge")
    ]
    return paths


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: render_pdf.py input.html output.pdf")
    html, pdf = (os.path.abspath(a) for a in sys.argv[1:3])
    chrome = next((c for c in _candidates() if c and os.path.exists(c)), None)
    if not chrome:
        sys.exit("No Chrome/Chromium/Edge found. Install one, or open the HTML "
                 "in a browser and print to PDF instead.")
    subprocess.run(
        [
            chrome,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--print-to-pdf=" + pdf,
            Path(html).as_uri(),  # correct file:/// URL on every OS
        ],
        check=True,
        capture_output=True,
    )
    print("wrote " + pdf)


if __name__ == "__main__":
    main()
