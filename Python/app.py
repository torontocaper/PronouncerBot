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
    print(f"{datetime.now()}: Request received. Starting event handler.")

    if "payload" in request.form:
        print(f"{datetime.now()}: Payload received.")
        payload = json.loads(request.form["payload"])
        print(payload)
        trigger_id = payload["trigger_id"]
        
        if payload["type"] == "shortcut":
            print(f"{datetime.now()}: Shortcut invoked. Opening modal.")
            client.views_open(
                trigger_id=trigger_id,
                view={
                    "type": "modal",
                    "title": {"type": "plain_text", "text": "Add a pronouncer"},
                    "submit": {"type": "plain_text", "text": "Submit"},
                    "callback_id": "submit_pronouncer",
                    "blocks": [
                        {
                            "type": "input",
                            "element": {
                                "type": "plain_text_input",
                                "action_id": "pronouncer_title",
                            },
                            "label": {
                                "type": "plain_text",
                                "text": "Title"
                            }
                        },
                        {
                            "type": "input",
                            "element": {
                                "type": "plain_text_input",
                                "action_id": "pronouncer_pronouncer",
                            },
                            "label": {
                                "type": "plain_text",
                                "text": "Pronouncer"
                            }
                        },
                        {
                            "type": "input",
                            "element": {
                                "type": "plain_text_input",
                                "action_id": "pronouncer_description",
                            },
                            "label": {
                                "type": "plain_text",
                                "text": "Description (optional)"
                            }
                        }
                    ]
                }           
            )
            return "OK"

        elif payload["type"] == "view_submission":
            print(f"{datetime.now()}: Submission received. Processing input.")
            view_id = payload["view"]["id"]
            client.views_update(
                token=bot_token,
                view={
                    "type": "modal",
                    "title": {"type": "plain_text", "text": "Add a pronouncer"},
                    "blocks": [
                        {
			            "type": "section",
			            "text": {
				            "type": "plain_text",
				            "text": "Thanks for the submission! You can close this box."
                            }
		                }
                    ]
                },
                view_id=view_id
            )

            values = payload["view"]["state"]["values"]
            
            for key, info in values.items():
                print(f"Random key: {key}\nInfo: {info}")
                if "pronouncer_title" in info:
                    new_title = info["pronouncer_title"]["value"]
                elif "pronouncer_pronouncer" in info:
                    new_pronouncer = info["pronouncer_pronouncer"]["value"]
                elif "pronouncer_description" in info:
                    new_description = info["pronouncer_description"]["value"]
            
            print(f"{new_title} - {new_pronouncer} ({new_description})")

            return "OK"
      
        else:
            return "OK"

    request_data = request.get_json()

    if "challenge" in request_data:
        challenge_key = request_data["challenge"]
        print(f"{datetime.now()}: This is an authentication challenge from Slack. Returning challenge key.")
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
                handle_pronouncer_request(channel_id, timestamp, user_id)
                
                return "OK"

def handle_pronouncer_request(channel_id, timestamp, user_id):
    conversation = client.conversations_replies(
        channel=channel_id,
        ts=timestamp
        )
    messages = conversation.get("messages")
    message_text = messages[0]["text"]
    client.chat_postMessage(
        channel=channel_id,
        thread_ts=timestamp,
        text=f"Hey <@{user_id}>, thanks for calling PronouncerBot. I'll look for a pronouncer for \"{message_text}\"."
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
    elif len(matches) <= 10:
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

    # if too many matches are found
    else: 
        client.chat_postMessage(
            channel=channel_id,
            thread_ts=timestamp,
            text=f"I found more than 10 potential matches. Please try again (but be more specific)!"
            )


if __name__ == '__main__':
    app.run(debug=True)