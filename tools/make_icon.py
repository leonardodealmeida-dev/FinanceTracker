"""Generates the app icon (assets/icon.png, icon.ico, icon.icns).

Run: python tools/make_icon.py   (needs Pillow)
"""

from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent.parent / "assets"
SIZE = 1024
SCALE = 2  # draw at 2x and downsample for smooth edges


def draw_icon():
    s = SIZE * SCALE
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Rounded-square background with a soft vertical gradient.
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, s - 1, s - 1), radius=int(s * 0.225), fill=255
    )
    top, bottom = (30, 48, 38), (14, 22, 17)
    gradient = Image.new("RGBA", (s, s))
    gd = ImageDraw.Draw(gradient)
    for y in range(s):
        t = y / s
        color = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        gd.line((0, y, s, y), fill=color + (255,))
    img.paste(gradient, (0, 0), mask)

    # Three ascending bars.
    green = (101, 207, 145, 255)
    light = (126, 226, 168, 255)
    base = int(s * 0.74)
    width = int(s * 0.15)
    gap = int(s * 0.07)
    heights = [0.20, 0.34, 0.50]
    total = 3 * width + 2 * gap
    x = (s - total) // 2
    for i, h in enumerate(heights):
        top_y = base - int(s * h)
        d.rounded_rectangle(
            (x, top_y, x + width, base), radius=int(width * 0.28),
            fill=light if i == 2 else green,
        )
        x += width + gap

    # Trend line with a dot at the end.
    pts = [(int(s * 0.22), int(s * 0.46)), (int(s * 0.40), int(s * 0.36)),
           (int(s * 0.56), int(s * 0.42)), (int(s * 0.78), int(s * 0.24))]
    d.line(pts, fill=(237, 245, 239, 255), width=int(s * 0.028), joint="curve")
    r = int(s * 0.035)
    ex, ey = pts[-1]
    d.ellipse((ex - r, ey - r, ex + r, ey + r), fill=(237, 245, 239, 255))

    return img.resize((SIZE, SIZE), Image.LANCZOS)


def main():
    OUT.mkdir(exist_ok=True)
    icon = draw_icon()
    icon.save(OUT / "icon.png")
    icon.save(
        OUT / "icon.ico",
        sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64),
               (128, 128), (256, 256)],
    )
    icon.save(OUT / "icon.icns")
    print("Wrote icon.png, icon.ico, icon.icns to", OUT)


if __name__ == "__main__":
    main()
