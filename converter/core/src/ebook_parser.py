import os
from PyPDF2 import PdfReader
import docx

def parse_text(file_path: str) -> str:
    """
    Parses a .txt, .pdf, or .docx file and returns its content.
    """
    _, extension = os.path.splitext(file_path)
    try:
        if extension == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        elif extension == ".pdf":
            return parse_pdf(file_path)
        elif extension == ".docx":
            return parse_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {extension}")
    except Exception as e:
        raise ValueError(f"Error parsing file: {e}")

def parse_pdf(file_path: str) -> str:
    """
    Parses a .pdf file and returns its content.
    """
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise ValueError(f"Error parsing PDF: {e}")

def parse_docx(file_path: str) -> str:
    """
    Parses a .docx file and returns its content.
    """
    try:
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        raise ValueError(f"Error parsing DOCX: {e}")