import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import ta

def get_news_sentiment(company_name, ticker):
    try:
        query = company_name.replace(" ", "+")
        url = f"https://news.google.com/rss/search?q={query}+stock+NSE&hl=en-IN&gl=IN&ceid=IN:en"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "xml")
        items = soup.find_all("item")[:10]
        headlines = []
        positive_words = ["growth", "profit", "surge", "rally", "gain", "beat", "record", "strong", "upgrade", "buy", "bullish", "expansion", "wins", "order", "contract", "dividend"]
        negative_words = ["loss", "decline", "fall", "drop", "miss", "weak", "downgrade", "sell", "bearish", "fraud", "probe", "penalty", "cut", "layoff", "debt", "crisis"]
        pos_count = 0
        neg_count = 0
        for item in items:
            title = item.find("title")
            if title:
                text = title.text.lower()
                headlines.append(title.text)
                pos_count += sum(1 for w in positive_words if w in text)
                neg_count += sum(1 for w in negative_words if w in text)
        total = pos_count + neg_count
        if total == 0:
            sentiment_score = 0.5
        else:
            sentiment_score = pos_count / total
        sentiment_label = "Bullish" if sentiment_score > 0.6 else "Bearish" if sentiment_score < 0.4 else "Neutral"
        return {
            "headlines": headlines[:5],
            "sentiment_score": round(sentiment_score, 2),
            "sentiment_label": sentiment_label,
            "positive_signals": pos_count,
            "negative_signals": neg_count,
        }
    except:
        return {
            "headlines": [],
            "sentiment_score": 0.5,
            "sentiment_label": "Neutral",
            "positive_signals": 0,
            "negative_signals": 0,
        }

def get_technical_indicators(hist):
    df = hist.copy()
    df["RSI"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()
    macd = ta.trend.MACD(df["Close"])
    df["MACD"] = macd.macd()
    df["MACD_signal"] = macd.macd_signal()
    df["MACD_hist"] = macd.macd_diff()
    bb = ta.volatility.BollingerBands(df["Close"], window=20)
    df["BB_upper"] = bb.bollinger_hband()
    df["BB_lower"] = bb.bollinger_lband()
    df["BB_mid"] = bb.bollinger_mavg()
    df["BB_pct"] = bb.bollinger_pband()
    df["EMA20"] = ta.trend.EMAIndicator(df["Close"], window=20).ema_indicator()
    df["EMA50"] = ta.trend.EMAIndicator(df["Close"], window=50).ema_indicator()
    df["EMA200"] = ta.trend.EMAIndicator(df["Close"], window=200).ema_indicator()
    df["ATR"] = ta.volatility.AverageTrueRange(df["High"], df["Low"], df["Close"]).average_true_range()
    df["OBV"] = ta.volume.OnBalanceVolumeIndicator(df["Close"], df["Volume"]).on_balance_volume()
    return df

def detect_candlestick_patterns(df):
    patterns = []
    last = df.iloc[-1]
    prev = df.iloc[-2]
    prev2 = df.iloc[-3]
    body = abs(last["Close"] - last["Open"])
    upper_shadow = last["High"] - max(last["Close"], last["Open"])
    lower_shadow = min(last["Close"], last["Open"]) - last["Low"]
    total_range = last["High"] - last["Low"]
    if total_range > 0:
        if body / total_range < 0.1:
            patterns.append(("Doji", "neutral", "Market indecision — possible reversal"))
        if lower_shadow > 2 * body and upper_shadow < body:
            if last["Close"] < last["Open"]:
                patterns.append(("Hammer", "bullish", "Potential bullish reversal"))
        if upper_shadow > 2 * body and lower_shadow < body:
            patterns.append(("Shooting Star", "bearish", "Potential bearish reversal"))
    if prev["Close"] < prev["Open"] and last["Close"] > last["Open"]:
        if last["Open"] < prev["Close"] and last["Close"] > prev["Open"]:
            patterns.append(("Bullish Engulfing", "bullish", "Strong bullish reversal signal"))
    if prev["Close"] > prev["Open"] and last["Close"] < last["Open"]:
        if last["Open"] > prev["Close"] and last["Close"] < prev["Open"]:
            patterns.append(("Bearish Engulfing", "bearish", "Strong bearish reversal signal"))
    if (prev2["Close"] > prev2["Open"] and
        prev["Close"] > prev["Open"] and
        last["Close"] > last["Open"]):
        patterns.append(("Three White Soldiers", "bullish", "Strong upward momentum"))
    if (prev2["Close"] < prev2["Open"] and
        prev["Close"] < prev["Open"] and
        last["Close"] < last["Open"]):
        patterns.append(("Three Black Crows", "bearish", "Strong downward momentum"))
    return patterns

def predict_stock_price(ticker, company_name, months=1):
    try:
        days = months * 21
        t = yf.Ticker(ticker)
        hist = t.history(period="2y")
        if hist.empty or len(hist) < 100:
            return None
        df = get_technical_indicators(hist)
        df = df.dropna()
        news = get_news_sentiment(company_name, ticker)
        patterns = detect_candlestick_patterns(df)
        sentiment_multiplier = 1 + (news["sentiment_score"] - 0.5) * 0.1
        df["Returns"] = df["Close"].pct_change()
        df["Volatility"] = df["Returns"].rolling(20).std()
        df["Day"] = np.arange(len(df))
        features = ["Day", "RSI", "MACD", "BB_pct", "ATR"]
        df_feat = df[features + ["Close"]].dropna()
        X = df_feat[features].values
        y = df_feat["Close"].values
        scaler_X = MinMaxScaler()
        scaler_y = MinMaxScaler()
        X_scaled = scaler_X.fit_transform(X)
        y_scaled = scaler_y.fit_transform(y.reshape(-1, 1)).ravel()
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_scaled, y_scaled)
        score = model.score(X_scaled, y_scaled)
        last_row = df_feat.iloc[-1]
        last_price = last_row["Close"]
        volatility = df["Volatility"].dropna().iloc[-1]
        future_prices = []
        future_upper = []
        future_lower = []
        current_day = last_row["Day"]
        current_rsi = last_row["RSI"]
        current_macd = last_row["MACD"]
        current_bb = last_row["BB_pct"]
        current_atr = last_row["ATR"]
        for i in range(1, days + 1):
            feat = scaler_X.transform([[current_day + i, current_rsi, current_macd, current_bb, current_atr]])
            pred_scaled = model.predict(feat)[0]
            pred = scaler_y.inverse_transform([[pred_scaled]])[0][0]
            pred = pred * sentiment_multiplier
            uncertainty = last_price * volatility * np.sqrt(i) * 2
            future_prices.append(round(pred, 2))
            future_upper.append(round(pred + uncertainty, 2))
            future_lower.append(round(max(pred - uncertainty, 0), 2))
        last_date = df.index[-1]
        future_dates = pd.date_range(start=last_date, periods=days + 1, freq="B")[1:]
        rsi_signal = "Overbought" if df["RSI"].iloc[-1] > 70 else "Oversold" if df["RSI"].iloc[-1] < 30 else "Neutral"
        macd_signal = "Bullish" if df["MACD"].iloc[-1] > df["MACD_signal"].iloc[-1] else "Bearish"
        bb_signal = "Overbought" if df["BB_pct"].iloc[-1] > 0.8 else "Oversold" if df["BB_pct"].iloc[-1] < 0.2 else "Neutral"
        trend = "Uptrend" if df["EMA20"].iloc[-1] > df["EMA50"].iloc[-1] else "Downtrend"
        bullish_signals = sum([
            macd_signal == "Bullish",
            rsi_signal == "Oversold",
            bb_signal == "Oversold",
            trend == "Uptrend",
            news["sentiment_label"] == "Bullish",
            any(p[1] == "bullish" for p in patterns),
        ])
        bearish_signals = sum([
            macd_signal == "Bearish",
            rsi_signal == "Overbought",
            bb_signal == "Overbought",
            trend == "Downtrend",
            news["sentiment_label"] == "Bearish",
            any(p[1] == "bearish" for p in patterns),
        ])
        overall = "Bullish" if bullish_signals > bearish_signals else "Bearish" if bearish_signals > bullish_signals else "Neutral"
        return {
            "historical_dates": df.index.tolist()[-180:],
            "historical_prices": df["Close"].tolist()[-180:],
            "future_dates": future_dates.tolist(),
            "future_prices": future_prices,
            "future_upper": future_upper,
            "future_lower": future_lower,
            "last_price": round(last_price, 2),
            "predicted_price": round(future_prices[-1], 2),
            "change_pct": round((future_prices[-1] - last_price) / last_price * 100, 2),
            "volatility": round(volatility * 100, 2),
            "model_score": round(score * 100, 2),
            "rsi": round(last_row["RSI"], 1),
            "rsi_signal": rsi_signal,
            "macd_signal": macd_signal,
            "bb_signal": bb_signal,
            "trend": trend,
            "overall_signal": overall,
            "bullish_signals": bullish_signals,
            "bearish_signals": bearish_signals,
            "patterns": patterns,
            "news": news,
            "sentiment_multiplier": sentiment_multiplier,
            "bb_upper": round(df["BB_upper"].iloc[-1], 2),
            "bb_lower": round(df["BB_lower"].iloc[-1], 2),
            "ema20": round(df["EMA20"].iloc[-1], 2),
            "ema50": round(df["EMA50"].iloc[-1], 2),
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return None
