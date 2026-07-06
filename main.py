from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message" : "Patients management system"}
    

@app.get("/about")
def about():
    return {"message" : "A fully functional patients management system"}