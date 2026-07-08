from fastapi import FastAPI , Path , Query , HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
import json

app = FastAPI()


class patient(BaseModel):
    id : Annotated[str,Field(...,description = "Id of patient" ,examples =['P001'])]
    name : Annotated[str,Field(..., description="Name of patient")]
    city: Annotated[str,Field(..., description="City of patient")]
    age : Annotated[int,Field(...,gt = 0 , le = 120,description="Age of patient")]
    gender : Annotated[Literal["male","female","other"],Field(...,description="Gender of patient")]
    height : Annotated[float,Field(...,gt = 0,description="Height of patient in meters")]
    weight : Annotated[float,Field(...,gt = 0,description="Weight of patient in kilograms")]

    @computed_field
    @property
    def bmi(self)->float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"


class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]




def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data


def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)


@app.get("/")
def hello():
    return {"message" : "Patients management system"}
    

@app.get("/about")
def about():
    return {"message" : "A fully functional patients management system"}



@app.get("/view")
def view():
    data = load_data()
    return data


@app.get("/patients/{patients_id}")
def view_patients(patients_id : str = Path(...,description = "Id of patient" ,example = "P001")):
    data = load_data()

    if patients_id in data:
        return data[patients_id]
    raise HTTPException(status_code = 404 , detail='Patient not found')


@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description= 'sort on the basis of height, weight, or bmi'), order_by: str = Query('asc',description= 'sort in asc or desc order')):

    valid_fields = ['height','weight','bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code= 400, detail=f'invalid field select from{valid_fields}')
    
    if order_by not in ['asc','desc']:
        raise HTTPException(status_code= 400 , detail='invalid field select from asc and desc')
    
    data = load_data()

    reverse = True if order_by == 'desc' else False 

    sorted_data = sorted(data.values(), key=lambda x:x.get(sort_by, 0), reverse=reverse)

    return sorted_data



@app.post("/create")
def create_patient(patient : patient):
    
    # load existing data 
    data = load_data()

    # check if patient already exists 
    if patient.id in data:
        raise HTTPException(status_code = 400 , detail='Patient already exists')
    
    # new patient add to database
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save data in json file
    save_data(data)

    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})



@app.put('/update/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    #existing_patient_info -> pydantic object -> updated bmi + verdict
    existing_patient_info['id'] = patient_id
    patient_pydandic_obj = patient(**existing_patient_info)
    
    #-> pydantic object -> dict
    existing_patient_info = patient_pydandic_obj.model_dump(exclude='id')

    # add this dict to data
    data[patient_id] = existing_patient_info

    # save data
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient updated'})
