"""
Update script for the Operator Metrics Dashboard.

This script computes aggregated metrics from ``applications.json`` and
appends them to ``metrics_history.json`` with a timestamp.  It is
intended to be run on a schedule (e.g. via GitHub Actions) to keep
your dashboard's metric history current.  The Streamlit app reads
``metrics_history.json`` to display deltas between runs.

Usage:
    python update_data.py

Author: Alexander Lee Minnick
"""

import json
import pathlib
from datetime import datetime

import pandas as pd

from app import load_applications, compute_metrics


def main() -> None:
    base_dir = pathlib.Path(__file__).parent
    apps_path = base_dir / 'applications.json'
    history_path = base_dir / 'metrics_history.json'

    # Compute current metrics
    df = load_applications(apps_path)
    current_metrics = compute_metrics(df)
    timestamp = datetime.now().isoformat(timespec='seconds')

    # Load existing history
    if history_path.exists():
        with history_path.open() as f:
            history = json.load(f)
    else:
        history = []

    # Append new snapshot
    history.append({'timestamp': timestamp, 'metrics': current_metrics})

    # Save back to file
    with history_path.open('w') as f:
        json.dump(history, f, indent=2)

    print(f"Appended metrics snapshot at {timestamp} to {history_path}")


if __name__ == '__main__':
    main()