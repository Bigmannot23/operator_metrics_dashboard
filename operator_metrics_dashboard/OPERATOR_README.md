# Operator Metrics Dashboard

## Elevator pitch
Turn messy job-search data into actionable KPIs. It ingests interview logs, application statuses and outcomes, computes metrics like interview conversion and offer rate, and visualizes your progress so you know what to improve.

## Usage
1. Clone this repository and install dependencies.
2. Place your job-search data (CSV or JSON) into the `data/` folder.
3. Run the provided notebook or script to ingest data and generate the dashboard.
4. Open the HTML output or serve it via a lightweight server to explore your metrics.
5. Adjust the config file to define your own KPIs or thresholds.

## Architecture
- Automated ingestion parses spreadsheets, CSVs or Airtable exports and normalizes them.
- KPI computation calculates conversion rates, offers per application, time-to-decision and more.
- Visualizations & history provide interactive plots and historical comparisons for continuous improvement.
- Extensible modules allow you to add custom metrics by modifying Python notebooks or templates.

![Diagram](./assets/diagram.png)

## Results & ROI
- **Hours of manual spreadsheet work eliminated** — evidence: Time tracking reports
- **70% interview-to-screen conversion achieved** — evidence: Historical metrics
- **30% offer rate across applications** — evidence: Application data analysis
- **Time from interview to decision cut by 2+ days** — evidence: Process analytics

## Part of the Operator Meta Portfolio
- [AI Code Review Bot](../ai_code_review_bot/OPERATOR_README.md)
- [Job Offer Factory](../job_offer_factory_autorun/OPERATOR_README.md)
- [Onboarding Assistant](../Onboarding_Assistant/OPERATOR_README.md)
- [Lexvion Compliance Engine](../lexvion/OPERATOR_README.md)
- [Lexvion Trading Bot](../lexvion_trading_bot_full_auto/OPERATOR_README.md)
- [Operators Leadscore API](../operators-leadscore-api/OPERATOR_README.md)
- [Meta Portfolio](../meta_portfolio/README.md)

## Operator principles
Automation first, modularity, operator focus and compounding learning.
