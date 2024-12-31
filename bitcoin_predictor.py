from flask import Flask, request, jsonify, render_template
import requests
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime, timedelta
import os
import pickle

app = Flask(__name__)
CACHE_FILE = "coin_list_cache.pkl"
CACHE_EXPIRATION_HOURS = 24

def fetch_live_data(coin="bitcoin"):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "30",
        "interval": "daily"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception("Failed to fetch data. Please check the coin name.")
    data = response.json()
    prices = data["prices"]
    return pd.DataFrame(prices, columns=["timestamp", "price"])

def predict_price(data, target_date):
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data['day'] = (data['timestamp'] - data['timestamp'].min()).dt.days
    X = data[['day']]
    y = data['price']
    model = LinearRegression()
    model.fit(X, y)

    target_day = (target_date - data['timestamp'].min()).days
    future_day = np.array([[target_day]])
    return model.predict(future_day)[0]

def get_all_coins():
    # Check if cache exists and is valid
    if os.path.exists(CACHE_FILE):
        cache_mtime = datetime.fromtimestamp(os.path.getmtime(CACHE_FILE))
        if datetime.now() - cache_mtime < timedelta(hours=CACHE_EXPIRATION_HOURS):
            with open(CACHE_FILE, "rb") as f:
                return pickle.load(f)

    # Fetch and cache the data
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    data = response.json()
    coin_list = [{"id": coin["id"], "name": coin["name"]} for coin in data]
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(coin_list, f)
    return coin_list

@app.route('/')
def index():
    coins = get_all_coins()
    return render_template('index.html', coins=coins)

@app.route('/predict', methods=['POST'])
def predict():
    coin = request.form['coin']
    target_date = request.form['date']

    try:
        target_date = datetime.strptime(target_date, "%Y-%m-%d")
        data = fetch_live_data(coin)
        data.columns = ["timestamp", "price"]
        predicted_price = predict_price(data, target_date)

        # Generate the graph
        plt.figure(figsize=(10, 6))
        plt.plot(data['timestamp'], data['price'], label='Actual Price')
        plt.axvline(x=target_date, color='r', linestyle='--', label=f'Predicted Price: ${predicted_price:.2f}')
        plt.annotate(f'Predicted: ${predicted_price:.2f}', xy=(target_date, predicted_price),
                     xytext=(target_date + timedelta(days=1), predicted_price),
                     arrowprops=dict(facecolor='black', arrowstyle='->'))
        plt.legend()
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.title(f'{coin.capitalize()} Price Prediction')

        # Save graph to a string
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        image = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()

        return jsonify({"predicted_price": predicted_price, "graph": image})
    except ValueError:
        return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD."})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
