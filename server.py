from fastapi import FastAPI
from main import Crawler as Cr

app = FastAPI()

test = 3
crawle = Cr()

@app.get("/")

async def read_root():
    return crawle.Start(test,True) 

