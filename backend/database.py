from sqlmodel import SQLModel, Session, create_engine
from typing import Annotated
from fastapi import Depends
from backend.models.leetcodeStats import leetcodeProfile
from backend.models.users import User
from backend.models.codeforcesStats import codeforcesProfile
from backend.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]