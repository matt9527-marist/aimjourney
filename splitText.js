/**
 * splitText.js takes in the app context information .txt file and splits it into distinct chunks
 * contained within a JSON file. Each chunk is roughly contained within a 50 word limit.
 * Chunks first divided as singular paragraphs using double line breaks "/\n\s*\n/" as the specified
 * chunk borders. Then these paragraphs are further split into their whole sentences if exceeding 50 words. 
 * 
 * @Developer keep in mind that each "paragraph" in our .txt file is saved in plaintext as one whole line.
 */

const fs = require('fs');

// Construct the relative path to the text file
//! CHANGE FILENAMES WHEN SELECTING DIFFERENT TARGET TEXT FILES OR MOVING DIRECTORIES
const txtPath = 'context/AIM-JOURNEY-CONTEXT.txt'; // Updated for the text file

// Load the text file
let dataBuffer = fs.readFileSync(txtPath, 'utf-8');

/**
 * splitIntoChunks is a first parse through the .txt file, dividing it 
 * by each paragraph, as specified by double line breaks.
 * @param {*} text obtained by the data buffer, which reads our context info file
 * @returns a mapping of chunks
 */
function splitIntoChunks(text) {
    // Split text into chunks using double newlines
    const chunks = text.split(/\n\s*\n/); // Split text by double line breaks (with optional whitespace)
    return chunks.map(chunk => chunk.trim()).filter(chunk => chunk.length > 0); // Trim each chunk and remove empty chunks
}

/**
 * splitChunkByWordLimit is a second parse done on each individual chunk given to us
 * by splitIntoChunks which further divides the chunk into individual sentences if the 
 * word limit for the chunk is exceeded. (Modify word limit according to OpenAI usage costs)
 * @param {*} chunk the chunk obtained from the first parse
 * @param {*} maxWordsPerChunk maximum word count allowed in one chunk 
 * @returns a mapping of chunks
 */
function splitChunkByWordLimit(chunk, maxWordsPerChunk) {
    const sentences = chunk.match(/[^.!?]+[.!?]+/g) || [chunk]; // Match sentences or keep chunk as is
    let result = [];
    let currentChunk = [];
    let currentWordCount = 0;

    sentences.forEach(sentence => {
        const wordsInSentence = sentence.trim().split(/\s+/); // Split sentence into words
        const sentenceWordCount = wordsInSentence.length;

        // If adding this sentence exceeds the max word count for the current chunk, save the current chunk
        if (currentWordCount + sentenceWordCount > maxWordsPerChunk) {
            result.push(currentChunk.join(' ').trim()); // Add the chunk to the result
            currentChunk = []; // Reset the chunk
            currentWordCount = 0; // Reset word count
        }

        // Add the current sentence to the chunk
        currentChunk.push(sentence.trim());
        currentWordCount += sentenceWordCount;
    });

    // Push any remaining sentences as the last chunk
    if (currentChunk.length > 0) {
        result.push(currentChunk.join(' ').trim());
    }

    return result;
}

// Extract text from the .txt file and split into smaller chunks
function processTextFile(dataBuffer) {
    const text = dataBuffer;

    // Split the text into chunks by double line breaks
    const initialChunks = splitIntoChunks(text);

    // Set the target number of words per chunk (e.g., 50 words)
    // *Iteration 1 testing - 100 words
    const maxWordsPerChunk = 500;

    // Further split each chunk by word limit
    const finalChunks = [];
    initialChunks.forEach(chunk => {
        const splitChunks = splitChunkByWordLimit(chunk, maxWordsPerChunk);
        finalChunks.push(...splitChunks); // Flatten the array
    });

    // Store the final chunks in a JSON file or export for further use
    //! CHANGE FILENAMES WHEN SELECTING DIFFERENT TARGET JSONS OR MOVING DIRECTORIES
    const outputPath = 'context/context_chunks.json'; // Updated for the output path
    fs.writeFileSync(outputPath, JSON.stringify(finalChunks, null, 2));
    console.log(`Chunks have been saved to ${outputPath}`);
}

// Process the loaded text file
processTextFile(dataBuffer);
