⚖️ Smart Legal Clause Analyzer
A production-ready, end-to-end RAG-based legal assistant built using LLMs, LangChain, FastAPI, Celery, and Docker. This intelligent system helps users analyze legal documents by retrieving relevant clauses and generating responses based on legal intent using retrieval-augmented generation (RAG).

🚀 Project Highlights
Retrieval-Augmented Generation (RAG) pipeline using ChromaDB and LangChain retrievers.

User-specific document storage and retrieval with ChromaDB collections.

High-performance embedding with HuggingFace mini-LLM and efficient batch processing for large-scale datasets.

Zero-shot intent classification to distinguish between queries: DefinitionQuery, ClauseRetrieval, ComparativeAnalysis.

Responses powered by Gemini 2.5 Flash model via Google Generative AI API.

Query context compression using LangChain's CompressedRetriever with Groq’s LLaMA3-70B-8192 model.

Background processing of embeddings using Celery workers.

Seamless deployment with Docker and PostgreSQL as the database backend.

Full chat history storage and downloadable JSON logs via FastAPI endpoints.

Robust error handling, memory management, and clean modular architecture.

🧠 Workflow Overview

    A[User Uploads Document with UserID] --> B[LangChain CSV Loader Loads File]
    B --> C[Document Chunked and Embedded using HuggingFace mini-LLM]
    C --> D[User-Specific ChromaDB Collection Created]
    A -->|Parallel| F[Celery Worker Handles Embedding & Memory Efficiently]
    G[User Submits Query with ID] --> H[Intent Classification (BART MNLI)]
    H -->|If Legal| I[CompressedRetriever + MultiQuery Retriever (LLaMA3-70B)]
    I --> J[Context + History Sent to Gemini 2.5 Flash via Prompt Template]
    J --> K[Model Generates Legal Answer]
    K --> L[Chat Stored in PostgreSQL]
    L --> M[Chat History View / Download via FastAPI JSON]
    H -->|If Non-Legal| N[Response: "Please provide a legal query"]

🧰 Tech Stack
Backend Framework:
Built using FastAPI, a modern, high-performance Python web framework for building APIs with automatic documentation.

Asynchronous Task Queue:
Used Celery for handling heavy background tasks like document embedding and processing, ensuring smooth performance.

Vector Store:
ChromaDB is used to store and retrieve document embeddings efficiently, with separate collections for main and user-specific datasets.

Embedding Model:
Employed a custom-loaded HuggingFace Mini-LLM to generate dense vector representations of text chunks.

Intent Classification:
Used facebook/bart-large-mnli for zero-shot classification of user queries into:

DefinitionQuery

ClauseRetrieval

ComparativeAnalysis

LLM for Compression (Retriever):
Implemented LLaMA3-70B-8192 via Groq API for compressing and retrieving the most relevant chunks from both datasets using LangChain’s CompressedRetriever.

Final Responder LLM:
Integrated Gemini 2.5 Flash through Google Generative AI API to generate context-aware, prompt-engineered legal responses.

Document Loading:
Utilized LangChain CSV Loader to ingest large legal datasets and user-uploaded documents.

RAG Framework:
Built on top of LangChain, enabling Retrieval-Augmented Generation with flexible chains, prompts, and retrievers.

Database:
PostgreSQL is used for storing file metadata and user chat history in a structured and query-efficient manner.

Containerization:
The entire application is fully Dockerized, allowing seamless deployment and scaling across environments.

Environment Management:
Managed sensitive keys and configurations via .env files, loaded securely using the python-dotenv library.

🧩 Core Functionalities
1. 📄 Document Upload
A user uploads a document along with a user ID.

The file is chunked, embedded using HuggingFace mini-LLM, and stored in a user-specific ChromaDB collection.

All metadata is stored in PostgreSQL.

Background processing is handled by Celery with optimized memory handling for large datasets.

2. 🧠 Query + Classification
User sends a query with their ID.

A zero-shot classifier determines if the query is legal or non-legal.

If non-legal: A polite rejection message is returned.

If legal: The query is routed based on intent classification:

DefinitionQuery

ClauseRetrieval

ComparativeAnalysis

3. 🔍 Contextual Retrieval + Generation
Relevant context is retrieved from:

The main legal dataset.

The user-specific uploaded dataset.

A CompressedRetriever is used (via LLaMA3-70B on Groq).

The final prompt includes:

Retrieved context

System instructions

Previous chat history

Gemini 2.5 Flash generates the final response.

4. 💬 Chat Logging
Every interaction (query + response) is stored in PostgreSQL.

A FastAPI endpoint serves chat logs in JSON format.

Logs are also downloadable.

🧪 Models Used
Model	Purpose	Source
HuggingFace mini-LLM	Embeddings	HuggingFace Transformers
facebook/bart-large-mnli	Zero-shot intent classification	HuggingFace
llama3-70b-8192	Context compression for retrieval	Groq API
gemini-1.5-flash	Response generation	Google GenAI API

🧠 What I Learned
Through building this project, I learned and implemented:

Advanced LangChain RAG architecture with custom retrievers and prompt engineering.

Efficient document chunking, batching, and memory handling for massive datasets.

Hands-on experience with HuggingFace transformers, embeddings, and vector stores.

Working with multiple LLMs via API (Groq, Google GenAI).

Backend architecture using FastAPI, REST APIs, and modular endpoints.

Task distribution using Celery, including setup and worker scaling.

Full integration with PostgreSQL for metadata and chat log persistence.

Deployment-ready Dockerization for the entire backend.

Proper error handling, structured logs, and performance optimization.

🐳 Deployment with Docker
1. Clone the Repo

git clone https://gitlab.com/nihaltariq66/Smart_Legal_Clause_Analyzez
cd legal-clause-analyzer

2. Set up Environment Variables
Create a .env file:

GOOGLE_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
DATABASE_URL=postgresql://user:pass@host/db

3. Build and Run Docker Containers

docker-compose up --build
🧪 API Endpoints
Method	Endpoint	Description
POST	/upload/	Upload document and embed (user ID + file)
POST	/status/	Give status of document upload  (Task ID)
POST	/query/	Submit a legal query with user ID
GET	/chatlogs/{user_id}	View full chat logs in JSON
GET	/download-chatlog/{user_id}	Download chat logs as .json

📌 Future Improvements
Add user authentication

Frontend UI for document upload and query
