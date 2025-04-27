from groq import Groq
import streamlit as st 

st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .main {
            background: linear-gradient(135deg, #ff9a9e, #fad0c4, #ffdde1);
        }
        .chat-container {
            max-width: 800px;
            margin: auto;
            padding: 10px;
        }
        .user-msg {
            background: #ffffff;
            color: black;
            padding: 12px;
            border-radius: 20px;
            margin: 5px;
            text-align: left;
            font-weight: bold;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
            width: fit-content;
        }
        .assistant-msg {
            background: #0dcaf0;
            color: white;
            padding: 12px;
            border-radius: 20px;
            margin: 5px;
            text-align: left;
            font-weight: bold;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
            width: fit-content;
        }
        .title {
            font-size: 28px;
            font-weight: bold;
            color: white;
            text-align: center;
            padding: 15px 0;
            background: #212529;
            border-radius: 10px;
            margin-bottom: 5px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
        }
        .quote {
            font-size: 18px;
            font-style: italic;
            color: #ffffff;
            text-align: center;
            padding: 10px;
            background: #343a40;
            border-radius: 8px;
            margin-bottom: 15px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
        }
        .footer {
            text-align: center;
            padding: 15px;
            font-size: 16px;
            color: white;
            background: #212529;
            border-radius: 10px;
            margin-top: 20px;
            box-shadow: 0px -4px 10px rgba(0, 0, 0, 0.3);
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">📚 DSA Tutor Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="quote">"Practice creates confidence. Confidence empowers you." – Simone Biles</div>', unsafe_allow_html=True)

def generate(prompt, history):
    client = Groq(api_key="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")
    stream = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful Data Structures and Algorithms (DSA) tutor for students. You will explain DSA topics step-by-step with examples and motivate students to keep practicing. If a question is not related to DSA, politely refuse to answer it."
            },
            {
                "role": "user",
                "content": f"Conversation history: {history}. Prompt: {prompt}",
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        top_p=1,
        stop=None,
        stream=True,
    )
    output = "" 
    for chunk in stream:
        if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
            output += chunk.choices[0].delta.content
    return output

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi! Tell me which DSA topic you are studying or struggling with?"}]
if "history" not in st.session_state:
    st.session_state["history"] = ""

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(f'<div class="{"user-msg" if msg["role"] == "user" else "assistant-msg"}">{msg["content"]}</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Ask about any DSA topic..."):
    with st.chat_message("user"):
        st.markdown(f'<div class="user-msg">{prompt}</div>', unsafe_allow_html=True)

    st.session_state.messages.append({"role": "user", "content": prompt})

    response = generate(prompt, st.session_state.history)
    msg = response

    st.session_state.history += f"User: {prompt}\nAssistant: {msg}\n"

    st.session_state.messages.append({"role": "assistant", "content": msg})
    with st.chat_message("assistant"):
        st.markdown(f'<div class="assistant-msg">{msg}</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">🔥 Made by Nish | Created with ❤️ to Master DSA Concepts</div>', unsafe_allow_html=True)
