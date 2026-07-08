from pydantic import BaseModel
from typing import List , Dict

class patient(BaseModel):
    name : str
    age : int 
    weight : float
    married : bool
    allergies: List[str]
    contact_details : Dict[str , str]


patient_info = {
    "name" : "Ananya",
    "age" : 28,
    "weight" : 90.0,
    "married" : False,
    "allergies" : ["peanuts", "eggs", "dust"],
    "contact_details" : {"email" : "ananyaverma@.com", "phone" : "9876543210"}
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