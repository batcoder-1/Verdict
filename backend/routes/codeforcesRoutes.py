from fastapi import APIRouter,Depends
from backend.routes.userRoutes import oauth2_scheme
from typing import Annotated
from backend.database import SessionDep
from backend.models.codeforcesStats import codeforcesProfile
from backend.services.codeforces import sync_profile,get_profile
codeforces=APIRouter()

@codeforces.post('/cp_analyzer/profile/codeforces/sync',
                 response_model=codeforcesProfile)
async def sync_codeforces_profile(token:Annotated[str,Depends(oauth2_scheme)],session:SessionDep):
    profile=await sync_profile(token,session)
    return profile

@codeforces.get('/cp_analyzer/profile/codeforces',
                response_model=codeforcesProfile)
async def get_codeforces_profile(token:Annotated[str,Depends(oauth2_scheme)],session:SessionDep):
    profile=await get_profile(token,session)
    return profile