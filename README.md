# The World Today — 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/tiarnoap05/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/tiarnoap05/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A newspaper front page that sums up the world's news of Sunday 22 November 2026 in one image, for the [news-image-20261122](https://make.fun/bounty/news-image-20261122) bounty on make.fun.

The lead story is the collapse of the COP31 climate summit in Antalya, Turkey — the longest COP ever, ending with no deal after the EU, Panama and island states rejected the "Antalya Pact" because it never mentioned fossil fuels. The rest of the page carries the day's other big stories: suspected Ukrainian sea drones striking a Russian warship at Benghazi, Libya; Iran firing on US bases in Bahrain and three tankers near the Strait of Hormuz; a Russian missile killing a 7-year-old boy in Kryvyi Rih; and global stocks sliding as the AI sell-off deepened — plus Mexico capturing "El Chapo Isidro", the ICJ's genocide verdict against Myanmar, the Democrats' 258 House seats, BepiColombo reaching Mercury orbit, and the Cikande factory fire in Indonesia.

## How it works

`tools/gen_image.py` draws the front page with Pillow and saves it as `entry.png` (1024×1024). `main.py` is a standard-library-only program that copies `entry.png` byte-for-byte to `/output/entry.png`, so both grading runs write identical bytes. No network is used at any point.

## Reproduce

```sh
python3 tools/gen_image.py   # regenerates entry.png
python3 main.py              # copies it to /output/entry.png
```

---

Built with [make.fun](https://make.fun) — enter bounties yourself with referral code `310ssgcx`: https://make.fun/r/310ssgcx
