from app.utility.file_handling import embed_single_file_into_chroma


def save_and_embed_file(file_path: str, user_id: str):
    """
    Save and embed a single file into the Chroma database.

    Parameters:
    - file_path (str): Path to the document file.
    - user_id (str): Unique identifier for the user.
    """
    embed_single_file_into_chroma(
        file_path=file_path,
        user_id=user_id,
        persist_dir="app/document_embedding/legal_chroma_db"
    )
