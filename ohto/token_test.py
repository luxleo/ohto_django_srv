import requests
import json
#INFO: jwt를 최초 획득하려면 username,password를 POST 메서드로 /accounts/token/ 으로 실어 보내면 된다.
JWT_TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY5MTc1MTI2LCJpYXQiOjE2NjkxNzMzMjYsImp0aSI6IjI3N2UyMjNmZmYzNDRiOGZiYzRjNDRmZDA0NTkzMTY5IiwidXNlcl9pZCI6MX0.vwZIfyjNhwY1c39esuUvEkVg9G-9WMCK9MjqS2eVegc"
)
REFRESH_TOKEN=(
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2OTIwODQ2NiwiaWF0IjoxNjY5MTIyMDY2LCJqdGkiOiI4YmYwNTUyYTU0NzI0YTA5YmUwMWY1Zjg5ZjA2ZDE1NSIsInVzZXJfaWQiOjF9.mAzdgrPtI_LYW7VW21nggwlTeovlfdSJU8Dg86RaQcw"
)
headers={
    'Content-Type': 'application/json; charset=utf-8',
    "Authorization": f"Bearer {JWT_TOKEN}"
}

#INFO: jwt 얻고 난 후에는 jwt를 header에 담아 인증한다.    data=json.dumps({"title":" python","desc":"simple desc","tags":""}))
res = requests.get("http://localhost:8000/playlist/17/get_songs/",headers=headers,)
print(res.json())
#INFO: jwt만료 되고나면 refresh token을 /accounts/token/refresh/ 로 data에 담아 넘겨 갱신한다.
      #logout시 storage에서 token날린다.