from src.tasks.dtos import Tastschema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from fastapi import HTTPException

def create_task(body : Tastschema,db:Session):
    data = body.model_dump()

    new_task = TaskModel(title = data['title'],
                          description = data['description'],
                            is_completed = data['is_completed'])
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {"message": "Task created successfully", "data": new_task}



def get_tasks(db:Session):
    tasks = db.query(TaskModel).all()
    return {"status":"All tasks","data":tasks}



def get_one_task(task_id:int,db:Session):
    task = db.query(TaskModel).get(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"status":"Task fetched successfully","data":task}


def update_task(task_id:int,body:Tastschema,db:Session):

    task = db.query(TaskModel).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    body = body.model_dump()
    for field, value in body.items():
        setattr(task, field, value)

    db.add(task)
    db.commit()
    db.refresh(task)
    
    return {"status":"Task updated successfully","data":task}



def delete_task(task_id:int,db:Session):
    task = db.query(TaskModel).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    
    return {"status":"Task deleted successfully"}