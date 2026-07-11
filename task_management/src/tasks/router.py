from fastapi import APIRouter, Depends
from src.tasks import controller
from src.tasks.dtos import Tastschema
from src.utils.db import get_db

task_router = APIRouter(prefix="/tasks")

@task_router.post("/create")
def create_task(body: Tastschema, db = Depends(get_db)):
    return controller.create_task(body, db)


@task_router.get("/all_tasks")
def get_all_tasks(db = Depends(get_db)):
    return controller.get_tasks(db)


@task_router.get("/task_by_id/{task_id}")
def get_one(task_id:int,db = Depends(get_db)):
    return controller.get_one_task(task_id, db)