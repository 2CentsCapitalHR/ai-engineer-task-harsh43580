# rag_engine/retriever.py
import os
import sys
import logging
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from configs.setting import EMBEDDINGS_DIR, EMBED_MODEL_NAME, RETRIEVAL_K

# ---------------- Logging Setup ----------------
LOG_FILE = "logs/retriever.log"
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ---------------- Constants ----------------
PERSIST_DIR = str(EMBEDDINGS_DIR)
EMBEDDING_MODEL = EMBED_MODEL_NAME
K = RETRIEVAL_K

# ---------------- Functions ----------------
def load_embeddings():
    """Load HuggingFace embeddings model with error handling."""
    try:
        logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")
        return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    except Exception as e:
        logger.exception("Failed to load embeddings model.")
        sys.exit(1)

def get_retriever():
    """Return a retriever instance from ChromaDB with error handling."""
    if not Path(PERSIST_DIR).exists():
        logger.error(f"ChromaDB persist directory not found: {PERSIST_DIR}")
        sys.exit(1)

    embeddings = load_embeddings()

    try:
        logger.info(f"Loading ChromaDB from: {PERSIST_DIR}")
        db = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
        return db.as_retriever(search_kwargs={"k": K})
    except Exception as e:
        logger.exception("Failed to load ChromaDB.")
        sys.exit(1)

def run_query(query: str):
    """Run a similarity search and return results."""
    retriever = get_retriever()
    try:
        results = retriever.get_relevant_documents(query)
        if not results:
            logger.warning("No results found for query.")
        else:
            logger.info(f"Retrieved {len(results)} results.")
        return results
    except Exception as e:
        logger.exception("Error during retrieval.")
        return []

# ---------------- Script Entry Point ----------------
if __name__ == "__main__":
    logger.info("Retriever script started.")
    user_query = "What documents are required for company incorporation?"
    logger.info(f"Query: {user_query}")

    results = run_query(user_query)

    for idx, r in enumerate(results, start=1):
        print(f"\n--- Result {idx} ---")
        print(f"Source   : {r.metadata.get('source')}")
        print(f"Category : {r.metadata.get('category')}")
        print(f"Content  :\n{r.page_content}\n")

    logger.info("Retriever script finished.")
