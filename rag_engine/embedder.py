# rag_engine/embedder.py
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from configs.setting import PROCESSED_TEXTS_DIR, EMBEDDINGS_DIR, EMBED_MODEL_NAME, CHUNK_SIZE, CHUNK_OVERLAP

# Using open-source sentence-transformers model from settings
embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)

# Text splitter for better chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,       # from settings
    chunk_overlap=CHUNK_OVERLAP, # from settings
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)

def create_vector_db():
    texts = []
    metadatas = []

    for txt_file in Path(PROCESSED_TEXTS_DIR).iterdir():
        if txt_file.suffix != ".txt":
            continue

        # Read processed text file
        content = txt_file.read_text(encoding="utf-8")
        # Create smaller chunks with overlap
        chunks = text_splitter.split_text(content)

        # Extract category from filename prefix
        category = txt_file.stem.split("_")[0]

        for chunk in chunks:
            chunk = chunk.strip()
            if chunk:
                texts.append(chunk)
                metadatas.append({
                    "source": txt_file.stem,
                    "category": category
                })

    # Create ChromaDB vector store
    db = Chroma.from_texts(
        texts,
        embeddings,
        metadatas=metadatas,
        persist_directory=str(EMBEDDINGS_DIR)
    )

    db.persist()
    print(f"✅ Vector DB created with {len(texts)} chunks → {EMBEDDINGS_DIR}")

if __name__ == "__main__":
    create_vector_db()
