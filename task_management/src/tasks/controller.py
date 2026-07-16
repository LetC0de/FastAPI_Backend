from src.tasks.dtos import Tastschema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from src.user.models import UserModel
from fastapi import HTTPException

def create_task(body : Tastschema,db:Session,user:UserModel):
    data = body.model_dump()

    new_task = TaskModel(title = data['title'],
                          description = data['description'],
                            is_completed = data['is_completed'],
                            user_id = user.id)
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task



def get_tasks(db:Session,user:UserModel):
    tasks = db.query(TaskModel).filter(TaskModel.user_id == user.id).all()
    return tasks



def get_one_task(task_id:int,db:Session):
    task = db.query(TaskModel).get(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task


def update_task(task_id:int,body:Tastschema,db:Session,user:UserModel):

    task: TaskModel = db.query(TaskModel).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.user_id != user.id:
        raise HTTPException(status_code=401, detail="You are not authorized to update this task")
    
    body = body.model_dump()
    for field, value in body.items():
        setattr(task, field, value)

    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task



def delete_task(task_id:int,db:Session):
    task = db.query(TaskModel).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    
    return None