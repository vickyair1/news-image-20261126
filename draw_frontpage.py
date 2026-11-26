#!/usr/bin/env python3
"""Draw the 26 November 2026 one-day world news front page (1024x1024).

Fresh build for make.fun bounty news-image-20261126. All art is vector
shapes drawn with Pillow at build time; the output PNG is deterministic.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (246, 241, 229)
INK = (26, 26, 26)
RED = (163, 22, 33)
NAVY = (31, 42, 68)
MUTED = (107, 98, 87)
PANEL_BG = (255, 253, 246)
RULE = (26, 26, 26)
SEA = (223, 232, 234)
LAND = (217, 201, 163)
LAND_EDGE = (150, 135, 105)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


F_SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)
F_SANSB = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_lines(draw, x, y, lines, fnt, fill, leading=None):
    if leading is None:
        leading = fnt.size + 3
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- stories
# n, art, region, place, kicker, headline, deck, source, taxonomy
PANELS = [
    (1, "chart", "AMERICAS", "NEW YORK", "MARKETS",
     "AI rout deepens: Nasdaq sinks 4% into Thanksgiving",
     "Nvidia -7%, Micron -10%, AMD -9%; worst Nov since 2008.",
     "REUTERS \u00b7 BLOOMBERG", "CONFIRMED"),
    (2, "refinery", "EUROPE", "UKRAINE\u2013RUSSIA", "WAR",
     "Ukraine hits Russian refineries again",
     "Two refineries ablaze; Putin warns of retaliation.",
     "REUTERS", "REPORTED"),
    (3, "space", "ASIA-PACIFIC", "TOKYO\u2013DARMSTADT", "SPACE",
     "BepiColombo reaches Mercury at last",
     "ESA\u2013JAXA craft enters orbit after an eight-year journey.",
     "ESA \u00b7 JAXA \u00b7 REUTERS", "CONFIRMED"),
    (4, "fire", "AFRICA", "CAIRO", "DISASTER",
     "Tanker fire kills at least 30 near Cairo",
     "A fuel tanker crash ignites a highway fire; dozens hurt.",
     "AP \u00b7 REUTERS", "CONFIRMED"),
    (5, "chess", "EUROPE", "GENEVA", "CHESS",
     "Gukesh holds Sindarov in 20 moves",
     "World champion draws game two; the match is level.",
     "REUTERS \u00b7 SPORTSTAR", "CONFIRMED"),
    (6, "football", "AMERICAS", "NEW YORK", "HOLIDAY",
     "America sits down to Thanksgiving",
     "Markets shut; Macy's parade; three NFL games today.",
     "AP", "OFFICIAL"),
    (7, "plane", "AMERICAS", "MISSISSIPPI", "CRASH",
     "Six dead, two of them children, in plane crash",
     "A small plane comes down off the coast; probe opened.",
     "AP", "CONFIRMED"),
    (8, "stamp", "ASIA-PACIFIC", "PYONGYANG", "DIPLOMACY",
     "North Korea expels Swiss diplomat",
     "Swiss office ordered shut in a sanctions row.",
     "REUTERS", "REPORTED"),
    (9, "asteroid", "GLOBAL", "SPACE", "SCIENCE",
     "New close-ups of the asteroid we hit",
     "Images show the crater left by NASA's 2022 impact test.",
     "NASA \u00b7 BBC", "CONFIRMED"),
    (10, "cricket", "ASIA-PACIFIC", "INDIA", "CRICKET",
     "Sooryavanshi, 15, smashes 204 off 53 balls",
     "Fastest List A double century ever \u2014 a world record.",
     "PTI \u00b7 CRICBUZZ", "CONFIRMED"),
    (11, "court", "AFRICA", "PRETORIA", "COURTS",
     "Court backs Ramaphosa in cash case",
     "President wins fight over Phala Phala cash case.",
     "REUTERS", "REPORTED"),
    (12, "shirt", "ASIA-PACIFIC", "DHAKA", "WORK",
     "Bangladesh lifts garment pay 36%",
     "Minimum wage rises for millions of garment workers.",
     "REUTERS", "CONFIRMED"),
]

# n, place, headline, source  (one line each in the brief band)
BRIEF = [
    (13, "LEBANON", "Second airport planned at Kleiat", "REUTERS"),
    (14, "LONDON", "UK moves jets as drone threat grows", "REUTERS"),
    (15, "KUALA LUMPUR", "Malaysia sues Google for $146m", "REUTERS"),
    (16, "WEST JAVA", "Nine miners dead as gold mine floods", "AP"),
    (17, "NEW YORK", "Tempus buys Personalis for $600m", "INVESTING.COM"),
    (18, "BENGALURU", "Flipkart chief to step down in Dec", "REUTERS"),
    (19, "DHAKA", "Hasina seeks return to Bangladesh 16 Dec", "AP"),
    (20, "KOSHI", "Quake of 5.6 shakes Nepal near China", "AP"),
    (21, "RAS AL KHAIMAH", "Road crash kills 11 in the UAE", "AP"),
    (22, "INDIA", "NZ hold India to a draw in 1st Test", "AP"),
    (23, "MUMBAI", "1,220 players in for IPL 2027 auction", "PTI"),
    (24, "WASHINGTON", "Meta meets Congress on suspensions", "AP"),
    (25, "WASHINGTON", "AG dodges questions on Nvidia probe", "AP"),
    (26, "WASHINGTON", "Fed split over high inflation causes", "REUTERS"),
    (27, "NEW YORK", "Anthropic dips below IPO price", "BLOOMBERG"),
    (28, "NEW DELHI", "India gives Nepal a \u20b915,000-crore package", "PTI"),
    (29, "NEW DELHI", "Modi meets Germany's Merz", "PTI"),
    (30, "NEW DELHI", "IITs to add 6,000 seats in AI and space", "PTI"),
    (31, "NEW DELHI", "India's space economy set to hit $45bn", "PTI"),
    (32, "MUMBAI", "Sensex falls 1,484; Nifty below 25,400", "PTI"),
    (33, "LONDON", "Duran Duran guitarist Andy Taylor dies, 65", "AP"),
    (34, "JERUSALEM", "Likud appeals Israeli election results", "JPOST"),
    (35, "LONDON", "UK warns firms of sabotage threat", "REUTERS"),
    (36, "BRAZIL", "Wolbachia mosquitoes cut infections 68%", "WMP STUDY"),
    (37, "NEW DELHI", "Constitution Day; 18 years since 26/11", "PTI"),
    (38, "NFL", "Bears\u2013Lions, Eagles\u2013Cowboys, Chiefs\u2013Bills", ""),
    (39, "NEW YORK", "Nvidia debt put on CreditWatch", "S&P GLOBAL"),
    (40, "INGLEWOOD", "Packers at Rams open Thanksgiving week", "NFL"),
]

NUMBERS = [
    ("-4%", "Nasdaq falls in the rout"),
    ("-7%", "Nvidia drops as chips slide"),
    ("3.3%", "Core PCE inflation, Oct y/y"),
    ("30", "killed in Cairo tanker fire"),
    ("36%", "Bangladesh garment pay rise"),
    ("1,220", "IPL 2027 auction entries"),
]

TALLY = [("AMERICAS", 12), ("EUROPE", 6), ("ASIA-PACIFIC", 15),
         ("MIDDLE EAST", 3), ("AFRICA", 2), ("OCEANIA", 1), ("GLOBAL", 1)]

# pin positions: story n -> (lon, lat)
PINS = {
    1: (-74.0, 40.7), 2: (35.0, 53.0), 3: (139.7, 35.7), 4: (31.2, 30.0),
    5: (6.1, 46.2), 6: (-85.0, 43.0), 7: (-91.0, 29.0), 8: (125.8, 39.0),
    9: (-118.1, 34.1), 10: (77.2, 28.6), 11: (28.0, -26.2), 12: (90.4, 23.8),
}

CONTINENTS = {
    "namerica": [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69),
                 (-85, 66), (-80, 73), (-65, 60), (-55, 47), (-60, 45),
                 (-70, 42), (-75, 35), (-80, 26), (-85, 20), (-90, 14),
                 (-95, 16), (-105, 20), (-110, 23), (-115, 30), (-125, 40),
                 (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    "samerica": [(-80, 10), (-75, 5), (-70, 12), (-60, 8), (-50, 0),
                 (-45, -5), (-40, -10), (-35, -8), (-40, -20), (-48, -28),
                 (-55, -35), (-65, -40), (-70, -50), (-73, -55), (-75, -40),
                 (-80, -20), (-80, -5)],
    "africa": [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31),
               (35, 28), (40, 20), (43, 12), (48, 11), (51, 10), (44, 0),
               (40, -10), (35, -20), (30, -30), (20, -35), (15, -30),
               (12, -18), (13, -10), (8, 4), (0, 5), (-8, 5)],
    "eurasia": [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57),
                (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62),
                (40, 68), (55, 69), (70, 72), (90, 75), (110, 76),
                (130, 72), (150, 70), (170, 66), (178, 65), (170, 60),
                (160, 55), (158, 50), (145, 45), (140, 40), (135, 35),
                (130, 33), (127, 35), (122, 38), (120, 30), (115, 23),
                (110, 20), (108, 12), (105, 8), (100, 8), (97, 15),
                (92, 20), (88, 22), (80, 15), (77, 8), (75, 12), (72, 20),
                (68, 23), (62, 25), (58, 25), (55, 26), (52, 28), (50, 30),
                (48, 30), (44, 29), (40, 32), (36, 36), (30, 36), (26, 38),
                (22, 37), (19, 40), (15, 44), (12, 44), (8, 44), (3, 43),
                (0, 40), (-2, 37), (-6, 36), (-9, 37)],
    "australia": [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32),
                  (130, -32), (135, -35), (140, -38), (145, -38), (150, -37),
                  (153, -32), (153, -27), (150, -22), (146, -19), (142, -15),
                  (142, -11), (137, -12), (135, -15), (132, -12), (130, -13),
                  (126, -14), (122, -17), (118, -20)],
}


# ---------------------------------------------------------------- art scenes
def art_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 32, 56))
    step = max(4, (h - 20) // 5)
    for i in range(5):
        bx = x + 12 + i * ((w - 24) // 5)
        bh = 8 + i * step
        d.rectangle([bx, y + h - 8 - bh, bx + 16, y + h - 8], fill=(90, 110, 150))
    pts = [(x + 8, y + 14), (x + w // 4, y + 26), (x + w // 2, y + 30),
           (x + 3 * w // 4, y + 52), (x + w - 8, y + h - 14)]
    d.line(pts, fill=(220, 60, 50), width=4)
    d.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4],
              fill=(220, 60, 50))


def art_refinery(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 44, 38))
    th = min(28, h - 8)
    for i, tw in enumerate((14, 20, 12)):
        tx = x + 16 + i * 26
        d.rectangle([tx, y + h - 6 - th, tx + tw, y + h - 6],
                    fill=(120, 110, 100))
        d.polygon([(tx, y + h - 6 - th), (tx + tw, y + h - 6 - th),
                   (tx + tw // 2, y + h - 6 - th - 8)], fill=(200, 90, 30))
    sr = min(13, h // 2 - 4)
    scx, scy = x + w - 34, y + h // 2
    d.ellipse([scx - sr, scy - sr, scx + sr, scy + sr], fill=(240, 160, 40))
    d.polygon([(scx - 6, scy + sr - 2), (scx + 6, scy + sr - 2),
               (scx, scy + sr + 10)], fill=(220, 80, 30))


def art_space(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 12, 28))
    for sx, sy in ((18, 12), (48, 26), (90, 10), (120, 30), (150, 14)):
        if sy < h - 4:
            d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2],
                      fill=(255, 255, 255))
    r = min(18, h // 2 - 3)
    cx, cy = x + w - 30, y + h - r - 3
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 120, 60))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(150, 80, 40))
    top = y + max(6, h // 3)
    d.polygon([(x + 30, y + h - 8), (x + 52, y + h - 8), (x + 44, top),
               (x + 38, top)], fill=(230, 230, 230))
    d.polygon([(x + 38, top), (x + 44, top), (x + 41, y + 4)],
              fill=(200, 60, 40))


def art_fire(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 30, 26))
    d.rectangle([x, y + h - 14, x + w, y + h - 6], fill=(70, 70, 70))
    d.rectangle([x + 14, y + h - 30, x + 70, y + h - 14], fill=(180, 60, 30))
    d.rectangle([x + 74, y + h - 26, x + 96, y + h - 14], fill=(120, 40, 20))
    for fx, fh, col in ((x + 100, 12, (240, 140, 30)), (x + 118, 16, (230, 80, 20)),
                        (x + 136, 10, (250, 180, 50))):
        fh = min(fh, h - 18)
        d.polygon([(fx, y + h - 14), (fx + 12, y + h - 14),
                   (fx + 6, y + h - 14 - fh)], fill=col)


def art_chess(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 220, 196))
    sq = min(w, h) // 4
    ox, oy = x + (w - sq * 4) // 2, y + (h - sq * 4) // 2
    for r in range(4):
        for c in range(4):
            if (r + c) % 2:
                d.rectangle([ox + c * sq, oy + r * sq,
                             ox + (c + 1) * sq, oy + (r + 1) * sq],
                            fill=(60, 50, 40))
    d.ellipse([ox + sq + 3, oy + sq + 3, ox + 2 * sq - 3, oy + 2 * sq - 3],
              fill=(255, 255, 255), outline=(0, 0, 0))
    d.ellipse([ox + 2 * sq + 3, oy + 2 * sq + 3, ox + 3 * sq - 3,
               oy + 3 * sq - 3], fill=(20, 20, 20))


def art_football(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 60, 20))
    cx, cy = x + w // 2, y + h // 2
    rx, ry = min(52, w // 2 - 8), max(8, h // 2 - 3)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(110, 55, 25),
              outline=(240, 220, 200), width=2)
    d.line([(cx - rx // 2, cy), (cx + rx // 2, cy)], fill=(240, 220, 200),
           width=3)
    for lx in range(-rx // 3, rx // 3 + 1, 9):
        d.line([(cx + lx, cy - 6), (cx + lx, cy + 6)], fill=(240, 220, 200),
               width=2)
    d.text((x + 8, y + 3), "THANKSGIVING", font=F_SANSB(10), fill=(255, 235, 200))


def art_plane(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(70, 130, 170))
    d.polygon([(x + 20, y + 16), (x + 90, y + 22), (x + 20, y + 28)],
              fill=(240, 240, 240))
    d.polygon([(x + 40, y + 22), (x + 55, y + 34), (x + 48, y + 22)],
              fill=(200, 200, 200))
    for wy in range(y + h - 16, y + h - 2, 5):
        d.arc([x + 10, wy - 4, x + w - 10, wy + 8], 0, 180, fill=(255, 255, 255))


def art_stamp(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 228, 210))
    d.rectangle([x + 16, y + 10, x + w - 60, y + h - 10], fill=(250, 248, 240),
                outline=(26, 26, 26))
    for ly in range(y + 18, y + h - 14, 8):
        d.line([(x + 22, ly), (x + w - 66, ly)], fill=(150, 140, 120))
    sr = min(16, h // 2 - 4)
    scx, scy = x + w - 30, y + h // 2
    d.ellipse([scx - sr, scy - sr, scx + sr, scy + sr], outline=(180, 30, 30),
              width=3)
    d.line([(scx - sr + 3, scy - sr + 3), (scx + sr - 3, scy + sr - 3)],
           fill=(180, 30, 30), width=3)
    d.line([(scx + sr - 3, scy - sr + 3), (scx - sr + 3, scy + sr - 3)],
           fill=(180, 30, 30), width=3)


def art_asteroid(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 12, 22))
    cx, cy = x + w // 2, y + h // 2 + 2
    r = min(20, h // 2 - 2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 145, 135))
    for crx, cry, cr in ((cx - r // 3, cy - r // 4, max(2, r // 4)),
                         (cx + r // 3, cy + r // 5, max(2, r // 4)),
                         (cx + r // 10, cy - r // 2, max(2, r // 5))):
        d.ellipse([crx - cr, cry - cr, crx + cr, cry + cr], fill=(105, 100, 90))
    d.polygon([(x + 14, y + 10), (x + 30, y + 14), (x + 14, y + 18)],
              fill=(220, 220, 220))


def art_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 120, 60))
    d.rectangle([x + 30, y + 8, x + w - 30, y + h - 8], fill=(190, 170, 120))
    d.rectangle([x + w // 2 - 4, y + 12, x + w // 2 + 4, y + h - 12],
                fill=(230, 220, 200))
    d.ellipse([x + w - 34, y + 10, x + w - 20, y + 24], fill=(200, 40, 30))
    d.text((x + 10, y + h - 30), "204", font=F_SANSB(26), fill=(255, 255, 255))


def art_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 200, 180))
    d.polygon([(x + 10, y + 14), (x + w - 10, y + 14), (x + w // 2, y + 2)],
              fill=(120, 100, 80))
    for i in range(4):
        cx = x + 20 + i * ((w - 40) // 3)
        d.rectangle([cx, y + 16, cx + 8, y + h - 8], fill=(240, 235, 220))
    d.rectangle([x + 10, y + h - 8, x + w - 10, y + h - 2], fill=(120, 100, 80))


def art_shirt(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(90, 140, 160))
    cx, cy = x + w // 2, y + h // 2
    s = min(22, h // 2 - 2)
    d.polygon([(cx - s, cy - s + 6), (cx - s - 16, cy - 2), (cx - s - 6, cy + 8),
               (cx - s, cy + 4), (cx - s, cy + s), (cx + s, cy + s),
               (cx + s, cy + 4), (cx + s + 6, cy + 8), (cx + s + 16, cy - 2),
               (cx + s, cy - s + 6)], fill=(245, 245, 240),
              outline=(26, 26, 26))
    d.text((x + 8, y + 3), "36%", font=F_SANSB(14), fill=(255, 255, 255))


ART = {"chart": art_chart, "refinery": art_refinery, "space": art_space,
       "fire": art_fire, "chess": art_chess, "football": art_football,
       "plane": art_plane, "stamp": art_stamp, "asteroid": art_asteroid,
       "cricket": art_cricket, "court": art_court, "shirt": art_shirt}


# ---------------------------------------------------------------- page build
def blit_art(img, art_fn, x, y, w, h):
    """Draw one art scene clipped exactly to its box (no bleed)."""
    tmp = Image.new("RGB", (w, h), (0, 0, 0))
    td = ImageDraw.Draw(tmp)
    art_fn(td, 0, 0, w, h)
    img.paste(tmp, (x, y))


def draw_panel(img, d, story, x, y, w, h, art_h, head_size):
    n, art, region, place, kicker, headline, deck, source, tax = story
    d.rectangle([x, y, x + w, y + h], fill=PANEL_BG, outline=RULE)
    blit_art(img, ART[art], x + 1, y + 1, w - 2, art_h)
    ty = y + art_h + 3
    d.text((x + 8, ty), "%d  %s \u00b7 %s \u00b7 %s" % (n, kicker, place, region),
           font=F_SANSB(9), fill=RED)
    ty += 13
    lines = wrap(d, headline, F_SERIF(head_size), w - 16)
    ty = text_lines(d, x + 8, ty, lines[:2], F_SERIF(head_size), INK,
                    head_size + 2)
    d.text((x + 8, ty + 1), deck, font=F_SANS(10), fill=(60, 60, 60))
    d.text((x + 8, y + h - 12), "%s  \u00b7  %s" % (source, tax),
           font=F_SANSB(8), fill=MUTED)


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=RULE)
    d.text((x + 8, y + 4), "WHERE IT HAPPENED \u2014 PINS = STORY NUMBERS",
           font=F_SANSB(10), fill=NAVY)
    my0, my1 = y + 18, y + h - 3
    mh = my1 - my0

    def px(lon, lat):
        return (x + (lon + 180.0) / 360.0 * w,
                my0 + (75.0 - lat) / 150.0 * mh)

    for name, pts in CONTINENTS.items():
        d.polygon([px(lon, lat) for lon, lat in pts], fill=LAND,
                  outline=LAND_EDGE)
    for lon, lat, r in ((-2, 54, 3), (138, 37, 4), (113, -2, 4), (172, -41, 3)):
        cx, cy = px(lon, lat)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=LAND,
                  outline=LAND_EDGE)
    for n, (lon, lat) in sorted(PINS.items()):
        cx, cy = px(lon, lat)
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED,
                  outline=(255, 255, 255), width=2)
        label = str(n)
        tw = d.textlength(label, font=F_SANSB(8))
        d.text((cx - tw / 2, cy - 5), label, font=F_SANSB(8),
               fill=(255, 255, 255))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 16  # side margin

    # top bar: 0-24
    d.rectangle([0, 0, W, 24], fill=INK)
    d.text((M, 5), "THE WORLD IN ONE DAY", font=F_SANSB(12), fill=(255, 255, 255))
    right = "EVERY STORY DATED THURSDAY 26 NOV 2026"
    d.text((W - M - d.textlength(right, font=F_SANSB(11)), 6), right,
           font=F_SANSB(11), fill=(255, 255, 255))

    # masthead: date 28-80, red rule 96, kicker 102, tally 120, rule 136
    date = "Thursday 26 November 2026"
    dw = d.textlength(date, font=F_SERIF(52))
    d.text(((W - dw) / 2, 28), date, font=F_SERIF(52), fill=INK)
    d.rectangle([M, 96, W - M, 99], fill=RED)
    kick = "Wall Street's AI rout  \u00b7  Thanksgiving in America  \u00b7  Mercury, at last"
    d.text(((W - d.textlength(kick, font=F_SANS(13))) / 2, 104), kick,
           font=F_SANS(13), fill=(60, 60, 60))
    tally = "40 STORIES  \u00b7  " + "  \u00b7  ".join(
        "%s %d" % (name, cnt) for name, cnt in TALLY)
    d.text(((W - d.textlength(tally, font=F_SANSB(11))) / 2, 122), tally,
           font=F_SANSB(11), fill=INK)
    d.line([(M, 136), (W - M, 136)], fill=RULE, width=1)

    # numbers strip: 142-174
    bw = (W - 2 * M - 5 * 8) // 6
    for i, (val, cap) in enumerate(NUMBERS):
        bx = M + i * (bw + 8)
        d.rectangle([bx, 142, bx + bw, 174], outline=RULE)
        d.text((bx + 8, 144), val, font=F_SANSB(19), fill=RED)
        d.text((bx + 8, 164), cap, font=F_SANS(9), fill=(60, 60, 60))

    # timeline strip: 180, rule 196
    tl = ("WED 13:30 UTC  PCE 3.3%   \u25c6   WED 21:00 UTC  Nasdaq \u22124% at "
          "the close   \u25c6   THU 01:00 UTC  Packers\u2013Rams kick off   "
          "\u25c6   TODAY  Thanksgiving (US) \u00b7 Constitution Day (India) "
          "\u00b7 18 yrs since 26/11")
    d.text(((W - d.textlength(tl, font=F_SANS(10))) / 2, 180), tl,
           font=F_SANS(10), fill=(60, 60, 60))
    d.line([(M, 196), (W - M, 196)], fill=RULE, width=1)

    # lead story: 202-318
    lead = PANELS[0]
    _, art, region, place, kicker, headline, deck, source, tax = lead
    ly, lh = 202, 116
    d.rectangle([M, ly, W - M, ly + lh], fill=PANEL_BG, outline=RULE)
    blit_art(img, ART[art], M + 1, ly + 1, 330, lh - 2)
    tx = M + 342
    d.text((tx, ly + 8), "1  %s \u00b7 %s \u00b7 %s  \u2014  THE DAY'S LEAD"
           % (kicker, place, region), font=F_SANSB(10), fill=RED)
    lines = wrap(d, headline, F_SERIF(24), W - M - tx - 10)
    ty = text_lines(d, tx, ly + 26, lines[:2], F_SERIF(24), INK, 28)
    dlines = wrap(d, deck, F_SANS(12), W - M - tx - 10)
    ty = text_lines(d, tx, ty + 4, dlines[:2], F_SANS(12), (60, 60, 60), 15)
    d.text((tx, ly + lh - 16), "%s  \u00b7  %s" % (source, tax),
           font=F_SANSB(9), fill=MUTED)

    # panel rows A/B/C: 324-428, 536-640, 646-750
    colw = (W - 2 * M - 2 * 10) // 3
    rows = [(324, 104, PANELS[1:4]), (536, 104, PANELS[4:7]),
            (646, 104, PANELS[7:10])]
    for ry, rh, stories in rows:
        for i, story in enumerate(stories):
            draw_panel(img, d, story, M + i * (colw + 10), ry, colw, rh,
                       art_h=34, head_size=13)

    # map band: 434-530 (map left, tally bars right)
    my, mh = 434, 96
    map_w = 640
    draw_map(d, M, my, map_w, mh)
    rx = M + map_w + 12
    rw = W - M - rx
    d.text((rx, my + 2), "REGION TALLY \u2014 40 STORIES", font=F_SANSB(10),
           fill=RED)
    by = my + 16
    for name, cnt in TALLY:
        d.text((rx, by), name, font=F_SANS(9), fill=INK)
        bar_x = rx + 92
        bar_w = int((rw - 92 - 26) * cnt / 15.0)
        d.rectangle([bar_x, by + 1, bar_x + bar_w, by + 8], fill=RED)
        d.text((bar_x + bar_w + 4, by), str(cnt), font=F_SANSB(9), fill=INK)
        by += 11

    # row D: 756-842, panels 11/12 + DATE CHECK box
    ry, rh = 756, 86
    draw_panel(img, d, PANELS[10], M, ry, colw, rh, art_h=28, head_size=13)
    draw_panel(img, d, PANELS[11], M + colw + 10, ry, colw, rh, art_h=28,
               head_size=13)
    dx = M + 2 * (colw + 10)
    d.rectangle([dx, ry, dx + colw, ry + rh], outline=RED, width=2)
    d.text((dx + 8, ry + 5), "DATE CHECK", font=F_SANSB(11), fill=RED)
    check = ("Wires cutoff 00:00 UTC Thu 26 Nov. Every story happened, or "
             "was first reported, on 26 Nov. LEFT OUT \u2014 NOT 26 NOV: "
             "Shenzhou-24, the Solomon treaty, the leaked Russian toll, the "
             "Gaza strike, the Houthi refinery claim, the Hormuz mines, the "
             "Cartagena rescue, the Huawei verdict.")
    clines = wrap(d, check, F_SANS(9), colw - 16)
    text_lines(d, dx + 8, ry + 20, clines[:5], F_SANS(9), INK, 11)

    # brief band: header 848, cols 870-1000
    by0 = 848
    d.text((M, by0), "ALSO ON THURSDAY \u2014 28 MORE STORIES",
           font=F_SANSB(11), fill=RED)
    d.line([(M, by0 + 16), (W - M, by0 + 16)], fill=RULE, width=1)
    cols = [BRIEF[i::3] for i in range(3)]
    colw_b = (W - 2 * M - 2 * 16) // 3
    cy0 = by0 + 22
    for ci, col in enumerate(cols):
        cx = M + ci * (colw_b + 16)
        cy = cy0
        for n, place, headline, src in col:
            line = "%d \u00b7 %s \u2014 %s" % (n, place, headline)
            if src:
                line += " \u00b7 " + src
            d.text((cx, cy), line, font=F_SANSB(9), fill=INK)
            cy += 13

    # footer
    d.line([(M, 1004), (W - M, 1004)], fill=RULE, width=1)
    foot = ("Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 BBC \u00b7 AFP \u00b7 PTI "
            "\u00b7 ESA \u00b7 JAXA \u00b7 NFL  \u2014  All stories 26 November 2026  "
            "\u00b7  Wires cutoff 00:00 UTC")
    d.text(((W - d.textlength(foot, font=F_SANS(9))) / 2, 1009), foot,
           font=F_SANS(9), fill=MUTED)

    img.save(OUT, "PNG")
    return OUT


if __name__ == "__main__":
    print(build())
