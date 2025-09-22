#!/usr/bin/env python3
"""
Installation script for AI Text Summarizer
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing AI Text Summarizer...")
    print("=" * 50)
    
    try:
        # Try minimal requirements first
        print("Installing Python packages (minimal versions)...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements-minimal.txt"])
        except subprocess.CalledProcessError:
            print("Trying individual package installation...")
            packages = ['nltk', 'scikit-learn', 'networkx', 'numpy', 'PyPDF2', 'langdetect']
            for pkg in packages:
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
                    print(f"[OK] {pkg} installed")
                except:
                    print(f"[WARN] {pkg} failed - continuing...")
        
        print("[OK] Python packages installed!")
        
        # Setup NLTK data
        print("\nSetting up NLTK data...")
        subprocess.check_call([sys.executable, "setup_nltk.py"])
        print("[OK] NLTK data setup completed!")
        
        print("\n" + "=" * 50)
        print("Installation completed!")
        print("\nTo run the application:")
        print("   python text_summarizer_app.py")
        
    except Exception as e:
        print(f"[ERROR] Setup error: {e}")
        print("\nTry manual installation:")
        print("   pip install nltk scikit-learn networkx numpy PyPDF2 langdetect")
        print("   python setup_nltk.py")

if __name__ == "__main__":
    install_requirements()