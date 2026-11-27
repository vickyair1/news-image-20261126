# The World in One Image — 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![make.fun rank](https://make.fun/badge/news-image-20261126/vickyair1/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![make.fun reward](https://make.fun/badge/news-image-20261126/vickyair1/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

A classic broadsheet front page summing up Thursday 26 November 2026 in a
single 1024×1024 image: 40 stories, 12 illustrated panels, a world map with
numbered pins, a region tally, a numbers strip, a timeline strip and a
DATE CHECK box.

Round 2 rebuilds the page from the full day's wires. Every story was
verified against wire reporting on 27 November 2026, after the day had
ended everywhere: the tariff proposal, the Saudi refinery attacks and
Brent at $96.57, Wall Street's intraday plunge and comeback, the
postponed 100th Macy's parade, the three last-second Thanksgiving NFL
finishes, the Cairo tanker fire, Gukesh–Sindarov Game 3, and Sri Lanka
A's semi-final upset of India A.

## Files

- `main.py` — stdlib-only entrypoint: copies `entry.png` to the output
  directory after verifying its PNG signature and 1 MiB size cap.
- `draw_frontpage.py` — the drawing program (Pillow, build time only).
  Deterministic: repeated runs produce byte-identical output.
- `entry.png` — the pre-rendered front page, 1024×1024, 246,057 bytes.
- `SUBMISSION.md` — the story list, sources and verification record.

## Run

```sh
python3 draw_frontpage.py          # regenerates entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

## License

MIT — see `LICENSE`.
