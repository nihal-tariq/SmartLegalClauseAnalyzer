import os

from dotenv import load_dotenv
from google import generativeai as genai


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY_gen_ai_"))
model = genai.GenerativeModel(model_name="gemini-2.5-flash")


def detect_legal_nature(query: str) -> str:
    """
    Uses Gemini model to determine if a query is legal in nature.

    Returns:
    - "LEGAL" or "NON-LEGAL"
    """
    legal_keywords = [
        "law", "legal", "contract", "agreement", "clause", "compliance",
        "liability", "indemnity", "jurisdiction", "breach", "force majeure",
        "obligation", "settlement", "statute", "regulation", "remedy",
        "termination", "dispute", "confidentiality", "arbitration"
    ]

    check_prompt = f"""
    If it is a greeting than consider it legal,

You are a legal assistant.  Determine if the following user query is legal in nature based on whether it relates to laws, contracts, clauses, regulations, or compliance.

Use this list of legal keywords as a reference: {', '.join(legal_keywords)}

Query: "{query}"

Respond only with one word: LEGAL or NON-LEGAL.
"""

    response = model.generate_content(check_prompt)
    result = response.text.strip().upper()
    return result
