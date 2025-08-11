# module/checklist_verifier.py
import json
import logging
import sys
from pathlib import Path
from configs.setting import CHECKLIST_FILE, PROCESSED_TEXTS_DIR

# ---------------- Console Logging ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# ---------------- Helpers ----------------
def load_checklist():
    """Load checklist.json into memory."""
    if not CHECKLIST_FILE.exists():
        logger.error(f"Checklist file not found: {CHECKLIST_FILE}")
        return {}
    try:
        with open(CHECKLIST_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info("✅ Checklist loaded.")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {CHECKLIST_FILE}: {e}")
        return {}

def normalize_name(name: str) -> str:
    """Normalize strings for matching (lowercase, no special chars)."""
    import re
    return re.sub(r'[^a-z0-9]', '', name.lower())

def verify_checklist(entity_type: str):
    """
    For a given entity type, checks which checklist docs are present in processed_texts.
    Returns dict with 'present' and 'missing'.
    """
    checklist_data = load_checklist()
    if entity_type not in checklist_data:
        logger.warning(f"No checklist found for entity type: {entity_type}")
        return {"present": [], "missing": []}

    required_docs = checklist_data[entity_type]
    # Normalize required names
    required_norm = {normalize_name(doc): doc for doc in required_docs}

    # Gather processed text filenames
    present_files = [f.stem for f in Path(PROCESSED_TEXTS_DIR).glob("*.txt")]
    present_norm = {normalize_name(f): f for f in present_files}

    present, missing = [], []

    for norm_key, original_doc in required_norm.items():
        if any(norm_key in fn for fn in present_norm.keys()):
            present.append(original_doc)
        else:
            missing.append(original_doc)

    return {"present": present, "missing": missing}

# ---------------- Test ----------------
if __name__ == "__main__":
    entity = "PrivateCompany_LimitedByShares_NonFinancial"
    logger.info(f"🔍 Verifying checklist for entity: {entity}")
    results = verify_checklist(entity)

    print("\n✅ PRESENT DOCUMENTS:")
    for doc in results["present"]:
        print(f"  - {doc}")

    print("\n❌ MISSING DOCUMENTS:")
    for doc in results["missing"]:
        print(f"  - {doc}")
