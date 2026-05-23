# Final Validation Checklist

This checklist validates the project against the assignment requirements using the current repository files and generated outputs.

| Requirement | Status | Evidence file/path | Notes |
| --- | --- | --- | --- |
| Track A completed | Complete | `track_a_social_network/github_network.py` | Includes data collection, edge/node table creation, network analysis, and visualizations. |
| Track B completed | Complete | `track_b_realtime_dashboard/app.py` | Includes live API polling, metrics, charting, status display, and alerting. |
| Edge list exists | Complete | `track_a_social_network/data/edge_list.csv` | Generated developer-developer edge list with shared repository weights. |
| Node table exists | Complete | `track_a_social_network/data/node_table.csv` | Generated node table with developer attributes and network metrics. |
| Community detection exists | Complete | `track_a_social_network/github_network.py` | Louvain detection implemented with `community_louvain.best_partition(...)`. |
| Node size uses centrality | Complete | `track_a_social_network/github_network.py` | Degree centrality is mapped to node size in PyVis and Matplotlib visualizations. |
| Communities use color | Complete | `track_a_social_network/github_network.py` | Louvain community IDs are mapped through `get_community_color(...)`. |
| Layout justification exists | Complete | `report/technical_report.md` | Section 11 explains the force-directed layout. Code comments also justify force-directed layouts. |
| Interactive/static visualization exists | Complete | `track_a_social_network/outputs/github_network.html`; `track_a_social_network/outputs/github_network.png` | Both interactive HTML and static PNG outputs are present. |
| Live API integration exists | Complete | `track_b_realtime_dashboard/app.py` | Uses CoinGecko simple price REST API. |
| Sliding window chart exists | Complete | `track_b_realtime_dashboard/app.py` | Uses Plotly line chart and keeps recent observations per coin. |
| Alert threshold exists | Complete | `track_b_realtime_dashboard/app.py` | BTC alert threshold is set to a drop of more than 2% over approximately five minutes. |
| Last updated timestamp exists | Complete | `track_b_realtime_dashboard/app.py` | `render_status(...)` displays the last updated timestamp. |
| Connection status exists | Complete | `track_b_realtime_dashboard/app.py` | Dashboard shows live or API unavailable status. |
| Source code exists | Complete | `track_a_social_network/github_network.py`; `track_b_realtime_dashboard/app.py` | Both track source files are present. |
| README exists | Complete | `README.md` | Project overview, setup, run instructions, outputs, and checklist are included. |
| Technical report exists | Complete | `report/technical_report.md` | Full technical report with Track A and Track B methodology is present. |
| Submission package ready | Complete | Project root | Required code, reports, README, requirements, generated Track A outputs, and Track B data file are present. |

## Remaining Issues

No assignment-blocking issues were found in the current repository validation.

## Non-Blocking Notes

- The final report still contains placeholders such as `[insert top developer from node_table.csv]`. These should be filled manually after confirming the final generated CSV values.
- API-based outputs can change over time because GitHub and CoinGecko data are live sources.
- The local repository includes generated files and a virtual environment directory. The `.gitignore` excludes `venv/` and Python cache files for submission hygiene.
