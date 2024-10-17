const fs = require('fs');
const pdf = require('pdf-parse');

// Construct the relative path to the PDF file
//! CHANGE FILENAMES WHEN SELECTING DIFFERENT TARGET JSONS OR MOVING DIRECTORIES
const pdfPath = 'parsers/DeclarationOfIndependence.pdf';

// Load the PDF file
let dataBuffer = fs.readFileSync(pdfPath);

// Function to split text into chunks based on sentence length
function splitIntoChunks(text, maxChunkSize) {
    // Split text into sentences using a regular expression
    const sentences = text.match(/[^.!?]+[.!?]+/g) || []; // Match sentences based on punctuation
    let chunks = [];
    let currentChunk = '';

    sentences.forEach(sentence => {
        // Trim the sentence to avoid leading/trailing whitespace
        sentence = sentence.trim();
        // Check if adding this sentence would exceed the max chunk size
        if ((currentChunk + sentence).length <= maxChunkSize) {
            currentChunk += sentence + ' '; // Add the sentence to the current chunk
        } else {
            // If the current chunk is full, push it to the chunks array
            chunks.push(currentChunk.trim());
            currentChunk = sentence + ' '; // Start a new chunk with the current sentence
        }
    });

    // Push any remaining text as the last chunk
    if (currentChunk.length > 0) {
        chunks.push(currentChunk.trim());
    }

    return chunks;
}

// Extract text from PDF and split into smaller chunks
pdf(dataBuffer).then(function(data) {
    const text = data.text;

    // Set a smaller chunk size (e.g., around 1250 characters)
    const maxChunkSize = 500; // Adjust as needed

    // Split the text into chunks
    const chunks = splitIntoChunks(text, maxChunkSize);

    // Store the chunks in a JSON file or export for further use
    //! CHANGE FILENAMES WHEN SELECTING DIFFERENT TARGET JSONS OR MOVING DIRECTORIES
    const outputPath = 'parsers/context_chunks.json';
    fs.writeFileSync(outputPath, JSON.stringify(chunks, null, 2));
    console.log(`Chunks have been saved to ${outputPath}`);
});
