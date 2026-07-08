from pydantic import BaseModel

class patient(BaseModel):
    name : str
    age : int 


patient_info = {
    "name" : "Ananya",
    "age" : 28
}

patient1 = patient(**patient_info)

def insert_patient_data(patient : patient):
    print(patient.name)
    print(patient.age)
    print("inserted")


insert_patient_data(patient1)