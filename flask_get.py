from flask import Flask, jsonify, request

app= Flask(__name__)

@app.route("/")
def home():
     name = request.args.get("name", "Guest")
     age = request.args.get("age", "unknown")
     return f"Hello, {name}! You are {age} years old."

if __name__ == "__main__":
    app.run(debug=True)
