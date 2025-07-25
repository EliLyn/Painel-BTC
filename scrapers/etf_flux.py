import requests
import pandas as pd
from bs4 import BeautifulSoup
import re # Importa a biblioteca de expressões regulares

def get_etf_flows():
    url = "https://farside.co.uk/?p=997"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20) # Aumentei o timeout para 20 segundos
        response.raise_for_status() # Levanta um erro para respostas HTTP ruins (4xx ou 5xx)
        
        soup = BeautifulSoup(response.text, "lxml")
        
        # Encontra a tabela principal de fluxos de ETF usando a classe 'etf'
        table = soup.find("table", class_="etf") 
        
        if table:
            # pandas.read_html é excelente para extrair tabelas HTML para DataFrames
            # Ele retorna uma lista de DataFrames, geralmente o que queremos é o primeiro [0]
            df = pd.read_html(str(table))[0] 
            
            # A tabela da Farside tem 3 linhas de cabeçalho/metadados que não são dados diários.
            # Os dados reais começam a partir da 4ª linha (índice 3 em Python)
            if len(df) > 3: # Garante que há pelo menos 4 linhas na tabela
                df = df.iloc[3:].copy() # Pega os dados a partir da 4ª linha
                
                # Vamos renomear a primeira coluna para 'Data' para facilitar o uso
                df.rename(columns={df.columns[0]: 'Data'}, inplace=True)

                # Limpeza e conversão das colunas numéricas
                for col in df.columns:
                    if col == 'Data': # Ignora a coluna de data, ela não é numérica
                        continue
                    
                    # Converte para string e remove parênteses '()', vírgulas ',' e sinais de dólar '$'
                    # O re.sub é mais robusto para expressões regulares
                    df[col] = df[col].astype(str).apply(lambda x: re.sub(r'[(),$]', '', x))
                    
                    # Tenta converter para numérico. Se houver erro (por exemplo, texto), coloca NaN
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # Removendo colunas que possam ter vindo vazias ou indesejadas
                # df.dropna(axis=1, how='all', inplace=True) # Remove colunas onde TODOS os valores são NaN
                
                # O site Farside já costuma listar as datas mais recentes primeiro.
                # Vamos pegar as 7 primeiras linhas (7 dias mais recentes de dados)
                return df.head(7) 
            else:
                print("AVISO: Tabela de ETFs encontrada, mas contém menos de 4 linhas de dados esperadas.")
                return pd.DataFrame({"Erro": ["Dados de ETF insuficientes ou formato alterado."]})

        else:
            print("ERRO: A tabela de fluxos de ETF com a classe 'etf' não foi encontrada na página.")
            return pd.DataFrame({"Erro": ["Tabela de ETFs não encontrada. Seletor 'etf' pode estar incorreto ou HTML mudou."]})

    except requests.exceptions.RequestException as e:
        print(f"ERRO DE CONEXÃO: Não foi possível acessar a URL da Farside Investors. Verifique sua conexão ou a URL. Detalhes: {e}")
        return pd.DataFrame({"Status": [f"Erro de Conexão: {e}"]})
    except IndexError:
        print("ERRO DE ESTRUTURA: A função read_html não conseguiu extrair dados de tabela. A estrutura da página da Farside pode ter mudado.")
        return pd.DataFrame({"Status": ["Erro de Estrutura: A tabela pode ter mudado no site."]})
    except Exception as e:
        print(f"ERRO INESPERADO: Ocorreu um erro desconhecido ao processar os dados da Farside. Detalhes: {e}")
        return pd.DataFrame({"Status": [f"Erro Inesperado: {e}"]})