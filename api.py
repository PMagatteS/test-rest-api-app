from fastapi import FastAPI
import uvicorn 
import json

with open("C:/Users/lenovo/Desktop/bullet.json") as f:
        dict = json.load(f)

app = FastAPI()

@app.get('/')
async def yo():
    return dict

uvicorn.run(app, port=5555)