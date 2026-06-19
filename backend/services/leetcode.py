from backend.dependencies import decode_token
from backend.models import leetcodeStats,users
from fastapi import HTTPException
import httpx
import asyncio
from sqlmodel import select
async def error_api(response):
     if response.status_code!=200:
            raise HTTPException(
                status_code=500,
                detail="Bad Gateway"
            )
async def error_data(errors):
    if errors:
        message = errors[0].get("message", "")

        if "does not exist" in message.lower():
            raise HTTPException(
            status_code=400,
            detail="Invalid LeetCode handle"
        )

        raise HTTPException(
        status_code=502,
        detail="LeetCode service unavailable"
    )
        
api="http://localhost:3000/"#currently for testing with docker running alongside 


async def sync_contests_api(handle):
    async with httpx.AsyncClient() as client:
        response=await client.get(api+handle+"/contest")
        await error_api(response)
        data=response.json()
        error=data.get("errors")
        error_data(error)
        return data["contestParticipation"]


async def get_sync_profile(handle):
    async with httpx.AsyncClient() as client:
        response, response1 = await asyncio.gather(
        client.get(api + handle + "/profile"),
        client.get(api + handle + "/contest"),
     )
        await error_api(response)
        await error_api(response1)
        data1=response.json()
        data2=response1.json()
        errors1 = data1.get("errors")
        errors2=  data2.get("errors")
        error_data(errors1)
        error_data(errors2)
        data={
            "profile":data1,
            "contest":data2
        }
    return data

async def sync_profile(token,session):
    id=await decode_token(token)
    db_user=session.get(users.User,id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
  
    user_leetcode_profile=session.get(leetcodeStats.leetcodeProfile,id)
    if db_user.leetcode_handle is None:
        raise HTTPException(
            status_code=400,
            detail="leetcode handle not provided"
        )
    data=await get_sync_profile(db_user.leetcode_handle)
    if len(data["contest"]) > 1:
        sync_leetcode_profile=leetcodeStats.leetcodeProfile(
            user_id=id,
            solved_problems=data["profile"]["totalSolved"],
            hard_solved_problems=data["profile"]["hardSolved"],
            medium_solved_problems=data["profile"]["mediumSolved"],
            easy_solved_problems=data["profile"]["easySolved"],
            ranking=data["profile"]["ranking"],
            contest_count=data["contest"]["contestAttend"],
            contest_rating=data["contest"]["contestRating"],
            contest_ranking=data["contest"]["contestGlobalRanking"],
            contest_percentage=data["contest"]["contestTopPercentage"]      
     )
    else:
        sync_leetcode_profile=leetcodeStats.leetcodeProfile(
            user_id=id,
            solved_problems=data["profile"]["totalSolved"],
            hard_solved_problems=data["profile"]["hardSolved"],
            medium_solved_problems=data["profile"]["mediumSolved"],
            easy_solved_problems=data["profile"]["easySolved"],
            ranking=data["profile"]["ranking"],      
     )
    if user_leetcode_profile is None:
        session.add(sync_leetcode_profile)
        session.commit()
        session.refresh(sync_leetcode_profile)
        return sync_leetcode_profile
    user_leetcode_profile.sqlmodel_update(sync_leetcode_profile)
    session.add(user_leetcode_profile)
    session.commit()
    session.refresh(user_leetcode_profile)
    return user_leetcode_profile

async def get_profile(token,session):
    id=await decode_token(token)
    user_leetcode_profile=session.get(leetcodeStats.leetcodeProfile,id)
    if user_leetcode_profile is None:
        raise HTTPException(
            status_code=404,
            detail="leetcode profile of user doesn't exist"
        )
    return user_leetcode_profile
#here fetch all the contest of user if it exist store it in map or set and then check for (user id+contest name and if its doesnt exist then only add it)
def convert_finishTime(time): # only non existing contest will get added fix it
    ratio=time/3600
    hours=int(ratio)
    minutes=int((float(ratio)-int(ratio))*60)
    if hours==0:
        time=f"{minutes} minutes"
    else:
        time=f"{hours} hour {minutes} minutes"
    return time

async def sync_contests(token,session):
    id=await decode_token(token)
    db_user=session.get(users.User,id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )
    leetcode_handle=db_user.leetcode_handle
    contests=await sync_contests_api(leetcode_handle)
    query=select(leetcodeStats.leetcodeContest).where(leetcodeStats.leetcodeContest.user_id==id)
    user_contests=session.exec(query).all()
    user_contests_name_id=set()
    
    for contest in user_contests:
       user_contests_name_id.add((
           contest.user_id,
           contest.contest_name
       ))
       
    leetcode_contests=[]
    for contest in contests:#what if user has participated in any contest
        if (db_user.id,contest["contest"]["title"]) in user_contests_name_id:
            continue
        new_contest=leetcodeStats.leetcodeContest(
            user_id=db_user.id,
            contest_name=contest["contest"]["title"],
            rating=contest["rating"],
            ranking=contest["ranking"],
            problems_solved=contest["problemsSolved"],
            total_problems=contest["totalProblems"],
            finishTime=convert_finishTime(contest["finishTimeInSeconds"])
        )
        leetcode_contests.append(new_contest)
        session.add(new_contest)
        
    session.commit() 
    for contest in leetcode_contests:
        session.refresh(contest)
    user_contests=session.exec(query).all()
    return user_contests 

async def get_contests(token:str,session):
    id=await decode_token(token)
    db_user=session.get(users.User,id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )
    query=select(leetcodeStats.leetcodeContest).where(leetcodeStats.leetcodeContest.user_id==id)
    user_contests=session.exec(query).all()
    return user_contests