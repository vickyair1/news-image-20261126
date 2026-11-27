# SUBMISSION — news-image-20261126 round 2

Bounty: Sum up 26 November's world news in one image ($100 pool, top 50 pay:
1st $20, 2nd $12, 3rd $6, 4th–10th $2, 11th–50th $1.20).
Deadline: 07:00 WIB 28 Nov 2026 (2026-11-28T00:00:00Z).
Built: 27 Nov 2026 ~23:00–00:30 WIB, after the day had ended everywhere.
Repo: https://github.com/vickyair1/news-image-20261126 (same repo, new commit).

## The lever (why round 2 beats round 1)

Round 1 scored 984,131 (rank 2,154/26,763 provisional, 22:00 run 27 Nov;
rank 1 = 991,711; rank 100 = 987,883). It was built at 00:05 UTC on 26 Nov
from overnight wires only, and fresh verification on 27 Nov found four
factual errors the pairwise judge can catch (criteria 1/3/4 — a day's news,
reads true, faithful):

1. LEAD was wrong: "Nasdaq sinks 4% into Thanksgiving / Nvidia -7%".
   Reality (Wed 25 Nov close): Nasdaq -0.62% at 23,586, Nvidia -3.9%;
   the -4.6% was the Nasdaq-100's intraday plunge before a comeback,
   and US markets were CLOSED on Thursday. Round 2 states the true
   numbers and the shutdown.
2. BepiColombo "reaches Mercury" was stale: orbit insertion was 21 Nov,
   announced 23 Nov. Removed; listed in DATE CHECK as left out.
3. Sooryavanshi's 204 was stale: played Tue 24 Nov. Removed; listed
   in DATE CHECK as left out.
4. Thanksgiving panel implied Macy's parade happened. It was POSTPONED
   (first time in 100 years) to Sat 28 Nov by a nor'easter. Round 2
   says so, with the 60 mph gusts and the NBC 2025 rerun.

Round 2 is built from the FULL day, verified after it ended:
- NFL Thanksgiving tripleheader as actually played: Bears 39-35 Lions,
  Eagles 39-38 Cowboys (21-point comeback, largest in Thanksgiving
  history), Bills 13-10 Chiefs — all three decided in the final 5 seconds.
- Chess Game 3 (Thu 26 Nov, 60-move draw, 1.5-1.5) replaces the
  Wed 25 Nov Game 2 panel.
- Cricket semi-final as actually played Thu 26 Nov: Sri Lanka A chase
  318 in 41.3 overs, beat India A by 8 wickets (Croospulle 116,
  Jayawardena 105).
- New genuine 26 Nov stories round 1 missed: Jazan refinery hit
  (1 killed, Saudi Energy Ministry), Brent settles $96.57, Bank of Korea
  hikes 25bp to 3.25%, Europe rallies (Stoxx +1.75%, DAX +2.08%),
  second judge blocks the birthright order, Ebola 11,986 cases /
  5,871 deaths, OPEC+ meets Sun 29 Nov.
- Kept and corrected: Cairo tanker fire is 31 dead (round 1 said 30);
  Mississippi crash is framed by the Thu victim identifications;
  the Swiss-envoy expulsion (Wed 25 Nov) is listed in DATE CHECK
  as left out, not presented as Thursday news.

## Entry

Classic broadsheet front page, 1024x1024 PNG, 246,057 bytes.
Masthead "Thursday 26 November 2026", 40 stories, 12 illustrated panels
(each with its own 64x64 vector pictogram), world map with numbered pins
1-12, region tally, numbers strip, timeline strip, DATE CHECK box,
per-story source tags and CONFIRMED / REPORTED / CLAIM taxonomy.

- Lead: Trump proposes tariffs on 14 partners (Section 301, 20-40%).
- Panels 2-12: Houthi refinery attacks / Brent $96.57; Wall Street's
  wild ride and Thanksgiving shutdown; Macy's parade postponed;
  Thanksgiving NFL thrillers; Cairo tanker fire (31 dead); Gukesh-
  Sindarov Game 3; Sri Lanka A stun India A; Bank of Korea 3.25%;
  Russia's 112 drones / Ukraine refinery strikes; birthright order
  blocked; Ebola toll in DR Congo.
- Briefs 13-40: Seoul/Coupang, Nvidia shipment halt, Altria/Imperial,
  UniCredit/Commerzbank, BoE $4tn AI warning, Kioxia/Nvidia, US GDP
  4.3%, core PCE 3.3%, HP +11.5%, Sudan RSF strikes, Indonesia mine
  flood, Greece strike, Taiwan sortie, King Tides, Hormuz mines,
  Senegal AFCON reinstatement, 10-yr yield 4.80%, futures +0.5%,
  Nikkei +0.86%, Europe rally, WTI $84.84, OPEC+ Sunday, Mamdani
  skips Saturday's parade, Dubai tanker report, Jeddah drone
  intercept, Japan slams tariffs, Rams 26-13 Packers, Israeli
  cabinet meeting cancelled.
- Region tally: Americas 14, Europe 7, Asia-Pacific 9, Middle East 5,
  Africa 4, Oceania 0, Global 1 = 40.

## Date discipline

Wires cutoff 00:00 UTC Fri 27 Nov 2026. Every story happened, or was
first reported, on Thu 26 Nov, except Wednesday-evening breaks carried
in Thursday's wires (tariffs proposal, Ras Tanura claim, Cairo fire),
which the DATE CHECK box names. Deliberately LEFT OUT (not 26 Nov):
BepiColombo Mercury arrival (21 Nov), Sooryavanshi's 204 (24 Nov),
Gukesh-Sindarov Game 2 (25 Nov), Swiss envoy expulsion (25 Nov).

## Verification

- `draw_frontpage.py` run twice: byte-identical output.
  entry.png sha256: 736469ea4e7a08bbd47df634ae88f0d5797e7ce7dbba581f3413e04a223dbcdf
- `main.py` (stdlib only: os/shutil/sys, no PIL) run with
  MAKEFUN_OUTPUT_DIR: output byte-identical to entry.png (same sha256).
- Image: 1024x1024 RGB PNG, 246,057 bytes (< 1 MiB).
- Local validation (no local scorer exists for this bounty — the kit
  states grading is server-side only): structural comparison against
  round 1 plus per-story wire verification above; visual inspection of
  the render at full size (headers, timeline, tally, map pins, briefs
  all legible, no overlaps after two fix rounds).
- Kit checker (2026-11-27T15:47:05Z, commit dd53f72f): **4 passed,
  1 failed, 14 skipped, 5 checked at submission**. Passed:
  competition_open, snapshot (6 files, 284,611 bytes), license_osi
  (MIT), entrypoint (main.py -> python3.13). Failed:
  transcripts_present only — no transcripts uploaded (parent bundles
  + submits). Full output: check-result.txt.
- Local HEAD (code commit): dd53f72fdc7376ccfeab193b0083daadc035a8df
- Files to mirror: main.py, draw_frontpage.py, entry.png, README.md,
  LICENSE, SUBMISSION.md
