from fastapi import APIRouter

from celery.result import AsyncResult

from app.celery.celery_app import celery_app


router = APIRouter()


@router.get("/{task_id}")
def get_task_status(task_id: str):
    """
    Retrieve the status and result of a Celery task by task ID.

    Parameters:
    - task_id (str): The ID of the task to check.

    Returns:
    - Dictionary containing task status, readiness, success, and result.
    """
    result = AsyncResult(task_id, app=celery_app)

    return {
        "task_id": task_id,
        "status": result.status,
        "ready": result.ready(),
        "successful": result.successful(),
        "result": str(result.result) if result.ready() else None,
    }
