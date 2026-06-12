
import fitz

def extract_pdf_text(uploaded_file):

    pdf = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    text = ""

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text
