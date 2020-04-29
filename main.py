from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os, logging, datetime, sys, aiohttp, data_obj

# Constant slugs for country code id
SLUG_FARM = {}

# Initialize application 
app = FastAPI()
# Mount templates directory for Jinja rendering
templates = Jinja2Templates(directory="templates")
# Mount static directory as the root 
app.mount("/static", StaticFiles(directory="static"), name="static")

# Aux Functions
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
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html",
    {"request": request,"summary" : (await data_fetch("https://api.covid19api.com/summary"))['Global']})

# Admin page route
@app.get("/admin")
async def admin(request: Request):
    print("Admin Route")
    return templates.TemplateResponse("admin.html", {"request": request})

# Get all worldwide data aggregated by country
@app.get("/all/{req}")
async def get_all(request: Request, req: str = None):
    if req.lower() not in ["deaths", "recovered", "confirmed"]:
        return templates.TemplateResponse("404.html", {"request": request})
    data = (await data_fetch("https://api.covid19api.com/summary"))['Global']
    if req.lower() == "deaths": ttl, recent = data['TotalDeaths'], data['NewDeaths']
    elif req.lower() == "recovered": ttl, recent = data['TotalRecovered'], data['NewRecovered']
    else: ttl, recent = data['TotalConfirmed'], data['NewConfirmed']
    return templates.TemplateResponse("all.html", {"request": request, "title": req.capitalize(), "total": ttl, "new": recent})

# Get data by country code
@app.get("/country/{c_code}")
async def test(request: Request, c_code: str = None):
    if not c_code or c_code.upper() not in SLUG_FARM.keys():
        return templates.TemplateResponse("404.html", {"request": request})
    dead, confirm, recover, active, country = 0, 0, 0, 0, SLUG_FARM[c_code.upper()]
    data = list(await data_fetch(f"https://api.covid19api.com/live/country/{country}/status/confirmed"))
    for x in data:
        if str(datetime.date.today()) in x['Date']:
            dead = dead + x['Deaths']
            confirm = confirm + x['Confirmed']
            recover = recover + x['Recovered']
            active = active + x['Active']
    d = data_obj.Data(data)
    v1, v2, v3 = await d.hist_viz(d, c_code), await d.viz_2(d, c_code), await d.viz_3(d, c_code),
    v4, reg, arima = await d.viz_4(d, c_code), await d.regression(d, c_code), await d.arima(d, c_code) 
    return templates.TemplateResponse("country.html",
        {"request": request, "data" : {"dead": dead, "confirmed": confirm, "active": active, "recovered": recover},
        "country": " ".join(map(lambda x: x.capitalize(), country.split("-"))), "v1": v1, "v2": v2, "v3": v3, "v4": v4, "reg": reg, "ari": arima})

# 404 error handling
@app.get("/.*")
async def err_render(request: Request):
    return templates.TemplateResponse("404.html", {"request": request})