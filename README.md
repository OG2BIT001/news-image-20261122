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

The front page carries the day's seven biggest stories, all reported
on 22 November 2026:

- **COP31 goes to the wire in Antalya** — summit president Murat
  Kurum tables a final text and urges a deal by 6am; the last fight is
  whether the pact names fossil fuels (Arab News, UN News).
- **Bahrain says Iran struck a plant; tankers hit in Hormuz** —
  Manama blames Tehran for a fire at a civilian industrial site; two
  tankers struck in the strait, per UKMTO (AFP).
- **States open a path to a "killer robot" pact** — 128 countries in
  Geneva agree to draft rules on autonomous weapons over two years
  (AFP).
- **Pentagon moves to curb defence ties with Canada** (AFP).
- **Rohingya hail the genocide verdict on Myanmar** — refugees
  welcome the UN court's ruling (AP).
- **Iran to ration power from Sunday** — rolling cuts as war damage
  deepens the energy crunch (AFP).
- **Belgium braces for an air traffic shutdown** — a national strike
  on Monday threatens to halt flights (AFP).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png (1024x1024 PNG, well under 1 MiB)
```

## License

MIT — see `LICENSE`.
