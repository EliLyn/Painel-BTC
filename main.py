import streamlit as st
from scrapers.etf_flux import get_etf_flows
from scrapers.long_short_ratio import get_long_short_ratio
from scrapers.open_interest import get_open_interest

st.set_page_config(page_title="Painel BTC Institucional", layout="wide")

st.title("📊 Painel BTC Institucional – Dados em Tempo Real")

# Seção 1 – Fluxo de ETFs
st.header("🚰 Fluxo de ETFs (USD$m)")
etf_df = get_etf_flows()
st.dataframe(etf_df, use_container_width=True)

# Seção 2 – Long/Short Ratio
st.header("📊 Long/Short Ratio (Binance Futures)")
long_short_df = get_long_short_ratio()

if 'long' in long_short_df.columns and 'short' in long_short_df.columns:
    long_short_df['Long/Short Ratio'] = long_short_df['long'] / long_short_df['short']
    st.metric(label="Ratio Atual", value=f"{long_short_df['Long/Short Ratio'].iloc[-1]:.2f}")
    st.line_chart(long_short_df['Long/Short Ratio'])
else:
    st.error("❌ Dados de long/short ratio ausentes ou inválidos.")

# Seção 3 – Open Interest
st.header("💰 Open Interest (BTC Perp – Binance)")
oi_df = get_open_interest()
st.dataframe(oi_df, use_container_width=True)
