# Data Visualization Final Project

## Group Members

- Student 1: [Yiğit Özdemir]
- Student 2: [Berzan Uludağ]
- Student 3: [Berkay Yurttaş]

## Project Overview

This project is a university Data Visualization final project that includes both mandatory tracks:

- Track A: Social Network Visualization & Community Discovery
- Track B: Real-Time Data Visualization Dashboard

Track A analyzes a multi-repository GitHub developer network using contributor data from the GitHub REST API. Track B implements a Streamlit dashboard that monitors live cryptocurrency prices from the CoinGecko API.

The project uses real API-based data. Output values may vary depending on live service availability, API rate limits, and the time when the scripts are executed.

## Track A: Social Network Visualization & Community Discovery

Track A uses GitHub REST API contributor data from selected open-source repositories, including:

- `django/django`
- `fastapi/fastapi`
- `pandas-dev/pandas`
- `scikit-learn/scikit-learn`
- `pallets/flask`

The script creates a raw contributor dataset, then models the data as developer-repository relationships. It projects this into a developer-developer network, where two developers are connected if they contributed to at least one same repository.

The edge list stores developer pairs, edge weights, and shared repositories. The node table stores developer-level attributes, repository counts, contribution totals, centrality values, and community IDs.

Louvain community detection is applied to identify groups of developers with stronger internal connections. Degree centrality and betweenness centrality are calculated to support analysis of central actors and possible bridge developers.

Track A outputs:

- `raw_contributors.csv`
- `edge_list.csv`
- `node_table.csv`
- `github_network.html`
- `github_network.png`

## Track B: Real-Time Data Visualization Dashboard

Track B uses the CoinGecko simple price API to monitor live cryptocurrency prices in USD for:

- Bitcoin (BTC)
- Ethereum (ETH)
- Solana (SOL)

The dashboard is implemented with Streamlit and refreshes every 30 seconds. It stores recent observations in `live_crypto_data.csv` and keeps approximately the last 15 minutes of data.

The dashboard includes raw price metric cards, connection status, last updated timestamp, a normalized rolling percentage-change line chart, and a Bitcoin alert. The normalized chart makes BTC, ETH, and SOL easier to compare on the same axis.

The alert triggers if Bitcoin drops more than 2% over approximately 5 minutes. If the CoinGecko API fails or returns a rate-limit error, the dashboard uses cached CSV data instead of crashing.

## Technologies Used

- Python
- Pandas
- NetworkX
- Louvain community detection
- PyVis
- Matplotlib
- Streamlit
- Plotly
- Requests

## Installation Instructions

From the project root, create a virtual environment:

```powershell
python -m venv venv
```

Activate the virtual environment:

```powershell
venv\Scripts\activate
```

Install the required dependencies:

```powershell
pip install -r requirements.txt
```

## How to Run Track A

Run the GitHub network script from the project root:

```powershell
python track_a_social_network/github_network.py
```

On Windows PowerShell, this command also works:

```powershell
python track_a_social_network\github_network.py
```

## How to Run Track B

Run the Streamlit dashboard from the project root:

```powershell
streamlit run track_b_realtime_dashboard/app.py
```

On Windows PowerShell, this command also works:

```powershell
streamlit run track_b_realtime_dashboard\app.py
```

## Output Files

Track A:

- `track_a_social_network/data/raw_contributors.csv`
- `track_a_social_network/data/edge_list.csv`
- `track_a_social_network/data/node_table.csv`
- `track_a_social_network/outputs/github_network.html`
- `track_a_social_network/outputs/github_network.png`

Track B:

- `track_b_realtime_dashboard/data/live_crypto_data.csv`

Reports:

- `report/technical_report.md`
- `report/visualization_design_document.md`
- `report/final_validation_checklist.md`

## API Notes

The project depends on live public APIs, so data may vary between runs.

GitHub API notes:

- The GitHub API may occasionally timeout, especially for large repositories.
- The Track A script retries failed requests and skips repositories that continue to fail.
- Partial data is saved if at least one repository succeeds.
- A GitHub token can be set with `GITHUB_TOKEN` to reduce rate-limit issues.

CoinGecko API notes:

- CoinGecko may occasionally return rate-limit errors such as `429 Too Many Requests`.
- The Track B dashboard handles these errors gracefully.
- If the API fails, the dashboard keeps existing data and displays cached observations.
- Cached data should not be interpreted as a fresh API response.

## Submission Package Checklist

- [ ] Technical_Report.pdf
- [ ] Source code
- [ ] README.md
- [ ] Output files
- [ ] Dashboard screenshot or screen recording if needed
- [ ] Group member names filled in
- [ ] Final outputs reviewed before submission
