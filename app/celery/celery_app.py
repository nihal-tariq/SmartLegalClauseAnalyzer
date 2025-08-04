import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    "worker",
    broker=os.getenv("REDIS_BROKER_URL"),
    backend=os.getenv("REDIS_BROKER_URL")
)

celery_app.conf.task_routes = {
    "app.worker.process_and_embed_document": {"queue": "default"}
}
