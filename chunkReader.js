const fs = require('fs');
const readline = require('readline');

// Set up readline interface for user input
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Ask the user for the file path
rl.question('Input the file path to the JSON: ', (filePath) => {
    try {
        // Load the chunks from the provided file path
        const chunks = JSON.parse(fs.readFileSync(filePath, 'utf8'));

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

    } catch (error) {
        console.error("Error reading or parsing the file:", error.message);
    }

    // Close the readline interface
    rl.close();
});
