# Text Summarizer

A Python-based text summarization tool using TF-IDF and PageRank algorithms.

## Features

- Extractive text summarization using TF-IDF and PageRank
- GUI application with user-friendly interface
- Command-line interface for batch processing
- File input/output support
- Customizable summary length
- Error handling and validation

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. The application will automatically download required NLTK data on first run.

## Usage

### GUI Application
Run the graphical interface:
```bash
python text_summarizer_app.py
```

Features:
- Paste text directly or load from file
- Adjust number of sentences in summary
- Copy or save summary to file
- Progress indicator for long texts

### Command Line Interface
```bash
# Summarize text from file
python cli_app.py -f input.txt -n 3 -o summary.txt

# Summarize text from stdin
python cli_app.py -n 5

# Get help
python cli_app.py -h
```

### Python Module
```python
from Summarize_Text import summarize_text

text = "Your long text here..."
summary = summarize_text(text, num_sentences=5)
print(summary)
```

## Files

- `Summarize_Text.py` - Core summarization logic
- `text_summarizer_app.py` - GUI application
- `cli_app.py` - Command-line interface
- `requirements.txt` - Python dependencies

## Algorithm

The summarizer uses:
1. Sentence tokenization
2. Text cleaning and stopword removal
3. TF-IDF vectorization
4. Cosine similarity matrix
5. PageRank algorithm for sentence scoring
6. Top-N sentence selection

## Error Handling

The application handles:
- Empty or insufficient text
- NLTK data download failures
- PageRank convergence issues
- File I/O errors
- Invalid input parameters