from core import settings
from fastapi import FastAPI


def get_application() -> FastAPI:
    app = FastAPI()

    return app


app = get_application()


@app.get("/")
async def root():
    return settings.__dict__
