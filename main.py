from fastapi import FastAPI
import os, logging, datetime

app = FastAPI()

# Main entrypoint for api. 
@app.get("/")
def index():
    pass