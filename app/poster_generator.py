from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import textwrap
import json
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
FONT_DIR = BASE_DIR / "fonts"
CONFIG_FILE = BASE_DIR / "config.json"

REGULAR_FONT = FONT_DIR / "DejaVuSans.ttf"
BOLD_FONT = FONT_DIR / "DejaVuSans-Bold.ttf"


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def load_font(path, size):
    return ImageFont.truetype(str(path), size)


def create_poster(quote):

    # --------------------------------------------------
    # 1. Load configuration
    # --------------------------------------------------

    config = load_config()
    poster_config = config["poster"]

    width = poster_config["width"]
    height = poster_config["height"]

    background_color = tuple(poster_config["background_color"])
    accent_color = tuple(poster_config["accent_color"])
    quote_color = tuple(poster_config["quote_color"])
    author_color = tuple(poster_config["author_color"])
    footer_color = tuple(poster_config["footer_color"])

    brand_name = config["brand_name"]
    footer_text = config["footer_text"]

    # --------------------------------------------------
    # 2. Check fonts
    # --------------------------------------------------

    print("Font directory:", FONT_DIR)
    print("Regular font exists:", REGULAR_FONT.exists())
    print("Bold font exists:", BOLD_FONT.exists())

    if not REGULAR_FONT.exists():
        raise FileNotFoundError(
            f"Regular font not found: {REGULAR_FONT}"
        )

    if not BOLD_FONT.exists():
        raise FileNotFoundError(
            f"Bold font not found: {BOLD_FONT}"
        )

    # --------------------------------------------------
    # 3. Create canvas
    # --------------------------------------------------

    image = Image.new(
        "RGB",
        (width, height),
        background_color
    )

    draw = ImageDraw.Draw(image)

    # --------------------------------------------------
    # 4. Adaptive quote font
    # --------------------------------------------------

    quote_length = len(quote["text"])

    if quote_length < 70:
        quote_size = 70
    elif quote_length < 120:
        quote_size = 60
    elif quote_length < 180:
        quote_size = 52
    else:
        quote_size = 46

    quote_font = load_font(
        REGULAR_FONT,
        quote_size
    )

    author_font = load_font(
        REGULAR_FONT,
        34
    )

    brand_font = load_font(
        BOLD_FONT,
        26
    )

    quote_mark_font = load_font(
        BOLD_FONT,
        130
    )

    # --------------------------------------------------
    # 5. Top accent line
    # --------------------------------------------------

    draw.rounded_rectangle(
        (70, 70, width - 70, 78),
        radius=4,
        fill=accent_color
    )

    # --------------------------------------------------
    # 6. Brand name
    # --------------------------------------------------

    draw.text(
        (70, 115),
        brand_name,
        font=brand_font,
        fill=accent_color
    )

    # --------------------------------------------------
    # 7. Quote mark
    # --------------------------------------------------

    draw.text(
        (70, 250),
        "“",
        font=quote_mark_font,
        fill=accent_color
    )

    # --------------------------------------------------
    # 8. Prepare quote text
    # --------------------------------------------------

    quote_text = quote["text"]

    wrap_width = poster_config["quote_wrap_width"]

    lines = textwrap.wrap(
        quote_text,
        width=wrap_width
    )

    line_height = int(
        quote_size * 1.35
    )

    total_height = (
        len(lines) * line_height
    )

    start_y = (
        (height - total_height) // 2
        - 40
    )

    # --------------------------------------------------
    # 9. Draw quote
    # --------------------------------------------------

    for i, line in enumerate(lines):

        bbox = draw.textbbox(
            (0, 0),
            line,
            font=quote_font
        )

        text_width = bbox[2] - bbox[0]

        x = (width - text_width) // 2

        y = start_y + i * line_height

        draw.text(
            (x, y),
            line,
            font=quote_font,
            fill=quote_color
        )

    # --------------------------------------------------
    # 10. Author
    # --------------------------------------------------

    author = f"— {quote['author']}"

    bbox = draw.textbbox(
        (0, 0),
        author,
        font=author_font
    )

    author_width = bbox[2] - bbox[0]

    author_y = start_y + total_height + 50

    draw.text(
        (
            (width - author_width) // 2,
            author_y
        ),
        author,
        font=author_font,
        fill=author_color
    )

    # --------------------------------------------------
    # 11. Bottom separator
    # --------------------------------------------------

    draw.rounded_rectangle(
        (70, height - 160, width - 70, height - 157),
        radius=2,
        fill=(70, 70, 75)
    )

    # --------------------------------------------------
    # 12. Footer
    # --------------------------------------------------

    bbox = draw.textbbox(
        (0, 0),
        footer_text,
        font=brand_font
    )

    footer_width = bbox[2] - bbox[0]

    draw.text(
        (
            (width - footer_width) // 2,
            height - 120
        ),
        footer_text,
        font=brand_font,
        fill=footer_color
    )

    # --------------------------------------------------
    # 13. Save poster
    # --------------------------------------------------

    OUTPUT_DIR.mkdir(
        exist_ok=True
    )

    today = datetime.now().strftime("%Y-%m-%d")

    output_path = OUTPUT_DIR / f"motivation_{today}.png"

    image.save(
        output_path,
        quality=95
    )

    return output_path