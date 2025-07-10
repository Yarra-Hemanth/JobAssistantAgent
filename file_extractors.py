import docx2txt
import fitz  # PyMuPDF
import asyncio

async def extract_text_from_pdf(file):
    try:
        file_bytes = await file.read()
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        return "\n".join([page.get_text() for page in doc])
    except:
        return "Failed to extract PDF text."


def extract_text_from_docx(file):
    try:
        return docx2txt.process(file)
    except:
        return "Failed to extract DOCX text."

def extract_text_from_txt(file):
    try:
        return file.read().decode('utf-8')
    except:
        return "Failed to extract TXT text."


async def extract_resume(uploaded_file):
    if uploaded_file is None:
        return "No file uploaded."

    file_name = uploaded_file.filename.lower()

    if file_name.endswith('.pdf'):
        return await extract_text_from_pdf(uploaded_file)
    elif file_name.endswith('.docx'):
        return extract_text_from_docx(uploaded_file)
    elif file_name.endswith('.txt'):
        return extract_text_from_txt(uploaded_file)
    else:
        return "Unsupported resume format"

