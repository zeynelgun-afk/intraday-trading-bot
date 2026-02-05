import time
import logging
import os
from datetime import datetime
from pytz import timezone
import config
import fmp_api
from ibkr_api import IBKRClient
from strategy import check_volume_spike
import threading
import dashboard  # Flask app import

def setup_logging():
    """Loglama ayarlarını yapar."""
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler(),
            dashboard.DashboardLogHandler() # SocketIO Logger
        ]
    )

def is_market_open() -> bool:
    """Market saatleri içinde miyiz kontrol eder."""
    now = datetime.now(timezone('US/Eastern'))
    current_time = now.strftime('%H:%M')
    
    return config.MARKET_OPEN <= current_time <= config.MARKET_CLOSE

def scan_and_trade(ib_client: IBKRClient):
    """Piyasayı tarar ve trade fırsatlarını değerlendirir."""
    logging.info("Tarama başlatıldı...")
    
    # Adım 1: En aktif hisseleri al
    candidates = fmp_api.get_most_active_stocks()
    if not candidates:
        logging.warning("Hiç hisse bulunamadı veya API hatası.")
        return

    # Adım 2: Her hisseyi kontrol et
    for symbol in candidates:
        if check_volume_spike(symbol):
            # Açık pozisyon kontrolü
            open_positions = ib_client.get_open_positions()
            existing_position = any(p['symbol'] == symbol for p in open_positions)
            
            if existing_position:
                logging.warning(f"{symbol}: Hacim patlaması tespit edildi ama zaten pozisyon açık")
                continue
                
            if len(open_positions) >= config.MAX_POSITIONS:
                logging.warning(f"{symbol}: Maksimum pozisyon sayısına ulaşıldı, işlem yapılmadı.")
                continue
                
            # Alım yap
            logging.info(f"[ALIM] {symbol} için hacim patlaması! Alış emri gönderiliyor.")
            ib_client.place_market_order(symbol, config.POSITION_SIZE, "BUY")
            
        time.sleep(1) # API rate limit koruması

    logging.info(f"Tarama tamamlandı - {len(candidates)} hisse incelendi")

def close_positions_at_eod(ib_client: IBKRClient):
    """Gün sonu kapanış işlemi."""
    logging.info("Gün sonu - Tüm pozisyonlar kapatılıyor")
    ib_client.close_all_positions()

def main():
    # Start Dashboard in Thread
    dash_thread = threading.Thread(target=dashboard.run_dashboard, daemon=True)
    dash_thread.start()
    
    setup_logging()
    logging.info("[START] Intraday Trading Bot başlatıldı")
    
    ib_client = IBKRClient()
    connected = ib_client.connect()
    
    if not connected:
        logging.critical("IBKR bağlantısı başarısız. Bot durduruluyor.")
        return
        
    balance = ib_client.get_account_balance()
    logging.info(f"Hesap bakiyesi: ${balance:,.2f}")

    try:
        while True:
            now = datetime.now(timezone('US/Eastern'))
            current_time = now.strftime('%H:%M')
            
            # Dashboard Update
            market_active = is_market_open()
            balance = ib_client.get_account_balance()
            positions = ib_client.get_open_positions() # Ensure this returns list of dicts with unrealizedPNL if possible
            
            dashboard.update_dashboard_state({
                "status": "Scanning" if market_active else "Waiting for Market Open",
                "balance": balance,
                "positions": positions,
                "last_update": now.strftime('%H:%M:%S'),
                "market_active": market_active
            })

            if market_active:
                if current_time >= config.EXIT_TIME:
                    close_positions_at_eod(ib_client)
                    logging.info("Gün sonu çıkış saati geldi. Program sonlandırılıyor.")
                    break  # Bot'u durdur
                else:
                    scan_and_trade(ib_client)
                    logging.info("Bir sonraki tarama için 1 dakika bekleniyor...")
                    time.sleep(60)  # 1 dakika bekle
            else:
                logging.info(f"Market kapalı ({current_time}), bekleniyor... (Açılış: {config.MARKET_OPEN})")
                time.sleep(300)  # 5 dakika bekle
                
    except KeyboardInterrupt:
        logging.info("Kullanıcı tarafından durduruldu.")
    except Exception as e:
        logging.error(f"Beklenmeyen hata: {e}")
    finally:
        ib_client.disconnect()
        logging.info("[STOP] Bot durduruldu")

if __name__ == "__main__":
    main()
