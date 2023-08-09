import os

from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, request

# get bot token from .env
load_dotenv()
bot_token = os.getenv("BOT_USER_TOKEN")

app = Flask(__name__)

challenge_key = ""
event_cache = []
print(f"{datetime.now()}: Current event cache: {event_cache}.")

@app.route("/", methods=["POST"])
def handle_slack_event():
    request_data = request.get_json()

    print(f"{datetime.now()}: Request received. Starting event handler.")

    if "challenge" in request_data:
        print(f"{datetime.now()}: This is an authentication challenge from Slack. The challenge key is {challenge_key}")
        challenge_key = request_data["challenge"]
        return challenge_key
    
    else:
        event_context = request_data["event_context"]
        event_time = request_data["event_time"]
        print(f"{datetime.now()}: Outer event info: Context: {event_context}; Event Time: {event_time}")

        event_id = request_data["event_id"]

        event_data = request_data["event"]
        user_id = event_data["user"]
        reaction_type = event_data["reaction"]
        
        item_data = event_data["item"]
        channel_id = item_data["channel"]
        timestamp = item_data["ts"]      
    
        print(f"{datetime.now()}: Inner event info: Event: {event_id}; User: {user_id}; Reaction: {reaction_type}; Channel: {channel_id}; Timestamp: {timestamp}.")

        return "OK"

if __name__ == '__main__':
    app.run(debug=True)