from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import userRoutes
from routes import leetcodeRoutes
from routes import codeforcesRoutes
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
       "https://verdict-uhvt.vercel.app"
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
