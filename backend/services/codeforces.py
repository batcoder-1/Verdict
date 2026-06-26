from backend.dependencies import decode_token
from backend.models.users import User
from fastapi import HTTPException
from backend.models.codeforcesStats import codeforcesProfile,codeforcesContest
from backend.services.leetcode import error_api
from sqlmodel import select
from datetime import timedelta,datetime,date
import httpx
from datetime import datetime,timezone,date
api="https://codeforces.com/api/user.info?handles="
contest_api="https://codeforces.com/api/user.rating?handle="
flag="&checkHistoricHandles=false"

async def get_streak(handle,start,offset):
    streak_api=f"https://codeforces.com/api/user.status?handle={handle}&from={start}&count={offset}"
    async with httpx.AsyncClient(timeout=15) as client:
        response=await client.get(streak_api)
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
        dates=[]
        ids=[]
        check_date=set()
        for i in data["result"]:
            d=datetime.fromtimestamp(i["creationTimeSeconds"],tz=timezone.utc).date()
            if i["verdict"] == "OK" and d not in check_date:
                dates.append(d)
                check_date.add(d)
                ids.append(i["id"])
        data={
            "dates":dates,
            "id":ids
        }
        return data
    
def check(d):
    d1=d.year
    d2=date.today().year
    if d1!=d2:
        return False
    return True

async def calculate_streak(handle,last_sync,current_longest_streak,last_submission_id,current_streak):
    start=1
    offset=100
    current_last_submission_id=None
    if last_sync is None:
        streak=0
        curr_streak=0
        longest_streak=0
        flag=True
        prev=None
        isFlag=False
        yesterday=date.today()-timedelta(days=1)
        check_date=set()
        while flag:# add the feature for last submission id 
            data=await get_streak(handle,start,offset)
            dates=data["dates"]
            ids=data["id"]
            if not dates:
                break
            if current_last_submission_id is None:
                current_last_submission_id=ids[0]
            for d in dates:
                if d in check_date:
                    continue
                check_date.add(d)
                if isFlag==False and (date.today() in check_date or yesterday in check_date):
                     isFlag=True
                if(check(d)==False):
                 flag=False
                 break
                if prev is not None and (prev-d).days>1:
                    if curr_streak==0 and isFlag:
                        curr_streak=streak
                    longest_streak=max(streak,longest_streak)
                    streak=1
                else: streak+=1
                prev=d
            longest_streak=max(longest_streak,streak)
            if curr_streak==0 and isFlag:
                curr_streak=streak
            if flag:
                start+=100
    else:
        streak=0
        curr_streak=0
        longest_streak=current_longest_streak
        flag=True
        prev=None
        yesterday=date.today()-timedelta(days=1)
        check_date=set()
        while flag:
            data=await get_streak(handle,start,offset)
            dates=data["dates"]
            ids=data["id"]
            if not dates:
                break
            if current_last_submission_id is None:
                current_last_submission_id=ids[0]
            for d,id in zip(dates,ids):
                if d in check_date:
                    continue
                check_date.add(d)
                if id == last_submission_id:
                    curr_streak=streak+current_streak
                    longest_streak=max(curr_streak,longest_streak)
                    flag=False
                    break
                if (date.today() not in check_date or yesterday not in check_date):
                     break
                if(check(d)==False or prev is not None and (prev-d).days>1):
                 longest_streak=max(streak,longest_streak)
                 curr_streak=streak
                 flag=False
                 break
                else: streak+=1
                prev=d
            if curr_streak==0:
                longest_streak=max(longest_streak,streak)
                curr_streak=streak
            if flag:
                start+=100
    return{
         "curr_streak":curr_streak,
         "longest_streak":longest_streak,
         "id":current_last_submission_id
         
    }
            
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
    last_synced_date=None
    longest_streak=0
    last_submission_id=None
    current_streak=0
    if user_codeforces_profile:
        last_synced_date=user_codeforces_profile.last_synced
        longest_streak=user_codeforces_profile.current_year_longest_streak
        last_submission_id=user_codeforces_profile.last_submission_id
        current_streak=user_codeforces_profile.current_streak
    data=await get_sync_profile(db_user.codeforces_handle)
    streak=await calculate_streak(db_user.codeforces_handle,last_synced_date,longest_streak,last_submission_id,current_streak)
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
        last_synced=date.today(),
        current_streak=streak["curr_streak"],
        current_year_longest_streak=streak["longest_streak"],
        last_submission_id=streak["id"]
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
    for contest in contests["result"]: 
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
        