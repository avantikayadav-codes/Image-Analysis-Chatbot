import streamlit as st
import google.generativeai as genai
import os, uuid

# ✅ Configure Gemini model (Replace with your own key)
genai.configure(api_key="AIzaSyCYk1TFesCCS7xerngzDa2XWsZw3y3zB0s")
model = genai.GenerativeModel("gemini-2.0-flash")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------- Image + Text processing ----------
def process_image_and_chat(image_file, user_message):
    file_extension = os.path.splitext(image_file.name)[-1]
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_extension}")

    with open(file_path, "wb") as buffer:
        buffer.write(image_file.getbuffer())

    try:
        image_data = genai.upload_file(file_path)
        result = model.generate_content([user_message, image_data])
        return result.text or "No response received."
    except Exception as e:
        return f"Error: {e}"

# ---------- Custom CSS ----------
def load_css():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url('https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=1920&auto=format&fit=crop');
            background-size: cover;
            background-position: center;
        }
        .title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #ffffff;
            text-align: center;
            margin: 20px 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        .bot-message {
            display: flex;
            align-items: flex-start;
            margin-bottom: 15px;
        }
        .bot-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin-right: 10px;
            background-image: url('C:\\lab\\2ndsem\\ailab\\aiproject\\userimage.png');
            background-size: cover;
            background-position: center;
        }
        .bot-text {
            background: #6B7280;
            color: white;
            padding: 12px 16px;
            border-radius: 10px;
            max-width: 70%;
            font-family: 'Arial', sans-serif;
            font-size: 16px;
            line-height: 1.5;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .user-message {
            display: flex;
            align-items: flex-start;
            justify-content: flex-end;
            margin-bottom: 15px;
        }
        .user-text {
            background: #4B5EAA;
            color: white;
            padding: 12px 16px;
            border-radius: 10px;
            max-width: 70%;
            font-family: 'Arial', sans-serif;
            font-size: 16px;
            line-height: 1.5;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .user-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin-left: 10px;
            background-image: url('C:\\lab\\2ndsem\\ailab\\aiproject\\userimage.png');
            background-size: cover;
            background-position: center;
        }
        .input-area {
            margin: 0 auto;
            max-width: 800px;
            background: rgba(255, 255, 255, 0.9);
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }
        .stFileUploader > div > div {
            background: #ffffff;
            border-radius: 5px;
            padding: 5px;
        }
        .stTextInput > div > div > input {
            background: #ffffff;
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
        }
        .stButton > button {
            background-color: #6B7280;
            color: #ffffff;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 1rem;
            font-weight: bold;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stButton > button:hover {
            background-color: #5B6475;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ---------- Main App ----------
def main():
    load_css()
    st.markdown('<div class="title">Conversational Image Recognition Chatbot</div>', unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = []
        st.session_state.conversation.append(
            {"role": "bot", "content": "Hello! I'm your image assistant. Upload an image and ask me anything about it!"}
        )

    # Display chat
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for message in st.session_state.conversation:
            if message["role"] == "bot":
                st.markdown(
                    '<div class="bot-message">'
                    '<div class="bot-avatar"></div>'
                    f'<div class="bot-text">{message["content"]}</div>'
                    '</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<div class="user-message">'
                    f'<div class="user-text">{message["content"]}</div>'
                    '<div class="user-avatar"></div>'
                    '</div>',
                    unsafe_allow_html=True,
                )
        st.markdown('</div>', unsafe_allow_html=True)

    # Upload + Input
    with st.container():
        st.markdown('<div class="input-area">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp"])
        st.session_state["uploaded_file"] = uploaded_file

        if uploaded_file:
            user_message = st.chat_input("Ask a question about the image...")
            if user_message:
                st.session_state.conversation.append({"role": "user", "content": user_message})

                if user_message.lower() in ["hi", "hello", "hey"]:
                    bot_response = "Hello! How can I assist you with this image today?"
                elif user_message.lower() in ["thanks", "thank you"]:
                    bot_response = "You're welcome! Any more questions about the image?"
                else:
                    bot_response = process_image_and_chat(uploaded_file, user_message)

                st.session_state.conversation.append({"role": "bot", "content": bot_response})
                st.rerun()
        else:
            st.warning("Please upload an image to start chatting.")
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
