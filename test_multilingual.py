#!/usr/bin/env python3
"""
Test script to demonstrate multilingual text summarization capabilities
"""

from Summarize_Text import summarize_text, detect_language

# Test texts in different languages
test_texts = {
    "English": """
    Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals. Colloquially, the term "artificial intelligence" is often used to describe machines that mimic "cognitive" functions that humans associate with the human mind, such as "learning" and "problem solving". As machines become increasingly capable, tasks considered to require "intelligence" are often removed from the definition of AI, a phenomenon known as the AI effect.
    """,
    
    "Spanish": """
    La inteligencia artificial es la inteligencia llevada a cabo por máquinas. En ciencias de la computación, una máquina inteligente ideal es un agente flexible que percibe su entorno y lleva a cabo acciones que maximicen sus posibilidades de éxito en algún objetivo o tarea. El término inteligencia artificial se aplica cuando una máquina imita las funciones cognitivas que los humanos asocian con otras mentes humanas, como por ejemplo: aprender y resolver problemas. A medida que las máquinas se vuelven cada vez más capaces, las tareas que requieren inteligencia se eliminan de la definición de inteligencia artificial.
    """,
    
    "French": """
    L'intelligence artificielle est une technologie qui permet aux machines d'imiter l'intelligence humaine. Elle englobe l'apprentissage automatique, le traitement du langage naturel et la vision par ordinateur. Les systèmes d'IA peuvent analyser des données, reconnaître des modèles et prendre des décisions. Cette technologie révolutionne de nombreux secteurs, notamment la santé, les transports et la finance. L'IA continue d'évoluer rapidement, offrant de nouvelles possibilités mais soulevant aussi des questions éthiques importantes.
    """,
    
    "German": """
    Künstliche Intelligenz ist ein Teilgebiet der Informatik, das sich mit der Automatisierung intelligenten Verhaltens und dem maschinellen Lernen befasst. Der Begriff ist schwer definierbar, da es bereits an einer genauen Definition von Intelligenz mangelt. Dennoch wird er in Forschung und Entwicklung verwendet. Im Verständnis des Begriffs künstliche Intelligenz spiegelt sich oft die aus der Aufklärung stammende Vorstellung vom Menschen als Maschine wider, dessen Nachahmung sich die sogenannte starke KI zum Ziel setzt.
    """
}

def test_multilingual_summarization():
    """Test summarization in multiple languages"""
    print("Multilingual Text Summarization Test")
    print("=" * 50)
    
    for language, text in test_texts.items():
        print(f"\nTesting {language}:")
        print("-" * 30)
        
        # Detect language
        detected = detect_language(text.strip())
        print(f"Detected language code: {detected}")
        
        # Generate summary
        summary = summarize_text(text.strip(), num_sentences=2)
        print(f"Summary: {summary}")
        print()

if __name__ == "__main__":
    test_multilingual_summarization()