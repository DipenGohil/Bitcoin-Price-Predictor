# Bitcoin Price Prediction Web Application

This project is a Python-based web application that predicts Bitcoin (or other cryptocurrency) prices for a specified date using historical data. It includes a simple UI for selecting coins and dates, and displays the prediction along with a graph of actual and predicted prices.

## Features
- **Dropdown Menu**: Select from a list of all available cryptocurrencies (powered by CoinGecko).
- **Date Picker**: Choose a specific date for prediction.
- **Dynamic Graphs**: View the predicted price on a graph alongside historical data.
- **RESTful Backend**: Fetch live cryptocurrency data and predict future prices using machine learning.

## Tech Stack
- **Frontend**: HTML, CSS (Bootstrap), JavaScript.
- **Backend**: Python (Flask).
- **Machine Learning**: Linear Regression using Scikit-learn.
- **Data Source**: [CoinGecko API](https://www.coingecko.com/en/api).

## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/bitcoin-price-prediction.git
   cd bitcoin-price-prediction
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Run the Application**:
   ```bash
   python bitcoin_predictor.py
   ```

4. **Access the Web App**:
   Open your browser and navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## File Structure
```
.
├── bitcoin_predictor.py                # Flask backend application
├── templates
│   └── index.html       # Frontend template
├── README.md            # Project documentation
├── coin_list_cache.pkl  # Cached coin list (auto-generated)
```

## Usage
1. Open the app in your browser.
2. Select a cryptocurrency from the dropdown menu.
3. Choose a target date using the calendar input.
4. Click "Predict" to view the predicted price and graph.

## Future Enhancements
- **Advanced Prediction Models**: Incorporate more complex machine learning algorithms.
- **Expanded Data Sources**: Support additional APIs or on-chain data for enhanced predictions.
- **User Authentication**: Allow users to save their predictions and preferences.

## Acknowledgements
- [CoinGecko API](https://www.coingecko.com/en/api) for live cryptocurrency data.
- [Bootstrap](https://getbootstrap.com/) for frontend styling.

