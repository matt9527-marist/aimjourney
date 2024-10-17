/***
 * This file sets up an Express server that acts as an intermediary between the client-side (Electron app) and the OpenAI API.
 */

// Import necessary modules
const express = require('express'); // Express is a web framework for Node.js used to create server-side logic

const axios = require('axios'); // Axios is used to make HTTP requests to external APIs (in this case, OpenAI API)

const cors = require('cors'); // CORS (Cross-Origin Resource Sharing) middleware is used to allow requests from different origins (e.g., from the Electron app to the server)

require('dotenv').config(); // dotenv loads environment variables from a .env file

// Define the port the server will run on
// It will use the port defined in the environment variables or default to port 5000
const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors()); // Enable CORS to allow cross-origin requests
app.use(express.json()); // Enable the server to parse incoming JSON payloads

// POST endpoint for handling chat messages sent from the client
app.post('/api/chat', async (req, res) => {

    // Extract the user message (prompt) from the request body
    const { prompt } = req.body;

    try {

        // Send a POST request to the OpenAI API to generate a response
        const response = await axios.post('https://api.openai.com/v1/chat/completions', {
            model: 'gpt-3.5-turbo', // Specify which model to use (e.g., GPT-3.5 Turbo)
            messages: [{ role: 'user', content: prompt }], // Send the user's prompt to the model
            temperature: 0.7, // Set the randomness/creativity of the responses (0 = deterministic, 1 = more creative)
            max_tokens: 150, // Limit the length of the bot's response (150 tokens in this case)
        }, {
            headers: {
                // Use the API key from the environment variables to authorize the request
                'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
                'Content-Type': 'application/json',
            },
        });

        // Extract the content of the response from OpenAI's API
        const botResponse = response.data.choices[0].message.content;
        
        // Send the bot's response back to the client in a JSON format
        res.json({ response: botResponse });

    } catch (error) {

        // Log any error that occurs when communicating with the OpenAI API
        console.error('Error communicating with OpenAI API:', error);

        // Send a generic error response to the client
        res.json({ response: "Internal Server Error - Issue connecting with OpenAI API" });

    }

});

// Start the server and listen on the specified port
app.listen(PORT, () => {

    console.log(`Server is running on http://localhost:${PORT}`);

});
