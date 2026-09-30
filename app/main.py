from quote_manager import get_random_quote
from poster_generator import create_poster


def main():

    print("Starting Daily Motivation...")

    quote = get_random_quote()

    print()
    print("Selected quote:")
    print(f'"{quote["text"]}"')
    print(f'— {quote["author"]}')
    print()

    poster_path = create_poster(quote)

    print(f"Poster created: {poster_path}")


if __name__ == "__main__":
    main()