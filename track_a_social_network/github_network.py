"""Collect contributor data for Track A: Social Network Visualization.

This stage only collects and saves raw contributor data. Graph construction
and visualization will be implemented later.
"""

from __future__ import annotations

import os
import time
from pathlib import Path

import pandas as pd
import requests


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

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TRACK_A_DIR = PROJECT_ROOT / "track_a_social_network"
DATA_DIR = TRACK_A_DIR / "data"
OUTPUTS_DIR = TRACK_A_DIR / "outputs"
RAW_CONTRIBUTORS_PATH = DATA_DIR / "raw_contributors.csv"


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


def main() -> None:
    """Run the Track A data collection workflow."""
    print("Starting Track A GitHub contributor data collection...")
    create_directories()
    collect_github_data()
    print("Track A data collection complete.")


if __name__ == "__main__":
    main()
