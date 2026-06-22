import streamlit as st
import google.generativeai as genai

# --- APP CONFIGURATION ---
st.set_page_config(page_title="AI Coding Tutor", page_icon="🐍")

# --- PERSONA PROMPTS ---
PERSONAS = {
    "Mister Sharma": (
        "You are Mister Sharma, a strict and formal Indian coding teacher. "
        "You call the student 'Beta'. You are very disciplined and scold the student "
        "for making silly syntax errors or being lazy. You want them to be the best "
        "coder in the world through hard work. Keep your tone formal and authoritative."
    ),
    "Bro": (
        "You are 'Bro', a chill, high-energy coding buddy. Use slang like 'lit', 'bet', 'no cap', "
        "and 'grind'. You are very encouraging and tell the student that bugs are just "
        "part of the journey. Keep it relaxed and friendly."
    ),
    "Grandma": (
        "You are 'Grandma', a sweet and patient tutor. You explain complex Python logic "
        "using analogies like baking cookies, knitting sweaters, or sharing chocolates. "
        "You are never angry, only encouraging and warm."
    )
}

# --- SIDEBAR ---
with st.sidebar:
    st.title("Settings")
    # API Key Input
    api_key = st.text_input("Enter Gemini API Key", type="password")
    
    # Avatar Selection
    avatar_choice = st.selectbox("Choose your Tutor:", list(PERSONAS.keys()))
    
    st.divider()
    st.info(f"Currently learning with: **{avatar_choice}**")

# --- GEMINI SETUP ---
if api_key:
    genai.configure(api_key=api_key)
else:
    st.warning("Please enter your Google Gemini API Key in the sidebar to start.")

# --- CHAT INTERFACE ---
st.title(f"Chatting with {avatar_choice}")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask a Python question..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if not api_key:
        st.error("Missing API Key!")
    else:
        try:
            # Prepare the model with the persona as a system instruction
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=PERSONAS[avatar_choice]
            )

            # Generate response
            response = model.generate_content(prompt)
            full_response = response.text

            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(full_response)
            
            # Save to history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
