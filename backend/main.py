from fastapi import FastAPI
from app.api.v1.endpoints import plumes

app = FastAPI(title="MethaneMinder API", version="0.1.0")
app.include_router(plumes.router, prefix="/v1")
