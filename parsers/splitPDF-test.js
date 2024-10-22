const fs = require('fs');
const pdf = require('pdf-parse');

// Construct the relative path to the PDF file
//! CHANGE FILENAMES WHEN SELECTING DIFFERENT TARGET JSONS OR MOVING DIRECTORIES
const pdfPath = 'parsers/DeclarationOfIndependence.pdf';

// Load the PDF file
let dataBuffer = fs.readFileSync(pdfPath);

// Function to split text into chunks based on sentence boundaries and word count
function splitIntoChunks(text, maxWordsPerChunk) {
    // Split text into sentences using a regular expression (based on punctuation)
    const sentences = text.match(/[^.!?]+[.!?]+/g) || []; // Match sentences based on punctuation
    let chunks = [];
    let currentChunk = [];
    let currentWordCount = 0;

    // Iterate through the sentences and accumulate them into chunks
    sentences.forEach(sentence => {
        const wordsInSentence = sentence.trim().split(/\s+/); // Split sentence into words
        const sentenceWordCount = wordsInSentence.length;

        // If adding this sentence exceeds the max word count for the current chunk, save the current chunk
        if (currentWordCount + sentenceWordCount > maxWordsPerChunk) {
            chunks.push(currentChunk.join(' ').trim()); // Add the chunk to the chunks array
            currentChunk = []; // Reset the chunk
            currentWordCount = 0;
        }

        // Add the current sentence to the chunk
        currentChunk.push(sentence.trim());
        currentWordCount += sentenceWordCount;
    });

    // Push any remaining sentences as the last chunk
    if (currentChunk.length > 0) {
        chunks.push(currentChunk.join(' ').trim());
    }

    return chunks;
}

// Extract text from PDF and split into smaller chunks
pdf(dataBuffer).then(function(data) {
    const text = data.text;

    // Set the target number of words per chunk (e.g., 50 words)
    const maxWordsPerChunk = 50; // Adjust as needed

    // Split the text into chunks by word count without cutting off sentences
    const chunks = splitIntoChunks(text, maxWordsPerChunk);

    // Store the chunks in a JSON file or export for further use
    //! CHANGE FILENAMES WHEN SELECTING DIFFERENT TARGET JSONS OR MOVING DIRECTORIES
    const outputPath = 'parsers/context_chunks.json';
    fs.writeFileSync(outputPath, JSON.stringify(chunks, null, 2));
    console.log(`Chunks have been saved to ${outputPath}`);
});
