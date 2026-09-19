import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sqlite3
import uuid
import streamlit as st
conn = sqlite3.connect('chat_history.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS conversation (
    id TEXT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()
cursor.execute("PRAGMA table_info(conversation)")
conversation_columns = [column[1] for column in cursor.fetchall()]
if "title" not in conversation_columns:
    cursor.execute("ALTER TABLE conversation ADD COLUMN title TEXT DEFAULT 'New Chat'")
    conn.commit()
cursor.execute('''
CREATE TABLE IF NOT EXISTS message (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id TEXT,
    role TEXT,
    content TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
def update_conversation_title(conversation_id, title):
    cursor.execute('''UPDATE conversation SET title = ? WHERE id = ?''', (title, conversation_id))
    conn.commit()
  
def load_chat_history(conversation_id):
    cursor.execute("SELECT role, content FROM message WHERE conversation_id = ?", (conversation_id,))
    rows = cursor.fetchall()
    return [{"role": role, "content": content} for role, content in rows]
def load_conversations():
    cursor.execute('''SELECT id,title FROM conversation ORDER BY created_at DESC''')
    return cursor.fetchall()
def delete_conversation(conversation_id):
    cursor.execute("DELETE FROM message WHERE conversation_id = ?", (conversation_id,))
    cursor.execute("DELETE FROM conversation WHERE id = ?", (conversation_id,))
    conn.commit()
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / "api.env")
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not configured.")
client = genai.Client(api_key=api_key)
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())
    cursor.execute("INSERT OR IGNORE INTO conversation (id,title) VALUES (?,?)", (st.session_state.conversation_id,"New Chat"))
    conn.commit()

st.title("🤖 General Conversation Chatbot")
with st.sidebar:
    st.header("💬 Chat History")

    if st.button("➕ New Chat"):
        new_id = str(uuid.uuid4())
        cursor.execute("INSERT INTO conversation (id,title) VALUES (?,?)", (new_id,"New Chat"))
        conn.commit()
        st.session_state.conversation_id = new_id
        st.session_state.messages = []
        st.rerun()
    conversations = load_conversations()
    for conv_id, title in conversations:
        col1,col2 = st.columns([4,1])
        with col1:  
            if st.button(title, key=f"chat_{conv_id}"):
                st.session_state.conversation_id = conv_id
                st.session_state.messages = load_chat_history(conv_id)
                st.rerun()  
        with col2:
            if st.button("",icon=":material/delete:", key=f"delete_{conv_id}",help="Delete this conversation"):
                delete_conversation(conv_id)
                if st.session_state.conversation_id == conv_id:
                    st.session_state.conversation_id = str(uuid.uuid4())
                    cursor.execute("INSERT OR IGNORE INTO conversation (id,title) VALUES (?,?)", (st.session_state.conversation_id,"New Chat"))
                    conn.commit()
                    st.session_state.messages = []
                st.rerun()
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history(st.session_state.conversation_id)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
for message in st.session_state.messages:
    with st.chat_message(message["role"]):st.write(message["content"])
user_input = st.chat_input("Type your message...")
 
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    cursor.execute("INSERT INTO message (conversation_id, role, content) VALUES (?, ?, ?)",
            (st.session_state.conversation_id, "user", user_input))
    conn.commit()
    cursor.execute("""SELECT COUNT(*) FROM message WHERE conversation_id = ? AND role = 'user'""", (st.session_state.conversation_id, ))
    user_message_count = cursor.fetchone()[0]
    if user_message_count == 1:
        update_conversation_title(st.session_state.conversation_id,
        title = user_input[:40])
    history = [] 
    for message in st.session_state.messages:
        role = "model" if message["role"] == "assistant" else "user"
        history.append(types.Content(role=role,parts=[types.Part.from_text(text=message["content"])]))
    response = client.models.generate_content(model="gemini-3.1-flash-lite", contents= history)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    st.chat_message("user").write(user_input)
    st.chat_message("assistant").write(response.text)   
    cursor.execute("INSERT INTO message (conversation_id, role, content) VALUES (?, ?, ?)",
                (st.session_state.conversation_id, "assistant", response.text))
    conn.commit()
    st.rerun()