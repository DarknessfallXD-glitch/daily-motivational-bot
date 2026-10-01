
import os
from pathlib import Path

import requests


def publish_to_facebook(poster_path, quote):
    """
    Publish a poster to a Facebook Page.

    Required environment variables:
      FACEBOOK_PAGE_ID
      FACEBOOK_PAGE_ACCESS_TOKEN
      FACEBOOK_GRAPH_API_VERSION
    """

    poster_path = Path(poster_path)

    if not poster_path.is_file():
        raise FileNotFoundError(f"Poster not found: {poster_path}")

    page_id = os.getenv("FACEBOOK_PAGE_ID")
    access_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
    api_version = os.getenv("FACEBOOK_GRAPH_API_VERSION")

    missing = [
        name
        for name, value in {
            "FACEBOOK_PAGE_ID": page_id,
            "FACEBOOK_PAGE_ACCESS_TOKEN": access_token,
            "FACEBOOK_GRAPH_API_VERSION": api_version,
        }.items()
        if not value
    ]

    if missing:
        print("Facebook publishing is not configured.")
        print("Missing environment variable(s): " + ", ".join(missing))
        return False

    caption = (
        f'"{quote["text"]}"\n\n'
        f"— {quote['author']}\n\n"
        "#DailyMotivation #Motivation #DailyQuote"
    )

    url = f"https://graph.facebook.com/{api_version}/{page_id}/photos"

    try:
        with poster_path.open("rb") as image_file:
            response = requests.post(
                url,
                data={
                    "access_token": access_token,
                    "caption": caption,
                },
                files={
                    "source": (
                        poster_path.name,
                        image_file,
                        "image/png",
                    )
                },
                timeout=60,
            )

        try:
            result = response.json()
        except ValueError:
            print("Facebook returned an unreadable response.")
            return False

        if not response.ok or "id" not in result:
            error = result.get("error", {})
            print("Facebook publishing failed.")
            print("Error:", error.get("message", "Unknown API error"))
            return False

        print("Facebook post created successfully.")
        print("Post ID:", result["id"])
        return True

    except requests.RequestException:
        print("Could not connect to Facebook. Check your connection and try again.")
        return False