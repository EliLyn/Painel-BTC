import pandas as pd
import requests

def get_long_short_ratio():
    try:
        url = "https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol=BTCUSDT&period=5m&limit=20"
        r = requests.get(url)
        data = r.json()
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['long'] = df['longAccount']
        df['short'] = df['shortAccount']
        return df[['timestamp', 'long', 'short']]
    except Exception:
        return pd.DataFrame()
