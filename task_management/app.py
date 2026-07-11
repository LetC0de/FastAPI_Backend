from fastapi import FastAPI
from src.utils.db import base,engine
from src.tasks.models import TaskModel

base.metadata.create_all(engine)

app = FastAPI(title="Task Management App")