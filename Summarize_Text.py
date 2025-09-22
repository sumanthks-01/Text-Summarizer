import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import numpy as np
import re
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

# Language mappings for supported languages
LANGUAGE_MAPPINGS = {
    'en': 'english', 'es': 'spanish', 'fr': 'french', 'de': 'german',
    'it': 'italian', 'pt': 'portuguese', 'ru': 'russian', 'ar': 'arabic',
    'hi': 'hindi', 'zh': 'chinese', 'ja': 'japanese', 'ko': 'korean',
    'nl': 'dutch', 'sv': 'swedish', 'da': 'danish', 'no': 'norwegian',
    'fi': 'finnish', 'tr': 'turkish', 'pl': 'polish', 'cs': 'czech',
    'hu': 'hungarian', 'ro': 'romanian', 'bg': 'bulgarian', 'hr': 'croatian',
    'sk': 'slovak', 'sl': 'slovene', 'et': 'estonian', 'lv': 'latvian',
    'lt': 'lithuanian', 'mt': 'maltese', 'ga': 'irish', 'cy': 'welsh',
    'kn': 'kannada', 'te': 'telugu', 'ta': 'tamil', 'ml': 'malayalam',
    'bn': 'bengali', 'gu': 'gujarati', 'pa': 'punjabi', 'or': 'oriya'
}

# Download necessary NLTK data
def download_nltk_data():
    try:
        stopwords.words('english')
    except LookupError:
        print("Downloading stopwords...")
        nltk.download('stopwords')
    
    # Try punkt_tab first (newer versions), then punkt (older versions)
    try:
        sent_tokenize("Test sentence.")
    except LookupError:
        print("Downloading punkt tokenizer...")
        try:
            nltk.download('punkt_tab')
        except:
            nltk.download('punkt')

def detect_language(text):
    """Detect the language of the input text"""
    try:
        lang_code = detect(text)
        return lang_code
    except (LangDetectException, Exception):
        return 'en'  # Default to English

def get_stopwords(lang_code):
    """Get stopwords for the detected language"""
    lang_name = LANGUAGE_MAPPINGS.get(lang_code, 'english')
    try:
        return set(stopwords.words(lang_name))
    except OSError:
        # If language not available, use English as fallback
        return set(stopwords.words('english'))

def multilingual_tokenize(text, lang_code):
    """Tokenize text using NLTK with language-aware processing"""
    # Use NLTK for all languages - it handles most cases well
    return sent_tokenize(text)

download_nltk_data()

def clean_text(text, lang_code='en'):
    """Removes special characters and lowers the text for different languages."""
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    # Language-specific cleaning
    if lang_code in ['ar', 'fa', 'ur']:  # Arabic script
        clean_text = re.sub(r'[^\u0600-\u06FF\s]', ' ', text)
    elif lang_code in ['hi', 'ne', 'mr']:  # Devanagari script
        clean_text = re.sub(r'[^\u0900-\u097F\s]', ' ', text)
    elif lang_code in ['kn']:  # Kannada script
        clean_text = re.sub(r'[^\u0C80-\u0CFF\s]', ' ', text)
    elif lang_code in ['te']:  # Telugu script
        clean_text = re.sub(r'[^\u0C00-\u0C7F\s]', ' ', text)
    elif lang_code in ['ta']:  # Tamil script
        clean_text = re.sub(r'[^\u0B80-\u0BFF\s]', ' ', text)
    elif lang_code in ['ml']:  # Malayalam script
        clean_text = re.sub(r'[^\u0D00-\u0D7F\s]', ' ', text)
    elif lang_code in ['bn']:  # Bengali script
        clean_text = re.sub(r'[^\u0980-\u09FF\s]', ' ', text)
    elif lang_code in ['gu']:  # Gujarati script
        clean_text = re.sub(r'[^\u0A80-\u0AFF\s]', ' ', text)
    elif lang_code in ['pa']:  # Punjabi script
        clean_text = re.sub(r'[^\u0A00-\u0A7F\s]', ' ', text)
    elif lang_code in ['or']:  # Oriya script
        clean_text = re.sub(r'[^\u0B00-\u0B7F\s]', ' ', text)
    elif lang_code in ['zh', 'ja']:  # Chinese/Japanese
        clean_text = re.sub(r'[^\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\s]', ' ', text)
    elif lang_code == 'ko':  # Korean
        clean_text = re.sub(r'[^\uac00-\ud7af\u1100-\u11ff\u3130-\u318f\s]', ' ', text)
    elif lang_code in ['ru', 'bg', 'mk', 'sr']:  # Cyrillic
        clean_text = re.sub(r'[^\u0400-\u04FF\s]', ' ', text)
    elif lang_code in ['el']:  # Greek
        clean_text = re.sub(r'[^\u0370-\u03FF\s]', ' ', text)
    else:  # Latin-based languages
        clean_text = re.sub(r'[^a-zA-ZÀ-ÿ\s]', ' ', text)
    
    clean_text = clean_text.lower()
    return clean_text

def remove_stopwords(sentence, lang_code='en'):
    """Removes stopwords from a sentence in the detected language."""
    stop_words = get_stopwords(lang_code)
    words = word_tokenize(sentence)
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return " ".join(filtered_words)

def summarize_text(article_text, num_sentences=5, language=None):
    """
    Summarizes the given text using TF-IDF and PageRank with multilingual support.
    """
    try:
        # Input validation
        if not article_text or not article_text.strip():
            return "Error: No text provided."
        
        # Detect language if not provided
        if language is None:
            language = detect_language(article_text)
        
        # 1. Tokenize into sentences using appropriate method
        sentences = multilingual_tokenize(article_text, language)
        if len(sentences) < 2:
            return "Error: Text must contain at least 2 sentences to summarize."
        
        # Adjust num_sentences if it's larger than available sentences
        num_sentences = min(num_sentences, len(sentences))
        
        # 2. Clean and preprocess sentences
        cleaned_sentences = []
        for s in sentences:
            cleaned = remove_stopwords(clean_text(s, language), language)
            if cleaned.strip():  # Only add non-empty cleaned sentences
                cleaned_sentences.append(cleaned)
        
        if len(cleaned_sentences) < 2:
            return "Error: Not enough meaningful content to summarize."
        
        # 3. Create sentence vectors using TF-IDF
        # Use language-appropriate stop words
        lang_name = LANGUAGE_MAPPINGS.get(language, 'english')
        try:
            stop_words_list = list(get_stopwords(language))
            vectorizer = TfidfVectorizer(min_df=1, stop_words=stop_words_list)
        except:
            vectorizer = TfidfVectorizer(min_df=1)
        
        try:
            sentence_vectors = vectorizer.fit_transform(cleaned_sentences)
        except ValueError as e:
            return f"Error in vectorization: {str(e)}"
        
        # 4. Build similarity matrix
        sim_mat = cosine_similarity(sentence_vectors)
        np.fill_diagonal(sim_mat, 0)
        
        # Check if similarity matrix has any connections
        if np.sum(sim_mat) == 0:
            # Fallback: return first few sentences
            return " ".join(sentences[:num_sentences])
        
        # 5. Use PageRank to score sentences
        nx_graph = nx.from_numpy_array(sim_mat)
        try:
            scores = nx.pagerank(nx_graph, max_iter=1000, tol=1e-6)
        except (nx.PowerIterationFailedConvergence, nx.NetworkXError):
            # Fallback: use TF-IDF scores
            tfidf_scores = np.mean(sentence_vectors.toarray(), axis=1)
            scores = {i: score for i, score in enumerate(tfidf_scores)}
        
        # 6. Rank sentences and get the top ones
        ranked_sentences = sorted(((scores[i], sentences[i]) for i in range(len(sentences)) if i < len(cleaned_sentences)), reverse=True)
        
        # 7. Get the top 'num_sentences' sentences for the summary
        summary_sentences = [s for score, s in ranked_sentences[:num_sentences]]
        summary = " ".join(summary_sentences)
        
        return summary
        
    except Exception as e:
        return f"Error during summarization: {str(e)}"

def main():
    """
    Main function to get user input and print the summary.
    """
    print("Welcome to the Text Summarizer!")
    print("Please paste the text you want to summarize below.")
    print("--------------------------------------------------")
    
    # Get multi-line input from the user
    lines = []
    while True:
        try:
            line = input()
            if not line:
                break
            lines.append(line)
        except EOFError:
            break
    
    article_text = "\n".join(lines)

    if not article_text.strip():
        print("\nNo text provided. Exiting.")
        return

    summary = summarize_text(article_text)

    print("\n-----------------")
    print("SUMMARY:")
    print("-----------------")
    print(summary)

if __name__ == "__main__":
    main()
