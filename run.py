#!/usr/bin/env python3
"""
Quick launcher for AI Text Summarizer
"""

import sys
import os

def main():
    """Launch the text summarizer application"""
    print("🤖 Starting AI Text Summarizer...")
    
    try:
        # Import and run the main application
        from text_summarizer_app import main as app_main
        app_main()
    except ImportError as e:
        print(f"[ERROR] Missing dependencies: {e}")
        print("\n💡 Please run the installation first:")
        print("   python install.py")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()