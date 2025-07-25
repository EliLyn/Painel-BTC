import requests
import pandas as pd
from datetime import datetime

def get_long_short_ratio():
    url = "https://fapi.coinglass.com/api/futures/longShortChart?symbol=BTC&type=binance"
    headers = {
        "accept": "application/json",
        "coinglassSecret": "glassnode-free"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return pd.DataFrame()

    data = response.json()
    if not data.get("data"):
        return pd.DataFrame()

    longs = data["data"].get("longAccount", [])
    shorts = data["data"].get("shortAccount", [])
    timestamps = data["data"].get("timestamp", [])

    if not (longs and shorts and timestamps):
        return pd.DataFrame()

    df = pd.DataFrame({
        "timestamp": [datetime.fromtimestamp(ts / 1000) for ts in timestamps],
        "long": longs,
        "short": shorts
    })
    return df
