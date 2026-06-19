from backend.dependencies import decode_token
from backend.models.users import User
from fastapi import HTTPException
from backend.models.codeforcesStats import codeforcesProfile,codeforcesContest
from backend.services.leetcode import error_api
from sqlmodel import select
import httpx
from datetime import datetime,timezone,date
api="https://codeforces.com/api/user.info?handles="
contest_api="https://codeforces.com/api/user.rating?handle="
flag="&checkHistoricHandles=false"

async def get_sync_contest(handle):
    async with httpx.AsyncClient() as client:
        response=await client.get(contest_api+handle)
        await error_api(response)
        data=response.json()
        if data is None:
            raise HTTPException(
                status_code=502,
                detail="codeforces service unavailable"
            )
        if data["status"] != "OK":
            raise HTTPException(
                status_code=404,
                detail="codeforces handle invalid"
            )
        return data

async def get_sync_profile(handle):
    async with httpx.AsyncClient() as client:
        response=await client.get(api+handle+flag)
        await error_api(response)
        data=response.json()
        if data is None:
            raise HTTPException(
                status_code=502,
                detail="codeforces service unavailable"
            )
        if data["status"] != "OK":
            raise HTTPException(
                status_code=404,
                detail="codeforces handle invalid"
            )
        return data

async def sync_profile(token:str,session):
    id=await decode_token(token)
    db_user=session.get(User,id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )
    user_codeforces_profile=session.get(codeforcesProfile,id)
    if db_user.codeforces_handle is None:
        raise HTTPException(
            status_code=400,
            detail="codeforces handle not provided"
        )
    data=await get_sync_profile(db_user.codeforces_handle)
    sync_profile=codeforcesProfile(
        id=id,
        firstname=data["result"][0]["firstName"],
        lastname=data["result"][0]["lastName"],
        rating=data["result"][0]["rating"],
        max_rating=data["result"][0]["maxRating"],
        rank=data["result"][0]["rank"],
        max_rank=data["result"][0]["maxRank"],
        country=data["result"][0]["country"],
        friendsCount=data["result"][0]["friendOfCount"], 
        last_synced=date.today()
        )
    if user_codeforces_profile is None:
        session.add(sync_profile)
        session.commit()
        session.refresh(sync_profile)
        return sync_profile
    user_codeforces_profile.sqlmodel_update(sync_profile)
    session.add(user_codeforces_profile)
    session.commit()
    session.refresh(user_codeforces_profile)
    return user_codeforces_profile

async def get_profile(token:str,session):
    id=await decode_token(token)
    user_codeforces_profile=session.get(codeforcesProfile,id)
    if user_codeforces_profile is None:
        raise HTTPException(
            status_code=404,
            detail="user handle not found"
        )
    return user_codeforces_profile

def convert_date(date):
    contest_date=datetime.fromtimestamp(date,tz=timezone.utc)
    return contest_date

async def sync_contest(token:str,session):
    id=await decode_token(token)
    db_user=session.get(User,id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )
    user_codeforces_handle=db_user.codeforces_handle
    if user_codeforces_handle is None:
        raise HTTPException(
            status_code=400,
            detail="codeforces handle not provided"
        )
    contests=await get_sync_contest(user_codeforces_handle)
    query=select(codeforcesContest).where(codeforcesContest.user_id==id)
    user_contest=session.exec(query).all()
    user_contest_userid_contestid=set()
    for contest in user_contest:
        user_contest_userid_contestid.add((contest.contest_id,contest.user_id))
    codeforces_contest=[]
    for contest in contests["result"]: # what if user has not participated in an any contest
        new_contest=codeforcesContest(
            user_id=id,
            contest_name=contest["contestName"],
            contest_id=contest["contestId"],
            new_rating=contest["newRating"],
            old_rating=contest["oldRating"],
            rank=contest["rank"],
            contest_date=convert_date(contest["ratingUpdateTimeSeconds"]),
            last_synced=date.today()
        )
        if (new_contest.contest_id,id) in user_contest_userid_contestid:
            continue
        codeforces_contest.append(new_contest)
        session.add(new_contest)
        
    session.commit()
    for contest in codeforces_contest:
        session.refresh(contest)
    user_contest=session.exec(query).all()
    return user_contest
    
    
async def get_contest(token:str,session):
    id=await decode_token(token)
    db_user=session.get(User,id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )
    query=select(codeforcesContest).where(codeforcesContest.user_id==id)
    user_contest=session.exec(query).all()
    return user_contest
        