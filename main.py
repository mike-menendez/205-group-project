# Authors: Mike Menendez, Frank Piva, Felix Romero-Flores, Edgaras Slezas
# Date: May 11, 2020
# Course: CST 205
# Description: This is the main driver web server. This backend serves all endpoints
#              and renders the requested web pages on the fly via Jinja2 templates.
#              this backend also fetches remote data from an external api

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import aiohttp
import data_obj
import search_data as sd

# Constant slugs for country code id
SLUG_FARM = {}

# Initialize application
app = FastAPI()
# Mount templates directory for Jinja rendering
templates = Jinja2Templates(directory="templates")
# Mount static directory as the root
app.mount("/static", StaticFiles(directory="static"), name="static")

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

# Index entrypoint for website.
@app.get("/", status_code=200)
async def index(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "summary": (await data_fetch("https://api.covid19api.com/summary"))['Global']})

# Data for search mapping
@app.get("/preload")
async def preload(request: Request):
    return sd.search_data

# Health check for SSL terminating proxy
@app.get("/health", status_code=200)
async def health_check(request: Request):
    return ""

# Admin page route
@app.get("/info")
async def admin(request: Request):
    return templates.TemplateResponse("info.html", {"request": request})

# Get all worldwide data aggregated by country
@app.get("/all/{req}")
async def get_all(request: Request, req: str = None):
    if req.lower() not in ["deaths", "recovered", "confirmed"]:
        return templates.TemplateResponse("404.html", {"request": request})
    data = (await data_fetch("https://api.covid19api.com/summary"))
    glob, data = data['Global'], data['Countries']
    countries = []
    if req.lower() == "deaths":
        ttl = 'TotalDeaths'
    elif req.lower() == "recovered":
        ttl = 'TotalRecovered'
    else:
        ttl = 'TotalConfirmed'
    for x in data:
        countries.append((x['Country'], x[ttl]))
    countries = list(filter(lambda x: x[1] != 0, countries))
    countries.sort(key=lambda x: x[1], reverse=True)
    return templates.TemplateResponse("all.html", {"request": request, "title": req.capitalize(), "countries": countries, "tot": glob[ttl]})

# Get data by country code
@app.get("/country/{c_code}")
async def test(request: Request, c_code: str = None):
    if not c_code or c_code.upper() not in SLUG_FARM.keys():
        return templates.TemplateResponse("404.html", {"request": request})
    country, data = SLUG_FARM[c_code.upper()], None
    temp = (await data_fetch("https://api.covid19api.com/summary"))['Countries']
    for x in temp:
        if x["Slug"] == country:
            data = x
            break
    if data is None:
        return templates.TemplateResponse("404.html", {"request": request})
    dead, confirm, recover, active = x['TotalDeaths'], x['TotalConfirmed'], x['TotalRecovered'], (
        x['TotalConfirmed'] - x['TotalDeaths'] - x['TotalRecovered'])
    d = data_obj.Data(temp)
    v1 = await d.hist_viz(d, c_code)
    return templates.TemplateResponse("country.html",
                                      {"request": request, "data": {"dead": dead, "confirmed": confirm, "active": active, "recovered": recover},
                                       "country": " ".join(map(lambda x: x.capitalize(), country.split("-"))), "v1": v1})

# 404 error handling
@app.get("/.*")
async def err_render(request: Request):
    return templates.TemplateResponse("404.html", {"request": request})
