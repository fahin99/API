from flask import Flask, jsonify, request

app = Flask(__name__)

user = {}


@app.route('/users', methods=["GET", "POST"])
def users():
    if request.method == "POST":
        name = request.json.get("name")
        age = request.json.get("age")
        if not name or not age:
            return jsonify({"error": "Name and age are required"}), 400
        user[name] = {"age": age}
        return jsonify({"message": "User created successfully", "user": user}), 201
    elif request.method == "GET":
        name = request.args.get("name")
        if not name:
            return jsonify({"error": "Name parameter is required"}), 400
        if name in user:
            return jsonify({name: user[name]}), 200
        else:
            return jsonify({"error": f"User {name} not found"}), 404
    return f"Unknown method: {request.method}", 404

#addition: updating name
@app.route('/users/<name>', methods=['PUT'])
def update_user(name):
    if name not in user:
        return jsonify({"error": f"User {name} not found"}), 404
    age = request.json.get("age")
    if not age:
        return jsonify({"error": "Age is required"}), 400
    user[name] = {"age": age}
    return jsonify({"message": "User updated successfully", "user": user[name]}), 200

@app.route('/users', methods=['DELETE'])
def delete_user():
    name=request.args.get("name")
    if not name:
        return jsonify({"error": "Name parameter is required"}), 400
    elif name in user:
        del user[name]
        return jsonify({"message": "User deleted successfully", "user": user}), 200
    else:
        return jsonify({"error": f"User {name} not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
