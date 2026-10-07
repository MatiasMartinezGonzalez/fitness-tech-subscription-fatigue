# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

Analysis of user backlash to paywall and pricing changes in fitness/outdoor apps — Strava, Garmin Connect, AllTrails, Surfline (treated) vs. Nike Run Club (control) — using app-store reviews, event studies, difference-in-differences, topic modeling, Garmin financials, and Google Trends.

The full design lives in [docs/design/2026-10-07-paywall-backlash-design.md](docs/design/2026-10-07-paywall-backlash-design.md). Read it before planning or implementing anything; it is the source of truth for scope, research questions, methods, and timeline.

## Working agreements

- **Build in public:** small, frequent, descriptive commits; one feature branch + PR per GitHub Issue; one Milestone per week. Never commit directly to `main` once the repo is published.
- **Writing voice:** README, design docs, methodology, and reports read as professional research written by the author — no conversational asides addressed to the reader.
- **Data:**
  - Raw scraped data goes in `data/raw/` and is never committed; processed aggregates and `data/events.csv` are.
  - Drop reviewer names/IDs during cleaning; quote reviews only briefly and anonymized.
  - Every row in `data/events.csv` must cite a source URL — never guess event dates.
- **Rigor:** state limitations explicitly (iOS review history is ~500 most recent only; Garmin is the only public financials; RQ3 is descriptive, not causal). Null results are valid findings.
- **Free tooling only.** Python, pandas, statsmodels, BERTopic, matplotlib/plotly, Jupyter, pytest, ruff.

## Commands

_To be filled in as the pipeline is built (environment setup, `make data`, tests, lint)._

## Layout

```
docs/            design spec, methodology, data dictionary, final report
data/            events.csv (committed); raw/ (ignored); processed/
src/collect/     scrapers, one module per source
src/clean/       cleaning pipeline
notebooks/       one notebook per research question
reports/figures/ exported charts
tests/           unit tests for cleaning, keyword tagger, window logic
```
