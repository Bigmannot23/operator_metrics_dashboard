# Operator Guide – Operator Metrics Dashboard

This operator‑oriented guide explains how to set up, configure, run, extend, and troubleshoot the **Operator Metrics Dashboard**.  It is written for non‑developers who want to reuse or adapt the system without digging into the code.

## 🧰 Setup

1. **Clone or copy the repository.**  If you are using this dashboard in your own GitHub repo, copy the entire `operator_metrics_dashboard/` folder into your repository.
2. **Install dependencies.**  From the `operator_metrics_dashboard/` directory run:

   ```bash
   pip install -r requirements.txt
   ```

3. **Add your job‑search data.**  Open `applications.json` and replace the sample entries with your own job applications.  Each object should include the following fields:

   - `company` – the organization you applied to.
   - `position` – the role applied for.
   - `date_applied` – an ISO date (`YYYY‑MM‑DD`).
   - `dm_sent` – `true` if you sent a direct message on LinkedIn or elsewhere.
   - `follow_up_sent` – `true` if you sent a follow‑up message.
   - `status` – one of `applied`, `interview`, `offer`, or `rejected`.
   - `hours_saved_by_automation` – estimate of time saved by your automation pipeline (in hours).

4. **Review the configuration.**  Open `config.yaml` to see tunable parameters such as `update_schedule`.  Adjust these values if you plan to run the update script on a different cadence or change the default model for future AI tasks.

5. **Run the dashboard locally.**  Execute:

   ```bash
   streamlit run app.py
   ```

   The dashboard will launch in your browser.  It reads from your `applications.json` and, if enabled, displays deltas from previous runs using `metrics_history.json`.

6. **Record a metrics snapshot.**  To compute and append a snapshot of your current metrics history run:

   ```bash
   python update_data.py
   ```

   This will create or update `metrics_history.json` and ensures your dashboard shows trends over time.

7. **Enable continuous updates (optional).**  Copy `.github/workflows/update.yml` into your repository and push it to GitHub.  This workflow installs dependencies, runs `update_data.py` on a schedule, and commits any changes back to the repo.  You can modify the cron schedule in `update.yml` to fit your needs.

## ⚙️ Configuration Options

The dashboard reads options from `config.yaml`.  The following keys are available:

| Key | Description |
| --- | --- |
| `model` | Default language model used by any AI features you add (e.g. `gpt-3.5-turbo` or `gpt-4`). |
| `temperature` | Sampling temperature for AI outputs.  Lower values (e.g. 0.0–0.3) give more deterministic answers. |
| `update_schedule` | String such as `"daily"` or `"weekly"` used by the GitHub Action; adjust the cron in `.github/workflows/update.yml` accordingly. |
| `metrics_history_enabled` | If `false`, the update script will skip writing to `metrics_history.json`. |
| `dashboard_title` | Customize the title shown at the top of the Streamlit app. |

You can extend the config with your own fields and read them in `app.py` or `update_data.py`.  Avoid storing secrets (e.g. API keys) in this file—use environment variables or repository secrets instead.

## ▶️ How to Run & Test

To run the dashboard and test that everything is working:

1. Run `streamlit run app.py` to launch the UI.  Verify that charts and KPIs load correctly.
2. Run `python update_data.py` and check that `metrics_history.json` is created or updated.
3. Execute the unit tests with:

   ```bash
   python -m unittest discover tests
   ```

   All tests should pass.  The tests check that your data files are valid and that the update script runs without errors.

## 🔧 How to Extend or Fork

- **Add new KPIs:** Modify `update_data.py` to compute additional metrics (e.g. time‑to‑first‑interview, DM response rate) and add corresponding charts in `app.py`.
- **Connect external data sources:** If your job‑search data lives in Google Sheets, Airtable, or another API, fetch it in `update_data.py` and write it to `applications.json` before computing metrics.
- **Customize the UI:** Use Streamlit’s components to tweak layouts, colors, or add new interactive filters.  Refer to `branding/branding_guide.md` for color choices.
- **Repurpose the dashboard:** The architecture is generic—replace `applications.json` with any dataset of records containing timestamps and statuses to create dashboards for sales pipelines, hiring funnels, etc.

## 🛠️ Troubleshooting Tips

| Issue | Solution |
| --- | --- |
| **“ModuleNotFoundError” when running scripts** | Ensure you installed dependencies (`pip install -r requirements.txt`) in the same environment where you run the scripts. |
| **Streamlit app shows no data** | Check that `applications.json` contains valid JSON and at least one entry.  Validate the JSON format via [jsonlint.com](https://jsonlint.com) if unsure. |
| **Metrics history not updating** | Ensure `metrics_history_enabled` is set to `true` in `config.yaml` and that `python update_data.py` runs without errors. |
| **GitHub Action fails** | Make sure your repository contains the `.github/workflows/update.yml` file and that the Python version in the workflow matches your local environment.  You may need to add a `python-version` matrix or update dependencies. |
| **Cron schedule does not suit your needs** | Edit the `cron` expression in `.github/workflows/update.yml`.  For weekly runs at midnight on Sundays use `0 0 * * 0`. |

With this guide, any operator should be able to launch, iterate on, and audit the **Operator Metrics Dashboard** with minimal friction.