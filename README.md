# Local Llama 3 Chatbot

A simple Streamlit web app for chatting with Ollama's Llama 3 model locally.

## Features

- Chat with Llama 3 model via Ollama
- Load PDF/DOCX/PPTX files from the project folder and ask questions about them
- Simple, beginner-friendly code
- Sidebar Document selection interface

## How to Run

1. Install Ollama and pull the Llama 3 model
2. Create a virtual environment
3. Install dependencies from `requirements.txt`
4. Place your PDF files in the `files` folder (created automatically on first run)
5. Run the Streamlit app with: `streamlit run app/main.py`
6. Select a document from the sidebar dropdown and click "Load File"
7. Start chatting about the document content!

## Prerequisites

- Python 3.8+
- Ollama installed locally with Llama 3 model

