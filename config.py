import os
from dotenv import load_dotenv

load_dotenv()

# FMP API
FMP_API_KEY = os.getenv('FMP_API_KEY')
FMP_BASE_URL = "https://financialmodelingprep.com/stable"

# IBKR API
IBKR_HOST = "127.0.0.1"
IBKR_PORT = 7497  # Paper trading (7496 = live)
IBKR_CLIENT_ID = 1

# Strateji Parametreleri
VOLUME_SPIKE_MULTIPLIER = 4.0  # Hacim normal ortalamanın 4 katı
PRICE_CHANGE_THRESHOLD = 0.007  # %0.7 fiyat artışı
MIN_STOCK_PRICE = 5.0  # Minimum hisse fiyatı ($5)
MAX_STOCK_PRICE = 500.0  # Maksimum hisse fiyatı
POSITION_SIZE = 10  # Her hisse için alınacak miktar
MAX_POSITIONS = 5  # Aynı anda maksimum pozisyon sayısı

# Market Saatleri (EST - New York)
MARKET_OPEN = "09:30"
MARKET_CLOSE = "16:00"
EXIT_TIME = "15:45"  # Pozisyonları kapatma zamanı

# Log
LOG_FILE = "logs/trading_bot.log"
