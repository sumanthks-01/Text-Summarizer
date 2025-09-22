#!/usr/bin/env python3
"""
Command-line interface for the Text Summarizer
"""

import argparse
import sys
from Summarize_Text import summarize_text, detect_language, LANGUAGE_MAPPINGS

def main():
    parser = argparse.ArgumentParser(description='Text Summarizer CLI')
    parser.add_argument('-f', '--file', help='Input text file path')
    parser.add_argument('-n', '--sentences', type=int, default=5, 
                       help='Number of sentences in summary (default: 5)')
    parser.add_argument('-l', '--language', help='Language code (auto-detect if not specified)')
    parser.add_argument('-o', '--output', help='Output file path (optional)')
    
    args = parser.parse_args()
    
    # Get input text
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
    else:
        print("Enter your text (press Ctrl+Z then Enter on Windows, or Ctrl+D on Unix to finish):")
        text = sys.stdin.read()
    
    if not text.strip():
        print("Error: No text provided.")
        sys.exit(1)
    
    # Detect or use specified language
    language = args.language if args.language else None
    detected_lang = detect_language(text) if language is None else language
    lang_name = LANGUAGE_MAPPINGS.get(detected_lang, detected_lang)
    print(f"Detected/Using language: {lang_name}")
    
    # Generate summary
    print("Generating summary...")
    summary = summarize_text(text, args.sentences, language)
    
    # Output summary
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(summary)
            print(f"Summary saved to '{args.output}'")
        except Exception as e:
            print(f"Error saving file: {e}")
            sys.exit(1)
    else:
        print("\n" + "="*50)
        print("SUMMARY:")
        print("="*50)
        print(summary)

if __name__ == "__main__":
    main()