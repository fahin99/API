import requests

url="http://127.0.0.1:5000/profile"
# test get
response_get=requests.get(url,params={"name":"Alice","age":30})
print("GET response: ", response_get.json())
# test post
response_post=requests.post(url,json={"name":"Bob","age":25})
print("POST response: ", response_post.json())