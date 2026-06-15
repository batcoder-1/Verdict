from sqlmodel import SQLModel,Field
from uuid import UUID
class leetcodeProfile(SQLModel,table=True):
    user_id:UUID=Field(foreign_key="user.id",primary_key=True)
    solved_problems:int|None=None
    hard_solved_problems:int|None=None
    medium_solved_problems:int|None=None
    easy_solved_problems:int|None=None
    unsolved_problems:int|None=None
    ranking:int|None=None
    contest_count:int|None=None
    contest_rating:int|None=None
    contest_ranking:int|None=None
    contest_percentage:float|None=None