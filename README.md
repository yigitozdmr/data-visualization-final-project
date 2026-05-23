# Data Visualization Final Project

## Project Overview

This project contains two complementary data visualization tracks developed for a university Data Visualization final project. Track A focuses on social network visualization using GitHub contributor data, while Track B focuses on real-time dashboard design using live cryptocurrency price data.

The project is implemented in Python and emphasizes data collection, network analysis, visual encoding, interactivity, and real-time monitoring. The visualizations are intended to support exploration and interpretation, not to make exaggerated claims about developer behavior or cryptocurrency markets.

## Assignment Context

The project demonstrates two common categories of visualization systems:

- A network visualization based on relationships extracted from real-world data.
- A real-time dashboard based on live API polling and continuously updated data.

Both tracks use public APIs and reproducible Python scripts. The work is organized so that each track can be run independently.

## Track A: Social Network Visualization

Track A builds a multi-repository GitHub developer network. Contributor data is collected from selected open-source repositories:

- `pallets/flask`
- `django/django`
- `fastapi/fastapi`
- `pandas-dev/pandas`
- `scikit-learn/scikit-learn`

The data is first treated as a bipartite relationship between developers and repositories. It is then projected into a developer-developer network, where two developers are connected if they contributed to at least one same repository. Edge weight represents the number of shared repositories.

The script calculates network metrics including degree, degree centrality, betweenness centrality, and Louvain community detection. It exports both an interactive PyVis HTML network and a static Matplotlib PNG network.

## Track B: Real-Time Data Dashboard

Track B implements a real-time cryptocurrency monitoring dashboard using CoinGecko live crypto data. The dashboard tracks:

- Bitcoin
- Ethereum
- Solana

Prices are fetched in USD from the CoinGecko simple price API. The Streamlit dashboard refreshes every 10 seconds, stores recent observations in a CSV file, displays current price metrics, and shows a rolling Plotly line chart. It also includes a threshold-based alert if Bitcoin drops more than 2% compared to approximately five minutes earlier.

## Folder Structure

```text
data-visualization-final-project/
|
|-- track_a_social_network/
|   |-- github_network.py
|   |-- data/
|   `-- outputs/
|
|-- track_b_realtime_dashboard/
|   |-- app.py
|   `-- data/
|
|-- report/
|   |-- technical_report.md
|   `-- visualization_design_document.md
|
|-- requirements.txt
|-- README.md
`-- .gitignore
```

## Technologies Used

- Python
- pandas
- requests
- NetworkX
- python-louvain
- PyVis
- Matplotlib
- Streamlit
- Plotly
- streamlit-autorefresh

## Installation Instructions

Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\activate
```

Install the required packages:

```powershell
pip install -r requirements.txt
```

## How to Run Track A

Run the GitHub developer network script from the project root:

```powershell
python track_a_social_network\github_network.py
```

The script collects GitHub contributor data, constructs the developer network, calculates network metrics, and generates the required output files.

## How to Run Track B

Run the Streamlit dashboard from the project root:

```powershell
streamlit run track_b_realtime_dashboard\app.py
```

The dashboard opens in a browser and refreshes automatically every 10 seconds.

## Output Files

Track A outputs:

- `track_a_social_network/data/raw_contributors.csv`
- `track_a_social_network/data/edge_list.csv`
- `track_a_social_network/data/node_table.csv`
- `track_a_social_network/outputs/github_network.html`
- `track_a_social_network/outputs/github_network.png`

Track B outputs:

- `track_b_realtime_dashboard/data/live_crypto_data.csv`

Report files:

- `report/technical_report.md`
- `report/visualization_design_document.md`

## API Notes

Track A uses the GitHub REST API. A GitHub token is optional but recommended to reduce rate-limit issues:

```powershell
$env:GITHUB_TOKEN="your_token_here"
```

Track B uses the free CoinGecko simple price API. API availability and rate limits may affect live dashboard updates. If the API request fails, the dashboard shows an unavailable connection status and preserves the most recent stored data when available.

## Group Members

- Student 1:
- Student 2:
- Student 3:

## Submission Checklist

- [ ] Track A script runs successfully.
- [ ] Track A CSV files are generated.
- [ ] Track A interactive HTML visualization is generated.
- [ ] Track A static PNG visualization is generated.
- [ ] Track B Streamlit dashboard runs successfully.
- [ ] Track B live data CSV is generated.
- [ ] Technical report is completed.
- [ ] Visualization design document is completed.
- [ ] Group member names are added.
- [ ] Final project files are reviewed before submission.
