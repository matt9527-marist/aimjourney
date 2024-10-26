# keywords.py takes in a JSON file containing text chunks and, for each chunk of text,
# generates keywords that will identify or be mapped to that chunk of text.

# This script should only be run once for the lifetime of the project or whenever 
# a new context_chunks.json needs to be generated for a new AIM-JOURNEY-CONTEXT file.
# *Run this script on each context update. 

import json
import spacy

# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")

# Define a set of required keywords
required_keywords = {"tension", "wrist", "micro", "pressure", "flick"}

# Load chunks from the JSON file
# ! CHANGE FILENAMES WHEN SELECTING DIFFERENT TARGET JSONS OR MOVING DIRECTORIES
with open('context/context_chunks.json', 'r', encoding='utf-8') as file:
    chunks = json.load(file)

# Dictionary to hold keywords for each chunk
chunk_keywords = {}

# Process each chunk
for index, chunk in enumerate(chunks):
    # Process the chunk with SpaCy
    doc = nlp(chunk)

    # Create a set to store unique keywords for the current chunk
    keywords = set()

    # Extract named entities
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'ORG', 'GPE', 'EVENT', 'LAW', 'WORK_OF_ART']:
            keywords.add(ent.text)

    # Add keywords based on part-of-speech tagging
    for token in doc:
        if token.is_alpha and not token.is_stop:  # Ignore stop words and non-alpha tokens
            keywords.add(token.text)

    # Add required keywords
    keywords.update(required_keywords.intersection(set(doc.text.lower().split())))

    # Map keywords to the chunk
    chunk_keywords[f'chunk_{index + 1}'] = list(keywords)

# Save the keywords mapping to a JSON file
# ! CHANGE FILENAMES WHEN SELECTING DIFFERENT TARGET JSONS OR MOVING DIRECTORIES
with open('context/chunk_keywords.json', 'w', encoding='utf-8') as outfile:
    json.dump(chunk_keywords, outfile, ensure_ascii=False, indent=4)

# Optional: Print the saved mapping for confirmation
print(f"Chunk keywords saved to 'chunk_keywords.json':\n{json.dumps(chunk_keywords, indent=4)}")
