# promptKeywords takes in user input, generates some hidden keywords from it, and then finds
# the most relevant chunk from a JSON file of text chunks given those keywords.

import json
import spacy
from collections import Counter
import sys

# Load the SpaCy model
nlp = spacy.load('en_core_web_sm')

# Load the chunks and their keywords
# ! CHANGE FILENAMES WHEN SELECTING DIFFERENT TARGET JSONS OR MOVING DIRECTORIES
with open('context/context_chunks.json', 'r', encoding='utf-8') as f:
    chunks = json.load(f)

# ! CHANGE FILENAMES WHEN SELECTING DIFFERENT TARGET JSONS OR MOVING DIRECTORIES
with open('context/chunk_keywords.json', 'r', encoding='utf-8') as f:
    chunk_keywords = json.load(f)

# List of specific keywords to ensure inclusion
specific_keywords = ['tension', 'wrist', 'micro', 'pressure', 'flick']

def extract_keywords(prompt):
    # Process the user prompt with SpaCy
    doc = nlp(prompt)
    keywords = set()
    
    # Add specific keywords
    for keyword in specific_keywords:
        if keyword in prompt:
            keywords.add(keyword)
    
    # Extract keywords based on entity types
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'ORG', 'GPE', 'EVENT', 'LAW', 'WORK_OF_ART']:
            keywords.add(ent.text)

    # Extract noun phrases
    for chunk in doc.noun_chunks:
        keywords.add(chunk.text)

    # Add other important words (but exclude stop words)
    for token in doc:
        if not token.is_stop and token.is_alpha:
            keywords.add(token.text)

    return keywords

def find_best_matching_chunk(user_prompt):
    user_keywords = extract_keywords(user_prompt)
    keyword_count = Counter()

    # Count occurrences of user keywords in chunk keywords
    for chunk_id, keywords in chunk_keywords.items():
        count = len(user_keywords.intersection(set(keywords)))
        keyword_count[chunk_id] += count

    # Find the chunk with the highest count of matching keywords
    if keyword_count:
        best_chunk_id = keyword_count.most_common(1)[0][0]  # Get the ID of the chunk with highest count
        return best_chunk_id
    return None

def get_chunk_text_by_id(chunk_id):
    chunk_index = int(chunk_id.split('_')[1]) - 1  # Extract the index from chunk_id
    if 0 <= chunk_index < len(chunks):
        return chunks[chunk_index]  # Return the corresponding chunk text
    return "Chunk ID is out of range."

# Main function to accept user prompt from command line
if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_prompt = ' '.join(sys.argv[1:])
        best_chunk = find_best_matching_chunk(user_prompt)
        if best_chunk:
            print(get_chunk_text_by_id(best_chunk))
        else:
            print("No matching chunk found.")
    else:
        print("No prompt provided.")
