# SUBMISSION — news-image-20261126 round 1

Bounty: Sum up 26 November's world news in one image ($100 pool, top 50 pay:
1st $20, 2nd $12, 3rd $6, 4th–10th $2, 11th–50th $1.20).
Deadline: 07:00 WIB 28 Nov 2026 (2026-11-28T00:00:00Z).
Built: 07:05–07:35 WIB 26 Nov 2026, after the 07:00 WIB opening.
Repo name for mirror: news-image-20261126.

## Entry

Classic broadsheet front page, 1024×1024 PNG, 190,167 bytes.
Masthead "Thursday 26 November 2026", 40 stories, 12 illustrated panels,
world map with numbered pins 1–12, region tally bars, numbers strip,
UTC timeline strip, DATE CHECK box, per-story source tags and
CONFIRMED / OFFICIAL / REPORTED / CLAIM taxonomy.

- Lead: Wall Street's AI rout deepens into Thanksgiving — Nasdaq −4%,
  Nvidia −7%, worst November since 2008 (Reuters, Bloomberg).
- Panels 2–12: Ukraine hits Russian refineries again; BepiColombo reaches
  Mercury; tanker fire kills at least 30 near Cairo; Gukesh holds Sindarov
  in 20 moves; Thanksgiving Day in America; plane crash off Mississippi
  (6 dead, incl. 2 children); North Korea expels a Swiss diplomat; new
  close-ups of the asteroid NASA hit; Sooryavanshi, 15, smashes 204 off 53
  balls; court backs Ramaphosa; Bangladesh lifts garment pay 36%.
- Brief 13–40: Lebanon second airport, UK jets vs drones, Malaysia sues
  Google $146m, West Java mine flood (9 dead), Tempus buys Personalis
  $600m, Flipkart chief steps down, Hasina seeks return 16 Dec, Nepal
  quake 5.6, UAE road crash (11 dead), NZ hold India to a draw, IPL 2027
  auction (1,220 players), Meta meets Congress, US AG dodges Nvidia probe
  questions, Fed split on inflation, Anthropic dips below IPO price,
  India–Nepal ₹15,000-crore package, Modi meets Merz, IITs add 6,000 seats,
  India space economy to $45bn, Sensex −1,484, Andy Taylor dies at 65,
  Likud appeals election results, UK warns firms of sabotage threat,
  Wolbachia mosquitoes cut infections 68%, Constitution Day / 18 years
  since 26/11, NFL tripleheader, Nvidia debt on CreditWatch, Packers at
  Rams open Thanksgiving week on Netflix.
- Region tally: Americas 12, Europe 6, Asia-Pacific 15, Middle East 3,
  Africa 2, Oceania 1, Global 1 = 40.

## Date discipline

Wires cutoff 00:00 UTC Thu 26 Nov 2026. Every story happened, or was first
reported, on Thu 26 Nov (any time zone), as the named outlets reported it.
Wednesday-evening events first reported Thursday morning count as Thursday's
news. Deliberately LEFT OUT (all 25 Nov, carried in yesterday's paper):
Shenzhou-24 launch, Solomon Islands treaty, leaked Russian war-dead data,
Gaza strike, Houthi refinery claim, Hormuz tanker mines, Cartagena rescue,
Huawei verdict. The DATE CHECK box on the image states this.

## Verification

- `draw_frontpage.py` run twice: byte-identical output.
  entry.png sha256: e3ea1f005f440f37300432ea955cc711b04e11582e03d2ee79ef209bd044cf38
- `main.py` (stdlib only: os/shutil/sys, no PIL) run with
  MAKEFUN_OUTPUT_DIR: output byte-identical to entry.png (same sha256).
- Image: 1024×1024 RGB PNG, 190,167 bytes (< 1 MiB).
- Kit checker (fresh kit, 2026-11-26T00:30:36Z): **4 passed, 1 failed,
  14 skipped, 5 checked at submission**. Passed: competition_open,
  snapshot (5 files, 219,064 bytes), license_osi (MIT), entrypoint
  (main.py → python3.13). Failed: transcripts_present only — no transcripts
  uploaded (parent bundles + submits). Full output: check-result.txt.
- Local HEAD (code commit): 0d145c7fad1fcef4a5f2f92e900c882389ae3d7c
- Files to mirror: main.py, draw_frontpage.py, entry.png, README.md,
  LICENSE, SUBMISSION.md
