from fastapi import FastAPI

from app.api.v1 import v1_router

app = FastAPI()

app.include_router(v1_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
