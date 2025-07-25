from fastapi import FastAPI


from app.routes import upload
from app.routes import query
from app.routes import status
from app.routes import chatlog


app = FastAPI(title="Legal Document Chatbot")


app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(status.router, prefix="/status", tags=["Status"])
app.include_router(query.router, prefix="/query", tags=["Query"])
app.include_router(chatlog.router, prefix="/chat_log", tags=["ChatLog"])
