# Subscription Fatigue in Fitness Tech

An analysis of user backlash to paywall and pricing changes in fitness and outdoor apps, using app-store reviews, event studies, difference-in-differences, topic modeling, public company financials, and search interest.

**Status:** In progress. Setup is complete; event research is under way. No findings have been produced yet, and this README will be updated with the headline result and key charts when the analysis is finished.

## Research questions

1. **RQ1: Did backlash happen?** After each paywall or price event, did ratings and sentiment worsen relative to a control app?
2. **RQ2: What drove it?** Which complaint topics (price, gated features, bugs, data ownership) appear, and how do they shift around events?
3. **RQ3: Does it show up in the business?** Do review signals line up with Garmin's Fitness-segment revenue and with Google Trends interest? This question is descriptive only.
4. **RQ4: So what?** Which paywall strategies drew the least backlash? The project closes with three to five evidence-backed recommendations for product teams.

A null result (no measurable backlash) is a valid finding and will be reported as such.

## Scope

| App | Role |
|---|---|
| Strava | Treated |
| Garmin Connect | Treated |
| AllTrails | Treated |
| Surfline | Treated |
| Nike Run Club | Control |

Event dates are researched and cited in `data/events.csv`; every row carries a source URL. The control app is verified to have had no paywall or pricing change during the study window.

## Methods

- **Event study:** weekly mean rating, share of 1-star reviews, and share of price-mentioning reviews in windows around each event.
- **Difference-in-differences:** treated apps against the control, with app and time fixed effects and robust standard errors. Robustness checks use alternate window lengths, placebo dates, and annotation of confounding releases or outages.
- **Text analysis:** a unit-tested keyword dictionary for price and paywall mentions, and BERTopic for complaint topics. Both are validated against a hand-labeled sample of about 200 reviews.
- **Business context:** Garmin Fitness-segment revenue from SEC filings and Google Trends interest, compared descriptively.

The full design is in [docs/design](docs/design/2026-10-07-paywall-backlash-design.md), and the execution plan is in [docs/project-plan.md](docs/project-plan.md).

## Limitations

- App Store history is limited to roughly the 500 most recent reviews per country, so Google Play is the primary dataset.
- Garmin is the only company in scope with public financials, so RQ3 rests on one company and about 20 quarters of data.
- RQ3 is descriptive and makes no causal claims.
- Review volume around some events may be too thin to estimate effects; such events are downgraded or dropped, and the decision is documented.
- App-store reviewers are a self-selected sample of users.

## Data handling

Raw scraped data is stored in `data/raw/` and is never committed; scripts reproduce it. Reviewer names and IDs are removed during cleaning. Processed aggregates and the event timeline are committed. Quoted reviews are kept brief and anonymized. Review content belongs to the respective platforms and reviewers.

## Repository layout

```
docs/            design spec, project plan, methodology, data dictionary, final report
data/            events.csv (committed); raw/ (ignored); processed/
src/collect/     scrapers, one module per source
src/clean/       cleaning pipeline
notebooks/       one notebook per research question
reports/figures/ exported charts
tests/           unit tests
```

## Setup

Requires Python 3.12.

```
python -m venv .venv
.venv/Scripts/activate        # Windows; use .venv/bin/activate on macOS or Linux
pip install -r requirements.txt
ruff check . && ruff format --check .
pytest
```

A single command to rebuild the processed data from raw sources will be added in Stage 3.

## Workflow

Work is tracked with GitHub Issues grouped into weekly milestones. Each issue is built on a feature branch and merged into `develop` by pull request after automated checks (ruff and pytest) pass. `develop` is merged into `main` at the end of each milestone.

## License

Code is released under the MIT License. See [LICENSE](LICENSE).
