#!/usr/bin/env python
"""
Silent dependency installer for SC-AKX200 Control Panel.
Runs pip install in the background without showing console.
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required packages silently."""
    try:
        # Get the directory where this script is located
        app_dir = os.path.dirname(os.path.abspath(__file__))
        requirements_file = os.path.join(app_dir, "requirements.txt")
        
        if os.path.exists(requirements_file):
            # Run pip install silently
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-q", "-r", requirements_file],
                capture_output=True,
                timeout=60
            )
    except Exception:
        # Silently fail - user's Python might already have packages
        pass

if __name__ == "__main__":
    install_dependencies()
