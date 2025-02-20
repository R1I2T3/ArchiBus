import streamlit as st
import google.generativeai as genai

print()

# Configure the Gemini model
genai.configure(api_key=st.secrets['default']['API_KEY'])

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Read system instruction from data.txt
with open("data.txt", "r") as file:
    custom_instruction = file.read().strip()

# Configure the Gemini model with dynamic system instruction
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    system_instruction=f"""Your helpful assistant for Archibus. Your name is Archibus AI , Always reply in Japanese."""
)



chat_session = model.start_chat(history=[
    {"role": "user", "parts": [custom_instruction]}
])


def init_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def handle_user_input(prompt: str):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response using the Gemini model
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Sending the message to Gemini Pro and receiving the response
            response = chat_session.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})


def main():
    # Set up Streamlit page
    st.set_page_config(page_title="Archibus AI", layout="wide")
    st.title("Archibus AI")

    # Add welcome message
    st.markdown("Archibusへようこそ")

    # Initialize chat history
    init_chat_history()

    # Display chat interface
    display_chat_history()

    # Chat input
    if prompt := st.chat_input("Ask me about anything..."):
        handle_user_input(prompt)

if __name__ == "__main__":
    main()
