#!/usr/bin/env python3
"""
Installation script for AI Text Summarizer
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("🚀 Installing AI Text Summarizer...")
    print("=" * 50)
    
    try:
        # Install requirements
        print("📦 Installing Python packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("[OK] Python packages installed successfully!")
        
        # Setup NLTK data
        print("\n📚 Setting up NLTK data...")
        subprocess.check_call([sys.executable, "setup_nltk.py"])
        print("[OK] NLTK data setup completed!")
        
        print("\n" + "=" * 50)
        print("✅ Installation completed successfully!")
        print("\n🎯 To run the application:")
        print("   python text_summarizer_app.py")
        print("\n📖 For CLI usage:")
        print("   python cli_app.py -h")
        
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Installation failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_requirements()