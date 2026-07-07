from fastapi import FastAPI , Path , HTTPException
import json

app = FastAPI()

def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data



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