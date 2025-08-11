# module/doc_parser.py
from pathlib import Path
import pdfplumber
import docx
import logging
import sys

# ---------------- Console Logging ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# ---------------- Functions ----------------
def extract_text_from_pdf(file_path: Path) -> str:
    """Extract text from a PDF file."""
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        logger.error(f"Error reading PDF {file_path.name}: {e}")
    return text.strip()

def extract_text_from_docx(file_path: Path) -> str:
    """Extract text from a DOCX file."""
    try:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    except Exception as e:
        logger.error(f"Error reading DOCX {file_path.name}: {e}")
        return ""

def parse_document(file_path: str) -> str:
    """
    Detect file type and return extracted text.
    Supports PDF and DOCX.
    """
    path_obj = Path(file_path)
    if not path_obj.exists():
        logger.error(f"File not found: {file_path}")
        return ""

    logger.info(f"Parsing document: {path_obj.name}")

    if path_obj.suffix.lower() == ".pdf":
        return extract_text_from_pdf(path_obj)
    elif path_obj.suffix.lower() == ".docx":
        return extract_text_from_docx(path_obj)
    else:
        logger.warning(f"Unsupported file type: {path_obj.suffix}")
        return ""

# ---------------- Test ----------------
if __name__ == "__main__":
    # Example test
    sample_pdf = "uploaded_docs/sample.pdf"
    sample_docx = "uploaded_docs/sample.docx"

    for sample in [sample_pdf, sample_docx]:
        text = parse_document(sample)
        print(f"\n--- Extracted from {sample} ---\n{text[:500]}...\n")
