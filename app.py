import streamlit as st
import requests
import openai
import os
from dotenv import load_dotenv
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import datetime

# --- Load Environment Variables ---
load_dotenv()
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# --- Helper: Fetch Stock Price from Finnhub ---
def get_stock_price(ticker):
    url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "current": data.get("c"),
            "high": data.get("h"),
            "low": data.get("l"),
            "open": data.get("o"),
            "prev_close": data.get("pc")
        }
    else:
        st.error(f"Finnhub API error: {response.status_code} - {response.text}")
        return None

# --- Helper: Fetch Historical Intraday Data ---
def get_intraday_data(ticker):
    now = int(datetime.datetime.now().timestamp())
    past = now - 3600 * 6  # last 6 hours
    url = f"https://finnhub.io/api/v1/stock/candle?symbol={ticker}&resolution=5&from={past}&to={now}&token={FINNHUB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['s'] != 'ok':
            
            return None
        df = pd.DataFrame({
            'timestamp': pd.to_datetime(data['t'], unit='s'),
            'price': data['c']
        })
        return df
    else:
        return None

# --- Helper: Generate GPT Summary ---
def generate_summary(ticker, price_data):
    prompt = (
        f"You are a financial analyst. Analyze the recent trend of {ticker} stock with the following data:\n"
        f"Current price: {price_data['current']}\n"
        f"Day high: {price_data['high']}\n"
        f"Day low: {price_data['low']}\n"
        f"Open price: {price_data['open']}\n"
        f"Previous close: {price_data['prev_close']}\n"
        f"Provide a short and simple summary of the stock trend."
    )

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful stock market analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating summary: {e}"

# --- Streamlit UI ---
st.set_page_config(page_title="Live Stock Viewer with GPT", layout="centered")
st.title("📈 Live Stock Price Tracker with GPT Summary")

ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, MSFT):", "AAPL")
update_interval = st.slider("Update interval (seconds):", 5, 60, 10)

# Autorefresh
st_autorefresh(interval=update_interval * 1000, key="refresh")

if not FINNHUB_API_KEY or not OPENAI_API_KEY:
    st.error("Missing API keys. Please check your .env file.")
elif ticker:
    price_slot = st.empty()
    summary_slot = st.empty()
    chart_slot = st.empty()

    price_data = get_stock_price(ticker)
    intraday_df = get_intraday_data(ticker)

    if price_data and price_data['current'] is not None:
        price_slot.markdown(
            f"### 📈 {ticker.upper()} Price: ${price_data['current']:.2f}"
            f"\n- Open: ${price_data['open']:.2f}"
            f"\n- High: ${price_data['high']:.2f}"
            f"\n- Low: ${price_data['low']:.2f}"
            f"\n- Prev Close: ${price_data['prev_close']:.2f}"
        )

        if intraday_df is not None:
            chart_slot.line_chart(intraday_df.set_index("timestamp"))
        else:
            chart_slot.warning("Intraday price data unavailable.")

        summary = generate_summary(ticker, price_data)
        summary_slot.info(summary)
    else:
        price_slot.error("Failed to fetch stock data. Check the ticker symbol or your Finnhub API key.")
        summary_slot.empty()
        chart_slot.empty()
