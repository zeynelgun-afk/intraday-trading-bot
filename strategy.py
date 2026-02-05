import logging
import fmp_api
import config

def check_volume_spike(symbol: str) -> bool:
    """
    Verilen hisse için hacim patlaması ve fiyat artışı olup olmadığını kontrol eder.
    
    Kriterler:
    1. Son 1 dk hacmi > Son 20 dk ortalama hacim * VOLUME_SPIKE_MULTIPLIER
    2. Fiyat değişimi > PRICE_CHANGE_THRESHOLD (%0.7)
    3. Fiyat aralığı: MIN_STOCK_PRICE < Fiyat < MAX_STOCK_PRICE
    """
    try:
        # Son 30 dakikalık veriyi çek
        df = fmp_api.get_1min_historical_data(symbol, limit=30)
        
        # Yeterli veri yoksa (en az 20 bar ortalama için + 1 bar güncel)
        if df.empty or len(df) < 21:
            return False
            
        # En güncel bar (zaman olarak en yeni, df.head() ile geldiği için ilk satır olabilir ama FMP sıralamasına dikkat)
        # FMP usually returns newest first. 
        latest = df.iloc[0]
        
        # Önceki 20 bar (latest hariç)
        previous_bars = df.iloc[1:21]
        
        avg_volume = previous_bars['volume'].mean()
        
        # 0'a bölme hatası önlemi
        if avg_volume == 0:
            return False
            
        # 1. Hacim Kontrolü
        volume_condition = latest['volume'] > (avg_volume * config.VOLUME_SPIKE_MULTIPLIER)
        
        # 2. Fiyat Artış Kontrolü ((Close - Open) / Open)
        price_change = (latest['close'] - latest['open']) / latest['open']
        price_condition = price_change > config.PRICE_CHANGE_THRESHOLD
        
        # 3. Fiyat Aralığı Kontrolü
        price_range_condition = config.MIN_STOCK_PRICE < latest['close'] < config.MAX_STOCK_PRICE
        
        if volume_condition and price_condition and price_range_condition:
            logging.info(f"Sinyal {symbol}: Vol={latest['volume']:.0f} (Avg={avg_volume:.0f}), Chg=%{price_change*100:.2f}, Price={latest['close']}")
            return True
            
        return False

    except Exception as e:
        logging.error(f"Strateji hatası ({symbol}): {e}")
        return False
