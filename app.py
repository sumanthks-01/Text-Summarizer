from flask import Flask, render_template, request, jsonify
from Summarize_Text import summarize_text, detect_language, LANGUAGE_MAPPINGS
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', languages=LANGUAGE_MAPPINGS)

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.json
        text = data.get('text', '').strip()
        num_sentences = int(data.get('sentences', 5))
        language = data.get('language')
        
        if not text:
            return jsonify({'error': 'No text provided'})
        
        if language == 'auto':
            language = None
            
        detected_lang = detect_language(text) if language is None else language
        summary = summarize_text(text, num_sentences, language)
        
        return jsonify({
            'summary': summary,
            'detected_language': detected_lang,
            'language_name': LANGUAGE_MAPPINGS.get(detected_lang, detected_lang)
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)