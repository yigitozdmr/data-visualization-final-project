"""Collect contributor data for Track A: Social Network Visualization.

This stage only collects and saves raw contributor data. Graph construction
and visualization will be implemented later.
"""

from __future__ import annotations

import itertools
import os
import time
from collections import defaultdict
from pathlib import Path

import community as community_louvain
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import requests
from pyvis.network import Network


REPOSITORIES = [
    "pallets/flask",
    "django/django",
    "fastapi/fastapi",
    "pandas-dev/pandas",
    "scikit-learn/scikit-learn",
]

CONTRIBUTOR_LIMIT_PER_REPOSITORY = 40
GITHUB_API_BASE_URL = "https://api.github.com"
REQUEST_TIMEOUT_SECONDS = 30
MAX_RETRY_ATTEMPTS = 3
RETRY_WAIT_SECONDS = 3

# Increase this to 2 if the developer-developer network becomes too dense.
MIN_EDGE_WEIGHT = 1

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TRACK_A_DIR = PROJECT_ROOT / "track_a_social_network"
DATA_DIR = TRACK_A_DIR / "data"
OUTPUTS_DIR = TRACK_A_DIR / "outputs"
RAW_CONTRIBUTORS_PATH = DATA_DIR / "raw_contributors.csv"
EDGE_LIST_PATH = DATA_DIR / "edge_list.csv"
NODE_TABLE_PATH = DATA_DIR / "node_table.csv"
HTML_OUTPUT_PATH = OUTPUTS_DIR / "github_network.html"
PNG_OUTPUT_PATH = OUTPUTS_DIR / "github_network.png"


def create_directories() -> None:
    """Create Track A data and outputs directories if they do not exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Data directory ready: {DATA_DIR}")
    print(f"Outputs directory ready: {OUTPUTS_DIR}")


def fetch_contributors(repo_name: str) -> list[dict[str, object]]:
    """Fetch up to 40 contributors for one GitHub repository."""
    url = f"{GITHUB_API_BASE_URL}/repos/{repo_name}/contributors"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "data-visualization-final-project",
    }

    # A token is optional, but useful for avoiding strict unauthenticated limits.
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    for attempt in range(1, MAX_RETRY_ATTEMPTS + 1):
        print(f"Request attempt {attempt}/{MAX_RETRY_ATTEMPTS} for {repo_name}...")

        try:
            response = requests.get(
                url,
                headers=headers,
                params={"per_page": CONTRIBUTOR_LIMIT_PER_REPOSITORY},
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            contributors = response.json()
        except requests.exceptions.HTTPError as error:
            print(f"API error while fetching {repo_name}: {error}")
        except requests.exceptions.RequestException as error:
            print(f"Network error while fetching {repo_name}: {error}")
        except ValueError as error:
            print(f"Invalid JSON response for {repo_name}: {error}")
        else:
            if isinstance(contributors, list):
                break

            print(f"Unexpected API response format for {repo_name}.")

        if attempt < MAX_RETRY_ATTEMPTS:
            print(f"Retrying {repo_name} in {RETRY_WAIT_SECONDS} seconds...")
            time.sleep(RETRY_WAIT_SECONDS)
    else:
        print(f"All retry attempts failed for {repo_name}. Skipping repository.")
        return []

    rows: list[dict[str, object]] = []
    for contributor in contributors[:CONTRIBUTOR_LIMIT_PER_REPOSITORY]:
        developer = contributor.get("login")
        if not developer:
            continue

        rows.append(
            {
                "developer": developer,
                "repository": repo_name,
                "contributions": contributor.get("contributions", 0),
                "github_profile_url": contributor.get("html_url", ""),
            }
        )

    return rows


def collect_github_data() -> pd.DataFrame:
    """Collect contributor data from all selected GitHub repositories."""
    all_contributors: list[dict[str, object]] = []
    successful_repositories: list[str] = []
    failed_repositories: list[str] = []

    for repo_name in REPOSITORIES:
        print(f"Fetching contributors for {repo_name}...")
        contributors = fetch_contributors(repo_name)

        if contributors:
            successful_repositories.append(repo_name)
            all_contributors.extend(contributors)
            print(f"Collected {len(contributors)} contributors from {repo_name}.")
        else:
            failed_repositories.append(repo_name)
            print(f"No contributor data collected from {repo_name}.")

    if not successful_repositories:
        raise RuntimeError(
            "No GitHub repositories were collected successfully. "
            "Check your network connection, GitHub API availability, or GITHUB_TOKEN."
        )

    contributors_df = pd.DataFrame(
        all_contributors,
        columns=[
            "developer",
            "repository",
            "contributions",
            "github_profile_url",
        ],
    )

    contributors_df.to_csv(RAW_CONTRIBUTORS_PATH, index=False)
    print(f"Saved {len(contributors_df)} rows to {RAW_CONTRIBUTORS_PATH}")
    print(f"Successful repositories: {', '.join(successful_repositories)}")
    print(
        "Failed repositories: "
        f"{', '.join(failed_repositories) if failed_repositories else 'None'}"
    )
    print(f"Total contributors collected: {len(contributors_df)}")

    return contributors_df


def build_edge_list(contributors_df: pd.DataFrame) -> pd.DataFrame:
    """Build developer-developer edges from shared repository contributions."""
    shared_repositories_by_pair: dict[tuple[str, str], set[str]] = defaultdict(set)

    # Treat the raw data as Developer -> Repository, then project developers.
    for repository, repo_group in contributors_df.groupby("repository"):
        developers = sorted(repo_group["developer"].dropna().unique())

        for source, target in itertools.combinations(developers, 2):
            shared_repositories_by_pair[(source, target)].add(repository)

    edge_rows: list[dict[str, object]] = []
    for (source, target), repositories in shared_repositories_by_pair.items():
        shared_repositories = sorted(repositories)
        weight = len(shared_repositories)

        if weight < MIN_EDGE_WEIGHT:
            continue

        edge_rows.append(
            {
                "source": source,
                "target": target,
                "weight": weight,
                "shared_repositories": "; ".join(shared_repositories),
            }
        )

    edge_list_df = pd.DataFrame(
        edge_rows,
        columns=["source", "target", "weight", "shared_repositories"],
    )

    if not edge_list_df.empty:
        edge_list_df = edge_list_df.sort_values(
            by=["weight", "source", "target"],
            ascending=[False, True, True],
        )

    return edge_list_df


def build_node_table(contributors_df: pd.DataFrame) -> pd.DataFrame:
    """Build developer-level metadata for the projected network nodes."""
    node_table_df = (
        contributors_df.groupby("developer")
        .agg(
            repositories=("repository", lambda values: "; ".join(sorted(set(values)))),
            repository_count=("repository", "nunique"),
            total_contributions=("contributions", "sum"),
        )
        .reset_index()
    )

    return node_table_df.sort_values(
        by=["repository_count", "total_contributions", "developer"],
        ascending=[False, False, True],
    )


def create_graph(edge_df: pd.DataFrame) -> nx.Graph:
    """Create an undirected weighted developer graph from the edge list."""
    graph = nx.Graph()

    for row in edge_df.itertuples(index=False):
        graph.add_edge(
            row.source,
            row.target,
            weight=int(row.weight),
            shared_repositories=row.shared_repositories,
        )

    return graph


def analyze_graph(graph: nx.Graph, node_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate graph metrics and append them to the node table."""
    for developer in node_df["developer"]:
        graph.add_node(developer)

    degree_by_developer = dict(graph.degree())
    degree_centrality = nx.degree_centrality(graph)
    betweenness_centrality = nx.betweenness_centrality(graph)

    if graph.number_of_edges() > 0:
        communities = community_louvain.best_partition(
            graph,
            weight="weight",
            random_state=42,
        )
    else:
        communities = {developer: 0 for developer in graph.nodes}

    analyzed_node_df = node_df.copy()
    analyzed_node_df["degree"] = analyzed_node_df["developer"].map(
        degree_by_developer
    )
    analyzed_node_df["degree_centrality"] = analyzed_node_df["developer"].map(
        degree_centrality
    )
    analyzed_node_df["betweenness_centrality"] = analyzed_node_df["developer"].map(
        betweenness_centrality
    )
    analyzed_node_df["community"] = analyzed_node_df["developer"].map(communities)

    return analyzed_node_df.sort_values(
        by=["degree_centrality", "betweenness_centrality", "developer"],
        ascending=[False, False, True],
    )


def print_network_summary(graph: nx.Graph, node_df: pd.DataFrame) -> None:
    """Print a concise summary of the analyzed developer network."""
    community_count = node_df["community"].nunique()
    top_degree = node_df.nlargest(5, "degree_centrality")
    top_betweenness = node_df.nlargest(5, "betweenness_centrality")

    print("Network analysis summary:")
    print(f"Number of nodes: {graph.number_of_nodes()}")
    print(f"Number of edges: {graph.number_of_edges()}")
    print(f"Number of communities: {community_count}")

    print("Top 5 developers by degree centrality:")
    for row in top_degree.itertuples(index=False):
        print(f"- {row.developer}: {row.degree_centrality:.4f}")

    print("Top 5 developers by betweenness centrality:")
    for row in top_betweenness.itertuples(index=False):
        print(f"- {row.developer}: {row.betweenness_centrality:.4f}")


def get_community_color(community: int) -> str:
    """Return a consistent color for each Louvain community."""
    color_palette = [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
    ]
    return color_palette[community % len(color_palette)]


def create_interactive_visualization(graph: nx.Graph, node_df: pd.DataFrame) -> None:
    """Create an interactive PyVis network visualization."""
    node_lookup = node_df.set_index("developer").to_dict(orient="index")
    top_label_developers = set(node_df.nlargest(5, "degree_centrality")["developer"])

    network = Network(
        height="800px",
        width="100%",
        bgcolor="#ffffff",
        font_color="#222222",
        notebook=False,
    )

    # Force-directed layouts help reveal community separation and bridge nodes.
    network.force_atlas_2based(
        gravity=-50,
        central_gravity=0.01,
        spring_length=130,
        spring_strength=0.08,
        damping=0.4,
    )

    for developer in graph.nodes:
        node_data = node_lookup.get(developer, {})
        degree_centrality = float(node_data.get("degree_centrality", 0.0))
        community = int(node_data.get("community", 0))
        label = developer if developer in top_label_developers else ""
        size = 8 + (degree_centrality * 60)
        tooltip = (
            f"<b>{developer}</b><br>"
            f"Community: {community}<br>"
            f"Degree: {int(node_data.get('degree', 0))}<br>"
            f"Degree centrality: {degree_centrality:.4f}<br>"
            "Betweenness centrality: "
            f"{float(node_data.get('betweenness_centrality', 0.0)):.4f}<br>"
            f"Repositories: {node_data.get('repositories', '')}"
        )

        network.add_node(
            developer,
            label=label,
            title=tooltip,
            size=size,
            color=get_community_color(community),
        )

    for source, target, edge_data in graph.edges(data=True):
        weight = int(edge_data.get("weight", 1))
        network.add_edge(
            source,
            target,
            value=weight,
            width=weight,
            title=f"Shared repositories: {edge_data.get('shared_repositories', '')}",
        )

    network.write_html(str(HTML_OUTPUT_PATH), notebook=False)
    print(f"Saved interactive visualization to {HTML_OUTPUT_PATH}")


def create_static_visualization(graph: nx.Graph, node_df: pd.DataFrame) -> None:
    """Create a static Matplotlib and NetworkX PNG visualization."""
    node_lookup = node_df.set_index("developer").to_dict(orient="index")
    top_label_developers = set(node_df.nlargest(5, "degree_centrality")["developer"])

    # Force-directed layout positions connected communities near each other and
    # helps highlight developers who bridge otherwise separate groups.
    positions = nx.spring_layout(graph, weight="weight", seed=42, k=0.35)

    node_sizes = [
        80 + (float(node_lookup.get(node, {}).get("degree_centrality", 0.0)) * 1200)
        for node in graph.nodes
    ]
    node_colors = [
        get_community_color(int(node_lookup.get(node, {}).get("community", 0)))
        for node in graph.nodes
    ]
    edge_widths = [
        0.3 + (0.5 * int(edge_data.get("weight", 1)))
        for _, _, edge_data in graph.edges(data=True)
    ]
    labels = {developer: developer for developer in top_label_developers}

    plt.figure(figsize=(16, 12))
    nx.draw_networkx_edges(
        graph,
        positions,
        alpha=0.15,
        edge_color="#555555",
        width=edge_widths,
    )
    nx.draw_networkx_nodes(
        graph,
        positions,
        node_size=node_sizes,
        node_color=node_colors,
        alpha=0.9,
        linewidths=0.4,
        edgecolors="#ffffff",
    )
    nx.draw_networkx_labels(
        graph,
        positions,
        labels=labels,
        font_size=9,
        font_weight="bold",
    )

    plt.title("GitHub Developer Network", fontsize=16)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(PNG_OUTPUT_PATH, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved static visualization to {PNG_OUTPUT_PATH}")


def main() -> None:
    """Run Track A data collection, analysis, and visualization."""
    print("Starting Track A GitHub contributor data collection...")
    create_directories()
    contributors_df = collect_github_data()

    print("Building developer-developer edge list...")
    edge_list_df = build_edge_list(contributors_df)
    edge_list_df.to_csv(EDGE_LIST_PATH, index=False)
    print(f"Saved {len(edge_list_df)} edges to {EDGE_LIST_PATH}")

    print("Building developer node table...")
    node_table_df = build_node_table(contributors_df)
    node_table_df.to_csv(NODE_TABLE_PATH, index=False)
    print(f"Saved {len(node_table_df)} nodes to {NODE_TABLE_PATH}")

    print("Analyzing developer network...")
    edge_list_df = pd.read_csv(EDGE_LIST_PATH)
    node_table_df = pd.read_csv(NODE_TABLE_PATH)
    graph = create_graph(edge_list_df)
    analyzed_node_table_df = analyze_graph(graph, node_table_df)
    analyzed_node_table_df.to_csv(NODE_TABLE_PATH, index=False)
    print(f"Updated node analysis metrics in {NODE_TABLE_PATH}")
    print_network_summary(graph, analyzed_node_table_df)

    print("Creating Track A visualizations...")
    create_interactive_visualization(graph, analyzed_node_table_df)
    create_static_visualization(graph, analyzed_node_table_df)

    print("Track A data collection, network analysis, and visualization complete.")


if __name__ == "__main__":
    main()
