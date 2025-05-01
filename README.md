# 📈 Live Stock Price Tracker with GPT Summary

This is a Streamlit-based web application that displays live stock prices using the Finnhub API and provides real-time sentiment analysis powered by OpenAI's GPT.

## 🔧 Features

- Live stock ticker price tracking (AAPL, MSFT, etc.)
- Auto-refreshing data at user-defined intervals
- Intraday price trend chart (last 6 hours, 5-min resolution)
- GPT-generated financial summaries of the stock's status

## 🧰 Requirements

- Python 3.8+
- Streamlit
- OpenAI API Key
- Finnhub API Key

## 🚀 Getting Started

1. **Clone the repository**
```bash
git clone https://github.com/your-username/stock-gpt-dashboard.git
cd stock-gpt-dashboard
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file with the following content:
```
FINNHUB_API_KEY=your_finnhub_api_key
OPENAI_API_KEY=your_openai_api_key
```

5. **Run the app**
```bash
streamlit run app.py
```

## 📦 APIs Used

- [Finnhub API](https://finnhub.io/)
- [OpenAI API](https://platform.openai.com/account/api-keys)

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
