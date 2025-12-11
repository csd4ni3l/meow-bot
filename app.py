import os, requests, random, http
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

MEOW_PHRASES = [
    ":3", ">:3",
    "meow", "mew", "meww", "mrrp", "mrrrp", "mrp", "mrrrow",
    "purr", "prr", "prrr",
    "nya", "nyan", "nyaa", "nyaaa", "nyanyanya", "nya~", "nya!",
    "owo", "uwu", "qwq", ">w<", "^_^",
    "=^.^=", "(=^･^=)",
    "*meow*", "*purr*", "*mrrp*", "*nya*",
    "chirp", "eep",
    "nyoom", "rawr",
    "cat"
]

CAT_EMOJI = "cat"
DUCK_EMOJI = "duck"

QUACK_PHRASES = ["quack", "duck"]

WELCOME_MESSAGE = """
mrrrp… hiii :3
*arches back, tail wiggle*

meow-meow, nyaaa~ I bring u cozy purrs and tiny toe-beans of chaos >:3c
sniff sniff… u smell like someone who needs a soft head-bonk *bonk*

mew! I shall now sit on your keyboard for maximum inconvenience
"""

http_cat_codes = [
    100, 101, 102, 103,
    200, 201, 202, 203, 204, 205, 206, 207, 208, 214, 226,
    300, 301, 302, 303, 304, 305, 307, 308,
    400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415,
    416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 428, 429, 431, 444, 450,
    451, 495, 496, 497, 498, 499,
    500, 501, 502, 503, 504, 506, 507, 508, 509, 510, 511, 521, 522, 523, 525, 530,
    599
]

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

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

@app.command("/meow_translate")
def meow_translate(ack, say, command):
    text = command.get("text", "")
    user = command["user_id"]
    ack()
    say(
        text=f"<@{user}> said " + " ".join([random.choice(MEOW_PHRASES) for _ in range(len(text.split(" ")))], mrkdown=False)
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
    ts = body["message"].get("thread_ts", body["message"]["ts"])
    ack()
    say(text=random.choice(MEOW_PHRASES), thread_ts=ts, mrkdown=False)

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
        say(WELCOME_MESSAGE)
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
        status_code = found_status_codes[0]
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
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
