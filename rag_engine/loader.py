# rag_engine/loader.py
import pdfplumber
import docx
from pathlib import Path

RAW_DIR = Path("data/adgm_reference_docs")
PROCESSED_DIR = Path("data/processed_texts")
PROCESSED_DIR.mkdir(exist_ok=True)

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

def run_loader():
    """Recursively process PDF/DOCX files in RAW_DIR subfolders."""
    for file in RAW_DIR.rglob("*"):  # rglob searches recursively
        if file.is_file():
            if file.suffix.lower() == ".pdf":
                text = extract_text_from_pdf(file)
            elif file.suffix.lower() == ".docx":
                text = extract_text_from_docx(file)
            else:
                print(f"Skipping unsupported file: {file.name}")
                continue

            # Category from subfolder name (e.g., template, policies, etc.)
            category = file.parent.name

            # Save processed text with category in filename to avoid duplicates
            out_filename = f"{category}_{file.stem}.txt"
            out_path = PROCESSED_DIR / out_filename
            out_path.write_text(text, encoding="utf-8")

            print(f"✅ Processed: {file.name} (Category: {category}) → {out_path.name}")

if __name__ == "__main__":
    run_loader()
