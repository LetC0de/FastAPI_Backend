from pydantic import BaseModel, EmailStr , AnyUrl , Field
from typing import List , Dict , Optional

class patient(BaseModel):
    name : str = Field(max_length = 50)
    age : int = Field(gt = 0 , le = 120)
    email : EmailStr
    weight : float = Field(gt = 0)
    married : bool = False
    allergies: Optional[List[str]] = Field(default = None,max_length = 5)
    contact_details : Dict[str , str]
    url : AnyUrl


patient_info = {
    "name" : "Ananya",
    "age" : 28,
    "email" : "ananyaverma@gmail.com",
    "weight" : 90.0,
    "married" : False,
    "allergies" : ["peanuts", "eggs", "dust"],
    "contact_details" : {"phone" : "9876543210"},
    "url" : "https://google.com"
}

patient1 = patient(**patient_info)

def insert_patient_data(patient : patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print("inserted")


insert_patient_data(patient1)