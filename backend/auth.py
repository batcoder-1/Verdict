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
from sqlmodel import select
from uuid import UUID
class Token(BaseModel):
    access_token:str
    token_type:str
password_hash=PasswordHash.recommended()
DUMMY_HASH=password_hash.hash("test@1234")

def create_access_token(data:dict,expires_delta:timedelta|None=None):
    data_encode=data.copy()
    if expires_delta:
        expire=datetime.now(timezone.utc)+expires_delta
    else:
        expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    data_encode.update({"exp":expire})
    encode_jwt=jwt.encode(data_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt
async def decode_token(token:str)->UUID:
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id=UUID(payload.get("sub"))
        if id is None:
            raise HTTPException(status_code=401,detail="User is unauthorized")
    except InvalidTokenError:
        raise HTTPException(status_code=401,detail="User is unauthorized")
    return id


def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(password,hash_password):
    return password_hash.verify(password,hash_password)

async def create_user(user:users.UserCreate,session):
   hashed_password=get_password_hash(user.password)
   db_user=users.User(
       username=user.username,
       hashed_password=hashed_password
   )
   try:
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
   except Exception as e:
      print(e)
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
            status_code=404,
            detail="username or password invalid"
        )
    if not verify_password(user.password,db_user.hashed_password):
        raise HTTPException(
            status_code=404,
            detail="username or password is invalid"
        )
    access_token=create_access_token(
        data={"sub":str(db_user.id)}
    )
    return Token(access_token=access_token,token_type="Bearer")

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
    return updated_user    
    
        