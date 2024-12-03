const express = require('express');
const axios = require('axios');
const cors = require('cors');
const { exec } = require('child_process');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// Function to determine whether to use python or python3
const detectPythonCommand = async () => {
    return new Promise((resolve, reject) => {
        exec('python --version', (error) => {
            if (!error) {
                resolve('python');
            } else {
                exec('python3 --version', (error) => {
                    if (!error) {
                        resolve('python3');
                    } else {
                        reject(new Error('Neither python nor python3 is available on the system.'));
                    }
                });
            }
        });
    });
};

let PYTHON_CMD = 'python'; // Default to python; will be updated if needed

// Detect Python command at server startup
detectPythonCommand()
    .then((cmd) => {
        PYTHON_CMD = cmd;
        console.log(`Using ${PYTHON_CMD} for Python scripts.`);
    })
    .catch((err) => {
        console.error(err.message);
        process.exit(1); // Exit the server if no Python interpreter is found
    });

app.post('/api/chat', async (req, res) => {
    const { prompt } = req.body;
    let chunkOutput = null;

    try {
        // Step 1: Call promptKeywords.py to retrieve the relevant chunk
        chunkOutput = await new Promise((resolve, reject) => {
            exec(`${PYTHON_CMD} promptKeywords.py "${prompt}"`, (error, stdout, stderr) => {
                if (error) {
                    console.error(`Error executing promptKeywords.py: ${error.message}`);
                    reject('Error executing prompt processing script');
                } else if (stderr) {
                    console.error(`stderr: ${stderr}`);
                    reject('Error executing prompt processing script');
                } else {
                    resolve(stdout.trim());
                }
            });
        });

        // Step 2: Continue to OpenAI API
        const response = await axios.post(
            'https://api.openai.com/v1/chat/completions',
            {
                model: 'gpt-3.5-turbo',
                messages: [
                    {
                        role: 'system',
                        content: 'You are an aim training / esports assistant. Use the given chunk of text and your own knowledge to give a response.',
                    },
                    { role: 'user', content: chunkOutput },
                    { role: 'user', content: prompt },
                ],
                temperature: 0.7,
                max_tokens: 150,
            },
            {
                headers: {
                    Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
                    'Content-Type': 'application/json',
                },
            }
        );

        const botResponse = response.data.choices[0].message.content;

        res.status(200).json({
            response: `Sent chunk: "${chunkOutput}" to OpenAI as context. 
            Returned ChatGPT response: "${botResponse}"`,
        });

    } catch (error) {
        console.error('Error processing request:', error);

        res.status(500).json({
            response: `Internal Server Error - Issue processing the request. Generated Chunk: 
            ${chunkOutput || 'No chunk available due to an error in chunk processing.'}`,
        });
    }
});

// Start the server and listen on the specified port
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
