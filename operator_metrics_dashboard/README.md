# Operator Metrics Dashboard

[![Build Status](https://img.shields.io/github/actions/workflow/status/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY/update.yml?branch=main)](https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY/actions)

## 📈 Proof‑of‑ROI Quick Stats

To demonstrate the operator mindset, the dashboard now includes a **proof‑of‑ROI block**.  It aggregates the measurable impact of your job search automation pipeline:

- **Hours saved by automation:** `{{ insert your total hours saved here }}` – the sum of `hours_saved_by_automation` across all applications.
- **Interview conversion rate:** `{{ insert your conversion rate here }}` – calculated as interviews / applications.
- **Offer rate:** `{{ insert your offer rate here }}` – calculated as offers / applications.
- **Time to decision:** `{{ insert average days to decision here }}` – average number of days between application and offer/interview.

These values are computed in `update_data.py` and surfaced on the dashboard so that recruiters and operators can instantly see the business impact of your system.  See the generated `metrics_history.json` and the **Total ROI** section of your meta‑portfolio for aggregated statistics across all projects.

The **Operator Metrics Dashboard** is a living proof‑of‑concept that
quantifies the impact of my job search automation pipeline.  Built with
Streamlit and powered by a simple JSON data store, this dashboard demonstrates
my ability to instrument a process, compute key performance indicators, and
present actionable insights in a clear, branded interface.

## 📊 What It Does

- **Ingests job search data:** Reads from `applications.json`, which contains a
  list of job applications with fields like company, position, status,
  whether a DM or follow‑up was sent, and estimated hours saved by
  automation.
- **Computes KPIs:** Calculates total applications, interviews,
  offers, direct messages sent, follow‑ups sent, conversion rates, and the
  total hours saved.
- **Visualizes results:** Renders interactive charts (e.g. outcome
  distribution and applications over time) alongside concise KPI cards.
- **Tracks history:** Includes an `update_data.py` script that records
  snapshots of your metrics over time into `metrics_history.json`.  The
  dashboard uses this history to display deltas between runs, proving your
  pipeline’s compounding improvements.
- **Automates updates:** A sample GitHub Action (`.github/workflows/update.yml`)
  runs `update_data.py` on a schedule, commits the updated history, and keeps
  your dashboard current without manual intervention.

## 🚀 Why It Matters

Your job search isn’t just about sending resumes—it’s an automation pipeline
designed to maximize leverage.  This dashboard:

1. **Provides transparency:** Recruiters and founders can immediately see how
   many applications you send, your interview and offer rates, and how
   automation saves you time.
2. **Demonstrates instrumentation:** Shows that you don’t just build systems; you
   measure their performance and iterate based on data.
3. **Showcases end‑to‑end thinking:** Combines data ingestion, processing, UI,
   and CI/CD into a cohesive project.  This is what operating like a founder
   looks like.

## 🛠️ Getting Started

1. Clone the repository or copy the `operator_metrics_dashboard` folder.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Run the dashboard locally:

   ```bash
   streamlit run app.py
   ```
4. Optional: edit `applications.json` with your own job search data.  Each
   record should follow this schema:

   ```json
   {
     "company": "Acme Corp",
     "position": "AI Prompt Engineer",
     "date_applied": "2025-07-20",
     "dm_sent": true,
     "follow_up_sent": false,
     "status": "interview",
     "hours_saved_by_automation": 2.5
   }
   ```
5. To record historical metrics, run:

   ```bash
   python update_data.py
   ```

   This will append a snapshot to `metrics_history.json`.

## 🤖 Continuous Updates via GitHub Actions

The included workflow file (`.github/workflows/update.yml`) demonstrates how
to schedule a daily update.  The action checks out the repository,
installs Python, runs `update_data.py`, and commits any changes to
`metrics_history.json`.  This pattern can be adapted for weekly updates or
other schedules.

## 🧠 How This Proves My Operator Value

This project isn’t just a dashboard—it’s a meta demonstration of how I
approach automation.  By measuring the effectiveness of my job search
pipeline, I show that:

- I close the loop between execution and feedback, turning every action into
  data that drives the next improvement.
- I build systems that can be run, monitored, and scaled by others.  A
  hiring manager could clone this repo and immediately see my metrics in
  action.
- I think like a founder: identifying key metrics, automating manual work,
  and using data to compound my advantages.

## 🔐 Security & Privacy

This project does **not** send any personal data to third‑party services.  All job application data stays in the local repository (or your hosting provider if deployed).  API keys should never be hardcoded—store them in environment variables or GitHub Secrets.  You can reset or delete your data at any time by clearing `applications.json` and `metrics_history.json`.

## 🛠️ Configuration

Behavior of the dashboard can be tuned without touching the code.  The included `config.yaml` exposes several options:

```yaml
model: gpt-3.5-turbo      # default model used for any AI tasks in future extensions
temperature: 0.2          # controls creativity of AI responses
update_schedule: "daily"  # how often the GitHub Action runs the update script
metrics_history_enabled: true  # set to false to disable history tracking
dashboard_title: "Operator Metrics Dashboard"
```

Feel free to adjust these values to fit your preferences or hosting constraints.  For example, if you only want to run updates once per week, set `update_schedule` to `"weekly"` and adjust the cron in `.github/workflows/update.yml`.

## 🧪 Unit Tests & Continuous Integration

A `tests/` folder has been added with simple unit tests that verify the integrity of your data and scripts.  Run `pytest` or `python -m unittest` from the root of this folder to execute the tests.  The included GitHub Action uses these tests to display a “build passing” badge at the top of this README.

## 📁 Project Structure

```
operator_metrics_dashboard/
│
├── app.py                  # Streamlit dashboard application
├── update_data.py          # Script to compute and append metrics history
├── applications.json       # Sample job search data
├── requirements.txt        # Python dependencies
├── metrics_history.json    # Generated by update_data.py (ignored if empty)
└── .github/workflows/
    └── update.yml          # GitHub Action for scheduled updates
```

## 📦 Integration with Meta‑Portfolio

When added to my meta‑tier portfolio, this folder serves as the embodiment
of the “Live Dashboards” recommendation.  The `meta-summary.md` file
explains how the dashboard demonstrates compounding leverage, operator
mindset, and transparency.  Link to this dashboard from your portfolio
site and GitHub README to provide a tangible, live artifact of your
automation philosophy.