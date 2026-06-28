from fastapi import APIRouter,Depends
from auth import Token
from routes.userRoutes import oauth2_scheme
from typing import Annotated
from services.leetcode import sync_profile,get_profile,get_contests,sync_contests
from database import SessionDep
from models import leetcodeStats
from dependencies import get_access_token
leetcode=APIRouter()

@leetcode.post('/cp_analyzer/profile/leetcode/sync',
               response_model=leetcodeStats.leetcodeProfile)
async def sync_leetcode_profile(token:Annotated[str,Depends(get_access_token)],session:SessionDep):
    profile=await sync_profile(token,session)
    return profile

@leetcode.get('/cp_analyzer/profile/leetcode',
              response_model=leetcodeStats.leetcodeProfile)
async def leetcode_profile(token:Annotated[str,Depends(get_access_token)],session:SessionDep):
    profile=await get_profile(token,session)
    return profile

@leetcode.post('/cp_analyzer/profile/leetcode/contest/sync',
        response_model=list[leetcodeStats.leetcodeContest])
async def sync_leetcode_contests(token:Annotated[str,Depends(get_access_token)],session:SessionDep):
    contests=await sync_contests(token,session)
    return contests

@leetcode.get('/cp_analyzer/profile/leetcode/contest',
              response_model=list[leetcodeStats.leetcodeContest])
async def get_leetcode_contests(token:Annotated[str,Depends(get_access_token)],session:SessionDep):
    contests=await get_contests(token,session)
    return contests