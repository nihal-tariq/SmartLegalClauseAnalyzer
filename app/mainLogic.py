import os
import gc
from collections import defaultdict


from dotenv import load_dotenv
from google import generativeai as genai


from app.utility.intent_classification import classify_intent
from app.utility.file_handling import embed_single_file_into_chroma
from app.utility.prompts_module import (
    definition_prompt,
    clause_retrieval_prompt,
    comparative_analysis_prompt
)
from app.utility.retriever import get_compressed_context


load_dotenv()


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY(gen_ai)")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="gemini-2.5-flash")


session_history = defaultdict(list)
MAX_HISTORY = 3


file_path = input("Enter document path (PDF/Word/CSV): ").strip()
user_id = input("Enter user ID (e.g., user123): ").strip()


if not os.path.exists(file_path):
    print("❌ File does not exist.")
    exit()


embed_single_file_into_chroma(
    file_path,
    user_id,
    "app/document_embedding/legal_chroma_db"
)


while True:
    user_query = input(
        "\nEnter your legal question (or type 'EXIT' to end): "
    ).strip()

    if user_query.upper() == "EXIT":
        print("Session ended.")
        break

    if not user_query:
        print("⚠️ Please enter a valid query.")
        continue

    intent, confidence = classify_intent(user_query)
    print(f"\nIntent: {intent} (Confidence: {confidence:.2f})")

    context = get_compressed_context(user_query, user_id)
    history = session_history[user_id][-MAX_HISTORY:]

    formatted_history = "\n".join([
        f"User: {q}\nAssistant: {r}" for q, r in history
    ])

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
        prompt = f"Query: {user_query}\nContext: {context}"

    full_prompt = (
        f"{formatted_history}\n\n"
        f"Current Query: {user_query}\n\n"
        f"Context: {context}\n\n"
        f"Answer the query."
    )

    response = model.generate_content(full_prompt)

    print("\nGemini Response:\n", response.text)

    session_history[user_id].append((user_query, response.text))

    gc.collect()
