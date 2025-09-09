from flask import Flask, jsonify, request
import json, os

app = Flask(__name__)

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

@app.route('/users', methods=["POST"])
def users():
    name=request.form.get("name") or (request.json and request.json.get("name"))
    age=request.form.get("age") or (request.json and request.json.get("age"))
    if not name or not age:
        return jsonify({"error": "Name and age are required"}), 400
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
    if not age:
        return jsonify({"error": "Age is required"}), 400
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
    html ="<h2>All Users</h2><ul>"
    for name, info in user.items():
        html += f"<li>{name}: Age: {info['age']}</li>"
    html += "</ul>"
    return html

if __name__ == "__main__":
    app.run(debug=True)
