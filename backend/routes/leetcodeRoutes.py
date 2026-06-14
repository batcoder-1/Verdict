from fastapi import APIRouter,Depends
from backend.auth import Token
from backend.routes.userRoutes import oauth2_scheme
from typing import Annotated
from backend.services.leetcode import sync_profile
from backend.database import SessionDep
from backend.models import leetcodeStats
leetcode=APIRouter()

@leetcode.post('/cp_analyzer/profile/leetcode/sync',
               response_model=leetcodeStats.leetcodeProfile)
async def sync_leetcode_profile(token:Annotated[str,Depends(oauth2_scheme)],session:SessionDep):
    profile=await sync_profile(token,session)
    return profile