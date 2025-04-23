from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

SAVE_DIR = "public"
TAG_LABEL_FONT = "C:/Windows/Fonts/malgun.ttf"

def paste_top3_images(buf: BytesIO, best_patterns: dict, filtered_tags: list) -> BytesIO:
    radar_img = Image.open(buf).convert("RGBA")
    width, height = radar_img.size

    FONT = ImageFont.truetype(TAG_LABEL_FONT, 20)
    PADDING = 20
    COVER_SIZE = 120
    LINE_HEIGHT = COVER_SIZE + 45
    COL_WIDTH = COVER_SIZE * 3 + PADDING * 3

    canvas = Image.new("RGBA", (width + COL_WIDTH, max(height, LINE_HEIGHT * len(filtered_tags))), (0, 0, 0, 255))
    canvas.paste(radar_img, (0, 0))

    for i, tag in enumerate(filtered_tags):
        x_offset = width + PADDING
        y_offset = i * LINE_HEIGHT + PADDING

        draw = ImageDraw.Draw(canvas)
        draw.text((x_offset, y_offset), f"{tag} Top 3", fill="white", font=FONT)

        for j, entry in enumerate(best_patterns[tag]):
            score, rate, pattern_key = entry  # entry는 [score, "title_index::pattern"]

            title_index = pattern_key.split("::")[0]

            img_path = os.path.join(SAVE_DIR, f"{title_index}.jpg")
            if os.path.exists(img_path):
                try:
                    cover = Image.open(img_path).convert("RGB").resize((COVER_SIZE, COVER_SIZE))
                    canvas.paste(cover, (x_offset + (COVER_SIZE + PADDING) * j, y_offset + 30))
                except Exception:
                    pass

                draw.text(
                    (x_offset + (COVER_SIZE + PADDING) * j, y_offset + 30 + COVER_SIZE + 2),
                    f"{float(rate):.2f}",
                    fill="white",
                    font=FONT
                )

    result_buf = BytesIO()
    canvas.save(result_buf, format="PNG")
    result_buf.seek(0)
    return result_buf
