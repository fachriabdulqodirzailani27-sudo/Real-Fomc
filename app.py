import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="FOMC & XAUUSD Real-Time Engine", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #030712; color: #f8fafc; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 FOMC & XAUUSD Real-Time Macro Engine")
st.markdown("Mengambil data pasar keuangan global secara **100% real-time** untuk acuan analisis trading Anda.")

if st.button("🔄 Sinkronkan Data Live Sekarang", type="primary"):
    st.rerun()

try:
    with st.spinner('Menghubungkan ke server pasar global...'):
        tnx = yf.Ticker("^TNX")
        dxy = yf.Ticker("DX-Y.NYB")
        gold = yf.Ticker("GC=F")

        tnx_df = tnx.history(period="5d")
        dxy_df = dxy.history(period="5d")
        gold_df = gold.history(period="5d")

        tnx_price = tnx_df['Close'].iloc[-1]
        tnx_prev = tnx_df['Close'].iloc[-2]
        tnx_change = ((tnx_price - tnx_prev) / tnx_prev) * 100

        dxy_price = dxy_df['Close'].iloc[-1]
        dxy_prev = dxy_df['Close'].iloc[-2]
        dxy_change = ((dxy_price - dxy_prev) / dxy_prev) * 100

        gold_price = gold_df['Close'].iloc[-1]
        gold_prev = gold_df['Close'].iloc[-2]
        gold_change = ((gold_price - gold_prev) / gold_prev) * 100

    st.subheader("Indikator Penggerak Utama XAUUSD (Live Market)")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="10Y Treasury Yield (^TNX)",
            value=f"{tnx_price:.3f}%",
            delta=f"{tnx_change:.2f}%"
        )

    with col2:
        st.metric(
            label="US Dollar Index (DXY)",
            value=f"{dxy_price:.2f}",
            delta=f"{dxy_change:.2f}%"
        )

    with col3:
        st.metric(
            label="Gold Spot (XAUUSD)",
            value=f"${gold_price:.2f}",
            delta=f"{gold_change:.2f}%"
        )

    st.markdown("---")
    st.subheader("🤖 Analisis Sentimen & Proyeksi Pasar")
    
    if tnx_change > 0 and dxy_change > 0:
        bias = "Strong Bearish untuk XAUUSD (Yield & DXY Menguat)"
        color = "red"
    elif tnx_change < 0 and dxy_change < 0:
        bias = "Strong Bullish untuk XAUUSD (Yield & DXY Melemah)"
        color = "green"
    else:
        bias = "Neutral / Konsolidasi (Pergerakan Market Mixed)"
        color = "orange"

    st.markdown(f"**Market Bias Saat Ini:** :{color}[{bias}]")
    st.info("Catatan: Data ditarik langsung secara real-time dari feed global dan diperbarui setiap kali Anda menyegarkan halaman.")

except Exception as e:
    st.error(f"Gagal mengambil data live: {e}")
