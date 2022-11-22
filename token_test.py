import requests
import json
#INFO: jwt를 최초 획득하려면 username,password를 POST 메서드로 /accounts/token/ 으로 실어 보내면 된다.
JWT_TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY5MDg5NzExLCJpYXQiOjE2NjkwODc5MTEsImp0aSI6IjQ0Zjc1YmI3NTc3ZjQzNjdhMWJjMDIxZTE3NzNhNWE0IiwidXNlcl9pZCI6MX0.6Q0jf0wlEmCkMlINneuMFrlO_uaZ8yYiGXsfuumYfoE"
)
REFRESH_TOKEN=(
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2OTE3NDMxMSwiaWF0IjoxNjY5MDg3OTExLCJqdGkiOiJmNWVlMTI2ZmFlNmU0MGExYmQxM2Q1Y2NlNmU0YjU2YyIsInVzZXJfaWQiOjF9.t0fJMlKi0MOL917c4qMbru0vi6FRV4ZfDfNomYIN6Yg"
)
headers={
    'Content-Type': 'application/json; charset=utf-8',
    "Authorization": f"Bearer {JWT_TOKEN}"
}

#INFO: jwt 얻고 난 후에는 jwt를 header에 담아 인증한다.    
res = requests.post("http://localhost:8000/playlist/",headers=headers,data=json.dumps({"title":"fire python","desc":"simple desc","cover_img":None,"tags":""}))
print(res.json())
#INFO: jwt만료 되고나면 refresh token을 /accounts/token/refresh/ 로 data에 담아 넘겨 갱신한다.
      #logout시 storage에서 token날린다.