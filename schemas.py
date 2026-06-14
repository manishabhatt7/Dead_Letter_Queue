from pydantic import BaseModel
from uuid import uuid4


class TaskMessage(BaseModel):
    event_id: str
    task_type: str
    payload: dict
    retry_count: int = 0



def create_message(task_type: str, payload: dict):
    return TaskMessage(
        event_id=str(uuid4()),
        task_type=task_type,
        payload=payload,
    )