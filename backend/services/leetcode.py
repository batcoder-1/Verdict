from dependencies import decode_token
from models import leetcodeStats,users
from fastapi import HTTPException
import httpx
import asyncio
from sqlmodel import select
from datetime import datetime,date
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
        
api="https://alfa-leetcode-api.onrender.com/" 


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
        response, response1,response2,response3 = await asyncio.gather(
        client.get(api + handle + "/profile"),
        client.get(api + handle + "/contest"),
        client.get(api+handle+"/calendar"),
        client.get(api+handle+f"/calendar?year={datetime.now().year}")
     )
        await error_api(response)
        await error_api(response1)
        await error_api(response2)
        await error_api(response3)
        data1=response.json()
        data2=response1.json()
        data3=response2.json()
        data4=response3.json()
        errors1=data1.get("errors")
        errors2=data2.get("errors")
        errors3=data3.get("errors")
        errors4=data4.get("errors")
        error_data(errors1)
        error_data(errors2)
        error_data(errors3)
        error_data(errors4)
        data={
            "profile":data1,
            "contest":data2,
            "calendar":data3,
            "calendar_current":data4
        }
    return data

def calculate_current_streak(submissions):
   dates=[]
   prev=""
   a=""
   for i in submissions:
       if i==':':
           date=int(a)
           dates.append(date)
           a=""
       if i>='0' and i<='9' and prev=='"':
            a+=i
       else:
           prev=i
   prevnum=0
   curr_streak=0
   for i in reversed(dates):
       d1=datetime.fromtimestamp(prevnum).date()
       d2=datetime.fromtimestamp(i).date()
       if prevnum!=0:
           if (d1-d2).days>1:
               break
       curr_streak+=1
       prevnum=i
   return curr_streak

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
            contest_percentage=data["contest"]["contestTopPercentage"],
            max_streak_current_year=data["calendar"]["streak"],
            current_streak=calculate_current_streak(data["calendar_current"]["submissionCalendar"]),
            last_synced=date.today()
            
     )
    else:
        sync_leetcode_profile=leetcodeStats.leetcodeProfile(
            user_id=id,
            solved_problems=data["profile"]["totalSolved"],
            hard_solved_problems=data["profile"]["hardSolved"],
            medium_solved_problems=data["profile"]["mediumSolved"],
            easy_solved_problems=data["profile"]["easySolved"],
            ranking=data["profile"]["ranking"], 
            max_streak_current_year=data["calendar"]["streak"],
            current_streak=calculate_current_streak(data["calendar_current"]["submissionCalendar"]),  
            last_synced=date.today()
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

def convert_finishTime(time): 
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
    for contest in contests:
        if (db_user.id,contest["contest"]["title"]) in user_contests_name_id:
            continue
        new_contest=leetcodeStats.leetcodeContest(
            user_id=db_user.id,
            contest_name=contest["contest"]["title"],
            rating=contest["rating"],
            ranking=contest["ranking"],
            problems_solved=contest["problemsSolved"],
            total_problems=contest["totalProblems"],
            finishTime=convert_finishTime(contest["finishTimeInSeconds"]),
            last_synced=date.today()
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
