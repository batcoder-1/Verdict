from fastapi import APIRouter,Depends
from backend.routes.userRoutes import oauth2_scheme
from typing import Annotated
from backend.database import SessionDep
from backend.models.codeforcesStats import codeforcesProfile,codeforcesContest
from backend.services.codeforces import sync_profile,get_profile,sync_contest,get_contest
from backend.dependencies import get_access_token
codeforces=APIRouter()

@codeforces.post('/cp_analyzer/profile/codeforces/sync',
                 response_model=codeforcesProfile)
async def sync_codeforces_profile(token:Annotated[str,Depends(get_access_token)],session:SessionDep):
    profile=await sync_profile(token,session)
    return profile

@codeforces.get('/cp_analyzer/profile/codeforces',
                response_model=codeforcesProfile)
async def get_codeforces_profile(token:Annotated[str,Depends(get_access_token)],session:SessionDep):
    profile=await get_profile(token,session)
    return profile

@codeforces.post('/cp_analyzer/profile/codeforces/contest/sync',
                 response_model=list[codeforcesContest])
async def sync_codeforces_contest(token:Annotated[str,Depends(get_access_token)],session:SessionDep):
    contests=await sync_contest(token,session)
    return contests

@codeforces.get('/cp_analyzer/profile/codeforces/contest',
                response_model=list[codeforcesContest])
async def get_codeforces_contest(token:Annotated[str,Depends(get_access_token)],session:SessionDep):
    contests=await get_contest(token,session)
    return contests