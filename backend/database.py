from sqlmodel import SQLModel,Session,create_engine
from typing import Annotated 
from fastapi import Depends
from backend.models.leetcodeStats import leetcodeProfile
from backend.models.users import User
from backend.models.codeforcesStats import codeforcesProfile
from backend.config import DATABASE_URL

database_url=DATABASE_URL
connect_args={"check_same_thread":False}
engine=create_engine(database_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
   with Session(engine) as session:
    yield session
SessionDep=Annotated[Session,Depends(get_session)]
