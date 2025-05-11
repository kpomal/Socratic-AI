import streamlit as st
import google.generativeai as genai
import datetime

# Gemini API Key Configuration
API_KEY = "AIzaSyAbJ3tch_ZdD9JKAp0IAnDpGgLl2SZir64"
genai.configure(api_key=API_KEY)

# Function to generate response using Gemini
def generate_gemini_response(prompt: str) -> str:
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")  # Use supported model
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else "No response from Gemini."
    except Exception as e:
        return f"Error from Gemini API: {e}"

# Generate downloadable text content for chat history
def get_chat_history_text(history):
    lines = []
    for msg in history:
        role = "You" if msg["role"] == "user" else "Socratic Tutor"
        lines.append(f"{role}:\n{msg['content']}\n")
    return "\n".join(lines)

# Streamlit Page Configuration
st.set_page_config(
    page_title="Socratic Tutor - Gemini Interview Coach",
    page_icon="🎓",
    layout="centered"
)

# Custom UI Styling for Desktop
st.markdown(
    """
    <style>
    body, html {
        background: #1a1a2e;
        color: #eaeaea;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    [data-testid="stAppViewContainer"] {
        max-width: 800px;  /* Increased max width for desktop */
        margin: auto;
        background: #16213e;
        padding: 2rem 3rem;
        border-radius: 10px;
        box-shadow: 0 0 25px rgba(33,150,243,0.8);
    }
    h1 {
        color: #00aaff;
        text-align: center;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .chat-bubble {
        border-radius: 12px;
        padding: 14px 18px;
        margin: 10px 0;
        max-width: 85%;
        word-wrap: break-word;
        font-size: 1.1rem;
        line-height: 1.5;
        box-shadow: 1px 1px 5px rgba(0,0,0,0.2);
    }
    .user {
        background: #00aaff;
        color: #123c69;
        margin-left: auto;
        text-align: right;
    }
    .ai {
        background: #324376;
        color: #d6e0f0;
        margin-right: auto;
        text-align: left;
    }
    input[type="text"], textarea {
        border-radius: 10px;
        padding: 0.85rem 1.2rem;
        font-size: 1.1rem;
        border: none;
        width: 100%;
        box-sizing: border-box;
        margin-bottom: 1.2rem;
        background-color: #243255;
        color: #e1e6f0;
        resize: vertical;
    }
    input[type="text"]::placeholder,
    textarea::placeholder {
        color: #8899bb;
    }
    button {
        background: #00aaff;
        color: #123c69;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 700;
        font-size: 1.1rem;
        cursor: pointer;
        transition: background-color 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 10px rgba(0,170,255,0.4);
        margin-top: 0.5rem;
    }
    button:hover {
        background: #0094d6;
    }
    .links-section {
        margin-top: 2rem;
        background: #223366;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        color: #aaccff;
    }
    .links-section h2 {
        color: #00aaff;
        margin-bottom: 0.75rem;
    }
    .links-section a {
        color: #66bbff;
        text-decoration: none;
    }
    .links-section a:hover {
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App Title and Instructions
st.title("🎓 Socratic Tutor - Gemini Interview Coach")
st.write("Ask an interview question or request mock questions. Optionally include a job description.")

# Initialize chat history in session state
if "history" not in st.session_state:
    st.session_state.history = []

# User Input Form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Your question or request:")
    job_description = st.text_area("Job description (optional):", height=120)
    send = st.form_submit_button("Send")

# Handle input when form is submitted
if send and user_input.strip():
    st.session_state.history.append({"role": "user", "content": user_input.strip()})
    lower_input = user_input.lower()

    if "generate interview questions" in lower_input or "mock questions" in lower_input:
        prompt = "Generate 5 mock interview questions"
        if job_description.strip():
            prompt += f" for the following job description:\n{job_description.strip()}"
        else:
            prompt += " for a general software engineering role."
    else:
        prompt = f"You are an expert interview coach. Answer this interview question:\n\n{user_input.strip()}"
        if job_description.strip():
            prompt += f"\n\nJob Description:\n{job_description.strip()}"

    ai_response = generate_gemini_response(prompt)
    st.session_state.history.append({"role": "ai", "content": ai_response})

# Display chat history with styled chat bubbles
for msg in st.session_state.history:
    bubble_class = "user" if msg["role"] == "user" else "ai"
    content_html = msg["content"].replace("\n", "<br>")
    st.markdown(f'<div class="chat-bubble {bubble_class}">{content_html}</div>', unsafe_allow_html=True)

# Download chat history button
if st.session_state.history:
    chat_text = get_chat_history_text(st.session_state.history)
    now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"socratic_tutor_chat_{now_str}.txt"
    st.download_button(
        label="Download Chat History",
        data=chat_text,
        file_name=file_name,
        mime="text/plain"
    )


