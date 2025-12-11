import os, requests, random
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

MEOW_PHRASES = [
    ":3", ">:3", ":3c", ">:3c", ">:^3",
    "meow", "mew", "meww", "mrrp", "mrrrp", "mrp", "mrrrow",
    "purr", "prr", "prrr", "brrrp",
    "nya", "nyan", "nyaa", "nyaaa", "nyanyanya", "nya~", "nya!",
    "neko", "nekochan",
    "owo", "uwu", "qwq", ">w<", "^_^",
    "=^.^=", "(=^･^=)",
    "*meow*", "*purr*", "*mrrp*", "*nya*",
    "chirp", "eep",
    "nyoom",
    "rawr"
]

QUACK_PHRASES = ["quack", "duck", "gizzy"]

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

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
def meow_action(ack, say):
    ack()
    say(text=random.choice(MEOW_PHRASES))

@app.command("/meow")
def meow(ack, say):
    ack()
    say(
        text="Meow! :3",
        blocks=[
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
    )

@app.command("/quack")
def quack(ack, say):
    ack()
    say(
        text="Quack! :3",
        blocks=[
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

@app.event("message")
def message_handler(body, say):
    message_text = body.get('event', {}).get('text', '').lower()
    if any([phrase in message_text.lower().split() for phrase in MEOW_PHRASES]):
        say(
            text="Meow! :3",
            blocks=[
                {
                    "type": "image",
                    "title": {
                        "type": "plain_text",
                        "text": "Meow!"
                    },
                    "block_id": "image4",
                    "image_url": requests.get("https://cataas.com/cat/cute/says/Meow?json=true").json()["url"] ,
                    "alt_text": ":3"
                }
            ]
        )
    elif any([phrase in message_text.lower().split() for phrase in QUACK_PHRASES]):
        say(
            text="Quack! :3",
            blocks=[
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
        )

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
