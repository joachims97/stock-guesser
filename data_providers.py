import requests
import pandas as pd
import os
from datetime import datetime, timedelta


def get_sp500_companies():
    url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"
    df = pd.read_csv(url)

    return df.to_dict('records')


def get_stock_price(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=5y&interval=1d"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()['chart']['result'][0]
        
        df = pd.DataFrame({
            'date': pd.to_datetime(data['timestamp'], unit='s'),
            'close': data['indicators']['quote'][0]['close']
        })
        return df
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return pd.DataFrame({'date': [], 'close': []})
        

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
   url = f"https://api.api-ninjas.com/v1/marketcap?ticker={symbol}"
   headers = {'X-Api-Key': os.getenv('NINJA_API_KEY')}
   try:
       response = requests.get(url, headers=headers)
       data = response.json()
       market_cap = data['market_cap']
       return f"${market_cap/1e12:.1f}T" if market_cap >= 1e12 else f"${market_cap/1e9:.1f}B"
   except:
       return None

