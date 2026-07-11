from fastapi import FastAPI
from src.utils.db import base,engine
from src.tasks.router import task_router


base.metadata.create_all(engine)

app = FastAPI(title="Task Management App")
app.include_router(task_router)