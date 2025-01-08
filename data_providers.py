import requests
import pandas as pd
import os
from datetime import datetime, timedelta


def get_sp500_companies():
    url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"
    df = pd.read_csv(url)

    return df.to_dict('records')


def get_stock_price(symbol):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5*365)
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from={start_date.strftime('%Y-%m-%d')}&apikey={os.getenv('FMP_API_KEY')}"
    response = requests.get(url)
    data = response.json().get('historical', [])
    return pd.DataFrame(data) if data else pd.DataFrame({'date': [], 'close': []})


def get_company_metrics(symbol):
    url = "https://yahoo-finance166.p.rapidapi.com/api/stock/get-financial-data"
    headers = {
        "x-rapidapi-key": os.getenv('RAPIDAPI_KEY'),
        "x-rapidapi-host": "yahoo-finance166.p.rapidapi.com"
    }
    params = {"region": "US", "symbol": symbol}
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        return {
            'revenue': data['quoteSummary']['result'][0]['financialData']['totalRevenue']['fmt'],
            'revenueGrowth': data['quoteSummary']['result'][0]['financialData']['revenueGrowth']['fmt'],
            'profitMargin': data['quoteSummary']['result'][0]['financialData']['profitMargins']['fmt']
        }
    except:
        return {'revenue': 'N/A', 'revenueGrowth': 'N/A', 'profitMargin': 'N/A'}


def get_market_cap(symbol):
    url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={os.getenv('FMP_API_KEY')}"
    try:
        response = requests.get(url)
        data = response.json()
        return data[0]['mktCap']
    except:
        return None


