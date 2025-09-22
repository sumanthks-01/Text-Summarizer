#!/usr/bin/env python3
"""
Setup script to download required NLTK data for multilingual support
"""

import nltk

def setup_nltk():
    """Download all required NLTK data for multilingual text summarization"""
    print("Setting up NLTK data for multilingual support...")
    
    # Download required packages
    packages = ['stopwords', 'punkt', 'punkt_tab', 'wordnet']
    
    for package in packages:
        try:
            print(f"Downloading {package}...")
            nltk.download(package, quiet=True)
            print(f"[OK] {package} downloaded successfully")
        except Exception as e:
            print(f"[ERROR] Failed to download {package}: {e}")
    
    print("\nMultilingual NLTK setup complete!")
    print("Supported languages include:")
    print("   - English, Spanish, French, German, Italian, Portuguese")
    print("   - Russian, Arabic, Hindi, Chinese, Japanese, Korean")
    print("   - Kannada, Telugu, Tamil, Malayalam, Bengali, Gujarati")
    print("   - Dutch, Swedish, Danish, Norwegian, Finnish, Turkish")
    print("   - And many more!")

if __name__ == "__main__":
    setup_nltk()