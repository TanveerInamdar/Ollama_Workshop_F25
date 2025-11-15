"""Local Llama 3 Chatbot with PDF support"""
import streamlit as st
from llm_client import generate_response
from pdf_utils import list_pdfs, extract_text, extract_text_from_upload, save_uploaded_file

st.set_page_config(page_title="Llama 3 Chatbot", page_icon="🦙")

# Sidebar - PDF Selection
with st.sidebar:
    st.header("📄 PDF Selection")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload PDF from your computer", 
        type="pdf",
        help="Upload a PDF file to ask questions about it"
    )
    
    # Auto-load when file is uploaded
    if uploaded_file is not None:
        # Check if this is a new file (not already loaded)
        if st.session_state.get("last_uploaded_file") != uploaded_file.name:
            with st.spinner("Loading PDF..."):
                # Save the file to pdfs folder
                saved_filename = save_uploaded_file(uploaded_file)
                
                if saved_filename:
                    # Extract text from the uploaded file
                    pdf_text = extract_text_from_upload(uploaded_file)
                    st.session_state.pdf_text = pdf_text
                    st.session_state.pdf_name = saved_filename
                    st.session_state.last_uploaded_file = uploaded_file.name
                    st.success(f"✅ Loaded and saved: {saved_filename}")
                    st.rerun()
                else:
                    st.error("❌ Failed to save PDF file")
    
    st.divider()
    
    # Existing PDF selection from folder
    pdfs = list_pdfs()
    
    if pdfs:
        st.subheader("Load from Folder")
        selected = st.selectbox("Choose a PDF:", ["None"] + pdfs)
        
        if selected != "None" and st.button("Load PDF"):
            st.session_state.pdf_text = extract_text(selected)
            st.session_state.pdf_name = selected
            st.success(f"✅ {selected}")
            st.rerun()
        
        if "pdf_name" in st.session_state:
            st.info(f"📖 {st.session_state.pdf_name}")
            if st.button("Clear"):
                del st.session_state.pdf_text, st.session_state.pdf_name
                st.session_state.pop("last_uploaded_file", None)
                st.rerun()
    else:
        st.warning("No PDFs found. Add files to `pdfs` folder or upload above.")

# Initialize chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add PDF context if loaded
    full_prompt = prompt
    if "pdf_text" in st.session_state:
        full_prompt = f"Context: {st.session_state.pdf_text}\n\nQuestion: {prompt}"
    
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("..."):
            response = generate_response(st.session_state.messages, full_prompt)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
