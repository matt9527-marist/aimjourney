// server.js
const express = require('express');
const axios = require('axios');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// POST endpoint for chat messages
app.post('/api/chat', async (req, res) => {
    const { prompt } = req.body;

    try {
        const response = await axios.post('https://api.openai.com/v1/chat/completions', {
            model: 'gpt-3.5-turbo', // Specify the model
            messages: [{ role: 'user', content: prompt }], // Customize with additional context if needed
            temperature: 0.7, // Adjust the creativity of the responses
            max_tokens: 150, // Limit the length of the response
        }, {
            headers: {
                'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
                'Content-Type': 'application/json',
            },
        });

        const botResponse = response.data.choices[0].message.content;
        
        res.json({ response: botResponse });
    } catch (error) {
        console.error('Error communicating with OpenAI API:', error);
        res.json({ response: "Internal Server Error"});
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
