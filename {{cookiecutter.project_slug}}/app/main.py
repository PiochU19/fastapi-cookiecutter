from core import settings
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return settings.__dict__
