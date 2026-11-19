#!/usr/bin/env python3
"""Render 'The World in One Day' — Thursday 19 November 2026.

A dense newspaper front page drawn entirely with PIL shapes:
masthead + date, 13 flat illustrated stories (3 big + 10 small),
a numbered 14-45 brief list, a world map with numbered pins,
and a sources footer. All 45 stories happened or were first
reported on Thursday 19 November 2026.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")

PAPER = (247, 242, 231)
INK = (26, 26, 26)
MUTED = (90, 86, 78)
RED = (178, 34, 34)
RULE = (60, 58, 52)
SEA = (223, 233, 236)

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_wrapped(draw, x, y, text, fnt, max_w, fill, leading=None, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading if leading is not None else int(fnt.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y

def text_h(fnt, lines=1, leading=None):
    lh = leading if leading is not None else int(fnt.size * 1.18)
    return lh * lines

# ---------------------------------------------------------------- stories
# (number, region, headline, summary, pin lon/lat)
BIG = [
    (1, "NORTH AMERICA", "Vice City opens its doors",
     "Grand Theft Auto VI begins its global rollout after a 13-year wait, with gamers queueing worldwide.",
     (-80, 26)),
    (2, "ASIA", "Three leaders, one table in Shenzhen",
     "Trump, Xi and Putin hold trilateral talks on the sidelines of the APEC summit in Shenzhen.",
     (114, 22)),
    (3, "SPACE", "Voyager 1, one light-day out",
     "NASA confirms the 48-year-old probe has reached a light-day from Earth - a first for any spacecraft.",
     (-118, 34)),
]

SMALL = [
    (4, "NORTH AMERICA", "Jeffries poised to make history",
     "Democrats nominate Hakeem Jeffries for Speaker; he would be the first Black Speaker.",
     (-77, 39)),
    (5, "MIDDLE EAST", "Gulf strikes widen",
     "US and Iran exchange fire again as Tehran's attacks spread to Kuwait and Bahrain.",
     (51, 26)),
    (6, "ASIA", "Cyclone Akvan bears down on India",
     "The storm is set to cross the coast between Machilipatnam and Puri.",
     (89, 17)),
    (7, "EUROPE", "€45bn lifeline for Kyiv",
     "The EU proposes a loan for Ukraine, to be repaid once Russia pays reparations.",
     (4, 51)),
    (8, "OCEANIA", "Canberra sanctions settlers",
     "Australia sanctions Israeli settlers and groups over West Bank expansion.",
     (149, -35)),
    (9, "TECH", "Nvidia cuts China off H-series",
     "The chipmaker halts Hopper shipments to China as acting chief Kress promises earlier pay rises.",
     (-122, 37)),
    (10, "EUROPE", "Tanker sunk by projectiles",
     "An LPG tanker that sank off Bulgaria was hit by projectiles, officials say.",
     (28, 43)),
    (11, "MIDDLE EAST", "Tanks push into central Gaza",
     "Israeli forces launch a fresh ground operation west of the Yellow Line.",
     (34, 31)),
    (12, "NORTH AMERICA", "Peltola seals the Senate",
     "Democrat Peltola wins Alaska, giving Democrats a 56-44 Senate majority.",
     (-150, 64)),
    (13, "ASIA", "Royals in Delhi, defence in Tokyo",
     "Modi meets the Prince and Princess of Wales; India and Japan open 2+2 defence talks.",
     (140, 36)),
]

ALSO = [
    "Earth is missing a billion years of history - scientists may have found why.",
    "Fed minutes: most officials expect further rate hikes.",
    "Oil falls as WTI closes at $83.26 amid Gulf tensions.",
    "NSA's classified internal network suffers an outage, reports say.",
    "Somalia accuses the UAE of building secret military bases.",
    "Deutsche Bank handled $582m in Epstein-linked deals, the FT reports.",
    "Saudi forces launch a major attack on Houthi rebels in Yemen.",
    "Riyadh says the danger has passed in three southern cities.",
    "Islam on track to be the world's largest religion by 2035, Pew finds.",
    "Liu Yunping becomes the first Taiwanese American House caucus chair.",
    "Microsoft in talks to sell AI services to ByteDance.",
    "US senators warn AI cyber threats are outpacing defences.",
    "Canada rethinks China ties as Carney chases a US deal.",
    "French minister says Melenchon could win the presidency.",
    "Cocaine and millions of pills seized in eastern Libya.",
    "US proposes tougher green-card rules and longer hiring.",
    "General Pants collapses into administration before Black Friday.",
    "ASX falls for a fifth straight session on a Wall Street rout.",
    "Australia's central bank board split over lifting rates.",
    "Australia moves to ban photographs of defence sites.",
    "Duckett's 133 puts England on top in the third ODI.",
    "Merck launches a self-amplifying mRNA rabies vaccine for pets.",
    "School bus bursts into flames; the driver is hailed a hero.",
    "Mother and daughter freed unharmed in a $1m Melbourne hostage ordeal.",
    "Fifty pupils hospitalised after pollution from a tar-mixing unit in India.",
    "Air India 171 crash probe report at its 'fag end', Centre tells court.",
    "Ukraine 'destroying the occupiers' as Russia attacks, Kyiv says.",
    "Gates: only a massive cyberattack would bring a new expert-led order (claim).",
    "Huang's Nvidia exit sends shockwaves through the AI world.",
    "Taiwan drafts a transnational-repression crime into law.",
    "Brazil wind additions fall below 400 MW in 2026 as developers shift.",
    "AI data centres could soon rival coal plants on power use.",
]

# ------------------------------------------------------- flat illustrations
def badge(draw, x, y, n, r=11):
    """Numbered circle badge (white number on red)."""
    draw.ellipse([x - r, y - r, x + r, y + r], fill=RED, outline=(255, 255, 255), width=2)
    f = font(SANS_B, 13)
    tw = draw.textlength(str(n), font=f)
    draw.text((x - tw / 2, y - 7), str(n), font=f, fill=(255, 255, 255))

def illo_vice_city(draw, x, y, w, h):
    """Sunset sky, sun, palms, neon skyline, car — Vice City."""
    # sunset bands
    bands = [(255, 170, 90), (255, 130, 110), (235, 90, 130), (150, 70, 140), (70, 50, 110)]
    for i, c in enumerate(bands):
        draw.rectangle([x, y + i * h // 5, x + w, y + (i + 1) * h // 5], fill=c)
    # sun
    cx, cy, r = x + w // 2, y + h // 2 - 6, 26
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 236, 160))
    # skyline
    base = y + h - 26
    heights = [52, 70, 44, 78, 60, 88, 50, 66]
    bw = w // len(heights)
    for i, hh in enumerate(heights):
        bx = x + i * bw
        draw.rectangle([bx + 2, base - hh, bx + bw - 2, base], fill=(38, 20, 60))
        for wy in range(base - hh + 6, base - 6, 12):
            for wx in range(bx + 6, bx + bw - 6, 10):
                if (wx + wy) % 20 == 0:
                    draw.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 220, 110))
    # neon strip
    draw.rectangle([x, base - 2, x + w, base + 2], fill=(255, 60, 180))
    # road + car
    draw.rectangle([x, base, x + w, y + h], fill=(24, 16, 40))
    carx, cary = x + w // 2 - 42, y + h - 20
    draw.rectangle([carx, cary, carx + 84, cary + 12], fill=(255, 60, 120))
    draw.polygon([(carx + 16, cary), (carx + 26, cary - 10), (carx + 58, cary - 10), (carx + 68, cary)], fill=(255, 60, 120))
    draw.ellipse([carx + 12, cary + 8, carx + 26, cary + 18], fill=(15, 15, 15))
    draw.ellipse([carx + 58, cary + 8, carx + 72, cary + 18], fill=(15, 15, 15))
    # palm silhouettes
    for px, ph in [(x + 18, 46), (x + w - 22, 54)]:
        draw.line([px, base, px, base - ph], fill=(20, 12, 34), width=4)
        for a in range(-70, 71, 35):
            import math
            ex = px + int(20 * math.sin(math.radians(a)))
            ey = base - ph - int(12 * math.cos(math.radians(a)))
            draw.line([px, base - ph, ex, ey], fill=(20, 12, 34), width=3)

def illo_summit(draw, x, y, w, h):
    """Three flagpoles (US / China / Russia) before a Shenzhen skyline."""
    draw.rectangle([x, y, x + w, y + h], fill=(168, 205, 232))
    draw.ellipse([x + w - 34, y + 10, x + w - 10, y + 34], fill=(255, 240, 170))
    # skyline behind
    base = y + h - 18
    for i, hh in enumerate([40, 64, 48, 84, 56, 72, 44]):
        bx = x + 8 + i * (w - 16) // 7
        draw.rectangle([bx, base - hh, bx + (w - 16) // 7 - 4, base], fill=(120, 140, 160))
    draw.rectangle([x, base, x + w, y + h], fill=(96, 110, 96))
    # three poles + flags
    flags = [
        ("us", [(255, 255, 255), (178, 34, 52)]),
        ("cn", [(222, 41, 16)]),
        ("ru", [(255, 255, 255), (0, 57, 166), (213, 0, 50)]),
    ]
    fw, fh = 74, 34
    for i, (code, stripes) in enumerate(flags):
        px = x + 12 + i * 105
        draw.line([px, y + 14, px, base], fill=(40, 40, 40), width=3)
        fx, fy = px + 2, y + 16
        if code == "us":
            for s in range(7):
                draw.rectangle([fx, fy + s * fh // 7, fx + fw, fy + (s + 1) * fh // 7],
                               fill=stripes[s % 2])
            draw.rectangle([fx, fy, fx + 30, fy + fh // 2], fill=(30, 50, 120))
            for sy in range(3):
                for sx in range(4):
                    draw.ellipse([fx + 4 + sx * 7, fy + 4 + sy * 6, fx + 7 + sx * 7, fy + 7 + sy * 6],
                                 fill=(255, 255, 255))
        elif code == "cn":
            draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16))
            draw.ellipse([fx + 6, fy + 5, fx + 16, fy + 15], fill=(255, 222, 0))
            for sx, sy in [(22, 6), (28, 12), (26, 19), (19, 17)]:
                draw.ellipse([fx + sx, fy + sy, fx + sx + 4, fy + sy + 4], fill=(255, 222, 0))
        else:
            for s, c in enumerate(stripes):
                draw.rectangle([fx, fy + s * fh // 3, fx + fw, fy + (s + 1) * fh // 3], fill=c)
    # table line
    draw.rectangle([x + 30, base - 2, x + w - 30, base + 2], fill=(60, 60, 60))

def illo_voyager(draw, x, y, w, h):
    """Black space, stars, gold dish probe, small Sun, trajectory."""
    draw.rectangle([x, y, x + w, y + h], fill=(8, 10, 26))
    import random
    rnd = random.Random(19)
    for _ in range(70):
        sx, sy = x + rnd.randint(2, w - 2), y + rnd.randint(2, h - 2)
        r = rnd.choice([1, 1, 1, 2])
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))
    # small Sun bottom-left
    draw.ellipse([x + 12, y + h - 30, x + 34, y + h - 8], fill=(255, 220, 90))
    # trajectory
    draw.line([x + 30, y + h - 20, x + w - 60, y + 34], fill=(120, 160, 220), width=2)
    # probe: gold dish + body + boom
    cx, cy = x + w - 62, y + 40
    draw.ellipse([cx - 30, cy - 26, cx + 30, cy + 26], outline=(255, 200, 60), width=4)
    draw.ellipse([cx - 30, cy - 26, cx + 30, cy + 26], fill=(255, 200, 60))
    draw.ellipse([cx - 12, cy - 10, cx + 12, cy + 10], fill=(200, 140, 20))
    draw.rectangle([cx - 8, cy + 8, cx + 8, cy + 34], fill=(180, 180, 190))
    draw.line([cx + 8, cy + 20, cx + 44, cy + 44], fill=(200, 200, 210), width=3)
    draw.line([cx - 8, cy + 20, cx - 40, cy + 46], fill=(200, 200, 210), width=3)

BIG_ILLOS = [illo_vice_city, illo_summit, illo_voyager]

# ------------------------------------------------------- small flat icons
def icon_capitol(draw, x, y, s):
    draw.rectangle([x, y + s * 0.62, x + s, y + s * 0.72], fill=(70, 90, 120))
    draw.polygon([(x + s * 0.5, y + s * 0.18), (x + s * 0.18, y + s * 0.62), (x + s * 0.82, y + s * 0.62)], fill=(70, 90, 120))
    draw.rectangle([x + s * 0.46, y + s * 0.06, x + s * 0.54, y + s * 0.2], fill=(70, 90, 120))
    for i in range(4):
        draw.rectangle([x + s * 0.12 + i * s * 0.22, y + s * 0.72, x + s * 0.2 + i * s * 0.22, y + s * 0.94], fill=(70, 90, 120))

def icon_blast(draw, x, y, s):
    draw.polygon([(x + s * 0.5, y + s * 0.05), (x + s * 0.68, y + s * 0.3), (x + s * 0.95, y + s * 0.35),
                  (x + s * 0.72, y + s * 0.55), (x + s * 0.8, y + s * 0.85), (x + s * 0.5, y + s * 0.68),
                  (x + s * 0.2, y + s * 0.85), (x + s * 0.28, y + s * 0.55), (x + s * 0.05, y + s * 0.35),
                  (x + s * 0.32, y + s * 0.3)], fill=(230, 120, 30))
    draw.ellipse([x + s * 0.32, y + s * 0.32, x + s * 0.68, y + s * 0.68], fill=(255, 220, 60))

def icon_cyclone(draw, x, y, s):
    import math
    cx, cy = x + s / 2, y + s / 2
    for k in range(3):
        pts = []
        for t in range(0, 300, 12):
            r = 4 + t / 300 * (s / 2 - 4)
            a = math.radians(t + k * 120)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a) * 0.85))
        draw.line(pts, fill=(40, 110, 170), width=3)

def icon_euro(draw, x, y, s):
    draw.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], fill=(255, 205, 0), outline=(150, 110, 0), width=2)
    f = font(SANS_B, int(s * 0.62))
    draw.text((x + s * 0.24, y + s * 0.14), "E", font=f, fill=(20, 60, 140))

def icon_stamp(draw, x, y, s):
    draw.rectangle([x + 2, y + s * 0.1, x + s - 2, y + s * 0.9], outline=(178, 34, 34), width=3)
    f = font(SANS_B, int(s * 0.42))
    draw.text((x + s * 0.3, y + s * 0.26), "AU", font=f, fill=(178, 34, 34))
    draw.line([x + s * 0.08, y + s * 0.78, x + s * 0.92, y + s * 0.78], fill=(178, 34, 34), width=2)

def icon_chip(draw, x, y, s):
    draw.rectangle([x + s * 0.18, y + s * 0.18, x + s * 0.82, y + s * 0.82], fill=(30, 110, 60))
    draw.rectangle([x + s * 0.36, y + s * 0.36, x + s * 0.64, y + s * 0.64], fill=(200, 230, 210))
    for i in range(3):
        draw.line([x + s * 0.3 + i * s * 0.2, y + s * 0.06, x + s * 0.3 + i * s * 0.2, y + s * 0.18], fill=(30, 110, 60), width=3)
        draw.line([x + s * 0.3 + i * s * 0.2, y + s * 0.82, x + s * 0.3 + i * s * 0.2, y + s * 0.94], fill=(30, 110, 60), width=3)
        draw.line([x + s * 0.06, y + s * 0.3 + i * s * 0.2, x + s * 0.18, y + s * 0.3 + i * s * 0.2], fill=(30, 110, 60), width=3)
        draw.line([x + s * 0.82, y + s * 0.3 + i * s * 0.2, x + s * 0.94, y + s * 0.3 + i * s * 0.2], fill=(30, 110, 60), width=3)

def icon_tanker(draw, x, y, s):
    draw.polygon([(x + s * 0.08, y + s * 0.55), (x + s * 0.9, y + s * 0.55), (x + s * 0.78, y + s * 0.78),
                  (x + s * 0.2, y + s * 0.78)], fill=(90, 60, 40))
    draw.rectangle([x + s * 0.6, y + s * 0.3, x + s * 0.72, y + s * 0.55], fill=(90, 60, 40))
    draw.line([x + s * 0.05, y + s * 0.86, x + s * 0.95, y + s * 0.86], fill=(40, 110, 170), width=3)
    draw.ellipse([x + s * 0.2, y + s * 0.12, x + s * 0.3, y + s * 0.22], fill=(230, 120, 30))
    draw.ellipse([x + s * 0.34, y + s * 0.06, x + s * 0.46, y + s * 0.18], fill=(230, 120, 30))

def icon_tank(draw, x, y, s):
    draw.rectangle([x + s * 0.08, y + s * 0.45, x + s * 0.82, y + s * 0.68], fill=(70, 90, 60))
    draw.rectangle([x + s * 0.3, y + s * 0.28, x + s * 0.56, y + s * 0.48], fill=(70, 90, 60))
    draw.line([x + s * 0.56, y + s * 0.36, x + s * 0.95, y + s * 0.3], fill=(50, 65, 45), width=4)
    for i in range(4):
        draw.ellipse([x + s * 0.14 + i * s * 0.17, y + s * 0.68, x + s * 0.26 + i * s * 0.17, y + s * 0.8], fill=(40, 40, 40))

def icon_ballot(draw, x, y, s):
    draw.rectangle([x + s * 0.14, y + s * 0.4, x + s * 0.86, y + s * 0.88], fill=(60, 90, 160))
    draw.rectangle([x + s * 0.36, y + s * 0.3, x + s * 0.64, y + s * 0.42], fill=(40, 60, 120))
    draw.line([x + s * 0.3, y + s * 0.62, x + s * 0.46, y + s * 0.74], fill=(255, 255, 255), width=3)
    draw.line([x + s * 0.46, y + s * 0.74, x + s * 0.74, y + s * 0.5], fill=(255, 255, 255), width=3)

def icon_crown(draw, x, y, s):
    draw.polygon([(x + s * 0.1, y + s * 0.75), (x + s * 0.1, y + s * 0.35), (x + s * 0.3, y + s * 0.55),
                  (x + s * 0.5, y + s * 0.2), (x + s * 0.7, y + s * 0.55), (x + s * 0.9, y + s * 0.35),
                  (x + s * 0.9, y + s * 0.75)], fill=(200, 160, 40))
    draw.ellipse([x + s * 0.44, y + s * 0.1, x + s * 0.56, y + s * 0.22], fill=(178, 34, 34))

SMALL_ICONS = {4: icon_capitol, 5: icon_blast, 6: icon_cyclone, 7: icon_euro,
               8: icon_stamp, 9: icon_chip, 10: icon_tanker, 11: icon_tank,
               12: icon_ballot, 13: icon_crown}

# ------------------------------------------------------- world map
CONTINENTS = [
    ("NORTH AMERICA", (201, 214, 192), [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70), (-80, 73), (-65, 62), (-55, 52), (-60, 47), (-70, 42), (-75, 35), (-80, 26), (-84, 30), (-90, 21), (-97, 16), (-94, 17), (-105, 20), (-110, 24), (-117, 33), (-125, 40), (-125, 49), (-135, 58), (-155, 58), (-165, 60)]),
    ("GREENLAND", (201, 214, 192), [(-58, 64), (-45, 60), (-30, 68), (-25, 70), (-40, 76), (-55, 76), (-60, 74)]),
    ("SOUTH AMERICA", (216, 201, 163), [(-79, 9), (-72, 11), (-62, 10), (-52, 5), (-50, 0), (-44, -3), (-35, -8), (-40, -20), (-48, -28), (-58, -35), (-65, -41), (-70, -50), (-73, -54), (-72, -40), (-70, -20), (-77, -12), (-80, -5), (-81, 0)]),
    ("EUROPE", (195, 207, 224), [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (3, 53), (8, 57), (10, 59), (18, 56), (21, 55), (24, 58), (28, 59), (30, 60), (23, 65), (18, 69), (12, 70), (5, 60), (-2, 58), (-5, 55), (-10, 52), (-10, 44), (-2, 37), (0, 39)]),
    ("AFRICA", (224, 201, 168), [(-6, 35), (10, 37), (20, 32), (32, 31), (35, 28), (38, 22), (43, 12), (48, 11), (51, 10), (46, 0), (40, -10), (36, -18), (32, -26), (28, -33), (20, -35), (16, -28), (12, -18), (9, -2), (9, 4), (-8, 4), (-13, 8), (-17, 15), (-17, 21), (-10, 31)]),
    ("ASIA", (211, 184, 176), [(30, 60), (40, 68), (55, 69), (70, 72), (90, 75), (110, 74), (130, 72), (150, 70), (170, 66), (178, 65), (170, 60), (162, 56), (158, 52), (142, 50), (140, 45), (135, 43), (130, 38), (127, 35), (122, 32), (120, 28), (114, 22), (108, 18), (105, 10), (100, 8), (98, 12), (94, 17), (89, 22), (86, 20), (80, 13), (77, 8), (75, 12), (72, 20), (66, 25), (61, 25), (57, 26), (52, 28), (48, 30), (44, 29), (40, 32), (36, 36), (33, 41), (30, 46), (28, 50), (30, 55)]),
    ("OCEANIA", (192, 201, 176), [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35), (140, -38), (146, -39), (150, -37), (153, -32), (153, -27), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)]),
]

# ------------------------------------------------------- page assembly
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    f_kick = font(SANS_B, 14)
    kick = "45 STORIES  ·  6 CONTINENTS  ·  ONE DAY"
    d.text(((W - d.textlength(kick, font=f_kick)) / 2, 10), kick, font=f_kick, fill=RED)
    f_mast = font(SERIF_B, 46)
    mast = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(mast, font=f_mast)) / 2, 30), mast, font=f_mast, fill=INK)
    f_date = font(SANS_B, 17)
    date = "THURSDAY, 19 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 82), date, font=f_date, fill=INK)
    d.rectangle([14, 106, W - 14, 109], fill=RULE)
    d.rectangle([14, 112, W - 14, 113], fill=RULE)

    # ---- big 3 ---------------------------------------------------------
    col_w, gap = 322, 14
    y0 = 120
    f_tag = font(SANS_B, 12)
    f_head = font(SERIF_B, 17)
    f_sum = font(SANS, 11)
    for i, (n, region, head, summ, _pin) in enumerate(BIG):
        x = 14 + i * (col_w + gap)
        BIG_ILLOS[i](d, x, y0, col_w, 106)
        d.rectangle([x, y0, x + col_w - 1, y0 + 105], outline=RULE, width=1)
        badge(d, x + 15, y0 + 15, n)
        ty = y0 + 112
        d.text((x, ty), region, font=f_tag, fill=RED)
        hy = ty + 16
        hy = draw_wrapped(d, x, hy, head, f_head, col_w, INK, leading=19, max_lines=2)
        draw_wrapped(d, x, hy + 2, summ, f_sum, col_w, (52, 50, 46), leading=13, max_lines=2)
    d.rectangle([14, 316, W - 14, 317], fill=RULE)

    # ---- small 10 ------------------------------------------------------
    f_stag = font(SANS_B, 10)
    f_shead = font(SANS_B, 14)
    f_ssum = font(SANS, 11)
    row_h, scol_w = 56, 490
    for i, (n, region, head, summ, _pin) in enumerate(SMALL):
        col = i % 2
        row = i // 2
        x = 14 + col * (scol_w + 16)
        y = 324 + row * row_h
        SMALL_ICONS[n](d, x, y + 4, 40)
        badge(d, x + 9, y + 12, n, r=8)
        tx = x + 50
        d.text((tx, y + 1), "%d  ·  %s" % (n, region), font=f_stag, fill=RED)
        d.text((tx, y + 15), head, font=f_shead, fill=INK)
        draw_wrapped(d, tx, y + 32, summ, f_ssum, scol_w - 50, (52, 50, 46), leading=12, max_lines=2)
    d.rectangle([14, 608, W - 14, 609], fill=RULE)

    # ---- also on (left column) -----------------------------------------
    f_sec = font(SANS_B, 13)
    d.text((14, 616), "ALSO ON THURSDAY 19 NOVEMBER", font=f_sec, fill=INK)
    d.rectangle([14, 634, 496, 635], fill=RULE)
    f_item = font(SANS, 10)
    ly = 638
    for i, item in enumerate(ALSO):
        num = 14 + i
        d.text((14, ly), "%d." % num, font=font(SANS_B, 10), fill=RED)
        d.text((40, ly), item, font=f_item, fill=INK)
        ly += 10.5
    # ly ends ~992; footer will sit below the map column instead

    # ---- map (right column) --------------------------------------------
    mx0, mx1, my0, my1 = 516, 1010, 640, 828
    d.text((mx0, 616), "WHERE IT HAPPENED", font=f_sec, fill=INK)
    d.rectangle([mx0, 634, mx1, 635], fill=RULE)
    d.rectangle([mx0, my0, mx1, my1], fill=SEA, outline=RULE, width=1)
    mw, mh = mx1 - mx0, my1 - my0

    def project(lon, lat):
        return (mx0 + (lon + 180) / 360.0 * mw,
                my0 + (75 - lat) / 135.0 * mh)

    for name, color, poly in CONTINENTS:
        pts = [project(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=color, outline=(120, 115, 105))
    # pin true dots + numbered circles (Santa Clara offset to avoid Pasadena)
    pins = [(n, lon, lat) for (n, _r, _h, _s, (lon, lat)) in BIG + SMALL]
    f_pin = font(SANS_B, 11)
    for n, lon, lat in pins:
        px, py = project(lon, lat)
        ox, oy = px, py
        if n == 9:  # Santa Clara sits on Pasadena's pin; lift it with a leader
            ox, oy = px - 16, py - 16
            d.line([px, py, ox, oy], fill=RED, width=1)
        d.ellipse([ox - 8, oy - 8, ox + 8, oy + 8], fill=RED, outline=(255, 255, 255), width=2)
        tw = d.textlength(str(n), font=f_pin)
        d.text((ox - tw / 2, oy - 6), str(n), font=f_pin, fill=(255, 255, 255))
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
    # legend: two rows of three chips
    leg = [("NORTH AMERICA", (201, 214, 192)), ("SOUTH AMERICA", (216, 201, 163)),
           ("EUROPE", (195, 207, 224)), ("AFRICA", (224, 201, 168)),
           ("ASIA", (211, 184, 176)), ("OCEANIA", (192, 201, 176))]
    f_leg = font(SANS_B, 10)
    for i, (name, color) in enumerate(leg):
        lx = mx0 + (i % 3) * 166
        ly2 = 838 + (i // 3) * 18
        d.rectangle([lx, ly2 + 1, lx + 14, ly2 + 11], fill=color, outline=RULE)
        d.text((lx + 18, ly2), name, font=f_leg, fill=INK)
    f_note = font(SANS, 10)
    note = "Pins 1-13 mark the illustrated stories above."
    d.text((mx0, 878), note, font=f_note, fill=MUTED)
    # stats strip
    d.rectangle([mx0, 896, mx1, 924], outline=RULE, width=1)
    f_stat = font(SANS_B, 11)
    stat = "45 STORIES  ·  13 ILLUSTRATED  ·  32 BRIEFS  ·  6 CONTINENTS"
    d.text(((mx0 + mx1 - d.textlength(stat, font=f_stat)) / 2, 904), stat, font=f_stat, fill=INK)

    # ---- footer --------------------------------------------------------
    f_foot = font(SANS, 10)
    src = "Sources: Reuters, AP, AFP, BBC, Al Jazeera, WHO, UN. Original drawings."
    d.text(((W - d.textlength(src, font=f_foot)) / 2, 984), src, font=f_foot, fill=MUTED)
    faith = ("Every story here happened or was first reported on Thursday 19 November 2026. "
             "Contested claims are marked as claims.")
    d.text(((W - d.textlength(faith, font=f_foot)) / 2, 999), faith, font=f_foot, fill=MUTED)
    return img

if __name__ == "__main__":
    page = build()
    page.save(OUT, optimize=True)
    size = os.path.getsize(OUT)
    print("wrote", OUT, size, "bytes", "OK" if size <= 1048576 else "TOO BIG")
