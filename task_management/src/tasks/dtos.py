from pydantic import BaseModel

class Tastschema(BaseModel):
    title : str
    description : str
    is_completed : bool = False