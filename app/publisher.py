from pathlib import Path


def publish_to_facebook(poster_path, quote):
    """
    Placeholder for Facebook publishing.

    For now, this only verifies that the poster exists
    and prepares the information that will eventually
    be sent to Facebook.
    """

    poster_path = Path(poster_path)

    if not poster_path.exists():
        raise FileNotFoundError(
            f"Poster not found: {poster_path}"
        )

    caption = (
        f'"{quote["text"]}"\n\n'
        f"— {quote['author']}\n\n"
        "#DailyMotivation #Motivation #DailyQuote"
    )

    print("================================")
    print("FACEBOOK PUBLISHER")
    print("================================")
    print(f"Poster: {poster_path}")
    print()
    print("Caption:")
    print(caption)
    print()
    print("Facebook publishing is not connected yet.")
    print("Poster is ready for publishing.")
    print("================================")

    return True