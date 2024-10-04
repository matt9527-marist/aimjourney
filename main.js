const { app, BrowserWindow, ipcMain } = require('electron');
const axios = require('axios');
require('electron-reload')(__dirname); // Enable live reloading

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      preload: __dirname + '/preload.js', // Preload script
    },
  });

  win.loadFile('index.html');
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// Listen for chat messages
ipcMain.on('send-message', async (event, message) => {
  try {
    const response = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      {
        model: 'gpt-3.5-turbo', // or use 'gpt-4' if you have access
        messages: [{ role: 'user', content: message }],
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer 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`, // Replace with your OpenAI API key
        },
      }
    );

    const chatResponse = response.data.choices[0].message.content;
    event.reply('chat-response', chatResponse);
  } catch (error) {
    console.error('Error:', error);
    event.reply('chat-response', 'Error: ' + error.message);
  }
});
