const axios = require('axios');

// Uncomment the following line if you are using dotenv for environment variables
// require('dotenv').config();

async function testChatGPT() {
    try {
        const response = await axios.post(
            'https://api.openai.com/v1/chat/completions',
            {
                model: 'gpt-3.5-turbo-instruct-0914', // or 'gpt-4' if you have access
                messages: [{ role: 'user', content: 'Hello, ChatGPT!' }],
            },
            {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer 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`, // Replace with your OpenAI API key
                },
            }
        );
        console.log('Response:', response.data);
    } catch (error) {
        console.error('Error:', error.response ? error.response.data : error.message);
    }
}

testChatGPT();
