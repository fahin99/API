from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        # data = request.get_json()
        name=request.json.get('name',"Guest")
        age=request.json.get('age',"unknown")
        return jsonify({"message": f"Profile created for {name}, age {age}, from POST"})
    if request.method == 'GET':
        name=request.args.get('name',"Guest")
        age=request.args.get('age',"unknown")
        return jsonify({"message": f"Profile retrieved for {name}, age {age}, from GET"})
if __name__ == '__main__':
    app.run(debug=True)
