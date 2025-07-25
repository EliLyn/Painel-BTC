import requests
import pandas as pd

def get_long_short_ratio():
    url = "https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol=BTCUSDT&period=1h&limit=5"

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status() # Lança um erro para status HTTP 4xx/5xx
        data = r.json()

        if data:
            df = pd.DataFrame(data)

            # Seleciona as colunas relevantes e renomeia
            df = df[['timestamp', 'longShortRatio']].copy()
            df.columns = ['Timestamp', 'Long/Short Ratio']

            # --- CORREÇÃO AQUI: Garante que 'Long/Short Ratio' é um número (float) ---
            # Converte para numérico, erros se tornam NaN (Not a Number)
            df['Long/Short Ratio'] = pd.to_numeric(df['Long/Short Ratio'], errors='coerce')

            # Remove linhas onde a conversão falhou (se houver)
            df.dropna(subset=['Long/Short Ratio'], inplace=True)

            # Converte o timestamp para data/hora legível
            df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')

            return df
        else:
            print("Nenhum dado de Long/Short Ratio recebido da Binance.")
            return pd.DataFrame({"Erro": ["Sem dados de Long/Short Ratio."]})

    except requests.exceptions.RequestException as e:
        print(f"Erro de rede ao buscar Long/Short Ratio: {e}")
        return pd.DataFrame({"Erro": [f"Erro de rede: {e}"]})
    except Exception as e:
        print(f"Erro inesperado no scraper de Long/Short Ratio: {e}")
        return pd.DataFrame({"Erro": [f"Erro inesperado: {e}"]})