from src.tasks.dtos import Tastschema

def create_task(body : Tastschema):
    print(body.model_dump())
    return {"message": "Task created successfully"}