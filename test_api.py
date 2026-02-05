import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("FMP_API_KEY")

endpoints = [
    # Stable plural (Skill file)
    f"https://financialmodelingprep.com/stable/most-actives?apikey={API_KEY}",
    # Intraday Stable (Try path param + query param mix)
    f"https://financialmodelingprep.com/stable/historical-chart/1min?symbol=AAPL&apikey={API_KEY}",
    # Intraday Stable (Path only - retest)
    f"https://financialmodelingprep.com/stable/historical-chart/1min/AAPL?apikey={API_KEY}",
]

for url in endpoints:
    print(f"Testing: {url.split('?')[0]}...")
    try:
        r = requests.get(url, timeout=5)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and len(data) > 0:
                print(f"Result: Success ({len(data)} items)")
                print(f"Sample: {data[0]}")
            else:
                print(f"Result: Empty or Invalid format: {data}")
        else:
            print(f"Result: Error {r.text[:100]}")
    except Exception as e:
        print(f"Exception: {e}")
    print("-" * 20)
