from ib_insync import *
import logging
import config

class IBKRClient:
    def __init__(self):
        self.ib = IB()
        self.connected = False

    def connect(self) -> bool:
        """
        IB Gateway veya TWS'e bağlanır.
        """
        try:
            self.ib.connect(config.IBKR_HOST, config.IBKR_PORT, clientId=config.IBKR_CLIENT_ID)
            self.connected = True
            logging.info(f"IBKR'a bağlandı (Host: {config.IBKR_HOST}, Port: {config.IBKR_PORT})")
            return True
        except Exception as e:
            self.connected = False
            logging.error(f"IBKR bağlantı hatası: {e}")
            return False

    def disconnect(self):
        """
        Bağlantıyı kapatır.
        """
        if self.connected:
            self.ib.disconnect()
            self.connected = False
            logging.info("IBKR bağlantısı kapatıldı")

    def get_account_balance(self) -> float:
        """
        Hesap bakiyesini (Net Liquidation Value) döndürür.
        """
        if not self.connected:
            return 0.0
        
        try:
            account_summary = self.ib.accountSummary()
            # NetLiquidation değerini bul
            for tag in account_summary:
                if tag.tag == 'NetLiquidation':
                    return float(tag.value)
            return 0.0
        except Exception as e:
            logging.error(f"Bakiye alma hatası: {e}")
            return 0.0

    def place_market_order(self, symbol: str, quantity: int, action: str) -> bool:
        """
        Market emri gönderir.
        """
        if not self.connected:
            return False

        try:
            contract = Stock(symbol, 'SMART', 'USD')
            self.ib.qualifyContracts(contract)
            
            order = MarketOrder(action, quantity)
            trade = self.ib.placeOrder(contract, order)
            
            logging.info(f"{action} {quantity} {symbol} @ MARKET")
            return True
        except Exception as e:
            logging.error(f"Emir hatası ({symbol}): {e}")
            return False

    def get_open_positions(self) -> list[dict]:
        """
        Açık pozisyonları listeler.
        """
        if not self.connected:
            return []
            
        try:
            portfolio = self.ib.portfolio()
            result = []
            for item in portfolio:
                if item.contract.secType == 'STK':
                    result.append({
                        'symbol': item.contract.symbol,
                        'quantity': item.position,
                        'avg_price': item.averageCost,
                        'unrealized_pnl': item.unrealizedPNL
                    })
            return result
        except Exception as e:
            logging.error(f"Pozisyon listeleme hatası: {e}")
            return []

    def close_all_positions(self):
        """
        Tüm açık pozisyonları kapatır.
        """
        positions = self.get_open_positions()
        if not positions:
            logging.info("Kapatılacak açık pozisyon yok.")
            return

        logging.info(f"Tüm pozisyonlar kapatılıyor ({len(positions)} adet)...")
        for pos in positions:
            if pos['quantity'] > 0:
                self.place_market_order(pos['symbol'], int(pos['quantity']), "SELL")
            elif pos['quantity'] < 0:
                self.place_market_order(pos['symbol'], abs(int(pos['quantity'])), "BUY")
        
        logging.info("Tüm pozisyonlar için kapanış emri gönderildi.")
