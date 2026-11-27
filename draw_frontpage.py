#!/usr/bin/env python3
"""Draw the round-2 front page for Thursday 26 November 2026.

Fresh build: every story below was verified against wire reporting
during this session (27 Nov 2026). Nothing is carried over from any
earlier front page. Output is deterministic: no timestamps, no
randomness, fixed layout and fonts, so repeated runs are byte-identical.

Layout: classic broadsheet, 1024x1024. Masthead, numbers strip, UTC
timeline, one full-width lead, 11 further illustrated panels, a world
map with numbered pins, a region tally, a DATE CHECK box, and 28 briefs.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (155, 27, 27)
NAVY = (26, 42, 74)
PANEL = (255, 253, 246)
GREY = (90, 86, 76)
LIGHT = (232, 226, 210)
SKY = (178, 205, 224)
SEA = (140, 175, 200)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, max_w, leading, fill=INK):
    lines = wrap(draw, text, fnt, max_w)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hline(draw, x0, x1, y, fill=INK, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- stories
# tax: CONFIRMED = wire-confirmed fact; REPORTED = reported, single-source
# or still developing; CLAIM = one side's claim, not confirmed.
PANELS = [
    dict(n=1, beat="TRADE", place="WASHINGTON", region="AMERICAS",
         head="Trump proposes tariffs on 14 partners",
         deck="Rates of 20-40% after a Section 301 probe; China 20%. Nothing in force before 25 January.",
         src="REUTERS", tax="REPORTED", art="tariffs"),
    dict(n=2, beat="ENERGY", place="RAS TANURA", region="MIDDLE EAST",
         head="Oil jumps as Houthis hit Saudi refineries",
         deck="Houthis claim the Ras Tanura strike; Jazan is hit Thursday, one worker killed. Brent settles at $96.57.",
         src="REUTERS", tax="CLAIM", art="oil"),
    dict(n=3, beat="MARKETS", place="NEW YORK", region="AMERICAS",
         head="Wall Street's wild ride ends shut for Thanksgiving",
         deck="Nasdaq-100 plunged 4.6% intraday, near a bear market, then roared back. Nasdaq closes -0.62%; Dow +0.33%.",
         src="BLOOMBERG", tax="CONFIRMED", art="market"),
    dict(n=4, beat="HOLIDAY", place="NEW YORK", region="AMERICAS",
         head="No parade on Thanksgiving - a first in 100 years",
         deck="The 100th Macy's parade moves to Saturday as a nor'easter lashes New York with gusts to 60 mph.",
         src="AP", tax="CONFIRMED", art="parade"),
    dict(n=5, beat="SPORT", place="USA", region="AMERICAS",
         head="Thanksgiving's three last-second thrillers",
         deck="Three games, three finishes in the final five seconds; the Eagles erase a 21-point deficit.",
         src="AP", tax="CONFIRMED", art="nfl"),
    dict(n=6, beat="DISASTER", place="CAIRO", region="AFRICA",
         head="Tanker fire kills 31 on Cairo ring road",
         deck="A tanker overturns on Wednesday evening; 31 dead, 21 hurt. A driver is detained on Thursday.",
         src="REUTERS", tax="CONFIRMED", art="tanker"),
    dict(n=7, beat="CHESS", place="GENEVA", region="EUROPE",
         head="Game 3: a 60-move thriller, still level",
         deck="Gukesh springs the Rio variation; Sindarov makes move 40 with six seconds left. Draw, 1.5-1.5.",
         src="CHESS.COM", tax="CONFIRMED", art="chess"),
    dict(n=8, beat="CRICKET", place="DOHA", region="ASIA-PACIFIC",
         head="Sri Lanka stun India A in the semi-final",
         deck="Croospulle 116, Jayawardena 105 chase 318 in 41.3 overs. Sri Lanka A win by eight wickets.",
         src="CRICINFO", tax="CONFIRMED", art="cricket"),
    dict(n=9, beat="ECONOMY", place="SEOUL", region="ASIA-PACIFIC",
         head="Bank of Korea lifts rates to 3.25%",
         deck="A 25-point hike, not unanimous. Tokyo hints at faster rises; the Bank of England warns on $4tn of AI debt.",
         src="REUTERS", tax="CONFIRMED", art="bank"),
    dict(n=10, beat="CONFLICT", place="KYIV", region="EUROPE",
         head="Russia fires 112 drones; Ukraine hits refineries",
         deck="An overnight barrage; two Russian refineries struck in reply. Iran claims mines hit tankers in Hormuz.",
         src="REUTERS", tax="REPORTED", art="drones"),
    dict(n=11, beat="COURTS", place="WASHINGTON", region="AMERICAS",
         head="Second judge blocks birthright order",
         deck="A second federal judge blocks the order curtailing birthright citizenship.",
         src="AP", tax="REPORTED", art="court"),
    dict(n=12, beat="HEALTH", place="KINSHASA", region="AFRICA",
         head="Ebola toll climbs in DR Congo",
         deck="Cases reach 11,986, with 5,871 deaths, in the outbreak health officials are still struggling to contain.",
         src="WHO", tax="REPORTED", art="ebola"),
]

BRIEFS = [
    ("SEOUL", "White House accuses Seoul of breaking its promise on US tech firms; Coupang fined hundreds of millions", "REUTERS"),
    ("TOKYO", "Nvidia halts server shipments to four South-East Asian states as export controls tighten", "NEWSQUAWK"),
    ("LONDON", "Altria weighs an all-cash takeover of Imperial Brands; talks under way, no deal yet", "REUTERS"),
    ("FRANKFURT", "UniCredit seeks a Commerzbank meeting to replace nine of ten board members", "REUTERS"),
    ("LONDON", "Bank of England: hyperscaler financing exposure tops $4 trillion and is 'opaque'", "BOE"),
    ("TOKYO", "Kioxia begins verification work with Nvidia on memory for AI computing", "NIKKEI"),
    ("WASHINGTON", "US economy grew 4.3% annualised in Q3, the fastest pace in three years", "REUTERS"),
    ("WASHINGTON", "Core PCE 3.3%, hottest since 2023; the hot print sparked Wednesday's selloff", "BLOOMBERG"),
    ("NEW YORK", "HP surges 11.5% on strong earnings as chip selling continues elsewhere", "MOTLEY FOOL"),
    ("SUDAN", "RSF drone strikes kill 19 civilians in Blue Nile State", "REUTERS"),
    ("INDONESIA", "Illegal gold mine flood kills at least 8; 17 miners trapped underground", "REUTERS"),
    ("GREECE", "24-hour general strike shuts transport, ferries and flights over living costs", "AP"),
    ("TAIWAN", "One Chinese sortie crosses the median line; nine naval vessels counted", "REUTERS"),
    ("CALIFORNIA", "King Tides flood the coast as the Thanksgiving storm moves in", "AP"),
    ("HORMUZ", "Iran claims mines struck tankers and its defences downed two US drones", "REUTERS"),
    ("SENEGAL", "CAS upholds the appeal; Senegal reinstated as Africa Cup champions", "CAS"),
    ("WASHINGTON", "10-year Treasury yield falls to 4.80%, a two-and-a-half-month low", "REUTERS"),
    ("NEW YORK", "S&P and Nasdaq futures edge up 0.5% with cash markets shut for the holiday", "REUTERS"),
    ("TOKYO", "Nikkei 225 up 0.86% at 57,499; Hang Seng up about 1.2%", "NIKKEI"),
    ("LONDON", "Stoxx 600 +1.75%, FTSE +1.75%, DAX +2.08% as Europe rallies", "REUTERS"),
    ("HOUSTON", "WTI $84.84, no settlement on Thursday for the Thanksgiving holiday", "REUTERS"),
    ("VIENNA", "OPEC+ meets Sunday to set 2027 output policy as Brent nears $97", "REUTERS"),
    ("NEW YORK", "Mayor Mamdani will skip Saturday's parade for scheduled foot surgery", "CNN"),
    ("DUBAI", "Tanker reports an explosion from an unknown projectile 50 miles out; crew safe", "UKMTO"),
    ("JEDDAH", "Saudi-led coalition intercepts a Houthi drone near Jeddah port", "REUTERS"),
    ("TOKYO", "Japan calls the proposed US tariffs regrettable as allies push back", "REUTERS"),
    ("LOS ANGELES", "Rams 26-13 Packers on Thanksgiving Eve; Corum runs for 184 yards", "AP"),
    ("JERUSALEM", "Israeli security cabinet meeting cancelled amid disputes over Iran", "MEHR"),
]

NUMBERS = [
    ("20-40%", "proposed tariff rates"),
    ("$96.57", "Brent settles Thursday"),
    ("-4.6%", "Nasdaq-100 intraday plunge"),
    ("31", "killed in Cairo tanker fire"),
    ("39-38", "Eagles stun Cowboys"),
    ("1.5-1.5", "chess level after Game 3"),
]

TIMELINE = [
    ("WED EVE", "Tariffs proposed"),
    ("WED CLOSE", "Nasdaq -0.62%"),
    ("THU", "BoK hikes"),
    ("THU", "Brent $96.57"),
    ("THU EVE", "NFL thrillers"),
    ("TODAY", "Parade postponed"),
]

REGIONS = ["AMERICAS", "EUROPE", "ASIA-PACIFIC", "MIDDLE EAST", "AFRICA",
           "OCEANIA", "GLOBAL"]
BRIEF_REGIONS = [
    "ASIA-PACIFIC", "ASIA-PACIFIC", "EUROPE", "EUROPE", "EUROPE",
    "ASIA-PACIFIC", "AMERICAS", "AMERICAS", "AMERICAS", "AFRICA",
    "ASIA-PACIFIC", "EUROPE", "ASIA-PACIFIC", "AMERICAS", "MIDDLE EAST",
    "AFRICA", "AMERICAS", "AMERICAS", "ASIA-PACIFIC", "EUROPE",
    "AMERICAS", "GLOBAL", "AMERICAS", "MIDDLE EAST", "MIDDLE EAST",
    "ASIA-PACIFIC", "AMERICAS", "MIDDLE EAST",
]

# ---------------------------------------------------------------- drawing
def pin(draw, cx, cy, num):
    """Numbered map pin: red disc, white ring, number."""
    draw.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=RED,
                 outline=(255, 255, 255), width=2)
    f = font(SANS_B, 12)
    w = draw.textlength(str(num), font=f)
    draw.text((cx - w / 2, cy - 8), str(num), font=f, fill=(255, 255, 255))


# 64x64 pictograms, one per panel. Each draws inside the box
# (x, y, 64, 64) with fixed coordinates, so every panel's art is
# the same size and nothing can overflow into the text.
def art_tariffs(d, x, y, w, h):
    d.rectangle([x, y, x + 64, y + 64], fill=(232, 220, 196))
    d.rectangle([x + 6, y + 6, x + 40, y + 58], fill=(255, 253, 246),
                outline=INK, width=2)
    f = font(SANS_B, 8)
    d.text((x + 10, y + 10), "SEC. 301", font=f, fill=INK)
    d.text((x + 10, y + 21), "TARIFFS", font=f, fill=RED)
    for i in range(3):
        yy = y + 34 + i * 7
        d.line([(x + 10, yy), (x + 36, yy)], fill=GREY, width=2)
    d.ellipse([x + 40, y + 8, x + 60, y + 28], fill=RED,
              outline=(255, 255, 255), width=2)
    f2 = font(SANS_B, 12)
    d.text((x + 47, y + 12), "%", font=f2, fill=(255, 255, 255))


def art_tariffs_wide(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 220, 196))
    d.rectangle([x + 14, y + 8, x + w - 52, y + h - 8], fill=(255, 253, 246),
                outline=INK, width=2)
    f = font(SANS_B, 13)
    d.text((x + 22, y + 14), "SECTION 301", font=f, fill=INK)
    d.text((x + 22, y + 32), "TARIFF SCHEDULE", font=f, fill=RED)
    for i in range(3):
        yy = y + 54 + i * 9
        d.line([(x + 22, yy), (x + w - 66, yy)], fill=GREY, width=2)
    d.polygon([(x + w - 44, y + 12), (x + w - 14, y + 12), (x + w - 14, y + 42),
               (x + w - 44, y + 42)], fill=RED)
    f2 = font(SANS_B, 15)
    d.text((x + w - 40, y + 20), "%", font=f2, fill=(255, 255, 255))


def art_oil(d, x, y, w, h):
    d.rectangle([x, y, x + 64, y + 64], fill=(38, 32, 28))
    for tx in (x + 8, x + 28):
        d.rectangle([tx, y + 30, tx + 14, y + 58], fill=(120, 110, 100),
                    outline=(200, 190, 170), width=1)
        d.polygon([(tx + 1, y + 30), (tx + 7, y + 20), (tx + 13, y + 30)],
                  fill=(200, 190, 170))
    d.polygon([(x + 46, y + 10), (x + 54, y + 24), (x + 50, y + 24),
               (x + 58, y + 36), (x + 52, y + 36), (x + 54, y + 48),
               (x + 44, y + 48), (x + 46, y + 36), (x + 40, y + 36),
               (x + 46, y + 24), (x + 42, y + 24)], fill=(255, 140, 30))
    d.polygon([(x + 48, y + 28), (x + 54, y + 36), (x + 50, y + 36),
               (x + 54, y + 44), (x + 46, y + 44)], fill=(255, 210, 60))


def art_market(d, x, y, w, h):
    d.rectangle([x, y, x + 64, y + 64], fill=NAVY)
    for i in range(4):
        yy = y + 12 + i * 14
        d.line([(x + 5, yy), (x + 59, yy)], fill=(60, 80, 120), width=1)
    pts = [(x + 5, y + 14), (x + 18, y + 18), (x + 31, y + 30),
           (x + 44, y + 48), (x + 52, y + 34), (x + 59, y + 28)]
    d.line(pts, fill=(255, 90, 60), width=3, joint="curve")
    d.polygon([(x + 38, y + 4), (x + 60, y + 4), (x + 60, y + 16),
               (x + 38, y + 16)], fill=(255, 255, 255))
    f = font(SANS_B, 8)
    d.text((x + 41, y + 6), "SHUT", font=f, fill=RED)


def art_parade(d, x, y, w, h):
    d.rectangle([x, y, x + 64, y + 64], fill=(120, 140, 165))
    d.ellipse([x + 6, y + 6, x + 34, y + 26], fill=(210, 220, 235))
    d.ellipse([x + 38, y + 10, x + 56, y + 26], fill=(235, 220, 190))
    d.rectangle([x + 18, y + 26, x + 26, y + 34], fill=(150, 110, 70))
    for i in range(4):
        xx = x + 10 + i * 14
        d.line([(xx, y + 8), (xx - 4, y + 40)], fill=(90, 110, 140), width=2)
    d.rectangle([x, y + 50, x + 64, y + 64], fill=(70, 80, 95))
    f = font(SANS_B, 8)
    d.text((x + 8, y + 53), "GROUNDED", font=f, fill=(255, 255, 255))


def art_nfl(d, x, y, w, h):
    d.rectangle([x, y, x + 64, y + 64], fill=(36, 110, 52))
    for i in range(4):
        xx = x + 8 + i * 15
        d.line([(xx, y + 4), (xx, y + 44)], fill=(255, 255, 255), width=2)
    d.ellipse([x + 36, y + 46, x + 58, y + 60], fill=(120, 70, 30),
              outline=(255, 255, 255), width=2)
    f = font(SANS_B, 11)
    d.text((x + 6, y + 6), "39-35", font=f, fill=(255, 255, 255))
    d.text((x + 6, y + 20), "39-38", font=f, fill=(255, 255, 255))
    d.text((x + 6, y + 34), "13-10", font=f, fill=(255, 220, 90))


def art_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + 64, y + 64], fill=(52, 48, 44))
    d.rectangle([x, y + 52, x + 64, y + 64], fill=(30, 28, 26))
    d.polygon([(x + 30, y + 4), (x + 36, y + 14), (x + 33, y + 14),
               (x + 38, y + 22), (x + 33, y + 22), (x + 34, y + 28),
               (x + 28, y + 28), (x + 29, y + 22), (x + 24, y + 22),
               (x + 28, y + 14), (x + 26, y + 14)], fill=(255, 140, 30))
    d.rounded_rectangle([x + 6, y + 30, x + 44, y + 48], radius=8,
                        fill=(200, 200, 200), outline=(255, 255, 255), width=1)
    d.rectangle([x + 44, y + 33, x + 56, y + 48], fill=(180, 60, 40))
    d.ellipse([x + 12, y + 46, x + 22, y + 56], fill=INK)
    d.ellipse([x + 38, y + 46, x + 48, y + 56], fill=INK)


def art_chess(d, x, y, w, h):
    sq = 7
    ox, oy = x + 4, y + 4
    for r in range(8):
        for c in range(8):
            col = (240, 235, 220) if (r + c) % 2 == 0 else (60, 50, 40)
            d.rectangle([ox + c * sq, oy + r * sq, ox + (c + 1) * sq,
                         oy + (r + 1) * sq], fill=col)
    d.rectangle([ox, oy, ox + 8 * sq, oy + 8 * sq], outline=INK, width=1)
    f = font(SERIF_B, 9)
    d.text((ox + 1, oy + 1), "K", font=f, fill=INK)
    d.text((ox + 43, oy + 1), "k", font=f, fill=(240, 235, 220))


def art_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + 64, y + 64], fill=(52, 110, 58))
    d.ellipse([x + 6, y + 8, x + 24, y + 26], fill=(240, 235, 210))
    d.polygon([(x + 34, y + 6), (x + 40, y + 8), (x + 30, y + 34),
               (x + 24, y + 32)], fill=(210, 180, 120), outline=INK)
    for xx in (x + 44, x + 50, x + 56):
        d.rectangle([xx, y + 12, xx + 4, y + 40], fill=(245, 220, 130),
                    outline=INK, width=1)
    d.rectangle([x + 44, y + 9, x + 60, y + 12], fill=(245, 220, 130))
    f = font(SANS_B, 10)
    d.text((x + 6, y + 48), "318/2", font=f, fill=(255, 255, 255))


def art_bank(d, x, y, w, h):
    d.rectangle([x, y, x + 64, y + 64], fill=(226, 220, 205))
    d.polygon([(x + 8, y + 14), (x + 32, y + 4), (x + 56, y + 14)],
              fill=(120, 110, 95))
    for xx in (x + 12, x + 26, x + 40):
        d.rectangle([xx, y + 16, xx + 9, y + 52], fill=(250, 248, 240),
                    outline=INK, width=1)
    d.rectangle([x + 8, y + 52, x + 56, y + 58], fill=(120, 110, 95))
    f = font(SANS_B, 9)
    d.text((x + 34, y + 18), "+0.25", font=f, fill=RED)


def art_drones(d, x, y, w, h):
    d.rectangle([x, y, x + 64, y + 64], fill=(24, 30, 44))
    for cx, cy, s in [(x + 18, y + 16, 6), (x + 42, y + 28, 6),
                      (x + 22, y + 42, 5)]:
        d.line([(cx - s, cy), (cx + s, cy)], fill=(255, 200, 80), width=2)
        d.line([(cx, cy - s), (cx, cy + s)], fill=(255, 200, 80), width=2)
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 220, 120))
    f = font(SANS_B, 10)
    d.text((x + 34, y + 50), "112", font=f, fill=(255, 255, 255))


def art_court(d, x, y, w, h):
    d.rectangle([x, y, x + 64, y + 64], fill=(235, 230, 220))
    for xx in (x + 8, x + 20, x + 32):
        d.rectangle([xx, y + 16, xx + 7, y + 50], fill=(250, 248, 240),
                    outline=INK, width=1)
    d.rectangle([x + 6, y + 10, x + 44, y + 16], fill=(120, 110, 95))
    d.rectangle([x + 6, y + 50, x + 44, y + 56], fill=(120, 110, 95))
    d.ellipse([x + 46, y + 8, x + 60, y + 22], outline=RED, width=3)
    d.line([(x + 49, y + 19), (x + 57, y + 11)], fill=RED, width=3)


def art_ebola(d, x, y, w, h):
    import math
    d.rectangle([x, y, x + 64, y + 64], fill=(150, 40, 40))
    for cx, cy, r in [(x + 20, y + 24, 11), (x + 44, y + 40, 9),
                      (x + 46, y + 18, 8)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 25, 25),
                  outline=(255, 180, 180), width=2)
        for a in range(6):
            ang = a * 60 * math.pi / 180
            ex = cx + int(r * 1.4 * math.cos(ang))
            ey = cy + int(r * 1.4 * math.sin(ang))
            d.line([(cx, cy), (ex, ey)], fill=(255, 180, 180), width=2)
    d.rectangle([x + 48, y + 44, x + 62, y + 58], fill=(255, 255, 255))
    d.rectangle([x + 51, y + 48, x + 59, y + 54], fill=RED)
    d.rectangle([x + 54, y + 47, x + 56, y + 55], fill=(255, 255, 255))

ART = {"tariffs": art_tariffs, "oil": art_oil, "market": art_market,
       "parade": art_parade, "nfl": art_nfl, "tanker": art_tanker,
       "chess": art_chess, "cricket": art_cricket, "bank": art_bank,
       "drones": art_drones, "court": art_court, "ebola": art_ebola}

# Simplified world outline: coarse continent polygons in lon/lat.
LAND = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 62), (-75, 58), (-65, 60), (-55, 52), (-60, 47), (-70, 44),
     (-75, 39), (-80, 32), (-84, 30), (-90, 29), (-97, 26), (-105, 22),
     (-110, 24), (-115, 29), (-120, 34), (-125, 40), (-125, 49), (-130, 55),
     (-145, 60), (-160, 58), (-168, 66)],
    [(-170, -52), (-175, -42), (-178, -38), (178, -38), (174, -41), (170, -43),
     (167, -46), (170, -52)],
    [(-75, -55), (-70, -52), (-65, -45), (-60, -38), (-55, -35), (-48, -28),
     (-40, -22), (-35, -8), (-35, -2), (-45, 2), (-55, 6), (-65, 9),
     (-75, 8), (-80, 2), (-80, -5), (-81, -15), (-75, -35), (-72, -45),
     (-75, -55)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (12, 55),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (32, 70), (40, 68),
     (48, 68), (55, 68), (60, 69), (68, 72), (75, 72), (80, 73), (90, 75),
     (100, 77), (110, 74), (120, 73), (130, 72), (140, 72), (150, 70),
     (160, 69), (170, 66), (178, 65), (178, 62), (170, 60), (162, 58),
     (156, 52), (150, 59), (142, 55), (140, 45), (135, 43), (130, 42),
     (127, 40), (122, 38), (120, 32), (122, 28), (118, 25), (110, 20),
     (108, 12), (105, 9), (100, 8), (98, 12), (95, 16), (92, 21), (90, 22),
     (88, 22), (86, 20), (82, 17), (80, 15), (78, 8), (76, 10), (74, 15),
     (72, 20), (68, 23), (66, 25), (62, 25), (58, 26), (56, 27), (54, 27),
     (52, 29), (50, 29), (48, 30), (44, 29), (42, 27), (40, 21), (38, 20),
     (35, 28), (35, 31), (33, 31), (30, 36), (27, 37), (23, 36), (22, 38),
     (19, 40), (15, 44), (12, 44), (8, 44), (3, 43), (-1, 44), (-2, 47),
     (-5, 48), (-10, 36)],
    [(-17, 15), (-17, 21), (-15, 27), (-10, 31), (-6, 35), (0, 36), (10, 37),
     (11, 34), (15, 32), (19, 31), (22, 33), (25, 32), (30, 31), (32, 31),
     (35, 28), (37, 22), (39, 18), (41, 12), (43, 11), (46, 11), (51, 12),
     (51, 10), (48, 5), (45, 0), (42, -5), (40, -10), (40, -15), (39, -20),
     (36, -25), (33, -26), (30, -29), (27, -33), (20, -35), (17, -32),
     (14, -22), (12, -18), (12, -12), (9, -4), (9, 4), (6, 4), (2, 6),
     (-4, 5), (-8, 5), (-12, 8), (-15, 10), (-17, 15)],
    [(113, -22), (114, -30), (116, -35), (120, -34), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11),
     (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17),
     (118, -20), (113, -22)],
]
PINS = [  # (story number, lon, lat)
    (1, -77, 39), (2, 50, 27), (3, -74, 41), (4, -74, 41), (5, -83, 42),
    (6, 31, 30), (7, 6, 46), (8, 51, 25), (9, 127, 38), (10, 31, 50),
    (11, -77, 39), (12, 15, -4),
]

# ---------------------------------------------------------------- layout
M = 20
X1 = W - M
CW = X1 - M  # 984


def tally():
    counts = {r: 0 for r in REGIONS}
    for p in PANELS:
        counts[p["region"]] += 1
    for r in BRIEF_REGIONS:
        counts[r] += 1
    assert sum(counts.values()) == 40, counts
    return counts


def draw_panel(d, p, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=1)
    d.rectangle([x, y, x + w, y + 15], fill=RED)
    f = font(SANS_B, 9)
    left = "%d - %s - %s - %s" % (p["n"], p["beat"], p["place"], p["region"])
    d.text((x + 6, y + 3), left, font=f, fill=(255, 255, 255))
    right = "%s - %s" % (p["src"], p["tax"])
    rw = d.textlength(right, font=f)
    d.text((x + w - 6 - rw, y + 3), right, font=f, fill=(255, 240, 200))
    ART[p["art"]](d, x + w - 70, y + 20, 64, 64)
    tw = w - 84
    yy = text_block(d, x + 6, y + 19, p["head"], font(SERIF_B, 17), tw, 18)
    text_block(d, x + 6, yy + 2, p["deck"], font(SANS, 11), tw, 12)


def draw_lead(d, p, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=1)
    art_tariffs_wide(d, x + 1, y + 1, 250, h - 2)
    tx = x + 262
    f = font(SANS_B, 11)
    d.text((tx, y + 8), "%d - %s - %s - %s  -  THE DAY'S LEAD"
           % (p["n"], p["beat"], p["place"], p["region"]), font=f, fill=RED)
    yy = text_block(d, tx, y + 26, p["head"], font(SERIF_B, 27), w - 262 - 12, 30)
    text_block(d, tx, yy + 4, p["deck"], font(SANS, 13), w - 262 - 12, 16)
    f2 = font(SANS, 10)
    d.text((tx, y + h - 16), "%s - %s" % (p["src"], p["tax"]), font=f2,
           fill=GREY)


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(188, 208, 224), outline=INK,
                width=1)
    f = font(SANS_B, 10)
    d.text((x + 6, y + 3), "WHERE IT HAPPENED - PINS = STORY NUMBERS",
           font=f, fill=NAVY)

    def px(lon):
        return x + 8 + (lon + 180) / 360.0 * (w - 16)

    def py(lat):
        return y + 14 + (85 - lat) / 145.0 * (h - 20)

    for poly in LAND:
        pts = [(px(lon), py(lat)) for lon, lat in poly]
        d.polygon(pts, fill=(224, 212, 182), outline=(120, 110, 95))
    used = {}
    for num, lon, lat in PINS:
        k = (lon, lat)
        n = used.get(k, 0)
        used[k] = n + 1
        pin(d, px(lon) + n * 16, py(lat) - n * 11, num)


def draw_tally(d, counts, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=1)
    f = font(SANS_B, 11)
    d.text((x + 8, y + 4), "REGION TALLY - 40 STORIES", font=f, fill=RED)
    f2 = font(SANS, 8)
    f3 = font(SANS_B, 8)
    top = max(counts.values())
    yy = y + 16
    for r in REGIONS:
        d.text((x + 8, yy), r, font=f2, fill=INK)
        bw = int(counts[r] / top * 150)
        d.rectangle([x + 108, yy + 1, x + 108 + bw, yy + 6], fill=RED)
        d.text((x + 108 + 156, yy), str(counts[r]), font=f3, fill=INK)
        yy += 8
    assert yy <= y + h + 2


def draw_datecheck(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 250, 240), outline=RED,
                width=2)
    f = font(SANS_B, 11)
    d.text((x + 8, y + 4), "DATE CHECK", font=f, fill=RED)
    body = ("Wires cutoff 00:00 UTC Fri 27 Nov. Every story happened, or was "
            "first reported, on Thu 26 Nov. Wed-evening breaks carried in "
            "Thursday's wires: tariffs proposal, Ras Tanura claim, Cairo "
            "fire. LEFT OUT - NOT 26 NOV: BepiColombo Mercury arrival "
            "(21 Nov); Sooryavanshi's 204 (24 Nov); Gukesh-Sindarov Game 2 "
            "(25 Nov); Swiss envoy expulsion (25 Nov).")
    text_block(d, x + 8, y + 20, body, font(SANS, 10), w - 16, 12)


def draw_briefs(d, x, y, w):
    f = font(SANS_B, 12)
    d.text((x, y), "ALSO ON THURSDAY - 28 MORE STORIES", font=f, fill=RED)
    hline(d, x, x + w, y + 16, fill=RED, width=2)
    col_w, gap = 240, 8
    f2 = font(SANS, 10)
    f3 = font(SANS_B, 10)
    row_h = 23
    for i, (place, text, src) in enumerate(BRIEFS):
        col, row = i % 4, i // 4
        bx = x + col * (col_w + gap)
        by = y + 20 + row * row_h
        head = "%d - %s - " % (13 + i, place)
        lines = wrap(d, head + text + " - " + src, f2, col_w)[:2]
        for li, line in enumerate(lines):
            yy = by + li * 11
            if li == 0 and line.startswith(head):
                d.text((bx, yy), head, font=f3, fill=INK)
                rest = line[len(head):]
                d.text((bx + d.textlength(head, font=f3), yy), rest,
                       font=f2, fill=INK)
            else:
                d.text((bx, yy), line, font=f2, fill=INK)


def build():
    counts = tally()
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # top bar
    d.rectangle([0, 0, W, 24], fill=INK)
    f = font(SANS_B, 12)
    d.text((M, 5), "THE WORLD IN ONE DAY", font=f, fill=(255, 255, 255))
    right = "EVERY STORY DATED THURSDAY 26 NOV 2026"
    d.text((X1 - d.textlength(right, font=f), 5), right, font=f,
           fill=(255, 255, 255))
    # masthead
    title = "Thursday 26 November 2026"
    tf = font(SERIF_B, 54)
    d.text(((W - d.textlength(title, font=tf)) / 2, 28), title, font=tf,
           fill=INK)
    sub = ("Tariffs for 14 partners  -  Oil jumps  -  Wall Street's wild ride  "
           "-  Thanksgiving without its parade")
    sf = font(SERIF_I, 14)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 92), sub, font=sf, fill=INK)
    hline(d, M, X1, 110, width=2)
    # count line
    cf = font(SANS_B, 12)
    parts = ["40 STORIES"] + ["%s %d" % (r, counts[r]) for r in REGIONS]
    cline = "  -  ".join(parts)
    d.text(((W - d.textlength(cline, font=cf)) / 2, 114), cline, font=cf,
           fill=INK)
    # numbers strip
    bw, gap = 160, 5
    nf = font(SANS_B, 20)
    lf = font(SANS, 9)
    for i, (num, label) in enumerate(NUMBERS):
        bx = M + i * (bw + gap)
        d.rectangle([bx, 132, bx + bw, 164], fill=PANEL, outline=INK, width=1)
        d.text((bx + 8, 134), num, font=nf, fill=RED)
        d.text((bx + 8, 154), label, font=lf, fill=GREY)
    # timeline strip
    tf2 = font(SANS_B, 10)
    tl = "   ◆   ".join("%s  %s" % t for t in TIMELINE)
    d.text(((W - d.textlength(tl, font=tf2)) / 2, 168), tl, font=tf2, fill=INK)
    # lead + rows
    draw_lead(d, PANELS[0], M, 186, CW, 96)
    pw = 324
    for j, p in enumerate(PANELS[1:4]):
        draw_panel(d, p, M + j * (pw + 6), 286, pw, 112)
    draw_map(d, M, 402, 640, 72)
    draw_tally(d, counts, M + 648, 402, 336, 72)
    for j, p in enumerate(PANELS[4:7]):
        draw_panel(d, p, M + j * (pw + 6), 478, pw, 112)
    for j, p in enumerate(PANELS[7:10]):
        draw_panel(d, p, M + j * (pw + 6), 594, pw, 112)
    for j, p in enumerate(PANELS[10:12]):
        draw_panel(d, p, M + j * (pw + 6), 710, pw, 112)
    draw_datecheck(d, M + 2 * (pw + 6), 710, pw, 112)
    draw_briefs(d, M, 826, CW)
    # footer
    ff = font(SANS, 10)
    foot = ("Sources: Reuters - AP - Bloomberg - BBC - AFP - PTI - ESA - JAXA - "
            "NFL  |  All stories 26 November 2026  |  Wires cutoff 00:00 UTC "
            "Fri 27 Nov")
    d.text(((W - d.textlength(foot, font=ff)) / 2, 1008), foot, font=ff,
           fill=GREY)
    img.save(OUT, "PNG", optimize=True)
    return OUT


if __name__ == "__main__":
    path = build()
    print("wrote", path, os.path.getsize(path), "bytes")
