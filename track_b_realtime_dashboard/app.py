"""Track B: Real-time cryptocurrency monitoring dashboard."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from streamlit_autorefresh import st_autorefresh


COINS = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "solana": "SOL",
}
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
CURRENCY = "usd"
# Polling every 30 seconds reduces CoinGecko rate-limit risk while remaining
# frequent enough for a student real-time dashboard.
REFRESH_INTERVAL_MS = 30_000
# Keep about 15 minutes of data per coin: 30 points * 30 seconds.
MAX_DATA_POINTS_PER_COIN = 30
BTC_ALERT_DROP_THRESHOLD = -2.0
BTC_ALERT_LOOKBACK_MINUTES = 5
# With 30-second polling, 10 intervals is approximately 5 minutes.
BTC_ALERT_LOOKBACK_POINTS = 10

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "track_b_realtime_dashboard" / "data"
LIVE_DATA_PATH = DATA_DIR / "live_crypto_data.csv"


def create_data_directory() -> None:
    """Ensure the dashboard data directory exists before writing CSV data."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def fetch_live_prices() -> tuple[dict[str, float], str | None]:
    """Fetch current crypto prices from the CoinGecko simple price API."""
    headers = {"User-Agent": "data-visualization-final-project"}

    try:
        response = requests.get(
            COINGECKO_URL,
            headers=headers,
            params={"ids": ",".join(COINS.keys()), "vs_currencies": CURRENCY},
            timeout=15,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.exceptions.HTTPError as error:
        if error.response is not None and error.response.status_code == 429:
            return (
                {},
                "CoinGecko API rate limit reached; showing cached data.",
            )
        return {}, f"CoinGecko API request failed; showing cached data. {error}"
    except requests.exceptions.RequestException as error:
        return {}, f"CoinGecko API request failed; showing cached data. {error}"
    except ValueError as error:
        return {}, f"CoinGecko returned invalid JSON; showing cached data. {error}"

    prices: dict[str, float] = {}
    for coin_id, symbol in COINS.items():
        price = payload.get(coin_id, {}).get(CURRENCY)
        if price is None:
            return {}, f"CoinGecko response is missing {symbol} price data."

        prices[symbol] = float(price)

    return prices, None


def load_recent_data() -> pd.DataFrame:
    """Load recent observations from CSV if available."""
    if not LIVE_DATA_PATH.exists():
        return create_empty_data_frame()

    try:
        data = pd.read_csv(LIVE_DATA_PATH, parse_dates=["timestamp"])
    except (OSError, ValueError, pd.errors.ParserError):
        return create_empty_data_frame()

    return normalize_recent_data(data)


def create_empty_data_frame() -> pd.DataFrame:
    """Create the expected dashboard data structure."""
    return pd.DataFrame(columns=["timestamp", "coin", "symbol", "price_usd"])


def normalize_recent_data(data: pd.DataFrame) -> pd.DataFrame:
    """Keep expected columns and trim to the latest observations per coin."""
    expected_columns = ["timestamp", "coin", "symbol", "price_usd"]
    if data.empty:
        return create_empty_data_frame()

    normalized = data.reindex(columns=expected_columns)
    normalized["timestamp"] = pd.to_datetime(normalized["timestamp"], errors="coerce")
    normalized["price_usd"] = pd.to_numeric(normalized["price_usd"], errors="coerce")
    normalized = normalized.dropna(subset=["timestamp", "coin", "symbol", "price_usd"])

    return (
        normalized.sort_values("timestamp")
        .groupby("symbol", group_keys=False)
        .tail(MAX_DATA_POINTS_PER_COIN)
    )


def append_observation(
    recent_data: pd.DataFrame,
    prices: dict[str, float],
    timestamp: datetime,
) -> pd.DataFrame:
    """Append the latest price snapshot and keep a sliding window."""
    new_rows = [
        {
            "timestamp": timestamp,
            "coin": coin_id,
            "symbol": symbol,
            "price_usd": prices[symbol],
        }
        for coin_id, symbol in COINS.items()
    ]

    updated_data = pd.concat(
        [recent_data, pd.DataFrame(new_rows)],
        ignore_index=True,
    )

    return normalize_recent_data(updated_data)


def save_recent_data(recent_data: pd.DataFrame) -> None:
    """Persist the latest sliding window to CSV for continuity between refreshes."""
    recent_data.to_csv(LIVE_DATA_PATH, index=False)


def get_latest_prices(recent_data: pd.DataFrame) -> dict[str, float]:
    """Return the newest available price for each tracked cryptocurrency."""
    if recent_data.empty:
        return {}

    latest_rows = recent_data.sort_values("timestamp").groupby("symbol").tail(1)
    return dict(zip(latest_rows["symbol"], latest_rows["price_usd"], strict=False))


def get_btc_drop_percent(recent_data: pd.DataFrame) -> float | None:
    """Compare current BTC price to the observation about five minutes ago."""
    btc_data = recent_data[recent_data["symbol"] == "BTC"].sort_values("timestamp")
    if len(btc_data) <= BTC_ALERT_LOOKBACK_POINTS:
        return None

    current_row = btc_data.iloc[-1]
    previous_row = btc_data.iloc[-(BTC_ALERT_LOOKBACK_POINTS + 1)]
    previous_price = float(previous_row["price_usd"])
    current_price = float(current_row["price_usd"])
    if previous_price == 0:
        return None

    return ((current_price - previous_price) / previous_price) * 100


def get_display_timestamp(recent_data: pd.DataFrame, fallback_timestamp: datetime) -> datetime:
    """Use cached data time when API polling fails so freshness stays honest."""
    if recent_data.empty:
        return fallback_timestamp

    latest_timestamp = recent_data["timestamp"].max()
    if pd.isna(latest_timestamp):
        return fallback_timestamp

    return latest_timestamp.to_pydatetime()


def render_status(
    connection_status: str,
    error_message: str | None,
    timestamp: datetime,
) -> None:
    """Render connection status and last update information."""
    status_column, time_column = st.columns(2)

    with status_column:
        if connection_status == "live":
            st.success("Connection status: Live")
        else:
            # Cached data keeps the dashboard usable when CoinGecko rate limits
            # or temporary API failures prevent a fresh observation.
            st.warning("Connection status: Using cached data")
            if error_message:
                st.caption(error_message)

    with time_column:
        st.info(f"Last updated: {timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}")


def render_price_metrics(latest_prices: dict[str, float]) -> None:
    """Render BTC, ETH, and SOL price metric cards."""
    metric_columns = st.columns(len(COINS))

    for column, symbol in zip(metric_columns, COINS.values(), strict=False):
        price = latest_prices.get(symbol)
        value = f"${price:,.2f}" if price is not None else "No data"

        with column:
            st.metric(label=f"{symbol} Price", value=value)


def render_price_chart(recent_data: pd.DataFrame) -> None:
    """Render a rolling Plotly line chart for the sliding data window."""
    if recent_data.empty:
        st.warning("Waiting for live price data...")
        return

    normalized_data = calculate_percentage_change(recent_data)
    if normalized_data.empty:
        st.warning("Waiting for enough valid price data to draw the chart...")
        return

    chart = px.line(
        normalized_data,
        x="timestamp",
        y="percentage_change",
        color="symbol",
        title="Rolling Crypto Price Change (%)",
        color_discrete_map={
            "BTC": "#4c78a8",
            "ETH": "#72b7b2",
            "SOL": "#59a14f",
        },
        labels={
            "timestamp": "Time",
            "percentage_change": "Change from window start (%)",
            "symbol": "Coin",
        },
    )
    chart.update_layout(
        template="plotly_white",
        height=430,
        margin={"l": 20, "r": 20, "t": 30, "b": 20},
        legend_title_text="",
    )

    st.plotly_chart(chart, use_container_width=True)


def calculate_percentage_change(recent_data: pd.DataFrame) -> pd.DataFrame:
    """Normalize prices so BTC, ETH, and SOL can be compared on one chart."""
    # Raw USD values make ETH and SOL appear almost flat next to BTC. Percentage
    # change uses each coin's first visible value as the baseline.
    normalized = recent_data.sort_values(["symbol", "timestamp"]).copy()
    normalized["baseline_price"] = normalized.groupby("symbol")[
        "price_usd"
    ].transform("first")
    normalized = normalized[normalized["baseline_price"] != 0].copy()
    normalized["percentage_change"] = (
        (normalized["price_usd"] - normalized["baseline_price"])
        / normalized["baseline_price"]
    ) * 100

    return normalized.drop(columns=["baseline_price"]).sort_values("timestamp")


def render_btc_alert(recent_data: pd.DataFrame) -> None:
    """Show a strong warning only when BTC drops more than 2% in about 5 minutes."""
    btc_drop_percent = get_btc_drop_percent(recent_data)

    if btc_drop_percent is None:
        st.caption("BTC alert status: collecting enough history for 5-minute check.")
        return

    if btc_drop_percent <= BTC_ALERT_DROP_THRESHOLD:
        st.error(
            "BTC warning: price dropped "
            f"{abs(btc_drop_percent):.2f}% compared to approximately "
            f"{BTC_ALERT_LOOKBACK_MINUTES} minutes ago."
        )
    else:
        st.caption(
            "BTC alert status: normal "
            f"({btc_drop_percent:+.2f}% over approximately "
            f"{BTC_ALERT_LOOKBACK_MINUTES} minutes)."
        )


def update_live_data() -> tuple[pd.DataFrame, str, str | None, datetime]:
    """Fetch, append, trim, and persist the latest live crypto observations."""
    create_data_directory()
    recent_data = load_recent_data()
    timestamp = datetime.now(timezone.utc)
    prices, error_message = fetch_live_prices()

    if prices:
        recent_data = append_observation(recent_data, prices, timestamp)
        save_recent_data(recent_data)
        return recent_data, "live", None, timestamp

    # On API failure, keep and display the existing CSV-backed data instead of
    # deleting history or crashing the dashboard.
    cached_timestamp = get_display_timestamp(recent_data, timestamp)
    return recent_data, "cached", error_message, cached_timestamp


def main() -> None:
    """Render the Streamlit real-time crypto monitoring dashboard."""
    st.set_page_config(page_title="Crypto Real-Time Dashboard", layout="wide")
    st_autorefresh(interval=REFRESH_INTERVAL_MS, key="crypto_dashboard_refresh")

    st.title("Real-Time Crypto Monitoring Dashboard")
    st.write(
        "Live USD prices for Bitcoin, Ethereum, and Solana from the free "
        "CoinGecko REST simple price API. The dashboard polls every 30 seconds "
        "to reduce rate-limit risk and keeps about 15 minutes of recent data."
    )

    recent_data, connection_status, error_message, timestamp = update_live_data()
    latest_prices = get_latest_prices(recent_data)

    render_status(connection_status, error_message, timestamp)
    render_price_metrics(latest_prices)
    render_btc_alert(recent_data)
    render_price_chart(recent_data)


if __name__ == "__main__":
    main()
