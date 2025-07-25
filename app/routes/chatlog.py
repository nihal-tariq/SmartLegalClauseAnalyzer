import json
from io import BytesIO

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import ChatHistory


router = APIRouter()


def get_db():
    """
    Provides a database session and ensures it is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/chatlog/download/{user_id}")
def download_chat_history_file(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Download chat history for a given user as a JSON file.
    """
    chats = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.timestamp.asc())
        .all()
    )

    if not chats:
        return {"message": "No chat history found for this user."}

    log = [
        {
            "timestamp": str(chat.timestamp),
            "user_query": chat.user_query,
            "model_response": chat.assistant_response,
        }
        for chat in chats
    ]

    json_data = json.dumps({"user_id": user_id, "chatlog": log}, indent=2)
    buffer = BytesIO(json_data.encode("utf-8"))

    return StreamingResponse(
        buffer,
        media_type="application/json",
        headers={
            "Content-Disposition": f"attachment; filename=chatlog_{user_id}.json"
        },
    )


@router.get("/chatlog/view/{user_id}")
def view_chat_history(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Display chat history for a given user as formatted JSON in the browser.
    """
    chats = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.timestamp.asc())
        .all()
    )

    if not chats:
        return {"message": "No chat history found for this user."}

    log = [
        {
            "timestamp": str(chat.timestamp),
            "user_query": chat.user_query,
            "model_response": chat.assistant_response,
        }
        for chat in chats
    ]

    return JSONResponse(
        content={"user_id": user_id, "chatlog": log},
        media_type="application/json"
    )
