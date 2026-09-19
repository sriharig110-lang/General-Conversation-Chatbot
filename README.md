# 🤖 General Conversation Chatbot

A general-purpose AI chatbot built with **Python, Streamlit, and Google's Gemini API**.

This project demonstrates how to build a conversational AI application with Gemini, multi-turn context, Streamlit session state, and SQLite-based chat storage.

---

## 🚀 Features

- 💬 General-purpose AI conversations
- 🤖 Powered by Google Gemini
- 🔄 Multi-turn conversation context
- 🖥️ Interactive Streamlit chat interface
- 🧠 Session-based conversation memory
- 💾 SQLite-based chat storage
- 🔐 API key protection using environment variables
- 🛠️ Gemini API integration and debugging
- 📦 Reproducible Python dependencies

---

## 🏗️ Architecture

```text
                    User
                     │
                     ▼
              ┌──────────────┐
              │  Streamlit   │
              │     UI       │
              └──────┬───────┘
                     │
                     ▼
             Conversation State
                     │
                     ▼
              ┌──────────────┐
              │ Gemini API   │
              └──────┬───────┘
                     │
                     ▼
                AI Response
                     │
                     ▼
              ┌──────────────┐
              │    SQLite    │
              │   Database   │
              └──────────────┘
```

## 🛠️ Tech Stack
```Python
Google Gemini API
google-genai
Streamlit
SQLite
python-dotenv
```
## 📁 Project Structure
```General-Conversation-Chatbot/
│
├── app.py
├── README.md
├── requirements.txt
└── .gitignore
Local files
The following files are intentionally excluded from GitHub:
api.env
chat_history.db
.venv/
The API key and local database should remain on the developer's machine.
```
## ⚙️ How It Works
The user enters a message through the Streamlit chat interface.
The application receives the user input.
Conversation context is maintained using Streamlit session state.
The conversation history is converted into the format expected by Gemini.
Gemini generates a response.
The response is displayed in the Streamlit interface.
Conversation messages can be stored in SQLite for persistent storage.
## 🧠 Conversation Context
The chatbot supports follow-up questions by maintaining previous messages.
Example:
```User:
What is Python?

Gemini:
Python is a general-purpose programming language...

User:
What are its advantages?

Gemini:
Python's advantages include simplicity, readability,
a large ecosystem, and extensive use in areas such
as data science and AI.
```
The previous conversation context allows Gemini to understand references such as "its" and "it".

## 💾 SQLite Storage
```The project uses SQLite to store conversation messages locally.
The database contains message information such as:
message ID
conversation ID
role
content
timestamp
This provides a foundation for persistent conversation history.
```
## 🔐 Environment Setup
Create an api.env file in the project root:
GEMINI_API_KEY=your_api_key_here
The API key is excluded from GitHub through .gitignore.
## 📦 Installation
```
Clone the repository:
git clone https://github.com/sriharig110-lang/General-Conversation-Chatbot.git
Move into the project directory:
cd General-Conversation-Chatbot
Create a virtual environment:
python -m venv .venv
Activate the environment on Windows:
.venv\Scripts\activate
Install the dependencies:
pip install -r requirements.txt
```
## ▶️ Run the Application
Start the Streamlit application:
streamlit run app.py
The chatbot will open in your browser.
## 📸 Application
The application provides a simple conversational interface where users can interact with Gemini and continue conversations using contextual follow-up questions.
## 🧠 Key Learning Outcomes
```This project helped me understand and implement:
LLM API integration
Gemini SDK usage
Multi-turn conversations
Conversation context management
Streamlit chat components
Streamlit session state
SQLite database integration
Environment variable management
API error debugging
Basic LLM application architecture
Python dependency management
```
## 🔮 Future Improvements
```
🗂️ Chat history sidebar
➕ Multiple conversation management
🔄 Switching between saved conversations
✏️ Conversation renaming
🗑️ Conversation deletion
⚡ Streaming Gemini responses
🛡️ Improved error handling
📤 Chat export
🌐 Deployment
🔐 User authentication
🔧 Gemini function calling and AI tools
```
## 👨‍💻 Author
Sri Hari
Aspiring AI/ML Engineer
Skills: Python | Machine Learning | Generative AI | LLM Applications | SQL | Data Science