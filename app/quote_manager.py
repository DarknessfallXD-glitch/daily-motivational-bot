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

    # Find quotes that have not been used yet
    unused_quotes = [
        quote for quote in quotes
        if quote["text"] not in history
    ]

    # If every quote has been used, start a new cycle
    if not unused_quotes:
        history = []
        unused_quotes = quotes

    # Select a random unused quote
    selected_quote = random.choice(unused_quotes)

    # Remember the selected quote
    history.append(selected_quote["text"])

    save_history(history)

    return selected_quote


if __name__ == "__main__":
    quote = get_random_quote()

    print(f'"{quote["text"]}"')
    print(f'— {quote["author"]}')