import pandas as pd
import requests

def get_open_interest():
    try:
        url = "https://fapi.binance.com/futures/data/openInterestHist?symbol=BTCUSDT&period=5m&limit=20"
        r = requests.get(url)
        data = r.json()
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['sumOpenInterest'] = pd.to_numeric(df['sumOpenInterest'])
        return df[['timestamp', 'sumOpenInterest']]
    except Exception:
        return pd.DataFrame()
