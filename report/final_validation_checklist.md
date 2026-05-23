# Final Validation Checklist

This checklist reviews the repository against the assignment submission requirements.

## Submission Package

| Requirement | Status | Evidence | Notes |
| --- | --- | --- | --- |
| Technical Report PDF exists | Complete | `report/technical_report.pdf` | PDF file is present in the report folder. |
| Executive summary of both projects exists | Complete | `report/technical_report.md` | Section 1 summarizes Track A and Track B. |
| Visualization Design Document exists | Complete | `report/visualization_design_document.md` | Separate design document is present. |
| User Persona exists | Complete | `report/technical_report.md`; `report/visualization_design_document.md` | Persona is included in both report documents. |
| Visual Encoding mappings exist | Complete | `report/technical_report.md`; `report/visualization_design_document.md` | Track A and Track B mappings are documented. |
| Track A community interpretation exists | Partial | `report/technical_report.md` | Community narrative section exists, but final community values should be copied from generated outputs. |
| Track B live trend interpretation exists | Complete | `report/technical_report.md`; `track_b_realtime_dashboard/app.py` | Report explains rolling trend monitoring; dashboard uses normalized percentage-change chart. |
| Source code is organized | Complete | `track_a_social_network/`; `track_b_realtime_dashboard/`; `report/` | Project is separated by track and report folders. |
| Source code is commented | Complete | `track_a_social_network/github_network.py`; `track_b_realtime_dashboard/app.py` | Comments explain API handling, projection logic, visual encodings, caching, and chart normalization. |
| README includes group members | Complete | `README.md` | Four group member placeholders are included. |
| README includes run/view instructions | Complete | `README.md` | Track A and Track B run commands are included. |

## Track A

| Requirement | Status | Evidence | Notes |
| --- | --- | --- | --- |
| Social network visualization exists | Complete | `track_a_social_network/outputs/github_network.html`; `track_a_social_network/outputs/github_network.png` | Interactive and static network visualizations are present. |
| Edge list exists | Complete | `track_a_social_network/data/edge_list.csv` | Edge list CSV is present. |
| Node table exists | Complete | `track_a_social_network/data/node_table.csv` | Node table CSV is present. |
| Community detection exists | Complete | `track_a_social_network/github_network.py` | Louvain community detection is implemented with edge weights. |
| Node color represents community | Complete | `track_a_social_network/github_network.py` | Community IDs are mapped to node colors. |
| Node size represents centrality | Complete | `track_a_social_network/github_network.py` | Degree centrality is mapped to node size. |
| Edge weight is defined | Complete | `track_a_social_network/github_network.py`; `track_a_social_network/data/edge_list.csv` | Edge weight is the number of shared repositories. |
| Layout justification exists | Complete | `report/technical_report.md`; `track_a_social_network/github_network.py` | Force-directed layout is explained in the report and comments. |
| Key actors are identified | Partial | `report/technical_report.md`; `track_a_social_network/data/node_table.csv` | Key actor section exists, but final names should be filled from `node_table.csv`. |
| Weak link or bridge analysis exists | Partial | `report/technical_report.md`; `track_a_social_network/data/edge_list.csv` | Bridge analysis section exists, but final bridge actors and values should be filled from outputs. |

## Track B

| Requirement | Status | Evidence | Notes |
| --- | --- | --- | --- |
| Real-time API integration exists | Complete | `track_b_realtime_dashboard/app.py` | Uses CoinGecko simple price REST API. |
| Functional dashboard exists | Complete | `track_b_realtime_dashboard/app.py` | Streamlit dashboard implementation is present. |
| Temporal chart exists | Complete | `track_b_realtime_dashboard/app.py` | Plotly rolling line chart is implemented. |
| Sliding window exists | Complete | `track_b_realtime_dashboard/app.py` | Keeps approximately 15 minutes of data using 30 points per coin. |
| Conditional alert exists | Complete | `track_b_realtime_dashboard/app.py` | BTC alert triggers on a drop greater than 2% over approximately 5 minutes. |
| Last updated timestamp exists | Complete | `track_b_realtime_dashboard/app.py` | Dashboard displays last updated timestamp. |
| Connection status exists | Complete | `track_b_realtime_dashboard/app.py` | Dashboard shows live or cached-data status. |
| Live trend interpretation exists | Complete | `report/technical_report.md`; `track_b_realtime_dashboard/app.py` | Live trend is represented through normalized percentage-change chart and explained in the report. |

## Evaluation Criteria

| Requirement | Status | Evidence | Notes |
| --- | --- | --- | --- |
| Technical Implementation | Complete | `track_a_social_network/github_network.py`; `track_b_realtime_dashboard/app.py` | Both tracks include working Python implementations with API use, persistence, and output generation. |
| Design & Aesthetics | Complete | `report/visualization_design_document.md`; output visualizations | Visual encodings, label management, color use, alert design, and cognitive load strategies are documented. |
| Analytical Depth | Partial | `report/technical_report.md`; generated CSV files | Methods are documented, but final report placeholders for exact Track A actors and communities should be filled before submission. |

## Remaining Items Before Submission

- Fill final Track A community, key actor, and bridge-analysis placeholders in `report/technical_report.md`.
- Confirm the exported PDF reflects the final updated report text.
- Add real group member names in `README.md`.

The project is ready for final submission if all evidence files are present and the PDF report has been exported.
