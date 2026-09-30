import json
import random
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

QUOTES_FILE = BASE_DIR / "data" / "quotes.json"
HISTORY_FILE = BASE_DIR / "data" / "history.json"


def load_quotes():
    with open(QUOTES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def load_history():
    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            history,
            file,
            indent=4,
            ensure_ascii=False
        )


def get_random_quote():
    quotes = load_quotes()
    history = load_history()

    if not quotes:
        raise ValueError("No quotes available.")

    unused_quotes = [
        quote for quote in quotes
        if quote["text"] not in history
    ]

    if not unused_quotes:
        history = []

        unused_quotes = quotes

    selected_quote = random.choice(unused_quotes)

    return selected_quote


def mark_quote_as_used(quote):
    history = load_history()

    if quote["text"] not in history:
        history.append(quote["text"])

    save_history(history)


if __name__ == "__main__":
    quote = get_random_quote()

    print(f'"{quote["text"]}"')
    print(f'— {quote["author"]}')