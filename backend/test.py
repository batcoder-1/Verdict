import requests
from models import leetcodeStats
handle="?handles=k_ni_ght"
api="https://codeforces.com/api/user.rating?handle=k_ni_ght"
res=requests.get(api)
contest=res.json()
for i in contest["result"]:
    print(i)
    