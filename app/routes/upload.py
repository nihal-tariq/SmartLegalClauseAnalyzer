import os
import shutil

from fastapi import APIRouter, UploadFile, File, Form

from app.celery.worker import process_and_embed_document


router = APIRouter()
UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/")
async def upload_document(
    user_id: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Upload a document and trigger a Celery task for processing and embedding.

    Parameters:
    - user_id (str): Unique identifier for the user.
    - file (UploadFile): The document to upload and process.

    Returns:
    - A JSON response with task info and confirmation.
    """
    file_path = os.path.join(UPLOAD_DIR, f"{user_id}_{file.filename}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    task = process_and_embed_document.delay(
        file_path=file_path,
        user_id=user_id
    )

    return {
        "message": f"File '{file.filename}' received. Processing started.",
        "user_id": user_id,
        "task_id": task.id,
    }
