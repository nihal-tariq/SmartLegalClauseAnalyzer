from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ChatHistory(Base):
    """
    SQLAlchemy model for storing chat history between a user and the assistant.

    Attributes:
        id (int): Primary key for the chat record.
        user_id (str): Identifier for the user (can be used to track user sessions).
        user_query (str): The query or message sent by the user.
        assistant_response (str): The assistant's response to the user query.
        timestamp (datetime): The UTC time when the interaction occurred. Defaults to current time.
    """
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    user_query = Column(Text, nullable=False)
    assistant_response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<ChatHistory(id={self.id}, user_id={self.user_id}, timestamp={self.timestamp})>"
