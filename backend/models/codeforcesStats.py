from sqlmodel import Field,SQLModel
from uuid import UUID
from datetime import datetime
class codeforcesProfile(SQLModel,table=True):
    id:UUID=Field(foreign_key="user.id",primary_key=True)
    firstname:str|None=None
    lastname:str|None=None
    rating:int|None=None
    max_rating:int|None=None
    rank:str|None=None
    max_rank:str|None=None
    country:str|None=None
    friendsCount:int|None=None
class codeforcesContest(SQLModel,table=True):
    user_id:UUID=Field(foreign_key="user.id")
    id:int=Field(primary_key=True,default=None)
    contest_name:str|None=None
    rank:int|None=None
    old_rating:int|None=None
    new_rating:int|None=None
    contest_date:datetime|None=None
    contest_id:int|None=None