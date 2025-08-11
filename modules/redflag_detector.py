# module/redflag_detector.py
from typing import List, Dict
import logging, sys

from modules.doc_parser import parse_document
from modules.doc_classifier import classify_document
from rag_engine.retriever import get_retriever
from rag_engine.llm_client import ask_gemini  # Our Gemini client

# ---------------- Console Logging ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def detect_red_flags(file_path: str) -> List[Dict]:
    """
    Parse a document, classify it, then check each section for compliance issues
    using RAG retrieval + Gemini LLM.
    """
    # Step 1: Parse document into raw text
    text = parse_document(file_path)
    if not text:
        logger.warning("No text extracted from document.")
        return []

    # (Optional) Split document into sections by paragraphs for focused checking
    sections = [sec.strip() for sec in text.split("\n\n") if sec.strip()]
    
    # Step 2: Classify
    classification = classify_document(file_path, text)
    logger.info(f"Classification: {classification}")

    # Step 3: Get retriever
    retriever = get_retriever()

    findings = []
    for sec in sections:
        # Step 4: Retrieve relevant ADGM rules
        retrieved_docs = retriever.get_relevant_documents(sec)
        references_text = "\n\n".join([doc.page_content for doc in retrieved_docs])
        
        # Step 5: Build prompt for Gemini
        prompt = f"""
        You are an ADGM corporate compliance checker.
        Entity Type: {classification.get("entity_type")}
        Document Clause:
        \"\"\"{sec}\"\"\"
        
        ADGM Regulations & Guidance (retrieved context):
        \"\"\"{references_text}\"\"\"
        
        Task:
        - Check if this clause fully complies with ADGM rules.
        - Flag any compliance risks, missing info, or deviations.
        - Mention the relevant ADGM reference title if possible.
        - Rate severity as Low/Medium/High.
        Respond in JSON with fields: section_summary, issue, reference, severity.
        """

        # Step 6: Call Gemini
        response = ask_gemini(prompt)

        # Step 7: Store finding
        findings.append({
            "section": sec[:80] + "...",  # preview of section
            "ai_analysis": response
        })

    return findings


if __name__ == "__main__":
    sample_file = "uploaded_docs/sample_adgm.docx"
    report = detect_red_flags(sample_file)
    for finding in report:
        print("\n--- Section ---\n", finding["section"])
        print("--- AI Analysis ---\n", finding["ai_analysis"])
