import streamlit as st
import pandas as pd
from scrapers.etf_flux import get_etf_flows
from scrapers.long_short import get_long_short_ratio
from scrapers.open_interest import get_open_interest

st.set_page_config(page_title="Painel BTC Institucional", layout="wide")
st.title("📊 Painel BTC Institucional – Dados em Tempo Real")

# Adiciona um botão de atualização
if st.button("🔄 Atualizar Dados"):
    st.cache_data.clear() # Limpa o cache para buscar dados novos
    st.rerun() # Reinicia a aplicação para recarregar os dados

st.write("---") # Linha divisória

# --- Colunas para organização dos dados ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🚰 Fluxo de ETFs (USD$m)")
    # Chama a função de scraping do ETF
    etf_df = get_etf_flows()
    if not etf_df.empty:
        st.dataframe(etf_df, use_container_width=True)
    else:
        st.warning("Não foi possível carregar os dados de Fluxo de ETFs. Tente atualizar.")

with col2:
    st.subheader("📊 Long/Short Ratio (Binance Futures)")
    # Chama a função de Long/Short
    long_short_df = get_long_short_ratio()
    if not long_short_df.empty:
        # Exibe o valor mais recente ou um resumo
        st.metric(label="Ratio Atual", value=f"{long_short_df['Long/Short Ratio'].iloc[-1]:.2f}")
        st.dataframe(long_short_df, use_container_width=True)
    else:
        st.warning("Não foi possível carregar os dados de Long/Short Ratio. Tente atualizar.")

with col3:
    st.subheader("📈 Open Interest (Binance Futures)")
    # Chama a função de Open Interest
    oi_df = get_open_interest()
    if not oi_df.empty:
        # Exibe o valor mais recente ou um resumo
        st.metric(label="OI BTC (USD)", value=f"${oi_df['Open Interest (USD)'].iloc[-1]:,.2f}")
        st.dataframe(oi_df, use_container_width=True)
    else:
        st.warning("Não foi possível carregar os dados de Open Interest. Tente atualizar.")

st.write("---") # Linha divisória
st.info("Dados de scraping e APIs públicas. Podem ocorrer falhas de conexão ou mudanças nas fontes.")