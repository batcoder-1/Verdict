from sqlmodel import Field,SQLModel
from uuid import UUID

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