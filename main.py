from fastapi import FastAPI , Path , Query , HTTPException
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