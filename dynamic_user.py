from flask import Flask, jsonify, request
import json, os
import secrets

app = Flask(__name__)
active_tokens={} #token -> username

DATA_FILE = 'users.json'
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        try:
            user = json.load(f)
        except json.JSONDecodeError:
            user = {}
else:
    user = {}

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(user, f, indent=4)
        
def validate_user(name, age):
    if not name or not name.strip():
        return {"error": "Name cannot be empty"}, 400
    if not age:
        return {"error": "Age must be taken input"}, 400
    try:
        age = int(age)
        if age <= 0:
            return {"error": "Age must be a positive integer"}, 400
    except ValueError:
        return {"error": "Age must be a valid integer"}, 400
    
    return None, age
        
def validate_name(name):
    if not name or not name.strip():
        return {"error": "Name cannot be empty"}, 400
    return None

@app.route('/users', methods=["POST"])
def users():
    name=request.form.get("name") or (request.json and request.json.get("name"))
    age=request.form.get("age") or (request.json and request.json.get("age"))
    error, age = validate_user(name, age)
    if error:
        return jsonify(error), 400
    elif name in user:
        return jsonify({"error": f"User {name} already exists"}), 400
    user[name] = {"age": age}
    save_data()
    if request.is_json or request.headers.get('Accept') == 'application/json':
        return jsonify({
                "message": "User created successfully", 
                name: user[name]
                }), 201
    return f"""
        <h2>User created successfully</h2>
        <p>Name: {name}</p>
        <p>Age: {age}</p>
        <a href="/users/all">View All Users</a>
    """, 201
    
#addition: updating name
@app.route('/users/<name>', methods=['PUT'])
def update_user(name):
    if name not in user:
        return jsonify({"error": f"User {name} not found"}), 404
    age = request.json.get("age")
    error, age = validate_user(name, age)
    if error:
        return jsonify(error), 400
    user[name] = {"age": age}
    save_data()
    if request.is_json or request.headers.get('Accept') == 'application/json':
        return jsonify({
            "message": "User updated successfully",
            name: user[name]
        }), 200
    return f"""
        <h2>User updated successfully</h2>
        <p>Name: {name}</p>
        <p>Age: {age}</p>
        <a href="/users/all">View All Users</a>
    """, 200

#addition: deleting user
@app.route('/users/<name>', methods=['DELETE'])
def delete_user(name):
    error=validate_name(name)
    if error:
        return jsonify(error), 400
    if name not in user:
        return jsonify({"error": f"User {name} not found"}), 404
    del user[name]
    save_data()
    if request.is_json or request.headers.get('Accept') == 'application/json':
        return jsonify({"message": "User deleted successfully"}), 200
    return f"""
        <h2>User deleted successfully</h2>
        <a href="/users/all">View All Users</a>
    """, 200

@app.route('/users/all', methods=['GET'])
def get_all_users():
    if request.is_json or request.headers.get('Accept') == 'application/json':
        return jsonify(user), 200
    html = "<h2>All Users</h2><ul>"
    for name, info in user.items():
        html += f"<li>{name}: Age: {info['age']}</li>"
    html += "</ul>"
    return html

#addition: get a user
@app.route('/users/<name>', methods=['GET'])
def get_user(name):
    error=validate_name(name)
    if error:
        return jsonify(error), 400
    if name not in user:
        return jsonify({"error": f"User {name} not found"}), 404
    if request.is_json or request.headers.get('Accept') == 'application/json':
        return jsonify(user[name]), 200
    return f"""
        <h2>User {name}</h2>
        <p>Age: {user[name]['age']}</p>
        <a href="/users/all">View All Users</a>
    """, 200
    
@app.route('/search', methods=['GET'])
def search_form():
    return """
        <h2>Search for a user</h2>
        <form action="/search/result" method="get">
            <label for="name">Enter name:</label>
            <input type="text" id="name" name="name">
            <input type="submit" value="Search">
        </form>
        <a href="/users/all">View All Users</a>
    """
@app.route('/search/result', methods=['GET'])
def search_result():
    name = request.args.get("name")
    error = validate_name(name)
    if error:
        return jsonify(error), 400

    if name not in user:
        return f"<h2>User {name} not found</h2><a href='/search'>Search again</a>", 404
    
    return f"""
        <h2>User {name}</h2>
        <p>Age: {user[name]['age']}</p>
        <a href="/search">Search again</a> |
        <a href="/users/all">View All Users</a>
    """

@app.route("/login", methods=["POST"])
def login():
    data=request.json
    username=data.get("username")
    password=data.get("password")
    
    if not username or not password:
        return {"status": "failed", "message": "Username and password are required"}, 400
    elif username in user and user[username]==password:
        token=secrets.token_hex(16)
        active_tokens[token]=username

        return {"status": "success", "message": "Login successful", "token":token}
    
    else:
        return {"status": "failed", "message": "Invalid username or password"}, 401

if __name__ == "__main__":
    app.run(debug=True)
