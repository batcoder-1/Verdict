from fastapi import APIRouter,Depends,Response
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from typing import Annotated
from auth import Token,create_user,authenticate_user,get_user,update_user
from models import users
from database import SessionDep
from dependencies import get_access_token
from config import ACCESS_TOKEN_EXPIRES_MINUTES
user=APIRouter()
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/cp_analyzer/login")
@user.post('/cp_analyzer/signup',
           response_model=Token)
async def signup(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],session:SessionDep):
    token=await create_user(users.UserCreate(username=form_data.username,password=form_data.password),session)
    return token

@user.post('/cp_analyzer/login')
async def login(response:Response,form_data:Annotated[OAuth2PasswordRequestForm,Depends()],session:SessionDep):
    token=await authenticate_user(users.UserCreate(username=form_data.username,password=form_data.password),session)
    response.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=ACCESS_TOKEN_EXPIRES_MINUTES * 60,
    )
    return {"message":"Login Successfull"}

@user.post('/cp_analyzer/logout')
async def logout(response:Response):
    response.delete_cookie("access_token")
    return{
        "messsage":"Logged out successfully"
    }

@user.get('/cp_analyzer/profile',
          response_model=users.UserRead)
async def profile(token:Annotated[str,Depends(get_access_token)],session:SessionDep):
    user=await get_user(token,session)
    return user

@user.patch('/cp_analyzer/profile',
        response_model=users.UserRead)
async def update_profile(token:Annotated[str,Depends(get_access_token)],session:SessionDep,user:users.userUpdate):
    updated_user=await update_user(token,session,user)
    return updated_user
