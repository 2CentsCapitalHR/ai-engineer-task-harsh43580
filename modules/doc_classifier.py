# module/doc_classifier.py
import sys
import logging
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from configs.setting import EMBEDDINGS_DIR, EMBED_MODEL_NAME

# ---------------- Console Logging ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# ---------------- Entity Keyword Map ----------------
ENTITY_KEYWORDS = {
    "PrivateCompany_LimitedByShares_NonFinancial": [
        "private company limited by shares", "non-financial"
    ],
    "PrivateCompany_LimitedByGuarantee_NonFinancial": [
        "private company limited by guarantee", "non-financial"
    ],
    "PrivateCompany_LimitedByShares_Financial": [
        "private company limited by shares", "financial services"
    ],
    "SPV_Continuance": [
        "continuance spv", "special purpose vehicle"
    ],
    "Branch_Financial_NonFinancial": [
        "branch", "financial services", "non-financial services"
    ],
    "LLP_Financial_NonFinancial": [
        "limited liability partnership", "llp"
    ]
}

# ---------------- Helper Functions ----------------
def classify_by_keywords(text: str, filename: str):
    """Check if keywords in filename/content match entity list."""
    combined = f"{filename.lower()} {text.lower()}"
    for entity, keywords in ENTITY_KEYWORDS.items():
        if all(word in combined for word in keywords):
            return entity
    return None

def classify_by_embeddings(text: str):
    """Fallback: Use ChromaDB vector search to guess closest entity type."""
    try:
        embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
        db = Chroma(persist_directory=str(EMBEDDINGS_DIR), embedding_function=embeddings)
        results = db.similarity_search(text, k=1)
        if results:
            return results[0].metadata.get("category")
    except Exception as e:
        logger.error(f"Embedding-based classification failed: {e}")
    return None

def classify_document(file_path: str, file_text: str):
    """Main classification logic."""
    filename = Path(file_path).stem
    logger.info(f"Classifying document: {filename}")

    # 1: Try keyword classification
    entity_type = classify_by_keywords(file_text, filename)
    if entity_type:
        logger.info(f"Matched entity via keywords: {entity_type}")
        return {
            "entity_type": entity_type,
            "category": "checklists_docs" if "checklist" in filename.lower() else "templates"
        }

    # 2: Try embeddings fallback
    entity_type = classify_by_embeddings(file_text)
    if entity_type:
        logger.info(f"Matched entity via embeddings: {entity_type}")
        return {
            "entity_type": entity_type,
            "category": "unknown"
        }

    logger.warning("No classification match found.")
    return {"entity_type": None, "category": None}

# ---------------- Test ----------------
if __name__ == "__main__":
    # Example test data
    sample_file = "uploaded_docs/sample_adgm_checklist.pdf"
    sample_text = "Private Company Limited by Shares – Non-Financial Services Checklist ..."
    result = classify_document(sample_file, sample_text)
    print(result)
