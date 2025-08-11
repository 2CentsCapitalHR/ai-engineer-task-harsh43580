<<<<<<< HEAD
# ADGM Corporate Agent – Compliance Automation Assistant

This project is an intelligent, end-to-end compliance assistant designed for the Abu Dhabi Global Market (ADGM) ecosystem. It automates the parsing, classification, verification, and red-flag analysis of incorporation and regulatory documents using advanced LLM-powered RAG (Retrieval-Augmented Generation) techniques.

## Features

- **Document Parsing**: Extract clean, structured text from uploaded PDFs and DOCX files.
- **AI Classification**: Automatically detect the ADGM entity type for each document.
- **Checklist Verification**: Match uploaded documents to required ADGM checklists; highlight present and missing items.
- **Red Flag Detection**: Analyze document clauses with RAG+LLM (e.g., Gemini) to identify compliance weaknesses and highlight risks.
- **Inline Annotation**: Insert AI-generated compliance comments into DOCX originals.
- **Final Reports**: Merge all findings (present/missing docs, flagged issues, annotated files) into a downloadable JSON (and optionally annotated DOCX).

## Project Structure

adgm_corporate_agent/
├── app.py # Streamlit Web App (Main Interface)
├── uploaded_docs/ # Uploaded and processed user files
├── configs/
│ ├── checklist.json # Entity-specific ADGM checklist definitions
│ └── settings.py # Central project config (paths, models, constants)
├── modules/
│ ├── init.py
│ ├── doc_parser.py # PDF/DOCX text extraction
│ ├── doc_classifier.py # AI document/entity classification
│ ├── checklist_verifier.py # Checklist presence/missing verification
│ ├── redflag_detector.py # Clause-level RAG+LLM compliance analysis
│ ├── commentor.py # Annotate DOCX with AI compliance comments
│ └── report_generator.py # Combine all findings into a report
├── rag_engine/
│ ├── embedder.py # Embedding/chunking and vector DB creation
│ ├── retriever.py # ChromaDB vector search utilities
│ └── llm_client.py # Gemini LLM API integration
├── data/
│ ├── adgm_reference_docs/ # ADGM reference/policy documents for RAG
│ ├── processed_texts/ # Processed, textified user docs for workflow
│ └── embeddings/ # ChromaDB vector store
└── requirements.txt # All Python dependencies


## Setup & Installation

1. **Clone the repository**

    ```
    git clone <your-repo-url>
    cd adgm_corporate_agent
    ```

2. **Create and activate a Python virtual environment**

    ```
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3. **Install all required packages**

    ```
    pip install -r requirements.txt
    ```
    Main dependencies include:
    - streamlit
    - pdfplumber
    - python-docx
    - langchain
    - chromadb
    - sentence-transformers
    - (and more for LLM APIs)

4. **Configure .env and Settings**

    - Store your Gemini API key in a `.env` file or as an environment variable if required.
    - Adjust `configs/settings.py` if you want to change paths, models, or chunking parameters.

5. **Prepare the Vector Database (RAG engine)**

    - Place your ADGM legal reference docs (PDF/DOCX/text) in `data/adgm_reference_docs/`.
    - Parse and chunk them into embeddings using:

      ```
      python rag_engine/embedder.py
      ```
      This will create a ChromaDB vectorstore for fast retrieval during red-flag detection.

## Usage

### 1. **Start the Streamlit Compliance Web App**

streamlit run app.py


- Upload one or more ADGM-related DOCX/PDF documents via the web UI.
- The app will:
  - Parse and classify documents
  - Check which checklist requirements are satisfied or missing
  - Run AI-powered compliance checks
  - Offer annotated downloads (DOCX + JSON report)

### 2. **Command-line (alternate) Usage**

If you still want to run the CLI pipeline for one document at a time:

python app.py uploaded_docs/sample.docx


## Configuration

- **`configs/settings.py`**: All paths, chunk sizes, models, and other global settings.
- **`configs/checklist.json`**: Edit or add checklists for additional ADGM entity types.
- **Vector DB and models**: Easily replaceable via the config file.

## How the Workflow Operates

1. **Document Upload**
 - User uploads one or more files via Streamlit.
2. **Parsing & Classification**
 - Files are converted to clean text and AI-classified (by keywords or embeddings).
3. **Checklist Verification**
 - Required documents for the detected entity type are checked against uploads.
4. **Red-Flag Detection (RAG + Gemini)**
 - Document text is chunked and compared with ADGM rules using ChromaDB embedding search.
 - Each clause is flagged for compliance issues using Gemini LLM.
5. **Annotation & Report Generation**
 - Annotated Word files available for download (with AI comments).
 - Structured JSON report generated for each submission.

## Supported ADGM Entity Types

- Private Company Limited by Shares (Non-Financial)
- Private Company Limited by Guarantee (Non-Financial)
- Private Company Limited by Shares (Financial)
- SPV / Special Purpose Vehicles
- LLPs & Branches
- (More can easily be added via your checklist/config files.)

## Sample Test Documents

To fully exercise the pipeline, try uploading (together or one by one):

- "Articles of Association"
- "Consent to Act (Director/Secretary)"
- "Ultimate Beneficial Owner (UBO) Declaration Form"
- "Board Resolution for Incorporation"
- "Beneficial Ownership Register Template"

Try purposely leaving out one requirement, or using incomplete/inaccurate clauses, and watch the red-flag detector in action!

## Troubleshooting & Tips

- If a required document isn't recognized: Check its filename formatting and content; normalization logic may need small adjustments for new templates.
- If you hit `"ModuleNotFoundError"`: Check your virtual environment and dependencies with `pip list`.
- If red-flag findings seem off: Double-check your vector DB is up to date, and that high-quality ADGM reference documents are present in `data/adgm_reference_docs/` with the vector store rebuilt.

## Roadmap and Further Enhancements

- PDF annotation support (currently only DOCX inline comments).
- Enhanced UI: color-coded checklist status, expandable flag explanations, preview of annotated files.
- Multi-model RAG support (open-source + Gemini hybrid).
- Integration with email/document workflows for corporate agents.

## License and Contribution

This codebase is provided for internal/enterprise regulatory workflow automation.  
Feel free to open issues or pull requests for improvements!

---

**Questions or need a test file?**  
Open an issue or contact the author.
=======
[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/vgbm4cZ0)
>>>>>>> 2e0aa4164ca191ff31431c5619774f61c7a2d35f
