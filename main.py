from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os, logging, datetime, sys, aiohttp

# Constant slugs for country code id
SLUG_FARM = {}

# Initialize application 
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.covid19api.com/countries") as resp:
            for x in await resp.json():
                SLUG_FARM[x["ISO2"]] = x["Slug"]
    # print(SLUG_FARM, file=sys.stderr)

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
async def test(request: Request, c_code: str = None):
    if c_code == None:
        return templates.TemplateResponse("404.html", {"request": request})
    return templates.TemplateResponse("country.html", {"request": request, "data" : SLUG_FARM[c_code.upper()]})
    