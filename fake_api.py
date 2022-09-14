"""
This is a simple API that can be used to exercise the ApiMonitor.

To run: uvicorn fake_api:app --reload
"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    """
    Simple hello world function.
    The status can be changed from "OK" to something else to simulate an outage.
    """
    return {"message": "Hello World",
            "status": "OK"}
    