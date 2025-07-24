"""
Streamlit application for the Operator Metrics Dashboard.

This dashboard ingests your job search tracker data, computes key performance
indicators (KPIs), and displays them in an interactive web app.  It is
designed to showcase your ability to instrument an automation pipeline and
communicate results clearly to recruiters, hiring managers, and founders.

The app reads from ``applications.json`` for raw application data and
``metrics_history.json`` for the historical metrics produced by the
``update_data.py`` script.  You can run the app locally by executing

    streamlit run app.py

in the ``operator_metrics_dashboard`` directory.  The dashboard includes
aggregate statistics, conversion rates, and charts that update whenever
``update_data.py`` is run (either manually or via a GitHub Action).

Author: Alexander Lee Minnick
"""

import json
import pathlib
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st


def load_applications(path: pathlib.Path) -> pd.DataFrame:
    """Load applications from a JSON file into a DataFrame.

    Each record should include the following keys:

    - company: string
    - position: string
    - date_applied: ISO date string (YYYY-MM-DD)
    - dm_sent: boolean (did you send a direct message?)
    - follow_up_sent: boolean (did you send a follow-up?)
    - status: one of {"applied", "interview", "offer", "rejected"}
    - hours_saved_by_automation: number (estimate of time saved)

    Args:
        path: Path to the JSON file.

    Returns:
        DataFrame with appropriate columns and parsed dates.
    """
    with path.open() as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    # parse dates
    df['date_applied'] = pd.to_datetime(df['date_applied'])
    return df


def compute_metrics(df: pd.DataFrame) -> dict:
    """Compute aggregate metrics from the applications DataFrame.

    Args:
        df: DataFrame containing applications.

    Returns:
        Dictionary of computed metrics.
    """
    metrics = {}
    metrics['total_applications'] = len(df)
    metrics['interviews'] = (df['status'] == 'interview').sum()
    metrics['offers'] = (df['status'] == 'offer').sum()
    metrics['dms_sent'] = df['dm_sent'].astype(int).sum()
    metrics['follow_ups_sent'] = df['follow_up_sent'].astype(int).sum()
    # Avoid division by zero
    metrics['interview_rate'] = (
        metrics['interviews'] / metrics['total_applications'] * 100 if metrics['total_applications'] else 0
    )
    metrics['offer_rate'] = (
        metrics['offers'] / metrics['total_applications'] * 100 if metrics['total_applications'] else 0
    )
    metrics['offer_to_interview_rate'] = (
        metrics['offers'] / metrics['interviews'] * 100 if metrics['interviews'] else 0
    )
    metrics['hours_saved'] = df['hours_saved_by_automation'].sum()
    return metrics


def load_metrics_history(path: pathlib.Path) -> list:
    """Load metrics history if available.

    The history is a list of entries with ``timestamp`` and computed metrics.

    Args:
        path: Path to the metrics_history JSON file.

    Returns:
        List of history entries (may be empty).
    """
    if path.exists():
        with path.open() as f:
            return json.load(f)
    return []


def compute_deltas(current: dict, previous: dict) -> dict:
    """Compute deltas between two metric snapshots.

    Args:
        current: Current metrics dictionary.
        previous: Previous metrics dictionary.

    Returns:
        Dictionary of deltas (current - previous) for each metric.
    """
    deltas = {}
    for key in current.keys():
        if key in previous and isinstance(current[key], (int, float)):
            deltas[key] = current[key] - previous[key]
    return deltas


def main() -> None:
    st.set_page_config(page_title="Operator Metrics Dashboard", layout="wide")

    data_path = pathlib.Path(__file__).parent / 'applications.json'
    history_path = pathlib.Path(__file__).parent / 'metrics_history.json'

    # Load data
    df = load_applications(data_path)
    metrics = compute_metrics(df)
    history = load_metrics_history(history_path)

    # Compute deltas (difference from previous run)
    deltas = {}
    if history:
        previous_metrics = history[-1].get('metrics', {})
        deltas = compute_deltas(metrics, previous_metrics)

    last_updated = (
        history[-1]['timestamp'] if history else datetime.now().isoformat(timespec='seconds')
    )

    # Branding: display logo and title
    logo_path = pathlib.Path(__file__).parent.parent / '29E28EED-2FC5-4739-8250-7D540CDB54DF.jpeg'
    if logo_path.exists():
        st.image(str(logo_path), width=200)
    st.title("Operator Metrics Dashboard")
    st.markdown(
        "This dashboard quantifies the impact of my job search automation pipeline. "
        "It surfaces key performance metrics, conversion rates, and estimated hours saved, "
        "demonstrating my operator mindset and data instrumentation skills."
    )
    st.write(f"**Last updated:** {last_updated}")

    # Layout: two columns for KPI cards
    col1, col2, col3 = st.columns(3)
    col1.metric(
        label="Applications Sent",
        value=metrics['total_applications'],
        delta=deltas.get('total_applications', 0),
    )
    col1.metric(
        label="Interviews",
        value=metrics['interviews'],
        delta=deltas.get('interviews', 0),
    )
    col1.metric(
        label="Offers",
        value=metrics['offers'],
        delta=deltas.get('offers', 0),
    )

    col2.metric(
        label="DMs Sent",
        value=metrics['dms_sent'],
        delta=deltas.get('dms_sent', 0),
    )
    col2.metric(
        label="Follow‑ups Sent",
        value=metrics['follow_ups_sent'],
        delta=deltas.get('follow_ups_sent', 0),
    )
    col2.metric(
        label="Hours Saved by Automation",
        value=f"{metrics['hours_saved']:.1f}",
        delta=deltas.get('hours_saved', 0),
    )

    col3.metric(
        label="Interview Rate",
        value=f"{metrics['interview_rate']:.1f}%",
        delta=f"{deltas.get('interview_rate', 0):.1f}%" if 'interview_rate' in deltas else "0%",
    )
    col3.metric(
        label="Offer Rate",
        value=f"{metrics['offer_rate']:.1f}%",
        delta=f"{deltas.get('offer_rate', 0):.1f}%" if 'offer_rate' in deltas else "0%",
    )
    col3.metric(
        label="Offer/Interview Rate",
        value=f"{metrics['offer_to_interview_rate']:.1f}%",
        delta=f"{deltas.get('offer_to_interview_rate', 0):.1f}%" if 'offer_to_interview_rate' in deltas else "0%",
    )

    st.markdown("---")

    # Status distribution chart
    status_counts = df['status'].value_counts().reset_index()
    status_counts.columns = ['status', 'count']
    fig_status = px.pie(
        status_counts,
        names='status',
        values='count',
        title='Application Outcome Distribution',
        color_discrete_sequence=px.colors.sequential.Blues,
    )
    st.plotly_chart(fig_status, use_container_width=True)

    # Applications over time
    df_daily = df.groupby(df['date_applied'].dt.date).size().reset_index(name='applications')
    fig_timeline = px.bar(
        df_daily,
        x='date_applied',
        y='applications',
        title='Applications Over Time',
        labels={'date_applied': 'Date Applied', 'applications': 'Number of Applications'},
        color_discrete_sequence=['#007ACC'],
    )
    st.plotly_chart(fig_timeline, use_container_width=True)

    # Raw data table
    st.markdown("## 📄 Raw Application Data")
    st.dataframe(df.sort_values('date_applied', ascending=False), use_container_width=True)

    st.markdown(
        "### 📘 About this Dashboard\n"
        "This dashboard is part of my meta‑tier portfolio.  It serves as live proof of how I "
        "instrument my own job search pipeline, quantify its impact, and continuously improve the process. "
        "The codebase includes automated data refresh via GitHub Actions and can be repurposed for other "
        "operators looking to track their own metrics."
    )


if __name__ == "__main__":
    main()