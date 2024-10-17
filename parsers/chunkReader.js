const fs = require('fs');

// Load the chunks from the JSON file

//! CHANGE THIS WHEN DEALING WITH AIMING DATA
const chunks = JSON.parse(fs.readFileSync('parsers/context_chunks.json', 'utf8'));

// Function to output each chunk independently
function outputChunks() {
    chunks.forEach((chunk, index) => {
        console.log(`Chunk ${index + 1}:\n`);
        console.log(chunk);
        console.log('\n--------------------------------------\n');
    });
}

// Execute the function to output the chunks
outputChunks();
