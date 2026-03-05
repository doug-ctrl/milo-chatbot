from flask import Flask, render_template, request, jsonify
from bot import get_milo_response, user_name

app = Flask(__name__)


# The "Home" page route
@app.route('/')
def index():
    return render_template('index.html', user=user_name)


# The "Logic" route - where the chat messages go
@app.route('/get_response', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"response": "I didn't hear anything!"})

    # Calling your existing bot logic!
    bot_reply = get_milo_response(user_input)
    return jsonify({"response": bot_reply})

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    # Setting debug=True lets the server restart automatically when you save changes
    app.run(debug=True, port=5001)