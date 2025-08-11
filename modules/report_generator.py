# module/report_generator.py
import json
import logging, sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def generate_report(entity_type: str,
                    checklist_results: Dict,
                    redflag_findings: List[Dict],
                    annotated_docx_path: str,
                    output_json_path: str = "compliance_report.json"):
    """
    Generate a compliance report combining checklist results and AI findings.
    
    :param entity_type: Detected entity type
    :param checklist_results: dict {present: [...], missing: [...]}
    :param redflag_findings: list of AI findings in dict format
    :param annotated_docx_path: path to annotated DOCX file from commentor
    :param output_json_path: where to save the JSON summary
    """
    report_data = {
        "report_generated_on": datetime.now().isoformat(),
        "entity_type": entity_type,
        "checklist_verification": {
            "present": checklist_results.get("present", []),
            "missing": checklist_results.get("missing", [])
        },
        "red_flag_findings": redflag_findings,
        "annotated_document_path": str(annotated_docx_path)
    }

    try:
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=4, ensure_ascii=False)
        logger.info(f"✅ Compliance report saved to {output_json_path}")
    except Exception as e:
        logger.error(f"Error saving report JSON: {e}")
        return None

    return report_data


if __name__ == "__main__":
    # Dummy test data
    dummy_checklist = {
        "present": ["Model Articles", "Consent to Act (Director/Secretary)"],
        "missing": ["Shareholding Structure Chart"]
    }
    dummy_findings = [
        {
            "section": "Share Capital...",
            "ai_analysis": "⚠ Missing detail on paid-up capital as per ADGM rules."
        },
        {
            "section": "UBO Declaration...",
            "ai_analysis": "⚠ Should specify disclosure of past nationalities."
        }
    ]
    sample_entity = "PrivateCompany_LimitedByShares_NonFinancial"

    generate_report(
        entity_type=sample_entity,
        checklist_results=dummy_checklist,
        redflag_findings=dummy_findings,
        annotated_docx_path="uploaded_docs/annotated.docx",
        output_json_path="final_report.json"
    )
