from sqlmodel import SQLModel, Session, create_engine
from typing import Annotated
from fastapi import Depends
from models.leetcodeStats import leetcodeProfile
from models.users import User
from models.codeforcesStats import codeforcesProfile
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]