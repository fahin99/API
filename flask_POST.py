from flask import Flask, jsonify, request

app=Flask(__name__)

@app.route("/", methods=["POST"])
def home():
    data = request.get_json()
    name = data.get("name", "Guest")
    age = data.get("age", "unknown")
    return jsonify({
        "message": f"Hello, {name}! You are {age} years old."
    })

if __name__ == "__main__":
    app.run(debug=True)
