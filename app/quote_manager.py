import json
import random
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
QUOTES_FILE = BASE_DIR / "data" / "quotes.json"


def load_quotes():
    with open(QUOTES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_random_quote():
    quotes = load_quotes()

    if not quotes:
        raise ValueError("No quotes available.")

    return random.choice(quotes)


if __name__ == "__main__":
    quote = get_random_quote()

    print(f'"{quote["text"]}"')
    print(f'— {quote["author"]}')