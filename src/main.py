from fastapi import FastAPI

from src.routes import cortex, query

app = FastAPI()


app.include_router(cortex.router)
app.include_router(query.router)


# Health check route
@app.get("/")
async def read_root():
    return {"message": "Server is running ✅"}
