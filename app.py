from flask import Flask, render_template, request, jsonify
from bot import get_milo_response, user_name
import os

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

import os

if __name__ == "__main__":
    # Render provides the PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    # host='0.0.0.0' is REQUIRED for Render to see the app
    app.run(host='0.0.0.0', port=port)