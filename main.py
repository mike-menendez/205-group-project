from fastapi import FastAPI
import os, logging, datetime

app = FastAPI()

# Main entrypoint for api. 
@app.get("/")
def index():
    pass

# Test route for clarity.
# http://localhost:8000/test/1?q=foo
@app.get("/test/{test_id}")
def test(test_id: int, q: str = None):
    # uncomment these lines to see them on the terminal
    # print(f"q:<{q}>")
    # print(f"test_id:<{test_id}>")
    return {"test_id": test_id, "q": q}
