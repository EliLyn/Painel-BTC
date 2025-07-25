import pandas as pd
import requests

def get_etf_flows():
    url = "https://www.coinglass.com/ETF"
    try:
        # Aqui você faria scraping ou usaria uma API real se tiver.
        # Simulação para fins de exemplo:
        df = pd.DataFrame({
            "Data": pd.date_range(end=pd.Timestamp.today(), periods=5),
            "Fluxo": [500, -200, 300, -100, 400]
        })
        return df
    except Exception:
        return pd.DataFrame()
