# 🤖 AI Text Summarizer

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

*Transform long texts into concise summaries using advanced AI algorithms*

</div>

---

## ✨ Features

### 🎯 **Dual Summarization Modes**
- **📝 Normal Mode** - Standard extractive text summarization
- **📚 Topics Mode** - Intelligent topic-based summarization for structured documents

### 📄 **Multi-Format Support**
- **PDF Files** - Extract and summarize PDF documents, notes, and research papers
- **Text Files** - Process .txt files and plain text input
- **Direct Input** - Paste text directly into the application

### 🎨 **Beautiful Modern Interface**
- **Dark Theme** - Easy on the eyes with professional gradient colors
- **Resizable Panes** - Drag dividers to adjust input/output sections
- **Real-time Status** - Color-coded feedback and progress indicators
- **Responsive Design** - Adapts to different screen sizes

### ⚙️ **Advanced Controls**
- **Customizable Length** - Adjust summary from 1-20 sentences
- **Progress Tracking** - Visual progress bar for long documents
- **File Operations** - Load, save, copy, and clear functions
- **Error Handling** - Robust error management and user feedback

---

## 🚀 Quick Start

### 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Text Summerizer"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run setup (first time only)**
   ```bash
   python setup_nltk.py
   ```

### 🎮 Usage

#### **GUI Application**
```bash
python text_summarizer_app.py
```

#### **Command Line Interface**
```bash
# Summarize from file
python cli_app.py -f document.txt -n 5 -o summary.txt

# Summarize from stdin
python cli_app.py -n 3

# Get help
python cli_app.py -h
```

#### **Python Module**
```python
from Summarize_Text import summarize_text

text = "Your long text here..."
summary = summarize_text(text, num_sentences=5)
print(summary)
```

---

## 🎯 How It Works

### **Algorithm Pipeline**
1. **📖 Text Processing** - Sentence tokenization and cleaning
2. **🔍 Feature Extraction** - TF-IDF vectorization
3. **🕸️ Similarity Analysis** - Cosine similarity matrix construction
4. **📊 Ranking** - PageRank algorithm for sentence scoring
5. **✂️ Selection** - Top-N sentence extraction

### **Topic Mode Features**
- **🔍 Auto-Detection** - Finds chapters, sections, and numbered topics
- **📋 Structured Output** - Each topic gets its own summary
- **🔄 Smart Fallback** - Uses paragraph splitting if no clear headings
- **⚖️ Balanced Distribution** - Evenly distributes sentence count across topics

---

## 📱 Interface Guide

### **📝 Input Section**
- **📄 Load PDF** - Upload PDF documents for text extraction
- **📁 Load File** - Import text files (.txt)
- **🗑️ Clear** - Reset input and output areas
- **Text Area** - Direct text input with syntax highlighting

### **⚙️ Settings & Controls**
- **Mode Selector** - Choose between normal/topics summarization
- **Length Control** - Adjust summary length (1-20 sentences)
- **✨ Generate Summary** - Process text with visual progress
- **Progress Bar** - Real-time processing indicator

### **📄 Output Section**
- **Summary Display** - Formatted output with custom fonts
- **📋 Copy Summary** - Copy results to clipboard
- **💾 Save Summary** - Export to text file
- **Status Updates** - Color-coded feedback messages

---

## 📁 Project Structure

```
Text Summerizer/
├── 📄 Summarize_Text.py      # Core summarization engine
├── 🖥️ text_summarizer_app.py # GUI application
├── ⌨️ cli_app.py             # Command-line interface
├── 🔧 setup_nltk.py          # NLTK data setup
├── 📋 requirements.txt       # Python dependencies
└── 📖 README.md              # This file
```

---

## 🛠️ Technical Details

### **Dependencies**
- **NLTK** - Natural language processing
- **scikit-learn** - Machine learning algorithms
- **NetworkX** - Graph algorithms for PageRank
- **PyPDF2** - PDF text extraction
- **Tkinter** - GUI framework (built-in)

### **Supported Formats**
- **Input**: PDF, TXT, Direct text
- **Output**: Plain text, Formatted summaries
- **Encoding**: UTF-8 support

### **Performance**
- **Speed**: Optimized for documents up to 10,000+ words
- **Memory**: Efficient processing with minimal RAM usage
- **Accuracy**: Advanced TF-IDF + PageRank algorithm

---

## 🎨 Customization

### **Color Themes**
The application uses a modern dark theme with customizable colors:
- **Primary**: Deep blue (#1a1a2e)
- **Secondary**: Navy blue (#16213e)
- **Accent**: Blue (#0f3460)
- **Highlight**: Red (#e94560)

### **Font Options**
- **Interface**: Segoe UI (Windows) / System default
- **Input**: Consolas (monospace)
- **Output**: Georgia (serif)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **NLTK Team** - Natural Language Toolkit
- **scikit-learn** - Machine Learning Library
- **NetworkX** - Graph Analysis Library
- **Python Community** - For excellent documentation and support

---

<div align="center">

**Made with ❤️ for better text processing**

[⭐ Star this repo](https://github.com/sumanthks-01/Text-Summarizer) | [🐛 Report Bug](https://github.com/sumanthks-01/Text-Summarizer/issues) | [💡 Request Feature](https://github.com/sumanthks-01/Text-Summarizer/issues)

</div>