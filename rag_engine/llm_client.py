# rag_engine/llm_client.py
import os
import sys
import logging
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv

# ---------------- Logging Setup ----------------
LOG_FILE = "logs/llm_client.log"
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

# ---------------- Load API Key ----------------
# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    logger.error("❌ GEMINI_API_KEY not found in environment variables.")
    sys.exit(1)

# ---------------- Configure Gemini ----------------
try:
    genai.configure(api_key=API_KEY)
    logger.info("✅ Gemini API configured successfully.")
except Exception as e:
    logger.exception("❌ Failed to configure Gemini API.")
    sys.exit(1)

# ---------------- Functions ----------------
def ask_gemini(prompt: str, model: str = "gemini-1.5-flash") -> str:
    """
    Send a prompt to the Gemini model and return the generated text.
    """
    try:
        logger.info(f"Sending prompt to Gemini model: {model}")
        response = genai.GenerativeModel(model).generate_content(prompt)
        text_out = response.text.strip()
        logger.info("✅ Gemini response received.")
        return text_out
    except Exception as e:
        logger.exception("❌ Error during Gemini API call.")
        return "Error: Could not get a response from Gemini."

# ---------------- Script Entry Point ----------------
if __name__ == "__main__":
    logger.info("🚀 Gemini LLM Client started.")
    user_prompt = input("Enter your query for Gemini: ").strip()
    if not user_prompt:
        logger.warning("⚠️ No prompt provided. Exiting.")
        sys.exit(0)

    answer = ask_gemini(user_prompt)
    print("\n--- Gemini Response ---")
    print(answer)
    logger.info("🏁 Gemini LLM Client finished.")
