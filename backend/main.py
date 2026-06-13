from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.database import create_db_and_tables,get_session
@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_tables()
    yield
app=FastAPI(lifespan=lifespan)

