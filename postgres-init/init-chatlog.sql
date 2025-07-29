CREATE DATABASE chatlog;

\c chatlog;

CREATE TABLE chat_history (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255),
    user_query TEXT,
    assistant_response TEXT,
    timestamp TIMESTAMP
);
