from fastapi import FastAPI

from .routes import cortex, query

app = FastAPI()


app.include_router(cortex.router, prefix="/cortex")
app.include_router(query.router, prefix="/query")


# Health check route
@app.get("/")
async def read_root():
    """Health check endpoint that returns API status."""
    return {"message": "Synapso API is running"}
