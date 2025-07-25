import requests
import pandas as pd

def get_open_interest():
    # URL da API openInterestHist da Binance Futures (período de 1 hora, últimos 5 dados)
    url = "https://fapi.binance.com/futures/data/openInterestHist?symbol=BTCUSDT&period=1h&limit=5"
    
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status() # Lança um erro para status HTTP 4xx/5xx
        data = r.json()
        
        if data:
            df = pd.DataFrame(data)
            
            # Seleciona as colunas relevantes e renomeia
            df = df[['timestamp', 'sumOpenInterest']].copy()
            df.columns = ['Timestamp', 'Open Interest (USD)']
            
            # --- CORREÇÃO AQUI: Garante que 'Open Interest (USD)' é um número (float) ---
            # Converte para numérico, erros se tornam NaN (Not a Number)
            df['Open Interest (USD)'] = pd.to_numeric(df['Open Interest (USD)'], errors='coerce')
            
            # Remove linhas onde a conversão falhou (se houver algum dado mal formatado)
            df.dropna(subset=['Open Interest (USD)'], inplace=True)

            # Converte o timestamp para data/hora legível
            df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
            
            return df
        else:
            print("Nenhum dado de Open Interest recebido da Binance.")
            return pd.DataFrame({"Erro": ["Sem dados de Open Interest."]})

    except requests.exceptions.RequestException as e:
        print(f"Erro de rede ao buscar Open Interest: {e}")
        return pd.DataFrame({"Erro": [f"Erro de rede: {e}"]})
    except Exception as e:
        print(f"Erro inesperado no scraper de Open Interest: {e}")
        return pd.DataFrame({"Erro": [f"Erro inesperado: {e}"]})