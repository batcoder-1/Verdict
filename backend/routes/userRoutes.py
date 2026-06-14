from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from typing import Annotated
from backend.auth import Token,create_user,authenticate_user,get_user,update_user
from backend.models import users
from backend.database import SessionDep
user=APIRouter()
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/cp_analyzer/login")
@user.post('/cp_analyzer/signup',
           response_model=Token)
async def signup(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],session:SessionDep):
    token=await create_user(users.UserCreate(username=form_data.username,password=form_data.password),session)
    return token

@user.post('/cp_analyzer/login',
           response_model=Token)
async def login(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],session:SessionDep):
    token=await authenticate_user(users.UserCreate(username=form_data.username,password=form_data.password),session)
    return token

@user.get('/cp_analyzer/profile',
          response_model=users.UserRead)
async def profile(token:Annotated[str,Depends(oauth2_scheme)],session:SessionDep):
    user=await get_user(token,session)
    return user

@user.patch('/cp_analyzer/profile',
        response_model=users.UserRead)
async def update_profile(token:Annotated[str,Depends(oauth2_scheme)],session:SessionDep,user:users.userUpdate):
    updated_user=await update_user(token,session,user)
    return updated_user