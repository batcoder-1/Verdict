from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.database import create_db_and_tables,get_session
from backend.routes import userRoutes
@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_tables()
    yield
app=FastAPI(lifespan=lifespan)
app.include_router(userRoutes.user)
@app.get('/cp_analyzer')
async def greet():
    return {
        "message":"Welcome to the site and enjoy you stay"
    }