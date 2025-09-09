import requests
url="http://127.0.0.1:5000/users"
headers = {"Content-Type": "application/json", "Accept": "application/json"}
running=True
while running:
    act=input("What do you want to do: ")
    if act=="create":
        name=input("Enter name: ")
        age=input("Enter age: ")
        # add a new user
        response_post=requests.post(url,json={"name":name,"age":age}, headers=headers)
        print("Post response: ", response_post.json())
    elif act=="update":
        name=input("Enter name: ")
        age=input("Enter the update age: ")
        #update the new user
        response_put=requests.put(f"{url}/{name}", json={"age": age}, headers=headers)
        print("Put response: ", response_put.json())

    elif act=="get":
        # retrieve a new user
        name=input("Enter name: ")
        response_get=requests.get(url,params={"name":name}, headers=headers)
        print("Get response: ", response_get.json())

    elif act=="delete":
        name=input("Enter name: ")
        #delete a new user
        response_del=requests.delete(f"{url}/{name}", headers=headers)
        print("Delete response: ", response_del.json())

    elif act=="list":
        #list all users
        response_list=requests.get(f"{url}/all", headers=headers)
        print("List response: ")
        for name, info in response_list.json().items():
            print(f"Name: {name}, Age: {info['age']}")
        
    elif act=="exit":
        running=False

    else:
        print("Please enter a valid action")