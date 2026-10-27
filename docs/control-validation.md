# Control Validation — Nike Run Club

**Issue:** 4 (project plan issue 4) · **Checked:** 2026-10-22 · **Result:** passes provisionally; two verification steps remain.

## Question

Did Nike Run Club (NRC) introduce a paywall or pricing change at any point in the study window? The design spec treats NRC as a free app with no paywall change; a change would invalidate it as the difference-in-differences control.

## Evidence

| Date | Source | Observation |
|---|---|---|
| 2022-02-06 | [Wayback copy of Nike NZ NRC page](http://web.archive.org/web/20220206134103/https://www.nike.com/nz/nrc-app) | FAQ: "The Nike Run Club app is free to download with no in-app purchases." |
| 2023-01-01 | [Wayback copy](http://web.archive.org/web/20230101020732/https://www.nike.com/nz/nrc-app) | Same statement. |
| 2024-01-01 | [Wayback copy](http://web.archive.org/web/20240101090107/https://www.nike.com/nz/nrc-app) | Same statement. |
| 2025-01-22 | [Wayback copy](http://web.archive.org/web/20250122224348/https://www.nike.com/nz/nrc-app) | Same statement. |
| 2026-01-03 | [Wayback copy](http://web.archive.org/web/20260103111700/https://www.nike.com/nz/nrc-app) | Same statement. |
| 2026-10-22 | [Nike NZ NRC page](https://www.nike.com/nz/nrc-app) | Same statement (live page). |

A web search for NRC paywall, subscription, or pricing changes returned no report of any change; the only hits were comparison blogs describing the app as free.

## Limitations

- Snapshots are roughly annual samples, so a short-lived change between them would not appear.
- The 2021 snapshot of the NZ page lacks the FAQ, and the US page snapshots do not carry the cost statement. Coverage of 2020–2021 is therefore weaker than 2022–2026.
- An absence of news coverage is not proof of no change.

## Review-history coverage (issue 5)

The Google Play history reachable for Nike Run Club starts on 2020-04-12. Its 8-week pre-window for the Strava event on 2020-03-12 therefore has no reviews, so that event cannot be used in the difference-in-differences. For every other event the control has 333 to 3,020 reviews in each ±8-week window.

## Remaining checks

1. Read the NRC App Store and Google Play listings for in-app purchases and release notes across the study window (the store changelogs are the closest thing to a continuous record).
2. Decide the study window from the feasibility check (issue 5), then re-verify the NRC coverage for that window specifically.

## Decision

NRC remains the control. No alternative control is named at this time. Revisit if either remaining check finds a paywall, a subscription tier, or an in-app purchase.
