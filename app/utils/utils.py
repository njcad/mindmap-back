"""
Utility functions for the app. Includes:
1. Parsing functions for different uploaded file types (txt, docx, pdf)
2. TODO: other utility functions
"""

from docx import Document
import PyPDF2
import io


def parse_txt(file_content):
    text = file_content.decode('utf-8')
    return [line.strip() for line in text.split('\n') if line.strip()]

def parse_docx(file_content):
    doc = Document(io.BytesIO(file_content))
    return [paragraph.text.strip() for paragraph in doc.paragraphs if paragraph.text.strip()]

def parse_pdf(file_content):
    """
    Parses a pdf file and returns a list of questions. 
    Current implementation is very basic and assumes questions are separated by question marks.
    TODO: improve this.
    """
    pdf_file = io.BytesIO(file_content)
    reader = PyPDF2.PdfReader(pdf_file)
    questions = []
    full_text = ""
    
    # First combine all text from all pages
    for page in reader.pages:
        full_text += page.extract_text() + " "
    
    # Split by question marks to identify questions
    potential_questions = full_text.split('?')
    
    for q in potential_questions:
        # Clean up the question
        cleaned = q.strip()
        # Skip if empty or too short
        if not cleaned or len(cleaned) < 5:  
            continue
            
        # Add back the question mark if it's not the last segment
        # (last segment won't be a question since it's after the last question mark)
        if q != potential_questions[-1]:
            cleaned += '?'
            
        # Look for common question starters
        question_starters = ['what', 'why', 'how', 'where', 'when', 'who', 'which', 'whose', 'whom']
        words = cleaned.lower().split()
        
        # Add if it starts with a question word or already has a question mark
        if (words and words[0] in question_starters) or '?' in cleaned:
            questions.append(cleaned)
            
    return questions