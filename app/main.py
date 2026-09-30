from quote_manager import get_random_quote, mark_quote_as_used
from poster_generator import create_poster
from publisher import publish_to_facebook


def main():
    print("Starting Daily Motivation...")
    print()

    # Get a quote
    quote = get_random_quote()

    print("Selected quote:")
    print(f'"{quote["text"]}"')
    print(f'— {quote["author"]}')
    print()

    # Generate poster
    poster_path = create_poster(quote)

    print(f"Poster created: {poster_path}")
    print()

    # Publish poster
    success = publish_to_facebook(
        poster_path,
        quote
    )

    # Only mark the quote as used after successful publishing
    if success:
        mark_quote_as_used(quote)
        print("Quote marked as used.")
    else:
        print("Publishing failed. Quote was NOT marked as used.")


if __name__ == "__main__":
    main()