import json 

name=input("Enter your name: ")
age=int(input("Enter your age: "))
print(f"\nHello {name}, you are {age} years old.")
person ={
    "name": name,
    "age": age,
    "skills": ["Python", "C++", "Problem-Solving"]
}

with open("person.json", "w") as json_file:
    json.dump(person, json_file, indent=4)
    
print("\nData has been written to person.json")

with open("person.json", "r") as json_file:
    load_person = json.load(json_file)

print("Loaded data from JSON file:\n")
print(load_person)