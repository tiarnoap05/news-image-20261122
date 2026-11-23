#!/usr/bin/env python3
"""Draw the front page for Sunday 22 November 2026, save entry.png.

A newspaper front page: masthead, dateline, COP31's collapse as the
lead story with a torn "Antalya Pact" document and a NO DEAL stamp,
four grid stories, an ALSO TODAY strip and a footer. Pillow drawing
only: no network, no timestamps, no randomness, so every run writes
the same bytes.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
INK = (24, 24, 24)
PAPER = (247, 243, 234)
MUTED = (96, 91, 80)
RED = (178, 34, 34)
DOC = (255, 255, 255)
GREY_LINE = (150, 146, 138)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


F_TITLE = font("DejaVuSerif-Bold.ttf", 64)
F_DATE = font("DejaVuSans-Bold.ttf", 21)
F_HEAD = font("DejaVuSerif-Bold.ttf", 33)
F_BODY = font("DejaVuSerif.ttf", 19)
F_KICK = font("DejaVuSans-Bold.ttf", 16)
F_GRID_HEAD = font("DejaVuSerif-Bold.ttf", 22)
F_GRID_BODY = font("DejaVuSans.ttf", 16)
F_LABEL = font("DejaVuSans-Bold.ttf", 15)
F_DOC_TITLE = font("DejaVuSans-Bold.ttf", 15)
F_STAMP = font("DejaVuSans-Bold.ttf", 46)
F_STAMP_SMALL = font("DejaVuSans-Bold.ttf", 17)
F_STRIP = font("DejaVuSans.ttf", 16)
F_STRIP_LABEL = font("DejaVuSans-Bold.ttf", 16)
F_FOOT = font("DejaVuSans.ttf", 13)


def wrap(draw, text, fnt, width):
    """Greedy word wrap measured with the real font, so nothing overflows."""
    lines = []
    cur = ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill=INK, leading=None):
    """Draw wrapped lines top-left at (x, y); return the y below the last."""
    if leading is None:
        leading = int(fnt.size * 1.32)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def torn_document(draw, x0, y0, x1, y1):
    """Two halves of a white document split by a jagged tear."""
    tx = (x0 + x1) // 2
    # Zigzag points down the tear, alternating a few pixels either side.
    teeth = []
    steps = 7
    for i in range(steps + 1):
        yy = y0 + (y1 - y0) * i / steps
        off = 0 if i in (0, steps) else (9 if i % 2 else -9)
        teeth.append((tx + off, yy))
    left = [(x0, y0)] + teeth + [(x0, y1)]
    right = [(tx, y0), (x1, y0), (x1, y1)] + list(reversed(teeth))
    draw.polygon(left, fill=DOC, outline=INK)
    draw.polygon(right, fill=DOC, outline=INK)
    # Fake text lines on each half.
    for i in range(4):
        ly = y0 + 34 + i * 13
        draw.line([(x0 + 14, ly), (tx - 16, ly)], fill=GREY_LINE, width=3)
        draw.line([(tx + 16, ly), (x1 - 14, ly)], fill=GREY_LINE, width=3)
    # The pact's title on the left half, and a red strike through the
    # "fossil fuels" line on the right half: the words the deal dropped.
    draw.text((x0 + 14, y0 + 8), "THE ANTALYA PACT", font=F_DOC_TITLE,
              fill=INK)
    strike_y = y0 + 34 + 2 * 13
    draw.line([(tx + 16, strike_y - 1), (x1 - 14, strike_y + 3)],
              fill=RED, width=3)


def no_deal_stamp(img, x, y):
    """A red NO DEAL stamp, slightly tilted, pasted onto the page."""
    layer = Image.new("RGBA", (380, 130), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rectangle([6, 6, 374, 124], outline=(178, 34, 34, 255), width=4)
    d.rectangle([14, 14, 366, 116], outline=(178, 34, 34, 255), width=2)
    text = "NO DEAL"
    tw = d.textlength(text, font=F_STAMP)
    d.text(((380 - tw) / 2, 22), text, font=F_STAMP,
           fill=(178, 34, 34, 255))
    sub = "ANTALYA  \u2022  22 NOV 2026"
    sw = d.textlength(sub, font=F_STAMP_SMALL)
    d.text(((380 - sw) / 2, 88), sub, font=F_STAMP_SMALL,
           fill=(178, 34, 34, 255))
    layer = layer.rotate(-9, resample=Image.BICUBIC, expand=True)
    img.paste(layer, (x, y), layer)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36
    cw = W - 2 * mx

    # Masthead.
    title = "THE WORLD TODAY"
    d.text(((W - d.textlength(title, font=F_TITLE)) / 2, 26), title,
           font=F_TITLE, fill=INK)
    d.line([(mx, 112), (W - mx, 112)], fill=INK, width=3)
    d.line([(mx, 118), (W - mx, 118)], fill=INK, width=1)

    # Dateline.
    date = "SUNDAY, 22 NOVEMBER 2026  \u2022  THE DAY'S WORLD NEWS IN ONE PAGE"
    d.text(((W - d.textlength(date, font=F_DATE)) / 2, 130), date,
           font=F_DATE, fill=MUTED)

    # Lead headline.
    lead_head = "COP31 COLLAPSES: CLIMATE TALKS END WITH NO DEAL"
    y = 168
    y = draw_lines(d, wrap(d, lead_head, F_HEAD, cw), mx, y, F_HEAD,
                   leading=42)

    # Lead visual: torn pact on the left, NO DEAL stamp on the right.
    vy = y + 14
    torn_document(d, mx, vy, mx + 520, vy + 110)
    no_deal_stamp(img, mx + 560, vy - 8)

    # Lead body.
    lead_body = (
        "ANTALYA \u2014 Two weeks of talks and two days of overtime ended "
        "on Sunday with no agreement at all. The EU, Panama and island "
        "states rejected the \u201cAntalya Pact\u201d because it never "
        "mentioned fossil fuels. UN chief Ant\u00f3nio Guterres called it "
        "\u201cdeeply disappointing\u201d \u2014 the first climate summit "
        "to collapse since Copenhagen in 2009, and the longest COP ever.")
    y = draw_lines(d, wrap(d, lead_body, F_BODY, cw), mx, vy + 132,
                   F_BODY, leading=26)

    # Layout guard: the lead must end before the grid divider at y=566.
    if y > 560:
        raise ValueError(f"lead overflows the lead area: ends at y={y}")

    # Divider above the grid.
    d.line([(mx, 566), (W - mx, 566)], fill=INK, width=2)

    stories = [
        ("LIBYA", "Ukrainian drones hit warship",
         "Suspected Ukrainian sea drones struck a Russian naval vessel "
         "docked at Benghazi \u2014 a second ship was also reported hit."),
        ("GULF", "Iran strikes US bases and tankers",
         "Iran fired missiles and drones at US bases in Bahrain, hit a "
         "civilian plant in Sitra, and struck three tankers near the "
         "Strait of Hormuz."),
        ("UKRAINE", "Kryvyi Rih missile kills boy, 7",
         "A Russian ballistic missile hit Zelenskyy\u2019s hometown, "
         "killing a 7-year-old boy and a 20-year-old woman and wounding "
         "60. A strike near Kyiv collapsed flats."),
        ("MARKETS", "Stocks slide as AI sell-off deepens",
         "The S&P 500 fell 3.7% into correction and the Nasdaq 5.3% on "
         "Friday; Japan\u2019s Nikkei dropped 5.06%."),
    ]
    col_w = (cw - 24) / 2
    row_y = [582, 730]
    for i, (kicker, head, body) in enumerate(stories):
        x = mx + (i % 2) * (col_w + 24)
        y = row_y[i // 2]
        d.text((x, y), kicker, font=F_KICK, fill=RED)
        y += 24
        y = draw_lines(d, wrap(d, head, F_GRID_HEAD, col_w), x, y,
                       F_GRID_HEAD, leading=27)
        end = draw_lines(d, wrap(d, body, F_GRID_BODY, col_w), x, y + 4,
                         F_GRID_BODY, leading=21)
        if end > row_y[i // 2] + 138:
            raise ValueError(f"grid story {i} overflows: ends at y={end}")
    # Grid separators.
    d.line([(W / 2, 582), (W / 2, 866)], fill=MUTED, width=1)
    d.line([(mx, 720), (W - mx, 720)], fill=MUTED, width=1)

    # ALSO TODAY strip.
    d.line([(mx, 884), (W - mx, 884)], fill=INK, width=2)
    strip = ("Mexico captures \u2018El Chapo Isidro\u2019 \u2022 ICJ: "
             "Myanmar guilty of Rohingya genocide \u2022 Democrats win "
             "258 House seats \u2022 BepiColombo orbits Mercury \u2022 "
             "Indonesia factory fire: 3 dead, 34 missing")
    label = "ALSO TODAY  "
    lw = d.textlength(label, font=F_STRIP_LABEL)
    d.text((mx, 900), label, font=F_STRIP_LABEL, fill=RED)
    end = draw_lines(d, wrap(d, strip, F_STRIP, cw - lw), mx + lw, 900,
                     F_STRIP, leading=21)
    if end > 958:
        raise ValueError(f"strip overflows: ends at y={end}")

    # Footer.
    d.line([(mx, 962), (W - mx, 962)], fill=INK, width=1)
    foot = ("THE WORLD TODAY  \u2022  Sunday 22 November 2026  \u2022  "
            "make.fun \u00b7 news-image-20261122")
    d.text(((W - d.textlength(foot, font=F_FOOT)) / 2, 972), foot,
           font=F_FOOT, fill=MUTED)

    out = Path(__file__).resolve().parent.parent / "entry.png"
    img.save(out, format="PNG")
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
