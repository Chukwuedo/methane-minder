from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.api.v1.endpoints import plumes, risk

app = FastAPI(
    title="Methane Minder Backend",
    description="API for methane plume data processing and visualization",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plumes.router, prefix="/v1")
app.include_router(risk.router, prefix="/v1")


@app.get("/")
async def root():
    return {"message": "Methane Minder API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
