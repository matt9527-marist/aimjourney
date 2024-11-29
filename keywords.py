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
                     'fingertip aim', 'micro adjustment', 'shot confirmation', 'effective split', 'substitute', 'isolation', 
                     'isolated practice', '144hz', '240hz', '360hz', 'ideal sensitivty', 'what sensitivity', 'sens range',
                     'muscle memory', 'changing sens', 'neuroscience', 'motor memory', 'good visuals', 'aim trainer themes',
                     'themes', 'visuals', 'aim theory', 'aim categories', 'static', 'static clicking', 'stationary target', 'static target',
                     'static flick', 'bardoz', 'bardoz method', 'fluidity', 'cluster farming', 'foundation', 'micro correction', 'initial flick', '1w4ts', '1w6ts', 'ww3t',
                     'dynamic', 'dynamic clicking', 'pasu', 'angleshot', 'shot timing', 'multi-target', 'roadmapping', 'peripheral awareness', 'arc dynamic', 
                     'bounceshot', 'b180', 'popcorn', 'tracking', 'smooth tracking', 'precise tracking', 'smoothbot', 'pgti', 'reactive tracking', 'edge tracking', 
                     'air', 'ground plaza', 'fuglaa', 'control tracking', 'whisphere', 'reaction smoothness', 'tension management', 
                     'target switching', 'voxts', 'psalmts', 'direct flicks', 'target prioritization', 'pokeball', 'flick accuracy', 'flick landings', 
                     'flicking technique', 'speed ts', 'evasive ts', 'speed switching', 'evasive switching', 'strafe aim', 'mirroring', 'anti-mirroring',
                     'voltaic overwatch', 'overwatch clicking', 'overwatch dynamic', 'soldier 76', 'cassidy', 'multi-click', 'overwatch click', 'ashe', 'widowmaker', 'strafeshot',
                     'overwatch tracking', 'ow tracking', 'soldier 76 tracking', 'pure reactive', 'instant acceleration', 'overwatch switching', 'ow switching scenarios', 'hitscan', 'tracer',
                     'valorant', 'valorant clicking', 'valorant switching', 'valorant tracking', 'valorant routine', 'valorant warmup',
                     'cs scenarios', 'counter strike', 'cs2', 'csgo', 'apex legends', 'apex', 'aim in apex', 'apex aim', 'apex routines', 'apex scenarios',
                     'wrist health', 'injury', 'health science', 'health', 'symptoms', 'pain', 'weakness', 'tendon', 'tendinopathy', 'prevention', '1hp', '1hp health', 'endurance', 'strengthening',
                     'plateau', 'plateauing'}

vague_keywords = {'aim', 'aiming', 'improve', 'improvement', 'practice', 'skill', 'train', 'trainer', 'training', 'esport', 'game'
                  'shooter', 'FPS', 'improving'}

common_keywords = {'monitor', 'mouse', 'sleeve', 'keyboard', 'shaky', 'shakiness', 'shaking', 'smooth aim', 'calm aim', 'aimbeast',
                   'setup', 'gear', 'grip', 'sens', 'ow', 'crosshair', 'pattern', 'learn', 'experiment', 'mouse accel', 'raw accel',
                   'viscose', 'matty', 'cartoon', 'minigod', 'mouse grip', 'claw', 'palm', 'fingertip', 'talent', 'genetics'}

faq_strings = {
    "What is the best sensitivity for aiming",
    "How do I aim faster in games",
    "What is aim training",
    "How long should you spend aim training",
    "Why play aim trainers",
    "which software is best",
    "which trainer do I use",
    "which trainer do I choose",
    "what sens do I run",
    "What is muscle memory",
    "how to fix shot spamming",
    "how to play tracking",
    "how to reduce shakiness",
    "how to fix shaky aim",
    "how to play reactive tracking",
    "what is tracking",
    "how to play switching",
    "how do i practice fast flicks",
    "how to move and aim",
    "how to dodge and aim",
    "what are good scenarios for clicking in ow",
    "what scenarios are good for soldier",
    "what tracking scenarios are good for overwatch",
    "how to get smooth aim on soldier",
    "what to play for ow",
    "what do I play for overwatch",
    "scenarios for soldier 76",
    "scenarios for cassidy",
    "scenarios for Sojourn",
    "scenarios for widow",
    "scenarios for widowmaker",
    "scenarios for ashe",
    "scenarios for tracer",
    "what routines for valorant",
    "good routines for valorant",
    "how to get better aim in valorant",
    "what routines are for apex",
    "what scenarios for apex",
    "how do I exercise my wrist",
    "why does my wrist hurt",
    "what sensitivity is best",
    "what sensitivity is most optimal",
    "how do you find your sensitivity",
    "what is the best fov",
    "what fov should I be using",
    "is there an optimal fov",
    "where should I be focusing",
    "my crosshair or the bot",
    "look at the crosshair or at the target",
    "should i use my wrist or arm",
    "wrist or arm to aim",
    "arm aimer or wrist aimer",
    "does hardware matter",
    "does setup matter",
    "do good peripherals make a difference",
    "how do i grip my mouse",
    "perfect mouse grip",
    "what is the best grip",
    "how long should i be training",
    "how much training do i need to see the results",
    "why am i not seeing results from aim training",
    "why is my aim still bad",
    "are routines good",
    "should i use routines",
    "should i be on a routine",
    "are routines helpful",
    "how to overcome plateaus",
    "how to stop plateauing",
    "how do you get out of a plateau",
    "do genetics matter",
    "does talent make you a good aimer",
    "is genetics important"
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
