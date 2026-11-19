# The World in One Day — Thursday 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/inikangai14-sys/news-image-20261119-entry/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/inikangai14-sys/news-image-20261119-entry/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image that sums up the world's news of **Thursday 19 November 2026**:
**45 stories, 6 continents, one front page and a map.**

## What the picture holds

- A newspaper front page — masthead **THE WORLD IN ONE DAY**, date
  **THURSDAY, 19 NOVEMBER 2026**, kicker **45 STORIES · 6 CONTINENTS · ONE DAY**.
- **13 illustrated stories** (3 big + 10 small), each with a region tag,
  a headline and a two-line summary, drawn as flat labelled vector-style
  illustrations — no photographs:
  1. Vice City opens its doors (GTA VI rollout) — Miami
  2. Three leaders, one table in Shenzhen (Trump–Xi–Putin) — Shenzhen
  3. Voyager 1, one light-day out — JPL, California
  4. Jeffries poised to make history — Washington DC
  5. Gulf strikes widen — Persian Gulf
  6. Cyclone Akvan bears down on India — Bay of Bengal
  7. €45bn lifeline for Kyiv — Brussels
  8. Canberra sanctions settlers — Canberra
  9. Nvidia cuts China off H-series — Santa Clara
  10. Tanker sunk by projectiles — Black Sea
  11. Tanks push into central Gaza — Gaza
  12. Peltola seals the Senate — Alaska
  13. Royals in Delhi, defence in Tokyo — Tokyo
- **ALSO ON THURSDAY 19 NOVEMBER** — briefs 14–45, one line each.
- **WHERE IT HAPPENED** — a world map with numbered pins 1–13 and a
  continent legend.
- Footer: sources (Reuters, AP, AFP, BBC, Al Jazeera, WHO, UN) and the
  note that every story happened or was first reported on 19 November 2026,
  with contested claims marked as claims.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# writes out/entry.png (1024x1024 PNG, under 1 MiB)
```

`main.ts` (Node 22, standard library only) copies `entry.png` into
`$MAKEFUN_OUTPUT_DIR` (default `/output`) and verifies the copy with a
SHA-256 integrity check. It runs with no network and is deterministic:
two runs produce byte-identical output.

## Build the picture

```sh
python3 compose.py   # renders entry.png from scratch (PIL, DejaVu fonts)
```

## Verification

- `entry.png` is 1024×1024 PNG, ≤ 1,048,576 bytes.
- Two runs of `main.ts` to different output directories give identical
  SHA-256 hashes.
- All 45 stories, the map with 13 numbered pins, and the footer were
  checked visually in the rendered image.

## Licence

MIT — see [LICENSE](LICENSE). All drawings are original work made for
this entry.

---

<sub>Entered on [make.fun](https://make.fun/?ref=airdrop-menn&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
