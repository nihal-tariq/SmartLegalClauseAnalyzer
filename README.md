⚖️ Smart Legal Clause Analyzer (RAG-based Legal AI System)
A production-grade Legal AI Assistant that leverages LLMs, Retrieval-Augmented Generation (RAG), and multi-format document processing to analyze legal documents, classify user intent, and generate legally informed answers.
Built using LangChain, FastAPI, Groq (LLaMA3-70B), Gemini 2.5 Flash, Celery, HuggingFace, PostgreSQL, and Docker, this system demonstrates scalable architecture, modular design, and advanced LLM integrations.

🔗 GitLab Repository: https://gitlab.com/nihaltariq66/Smart_Legal_Clause_Analyzez.git


Quick Start (Docker Setup)

# 1. Clone the Repository
git clone https://gitlab.com/nihaltariq66/Smart_Legal_Clause_Analyzez.git
cd Smart_Legal_Clause_Analyzez

# 2. Create a .env file and add your API keys and DB config
touch .env
# Add GOOGLE_API_KEY, GROQ_API_KEY, CHATLOG_DATABASE, etc.

# 3. Build and run the containers
docker-compose up --build

# 4. (Subsequent Runs)
docker-compose up

🧠 FastAPI runs on http://localhost:8007

🐘 PostgreSQL on port 5433

♻️ Redis on port 6380

 Project Summary
This project delivers a multi-stage intelligent legal assistant pipeline:

User uploads documents (PDF, Word, or CSV)

Documents are parsed using LangChain loaders

Text is chunked & embedded with a HuggingFace Mini LLM

User-specific ChromaDB collections are created alongside a main collection preloaded with hundreds of legal CSVs

Queries are routed through a robust classification pipeline:

Legal vs Non-Legal detection via Gemini 2.5 Flash

Zero-shot intent classification using BART MNLI (Definition, Clause Retrieval, Comparative Analysis)

Context is retrieved from both user and main DB via ContextualCompressionRetriever + MultiQueryRetriever

Final response is generated using Gemini 2.5 Flash

All chat history is stored in PostgreSQL and can be retrieved/downloaded as JSON

🧠 Architecture Overview

flowchart TD
    A[User Uploads PDF/Word/CSV] --> B[LangChain Document Loaders]
    B --> C[Text Chunked + Embedded via HuggingFace Mini LLM]
    C --> D[ChromaDB Collection Created for User]
    C --> E[Main ChromaDB Indexed with Hundreds of Legal CSVs]

    F[User Query] --> G[Gemini 2.5 Flash: Is Legal?]
    G -->|Yes| H[Zero-Shot Intent Classifier (BART MNLI)]
    H --> I[Retrieve Context: User + Main DB (via LLaMA3-70B on Groq)]
    I --> J[Context Sent to Gemini 2.5 Flash]
    J --> K[Response Generated]
    K --> L[Chat History Stored in PostgreSQL]
    L --> M[Available via /chat_log and /download-chatlog]

    G -->|No| N[Return Message: “Please enter a legal query”]

🔬 Key Components
📄 Document Ingestion
Supports PDF, Word, and CSV uploads using LangChain loaders (PyMuPDFLoader, Docx2txtLoader, CSVLoader).
Documents are chunked, embedded, and stored in user-specific ChromaDB collections, all linked to a user_id.

🧠 LLM & Retrieval Stack
Retriever: LLaMA3-70B-8192 via Groq with ContextualCompressionRetriever + MultiQueryRetriever

Legal/Non-Legal Classifier: Gemini 2.5 Flash (Google GenAI API)

Intent Classifier: facebook/bart-large-mnli with zero-shot templates

Responder: Gemini 2.5 Flash for prompt-based legal answers

Embedder: HuggingFace Mini-LLM for generating dense vector embeddings

🧩 FastAPI Endpoints

⚙️ Background Task Management
All embedding and storage tasks run via Celery workers, backed by Redis.
Optimized for low memory usage and large document handling.

🗃️ Data Storage
ChromaDB: Local persistent vector store with per-user collections and a central legal knowledgebase created from hundreds of CSVs.

PostgreSQL: Stores file metadata and logs all chat history linked to user_id for retrieval or audit.

Deployment-Ready Docker Setup
Containerized with:

FastAPI

Celery Worker

PostgreSQL

Redis

Environment-managed via .env

All volumes and collections persist across reboots

 Future Plans
 OAuth2-based user authentication

 Frontend with live chat + document upload