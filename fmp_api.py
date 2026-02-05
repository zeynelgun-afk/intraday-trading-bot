import requests
import pandas as pd
import time
import logging
import config

def get_most_active_stocks() -> list[str]:
    """
    Financial Modeling Prep API'den en yüksek hacimli hisseleri getirir.
    Returns:
        list[str]: Sembol listesi
    """
    url = f"{config.FMP_BASE_URL}/most-actives"
    params = {"apikey": config.FMP_API_KEY}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # İlk 20 hisseyi al
        symbols = [item['symbol'] for item in data[:20]]
        return symbols
    except Exception as e:
        logging.error(f"FMP API hatası (Most Active): {e}")
        return []

def get_1min_historical_data(symbol: str, limit: int = 30) -> pd.DataFrame:
    """
    Belirtilen sembol için son 30 dakikalık 1-dakika OHLCV verisini getirir.
    NOTE: Historical chart endpoints might still use path structure on Stable, 
    but let's try standard v3 structure first or check documentation.
    Stable usually keeps path for charts: /historical-chart/1min/AAPL
    """
    url = f"{config.FMP_BASE_URL}/historical-chart/1min/{symbol}"
    params = {"apikey": config.FMP_API_KEY}
    
    try:
        # Rate limit
        time.sleep(1)
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data:
            return pd.DataFrame()
            
        df = pd.DataFrame(data)
        # Sadece gerekli kolonları ve limit kadar satırı al
        df['date'] = pd.to_datetime(df['date'])
        df = df.head(limit)
        
        df['date'] = pd.to_datetime(df['date'])
        df = df.head(limit)
        
        # Numeric dönüşüm
        cols = ['open', 'high', 'low', 'close', 'volume']
        df[cols] = df[cols].apply(pd.to_numeric)
        
        return df
    except requests.exceptions.HTTPError as e:
        if e.response.status_code in [403, 404]:
            logging.warning(f"FMP API Erişim Sorunu ({symbol}): {e}")
        else:
            logging.error(f"FMP API HTTP Hatası ({symbol}): {e}")
        return pd.DataFrame()
    except Exception as e:
        logging.error(f"FMP API hatası (Historical Data - {symbol}): {e}")
        return pd.DataFrame()

def get_current_price(symbol: str) -> float:
    """
    Hissenin güncel fiyatını getirir.
    Use /quote-short?symbol=X on stable
    """
    url = f"{config.FMP_BASE_URL}/quote-short"
    params = {"apikey": config.FMP_API_KEY, "symbol": symbol}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data:
            return float(data[0]['price'])
        return 0.0
    except Exception as e:
        logging.error(f"FMP API hatası (Current Price - {symbol}): {e}")
        return 0.0
