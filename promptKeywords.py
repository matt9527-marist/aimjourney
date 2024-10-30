# promptKeywords takes in user input, generates some hidden keywords from it, and then finds
# the most relevant chunk from a JSON file of text chunks given those keywords.

#* This program is called by SERVER after being handed the user's prompt from clientside.
#* Can also serve as a standalone script for debugging the keyword extraction and chunk
#* weighing process. Do not make changes to the server call function in main or find_best_matching_chunk.
#* Add keywords to the keyword lists to influence chunk weighing process. 

import json
import spacy
from collections import Counter
import sys
import os

# Load the SpaCy model
nlp = spacy.load('en_core_web_sm')


# Load the chunks and their keywords
# ! CHANGE FILENAMES WHEN SELECTING DIFFERENT TARGET JSONS OR MOVING DIRECTORIES
with open('context/context_chunks.json', 'r', encoding='utf-8') as f:
    chunks = json.load(f)

# ! CHANGE FILENAMES WHEN SELECTING DIFFERENT TARGET JSONS OR MOVING DIRECTORIES
with open('context/chunk_keywords.json', 'r', encoding='utf-8') as f:
    chunk_keywords = json.load(f)


# List of specific keywords to ensure inclusion. If found in prompt, will significantly influence which chunk is chosen.
#* These keywords are highly specific and chosen deliberately to push prompts containing them to top priority
specific_keywords = ['tension', 'wrist', 'micro', 'pressure', 'flick', 'tense', 'hurts', 'pain', 'Overwatch', 'OW', 'OW2', 'VALORANT', 'val',
                     'cs', 'Counter Strike', 'csgo', 'rainbow six', 'r6', 'cod', 'Call of Duty', 'apex', 'Apex Legends', 'dynamic', 'clicking',
                     'tracking', 'precise', 'reactive', 'switching', 'target switching', 'speed', 'evasive', 'stability', 'stable', 'static click',
                     'static', 'Bardoz', 'fluidity', 'target priority', 'crosshair placement', 'smoothness', 'smoothly', 'wrist aim', 'arm aim',
                     'fingertip aim', 'micro adjustment', 'shot confirmation']

# List of vague keywords to reduce scoring impact
#* These keywords are too vague and sparse across the data context to provide any good influence on the prompt
vague_keywords = ['aim', 'aiming', 'improve', 'improvement', 'practice', 'skill', 'train', 'trainer', 'training']

# List of common keywords to slightly skew scoring impact positively.
#* These keywords will add a slight positive bias to the chunk weight, applied for terms included in frequently asked questions
common_keywords = ['monitor', 'mouse', 'sleeve', 'keyboard', 'shaky', 'shakiness', 'shaking', 'smooth aim', 'calm aim']


def extract_keywords(prompt):
    # Process the user prompt with SpaCy
    doc = nlp(prompt)
    keywords = set()
    
    # Add specific keywords
    for keyword in specific_keywords:
        if keyword in prompt:
            keywords.add(keyword)

    # Add common keywords
    for keyword in common_keywords:
        if keyword in prompt:
            keywords.add(keyword)
    
    # Extract keywords based on entity types
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'ORG', 'GPE', 'EVENT', 'LAW', 'QUANTITY', 'PRODUCT']:
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
    scores = {}

    # Score chunks based on matching keywords
    for chunk_id, keywords in chunk_keywords.items():
        scores[chunk_id] = 0  # Initialize score for each chunk

        # Count specific keyword matches (positive impact)
        specific_matches = user_keywords.intersection(set(keywords).intersection(specific_keywords))
        scores[chunk_id] += len(specific_matches) * 10  # Higher weight for specific keywords

        # Count common keyword matches (slight positive impact)
        common_matches = user_keywords.intersection(set(keywords).intersection(common_keywords))
        scores[chunk_id] += len(common_matches) * 3.5  # Moderate weight for common keywords

        # Count vague keyword matches (negative impact)
        vague_matches = user_keywords.intersection(set(keywords).intersection(vague_keywords))
        scores[chunk_id] -= len(vague_matches) * 5  # Decrease score for vague keywords

        # Count normal keyword matches
        normal_matches = user_keywords.intersection(set(keywords)) - specific_matches - common_matches - vague_matches
        scores[chunk_id] += len(normal_matches)  # Standard weight for normal matches

    # Find the chunk with the highest score
    if scores:
        best_chunk_id = max(scores, key=scores.get)  # Get the ID of the chunk with the highest score
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
    elif os.getenv('RUNNING_FROM_SERVER'):  # Check if running from the server
        print("No prompt provided.")
        sys.exit(1)  # Exit if running from the server without prompt
    else:
        user_prompt = input("Please enter your prompt: ")  # Manual input if not from server
        # Extract and print keywords from the manually entered prompt
        extracted_keywords = extract_keywords(user_prompt)
        print(f"Extracted keywords: {extracted_keywords}")  # Print the extracted keywords

        # Initialize keyword scores based on the scoring logic
        keyword_scores = {keyword: 0 for keyword in extracted_keywords}
        
        # Output the list of found keywords and their scores in descending order
        # That is, the top listed keyword provided the most impact in selecting the given chunk
        for chunk_id, keywords in chunk_keywords.items():
            # Count specific keyword matches (positive impact)
            specific_matches = extracted_keywords.intersection(set(keywords).intersection(specific_keywords))
            for keyword in specific_matches:
                keyword_scores[keyword] += 10  # Higher weight for specific keywords
            
            # Count common keyword matches (slight positive impact)
            common_matches = extracted_keywords.intersection(set(keywords).intersection(common_keywords))
            for keyword in common_matches:
                keyword_scores[keyword] += 3.5  # Moderate weight for common keywords
            
            # Count vague keyword matches (negative impact)
            vague_matches = extracted_keywords.intersection(set(keywords).intersection(vague_keywords))
            for keyword in vague_matches:
                keyword_scores[keyword] -= 5  # Decrease score for vague keywords

            # Count normal keyword matches
            normal_matches = extracted_keywords.intersection(set(keywords)) - specific_matches - common_matches - vague_matches
            for keyword in normal_matches:
                keyword_scores[keyword] += 1  # Standard weight for normal matches

        # Sort the keywords by score in descending order
        sorted_keywords = sorted(keyword_scores.items(), key=lambda item: item[1], reverse=True)

        # Print sorted keywords and their scores
        print("\nKeyword Scores (in descending order):")
        for keyword, score in sorted_keywords:
            print(f"{keyword}: {score}")

    best_chunk = find_best_matching_chunk(user_prompt)
    if best_chunk:
        print(get_chunk_text_by_id(best_chunk))
    else:
        print("No matching chunk found.")
