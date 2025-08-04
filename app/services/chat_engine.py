import os
from collections import defaultdict

from dotenv import load_dotenv
from google import generativeai as genai

from app.utility.intent_classification import classify_intent
from app.utility.legal_nature import detect_legal_nature
from app.utility.prompts_module import (
    definition_prompt,
    clause_retrieval_prompt,
    comparative_analysis_prompt,
)
from app.utility.retriever import get_compressed_context
from app.db import SessionLocal
from app.models import ChatHistory


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY_gen_ai"))
model = genai.GenerativeModel(model_name="gemini-2.5-flash")

session_history = defaultdict(list)
MAX_HISTORY = 6


def handle_chat_query(user_id: str, user_query: str):
    """
    Handles a user's query, verifying legal nature using Gemini,
    then classifying intent and generating a legal response.
    """

    legal_check = detect_legal_nature(user_query)

    if legal_check != "LEGAL":
        return {
            "intent": "Rejected",
            "confidence": 1.0,
            "response": "❌ I only respond to legal questions. Please ask something related to law, contracts, or compliance."
        }

    intent, confidence = classify_intent(user_query)

    context = get_compressed_context(user_query, user_id)

    history = session_history[user_id][-MAX_HISTORY:]
    formatted_history = "\n".join(
        [f"User: {q}\nAssistant: {r}" for q, r in history]
    )

    # Routing
    if intent == "DefinitionQuery":
        prompt = definition_prompt.format(
            user_query=user_query,
            context=context
        )
    elif intent == "ClauseRetrieval":
        prompt = clause_retrieval_prompt.format(
            user_query=user_query,
            context=context
        )
    elif intent == "ComparativeAnalysis":
        prompt = comparative_analysis_prompt.format(
            user_query=user_query,
            context=context
        )
    else:
        return {
            "intent": intent,
            "confidence": confidence,
            "response": "❌ Unable to identify a valid legal intent. Please rephrase your legal question."
        }


    full_prompt = (
        f"{formatted_history}\n\nCurrent Query: {user_query}\n\n"
        f"Context: {context}\n\nAnswer the query."
    )

    response = model.generate_content(full_prompt)
    answer = response.text

    session_history[user_id].append((user_query, answer))

    db = SessionLocal()
    chat = ChatHistory(
        user_id=user_id,
        user_query=user_query,
        assistant_response=answer
    )
    db.add(chat)
    db.commit()
    db.close()

    return {
        "intent": intent,
        "confidence": confidence,
        "response": answer
    }
