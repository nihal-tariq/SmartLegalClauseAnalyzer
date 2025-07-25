import os
import re

import chromadb
from chromadb.errors import NotFoundError

from tqdm import tqdm

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    Docx2txtLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def clean_text(text: str) -> str:
    """
    Clean and normalize input text by removing extra symbols and spaces.
    """
    text = re.sub(r"[^\w\s.,;:?!-]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def embed_single_file_into_chroma(
    file_path: str,
    user_id: str,
    persist_dir: str,
    collection_prefix: str = "user_",
    batch_size: int = 32
) -> dict:
    """
    Embed a single file into ChromaDB, creating/updating a user-specific
    collection.

    Args:
        file_path (str): Path to the uploaded file.
        user_id (str): Unique identifier for the user.
        persist_dir (str): Path to persist ChromaDB.
        collection_prefix (str): Prefix for collection names.
        batch_size (int): Embedding batch size.

    Returns:
        dict: Metadata about the collection and operation.
    """
    ext = os.path.splitext(file_path)[1].lower()

    try:
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif ext == ".csv":
            loader = CSVLoader(file_path)
        elif ext == ".txt":
            loader = TextLoader(file_path)
        elif ext in (".docx", ".doc"):
            loader = Docx2txtLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path}")

        docs = loader.load()

    except Exception as e:
        raise RuntimeError(f"Error loading file: {e}")

    if not docs:
        raise ValueError(f"No content loaded from: {file_path}")

    for doc in docs:
        doc.page_content = clean_text(doc.page_content)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(docs)

    if not chunks:
        raise ValueError(f"No usable chunks created from: {file_path}")

    print(f"✅ Extracted {len(chunks)} chunks.")

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    client = chromadb.PersistentClient(path=persist_dir)
    collection_name = f"{collection_prefix}{user_id}"

    try:
        client.get_collection(collection_name)
        collection_exists = True
    except NotFoundError:
        collection_exists = False

    if collection_exists:
        vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=embedding_model,
            client=client,
            persist_directory=persist_dir
        )
        print(f"🔄 Updating collection: {collection_name}")
    else:
        vectorstore = Chroma.from_documents(
            documents=[],
            embedding=embedding_model,
            collection_name=collection_name,
            client=client,
            persist_directory=persist_dir
        )
        print(f"🚀 Created new collection: {collection_name}")

    print(f"📦 Embedding in batches of {batch_size} ...")
    for i in tqdm(
        range(0, len(chunks), batch_size),
        desc="Embedding"
    ):
        batch = chunks[i:i + batch_size]
        vectorstore.add_documents(batch)

    return {
        "collection_name": collection_name,
        "operation": "updated" if collection_exists else "created",
        "chunks_embedded": len(chunks),
        "file_processed": os.path.basename(file_path)
    }
