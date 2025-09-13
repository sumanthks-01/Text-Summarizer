#!/usr/bin/env python3
"""
Setup script to download required NLTK data
"""

import nltk

def setup_nltk():
    """Download all required NLTK data"""
    print("Setting up NLTK data...")
    
    # Download required packages
    packages = ['stopwords', 'punkt', 'punkt_tab']
    
    for package in packages:
        try:
            print(f"Downloading {package}...")
            nltk.download(package, quiet=True)
            print(f"[OK] {package} downloaded successfully")
        except Exception as e:
            print(f"[ERROR] Failed to download {package}: {e}")
    
    print("NLTK setup complete!")

if __name__ == "__main__":
    setup_nltk()