import requests
from models import leetcodeStats
import asyncio
from datetime import datetime,date,timedelta
import time
handle="?handles=k_ni_ght"
api="https://codeforces.com/api/user.status?handle=Dominater069&from=1&count=10"
api2="http://localhost:3000/Naman-Bhavsar/calendar?year=2026"
api3="http://localhost:3000/Batknight2005/acSubmission?limit=21"
# res=requests.get(api)
# contest=res.json()
ids=[]
dates=[]
last_sync_date=1

s=time.perf_counter()
async def get_submission(start,offset):
    api=f"https://codeforces.com/api/user.status?handle=k_ni_ght&from={start}&count={offset}"
    res=requests.get(api)
    contest=res.json()
    dates=[]
    check=set()
    for i in contest["result"]:
        d=datetime.fromtimestamp(i["creationTimeSeconds"]).date()
        if i["verdict"] == 'OK' and d not in check:
         dates.append(d)
         check.add(d)
    return dates

def check(d):
    d1=d.year
    d2=date.today().year
    if d1 != d2:
        return False
    return True

start=1
offset=100
if last_sync_date is None:
    streak=0
    curr_streak=0
    longest_streak=0
    flag=True
    cnt=0
    prev=None
    isFlag=False
    yesterday=date.today()-timedelta(days=1)
    check_date=set()   
    while flag:
        dates=asyncio.run(get_submission(start,offset))
        if not dates:
            break
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
                #  print(f"{d} {prev}")
                if curr_streak==0 and isFlag:
                     curr_streak=streak
                longest_streak=max(streak,longest_streak)
                streak=1
            else: streak+=1
            prev=d
            print(d)
        longest_streak=max(streak,longest_streak)
        if curr_streak==0 and isFlag:
             curr_streak=streak
        if flag:
            start+=100
        cnt+=1
else:
    streak=0
    curr_streak=0
    longest_streak=0
    flag=True
    cnt=0
    prev=None
    isFlag=False
    yesterday=date.today()-timedelta(days=1)
    check_date=set()   
    while flag:
        dates=asyncio.run(get_submission(start,offset))
        if not dates:
            break
        for d in dates:
            if d in check_date:
                continue
            check_date.add(d)
            if(date.today() not in check_date or yesterday not in check_date):
                break
            if((check(d)==False or prev is not None and (prev-d).days>1)):
                flag=False
                longest_streak=max(longest_streak,streak)
                curr_streak=streak
                break
            else: streak+=1
            prev=d
            print(d)
        if curr_streak==0 and isFlag:
             curr_streak=streak
             longest_streak=max(curr_streak,longest_streak)
        if flag:
            start+=100
        cnt+=1
print(longest_streak)
print(curr_streak)
e=time.perf_counter()
print(f"Runtime: {e- s:.6f} seconds")