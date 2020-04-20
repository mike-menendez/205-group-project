from fastapi import FastAPI
import os, logging, datetime

app = FastAPI()

# Main entrypoint for api. 
@app.get("/")
def index():
    return {"it": "works"}

# Get data by country code
@app.get("/country/{c_code}")
def test(c_code: str = None):
    return {"country": c_code}
