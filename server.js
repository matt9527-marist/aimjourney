/***
 * This file sets up an Express server that acts as an intermediary between the client-side (Electron app) and the OpenAI API.
 */

// Import necessary modules
const express = require('express'); // Express is a web framework for Node.js used to create server-side logic

const axios = require('axios'); // Axios is used to make HTTP requests to external APIs (in this case, OpenAI API)

const cors = require('cors'); // CORS (Cross-Origin Resource Sharing) middleware is used to allow requests from different origins (e.g., from the Electron app to the server)

const { exec } = require('child_process');

require('dotenv').config(); // dotenv loads environment variables from a .env file

// Define the port the server will run on
// It will use the port defined in the environment variables or default to port 5000
const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors()); // Enable CORS to allow cross-origin requests
app.use(express.json()); // Enable the server to parse incoming JSON payloads

// POST endpoint for handling user prompts
app.post('/api/chat', async (req, res) => {
    const { prompt } = req.body;
    let chunkOutput = null;

    try {
        // Step 1: Call promptKeywords.py to retrieve the relevant chunk
        chunkOutput = await new Promise((resolve, reject) => {
            exec(`python3 promptKeywords.py "${prompt}"`, (error, stdout, stderr) => {
                if (error) {
                    console.error(`Error executing promptKeywords.py: ${error.message}`);
                    reject('Error executing prompt processing script');
                } else if (stderr) {
                    console.error(`stderr: ${stderr}`);
                    reject('Error executing prompt processing script');
                } else {
                    resolve(stdout.trim()); // Resolve with the chunk output
                }
            });
        });

        // Step 2: Continue to OpenAI API after retrieving chunk output. Send that chunk along with the user prompt and 
        // simple prompt engineering message to the API. Return the API response to the client
        const response = await axios.post(
            'https://api.openai.com/v1/chat/completions',
            {
                model: 'gpt-3.5-turbo',
                messages: [
                    { role: 'system', content: 
                        'You are an aim training / esports assistant. Use the given chunk of text and your own knowledge to give a response.' }, // Optional system message
                    { role: 'user', content: chunkOutput }, // Send the chunk as the first message
                    { role: 'user', content: prompt } // Then send the user prompt
                ],
                temperature: 0.7,
                max_tokens: 150,
            },
            {
                headers: {
                    'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
                    'Content-Type': 'application/json',
                },
            }
        );

        const botResponse = response.data.choices[0].message.content;

        //* @Developer, for debugging purposes, we include the sent context chunk. This can be removed. 
        
        // Send a single response combining both outputs
        res.status(200).json({
            response: `Sent chunk: "${chunkOutput}" to OpenAI as context. 
            Returned ChatGPT response: "${botResponse}"`
        });

    } catch (error) {
        console.error('Error processing request:', error);

        // Send error response with chunk output if available
        res.status(500).json({
            response: `Internal Server Error - Issue processing the request. Generated Chunk: 
            ${chunkOutput || "No chunk available due to an error in chunk processing."}`
        });
    }
});

// Start the server and listen on the specified port
app.listen(PORT, () => {

    console.log(`Server is running on http://localhost:${PORT}`);

});
