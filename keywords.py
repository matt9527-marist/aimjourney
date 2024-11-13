# keywords.py takes in a JSON file containing text chunks and, for each chunk of text,
# generates keywords that will identify or be mapped to that chunk of text.

# This script should only be run once for the lifetime of the project or whenever 
# a new context_chunks.json needs to be generated for a new AIM-JOURNEY-CONTEXT file.
# *Run this script on each context update. 
# *Continuously add keywords to tailor chunk retrieval process for different user prompts.

import json
import spacy

# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")

# Define sets of keywords for categorization
specific_keywords = {'tension', 'wrist', 'micro', 'pressure', 'flick', 'tense', 'hurts', 'pain', 'Overwatch', 'OW', 'OW2', 'VALORANT', 'val',
                     'cs', 'Counter Strike', 'csgo', 'rainbow six', 'r6', 'cod', 'Call of Duty', 'apex', 'Apex Legends', 'dynamic',
                     'precise tracking', 'reactive tracking', 'switching', 'target switching', 'speed', 'evasive', 'stability', 'stable', 'static click',
                     'static', 'Bardoz', 'fluidity', 'target priority', 'crosshair placement', 'smoothness', 'smoothly', 'wrist aim', 'arm aim',
                     'fingertip aim', 'micro adjustment', 'shot confirmation'}

vague_keywords = {'aim', 'aiming', 'improve', 'improvement', 'practice', 'skill', 'train', 'trainer', 'training'}

common_keywords = {'monitor', 'mouse', 'sleeve', 'keyboard', 'shaky', 'shakiness', 'shaking', 'smooth aim', 'calm aim'}

faq_strings = {
    "What is the best sensitivity for aiming?",
    "How do I aim faster in games?"
}

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

    # Identify and add specific, vague, and common keywords
    specific_matches = specific_keywords.intersection(set(doc.text.lower().split()))
    vague_matches = vague_keywords.intersection(set(doc.text.lower().split()))
    common_matches = common_keywords.intersection(set(doc.text.lower().split()))
    faq_matches = faq_strings.intersection(set(doc.text.lower().split()))

    # Add categorized keywords to the chunk keywords list
    keywords.update(specific_matches)
    keywords.update(vague_matches)
    keywords.update(common_matches)
    keywords.update(faq_matches)

    # Map keywords to the chunk
    chunk_keywords[f'chunk_{index + 1}'] = list(keywords)

# Save the keywords mapping to a JSON file
# ! CHANGE FILENAMES WHEN SELECTING DIFFERENT TARGET JSONS OR MOVING DIRECTORIES
with open('context/chunk_keywords.json', 'w', encoding='utf-8') as outfile:
    json.dump(chunk_keywords, outfile, ensure_ascii=False, indent=4)

# Optional: Print the saved mapping for confirmation
print(f"Chunk keywords saved to 'chunk_keywords.json':\n{json.dumps(chunk_keywords, indent=4)}")
