# Project Plan — Subscription Fatigue in Fitness Tech

**Date:** 2026-10-07
**Status:** Draft — awaiting review
**Source of truth for scope and methods:** [design spec](design/2026-10-07-paywall-backlash-design.md). This plan covers execution only: work breakdown, sequencing, acceptance criteria, and risk tracking.

## 1. Delivery overview

| Item | Value |
|---|---|
| Capacity | ~5–8 hrs/week, 4–6 weeks (≈ 30–45 hrs total) |
| Planned scope | Weeks 1–5; Week 6 is buffer |
| Tracking | One GitHub Issue per task, one Milestone per week |
| Branching | `main` holds reviewed, stable work. `develop` is the integration branch for code. Each code issue gets a feature branch off `develop` and a PR back into `develop`. `develop` merges into `main` at the end of each milestone. Documentation-only changes may be committed directly to `main`. |
| Labels | `collect`, `clean`, `analysis`, `docs`, `infra`, `risk`, plus `RQ1`–`RQ4` |

## 2. Stages at a glance

The project runs in seven stages. Work on one stage at a time, in order. Each stage has a single goal, a short list of actions, and an explicit condition for moving on.

| Stage | Name | Goal | Week | Status |
|---|---|---|---|---|
| 0 | Foundation | Plan, spec, and working agreements in place | Done | Done |
| 1 | Setup | Repository scaffold and CI running | 1 | In progress |
| 2 | Event research | A cited event timeline and a validated control app | 1 | Not started |
| 3 | Data collection and cleaning | A clean, anonymized review dataset | 2 | Not started |
| 4 | Analysis | Answers to RQ1, RQ2, and RQ3 | 3–4 | Not started |
| 5 | Synthesis | Recommendations (RQ4), README, final report | 5 | Not started |
| 6 | Buffer and release | Catch-up, final checks, optional automation | 6 | Not started |

Status values are `Not started`, `In progress`, and `Done`. A stage moves to `In progress` when its first issue is opened and to `Done` when its exit condition is met. Claude updates this table at the start and end of each stage; the log below records each change.

### Stage 1 — Setup

- **Goal:** a repository where code can be written, tested, and checked automatically.
- **Do:** create the folder layout, `.gitignore`, `requirements.txt`, and the CI workflow (issues 1–2). Create the `develop` branch.
- **Done when:** a test pull request into `develop` shows a passing CI check.
- **Next:** Stage 2.

### Stage 2 — Event research

- **Goal:** know exactly which pricing and paywall changes happened, and when, with evidence.
- **Do:** research each app's events and record them in `data/events.csv` with a source URL (issue 3); confirm Nike Run Club had no change in the window (issue 4); count available Google Play reviews around each event (issue 5); draft the data dictionary (issue 6).
- **Why it matters:** every later result depends on these dates. A wrong date invalidates the analysis, so this stage is deliberately slow and manual.
- **Done when:** every event row has a source, the control is validated, and each event is marked keep, downgrade, or drop.
- **Next:** Stage 3.

### Stage 3 — Data collection and cleaning

- **Goal:** a trustworthy dataset that anyone can rebuild from the repository.
- **Do:** write the scrapers (issues 7–8), the cleaning pipeline with tests (issue 9), the Garmin and Trends pulls (issues 10–11), one command that rebuilds everything (issue 12), and the exploratory notebook (issue 13).
- **Done when:** the cleaned dataset contains no reviewer identifiers, tests pass, and the exploratory charts show enough reviews around each kept event.
- **Next:** Stage 4.

### Stage 4 — Analysis

- **Goal:** answer the research questions with evidence.
- **Do, in order:** RQ1 event study and difference-in-differences (issues 14–17), then the keyword tagger, hand-labeling, and topic model for RQ2 (issues 18–21), then the Garmin and Trends comparison for RQ3 (issue 22).
- **Done when:** each notebook runs from start to finish and reports validation metrics, robustness checks, and null results where they occur.
- **Next:** Stage 5.

### Stage 5 — Synthesis

- **Goal:** turn the findings into something a reader can use in under a minute.
- **Do:** build the event comparison table and recommendations (issues 23–24), then the methodology and limitations document, README, and final report (issues 25–27).
- **Done when:** every success criterion in §7 is met.
- **Next:** Stage 6.

### Stage 6 — Buffer and release

- **Goal:** finish cleanly.
- **Do:** close slipped issues, re-run the full pipeline from a clean clone, and tag a release. Add the monthly GitHub Action only if time remains.
- **Done when:** the repository reproduces from a fresh clone and `main` is green.

### Status log

| Date | Stage | Change |
|---|---|---|
| 2026-10-07 | 0 | Done — design spec, project plan, and working agreements on `main`; `develop` branch created |
| 2026-10-07 | 1 | In progress — scaffold and CI on `feature/1-repo-scaffold-ci`; PR into `develop` pending |

## 3. Critical path

```
Repo + CI ─┐
           ├─► events.csv ─► feasibility check ─► scrapers ─► cleaning ─► EDA
NRC check ─┘                                                      │
                                                                  ├─► RQ1 event study / DiD ─┐
                                                                  ├─► RQ2 tagger / topics ───┼─► RQ4 ─► README + report
                                  Garmin 10-Q/K + Trends ─────────┴─► RQ3 ──────────────────┘
```

- `events.csv` gates everything: event windows, the control-app check, and the feasibility check all depend on it.
- The feasibility check (Google Play history depth per event) decides which events enter RQ1 and must finish before full collection.
- Garmin financials and Google Trends collection are independent of review cleaning and can run in parallel during Week 2.
- RQ4 depends on effect sizes (RQ1) and complaint topics (RQ2); RQ3 is descriptive and does not block it.

## 4. Milestones and issues

Estimates are in hours. "AC" is the acceptance criteria for closing the issue.

### Week 1 — Setup and event research (≈ 7 hrs)

| # | Issue | Est. | AC |
|---|---|---|---|
| 1 | Repo scaffold: layout, `.gitignore` (`data/raw/`), LICENSE, `requirements.txt` | 1 | Directories match the spec; `data/raw/` ignored; dependencies pinned |
| 2 | CI: ruff + pytest on every PR | 1 | Workflow runs on PR; passes on an empty test suite |
| 3 | Research and cite event timeline (`data/events.csv`) | 3 | Every row has date, type, description, and source URL; no inferred dates; Wayback links where the original is gone |
| 4 | Verify Nike Run Club had no paywall or pricing change in the study window | 0.5 | Result documented; alternative control named if NRC fails |
| 5 | Feasibility check: Google Play review depth around each event | 1.5 | Table of review counts per app per ±8-week window; each event marked keep / downgrade / drop |
| 6 | Data dictionary stub for `events.csv` and the cleaned review schema | 0.5 | Column names, types, and constraints agreed before cleaning is written |

**Exit criteria:** `events.csv` cited and reviewed; control validated; event list finalized from the feasibility results.

### Week 2 — Collection and cleaning (≈ 8 hrs)

| # | Issue | Est. | AC |
|---|---|---|---|
| 7 | Google Play scraper (`src/collect/`) | 1.5 | Throttled, cached raw pulls, resumable; one file per app |
| 8 | App Store RSS scraper | 1 | Pulls available reviews per country; limitation documented |
| 9 | Cleaning pipeline (`src/clean/`): dedupe, English filter, date normalization, app/version tagging, drop reviewer names/IDs | 2 | No PII columns in output; unit tests for each step |
| 10 | Garmin Fitness-segment revenue from SEC EDGAR | 1 | Quarterly series with filing citations |
| 11 | Google Trends pull (`pytrends`, manual CSV fallback) | 0.5 | Weekly interest per app, cached |
| 12 | Single entry point (`make data`) rebuilds raw → processed | 0.5 | Clean-clone run succeeds |
| 13 | EDA notebook `01_eda` | 1.5 | Weekly rating and volume per app with event markers |

**Exit criteria:** processed dataset committed as aggregates; cleaning tests green; EDA shows usable volume per kept event.

### Week 3 — RQ1: did backlash happen? (≈ 7 hrs)

| # | Issue | Est. | AC |
|---|---|---|---|
| 14 | Window logic with unit tests | 1 | Event windows (±4, ±8, ±12 weeks) correct at edges and for overlapping events |
| 15 | Event study: mean stars, share of 1★, share of price mentions | 2 | One chart per event with confidence intervals |
| 16 | DiD vs. Nike Run Club (statsmodels OLS, app and time fixed effects, robust SEs) | 2 | Estimates tabulated per event; pre-trend check reported |
| 17 | Robustness: alternate windows, placebo dates, confounder annotation | 2 | Results table; confounding releases or outages noted per event |

**Exit criteria:** `02_event_study` notebook runs end to end; each event has an effect estimate or a documented reason for exclusion. A null result is reported as such.

### Week 4 — RQ2 and RQ3 (≈ 8 hrs)

| # | Issue | Est. | AC |
|---|---|---|---|
| 18 | Keyword tagger for price and paywall mentions, with tests | 1.5 | Dictionary documented; tests cover positives, negatives, and edge cases |
| 19 | Hand-label ~200 reviews | 1.5 | Labeled sample stored without identifiers; labeling rules written down |
| 20 | BERTopic model, CPU-only, stratified sampling if slow | 2 | Topics labeled; topic share shown around events |
| 21 | Validation: precision and recall for tagger and topic labels; sentiment cross-check | 1 | Metrics reported in the notebook and methodology doc |
| 22 | RQ3: Garmin revenue vs. review signals and Trends | 2 | Correlations with caveats (n=1 company, ~20 quarters); no causal language |

**Exit criteria:** `03_topics` and `04_business` run end to end; validation metrics stated.

### Week 5 — RQ4 and write-up (≈ 7 hrs)

| # | Issue | Est. | AC |
|---|---|---|---|
| 23 | Event comparison table: gated feature, price change, communication approach, RQ1 effect, dominant complaints | 2 | Every cell traceable to a source or an estimate |
| 24 | 3–5 recommendations | 1.5 | Each tied to a specific chart or estimate |
| 25 | Methodology and limitations document | 1 | Covers iOS history depth, n=1 financials, scraping gaps, descriptive RQ3 |
| 26 | README: headline finding and 2–3 charts, reproduce instructions | 1.5 | Headline visible within 30 seconds; reproduces from a clean clone |
| 27 | Final report | 1 | Reads as professional research; quotes short and anonymized |

**Exit criteria:** all success criteria in §6 met.

### Week 6 — Buffer

Catch-up on slipped issues first. If the schedule holds, the optional item is the monthly GitHub Action that re-scrapes reviews and refreshes the summary charts.

## 5. Data contracts

Defined in issue 6 and finalized in the data dictionary; stages depend on these, not on each other's code.

- **`data/events.csv`:** `app`, `event_date`, `event_type`, `description`, `source_url`, `confidence`, `notes`. `source_url` is required and non-null.
- **Cleaned reviews (`data/processed/`):** `app`, `platform`, `review_date`, `stars`, `text`, `app_version`, `language`. No names, user IDs, or review IDs that could identify a reviewer.
- **Weekly aggregates:** `app`, `week`, `n_reviews`, `mean_stars`, `share_1star`, `share_price_mention`.

## 6. Risk register

| Risk | Likelihood | Impact | Trigger | Mitigation | Owner issue |
|---|---|---|---|---|---|
| Thin Google Play history for an event | Medium | High | Fewer reviews per window than the volume threshold set in issue 5 | Drop or downgrade the event; document | 5 |
| Scraper blocked or rate-limited | Medium | Medium | HTTP errors, empty pulls | Throttle, cache, smaller samples | 7 |
| Confounding releases or outages near events | High | Medium | Release notes or status pages within a window | Annotate; placebo and window robustness | 17 |
| Control app also changed | Low | High | Any NRC pricing or paywall change in the window | Choose an alternative control in Week 1 | 4 |
| Too few treated events after feasibility filtering | Medium | High | Fewer than three events kept | Fall back to descriptive event studies; state the lack of DiD power | 5 |
| BERTopic too slow on CPU | Medium | Low | Fit time exceeds budget | Stratified sampling per app and period | 20 |
| Pytrends rate limit | Medium | Low | 429 responses | Manual CSV export | 11 |
| Scope slips past Week 5 | Medium | Medium | Any milestone exits late | Use the Week 6 buffer; cut the GitHub Action first | — |

## 7. Definition of done

**Per issue:** merged by PR into `develop`, CI green, tests included for any logic, no raw data or reviewer identifiers committed, documentation updated.

**Per research question:**

| RQ | Deliverable | Done when |
|---|---|---|
| RQ1 | `02_event_study` notebook, figures | Estimates and robustness for each kept event; null results reported |
| RQ2 | `03_topics` notebook, figures | Tagger and topic validation metrics reported |
| RQ3 | `04_business` notebook | Correlations stated with caveats; descriptive framing only |
| RQ4 | `05_recommendations` notebook, report section | 3–5 recommendations, each tied to evidence |

**Project:** the success criteria in the design spec §9.

## 8. Change control

Scope changes (dropping an event, replacing the control, cutting a method) are recorded in a decision log at the bottom of this file with the date, reason, and affected issues. The design spec is updated only when a research question or method changes.

## 9. Decision log

| Date | Decision | Reason | Affected |
|---|---|---|---|
| 2026-10-07 | Add this plan alongside the design spec rather than a PRD | Research project; the design spec already covers scope and methods | — |
| 2026-10-07 | Adopt a `develop` integration branch; allow docs-only commits directly to `main` | Separates in-progress code from stable work while keeping documentation changes lightweight | `CLAUDE.md`, §1 |
