from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import aiohttp
import os, logging, datetime

# Constant slugs for country code id
SLUG_FARM = {}

# Initialize application 
app = FastAPI()

# Mount static directory as the root 
app.mount("/static", StaticFiles(directory="static"))

# Mount templates directory for Jinja rendering
templates = Jinja2Templates(directory="templates")

# Index entrypoint for website. 
@app.get("/")
async def index(request: Request):
    async with aiohttp.ClientSession() as session: 
        async with session.get("https://api.covid19api.com/summary") as resp:
            return templates.TemplateResponse("index.html", {"request": request, "summary" : await resp.json()})

# Get data by country code
@app.get("/country/{c_code}")
def test(request: Request, c_code: str = None):
    return {"country": c_code}
    