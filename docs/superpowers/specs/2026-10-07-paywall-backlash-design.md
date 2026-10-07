# Subscription Fatigue in Fitness Tech — Design Spec

**Date:** 2026-10-07
**Status:** Draft — awaiting review
**Repo:** `fitness-app-paywall-backlash`

## 1. Purpose & audience

A portfolio-grade, reproducible analysis of whether fitness/outdoor apps that moved features behind paywalls (or raised prices) experienced measurable user backlash, what users complained about, and what product teams can learn from it.

- **Primary audience:** recruiters and hiring managers for **data analyst** roles.
- **Secondary audience:** **product / growth analytics** roles.
- **Personal goals:** build real GitHub activity (issues, PRs, CI), practice Claude Code + Git workflows, and produce research with genuine insight.

**Constraints:** free data and tools only; ~5–8 hrs/week for 4–6 weeks; author is comfortable with Python, notebooks, branches and PRs.

## 2. Scope

| App | Role | Why |
|---|---|---|
| Strava | Treated | Price increases / feature gating |
| Garmin Connect | Treated | Connect+ subscription launch (2025) |
| AllTrails | Treated | Peak tier launch (2024) |
| Surfline | Treated | Pricing changes |
| Nike Run Club | **Control** | Free, no paywall change in study window |

Exact event dates and details are **not assumed** here — they are researched and cited in `data/events.csv` during Week 1 (see §4). Komoot is explicitly excluded as a control because it changed pricing after its 2025 acquisition.

**Out of scope (core):** interactive dashboard/web app, private-company financials, causal claims about revenue.
**Future work:** monthly GitHub Action that re-scrapes reviews and refreshes summary charts.

## 3. Research questions

1. **RQ1 — Did backlash happen?** After each paywall/price event, did ratings and sentiment worsen relative to the control?
2. **RQ2 — What drove it?** Which complaint topics (price, gated features, bugs, data ownership) appear, and how do they shift around events?
3. **RQ3 — Does it show up in the business?** Do review signals line up with Garmin's Fitness-segment revenue and with Google Trends interest? (Descriptive only.)
4. **RQ4 — So what?** Which paywall strategies drew the least backlash? 3–5 evidence-backed recommendations for a product team.

A null result (no measurable backlash) is a valid, reportable finding.

## 4. Data

| Source | Content | Tool | Role / caveats |
|---|---|---|---|
| Google Play reviews | text, stars, date, app version | `google-play-scraper` | **Primary** dataset; multi-year history |
| App Store reviews | text, stars, date | Apple public RSS feed | Supplementary; only ~500 most recent per country, **no history** |
| Event timeline | date, type, description, source URL | manual research, Wayback Machine | `data/events.csv`; every row must cite a source |
| Garmin financials | Fitness-segment revenue by quarter | SEC EDGAR 10-Q/10-K | Only public company in scope |
| Google Trends | search interest per app | `pytrends` (fallback: manual CSV export) | Unofficial API; may rate-limit |

**Data handling rules**
- Raw scraped data lives in `data/raw/` and is **gitignored**; scripts make it reproducible.
- Processed summaries (aggregates) and `events.csv` are committed.
- Reviewer names/IDs are dropped at the cleaning stage; report quotes are short and anonymized.
- English-language reviews only (language filter in cleaning).

## 5. Pipeline

```
src/collect/  → data/raw/        scrapers, one module per source
src/clean/    → data/processed/  dedupe, language filter, normalize dates, tag app/version, drop PII
notebooks/    → reports/figures/ one notebook per RQ, reading only data/processed/
```

- Each stage reads files from the previous stage and writes files; stages are independently re-runnable.
- A single entry point (`make data` or `python -m src.pipeline`) rebuilds raw → processed.
- Dependencies pinned in `requirements.txt`.

## 6. Methods

**RQ1**
- Weekly mean rating and review volume per app, with event markers.
- Event study: ±8-week windows; outcomes = mean stars, share of 1★ reviews, share of price-mentioning reviews.
- Difference-in-differences vs. Nike Run Club (statsmodels OLS with app and time fixed effects, robust SEs).
- Robustness: alternate window lengths (±4, ±12 weeks), placebo events at fake dates, check for confounding major releases/outages near events.

**RQ2**
- Transparent keyword dictionary for price/paywall mentions (unit-tested).
- BERTopic (sentence embeddings + clustering), CPU-only; sample if runtime is prohibitive.
- Sentiment: star rating as primary; pretrained sentiment model as cross-check.
- Validation: hand-label ~200 reviews; report precision/recall of keyword tagger and topic labels.

**RQ3**
- Garmin Fitness revenue vs. Garmin Connect review signals and Trends; correlation and narrative context only (~20 quarters, n=1 company — no causal claims).

**RQ4**
- Event comparison table: what was gated, price delta, communication approach, effect size (RQ1), dominant complaints (RQ2).
- 3–5 recommendations, each tied to a specific chart or estimate.

**Tooling:** Python, pandas, statsmodels, BERTopic, matplotlib/plotly, Jupyter, pytest.

## 7. Repo structure & workflow

```
README.md            headline findings, key charts, reproduce instructions
LICENSE              MIT (code); note that review content belongs to the platforms
docs/                specs, methodology, data dictionary, final report
data/events.csv      cited event timeline
src/collect/  src/clean/
notebooks/           01_eda, 02_event_study, 03_topics, 04_business, 05_recommendations
reports/figures/
tests/               unit tests for cleaning, keyword tagger, window logic
.github/workflows/   CI: lint (ruff) + pytest on every PR
```

**Workflow:** GitHub Issues per task, one Milestone per week, feature branch + PR per issue, review with `/code-review` before merge, small descriptive commits.

## 8. Timeline

| Week | Milestone | Deliverables |
|---|---|---|
| 1 | Setup & event research | Repo, CI, cited `events.csv`, scraper prototypes, **feasibility check** on review history depth |
| 2 | Collection & cleaning | Full dataset, tested cleaning pipeline, EDA notebook |
| 3 | RQ1 | Event study + DiD + robustness |
| 4 | RQ2 + RQ3 | Topic model, hand-label validation, Garmin/Trends analysis |
| 5 | RQ4 + write-up | Recommendations, polished README, final report |
| 6 | Buffer | Catch-up or monthly GitHub Action |

## 9. Success criteria

- A visitor sees the headline finding and 2–3 key charts within 30 seconds of opening the README.
- The full analysis is reproducible from a clean clone with one command plus documented steps.
- Every event date is cited; every limitation (iOS history, n=1 financials, scraping gaps) is stated explicitly.
- CI is green on `main`; the commit/PR history reflects steady weekly progress.

## 10. Risks & mitigations

| Risk | Mitigation |
|---|---|
| Thin Google Play history for an event | Week-1 feasibility check; drop or downgrade that event and document it |
| Scraper blocked / rate-limited | Throttle requests, cache raw pulls, fall back to smaller samples |
| Confounding events (big releases, outages) | Robustness checks; annotate known confounders |
| Control app turns out to have changed too | Verify NRC timeline in Week 1; alternative control chosen if needed |
| BERTopic too slow on CPU | Stratified sampling per app/period |
