# Intraday Hacim Patlaması Trading Botu

Bu bot, Financial Modeling Prep (FMP) API kullanarak Amerikan borsasındaki en yüksek hacimli hisseleri tarar ve ani hacim patlaması (volume spike) tespit ettiğinde Interactive Brokers (IBKR) üzerinden otomatik alım yapar. Pozisyonlar gün sonunda otomatik olarak kapatılır.

## Özellikler

- **Otonom Tarama:** Piyasadaki en aktif hisseleri sürekli izler.
- **Hacim Analizi:** 1 dakikalık verilerle anormal hacim artışlarını tespit eder.
- **Otomatik Alım-Satım:** IBKR API ile saniyeler içinde emir gönderir.
- **Risk Yönetimi:** Maksimum pozisyon sayısı ve hisse başına sabit miktar kontrolü.
- **Gün Sonu Kapanış:** Market kapanmadan önce (15:45 EST) tüm pozisyonları nakite geçer.

## Gereksinimler

- Python 3.10+
- Interactive Brokers Hesabı (TWS veya IB Gateway kurulu olmalı)
- Financial Modeling Prep API Key (Ücretsiz plan yeterli olabilir ama gecikmesiz veri için premium önerilir)

## Kurulum

1. Depoyu klonlayın veya indirin:
   ```bash
   git clone https://github.com/yourusername/intraday-trading-bot.git
   cd intraday-trading-bot
   ```

2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

3. Çevre değişkenlerini ayarlayın:
   `.env` adında bir dosya oluşturun ve içine FMP API anahtarınızı ekleyin:
   ```env
   FMP_API_KEY=your_fmp_api_key_here
   ```

4. Interactive Brokers TWS veya Gateway ayarları:
   - **Enable ActiveX and Socket Clients** seçeneğini işaretleyin.
   - **Socket Port** olarak `7497` (Paper Trading için) ayarlayın. Canlı işlem için `config.py` içinden portu `7496` yapın.
   - **Trusted IPs** kısmına `127.0.0.1` ekleyin.

## Kullanım

Botu başlatmak için:

```bash
python main.py
```

## Strateji

Bot şu kriterler sağlandığında alım yapar:
1. Son 1 dakikalık hacim, önceki 20 dakikalık ortalamanın **4 katından** (config: `VOLUME_SPIKE_MULTIPLIER`) fazla ise.
2. Fiyat artışı **%0.7**'den (config: `PRICE_CHANGE_THRESHOLD`) büyük ise.
3. Hisse fiyatı **$5 - $500** arasında ise.

## Dosya Yapısı

- `main.py`: Ana döngü ve programın giriş noktası.
- `strategy.py`: Alım-satım sinyallerini üreten algoritma.
- `fmp_api.py`: FMP veri sağlayıcısı ile iletişim.
- `ibkr_api.py`: IBKR emir iletim sistemi.
- `config.py`: Tüm ayarların bulunduğu dosya.

## Güvenlik Uyarısı

Bu botu gerçek para ile kullanmadan önce mutlaka **Paper Trading** (Sanal Hesap) modunda test edin. Algoritmik ticaret risk içerir.

## Lisans

MIT License
