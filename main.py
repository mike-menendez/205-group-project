from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os, logging, datetime, sys, aiohttp, numpy, seaborn, sklearn

# Constant slugs for country code id
SLUG_FARM = {}

# Initialize application 
app = FastAPI()
# Mount templates directory for Jinja rendering
templates = Jinja2Templates(directory="templates")

# Fetches data from the remote api, as the api only supports GET, we're taking a shortcut
async def data_fetch(loc: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(loc) as resp:
            return await resp.json()

# Initalize all the slugs needed for getting data from country
@app.on_event("startup")
async def startup_event():
    for x in await data_fetch("https://api.covid19api.com/countries"):
        SLUG_FARM[x["ISO2"]] = x["Slug"]
    # Mount static directory as the root 
    app.mount("/static", StaticFiles(directory="static"))

# Index entrypoint for website. 
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html",
    {"request": request,"summary" : await data_fetch("https://api.covid19api.com/summary")})

# Get data by country code
@app.get("/country/{c_code}")
async def test(request: Request, c_code: str = None):
    if not c_code or c_code.upper() not in SLUG_FARM.keys():
        return templates.TemplateResponse("404.html", {"request": request})
    dead, confirm, recover, active = 0, 0, 0, 0
    for x in list(await data_fetch(f"https://api.covid19api.com/live/country/{c_code}/status/confirmed")):
        if "2020-04-23" in x['Date']:
            dead = dead + x['Deaths']
            confirm = confirm + x['Confirmed']
            recover = recover + x['Recovered']
            active = active + x['Active']
    return templates.TemplateResponse("country.html",
        {"request": request, "data" : {"dead": dead, "confirmed": confirm, "active": active, "recovered": recover}})

# 404 error handling
@app.get("/.*")
async def err_render(request: Request):
    return templates.TemplateResponse("404.html", {"request": request})
    