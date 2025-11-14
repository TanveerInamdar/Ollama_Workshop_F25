"""Local Llama 3 Chatbot with PDF/DOCX/PPTX support"""
import streamlit as st
from llm_client import generate_response
from file_utils import list_files, extract_text

st.set_page_config(page_title="Llama 3 Chatbot", page_icon="🦙")

# Sidebar - File selection
with st.sidebar:
    st.header("📄 Document Selection")
    files = list_files()

    if files:
        selected = st.selectbox("Choose a file:", ["None"] + files)

        if selected != "None" and st.button("Load File"):
            # Initialize per-file storage if not already (for no chat-history mixing)
            st.session_state.file_texts = st.session_state.get("file_texts", {})
            st.session_state.file_histories = st.session_state.get("file_histories", {})

            # Extract text and set max_chars (can adjust / is optional)
            st.session_state.file_texts[selected] = extract_text(selected, max_chars=4000)
            st.session_state.file_histories[selected] = []

            # Track which file is currently active
            st.session_state.current_file = selected
            st.success(f"✅ Loaded {selected}")

        if "current_file" in st.session_state:
            st.info(f"📖 {st.session_state.current_file}")
            if st.button("Clear"):
                file = st.session_state.current_file
                del st.session_state.file_texts[file]
                del st.session_state.file_histories[file]
                del st.session_state.current_file
                st.rerun()
    else:
        st.warning("No files found. Add files to `files` folder.")

# Initialize general chat messages (optional, if using across files)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history for the current file
current_file = st.session_state.get("current_file")
if current_file and current_file in st.session_state.file_histories:
    for msg in st.session_state.file_histories[current_file]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    if not current_file:
        st.warning("Please load a file first!")
    else:
        # Prepare prompt with file context
        context = st.session_state.file_texts[current_file]
        full_prompt = f"Context from file '{current_file}':\n{context}\n\nQuestion: {prompt}"

        # Add user message to prompt
        st.session_state.file_histories[current_file].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("..."):
                response = generate_response(st.session_state.file_histories[current_file], full_prompt)
                st.markdown(response)

        # Save the response to chat file history
        st.session_state.file_histories[current_file].append({"role": "assistant", "content": response})
