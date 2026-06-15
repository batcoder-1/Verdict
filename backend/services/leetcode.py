from backend.dependencies import decode_token
from backend.models import leetcodeStats,users
from fastapi import HTTPException
import httpx
import asyncio
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
            detail="leetcode profile of user doesnt exist"
        )
    return user_leetcode_profile