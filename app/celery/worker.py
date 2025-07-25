from app.celery.celery_app import celery_app
from app.utility.embedder import embed_single_file_into_chroma
import traceback
import logging
import os
import json

# Optional: setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


@celery_app.task(name="process_and_embed_document")
def process_and_embed_document(file_path: str, user_id: str):
    """
    Celery task to embed a single file into Chroma vector store for a specific user.
    Logs status and writes a `.status.json` to track completion.
    """
    status_dir = "../status_logs"
    os.makedirs(status_dir, exist_ok=True)
    status_path = os.path.join(status_dir, f"{user_id}.status.json")

    try:
        logging.info(f"[{user_id}] Starting embedding task for file: {file_path}")
        result = embed_single_file_into_chroma(
            file_path=file_path,
            user_id=user_id,
            persist_dir="app/document_embedding/legal_chroma_db"
        )

        # Write success status
        with open(status_path, "w") as f:
            json.dump({"status": "completed", "details": result}, f, indent=2)

        logging.info(f"[{user_id}] Embedding completed: {result['chunks']} chunks embedded")
        return result

    except Exception as e:
        logging.error(f"[{user_id}] Embedding failed: {str(e)}")
        traceback.print_exc()

        # Write failure status
        with open(status_path, "w") as f:
            json.dump({
                "status": "error",
                "error": str(e),
                "traceback": traceback.format_exc()
            }, f, indent=2)

        return {"status": "error", "error": str(e)}
