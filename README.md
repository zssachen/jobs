# AI & Robots Job Exposure Visualization

**Live site:** [zssachen.github.io/jobs](https://zssachen.github.io/jobs/)

An interactive visualization of AI and robot automation risk across every US occupation, built on top of BLS employment data and Andrej Karpathy's job-scoring project.

---

## Lineage / Data Provenance

```
BLS Occupational Outlook Handbook (public domain)
        |
        v
Andrej Karpathy — github.com/karpathy/jobs
  (Gemini Flash used to score each occupation 0–10 for AI exposure)
        |
        v
mariodian — github.com/mariodian/jobs
  (treemap front-end built on karpathy's dataset)
        |
        v
This project — github.com/zssachen/jobs
  (robot toggle, automation timelines, job search, sources panel)
```

The raw occupational scoring data originates from **karpathy/jobs**. The original treemap layout is adapted from **mariodian/jobs**. This project extends both with the features described below.

---

## Purpose

The original karpathy/jobs project visualises how exposed every US job title is to AI automation on a 0–10 scale. This extension asks two additional questions:

1. **What changes if dexterous robots reach human-level physical skill?** Many jobs that score low on AI exposure (construction, agriculture, healthcare aides) are vulnerable to robots even when AI alone cannot replace them. The "With Robots" mode applies evidence-based score boosts to those categories.

2. **When will each category be automated?** Using peer-reviewed research from 9 sources, each of the ~25 job categories is assigned a low/mid/high year range for when 80%+ of roles in that category could be automated. A weighted milestone shows when 80% of *all* US jobs cross that threshold.

---

## Features

| Feature | Description |
|---|---|
| **Treemap view** | Squarified treemap coloured by AI exposure score (0–10). Area = number of jobs. |
| **Columns view** | Bar chart view of job categories sorted by exposure score. |
| **Without / With Robots toggle** | Boosts exposure scores for physical/manual categories (e.g. construction +3, agriculture +2) assuming dexterous robots reach human-level skill. Scores capped at 10. |
| **Color by Timeline** | Recolours the treemap by predicted automation year: red = near-term (2025–2030), yellow = mid (2030–2045), blue = long-term (2045–2065+). |
| **Per-category timeline estimates** | Each category has a low/mid/high automation year derived from the 9 research sources. Visible on hover. |
| **80% milestone stat** | Employment-weighted calculation: the year by which 80% of all US jobs (by headcount) are predicted to no longer require a human. |
| **Job search** | Searchable dropdown of all 342 job titles. Keyboard-navigable (Up/Down/Enter/Escape). Selecting a job highlights it on the treemap and shows its score, category, employment count, and timeline. |
| **Provenance header** | Full data chain displayed across the top of the page with links to all original sources. |
| **Sources / citations panel** | Collapsible panel listing all 9 research papers with legal/access notes. |
| **Tooltip** | Hover any treemap cell to see job title, score, employment count, and automation timeline. |

---

## Research Sources

The automation timeline estimates are derived from the following peer-reviewed papers and industry reports. All are open-access or freely downloadable.

| # | Source | Key finding used |
|---|---|---|
| 1 | Frey & Osborne (2013) — *The Future of Employment*, Oxford | 47% of US jobs at high automation risk; office/admin and transport highest |
| 2 | McKinsey Global Institute (2017) — *A Future That Works* | 60% of occupations have 30%+ automatable activities; data processing 64–69% |
| 3 | Goldman Sachs (2023) — *The Potentially Large Effects of AI on Economic Growth* | 300M jobs exposed globally; legal/admin most affected in near term |
| 4 | OpenAI / Penn (2023) — *GPTs are GPTs* (Eloundou et al.) | 80% of US workers have 10%+ tasks exposed; highest in white-collar knowledge work |
| 5 | IMF (2024) — *Gen-AI: Artificial Intelligence and the Future of Work* | 40% of global jobs exposed; advanced economies 60% |
| 6 | WEF (2023) — *Future of Jobs Report* | 23% of jobs transformed by 2027; analytical/creative roles growing, clerical declining |
| 7 | Acemoglu & Restrepo (2022) — *Tasks, Automation, and the Rise in US Wage Inequality* | Historical automation impact; physical task categories last to automate |
| 8 | MIT Work of the Future (2023) — *Shaping the Future of Work* | Physical/outdoor roles remain human-complementary through 2035+ |
| 9 | ARK Invest (2023) — *Big Ideas 2023* | Dexterous robotics reaching cost-parity with human labour ~2030–2035 |

BLS data is **US Government public domain**. karpathy/jobs is a public GitHub repository (no explicit licence — will comply with any removal request). All research papers are cited for commentary/analysis purposes only; no copyrighted text is reproduced.

---

## Running Locally

The page is fully self-contained — no build step, no server, no external fetches.

```bash
git clone https://github.com/zssachen/jobs.git
cd jobs
# open index.html in any browser
```

To rebuild `index.html` from the raw data (after editing `_build.py`):

```bash
python3 _build.py
# outputs index.html; verifies 0 non-ASCII characters in markup
```

---

## Version History

| Version | Date | Notes |
|---|---|---|
| v1.0 | 2026-03-15 | Initial public release — treemap, robot toggle, timeline mode, job search, sources panel, provenance header |

---

## Credits

- **Andrej Karpathy** — [github.com/karpathy/jobs](https://github.com/karpathy/jobs) — original occupational AI-exposure scoring
- **mariodian** — [github.com/mariodian/jobs](https://github.com/mariodian/jobs) — original treemap front-end
- **BLS** — [bls.gov/ooh](https://www.bls.gov/ooh/) — employment data
- Extended and maintained by [zssachen](https://github.com/zssachen)
