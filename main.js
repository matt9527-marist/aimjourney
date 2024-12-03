/***
 * main.js serves as the main process script that handles the core functionality
 * of the application, primarily controlling the application lifecycle and window management.
 * 
 * Electron apps consist of two main types of processes: the main process (which main.js runs) 
 * and renderer processes (which handle the UI). 
 * Communication between these processes happens through 
 * IPC (Inter-Process Communication).
 */

// Import necessary modules from Electron and other libraries
// app manages the application lifecycle, BrowserWindow creates and manages app windows, 
// ipcMain listens for asynchronous messages
const { app, BrowserWindow, ipcMain } = require('electron'); 

const axios = require('axios'); // Axios is used to make HTTP requests to the OpenAI API

//*require('electron-reload')(__dirname); // Enables live reloading during development when files are changed 
// @Developer do CRTL+S to save, auto reloads app.

/**
 * Function to create the main application window.
 * Sets the size, web preferences, and loads the main HTML file.
 */
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

   // Load the index.html file, which acts as the main UI
  win.loadFile('index.html');
  
}

app.whenReady().then(createWindow);

/**
 * If all windows are closed, quit the app unless the platform is macOS ('darwin').
 * macOS applications usually keep running until explicitly quit by the user.
 */
app.on('window-all-closed', () => {

  if (process.platform !== 'darwin') {
    app.quit();
  }

});

/**
 * On macOS, re-create a window if the app is activated and there are no windows open.
 */
app.on('activate', () => {

  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }

});

/**
 * Listen for chat messages sent from the renderer process (via IPC).
 * Sends the user's message to the OpenAI API and returns the response.
 * !Deprecated, left as fallback API call / reusable code in case server fails.
 */
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
          'Authorization': `Bearer`, // Replace with your OpenAI API key
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
