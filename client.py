import requests
url="http://127.0.0.1:5000/users"
name=input("Enter name: ")
age=input("Enter age: ")
# add a new user
response_post=requests.post(url,json={"name":name,"age":age})
print("Post response: ", response_post.json())

#update the new user
response_put=requests.put(f"{url}/{name}", json={"age": 20})
print("Put response: ", response_put.json())

# retrieve a new user
response_get=requests.get(url,params={"name":name})
print("Get response: ", response_get.json())
