#!/usr/bin/env python3
"""The World Today - Sunday 22 November 2026.

Draws a 1024x1024 newspaper front page summing up the day's world
news and writes it as a PNG to $MAKEFUN_OUTPUT_DIR/entry.png
(or /output/entry.png). Python 3.13, standard library only, no
network. Deterministic: two runs write identical bytes.

Everything is drawn from scratch in this file: a hand-authored 5x7
bitmap typeface, geometric icons, a wire-frame globe, and a
hand-encoded PNG (zlib + struct, CRC per chunk).
"""

import hashlib
import os
import struct
import sys
import zlib
from pathlib import Path

W, H = 1024, 1024

PAPER = (246, 241, 229)
INK = (17, 17, 17)
RED = (176, 32, 32)
BLUE = (31, 78, 121)
GREY = (102, 102, 102)
LIGHT_GREY = (200, 192, 175)
STEEL = (90, 120, 150)

# ---------------------------------------------------------------- font
# 5x7 bitmap glyphs, '#' = pixel on. 7 rows of 5 characters each.
FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "...#.", "..#..", "..#..", "..#.."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    "'": ("..#..", "..#..", "..#..", ".....", ".....", ".....", "....."),
    "-": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    "(": ("...##", "..#..", ".#...", ".#...", ".#...", "..#..", "...##"),
    ")": ("##...", "..#..", "...#.", "...#.", "...#.", "..#..", "##..."),
    "/": ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
    "&": (".###.", "#...#", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"),
    "%": ("##..#", "##.#.", "...#.", "..#..", ".#...", "#.##.", "#..##"),
    "+": (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    "=": (".....", ".....", "#####", ".....", "#####", ".....", "....."),
    '"': (".#.#.", ".#.#.", ".#.#.", ".....", ".....", ".....", "....."),
}

for _ch, _g in FONT.items():
    assert len(_g) == 7 and all(len(_r) == 5 for _r in _g), _ch


def text_width(text, scale):
    """Pixel width of text at the given scale (no trailing space)."""
    if not text:
        return 0
    return len(text) * 6 * scale - scale


def wrap_text(text, scale, max_w):
    """Greedy word wrap; returns a list of lines fitting max_w."""
    lines = []
    for para in text.split("\n"):
        cur = ""
        for word in para.split(" "):
            trial = word if not cur else cur + " " + word
            if text_width(trial, scale) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, color)

    def hline(self, x, y, w, color, t=1):
        self.rect(x, y, w, t, color)

    def vline(self, x, y, h, color, t=1):
        self.rect(x, y, t, h, color)

    def line(self, x0, y0, x1, y1, color, t=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            self.rect(x - t // 2, y - t // 2, t, t, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def circle(self, cx, cy, r, color, t=1):
        import math
        steps = max(24, int(2 * math.pi * r))
        for i in range(steps):
            a = 2 * math.pi * i / steps
            x = int(round(cx + r * math.cos(a)))
            y = int(round(cy + r * math.sin(a)))
            self.rect(x - t // 2, y - t // 2, t, t, color)

    def filled_circle(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, color)

    def ellipse(self, cx, cy, rx, ry, color, t=1):
        import math
        steps = max(24, int(2 * math.pi * max(rx, ry)))
        for i in range(steps):
            a = 2 * math.pi * i / steps
            x = int(round(cx + rx * math.cos(a)))
            y = int(round(cy + ry * math.sin(a)))
            self.rect(x - t // 2, y - t // 2, t, t, color)

    def text(self, x, y, s, scale, color):
        s = s.upper()  # the typeface is caps-only; fold case here
        cx = x
        for ch in s:
            glyph = FONT.get(ch)
            if glyph is None:
                raise ValueError("no glyph for %r" % ch)
            for row, bits in enumerate(glyph):
                for col, bit in enumerate(bits):
                    if bit == "#":
                        self.rect(cx + col * scale, y + row * scale,
                                  scale, scale, color)
            cx += 6 * scale

    def text_center(self, cx, y, s, scale, color):
        self.text(cx - text_width(s, scale) // 2, y, s, scale, color)

    def paragraph(self, x, y, s, scale, color, max_w, leading=None):
        if leading is None:
            leading = 7 * scale + 3
        yy = y
        for line in wrap_text(s, scale, max_w):
            self.text(x, yy, line, scale, color)
            yy += leading
        return yy


# ---------------------------------------------------------------- icons
def icon_tanker(cv, x, y, s):
    # sea
    cv.rect(x, y + s - 22, s, 22, (214, 231, 240))
    for k in range(4):
        cv.hline(x + 6 + k * 24, y + s - 16 + (k % 2) * 5, 16, BLUE, 3)
    # hull
    cv.rect(x + 8, y + s - 46, s - 24, 24, INK)
    cv.line(x + s - 16, y + s - 46, x + s - 4, y + s - 34, INK, 3)
    # containers
    cv.rect(x + 14, y + s - 66, 22, 20, RED)
    cv.rect(x + 38, y + s - 66, 22, 20, BLUE)
    cv.rect(x + 62, y + s - 66, 22, 20, (120, 120, 120))
    # bridge tower
    cv.rect(x + s - 26, y + s - 72, 14, 26, (240, 240, 240))
    cv.rect(x + s - 26, y + s - 72, 14, 4, RED)
    # smoke
    cv.filled_circle(x + 30, y + 14, 5, GREY)
    cv.filled_circle(x + 44, y + 8, 7, GREY)
    cv.filled_circle(x + 58, y + 15, 5, GREY)


def icon_building(cv, x, y, s):
    # standing half
    cv.rect(x + 10, y + 26, 34, s - 26, (150, 150, 150))
    for r in range(4):
        for c in range(2):
            cv.rect(x + 16 + c * 15, y + 34 + r * 16, 8, 9, (250, 240, 200))
    # collapsed half: jagged rubble
    cv.line(x + 44, y + 26, x + 58, y + 44, INK, 3)
    cv.line(x + 58, y + 44, x + 52, y + 60, INK, 3)
    cv.line(x + 52, y + 60, x + 68, y + 74, INK, 3)
    cv.rect(x + 48, y + s - 30, s - 56, 30, (120, 120, 120))
    cv.rect(x + 56, y + s - 42, 12, 12, (90, 90, 90))
    cv.rect(x + 76, y + s - 36, 10, 6, (90, 90, 90))
    # smoke
    cv.filled_circle(x + 62, y + 16, 6, GREY)
    cv.filled_circle(x + 76, y + 9, 8, GREY)
    cv.filled_circle(x + 90, y + 18, 5, GREY)
    # drone overhead
    cx, cy = x + s - 18, y + 12
    cv.rect(cx - 12, cy - 1, 24, 2, INK)
    cv.rect(cx - 1, cy - 12, 2, 24, INK)
    cv.filled_circle(cx, cy, 3, RED)


def icon_robot(cv, x, y, s):
    # antenna
    cv.vline(x + s // 2, y + 8, 16, INK, 3)
    cv.filled_circle(x + s // 2, y + 6, 4, RED)
    # head
    cv.rect(x + 22, y + 24, s - 44, 52, INK)
    cv.rect(x + 25, y + 27, s - 50, 46, (200, 205, 210))
    # eyes
    cv.rect(x + 34, y + 38, 12, 10, RED)
    cv.rect(x + s - 46, y + 38, 12, 10, RED)
    # mouth grille
    for k in range(4):
        cv.vline(x + 38 + k * 10, y + 58, 10, INK, 2)
    # ears
    cv.rect(x + 14, y + 40, 8, 16, INK)
    cv.rect(x + s - 22, y + 40, 8, 16, INK)
    # shoulders
    cv.rect(x + 14, y + 84, s - 28, 14, BLUE)
    cv.rect(x + 14, y + 84, s - 28, 3, INK)


def icon_exam(cv, x, y, s):
    # sheet
    cv.rect(x + 22, y + 8, s - 44, s - 16, (255, 255, 255))
    cv.rect(x + 22, y + 8, s - 44, 2, INK)
    cv.rect(x + 22, y + s - 10, s - 44, 2, INK)
    cv.rect(x + 22, y + 8, 2, s - 16, INK)
    cv.rect(x + s - 24, y + 8, 2, s - 16, INK)
    # ruled lines
    for r in range(3):
        cv.hline(x + 30, y + 26 + r * 12, s - 60, LIGHT_GREY, 2)
    # AI crossed out
    cv.text(x + 34, y + 62, "AI", 4, INK)
    cv.line(x + 30, y + 60, x + 82, y + 92, RED, 4)
    cv.line(x + 82, y + 60, x + 30, y + 92, RED, 4)
    # pencil
    cv.line(x + s - 30, y + 16, x + s - 14, y + 40, (240, 180, 40), 5)


def icon_scales(cv, x, y, s):
    cx = x + s // 2
    # base and post
    cv.rect(x + 18, y + s - 14, s - 36, 8, INK)
    cv.vline(cx, y + 18, s - 32, INK, 4)
    # beam
    cv.hline(x + 14, y + 20, s - 28, INK, 4)
    cv.filled_circle(cx, y + 20, 4, RED)
    # left pan
    cv.line(x + 18, y + 22, cx - 26, y + 58, INK, 2)
    cv.line(x + 18, y + 22, cx - 40, y + 58, INK, 2)
    cv.line(cx - 40, y + 58, cx - 26, y + 58, INK, 2)
    cv.line(cx - 40, y + 58, cx - 33, y + 70, INK, 2)
    cv.line(cx - 26, y + 58, cx - 33, y + 70, INK, 2)
    # right pan
    cv.line(x + s - 18, y + 22, cx + 26, y + 58, INK, 2)
    cv.line(x + s - 18, y + 22, cx + 40, y + 58, INK, 2)
    cv.line(cx + 26, y + 58, cx + 40, y + 58, INK, 2)
    cv.line(cx + 26, y + 58, cx + 33, y + 70, INK, 2)
    cv.line(cx + 40, y + 58, cx + 33, y + 70, INK, 2)
    # pan bowls
    cv.filled_circle(cx - 33, y + 70, 7, BLUE)
    cv.filled_circle(cx + 33, y + 70, 7, BLUE)


def icon_racecar(cv, x, y, s):
    # checkered flag
    cv.vline(x + s - 30, y + 10, 44, INK, 3)
    for r in range(2):
        for c in range(4):
            if (r + c) % 2 == 0:
                cv.rect(x + s - 30 + c * 7, y + 10 + r * 7, 7, 7, INK)
    # body
    cv.rect(x + 8, y + 62, s - 24, 18, RED)
    cv.line(x + 8, y + 62, x + 22, y + 50, RED, 4)
    cv.rect(x + 26, y + 48, 34, 16, RED)
    cv.rect(x + 30, y + 50, 26, 12, (200, 225, 240))
    cv.rect(x + s - 30, y + 66, 18, 8, INK)
    # wheels
    cv.filled_circle(x + 26, y + 84, 11, INK)
    cv.filled_circle(x + 26, y + 84, 5, (220, 220, 220))
    cv.filled_circle(x + s - 28, y + 84, 11, INK)
    cv.filled_circle(x + s - 28, y + 84, 5, (220, 220, 220))
    # speed lines
    for k in range(3):
        cv.hline(x + 6, y + 30 + k * 8, 22 - k * 4, GREY, 2)


# ---------------------------------------------------------------- lead art
def lead_art(cv, x, y, w, h):
    cx, cy = x + w // 2, y + h // 2 - 14
    r = 96
    # globe
    cv.circle(cx, cy, r, INK, 3)
    cv.ellipse(cx, cy, 38, r, INK, 2)
    cv.ellipse(cx, cy, 74, r, INK, 2)
    cv.hline(cx - r, cy, 2 * r, INK, 2)
    cv.hline(cx - 82, cy - 52, 164, INK, 2)
    cv.hline(cx - 82, cy + 52, 164, INK, 2)
    # continents (blobs)
    cv.filled_circle(cx - 42, cy - 28, 16, STEEL)
    cv.filled_circle(cx - 26, cy - 14, 12, STEEL)
    cv.filled_circle(cx + 44, cy + 30, 14, STEEL)
    cv.filled_circle(cx + 30, cy + 44, 10, STEEL)
    cv.filled_circle(cx + 52, cy - 34, 9, STEEL)
    # red crack across the globe
    cv.line(cx - 88, cy - 78, cx - 40, cy - 30, RED, 4)
    cv.line(cx - 40, cy - 30, cx - 66, cy + 6, RED, 4)
    cv.line(cx - 66, cy + 6, cx - 18, cy + 52, RED, 4)
    cv.line(cx - 18, cy + 52, cx + 30, cy + 88, RED, 4)
    # NO DEAL stamp band
    cv.rect(cx - r - 2, cy - 18, 2 * r + 4, 36, RED)
    cv.text_center(cx, cy - 11, "NO DEAL", 3, (255, 255, 255))
    cv.text_center(cx, y + h - 26, "COP31 - ANTALYA", 2, GREY)


# ---------------------------------------------------------------- page
STORIES = [
    ("HORMUZ", icon_tanker,
     "BAHRAIN BLAMES IRAN AS TANKERS HIT IN HORMUZ",
     "Manama says Tehran hit a plant; two tankers struck in the strait, UKMTO says."),
    ("KYIV", icon_building,
     "RUSSIAN DRONE FLATTENS FLATS NEAR KYIV",
     "Five killed in Dymer as a block collapses; rescuers hunt for the missing."),
    ("GENEVA", icon_robot,
     "STATES OPEN PATH TO 'KILLER ROBOT' PACT",
     "128 countries agree to draft rules on autonomous weapons over the next two years."),
    ("SEOUL", icon_exam,
     "MINISTER QUITS OVER AI EXAM-CHEATING CHAOS",
     "Seoul's education chief resigns after last-minute rule changes for the college exam."),
    ("ROHINGYA", icon_scales,
     "ROHINGYA HAIL GENOCIDE VERDICT ON MYANMAR",
     "Refugees welcome the UN court's ruling; the UN vows they 'will not be alone'."),
    ("LAS VEGAS", icon_racecar,
     "VERSTAPPEN WINS WILD LAS VEGAS GP",
     "35 lead changes in 50 laps as the Red Bull star beats Norris by 0.639 seconds."),
]


def build():
    cv = Canvas(W, H, PAPER)
    m = 30
    cw = W - 2 * m

    # masthead
    cv.text_center(W // 2, 26, "THE WORLD TODAY", 7, INK)
    cv.hline(m, 92, cw, INK, 3)
    cv.hline(m, 98, cw, INK, 1)

    # red date band
    cv.rect(m, 106, cw, 44, RED)
    cv.text_center(W // 2, 118, "SUNDAY 22 NOVEMBER 2026", 2, (255, 255, 255))

    # lead story
    ly = 164
    cv.text(m, ly, "CLIMATE - ANTALYA", 2, RED)
    hy = ly + 22
    yy = cv.paragraph(m, hy, "COP31 COLLAPSES AS EU REJECTS FOSSIL-FREE DEAL",
                      3, INK, 610, leading=24)
    yy = cv.paragraph(m, yy + 10,
                      "Two days of overtime end in failure: the final text "
                      "named no fossil fuels, and the EU said no. The "
                      "longest climate summit ever closes with no deal.",
                      2, INK, 610, leading=17)
    yy = cv.paragraph(m, yy + 12,
                      "GUTERRES: 'DEEPLY DISAPPOINTED'",
                      2, RED, 610, leading=17)
    lead_art(cv, 668, ly - 8, 326, 300)
    cv.hline(m, 466, cw, INK, 3)

    # story grid: 2 columns x 3 rows
    gx, gy = m, 484
    col_w = (cw - 16) // 2
    row_h = 158
    for i, (kicker, icon, headline, deck) in enumerate(STORIES):
        cx = gx + (i % 2) * (col_w + 16)
        cy = gy + (i // 2) * row_h
        # icon box
        cv.rect(cx, cy, 120, 120, (255, 255, 255))
        cv.rect(cx, cy, 120, 2, INK)
        cv.rect(cx, cy + 118, 120, 2, INK)
        cv.rect(cx, cy, 2, 120, INK)
        cv.rect(cx + 118, cy, 2, 120, INK)
        icon(cv, cx, cy, 120)
        tx = cx + 134
        tw = col_w - 134
        cv.text(tx, cy + 2, kicker, 2, RED)
        yy = cv.paragraph(tx, cy + 24, headline, 2, INK, tw, leading=17)
        cv.paragraph(tx, yy + 4, deck, 2, GREY, tw, leading=17)

    # footer
    cv.hline(m, 962, cw, INK, 2)
    cv.text_center(W // 2, 976,
                   "SOURCES: AFP / AP / REUTERS / YONHAP / AL JAZEERA",
                   2, GREY)
    return cv


# ---------------------------------------------------------------- png
def png_bytes(cv):
    raw = bytearray()
    for y in range(cv.h):
        raw.append(0)
        raw += cv.px[y * cv.w * 3:(y + 1) * cv.w * 3]
    comp = zlib.compress(bytes(raw), 9)

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", comp) + chunk(b"IEND", b""))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out = Path(out_dir) / "entry.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    data = png_bytes(build())
    out.write_bytes(data)
    print("wrote %s (%d bytes)" % (out, len(data)))
    print("sha256 %s" % hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    sys.exit(main())
