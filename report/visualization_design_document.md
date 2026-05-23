# Visualization Design Document

## 1. User Persona

The primary user is a university evaluator or data visualization student who needs to inspect whether the project applies appropriate visual design, data transformation, and interaction principles. The user is technically literate but should not need to read the source code to understand the main visual encodings.

## 2. User Goals

- Understand the structure of a multi-repository GitHub developer network.
- Identify central developers and possible bridge actors.
- Observe community patterns in the developer network.
- Monitor live cryptocurrency prices for Bitcoin, Ethereum, and Solana.
- Detect whether Bitcoin has dropped more than the defined short-term alert threshold.
- Interpret the visualizations without unnecessary visual clutter.

## 3. Track A Visual Encoding Table

| Data Attribute | Visual Encoding | Purpose |
| --- | --- | --- |
| Developer | Node | Represents each GitHub contributor. |
| Shared repository relationship | Edge | Shows that two developers contributed to at least one same repository. |
| Number of shared repositories | Edge width | Emphasizes stronger developer relationships. |
| Louvain community | Node color | Separates detected network communities. |
| Degree centrality | Node size | Highlights highly connected developers. |
| Top 5 developers by degree centrality | Text label | Identifies key actors without labeling every node. |
| Developer details | Tooltip | Provides detailed information on demand. |

## 4. Track B Visual Encoding Table

| Data Attribute | Visual Encoding | Purpose |
| --- | --- | --- |
| Current cryptocurrency price | Metric card | Supports quick reading of current values. |
| Time | X-axis position | Shows price movement over the recent window. |
| Price in USD | Y-axis position | Enables comparison of price changes over time. |
| Cryptocurrency symbol | Line color | Distinguishes BTC, ETH, and SOL. |
| API connection state | Status indicator | Shows whether live data is currently available. |
| Last update time | Timestamp text | Communicates data freshness. |
| BTC drop threshold | Warning banner | Draws attention only when the alert condition is met. |

## 5. Pre-Attentive Attributes Used

The project uses several pre-attentive attributes to help users interpret patterns quickly:

- Color separates communities in Track A and coin series in Track B.
- Size highlights more central developers in Track A.
- Width emphasizes stronger shared-repository relationships in Track A.
- Position supports network clustering in Track A and time-series reading in Track B.
- Strong red warning color signals alert conditions in Track B.

## 6. Cognitive Load Reduction Strategies

The design reduces cognitive load by limiting the amount of information shown at once. Track A labels only the top five developers by degree centrality and moves detailed metrics into tooltips. This prevents the network from becoming unreadable.

Track B separates information into metric cards, status information, alert text, and a line chart. This allows users to scan current values first, then inspect recent trends if needed.

Both tracks avoid unnecessary decorative elements and use clear visual hierarchy.

## 7. Color Usage Justification

Track A uses color to represent Louvain community membership. This helps users distinguish groups without reading node attributes manually.

Track B uses muted line colors for normal price data so the chart remains readable. A strong red color is reserved for the Bitcoin alert condition. This makes the warning visually distinct and prevents normal data from appearing unnecessarily alarming.

Colors are used categorically rather than as precise numerical scales.

## 8. Label Management Strategy

Labels are intentionally limited in Track A. Network diagrams can become visually noisy when every node is labeled, especially after bipartite data is projected into developer-developer edges.

The project labels only the top five developers by degree centrality. Other node details are available through interactive tooltips in the HTML visualization. This balances readability with access to detailed information.

Track B uses short labels for metric cards and chart legends to keep the dashboard compact.

## 9. Alert Design Strategy

The Track B alert is threshold-based. If Bitcoin drops more than 2% compared to approximately five minutes earlier, the dashboard displays a red warning banner.

The alert is designed to be simple, visible, and interpretable. It is not presented as a financial recommendation. Normal conditions are shown with muted text so that the alert state receives attention only when necessary.

## 10. Accessibility Considerations

The project uses text labels, tooltips, and metric values so that meaning is not communicated by color alone. Track A combines color with node size, edge width, labels, and tooltips. Track B combines color with metric cards, axis labels, status text, and warning text.

The dashboard uses readable spacing and avoids overloaded panels. The network visualization limits labels to reduce overlap and improve legibility. Future accessibility improvements could include a colorblind-safe palette, larger font options, and a textual summary of the top network actors and current alert state.
