import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import numpy as np
import re

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

download_nltk_data()

def clean_text(text):
    """Removes special characters and lowers the text."""
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    clean_text = re.sub(r'[^a-zA-Z]', ' ', text)
    clean_text = clean_text.lower()
    return clean_text

def remove_stopwords(sentence):
    """Removes stopwords from a sentence."""
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(sentence)
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return " ".join(filtered_words)

def summarize_text(article_text, num_sentences=5):
    """
    Summarizes the given text using TF-IDF and PageRank.
    """
    try:
        # Input validation
        if not article_text or not article_text.strip():
            return "Error: No text provided."
        
        # 1. Tokenize into sentences
        sentences = sent_tokenize(article_text)
        if len(sentences) < 2:
            return "Error: Text must contain at least 2 sentences to summarize."
        
        # Adjust num_sentences if it's larger than available sentences
        num_sentences = min(num_sentences, len(sentences))
        
        # 2. Clean and preprocess sentences
        cleaned_sentences = []
        for s in sentences:
            cleaned = remove_stopwords(clean_text(s))
            if cleaned.strip():  # Only add non-empty cleaned sentences
                cleaned_sentences.append(cleaned)
        
        if len(cleaned_sentences) < 2:
            return "Error: Not enough meaningful content to summarize."
        
        # 3. Create sentence vectors using TF-IDF
        vectorizer = TfidfVectorizer(min_df=1, stop_words='english')
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
