import streamlit as st
from pathlib import Path

from modules.doc_parser import parse_document
from modules.doc_classifier import classify_document
from modules.checklist_verifier import verify_checklist
from modules.redflag_detector import detect_red_flags
from modules.commentor import add_comments_to_docx
from modules.report_generator import generate_report

# Config
st.set_page_config(page_title="ADGM Corporate Compliance Checker", layout="wide")
st.title("🏢 ADGM Corporate Compliance Checker")

UPLOAD_DIR = Path("uploaded_docs")
UPLOAD_DIR.mkdir(exist_ok=True)

# Multi-file upload
uploaded_files = st.file_uploader(
    "Upload one or more DOCX/PDF files", 
    type=["docx", "pdf"], 
    accept_multiple_files=True
)

if uploaded_files:
    all_checklist_present = []
    all_checklist_missing = []
    all_redflags = []
    all_entity_types = []
    annotated_paths = []

    for uploaded_file in uploaded_files:
        # Save uploaded file
        temp_path = UPLOAD_DIR / uploaded_file.name
        temp_path.write_bytes(uploaded_file.read())
        st.success(f"✅ File uploaded: {uploaded_file.name}")

        # 1️⃣ Parse document
        with st.spinner(f"📄 Parsing {uploaded_file.name}..."):
            doc_text = parse_document(str(temp_path))
        if not doc_text:
            st.error(f"❌ Could not parse {uploaded_file.name}")
            continue

        # 2️⃣ Classify
        classification = classify_document(str(temp_path), doc_text)
        entity_type = classification.get("entity_type")
        if not entity_type:
            st.error(f"❌ Could not classify {uploaded_file.name}")
            continue
        all_entity_types.append(entity_type)
        st.info(f"**Entity Type for {uploaded_file.name}:** {entity_type}")

        # 3️⃣ Checklist Verification
        checklist_results = verify_checklist(entity_type)
        all_checklist_present.extend(checklist_results['present'])
        all_checklist_missing.extend(checklist_results['missing'])

        # 4️⃣ Red Flag Detection
        redflag_findings = detect_red_flags(str(temp_path))
        all_redflags.extend(redflag_findings)

        # 5️⃣ Annotate Document if DOCX
        if temp_path.suffix.lower() == ".docx":
            annotated_path = temp_path.with_name(temp_path.stem + "_annotated.docx")
            add_comments_to_docx(str(temp_path), redflag_findings, str(annotated_path))
            annotated_paths.append(annotated_path)
            with open(annotated_path, "rb") as f:
                st.download_button(f"📥 Download Annotated DOCX: {annotated_path.name}", f, file_name=annotated_path.name)

    # Remove duplicates in checklist results
    all_checklist_present = sorted(set(all_checklist_present))
    all_checklist_missing = sorted(set(all_checklist_missing))

    # Show combined checklist
    st.subheader("📋 Combined Checklist Verification")
    st.write(f"✅ Present Documents: {len(all_checklist_present)}", all_checklist_present)
    st.write(f"❌ Missing Documents: {len(all_checklist_missing)}", all_checklist_missing)

    # Show combined red flags
    st.subheader("⚖ Combined Red Flag Findings")
    if all_redflags:
        st.json(all_redflags)
    else:
        st.success("No compliance issues found.")

    # 6️⃣ Generate combined final report
    report_path = "final_compliance_report.json"
    generate_report(
        entity_type=", ".join(set(all_entity_types)),
        checklist_results={"present": all_checklist_present, "missing": all_checklist_missing},
        redflag_findings=all_redflags,
        annotated_docx_path=", ".join([str(p) for p in annotated_paths]) if annotated_paths else "N/A",
        output_json_path=report_path
    )
    with open(report_path, "rb") as f:
        st.download_button("📥 Download Combined Compliance Report (JSON)", f, file_name=Path(report_path).name)

    st.success("🎯 Compliance check complete for all uploaded files.")
