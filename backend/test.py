import requests
handle="?handles=k_ni_ght"
api="https://codeforces.com/api/user.info"+handle+"&checkHistoricHandles=false"
res=requests.get(api)
data=res.json()
# print(type(data["result"][0]["rank"]))
print(data["status"])