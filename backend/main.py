from fastapi import FastAPI
from app.api.v1.endpoints import plumes

app = FastAPI(
    title="Methane Minder Backend",
    description="API for methane plume data processing and visualization",
    version="0.1.0",
)

app.include_router(plumes.router, prefix="/v1")


@app.get("/")
async def root():
    return {"message": "Methane Minder API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
