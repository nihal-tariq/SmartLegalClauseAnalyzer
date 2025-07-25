import os
from dotenv import load_dotenv
from typing import Optional, List, Any

from langchain_chroma import Chroma
from langchain.retrievers import ContextualCompressionRetriever, MultiQueryRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.llms.base import LLM
from groq import Groq

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_KEY_API")


# ---------------------- Custom LLM Wrapper for Groq ----------------------
class GroqLLM(LLM):
    model: str = "llama3-70b-8192"
    temperature: float = 0.7
    max_completion_tokens: int = 1024
    client: Any = Groq(api_key=GROQ_API_KEY)

    @property
    def _llm_type(self) -> str:
        return "groq-custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_completion_tokens,
            top_p=1,
            stream=False,
            stop=stop,
        )
        return response.choices[0].message.content


# ---------------------- Embedding Model ----------------------
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


# ---------------------- Retriever Builder ----------------------
def build_contextual_compression_retriever(user_id: str, persist_dir: str = "app/document_embedding/legal_chroma_db"):
    """
    Combines base and user-specific Chroma collections with multi-query and compression logic.
    """
    base_vectorstore = Chroma(
        persist_directory=persist_dir,
        embedding_function=embedding,
        collection_name="legal_index"
    )

    user_collection_name = f"user_{user_id}"
    user_vectorstore = Chroma(
        persist_directory=persist_dir,
        embedding_function=embedding,
        collection_name=user_collection_name
    )

    from langchain.retrievers import EnsembleRetriever

    base_retriever = base_vectorstore.as_retriever(search_kwargs={"k": 5})
    user_retriever = user_vectorstore.as_retriever(search_kwargs={"k": 5})

    combined_retriever = EnsembleRetriever(
        retrievers=[base_retriever, user_retriever],
        weights=[0.5, 0.5]
    )

    multi_query_retriever = MultiQueryRetriever.from_llm(
        retriever=combined_retriever,
        llm=GroqLLM()
    )

    compressor = LLMChainExtractor.from_llm(GroqLLM())

    return ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=multi_query_retriever
    )


# ---------------------- Retrieve Compressed Context ----------------------
def get_compressed_context(user_query: str, user_id: str) -> str:
    """
    Retrieves compressed and relevant chunks from both global and user-specific collections.
    """
    compression_retriever = build_contextual_compression_retriever(user_id=user_id)
    compressed_documents = compression_retriever.invoke(user_query)
    return "\n\n".join([doc.page_content for doc in compressed_documents])
