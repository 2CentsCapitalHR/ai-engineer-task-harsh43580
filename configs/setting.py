# configs/settings.py
from pathlib import Path

# ---------------- Paths ----------------
BASE_DIR = Path(__file__).resolve().parent.parent  # Project root
RAW_DOCS_DIR = BASE_DIR / "data/adgm_reference_docs"
PROCESSED_TEXTS_DIR = BASE_DIR / "data/processed_texts"
EMBEDDINGS_DIR = BASE_DIR / "data/embeddings"
CHECKLIST_FILE = BASE_DIR / "configs/checklist.json"

# ---------------- RAG Engine Settings ----------------
EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
RETRIEVAL_K = 5
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

# ---------------- LLM Settings ----------------
GEMINI_MODEL = "gemini-1.5-flash"  # Free-tier
SYSTEM_PROMPT = "You are an ADGM corporate compliance expert."

# ---------------- Other ----------------
LOG_LEVEL = "INFO"
