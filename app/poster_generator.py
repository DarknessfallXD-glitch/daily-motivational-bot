from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import textwrap


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)


WIDTH = 1080
HEIGHT = 1350


def load_font(size):
    font_paths = [
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    ]

    for path in font_paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)

    return ImageFont.load_default()


def create_poster(quote, filename="motivation.png"):

    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        "#111111"
    )

    draw = ImageDraw.Draw(image)

    quote_font = load_font(58)
    author_font = load_font(36)
    branding_font = load_font(30)

    # Wrap the quote
    wrapped_quote = textwrap.fill(
        quote["text"],
        width=28
    )

    # Calculate quote position
    quote_box = draw.multiline_textbbox(
        (0, 0),
        wrapped_quote,
        font=quote_font,
        spacing=15,
        align="center"
    )

    quote_width = quote_box[2] - quote_box[0]
    quote_height = quote_box[3] - quote_box[1]

    quote_x = (WIDTH - quote_width) / 2
    quote_y = (HEIGHT - quote_height) / 2 - 100

    # Draw quote
    draw.multiline_text(
        (quote_x, quote_y),
        wrapped_quote,
        font=quote_font,
        fill="white",
        spacing=15,
        align="center"
    )

    # Author
    author = f"— {quote['author']}"

    author_box = draw.textbbox(
        (0, 0),
        author,
        font=author_font
    )

    author_width = author_box[2] - author_box[0]

    draw.text(
        ((WIDTH - author_width) / 2, quote_y + quote_height + 70),
        author,
        font=author_font,
        fill="#CCCCCC"
    )

    # Branding
    branding = "DAILY MOTIVATION"

    branding_box = draw.textbbox(
        (0, 0),
        branding,
        font=branding_font
    )

    branding_width = branding_box[2] - branding_box[0]

    draw.text(
        ((WIDTH - branding_width) / 2, HEIGHT - 100),
        branding,
        font=branding_font,
        fill="#888888"
    )

    output_path = OUTPUT_DIR / filename

    image.save(output_path, quality=95)

    return output_path