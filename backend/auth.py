from datetime import datetime,timedelta,timezone
from typing import Annotated
import jwt
from fastapi import HTTPException,status
from pwdlib import PasswordHash
from pydantic import BaseModel
from jwt.exceptions import InvalidTokenError
from backend.config import ALGORITHM,SECRET_KEY,ACCESS_TOKEN_EXPIRES_MINUTES
from backend.models import users
from backend.database import SessionDep
from sqlmodel import select,delete
from uuid import UUID
from backend.dependencies import decode_token
from backend.utils import DUMMY_HASH,get_password_hash,verify_password
from backend.models.leetcodeStats import leetcodeContest
from backend.models.codeforcesStats import codeforcesContest
class Token(BaseModel):
    access_token:str
    token_type:str

def create_access_token(data:dict,expires_delta:timedelta|None=None):
    data_encode=data.copy()
    if expires_delta:
        expire=datetime.now(timezone.utc)+expires_delta
    else:
        expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    data_encode.update({"exp":expire})
    encode_jwt=jwt.encode(data_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt

async def create_user(user:users.UserCreate,session):
   hashed_password=get_password_hash(user.password)
   query=select(users.User).where(users.User.username==user.username)
   db_user=session.exec(query).first()
   if db_user != None:
       raise HTTPException(
           status_code=400,
           detail="username already exist"
       )
   db_user=users.User(
       username=user.username,
       hashed_password=hashed_password
   )
   try:
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
   except:
        raise HTTPException(
            status_code=500,
            detail="internal server error"
        )
   access_token=create_access_token(
       data={"sub":str(db_user.id)}
   )
   return Token(access_token=access_token,token_type="Bearer")

async def authenticate_user(user:users.UserCreate,session):
    query=select(users.User).where(users.User.username==user.username)
    db_user=session.exec(query).first()
    if not db_user:
        verify_password(user.password,DUMMY_HASH)
        raise HTTPException(
            status_code=401,
            detail="username or password invalid"
        )
    if not verify_password(user.password,db_user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="username or password is invalid"
        )
    access_token=create_access_token(
        data={"sub":str(db_user.id)}
    )
    return Token(access_token=access_token,token_type="Bearer")

def check_leetcode_user(id,session):
    query=select(leetcodeContest).where(leetcodeContest.user_id==id)
    user_leetcode_contest=session.exec(query).all()
    if len(user_leetcode_contest) > 0:
        return True
    return False

def check_codeforces_user(id,session):
    query=select(codeforcesContest).where(codeforcesContest.user_id==id)
    user_codeforces_contest=session.exec(query).all()
    if len(user_codeforces_contest)>0:
        return True
    return False

async def get_user(token:str,session):
    id=await decode_token(token)
    db_user=session.get(users.User,id)
    if db_user is None:
        raise HTTPException(status_code=404,detail="User Not found")
    user=users.UserRead(
        username=db_user.username,
        id=db_user.id,
        leetcode_handle=db_user.leetcode_handle,
        codeforces_handle=db_user.codeforces_handle
    )
    if user is None:
        raise HTTPException(status_code=401,detail="User is unauthorized")
    return user

async def update_user(token:str,session,user:users.userUpdate)->users.UserRead:
    id=await decode_token(token)
    db_user=session.get(users.User,id)
    if db_user is None:
        raise HTTPException(
            status_code=400,detail="User not found"
        )
    if user.codeforces_handle is None and user.leetcode_handle is None:
        raise HTTPException(
            status_code=400,
            detail="Atleast one field must be provided"
        )
    db_user.sqlmodel_update(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    updated_user=users.UserRead(
        username=db_user.username,
        id=db_user.id,
        leetcode_handle=db_user.leetcode_handle,
        codeforces_handle=db_user.codeforces_handle
    )
    
    if check_leetcode_user(id,session):
        query=delete(leetcodeContest).where(leetcodeContest.user_id==id)
        session.exec(query)
    if check_codeforces_user(id,session):
        query1=delete(codeforcesContest).where(codeforcesContest.user_id==id)
        session.exec(query1)
        
    session.commit()
    return updated_user    
    
        