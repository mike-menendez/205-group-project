# 205-group-project
Group Project for CST 205

## Data

COVID-19 data comes from [Kyle Redelinghuys'](https://twitter.com/ksredelinghuys) [COVID-19 API](https://covid19api.com/#) which in turn pulls its data from the [COVID-19 Data Repository](https://github.com/CSSEGISandData/COVID-19), provided by JHU CCSE. It is programmatically retrieved, re-formatted and stored in the server every 10 minutes.

## Prerequisites

[Python 3.6](https://www.python.org/downloads/)

## Installation:

`git clone https://github.com/mike-menendez/205-group-project`

`cd 205-group-project`

`pip install -r requirements.txt`

### Start the API for development

`uvicorn main:app --reload`

## Docker
Docker for development

### Installation
`git clone https://github.com/mike-menendez/205-group-project`

`cd 205-group-project`

`docker build . -t covid`

### Run
`docker run -d -v ${PWD}:/usr/src/app --name covid --network="host" covid`

Access it by going to http://127.0.0.1:8000

### Stop
`docker stop covid`
