from fastapi import APIRouter, Form

from app.services.chat_engine import handle_chat_query


router = APIRouter()


@router.post("/")
def query_legal_bot(
    user_id: str = Form(...),
    user_query: str = Form(...)
):
    """
    Handle POST request to query the legal bot.

    Parameters:
    - user_id (str): Unique identifier for the user.
    - user_query (str): User's legal query.

    Returns:
    - JSON response from the chat engine.
    """
    result = handle_chat_query(user_id, user_query)
    return result
