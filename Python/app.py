import os

from dotenv import load_dotenv
from flask import Flask, request

# get bot token from .env
load_dotenv()
bot_token = os.getenv("BOT_USER_TOKEN")

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handle_slack_event():
    request_data = request.get_json()

    if "challenge" in request_data:
        challenge_key = request_data["challenge"]
        return challenge_key

if __name__ == '__main__':
    app.run(debug=True)