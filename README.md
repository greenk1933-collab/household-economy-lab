# household-economy-lab
# The Household Economy Data Tools. By Kiernan Green, for consideration of The Globe and Mail Personal Finance Unit.

Three functioning, local Canadian personal-finance data-journalism pilots. Research snapshot: **November 10, 2026**. Independently developed; not commissioned or endorsed by The Globe and Mail.

## Open the products

**On the computer where this bundle was built:** double-click **Launch Lab.cmd**. It uses the already installed workspace runtime and opens `http://127.0.0.1:8501`. Allow a few seconds for the app to start, then refresh the browser if needed. Keep its terminal open; Ctrl+C stops the server. No paid credentials or cloud publication are required. If port 8501 is occupied, run `powershell -File .\launch.ps1 -Port 8502`.

**On another computer:** install Python 3.12 or later, open a terminal in this directory and run:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py --global.developmentMode false
```

On macOS/Linux use `.venv/bin/python` instead. `setup.ps1` performs the Windows installation. Installing dependencies needs internet; running the supplied snapshots does not. No private account balances are transmitted by these calculators. Server binding is loopback only.

## What you get

1. **Credit-card payments:** an audit of 24 product-family/jurisdiction records across 11 issuer brands. Six verified Tangerine product/jurisdiction combinations are enabled for simulation, with adjustable balances, APRs, promotional expiry and payments, two payoff paths, and CSV export. Shared contracts are not counted as independent cards. Unmatched issuer terms remain audit-only.
2. **Ontario housing:** an exact schedule calculator within its stated builder-purchase scope; a separate live supply/demand incidence diagram grounded in the original CECN104 Module 4 pp. 30–34; and a regional index/construction explorer plus verified builder offers. Quote-basis and rebate-assignment controls prevent double subtraction. The product makes no causal rebate-capture claim.
3. **Canadian value added:** official 2022 industry multipliers, 12 display categories, direct/upstream GDP and labour-income components, comparisons, downloads and 2026 context. A separate retail sensitivity calculator takes explicit user assumptions. It does not pretend that a producer-price coefficient measures a retail product's Canadian content.

The `exports/` folder contains three reviewed PNG/SVG graphics. `reports/` includes combined source register, raw-file hashes, table lineage, data dictionaries, coverage, findings, methods, limits, test results and interview briefs. The individual project folders retain the complete scripts, raw sources and processed data.

## Rebuild and test

With the environment installed and activated:

```text
python pipeline.py
python -m pytest -q
```

`pipeline.py` is an **offline rebuild**. For an explicit source refresh:

```text
python pipeline.py --acquire --test
```

Source websites can replace documents at existing URLs. Review contract amendments, statutory changes and manual transcription scope before treating refreshed files as newly verified. A bulk refresh does not autonomously adjudicate new legal language. The full archive retains roughly 200 MB of original public downloads; the labour archive is the largest. Parsing the labour table uses chunks. Graphics require Matplotlib; no external image-generation API is used.

On this existing Codex workspace, the bundled dependencies live outside the distributable under `work/pydeps`. `launch.ps1` detects that environment; a portable copy uses `.venv` instead. Runtime packages are not duplicated in the ZIP.

## Findings you can demonstrate

- With the documented Tangerine non-Quebec rules and the disclosed $11,000 opening-debt / $600 monthly scenario, highest-rate-first excess allocation reduces calculated interest by **$95.16**; both paths take 22 periods. This is a simplified scenario, not an account statement.
- An eligible non-first-time $1 million pre-HST new-home purchase receives **$130,000 total relief**, including **$24,000 ordinary Ontario relief**: the increase over ordinary rebates is **$106,000**. Legal entitlement is not the same as measured economic benefit.
- Official 2022 coefficients associate **$73.90 Canadian GDP** with $100 of domestic household-furniture/cabinet industry output delivered to final demand at basic prices. This does not mean $73.90 of every retail furniture purchase stays in Canada.

See `reports/findings.md` and the source register for original document/table locators, units, dates and caveats.

## Material limits

No verified matched pre/post property panel was obtainable; four historical search-index observations are explicitly quarantined. There is no identified developer-capture percentage or invented regional elasticity. Published supply/demand estimates have different scopes and remain separate from the scenario inputs. No original transaction interviews or private statements were obtained.

Official detailed retail margin/import matrices were available on request rather than acquired through public bulk files. The value-added model therefore uses an official-multiplier fallback with clearly hypothetical retail decomposition. It makes no brand-content, net job-creation or causal net-GDP claim.

The housing calculator excludes owner-built/rental/co-op/leased-land/assignment/non-resident cases, unusual tax timing and new original agreements after March 2027. Other closing charges are included only when entered. Six Tangerine variants are supported, rather than institution-specific calculations with unverified minimum/APR terms.

## Private source context

`inputs/` preserves the user's course material and interview conversation for this private handoff. Those files are not open-licensed merely because they were supplied. Do not publish that folder or wholesale issuer/builder PDFs without checking rights. Official statistical reuse/licence notes are retained in the source register. No external message, purchase or public deployment was performed.

## Verification and delivery status

The full offline pipeline completed and **90 automated tests passed**. See [browser and launch checks](reports/browser_qa.md), [acceptance and outstanding evidence](reports/acceptance.md), and [execution record](reports/progress_log.md). The preview servers were stopped after verification; use the launcher to reopen the products.
