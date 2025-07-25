import os

import chromadb
from chromadb.errors import NotFoundError

from langchain_community.document_loaders import (
    PyPDFLoader,
    CSVLoader,
    TextLoader,
    Docx2txtLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from app.utils import clean_text, batch_generator


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={
        "device": "cpu",
        "trust_remote_code": False
    },
    encode_kwargs={
        "batch_size": 5
    }
)


LOADER_MAP = {
    ".pdf": PyPDFLoader,
    ".csv": CSVLoader,
    ".txt": TextLoader,
    ".doc": Docx2txtLoader,
    ".docx": Docx2txtLoader
}


def load_and_clean_documents(file_path: str):
    """
    Load a document and clean its content based on file extension.
    """
    ext = os.path.splitext(file_path)[1].lower()
    loader_cls = LOADER_MAP.get(ext)

    if not loader_cls:
        raise ValueError(f"Unsupported file type: {file_path}")

    docs = loader_cls(file_path).load()

    for doc in docs:
        doc.page_content = clean_text(doc.page_content)

    return docs


def split_documents(docs, chunk_size=500, chunk_overlap=100):
    """
    Split documents into chunks using a recursive text splitter.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_documents(docs)


def get_or_create_vectorstore(user_id: str, persist_dir: str):
    """
    Retrieve or create a Chroma vectorstore collection for a given user.
    """
    collection_name = f"user_{user_id}"
    client = chromadb.PersistentClient(path=persist_dir)

    print(f"[INFO] Checking or creating collection for {collection_name}")

    try:
        client.get_collection(collection_name)
    except NotFoundError:
        client.create_collection(collection_name)

    return Chroma(
        collection_name=collection_name,
        embedding_function=embedding_model,
        client=client,
        persist_directory=persist_dir
    )


def embed_single_file_into_chroma(
    file_path: str,
    user_id: str,
    persist_dir: str,
    batch_size: int = 32
):
    """
    Load, clean, split, embed and store a document into Chroma vectorstore.
    """
    try:
        print(f"[INFO] Loading and cleaning document: {file_path}")
        docs = load_and_clean_documents(file_path)
        print(f"[INFO] Loaded and cleaned {len(docs)} document(s)")

        chunks = split_documents(docs)
        print(f"[INFO] Document split into {len(chunks)} chunks")

        vectorstore = get_or_create_vectorstore(user_id, persist_dir)
        print(f"[INFO] Vectorstore for user_{user_id} ready")

        for i, batch in enumerate(batch_generator(chunks, batch_size)):
            total_batches = (len(chunks) + batch_size - 1) // batch_size
            print(f"[INFO] Embedding batch {i + 1}/{total_batches}")
            vectorstore.add_documents(batch)

        print("[INFO] Embedding complete, saving to collection")

        return {
            "collection_name": f"user_{user_id}",
            "chunks": len(chunks),
            "filename": os.path.basename(file_path)
        }

    except Exception as e:
        print(f"[ERROR] Embedding failed: {e}")
        raise RuntimeError(
            f"Failed to embed document '{file_path}': {str(e)}"
        ) from e
