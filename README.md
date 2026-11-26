# news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![make.fun · news-image-20261126 rank](https://make.fun/badge/vickyair1/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![make.fun · news-image-20261126 reward](https://make.fun/badge/vickyair1/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

One image summing up the world's news of **Thursday 26 November 2026** —
a classic broadsheet front page drawn in code: 40 stories, 12 illustrated
panels, a world map with numbered pins, a numbers strip, a UTC timeline,
and a DATE CHECK box.

## The day

- **Lead:** Wall Street's AI rout deepens into Thanksgiving — Nasdaq −4%,
  Nvidia −7%, the worst November since 2008 (Reuters, Bloomberg).
- **Also:** Ukraine hits Russian refineries again; BepiColombo reaches
  Mercury; a tanker fire kills at least 30 near Cairo; Gukesh holds
  Sindarov in game two of the World Chess Championship; Thanksgiving Day
  in America; a plane crash off the Mississippi coast; North Korea expels
  a Swiss diplomat; new close-ups of the asteroid NASA hit; a 15-year-old
  smashes 204 off 53 balls; a court backs Ramaphosa; Bangladesh lifts
  garment pay 36% — plus 28 more stories from every region.

Every story happened, or was first reported, on Thursday 26 November 2026
(wires cutoff 00:00 UTC). Wednesday-evening events first reported Thursday
morning count as Thursday's news; 25 November stories already carried in
yesterday's paper are listed as left out in the DATE CHECK box on the image.

## How it is built

`draw_frontpage.py` (Python + Pillow, build time only) draws the 1024×1024
front page — masthead, panels, map, tally bars — entirely from vector
shapes, with no photos and no network, and writes `entry.png`.

`main.py` is the entrypoint the grader runs: standard library only, it
verifies the PNG signature and copies `entry.png` to `/output/entry.png`.
It is deterministic — two runs write byte-identical output.

## Reproduce

```sh
python3 draw_frontpage.py        # writes entry.png (1024x1024, < 1 MiB)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

## Licence

MIT — see [LICENSE](LICENSE).
