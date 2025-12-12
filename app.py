import os, requests, random, http, re, dotenv

from constants import *

from openrouter import OpenRouter
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

dotenv.load_dotenv(".env")

openrouter_client = OpenRouter(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    server_url=os.getenv("OPENROUTER_URL"),
)

def catify_text(text):
    text = text.lower()
    
    text = re.sub(r'[rl]', 'w', text)
    text = re.sub(r'na', 'nya', text)
    text = re.sub(r'tion\b', 'shun', text)
    text = re.sub(r'th', 'd', text)
    text = re.sub(r'ou', 'uw', text)
    text = re.sub(r'ove', 'uv', text)
    text = re.sub(r'!+', ' nya~ >w<', text)
    text = re.sub(r'\?+', ' nyaaaa?', text)
    
    if not re.search(r'nya|mew|meow|uwu|owo', text):
        text += ' nya~'

    return text

app = App(token=os.environ.get("BOT_TOKEN"))

def generate_httpcat_blocks(status_code):
    return [
        {
            "type": "image",
            "title": {
                "type": "plain_text",
                "text": f"CAT {status_code} {http.HTTPStatus(status_code).phrase} :3"
            },
            "block_id": "image4",
            "image_url": f"https://http.cat/{status_code}",
            "alt_text": ":3"
        }
    ]

def generate_meow_blocks():
    return [
        {
            "type": "image",
            "title": {
                "type": "plain_text",
                "text": "Meow!"
            },
            "block_id": "image4",
            "image_url": "https://cataas.com/cat/cute/says/Meow",
            "alt_text": ":3"
        }
    ]

def generate_quack_blocks():
    return [
        {
            "type": "image",
            "title": {
                "type": "plain_text",
                "text": "Quack!"
            },
            "block_id": "image4",
            "image_url": requests.get("https://random-d.uk/api/quack").json()["url"],
            "alt_text": ":3"
        }
    ]

@app.command("/catify")
def catify(ack, say, command):
    text = command.get("text", "")
    user = command["user_id"]

    ack()

    say(
        text=f"<@{user}> said " + catify_text(text), mrkdwn=False
    )

@app.command("/meow_button")
def meow_button(ack, say):
    ack()

    say(
        text="Meow! :3",
        blocks=[
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Click me :3"},
                        "action_id": "meow_button",
                        "value": "meow"
                    }
                ]
            }
        ]
    )

@app.action("meow_button")
def meow_action(ack, say, body):
    ack()
    
    ts = body["message"].get("thread_ts", body["message"]["ts"])
    
    say(text=random.choice(MEOW_PHRASES), thread_ts=ts, mrkdwn=False)

@app.command("/meow")
def meow(ack, say):
    ack()

    say(
        text="Meow! :3",
        blocks=generate_meow_blocks()
    )

@app.command("/cat_gif")
def cat_gif(ack, say):
    ack()

    say(
        text="Coming soon! nyanyanya"
    )

@app.command("/httpcat")
def httpcat(ack, say, respond, command):
    ack()
    
    text = command.get("text", "")
    if text:
        if not text.isnumeric():
            respond("Status Code must be numeral! >:3")
            return

        status_code = int(text)

        if status_code not in http_cat_codes:
            respond("This is either an invalid HTTP status code or not available on http.cat >:3")
            return
        
    say(
        text=f"CAT {status_code} {http.HTTPStatus(status_code).phrase} :3",
        blocks=generate_httpcat_blocks(status_code)
    )

@app.command("/quack")
def quack(ack, say):
    ack()
    say(
        text="Quack! :3",
        blocks=generate_quack_blocks()
    )

@app.command("/cat_fact")
def cat_fact(ack, say):
    ack()
    fact = requests.get("https://catfact.ninja/fact").json()["fact"]
    say(
        text="Cat Fact: " + fact,
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Cat Fact: " + fact
                },
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "New fact"},
                    "action_id": "cat_fact_button",
                    "value": "meow"
                }
            }
        ]
    )

@app.action("cat_fact_button")
def cat_fact_button(ack, respond):
    ack()
    fact = requests.get("https://catfact.ninja/fact").json()["fact"]
    respond(
        replace_original=True,
        text="Cat Fact: " + fact,
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Cat Fact: " + fact
                },
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "New fact"},
                    "action_id": "cat_fact_button",
                    "value": "meow"
                }
            }
        ]
    )

@app.event("app_mention")
def mention(body, say):
    thread_ts = body['event']['ts']
    say(text=WELCOME_MESSAGE, thread_ts=thread_ts)

@app.event("message")
def message_handler(event, say, client, message):
    ts = event.get('ts')
    message_text = event.get('text', '').lower()
    channel_id = message["channel"]
    message_ts = message["ts"]

    if event.get("channel_type") == "im" and "bot_id" not in event:
        messages = [{"role": "system", "content": AI_SYSTEM_PROMPT}]
        messages.extend([{"role": "assistant" if "bot_id" in msg else "user", "content": msg.get("text", "")} for msg in client.conversations_history(channel=channel_id, limit=AI_CONTEXT_MSG_LIMIT).get("messages", [])])
        messages.append({"role": "user", "content": message_text})

        response = openrouter_client.chat.send(
            model=os.getenv("OPENROUTER_MODEL"),
            messages=messages,
            stream=False,
        )

        say(response.choices[0].message.content)
        
        return

    found_status_codes = [status_code for status_code in http_cat_codes if str(status_code) in message_text.lower()]

    if any([phrase in message_text.lower().split() for phrase in MEOW_PHRASES]):
        say(
            text="Meow! :3",
            blocks=generate_meow_blocks(),
            thread_ts=ts
        )
        client.reactions_add(
            channel=channel_id,
            name=CAT_EMOJI,
            timestamp=message_ts
        )
    elif any([phrase in message_text.lower().split() for phrase in QUACK_PHRASES]):
        say(
            text="Quack! :3",
            blocks=generate_quack_blocks(),
            thread_ts=ts
        )
        
        client.reactions_add(
            channel=channel_id,
            name=DUCK_EMOJI,
            timestamp=message_ts
        )

    elif found_status_codes:
        status_code = int(found_status_codes[0])
        say(
            text=f"CAT {status_code} {http.HTTPStatus(status_code).phrase} :3",
            blocks=generate_httpcat_blocks(status_code),
            thread_ts=ts
        )
        
        client.reactions_add(
            channel=channel_id,
            name=CAT_EMOJI,
            timestamp=message_ts
        )

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["APP_TOKEN"]).start()
