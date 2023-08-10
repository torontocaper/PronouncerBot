import json
import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, request
from slack_sdk import WebClient

# get the bot token for authentication and fire up the slack client
load_dotenv()
bot_token = os.getenv("BOT_USER_TOKEN")
client = WebClient(token=bot_token)
# headers = {"Authorization": "Bearer " + bot_token}

# Load JSON data from file
with open("Python/pronouncers.json", "r") as json_file:
    pronouncer_data = json.load(json_file)

app = Flask(__name__)

event_cache = []
print(f"{datetime.now()}: Current event cache: {event_cache}.")

@app.route("/", methods=["POST"])
def handle_slack_event():
    request_data = request.get_json()

    print(f"{datetime.now()}: Request received. Starting event handler.")

    if "challenge" in request_data:
        challenge_key = request_data["challenge"]
        print(f"{datetime.now()}: This is an authentication challenge from Slack. The challenge key is {challenge_key}")
        return challenge_key
    
    else:
        # event_context = request_data["event_context"]
        # event_time = request_data["event_time"]
        # print(f"{datetime.now()}: Outer event info: Context: {event_context}; Event Time: {event_time}")

        event_id = request_data["event_id"]
        event_data = request_data["event"]
        user_id = event_data["user"]
        reaction_type = event_data["reaction"]
        item_data = event_data["item"]
        channel_id = item_data["channel"]
        timestamp = item_data["ts"]      
    
        # print(f"{datetime.now()}: Inner event info: Event: {event_id}; User: {user_id}; Reaction: {reaction_type}; Channel: {channel_id}; Timestamp: {timestamp}.")

        if event_id in event_cache:
            print(f"{datetime.now()}: Event {event_id} has already been processed. Exiting event handler.")
            return "OK"

        else: 
            print(f"{datetime.now()}: Event {event_id} has not been processed. Starting event processing.")
            event_cache.append(event_id)

            # if the emoji is anything other than :pronounce:, bail
            if reaction_type != "pronounce":
                print(f"{datetime.now()}: Reaction was of type :{reaction_type}:. Exiting event handler.")
                return "OK"
            else:
                conversation = client.conversations_replies(
                    channel=channel_id,
                    ts=timestamp
                    )
                messages = conversation.get("messages")
                message_text = messages[0]["text"]
                client.chat_postMessage(
                    channel=channel_id,
                    thread_ts=timestamp,
                    text=f"Hey <@{user_id}>, thanks for calling PronouncerBot. I'll look for a pronouncer for {message_text}."
                    )

                # search the database for the message text
                matches = []
                for entry in pronouncer_data:
                    if message_text.lower() in entry["Title"].lower():
                       matches.append(entry)

                # if no matches are found
                if len(matches) == 0:
                    client.chat_postMessage(
                        channel=channel_id,
                        thread_ts=timestamp,
                        text=f"No matches. Sorry!"
                        )
                
                # if one match is found
                elif len(matches) == 1:
                    client.chat_postMessage(channel=channel_id, thread_ts=timestamp, text=f"I found a match!")
                    title = matches[0]["Title"]
                    pronouncer = matches[0]["Pronouncer"]
                    client.chat_postMessage(
                        channel=channel_id,
                        thread_ts=timestamp,
                        text=f"{title} - {pronouncer}."
                        )

                # if several matches are found
                else:
                    client.chat_postMessage(
                        channel=channel_id,
                        thread_ts=timestamp,
                        text=f"I found {len(matches)} potential matches!"
                        ) 
                    for match in matches:
                        title = match["Title"]
                        pronouncer = match["Pronouncer"]
                        client.chat_postMessage(
                            channel=channel_id,
                            thread_ts=timestamp,
                            text=f"{title} - {pronouncer}."
                            )

                return "OK"

# format the message using blocks
def send_simple_message(channel_id, timestamp):
    message = ""
    client.chat_postMessage(
        channel=channel_id,
        thread_ts=timestamp,
        text=message
    )
    return "OK"

def format_block():
    pass

def add_pronouncer():
    # add a json-formatted object to the main database
    pass

if __name__ == '__main__':
    app.run(debug=True)