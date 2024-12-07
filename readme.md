# **AimJourney**

<span style="color:red">This project is currently in development. Expect certain features to not function as intended.</span>

### A desktop assistant that provides well-informed aiming and competitive gaming advice for Esports video games using AI-powered insights.

---

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Screenshots](#screenshots)
- [Tech Stack](#tech-stack)
- [Contributing](#contributing)

---

## Introduction

*AimJourney* is a desktop application designed for Esports enthusiasts who want to improve their aim. Built using Electron and integrated with ChatGPT, the app provides personalized aiming advice based on user input, game mechanics, and statistical analysis. Whether you're playing FPS games or practicing in aim trainers, *AimJourney* helps enhance your performance by offering AI-powered tips. AimJourney also equally serves as a setup and progress tracking utility for Kovaak's FPS Aim Trainer. Users can download settings directly into the game's directory and pull player statistics from the directory for use in graph visualizations and improvement tracking. 

---

## Features
- **Enhanced ChatGPT Aim Assistant**: Embedded ChatGPT chatbot for quick Q&A related to aim training, esports, and personal improvement in competitive gaming.
- **Kovaak's Setup Utility**: Users can download visual themes, crosshairs, and sounds for use in Kovaak's FPS Aim Trainer
- **Scenario Stats Tracker**: Pulls from local Kovaak's stats directory to create graphs and visualize trends in performance.
- **In-App Achievements**: App rewards for completing specific tasks or hitting score thresholds on specific aim training scenarios. 
- **Modern UI**: Smooth, user-friendly interface with dynamic elements.

---

## Installation
### Steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AimJourney.git
   cd AimJourney
2. In the project directory:
   Run Install.bat via ./install
   (Install NodeJS from https://nodejs.org if it is not already)
   Run Launch.bat to start the Axios server on local host.
   (Or do 
   ```bash
   node server.js, npm run start)
3. Input YOUR OpenAI key replacing “???” in the .env file.
4. In the Client:
   Navigate to “Chat Assistant” and check the “Debug Mode” checkbox
5. Try these 5 prompts:

What does our app say about neuroscience and how much muscle memory plays a role in gaming mechanics?
What should esports players look to do to prevent wrist injuries or tendinopathy?
What are the three fundamental categories of FPS aiming mechanics as defined by aim theory?
What does this app recommend for what to look for in a gaming monitor and why?
Can we expect our progress in aiming or esports to be linear?   

Additionally, you may want to try them with standard ChatGPT to see the differences in responses.
After trying the prompts, run TestAnalysisPrep.py to prepare results.
Go to https://colab.research.google.com/drive/1Uwo7SL2aVQX_RwLrxRga8qQ1UlE5OMu7?usp=sharing 
	And upload ChatData.xlsx to see how the 5 new prompts performed.

### Prerequisites:
- [Node.js](https://nodejs.org/) (v16 or higher)
- [Electron](https://www.electronjs.org/)
- [OpenAI API Key](https://platform.openai.com/) for ChatGPT integration

- [Data/Context](https://docs.google.com/document/d/1Oahyqp7lf0oc4bzQCy81VmLtFhiL14fZq1_BNkB3rvY/edit?usp=sharing) The information aiding ChatGPT

---

## Tech Stack
- **Frontend**: HTML, CSS, JavaScript (React)
- **Backend**: Node.js, Express, Python NLP
- **AI Integration**: OpenAI ChatGPT API
- **Build Tool**: Electron

---

## Contributing
@ William Boulton
