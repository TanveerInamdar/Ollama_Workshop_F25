"""PDF utility functions"""
from pathlib import Path
from PyPDF2 import PdfReader

PDF_FOLDER = Path(__file__).parent.parent / "pdfs"
PDF_FOLDER.mkdir(exist_ok=True)


def list_pdfs():
    """Return list of PDF filenames in pdfs folder"""
    return sorted([f.name for f in PDF_FOLDER.glob("*.pdf")])


def extract_text(filename):
    """Extract text from PDF file"""
    pdf_path = PDF_FOLDER / filename
    
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip() or "No text found in PDF"
    except Exception as e:
        return f"Error reading PDF: {e}"


def save_uploaded_file(uploaded_file):
    """Save uploaded file to pdfs folder and return the filename"""
    try:
        file_path = PDF_FOLDER / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return uploaded_file.name
    except Exception as e:
        return None


def extract_text_from_upload(uploaded_file):
    """Extract text directly from uploaded file object"""
    try:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip() or "No text found in PDF"
    except Exception as e:
        return f"Error reading PDF: {e}"

