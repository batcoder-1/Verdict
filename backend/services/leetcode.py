from backend.auth import decode_token
from backend.models import leetcodeStats,users
from fastapi import HTTPException
import httpx
api="http://localhost:3000/"#currently for testing with docker running alongside 
async def get_sync_profile(handle):
    async with httpx.AsyncClient() as client:
        response=await client.get(api+handle+"/profile")
        if response.status_code!=200:
            raise HTTPException(
                status_code=500,
                detail="Bad Gateway"
            )
        data=response.json()
        errors = data.get("errors")

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
    profile=await get_sync_profile(db_user.leetcode_handle)
    sync_leetcode_profile=leetcodeStats.leetcodeProfile(
         user_id=id,
         solved_problems=profile["totalSolved"],
         hard_solved_problems=profile["hardSolved"],
         medium_solved_problems=profile["mediumSolved"],
         easy_solved_problems=profile["easySolved"],
         ranking=profile["ranking"]
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