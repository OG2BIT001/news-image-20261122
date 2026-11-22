"""THE WORLD TODAY - one image summing up the world news of Sunday
22 November 2026, drawn as a newspaper front page.

Standard library only, no network, fully deterministic: the program
draws the page pixel by pixel with its own bitmap typeface and writes
it as a PNG to /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png
outside the grader's container, following the kit starter's pattern).
Run it twice and the bytes are identical.
"""

import os
import struct
import zlib
from pathlib import Path

W = 1024
H = 1024

PAPER = (247, 242, 231)
PANEL = (238, 229, 205)
INK = (18, 20, 26)
GREY = (92, 96, 106)
FAINT = (196, 188, 168)
RED = (178, 30, 42)
BLUE = (24, 62, 110)
SKY = (126, 178, 219)
LAND = (240, 234, 214)
SUN = (232, 148, 44)

# ---------------------------------------------------------------- font
# A 5x7 bitmap typeface, drawn by hand for this program. Each glyph is
# seven rows of five pixels, '#' for ink. Lowercase letters render as
# small caps (the cap glyph), which suits a poster-style front page.

FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": (".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "J": ("..###", "....#", "....#", "....#", "....#", "#...#", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."),
    "X": ("#...#", ".#.#.", "..#..", "..#..", "..#..", ".#.#.", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    "3": ("#####", "...#.", "..#..", "...#.", "....#", "#...#", ".###."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    ";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    "'": (".##..", ".##..", ".#...", ".....", ".....", ".....", "....."),
    "-": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    "(": ("...##", "..#..", ".#...", ".#...", ".#...", "..#..", "...##"),
    ")": (".##..", "..#..", "...#.", "...#.", "...#.", "..#..", ".##.."),
    "/": ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
    "\u00b7": (".....", ".....", ".....", ".###.", ".###.", ".....", "....."),
    "%": ("##..#", "##.#.", "....#", "...#.", "..#..", ".#...", "#.##."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    "&": (".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"),
    "+": (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    "\u00dc": (".#.#.", ".....", "#...#", "#...#", "#...#", "#...#", ".###."),
}


def glyph(ch):
    if "a" <= ch <= "z":
        ch = ch.upper()
    return FONT.get(ch, FONT[" "])


def text_width(s, scale):
    if not s:
        return 0
    return len(s) * 6 * scale - scale


# ------------------------------------------------------------- canvas

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
            if 0 <= yy < self.h:
                base = (yy * self.w) * 3
                for xx in range(x, x + w):
                    if 0 <= xx < self.w:
                        i = base + xx * 3
                        self.px[i:i + 3] = bytes(color)

    def hline(self, x, y, w, color, thick=1):
        self.rect(x, y, w, thick, color)

    def vline(self, x, y, h, color, thick=1):
        self.rect(x, y, thick, h, color)

    def line(self, x0, y0, x1, y1, color, thick=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            for ox in range(thick):
                for oy in range(thick):
                    self.set(x0 + ox, y0 + oy, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, color, thick=1):
        x, y, err = r, 0, 0
        while x >= y:
            for dx, dy in ((x, y), (y, x), (-y, x), (-x, y),
                           (-x, -y), (-y, -x), (y, -x), (x, -y)):
                for t in range(thick):
                    self.set(cx + dx, cy + dy, color)
                    if dx:
                        self.set(cx + dx - (t + 1) * (1 if dx > 0 else -1),
                                 cy + dy, color)
            y += 1
            if err <= 0:
                err += 2 * y + 1
            if err > 0:
                x -= 1
                err -= 2 * x + 1

    def disc(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            span = int((r * r - (yy - cy) ** 2) ** 0.5)
            self.hline(cx - span, yy, 2 * span + 1, color)

    def ellipse(self, cx, cy, rx, ry, color, thick=1):
        import math
        steps = max(rx, ry) * 4
        for i in range(steps + 1):
            t = 2 * math.pi * i / steps
            x = int(round(cx + rx * math.cos(t)))
            y = int(round(cy + ry * math.sin(t)))
            for ox in range(thick):
                for oy in range(thick):
                    self.set(x + ox, y + oy, color)

    def text(self, x, y, s, scale, color, bold=False):
        cx = x
        for ch in s:
            g = glyph(ch)
            for row in range(7):
                for col in range(5):
                    if g[row][col] == "#":
                        bx = cx + col * scale
                        by = y + row * scale
                        self.rect(bx, by, scale, scale, color)
                        if bold:
                            self.rect(bx + max(1, scale // 2), by,
                                      scale, scale, color)
            cx += 6 * scale
        return cx - scale - x if s else 0

    def text_centered(self, cx, y, s, scale, color, bold=False):
        w = text_width(s, scale)
        if bold:
            w += max(1, scale // 2)
        self.text(cx - w // 2, y, s, scale, color, bold)
        return w


def wrap(s, scale, max_w):
    words = s.split()
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- art

def draw_globe(cv, x, y, w, h):
    """A simple wire-frame style globe under a rising sun, for the
    climate lead story's art panel."""
    cv.rect(x, y, w, h, BLUE)
    cx, cy, r = x + w // 2, y + h // 2 - 6, 104
    # sun and rays, top right
    sx, sy = x + w - 52, y + 44
    cv.disc(sx, sy, 17, SUN)
    for dx, dy in ((0, -30), (0, 30), (-30, 0), (30, 0),
                   (-21, -21), (21, -21), (-21, 21), (21, 21)):
        cv.line(sx + dx * 2 // 3, sy + dy * 2 // 3,
                sx + dx, sy + dy, SUN, 3)
    # globe
    cv.disc(cx, cy, r, SKY)
    cv.circle(cx, cy, r, LAND, 3)
    for frac in (0.38, 0.72):
        cv.ellipse(cx, cy, int(r * frac), r, LAND, 2)
    cv.ellipse(cx, cy, r, int(r * 0.42), LAND, 2)
    cv.ellipse(cx, cy, r, int(r * 0.78), LAND, 2)
    # a few stars in the night-blue field
    for px, py in ((x + 26, y + 30), (x + 58, y + 74), (x + 30, y + 150),
                   (x + 66, y + 208), (x + w - 30, y + 120),
                   (x + w - 66, y + 216), (x + w - 24, y + 178)):
        cv.rect(px, py, 4, 4, LAND)


# -------------------------------------------------------------- page

def story(cv, x, y, w, kicker, head_lines, deck):
    cv.text(x, y, kicker, 2, RED, bold=True)
    hy = y + 20
    for ln in head_lines:
        cv.text(x, hy, ln, 3, INK, bold=True)
        hy += 26
    dy = hy + 4
    for ln in wrap(deck, 2, w):
        cv.text(x, dy, ln, 2, INK)
        dy += 18
    return dy


def compose():
    cv = Canvas(W, H, PAPER)
    # page frame
    cv.rect(16, 16, W - 32, 3, INK)
    cv.rect(16, H - 19, W - 32, 3, INK)
    cv.rect(16, 16, 3, H - 32, INK)
    cv.rect(W - 19, 16, 3, H - 32, INK)

    # masthead
    cv.text_centered(W // 2, 44, "THE WORLD TODAY", 8, INK, bold=True)
    cv.hline(44, 122, W - 88, INK, 6)
    # date bar
    cv.rect(44, 138, W - 88, 46, RED)
    cv.text(60, 151, "VOL. I - NO. 22", 2, PAPER)
    cv.text_centered(W // 2, 148, "SUNDAY 22 NOVEMBER 2026", 3, PAPER,
                     bold=True)
    right = "WIRE EDITION"
    cv.text(W - 60 - text_width(right, 2), 151, right, 2, PAPER)

    # ---- lead story: COP31
    lx, lw = 44, 596
    cv.text(lx, 206, "CLIMATE SUMMIT \u00b7 ANTALYA, T\u00dcRKIYE", 2, RED,
            bold=True)
    hy = 236
    for ln in ("COP31 GOES TO", "THE WIRE AS", "FINAL TEXT LANDS"):
        cv.text(lx, hy, ln, 6, INK, bold=True)
        hy += 54
    deck = ("SUMMIT PRESIDENT MURAT KURUM TABLES A FINAL TEXT AND URGES "
            "DELEGATES TO SETTLE IT BY 6AM. THE LAST FIGHT: WHETHER THE "
            "PACT NAMES FOSSIL FUELS AT ALL.")
    dy = hy + 10
    for ln in wrap(deck, 2, lw):
        cv.text(lx, dy, ln, 2, INK)
        dy += 21
    cv.text(lx, dy + 8, "TALKS RAN PAST FRIDAY'S DEADLINE IN OVERTIME.",
            2, GREY)

    # lead art panel
    draw_globe(cv, 664, 206, 316, 268)
    cv.text_centered(664 + 158, 486, "ONE TEXT FOR 200 NATIONS",
                     2, GREY)

    cv.hline(44, 528, W - 88, INK, 3)

    # ---- story grid, two columns
    c1, c2, cw = 44, 540, 440
    cv.vline(512, 540, 398, FAINT, 2)
    rows = (540, 676, 812)
    for yy in (668, 804):
        cv.hline(44, yy, W - 88, FAINT, 2)

    story(cv, c1, rows[0], cw,
          "WAR AT SEA \u00b7 STRAIT OF HORMUZ",
          ("BAHRAIN SAYS IRAN STRUCK", "PLANT; TANKERS HIT"),
          "MANAMA SAYS AN IRANIAN STRIKE SET A PLANT ABLAZE. "
          "TWO TANKERS WERE STRUCK IN THE STRAIT - UKMTO.")
    story(cv, c2, rows[0], cw,
          "ARMS CONTROL \u00b7 GENEVA",
          ("STATES OPEN PATH TO A", "'KILLER ROBOT' PACT"),
          "128 COUNTRIES AGREE TO DRAFT RULES ON AUTONOMOUS "
          "WEAPONS OVER TWO YEARS. CAMPAIGNERS WANT MORE.")
    story(cv, c1, rows[1], cw,
          "DEFENCE \u00b7 WASHINGTON",
          ("PENTAGON MOVES TO CURB", "TIES WITH CANADA"),
          "AFP REPORTS THE US DEFENCE DEPARTMENT IS MOVING TO "
          "RESTRICT ITS COOPERATION WITH OTTAWA.")
    story(cv, c2, rows[1], cw,
          "WORLD COURT \u00b7 COX'S BAZAR",
          ("ROHINGYA HAIL GENOCIDE", "VERDICT ON MYANMAR"),
          "REFUGEES WELCOME THE UN COURT'S GENOCIDE RULING; UN "
          "ASSEMBLY CHIEF: 'YOU WILL NOT BE ALONE.'")
    story(cv, c1, rows[2], cw,
          "ENERGY \u00b7 TEHRAN",
          ("IRAN TO RATION POWER", "FROM SUNDAY"),
          "ROLLING CUTS OF UP TO TWO HOURS A DAY START SUNDAY "
          "AS WAR DAMAGE DEEPENS THE ENERGY CRUNCH.")
    story(cv, c2, rows[2], cw,
          "TRAVEL \u00b7 BRUSSELS",
          ("BELGIUM BRACES FOR AIR", "TRAFFIC SHUTDOWN"),
          "A NATIONAL STRIKE ON MONDAY THREATENS TO HALT FLIGHTS "
          "ACROSS BELGIUM, AFP REPORTS.")

    # footer
    cv.hline(44, 950, W - 88, INK, 3)
    cv.text_centered(W // 2, 962,
                     "FROM WIRE REPORTS OF 22 NOVEMBER 2026 \u00b7 AFP "
                     "\u00b7 AP \u00b7 REUTERS \u00b7 UN NEWS",
                     2, GREY)
    return cv


# ---------------------------------------------------------------- png

def encode_png(cv):
    raw = bytearray()
    row_bytes = cv.w * 3
    for yy in range(cv.h):
        raw.append(0)
        raw += cv.px[yy * row_bytes:(yy + 1) * row_bytes]

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    return png


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    data = encode_png(compose())
    (out_dir / "entry.png").write_bytes(data)


if __name__ == "__main__":
    main()
