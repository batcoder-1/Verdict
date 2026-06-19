import requests
from models import leetcodeStats
handle="?handles=k_ni_ght"
api="https://codeforces.com/api/user.rating?handle=k_ni_ght"
api2="http://localhost:3000/Naman-Bhavsar/calendar?year=2026"
api3="http://localhost:3000/Batknight2005/acSubmission?limit=21"
res=requests.get(api2)
contest=res.json()
print(contest["streak"])
last_synced=1781827200

# curr_streak=0
# prev=0
# print(type(contest["submissionCalendar"]))
# a=""
# dates=[]
# prev=""
# for i in contest["submissionCalendar"]:
#     if i==':':
#        date=int(a)
#        dates.append(date) 
#        a=""
#     if i >='0' and i<='9' and prev=='"':
#         a+=i
#     else:
#         prev=i
# prev=0
# for i in reversed(dates):
#     if prev!=0:
#         if prev-i != 86400:
#             break
#     curr_streak+=1
#     prev=i
# print(curr_streak)


    