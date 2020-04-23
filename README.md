# 205-group-project
Group Project for CST 205

## Data

COVID-19 data comes from http://covid19api.herokuapp.com/ which in turn pulls it's data from the 2019 Novel Coronavirus (nCoV) Data Repository, provided by JHU CCSE. It is programmatically retrieved, re-formatted and stored in the server for every 10 minutes.

## Prerequisites

[Python 3.x](https://www.python.org/downloads/)

## Installation:

`git clone https://github.com/mike-menendez/205-group-project`

`cd 205-group-project`

`pip install -r requirements.txt`

### Start the API for development

`uvicorn main:app --reload`