Cat themed Slack bot which has cute cats and random stuff no one actually needs (also quacking ducks)!

## Features
- Saves humanity
- Meow button (if you press it it will reply with a random cat-like word in a thread)
- Catifier which turns all your text to cute cat-like lang.
- Cat pictures and reactions when you say meow or any cat-like word and duck pictures/reactions when you say quack/duck-like words!
- https://http.cat command which returns the image for the status code, and also replies to any message containing any valid status code with the cat image!
- Welcome message when you mention the bot!
- Cat facts
- Cat-like AI when DMed

## How to run
- Download source code from this repo
- Install requirements
  - Use uv and run `uv sync`
OR
  - Install Python >=3.11
  - Create a venv with `python3 -m venv .venv`
  - Activate it: `source .venv/bin/activate`
  - Install requirements: `pip3 install -r requirements.txt`
- Move `.env.example` to `.env` and update the example values inside.
- Update `constants.py` if you want to change any default values.
- Run with `uv run app.py` or `python3 app.py` depending on the environment