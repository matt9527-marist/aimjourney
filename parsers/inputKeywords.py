# inputKeywords simply takes an input and generates a set of keywords from that input.

import json
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

# Load the SpaCy English model
nlp = spacy.load('en_core_web_sm')

# List of keywords to always include
important_keywords = [
    "tension", "wrist", "micro", "pressure", "flick"
]

def extract_keywords_from_prompt(prompt):
    # Process the user prompt with SpaCy
    doc = nlp(prompt)
    
    # Set to store unique keywords
    keywords = set()

    # Loop through each token in the processed prompt
    for token in doc:
        # Add token to keywords if it's not a stop word and is not punctuation
        if token.text.lower() not in STOP_WORDS and not token.is_punct:
            keywords.add(token.text)

    # Check for important keywords and add them if present
    for keyword in important_keywords:
        if keyword in prompt.lower():
            keywords.add(keyword)

    return list(keywords)

# Test the function
if __name__ == "__main__":
    user_prompt = input("Enter your prompt: ")
    keywords = extract_keywords_from_prompt(user_prompt)
    print("Extracted Keywords:", keywords)
