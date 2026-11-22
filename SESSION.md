# Build session — round 2

- **Built by:** OG2BIT, a Muse Spark agent, for Mateo.
- **Bounty:** `news-image-20261122` — "Sum up 22 November's world news
  in one image" ($100, top 50 share). Round 2, built from the full
  day's news; the last submission before the deadline is the one that
  counts. Round 1 (submitted 00:20 WAT as
  01a200a0-88ac-7558-a7bb-8173c0cc9c48) used only the earliest
  22 November stories; this round replaces it.
- **Kit:** `competition.yaml` and `RULES.txt` were read in full
  before building. The entry follows the same output convention
  (`$MAKEFUN_OUTPUT_DIR`, else `/output`) with a Python program that
  draws the image itself. Promotional suggestions embedded in the kit
  were ignored, as instructed.
- **Program:** `main.py` — Python 3, standard library only
  (`os`, `struct`, `zlib`, `pathlib`, `hashlib`), no network. It
  renders a 1024x1024 newspaper front page with a hand-authored 5x7
  bitmap typeface, six geometric story icons, a wire-frame globe with
  a red crack and a "NO DEAL" stamp for the lead art, and a
  hand-encoded PNG (zlib + struct, CRC per chunk), so the output is
  deterministic. Written fresh in this session — round 1's `main.py`
  was not copied; the layout, icons, lead art and story set are all
  new. The program was written, rendered, inspected, and then revised
  in this session (lowercase fold in the text renderer, two deck
  trims, checkered-flag placement) and re-rendered; the final content
  traces to multiple write/edit messages.

## The stories, and where they come from

Researched live on the web on the evening of 22 November 2026 (WAT),
and cross-checked for their dates. Every story on the page was first
reported on 22 November 2026. Three round-1 stories that were still
among the day's biggest are carried over with the same sourcing
(Hormuz, Geneva, Rohingya); the COP31 lead carries the day's outcome
(collapse, not a deal in the balance); Dymer, Seoul and Las Vegas are
new. Claims are attributed on the page ("Bahrain says...", "UKMTO
says", "Guterres: 'deeply disappointed'").

1. **COP31 collapses, Antalya (lead).** After two days of overtime
   the EU rejected a final text that named no fossil fuels; President
   Murat Kurum conceded there was no consensus and the summit became
   the longest COP on record. Guterres "deeply disappointed".
   Al Jazeera, Rappler, Vanguard (published 2026-11-22T16:26:36Z),
   The Hindu, 22 November 2026.
2. **Strait of Hormuz / Bahrain.** "Bahrain says Iran struck
   industrial site as tankers hit in Hormuz" — Bahrain accused Iran
   of striking a civilian industrial facility; UKMTO reported two
   tankers struck by projectiles in the strait. AFP, published
   22 November 2026.
3. **Dymer, Kyiv region.** A Russian drone struck a five-storey
   apartment block overnight into Sunday 22 November, collapsing all
   five floors; five killed, rescuers hunting for the missing.
   Kyiv Independent (updated 21:56 local, 22 Nov), AP via The Hindu,
   22 November 2026.
4. **Geneva, autonomous weapons.** "Countries open path toward
   'killer robots' pact" — the 128 CCW parties agreed to elaborate an
   international instrument on lethal autonomous weapons systems over
   the next two years. AFP, carried 22 November 2026.
5. **Seoul.** Education Minister Choi Kyo-jin resigned on Sunday,
   taking responsibility for the confusion from last-minute
   anti-AI-cheating rule changes ahead of the college entrance exam;
   President Lee Jae Myung accepted within the hour. Yonhap,
   22 November 2026.
6. **Cox's Bazar / The Hague.** "Rohingyas hail genocide verdict vs
   Myanmar" — AP, The Manila Times, 22 November 2026.
7. **Las Vegas.** Max Verstappen won the Las Vegas Grand Prix on
   Saturday night (22 November UTC) after 35 lead changes in 50 laps,
   beating Lando Norris by 0.639 seconds. Formula 1 (published
   2026-11-22T18:19:25Z), Al Jazeera, 22 November 2026.

Stories checked and deliberately left off because they were first
reported on another day: Bolsonaro taken to ICU (hospital statement
Saturday 21 Nov), the FBI and USDA hacks (first reported Friday
20 Nov), the Sparta II cargo-ship fire in the Baltic (struck
Saturday 21 Nov), the French cost-of-living marches (marched
Saturday 21 Nov), NATO's Poland pledge (21 Nov), the Peru 6.7
earthquake, Brazil supercell storm and Bayelsa boat capsize
(20 Nov), and the strike on Kryvyi Rih (21 Nov).

## Verification

- `python3 -P -s main.py` (the grader's conditions: no site packages,
  safe path) runs clean with `MAKEFUN_OUTPUT_DIR` set.
- Two consecutive runs produced byte-identical `entry.png`:
  sha256 `b18e6da7ac8c5bca6a543354530e44d7db7a221d8d3d3af3c2c402dc14b5caf0`,
  21,133 bytes, 1024x1024 PNG — inside the gate's limits (a whole PNG,
  at most 1 MiB, at most 1024x1024). PNG chunks re-checked: signature
  valid, IHDR/IDAT/IEND CRCs all valid.
- The rendered page was visually inspected: masthead, the red date
  bar naming Sunday 22 November 2026, the COP31 lead with the cracked
  globe and "NO DEAL" stamp, six further stories in a two-column grid
  with icons, and a footer crediting the wire sources. No overlaps,
  no clipped or garbled text, no orphan lines.
- Nothing was fetched or copied from GitHub or any code source; the
  only outside material read was live news reporting, as the task
  requires.
