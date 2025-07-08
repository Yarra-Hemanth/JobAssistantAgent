# extract_utils.py
import docx2txt
# import textract
import fitz  # PyMuPDF

def extract_text_from_pdf(file):
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "\n".join([page.get_text() for page in doc])
    except:
        return "Failed to extract PDF text."

def extract_text_from_docx(file):
    return docx2txt.process(file)

def extract_text_from_txt(file):
    return file.read().decode('utf-8')


def extract_resume(uploaded_file):
    if uploaded_file is None:
        return "No file uploaded."

    file_name = uploaded_file.name.lower()

    if file_name.endswith('.pdf'):
        return extract_text_from_pdf(uploaded_file)
    elif file_name.endswith('.docx'):
        return extract_text_from_docx(uploaded_file)
    elif file_name.endswith('.txt'):
        return extract_text_from_txt(uploaded_file)
    else:
        return "Unsupported resume format"
