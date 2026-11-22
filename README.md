[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/OG2BIT001/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/OG2BIT001/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# The World Today — Sunday 22 November 2026

An entry for the make.fun bounty **news-image-20261122**: "Sum up
22 November's world news in one image."

`main.py` (Python 3.13, standard library only, no network) draws a
newspaper front page for Sunday 22 November 2026 pixel by pixel — its
own hand-drawn 5x7 bitmap typeface, a wire-frame globe for the lead
art — and writes it as a PNG to `/output/entry.png` (or to
`$MAKEFUN_OUTPUT_DIR/entry.png` outside the grader's container). The
program is deterministic: run it twice and the bytes are identical.
The rendered image is kept in this repository as `entry.png`.

The front page carries the day's seven biggest stories, all first
reported on 22 November 2026:

- **COP31 collapses in Antalya** — after two days of overtime, the
  EU rejects a final text that names no fossil fuels; the longest
  climate summit ever ends with no deal, and Guterres is "deeply
  disappointed" (Al Jazeera, Rappler, Vanguard, The Hindu).
- **Bahrain says Iran struck a plant; tankers hit in Hormuz** —
  Manama blames Tehran for a fire at a civilian industrial site; two
  tankers struck in the strait, per UKMTO (AFP).
- **Russian drone flattens flats near Kyiv** — five killed in Dymer
  as a five-storey block collapses; rescuers hunt for the missing
  (AP, Kyiv Independent).
- **States open a path to a "killer robot" pact** — 128 countries in
  Geneva agree to draft rules on autonomous weapons over two years
  (AFP).
- **South Korea's education minister quits** — Choi Kyo-jin resigns
  over the AI-cheating chaos around the college entrance exam
  (Yonhap).
- **Rohingya hail the genocide verdict on Myanmar** — refugees
  welcome the UN court's ruling (AP).
- **Verstappen wins a wild Las Vegas GP** — 35 lead changes in 50
  laps; the Red Bull star beats Norris by 0.639 seconds
  (Formula 1, Al Jazeera).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png (1024x1024 PNG, well under 1 MiB)
```

## License

MIT — see `LICENSE`.
