from sqlmodel import SQLModel,Session,create_engine
from typing import Annotated 
from fastapi import Depends
from backend.models.leetcodeStats import leetcodeProfile
from backend.models.users import User
from backend.models.codeforcesStats import codeforcesProfile
sqlite_file_name="cp_analyzer.db"
sqlite_url=f"sqlite:///{sqlite_file_name}"
connect_args={"check_same_thread":False}
engine=create_engine(sqlite_url,connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
   with Session(engine) as session:
    yield session
print(SQLModel.metadata.tables.keys())
SessionDep=Annotated[Session,Depends(get_session)]
