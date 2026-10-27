"""Feasibility check: Google Play review depth around each event (issue 5).

Pulls review dates and star ratings (no text, names, or IDs) newest-first for
each app until the oldest date needed is reached, caches them under
``data/raw/feasibility/``, then counts reviews in the +/-8 week window around
every event in ``data/events.csv``.
"""

import csv
import json
import time
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
from google_play_scraper import Sort, reviews

ROOT = Path(__file__).resolve().parents[2]
EVENTS = ROOT / "data" / "events.csv"
CACHE = ROOT / "data" / "raw" / "feasibility"
OUT = ROOT / "data" / "processed" / "feasibility.csv"

PACKAGES = {
    "Strava": "com.strava",
    "Garmin Connect": "com.garmin.android.apps.connectmobile",
    "AllTrails": "com.alltrails.alltrails",
    "Surfline": "com.surfline.android",
    "Nike Run Club": "com.nike.plusgps",
}
WINDOW_WEEKS = 8
BATCH = 200
THROTTLE_S = 1.0
# Minimum reviews on the smaller side (pre or post) to keep or downgrade an event.
KEEP_MIN = 100
DOWNGRADE_MIN = 30


def pull(app: str, oldest: date) -> list[dict]:
    """Page newest-first until reviews older than ``oldest`` are reached."""
    path = CACHE / f"{app.lower().replace(' ', '_')}.jsonl"
    if path.exists():
        with path.open(encoding="utf-8") as f:
            cached = [json.loads(line) for line in f]
        if cached and min(r["date"] for r in cached) <= oldest.isoformat():
            return cached

    CACHE.mkdir(parents=True, exist_ok=True)
    rows, token = [], None
    while True:
        batch, token = reviews(
            PACKAGES[app],
            lang="en",
            country="us",
            sort=Sort.NEWEST,
            count=BATCH,
            continuation_token=token,
        )
        rows += [{"date": r["at"].date().isoformat(), "stars": r["score"]} for r in batch]
        if not batch or token is None or rows[-1]["date"] < oldest.isoformat():
            break
        time.sleep(THROTTLE_S)

    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    return rows


def classify(pre: int, post: int) -> str:
    low = min(pre, post)
    if low >= KEEP_MIN:
        return "keep"
    if low >= DOWNGRADE_MIN:
        return "downgrade"
    return "drop"


def main() -> None:
    with EVENTS.open(encoding="utf-8", newline="") as f:
        events = list(csv.DictReader(f))
    delta = timedelta(weeks=WINDOW_WEEKS)

    oldest = {}
    for e in events:
        d = datetime.strptime(e["event_date"], "%Y-%m-%d").date() - delta
        oldest[e["app"]] = min(oldest.get(e["app"], d), d)
    # Control app is needed over the whole treated span.
    oldest["Nike Run Club"] = min(oldest.values())

    dates = {}
    for app, since in oldest.items():
        data = pull(app, since)
        dates[app] = pd.to_datetime(pd.Series([r["date"] for r in data]))
        print(f"{app}: {len(data)} reviews, oldest {dates[app].min().date()}", flush=True)

    out = []
    for e in events:
        d = pd.Timestamp(e["event_date"])
        s = dates[e["app"]]
        pre = int(((s >= d - delta) & (s < d)).sum())
        post = int(((s >= d) & (s < d + delta)).sum())
        covered = s.min() <= d - delta
        out.append(
            {
                "app": e["app"],
                "event_date": e["event_date"],
                "event_type": e["event_type"],
                "reviews_pre_8w": pre,
                "reviews_post_8w": post,
                "history_reaches_window": covered,
                "decision": classify(pre, post) if covered else "drop",
            }
        )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(out).to_csv(OUT, index=False)
    print(pd.DataFrame(out).to_string(index=False))


if __name__ == "__main__":
    main()
