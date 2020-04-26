from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os, logging, datetime, sys, aiohttp, numpy as np, seaborn as sn, sklearn as sk, pandas as pd

# Constant slugs for country code id
SLUG_FARM = {}

# Initialize application 
app = FastAPI()
# Mount templates directory for Jinja rendering
templates = Jinja2Templates(directory="templates")
# Mount static directory as the root 
# app.mount("/static", StaticFiles(directory="static"))

# Aux Functions
# Fetches data from the remote api, as the api only supports GET, we're taking a shortcut
async def data_fetch(loc: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(loc) as resp:
            return await resp.json()

# These are compute intensive tasks, would be good to either do this in the background
# AOT, or we just run them once every 15 mins and the first access takes a hit with
# subsequent accesses being fast for the next 15 mins with: time.ctime(os.path.getmtime("image.jpg"))

# takes in list of dictionaries, spits out a dataframe
async def data_prep(data):
    pass

# takes in a dataframe, returns path to vizualization in the format of "static/{c_code}_hist.jpg"
async def hist_viz(data, c_code):
    pass

# takes in a dataframe, returns path to vizualization in the format of "static/{c_code}_viz2.jpg"
async def viz_2(data, c_code):
    pass

# takes in a dataframe, returns path to vizualization in the format of "static/{c_code}_viz3.jpg"
async def viz_3(data, c_code):
    pass

# takes in a dataframe, returns path to vizualization in the format of "static/{c_code}_viz4.jpg"
async def viz_4(data, c_code):
    pass

# takes in a dataframe, returns path to vizualization in the format of "static/{c_code}_reg.jpg"
async def regression(data, c_code):
    pass

# Most likely won't be doing this one as it is extremely compute intensive, I've only gpu trained these
# and they took forever even then although the datasets were much larger
# takes in a dataframe, returns path to vizualization in the format of "static/{c_code}_arma.jpg"
async def arma(data, c_code):
    pass

# Initalize all the slugs needed for getting data from country
@app.on_event("startup")
async def startup_event():
    for x in await data_fetch("https://api.covid19api.com/countries"):
        SLUG_FARM[x["ISO2"]] = x["Slug"]

# Index entrypoint for website. 
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html",
    {"request": request,"summary" : (await data_fetch("https://api.covid19api.com/summary"))['Global']})

@app.get("/admin")
async def admin(request: Request):
    print("Admin Route")
    return templates.TemplateResponse("admin.html", {"request": request})

# Get data by country code
@app.get("/country/{c_code}")
async def test(request: Request, c_code: str = None):
    if not c_code or c_code.upper() not in SLUG_FARM.keys():
        return templates.TemplateResponse("404.html", {"request": request})
    dead, confirm, recover, active, country = 0, 0, 0, 0, SLUG_FARM[c_code.upper()]
    data = list(await data_fetch(f"https://api.covid19api.com/live/country/{country}/status/confirmed"))
    for x in data:
        if "2020-04-23" in x['Date']:
            dead = dead + x['Deaths']
            confirm = confirm + x['Confirmed']
            recover = recover + x['Recovered']
            active = active + x['Active']
    data = data_prep(data)
    v1, v2, v3, v4, reg = hist_viz(data, c_code), viz_2(data, c_code), viz_3(data, c_code), viz_4(data, c_code), regression(data, c_code) 

    return templates.TemplateResponse("country.html",
        {"request": request, "data" : {"dead": dead, "confirmed": confirm, "active": active, "recovered": recover}, "country": 
        " ".join(map(lambda x: x.capitalize(), country.split("-")))})

# 404 error handling
@app.get("/.*")
async def err_render(request: Request):
    return templates.TemplateResponse("404.html", {"request": request})