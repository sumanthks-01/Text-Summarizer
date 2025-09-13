import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from Summarize_Text import summarize_text
import threading
import re
import PyPDF2

class TextSummarizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ AI Text Summarizer")
        self.root.geometry("1000x800")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(True, True)
        self.root.minsize(800, 650)
        
        # Color scheme
        self.colors = {
            'bg_primary': '#1a1a2e',
            'bg_secondary': '#16213e', 
            'accent': '#0f3460',
            'highlight': '#e94560',
            'text_primary': '#ffffff',
            'text_secondary': '#b8b8b8',
            'success': '#27ae60',
            'warning': '#f39c12'
        }
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        """Configure custom styles for ttk widgets"""
        style = ttk.Style()
        
        # Configure button styles
        style.configure('Custom.TButton',
                       font=('Segoe UI', 10, 'bold'))
        
        style.configure('Accent.TButton',
                       font=('Segoe UI', 10))
    
    def create_widgets(self):
        # Header frame
        header_frame = tk.Frame(self.root, bg=self.colors['bg_primary'], height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Title with icon
        title_label = tk.Label(header_frame, 
                              text="🤖 AI Text Summarizer", 
                              font=("Segoe UI", 28, "bold"), 
                              bg=self.colors['bg_primary'], 
                              fg=self.colors['text_primary'])
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(header_frame,
                                 text="Transform long texts into concise summaries using AI",
                                 font=("Segoe UI", 12),
                                 bg=self.colors['bg_primary'],
                                 fg=self.colors['text_secondary'])
        subtitle_label.pack()
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Create PanedWindow for resizable sections
        self.paned_window = tk.PanedWindow(main_container, 
                                          orient=tk.VERTICAL,
                                          bg=self.colors['bg_primary'],
                                          sashwidth=8,
                                          sashrelief='raised',
                                          sashpad=2)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Input section
        input_frame = tk.LabelFrame(self.paned_window, 
                                   text="📝 Input Text", 
                                   bg=self.colors['bg_secondary'],
                                   fg=self.colors['text_primary'],
                                   font=('Segoe UI', 11, 'bold'),
                                   bd=1,
                                   relief='solid')
        self.paned_window.add(input_frame, minsize=200)
        
        # File input buttons (moved to top for visibility)
        file_frame = tk.Frame(input_frame, bg=self.colors['bg_secondary'], height=50)
        file_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        file_frame.pack_propagate(False)
        
        ttk.Button(file_frame, text="📄 Load PDF", 
                  style='Accent.TButton',
                  command=self.load_pdf).pack(side=tk.LEFT, pady=10)
        ttk.Button(file_frame, text="📁 Load File", 
                  style='Accent.TButton',
                  command=self.load_file).pack(side=tk.LEFT, padx=(10, 0), pady=10)
        ttk.Button(file_frame, text="🗑️ Clear", 
                  style='Accent.TButton',
                  command=self.clear_input).pack(side=tk.LEFT, padx=(10, 0), pady=10)
        
        # Text input area
        self.text_input = scrolledtext.ScrolledText(input_frame, 
                                                   wrap=tk.WORD, 
                                                   font=("Consolas", 11),
                                                   bg='#2c2c54',
                                                   fg='#ffffff',
                                                   insertbackground='#e94560',
                                                   selectbackground='#0f3460',
                                                   relief='flat',
                                                   borderwidth=0)
        self.text_input.pack(fill=tk.BOTH, expand=True, pady=(5, 10), padx=10)
        
        # Settings and controls frame as a separate pane
        controls_frame = tk.LabelFrame(self.paned_window, 
                                      text="⚙️ Settings & Controls", 
                                      bg=self.colors['bg_secondary'],
                                      fg=self.colors['text_primary'],
                                      font=('Segoe UI', 11, 'bold'),
                                      bd=1,
                                      relief='solid')
        self.paned_window.add(controls_frame, minsize=100, height=120)
        
        # Settings content
        settings_content = tk.Frame(controls_frame, bg=self.colors['bg_secondary'])
        settings_content.pack(fill=tk.X, padx=15, pady=15)
        
        # Summary mode
        mode_label = tk.Label(settings_content, 
                             text="Mode:",
                             font=("Segoe UI", 11),
                             bg=self.colors['bg_secondary'],
                             fg=self.colors['text_primary'])
        mode_label.pack(side=tk.LEFT)
        
        self.summary_mode = tk.StringVar(value="normal")
        mode_combo = ttk.Combobox(settings_content, 
                                 textvariable=self.summary_mode,
                                 values=["normal", "topics"],
                                 state="readonly",
                                 width=8,
                                 font=("Segoe UI", 10))
        mode_combo.pack(side=tk.LEFT, padx=(10, 15))
        
        # Number of sentences
        length_label = tk.Label(settings_content, 
                               text="Length:",
                               font=("Segoe UI", 11),
                               bg=self.colors['bg_secondary'],
                               fg=self.colors['text_primary'])
        length_label.pack(side=tk.LEFT)
        
        self.num_sentences = tk.IntVar(value=5)
        sentences_spinbox = ttk.Spinbox(settings_content, from_=1, to=20, 
                                       textvariable=self.num_sentences, 
                                       width=5,
                                       font=("Segoe UI", 10))
        sentences_spinbox.pack(side=tk.LEFT, padx=(10, 0))
        
        # Summarize button
        self.summarize_btn = ttk.Button(settings_content, 
                                       text="✨ Generate Summary", 
                                       style='Custom.TButton',
                                       command=self.summarize_threaded)
        self.summarize_btn.pack(side=tk.RIGHT)
        
        # Progress bar
        self.progress = ttk.Progressbar(controls_frame, 
                                       mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(10, 15), padx=15)
        
        # Output section
        output_frame = tk.LabelFrame(self.paned_window, 
                                    text="📄 Generated Summary", 
                                    bg=self.colors['bg_secondary'],
                                    fg=self.colors['text_primary'],
                                    font=('Segoe UI', 11, 'bold'),
                                    bd=1,
                                    relief='solid')
        self.paned_window.add(output_frame, minsize=150)
        
        # Summary output area
        self.summary_output = scrolledtext.ScrolledText(output_frame, 
                                                       wrap=tk.WORD, 
                                                       font=("Georgia", 12),
                                                       bg='#2c2c54',
                                                       fg='#ffffff',
                                                       selectbackground='#0f3460',
                                                       relief='flat',
                                                       borderwidth=0,
                                                       state=tk.DISABLED)
        self.summary_output.pack(fill=tk.BOTH, expand=True, pady=(10, 10), padx=10)
        
        # Output buttons
        output_btn_frame = tk.Frame(output_frame, bg=self.colors['bg_secondary'])
        output_btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(output_btn_frame, text="📋 Copy Summary", 
                  style='Accent.TButton',
                  command=self.copy_summary).pack(side=tk.LEFT)
        ttk.Button(output_btn_frame, text="💾 Save Summary", 
                  style='Accent.TButton',
                  command=self.save_summary).pack(side=tk.LEFT, padx=(15, 0))
        
        # Status label
        self.status_label = tk.Label(output_btn_frame,
                                    text="Ready to summarize",
                                    font=("Segoe UI", 10),
                                    bg=self.colors['bg_secondary'],
                                    fg=self.colors['text_secondary'])
        self.status_label.pack(side=tk.RIGHT)
        
    def load_pdf(self):
        """Load and extract text from PDF file"""
        file_path = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                    
                    self.text_input.delete(1.0, tk.END)
                    self.text_input.insert(1.0, text)
                    self.update_status(f"Loaded PDF: {file_path.split('/')[-1]} ({len(pdf_reader.pages)} pages)", 'success')
            except Exception as e:
                self.update_status(f"Failed to load PDF: {str(e)}", 'error')

    def load_file(self):
        """Load text from a file"""
        file_path = filedialog.askopenfilename(
            title="Select text file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_input.delete(1.0, tk.END)
                    self.text_input.insert(1.0, content)
                    self.update_status(f"Loaded {file_path.split('/')[-1]}", 'success')
            except Exception as e:
                self.update_status(f"Failed to load file: {str(e)}", 'error')
    
    def clear_input(self):
        """Clear the input text area"""
        self.text_input.delete(1.0, tk.END)
        self.summary_output.configure(state=tk.NORMAL)
        self.summary_output.delete(1.0, tk.END)
        self.summary_output.configure(state=tk.DISABLED)
        self.update_status("Ready to summarize", 'info')
        
    def copy_summary(self):
        """Copy summary to clipboard"""
        summary = self.summary_output.get(1.0, tk.END).strip()
        if summary:
            self.root.clipboard_clear()
            self.root.clipboard_append(summary)
            self.update_status("Summary copied to clipboard!", 'success')
        else:
            self.update_status("No summary to copy!", 'warning')
            
    def save_summary(self):
        """Save summary to a file"""
        summary = self.summary_output.get(1.0, tk.END).strip()
        if not summary:
            self.update_status("No summary to save!", 'warning')
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save summary",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(summary)
                self.update_status(f"Summary saved to {file_path.split('/')[-1]}", 'success')
            except Exception as e:
                self.update_status(f"Failed to save: {str(e)}", 'error')
    
    def summarize_threaded(self):
        """Run summarization in a separate thread to prevent GUI freezing"""
        threading.Thread(target=self.summarize_text, daemon=True).start()
        
    def extract_topics(self, text):
        """Extract topics from text based on headings and structure"""
        topics = []
        
        # Split by common heading patterns
        sections = re.split(r'\n\s*(?:[A-Z][^\n]*|\d+\.\s*[A-Z][^\n]*|Chapter\s+\d+|Section\s+\d+)\s*\n', text)
        headings = re.findall(r'\n\s*((?:[A-Z][^\n]*|\d+\.\s*[A-Z][^\n]*|Chapter\s+\d+|Section\s+\d+))\s*\n', text)
        
        # If no clear headings, split by paragraphs
        if len(sections) < 3:
            paragraphs = text.split('\n\n')
            sections = [p for p in paragraphs if len(p.strip()) > 100]
            headings = [f"Topic {i+1}" for i in range(len(sections))]
        
        # Pair headings with content
        for i, section in enumerate(sections[1:], 0):  # Skip first empty section
            if section.strip() and len(section.strip()) > 50:
                heading = headings[i] if i < len(headings) else f"Topic {i+1}"
                topics.append((heading.strip(), section.strip()))
        
        return topics
    
    def summarize_text(self):
        """Summarize the input text"""
        # Get input text
        input_text = self.text_input.get(1.0, tk.END).strip()
        
        if not input_text:
            self.root.after(0, lambda: self.update_status("Please enter some text to summarize!", 'warning'))
            return
        
        # Update UI for processing
        self.root.after(0, lambda: self.summarize_btn.configure(state='disabled'))
        self.root.after(0, lambda: self.progress.start())
        self.root.after(0, lambda: self.update_status("Processing text...", 'info'))
        
        try:
            mode = self.summary_mode.get()
            
            if mode == "topics":
                # Topic-based summarization
                topics = self.extract_topics(input_text)
                if not topics:
                    summary = "No clear topics found. Using normal summarization.\n\n"
                    summary += summarize_text(input_text, self.num_sentences.get())
                else:
                    summary = f"📚 TOPIC-BASED SUMMARY ({len(topics)} topics found)\n"
                    summary += "=" * 60 + "\n\n"
                    
                    for i, (heading, content) in enumerate(topics, 1):
                        topic_summary = summarize_text(content, max(2, self.num_sentences.get() // len(topics)))
                        summary += f"{i}. {heading}\n"
                        summary += "-" * 40 + "\n"
                        summary += f"{topic_summary}\n\n"
            else:
                # Normal summarization
                summary = summarize_text(input_text, self.num_sentences.get())
            
            # Update output
            self.root.after(0, lambda: self.update_summary(summary))
            self.root.after(0, lambda: self.update_status("Summary generated successfully!", 'success'))
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.root.after(0, lambda: self.update_status(error_msg, 'error'))
        
        finally:
            # Re-enable button and stop progress
            self.root.after(0, lambda: self.summarize_btn.configure(state='normal'))
            self.root.after(0, lambda: self.progress.stop())
    
    def update_status(self, message, status_type='info'):
        """Update status label with colored messages"""
        colors = {
            'info': self.colors['text_secondary'],
            'success': self.colors['success'],
            'warning': self.colors['warning'],
            'error': self.colors['highlight']
        }
        self.status_label.configure(text=message, fg=colors.get(status_type, colors['info']))
    
    def update_summary(self, summary):
        """Update the summary output area"""
        self.summary_output.configure(state=tk.NORMAL)
        self.summary_output.delete(1.0, tk.END)
        self.summary_output.insert(1.0, summary)
        self.summary_output.configure(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = TextSummarizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()