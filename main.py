#!/usr/bin/env python3
"""
Sum up 20 November 2026 world news in one image.
make.fun bounty: news-image-20261120, $250, 50 places paid.
Deadline: Sun 22 Nov 2026 00:00 UTC.

Design: a real broadsheet front page, in the manner of a classic
newspaper nameplate paper - off-white paper, black serif type, thin
rules, columns. No bright panels, no icons, no flat AI look.

Deterministic: no network, no random, no timestamps, no external files.
Draws a 1024x1024 front page with Pillow only and writes one PNG to
the output directory only (MAKEFUN_OUTPUT_DIR, else /output).
It never writes beside its own file: in the grader that folder is
read-only, and a second save there fails the run.

Run: python3 main.py
Requires: Pillow (PIL). Fonts: DejaVu Serif if present, else default.
"""

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (248, 246, 240)
INK = (18, 18, 18)
GREY = (96, 96, 92)
LIGHT_GREY = (150, 150, 146)
RED = (139, 30, 30)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    except Exception:
        pass
    try:
        return ImageFont.truetype(name, size)
    except Exception:
        return ImageFont.load_default()


F_NAME = lambda s: load_font("DejaVuSerif-Bold.ttf", s)
F_HEAD = lambda s: load_font("DejaVuSerif-Bold.ttf", s)
F_BODY = lambda s: load_font("DejaVuSerif.ttf", s)
F_BODY_B = lambda s: load_font("DejaVuSerif-Bold.ttf", s)


def rule(draw, x0, y, x1, width=1):
    draw.line([(x0, y), (x1, y)], fill=INK, width=width)


def wrap(draw, text, font, max_width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, font, color, max_width, line_h):
    for line in wrap(draw, text, font, max_width):
        draw.text((x, y), line, font=font, fill=color)
        y += line_h
    return y


def columns(draw, x, y, width, text, font, line_h, ncols, gutter=18):
    """Body text flowing across ncols columns. Returns bottom y."""
    col_w = (width - gutter * (ncols - 1)) // ncols
    lines = wrap(draw, text, font, col_w)
    per = (len(lines) + ncols - 1) // ncols
    bottom = y
    for c in range(ncols):
        chunk = lines[c * per:(c + 1) * per]
        cy = y
        for line in chunk:
            draw.text((x + c * (col_w + gutter), cy), line, font=font, fill=INK)
            cy += line_h
        bottom = max(bottom, cy)
    return bottom


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36
    x1 = W - mx

    # ---- Nameplate ----
    d.text((mx, 18), "FRIDAY, NOVEMBER 20, 2026", font=F_BODY_B(15), fill=INK)
    right = "WORLD NEWS IN ONE IMAGE"
    d.text((x1 - d.textlength(right, font=F_BODY_B(15)), 18), right,
           font=F_BODY_B(15), fill=INK)
    name = "The World"
    nw = d.textlength(name, font=F_NAME(84))
    d.text(((W - nw) / 2, 30), name, font=F_NAME(84), fill=INK)
    d.text((mx, 122), "Vol. I  —  No. 20", font=F_BODY(14), fill=GREY)
    late = "LATE EDITION"
    d.text((x1 - d.textlength(late, font=F_BODY(14)), 122), late,
           font=F_BODY(14), fill=GREY)
    rule(d, mx, 146, x1, 3)
    rule(d, mx, 151, x1, 1)

    # ---- Lead story: Kyiv ----
    y = 168
    d.text((mx, y), "KYIV, UKRAINE", font=F_BODY_B(16), fill=RED)
    y = draw_wrapped(d, mx, y + 24,
                     "Russia Hits Kyiv With 400 Drones and Missiles; Two Land in Poland",
                     F_HEAD(40), INK, x1 - mx, 48)
    y += 6
    d.text((mx, y), "By the Foreign Desk", font=F_BODY(14), fill=GREY)
    y += 26
    y = columns(d, mx, y, x1 - mx,
                "Russia launched its heaviest overnight attack of the war on "
                "Friday, firing more than 400 drones and 110 missiles at "
                "Ukraine. At least eight people were killed in Kyiv and "
                "nearly 30 injured, and strikes on power stations forced "
                "nuclear plants to cut output. Two Russian missiles also "
                "came down inside Poland, a NATO member, without casualties. "
                "Ukraine said its air force shot down or suppressed 462 "
                "aerial targets, and European leaders proposed legally "
                "binding security guarantees tied to a future ceasefire.",
                F_BODY(17), 23, 3)
    y += 10
    rule(d, mx, y, x1, 1)
    y += 14

    # ---- Second row: two stories ----
    col_w = (x1 - mx - 24) // 2
    y0 = y
    # Left: ICJ Myanmar
    d.text((mx, y0), "THE HAGUE", font=F_BODY_B(15), fill=RED)
    yL = draw_wrapped(d, mx, y0 + 22,
                      "Court Finds Myanmar Guilty of Genocide",
                      F_HEAD(26), INK, col_w, 32)
    yL = draw_wrapped(d, mx, yL + 4,
                      "The International Court of Justice ruled that Myanmar "
                      "committed genocide against the Rohingya Muslims, the "
                      "first time the court has held a state responsible.",
                      F_BODY(16), INK, col_w, 22)
    # Right: Shenzhen
    rx = mx + col_w + 24
    d.text((rx, y0), "SHENZHEN", font=F_BODY_B(15), fill=RED)
    yR = draw_wrapped(d, rx, y0 + 22,
                      "Trump, Xi and Putin Pledge Peace After Summit",
                      F_HEAD(26), INK, col_w, 32)
    yR = draw_wrapped(d, rx, yR + 4,
                      "After their first three-way meeting, the three leaders "
                      "issued a joint declaration on peace and stability. Mr. "
                      "Trump later gave a 90-minute news conference, and the "
                      "United States and China agreed that humans must oversee "
                      "military decisions on artificial intelligence.",
                      F_BODY(16), INK, col_w, 22)
    y = max(yL, yR) + 10
    rule(d, mx, y, x1, 1)
    y += 14

    # ---- Third row: two stories ----
    y0 = y
    d.text((mx, y0), "ODISHA, INDIA", font=F_BODY_B(15), fill=RED)
    yL = draw_wrapped(d, mx, y0 + 22,
                      "Cyclone Akvan Comes Ashore",
                      F_HEAD(26), INK, col_w, 32)
    yL = draw_wrapped(d, mx, yL + 4,
                      "The severe storm made landfall on the Andhra Pradesh-"
                      "Odisha coast with winds of 90 to 100 kilometres an "
                      "hour, gusting to 110.",
                      F_BODY(16), INK, col_w, 22)
    d.text((rx, y0), "NEW YORK", font=F_BODY_B(15), fill=RED)
    yR = draw_wrapped(d, rx, y0 + 22,
                      "Stocks Slide as AI Sell-Off Deepens",
                      F_HEAD(26), INK, col_w, 32)
    yR = draw_wrapped(d, rx, yR + 4,
                      "The S&P 500 fell 3.7 per cent on Friday as a "
                      "sell-off in artificial intelligence and chip shares "
                      "pushed the market into correction.",
                      F_BODY(16), INK, col_w, 22)
    y = max(yL, yR) + 12

    # ---- Bottom strip ----
    rule(d, mx, y, x1, 3)
    rule(d, mx, y + 5, x1, 1)
    y += 16
    d.text((mx, y), "ALSO TODAY", font=F_BODY_B(15), fill=RED)
    y = draw_wrapped(d, mx, y + 22,
                     "COP31 talks stall over fossil fuels in Antalya  •  "
                     "Magnitude 6.7 earthquake shakes central Peru  •  "
                     "Oil tanker on fire in the Strait of Hormuz as the "
                     "United States blockades Iranian shipping",
                     F_BODY(16), INK, x1 - mx, 22)
    y += 8
    rule(d, mx, y, x1, 1)
    y += 8
    d.text((mx, y), "FRIDAY, NOVEMBER 20, 2026", font=F_BODY(13), fill=GREY)
    foot = "THE WORLD  •  WORLD NEWS IN ONE IMAGE"
    d.text((x1 - d.textlength(foot, font=F_BODY(13)), y), foot,
           font=F_BODY(13), fill=GREY)

    return img


def main():
    img = draw()
    # Only ever write to the output directory. Never write beside
    # this file: in the grader that folder is read-only.
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "entry.png"
    img.save(out, format="PNG", compress_level=6, optimize=False)
    print(f"Wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
