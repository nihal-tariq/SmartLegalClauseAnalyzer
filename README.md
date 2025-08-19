⚖️ Smart Legal Clause Analyzer

RAG-based Legal AI System

A production-grade Legal AI Assistant that leverages LLMs, Retrieval-Augmented Generation (RAG), and multi-format document processing to:

Analyze legal documents

Classify user intent

Generate legally informed answers

🚀 Built with: LangChain, FastAPI, Groq (LLaMA3-70B), Gemini 2.5 Flash, Celery, HuggingFace, PostgreSQL, and Docker.
Demonstrates scalable architecture, modular design, and advanced LLM integrations.

🔗 Repository: GitLab – Smart Legal Clause Analyzer

⚡ Quick Start (Docker Setup)
# 1. Clone the Repository
git clone https://gitlab.com/nihaltariq66/Smart_Legal_Clause_Analyzez.git
cd Smart_Legal_Clause_Analyzez

# 2. Create a .env file and add your API keys + DB config
touch .env
# Add GOOGLE_API_KEY, GROQ_API_KEY, CHATLOG_DATABASE, etc.

# 3. Build and run containers
docker-compose up --build

# 4. (Subsequent Runs)
docker-compose up


📡 Services:

🧠 FastAPI → http://localhost:8007

🐘 PostgreSQL → localhost:5433

♻️ Redis → localhost:6380

📜 Project Summary

This system delivers a multi-stage intelligent legal assistant pipeline:

Document Uploads → PDF, Word, CSV

Parsing & Chunking → via LangChain loaders

Embeddings & Storage → HuggingFace Mini LLM + ChromaDB (per-user + central legal DB)

Query Classification →

Legal vs Non-Legal → Gemini 2.5 Flash

Intent Classification → BART MNLI (Definition, Clause Retrieval, Comparative Analysis)

Context Retrieval → Multi-query search from User DB + Main DB

Answer Generation → Gemini 2.5 Flash

Logging → Chat history stored in PostgreSQL, exportable as JSON

🧠 Architecture Overview
flowchart TD
    A[User Uploads PDF/Word/CSV] --> B[LangChain Document Loaders]
    B --> C[Chunk & Embed via HuggingFace Mini LLM]
    C --> D[User-specific ChromaDB Collection]
    C --> E[Main ChromaDB (Legal CSVs)]

    F[User Query] --> G[Gemini 2.5 Flash: Legal/Non-Legal]
    G -->|Yes| H[Intent Classifier: BART MNLI]
    H --> I[Context Retrieval: User + Main DB]
    I --> J[Gemini 2.5 Flash Generates Response]
    J --> K[Response Stored in PostgreSQL]
    K --> M[Retrieve via /chat_log & /download-chatlog]

    G -->|No| N[Return "Please enter a legal query"]

🔬 Key Components
📄 Document Ingestion

Formats: PDF, Word, CSV

Loaders: PyMuPDFLoader, Docx2txtLoader, CSVLoader

Stored in user-specific ChromaDB collections, linked via user_id

🧠 LLM & Retrieval Stack

Retriever → LLaMA3-70B (Groq) + ContextualCompressionRetriever + MultiQueryRetriever

Legal/Non-Legal Classifier → Gemini 2.5 Flash

Intent Classifier → BART-MNLI (zero-shot)

Responder → Gemini 2.5 Flash

Embedder → HuggingFace Mini-LLM

⚙️ Background Processing

Celery workers (task queue)

Redis backend

Handles asynchronous embedding & storage

🗃️ Data Storage

ChromaDB → Persistent vector DB (per-user + central legal knowledgebase)

PostgreSQL → File metadata + chat history (linked to user_id)

📦 Deployment-Ready (Dockerized)

✅ Containers:

FastAPI

Celery Worker

PostgreSQL

Redis

✅ Features:

.env driven config

Persistent volumes (DB + ChromaDB)

Scalable, restart-safe setup

🔮 Future Roadmap

🔐 OAuth2-based authentication (User roles: Lawyer, Client, Admin)

💬 Frontend with live chat + doc upload

📑 Advanced legal summarization & comparison tools

📊 Analytics dashboard for case trends & query insights