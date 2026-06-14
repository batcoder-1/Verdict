from sqlmodel import Field, SQLModel
from uuid import UUID,uuid4

class UserBase(SQLModel):
    username:str=Field(unique=True,index=True)
    isActive:bool=Field(default=True)

class User(UserBase,table=True):
    id:UUID=Field(default_factory=uuid4,primary_key=True)
    hashed_password:str
    leetcode_handle:str|None=Field(default=None,index=True)
    codeforces_handle:str|None=Field(default=None,index=True)
class UserCreate(UserBase):
    password:str
class UserRead(UserBase):
    id:UUID
    leetcode_handle:str|None
    codeforces_handle:str|None

class userUpdate(SQLModel):
    leetcode_handle:str|None=None
    codeforces_handle:str|None=None