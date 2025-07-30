from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    user_query = Column(Text, nullable=False)
    assistant_response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Add __repr__ for better debugging
    def __repr__(self):
        return f"<ChatHistory(id={self.id}, user_id={self.user_id}, timestamp={self.timestamp})>"