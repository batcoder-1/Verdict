from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.routes import userRoutes
from backend.routes import leetcodeRoutes
from backend.routes import codeforcesRoutes
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(userRoutes.user)
app.include_router(leetcodeRoutes.leetcode)
app.include_router(codeforcesRoutes.codeforces)
@app.get('/cp_analyzer')
async def greet():
    return {
        "message":"Welcome to the site and enjoy you stay"
    }