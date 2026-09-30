from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import textwrap
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"

WIDTH = 1080
HEIGHT = 1350


def load_font(path, size):
    return ImageFont.truetype(path, size)


def create_poster(quote):
    # --------------------------------------------------
    # 1. Create canvas
    # --------------------------------------------------

    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        (18, 18, 20)
    )

    draw = ImageDraw.Draw(image)

    # --------------------------------------------------
    # 2. Font paths
    # --------------------------------------------------

   # --------------------------------------------------
# 2. Font paths
# --------------------------------------------------
# --------------------------------------------------
# 2. Font paths
# --------------------------------------------------

    windows_regular = Path("C:/Windows/Fonts/arial.ttf")
    windows_bold = Path("C:/Windows/Fonts/arialbd.ttf")

    linux_regular = Path(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    )

    linux_bold = Path(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    )

    if windows_regular.exists():
        regular_font_path = windows_regular
        bold_font_path = windows_bold

    elif linux_regular.exists():
        regular_font_path = linux_regular
        bold_font_path = linux_bold

    else:
        raise FileNotFoundError(
            "No suitable font found."
        )
    # --------------------------------------------------
    # 3. Adaptive quote font
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
        regular_font_path,
        quote_size
    )

    # Other fonts
    author_font = load_font(
        regular_font_path,
        34
    )

    brand_font = load_font(
        bold_font_path,
        26
    )

    quote_mark_font = load_font(
        bold_font_path,
        130
    )

    # --------------------------------------------------
    # 4. Top accent line
    # --------------------------------------------------

    draw.rounded_rectangle(
        (70, 70, 1010, 78),
        radius=4,
        fill=(255, 180, 70)
    )

    # --------------------------------------------------
    # 5. Brand name
    # --------------------------------------------------

    draw.text(
        (70, 115),
        "DAILY MOTIVATION",
        font=brand_font,
        fill=(255, 180, 70)
    )

    # --------------------------------------------------
    # 6. Quote mark
    # --------------------------------------------------

    draw.text(
        (70, 250),
        "“",
        font=quote_mark_font,
        fill=(255, 180, 70)
    )

    # --------------------------------------------------
    # 7. Prepare quote text
    # --------------------------------------------------

    quote_text = quote["text"]

    lines = textwrap.wrap(
        quote_text,
        width=28
    )

    line_height = int(
        quote_size * 1.35
    )

    total_height = (
        len(lines) * line_height
    )

    # Center quote vertically
    start_y = (
        (HEIGHT - total_height) // 2
        - 40
    )

    # --------------------------------------------------
    # 8. Draw quote
    # --------------------------------------------------

    for i, line in enumerate(lines):

        bbox = draw.textbbox(
            (0, 0),
            line,
            font=quote_font
        )

        text_width = (
            bbox[2] - bbox[0]
        )

        x = (
            WIDTH - text_width
        ) // 2

        y = (
            start_y
            + i * line_height
        )

        draw.text(
            (x, y),
            line,
            font=quote_font,
            fill=(245, 245, 245)
        )

    # --------------------------------------------------
    # 9. Author
    # --------------------------------------------------

    author = f"— {quote['author']}"

    bbox = draw.textbbox(
        (0, 0),
        author,
        font=author_font
    )

    author_width = (
        bbox[2] - bbox[0]
    )

    author_y = (
        start_y
        + total_height
        + 50
    )

    draw.text(
        (
            (WIDTH - author_width) // 2,
            author_y
        ),
        author,
        font=author_font,
        fill=(180, 180, 185)
    )

    # --------------------------------------------------
    # 10. Bottom separator
    # --------------------------------------------------

    draw.rounded_rectangle(
        (70, 1190, 1010, 1193),
        radius=2,
        fill=(70, 70, 75)
    )

    # --------------------------------------------------
    # 11. Footer
    # --------------------------------------------------

    footer = (
        "ONE DAY. ONE QUOTE. ONE STEP FORWARD."
    )

    bbox = draw.textbbox(
        (0, 0),
        footer,
        font=brand_font
    )

    footer_width = (
        bbox[2] - bbox[0]
    )

    draw.text(
        (
            (WIDTH - footer_width) // 2,
            1230
        ),
        footer,
        font=brand_font,
        fill=(140, 140, 145)
    )

    # --------------------------------------------------
    # 12. Save poster
    # --------------------------------------------------

    OUTPUT_DIR.mkdir(
        exist_ok=True
    )

    today = datetime.now().strftime("%Y-%m-%d")

    output_path = (
        OUTPUT_DIR / f"motivation_{today}.png"
    )

    image.save(
        output_path,
        quality=95
    )

    return output_path
