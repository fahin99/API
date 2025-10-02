from flask import Flask, jsonify, request, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import json, os
import secrets

app = Flask(__name__)
active_tokens={} #token -> username
app.secret_key='supersecretkey'

DATA_FILE = 'users.json'
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        try:
            user = json.load(f)
        except json.JSONDecodeError:
            user = {}
else:
    user = {}
    
def override_http_method():
    if request.method=="POST":
        method=request.form.get("_method")
        if method:
            request.environ["REQUEST_METHOD"]=method.upper()

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
        html += f"""
        <li>
            {name}: Age {info['age']}
            <!-- Delete Form -->
            <form action="/users/{name}" method="post" style="display:inline;">
                <input type="hidden" name="_method" value="DELETE">
                <input type="submit" value="Delete">
            </form>

            <!-- Update Form -->
            <form action="/users/{name}" method="post" style="display:inline;">
                <input type="hidden" name="_method" value="PUT">
                <input type="number" name="age" placeholder="New Age">
                <input type="submit" value="Update">
            </form>
        </li>
        """
    html += "</ul><a href='/users'>Create New User</a>"
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
    username = request.form.get("username") or (request.json and request.json.get("username"))
    password = request.form.get("password") or (request.json and request.json.get("password"))

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if username in user:
        # generate token
        stored_pw=user[username].get("password")
        if stored_pw and check_password_hash(stored_pw, password):
            token = secrets.token_hex(16)  # random unique token
            active_tokens[token] = username  # store in dictionary

            if request.is_json or request.headers.get('Accept') == 'application/json':
                return redirect(url_for('dashboard', token=token))

            return f"<h2>Welcome {username}!</h2><p>Your token: {token}</p><a href='/secret?token={token}'>Go to Secret</a>"

    return jsonify({"error": "Invalid username or password"}), 401


@app.route("/login", methods=["GET"])
def login_form():
    return """
        <h2> Login</h2>
        <form action="/login" method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username"><br><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password"><br><br>
            <input type="submit" value="Login">
            <p><a href="/signup">New here? Signup</a></p>
        </form>
    """
@app.route("/secret",methods=['GET'])
def secret():
    auth_header=request.headers.get("Authorization") or request.args.get("token")
    if not auth_header:
        return {"status":"failed", "message":"missing token"}, 401

    if auth_header.startswith("token-"):
        token=auth_header[len("token-"):]
    else:
        return {"status":"failed", "message":"Invalid token format"}, 401
    if token in active_tokens:
        return {"status":"success", "message":f"Hello, {active_tokens[token]}! This is a secret message."}
    else:
        return {"status":"failed", "message":"Unauthorized"}, 401
    
@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username") or (request.json and request.json.get("username"))
    password = request.form.get("password") or (request.json and request.json.get("password"))
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    if username in user:
        return jsonify({"error": "Username already exists"}), 400
    hashed_password = generate_password_hash(password)
    user[username] = {"age": None, "password": hashed_password}
    save_data()
    return jsonify({"message": "User created successfully"}), 201  
    
@app.route('/signup', methods=['GET'])
def signup_form():
    return """
        <h2> Signup</h2>
        <form action="/signup" method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username"><br><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password"><br><br>
            <input type="submit" value="Signup">
        </form>
        <a href="/login">Already have an account? Login here</a>
    """

@app.route("/dashboard")
def dashboard():
    token=request.args.get("token")
    if token in active_tokens:
        username=active_tokens[token]
        return f"""
            <h2>Welcome to your dashboard, {username}!</h2>
            <p>This is a protected area.</p>
            <a href="/secret?token={token}">Go to Secret</a><br>
            <a href="/users/all">View All Users</a><br>
            <a href="/logout?token={token}">Logout</a>
        """
    return redirect(url_for('login_form'))

@app.route("/logout")
def logout():
    token=request.args.get("token")
    if token in active_tokens:
        del active_tokens[token]
        return redirect(url_for('login_form'))
    return redirect(url_for('dashboard'))
        
if __name__ == "__main__":
    app.run(debug=True)
