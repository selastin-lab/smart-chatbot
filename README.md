# Smart Chatbot with Gemini API

## Overview
This project is a smart chatbot built in Python that responds to user messages using predefined intents and can leverage the Gemini API for AI-based responses. The chatbot can handle common questions, greetings, and other intents, and can also generate dynamic responses for more complex queries.

## How I Created This Project
1. **Intents Definition**:
   - Created `intents.json` to define the chatbot’s knowledge base.
   - Each intent has:
     - `tag`: Name of the intent.
     - `patterns`: Possible user inputs.
     - `responses`: Predefined responses to reply with.
2. **Python Script**:
   - Wrote `smart_chatbot.py` to:
     - Load the `intents.json` file.
     - Take user input and match it to an intent.
     - Randomly select a response for matched intents.
     - Call the **Gemini API** for AI-generated responses if no intent matches or advanced interaction is needed.
3. **Gemini API Integration**:
   - Registered and obtained an API key from Gemini API.
   - Integrated API calls in `smart_chatbot.py` to get AI-generated responses.
   - Ensured fallback responses from `intents.json` if API fails.
4. **Testing**:
   - Ran the script locally and tested multiple conversation scenarios.
   - Added more patterns and responses to make the chatbot robust.
5. **Project Structure**:
   - `__pycache__/`: Auto-generated cache folder for Python.
   - `.gitignore`: Lists files and folders to ignore in Git.
   - `intents.json`: Contains chatbot intents, patterns, and responses.
   - `smart_chatbot.py`: Main script integrating intents and Gemini API.

## Features
- Handles predefined intents and responds with appropriate messages.
- Uses Gemini API to provide dynamic AI-powered responses.
- Easily expandable by adding more intents in `intents.json`.
- Simple to run and test locally.

## Setup and Installation
1. Install Python 3.x if not already installed.
2. Clone the repository or download the project files.
3. Install required dependencies (if any):
pip install -r requirements.txt

vbnet
Copy code
4. Set your Gemini API key as an environment variable or inside the script (for testing only).
5. Run the chatbot:
python smart_chatbot.py

csharp
Copy code
6. Interact with the chatbot through the terminal.

## Example Usage
User: Hello
Bot: Hi there! How can I help you?
User: Tell me a joke
Bot: (Uses Gemini API to generate a funny response)
User: What is your name?
Bot: I am a smart chatbot created to assist you.

pgsql
Copy code

## Notes
- Make sure your Gemini API key is valid and has network access.
- Add more intents in `intents.json` to expand chatbot capabilities.
- Python 3.x is recommended for smooth execution.

## License
This project is for educational and experimentation purposes. Commercial use requires permission.
