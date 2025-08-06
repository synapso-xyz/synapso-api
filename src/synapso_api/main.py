from fastapi import FastAPI

from .routes import cortex, query, system

synapso_api = FastAPI()


synapso_api.include_router(cortex.router, prefix="/cortex")
synapso_api.include_router(query.router, prefix="/query")
synapso_api.include_router(system.router, prefix="/system")


# Health check route
@synapso_api.get("/")
async def read_root():
    """Health check endpoint that returns API status."""
    return {"message": "Synapso API is running"}
