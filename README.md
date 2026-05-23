# Data Visualization Final Project

## Overview

This repository contains a university Data Visualization final project with two required tracks:

- **Track A: Social Network Visualization & Community Discovery**
- **Track B: Real-Time Data Visualization Dashboard**

The project uses real API-based datasets and Python visualization tools. Track A analyzes relationships among GitHub developers across multiple open-source repositories. Track B monitors live cryptocurrency prices from CoinGecko in a Streamlit dashboard.

The project is designed for academic evaluation of data collection, visual encoding, interactivity, network analysis, and real-time dashboard design. Results may vary because both tracks depend on live public APIs.

## Assignment Requirements Covered

Track A covers:

- Real-world social network data from the GitHub REST API
- Multi-repository GitHub developer network construction
- Developer-developer projected network
- Edge list and node table generation
- Degree centrality and betweenness centrality
- Louvain community detection
- Community-based node color
- Degree-centrality-based node size
- Shared-repository edge weight and edge width
- Interactive HTML network visualization
- Static PNG network visualization

Track B covers:

- Real-time dashboard using Streamlit
- Live REST API polling with CoinGecko
- BTC, ETH, and SOL price monitoring in USD
- 30-second auto-refresh interval
- Sliding window of approximately the last 15 minutes
- CSV persistence for recent observations
- Raw price metric cards
- Normalized rolling percentage-change chart
- Connection status and last updated timestamp
- Cached data fallback if the API fails or rate limits occur
- BTC alert if price drops more than 2% over approximately 5 minutes

## Track A: GitHub Developer Network

Track A builds a multi-repository GitHub Developer Network from contributor data. The repositories are:

- `django/django`
- `fastapi/fastapi`
- `pandas-dev/pandas`
- `scikit-learn/scikit-learn`
- `pallets/flask`

The GitHub API can occasionally return timeouts for large repositories. In particular, `pallets/flask` may fail due to a GitHub API timeout. The script handles failures gracefully, saves partial data when at least one repository succeeds, and reports successful and failed repositories.

The data is modeled first as a developer-repository relationship. It is then projected into a developer-developer network where two developers are connected if they contributed to at least one same repository.

## Track B: Real-Time Crypto Dashboard

Track B is a Streamlit dashboard that tracks live cryptocurrency prices from the CoinGecko API:

- Bitcoin (BTC)
- Ethereum (ETH)
- Solana (SOL)

The dashboard refreshes every 30 seconds to reduce rate-limit risk while still providing a real-time monitoring experience suitable for a student project. It stores recent observations in a CSV file, keeps approximately the last 15 minutes of data, and uses cached data if CoinGecko temporarily fails or returns a rate-limit response.

The metric cards show raw USD prices. The main rolling chart uses normalized percentage change from the start of the current window so BTC, ETH, and SOL can be compared on the same chart without smaller-price assets appearing flat.

## Folder Structure

```text
data-visualization-final-project/
|
|-- track_a_social_network/
|   |-- github_network.py
|   |-- data/
|   |   |-- raw_contributors.csv
|   |   |-- edge_list.csv
|   |   `-- node_table.csv
|   `-- outputs/
|       |-- github_network.html
|       `-- github_network.png
|
|-- track_b_realtime_dashboard/
|   |-- app.py
|   `-- data/
|       `-- live_crypto_data.csv
|
|-- report/
|   |-- technical_report.md
|   |-- visualization_design_document.md
|   `-- final_validation_checklist.md
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

## Setup Instructions

Run all commands from the project root:

```powershell
cd D:\data-visualization-final-project
```

Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\activate
```

## Install Dependencies

Install the required Python packages:

```powershell
pip install -r requirements.txt
```

## Run Track A

Run the GitHub network analysis script:

```powershell
python track_a_social_network\github_network.py
```

The script will:

- collect GitHub contributor data
- save `raw_contributors.csv`
- build `edge_list.csv`
- build and update `node_table.csv`
- calculate degree centrality and betweenness centrality
- apply Louvain community detection
- export the interactive HTML network
- export the static PNG network

Optional GitHub token support is available to reduce rate-limit issues:

```powershell
$env:GITHUB_TOKEN="your_token_here"
python track_a_social_network\github_network.py
```

## Run Track B

Run the Streamlit dashboard:

```powershell
streamlit run track_b_realtime_dashboard\app.py
```

The dashboard opens in a browser and refreshes every 30 seconds.

## Output Files

Track A output files:

- `track_a_social_network/data/raw_contributors.csv`
- `track_a_social_network/data/edge_list.csv`
- `track_a_social_network/data/node_table.csv`
- `track_a_social_network/outputs/github_network.html`
- `track_a_social_network/outputs/github_network.png`

Track B output file:

- `track_b_realtime_dashboard/data/live_crypto_data.csv`

Report files:

- `report/technical_report.md`
- `report/visualization_design_document.md`
- `report/final_validation_checklist.md`

## API Reliability Notes

This project depends on live public APIs. Data and output files may vary depending on API availability, rate limits, repository activity, and the time of execution.

GitHub API notes:

- Track A uses the GitHub REST API contributors endpoint.
- Some repositories may return temporary timeout errors.
- The script retries requests and skips failed repositories gracefully.
- A GitHub token is optional but recommended.

CoinGecko API notes:

- Track B uses the free CoinGecko simple price API.
- The dashboard polls every 30 seconds to reduce rate-limit risk.
- If CoinGecko returns `429 Too Many Requests` or another API error, the dashboard keeps existing CSV data and displays cached data instead of crashing.
- Cached data should be interpreted as the most recent stored observation, not a fresh API response.

## Group Members

- Student 1:
- Student 2:
- Student 3:

## Submission Checklist

- [ ] Dependencies are installed from `requirements.txt`.
- [ ] Track A script runs successfully.
- [ ] Track A CSV files are generated.
- [ ] Track A interactive HTML visualization is generated.
- [ ] Track A static PNG visualization is generated.
- [ ] Track B Streamlit dashboard runs successfully.
- [ ] Track B live data CSV is generated.
- [ ] Technical report is completed.
- [ ] Visualization design document is completed.
- [ ] Final validation checklist is completed.
- [ ] Group member names are added.
- [ ] Generated outputs are reviewed before submission.
