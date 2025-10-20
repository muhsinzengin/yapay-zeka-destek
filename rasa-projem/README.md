# Yapay Zeka Destek Sistemi

Rasa 3.6 tabanlı, MongoDB entegreli, Telegram bildirimleri ve GPT-4 Turbo fallback özellikli tam kapsamlı müşteri destek chatbot sistemi.

## Özellikler

- 🤖 Rasa 3.6 ile güçlendirilmiş doğal dil işleme
- 🇹🇷 Türkçe dil desteği
- 💾 MongoDB ile konuşma kayıtları ve analitik
- 📱 Telegram bildirimleri (yeni müşteri, admin girişi)
- 🧠 %80 güven eşiği altında GPT-4 Turbo fallback
- 📊 Gelişmiş admin paneli (Dashboard, Eğitim, Canlı Sohbet)
- 💬 Yarım ekran sağ üst chat penceresi
- 🔐 Telegram ile 6 haneli kod doğrulama
- 📈 Duygu analizi
- ⏰ Otomatik gece eğitimi
- 💰 Yapay zeka maliyet takibi
- 🔒 HTTPS güvenlik desteği
- 📦 Haftalık otomatik yedekleme
- 🗑️ 30 günlük log otomatik temizleme

## Sistem Gereksinimleri

- Python 3.10
- MongoDB 4.4+
- Node.js (opsiyonel, geliştirme için)

## Kurulum

### 1. Bağımlılıkları Yükleyin

```bash
cd rasa-projem
pip install -r requirements.txt
```

### 2. Ortam Değişkenlerini Ayarlayın

`.env.example` dosyasını `.env` olarak kopyalayın ve değerleri düzenleyin:

```bash
cp .env.example .env
```

Gerekli değişkenler:
- `MONGODB_URI`: MongoDB bağlantı adresi
- `TELEGRAM_BOT_TOKEN`: Telegram bot token'ı
- `TELEGRAM_ADMIN_CHAT_ID`: Admin Telegram chat ID'si
- `OPENAI_API_KEY`: OpenAI API anahtarı (GPT-4 için)

### 3. MongoDB'yi Başlatın

```bash
# MongoDB servisini başlatın (sistem bağımlı)
sudo systemctl start mongodb
# veya
mongod --dbpath /path/to/data
```

### 4. Rasa Modelini Eğitin

```bash
rasa train
```

### 5. Servisleri Başlatın

Üç ayrı terminal penceresinde:

**Terminal 1 - Rasa Server:**
```bash
rasa run --enable-api --cors "*"
```

**Terminal 2 - Action Server:**
```bash
rasa run actions
```

**Terminal 3 - Flask API Server:**
```bash
python app.py
```

## Kullanım

### Webchat
Tarayıcıda açın: `http://localhost:5000/webchat/index.html`

### Admin Panel
1. Tarayıcıda açın: `http://localhost:5000/admin/dashboard.html`
2. Telegram'a gelen 6 haneli kodu girin
3. Dashboard, Eğitim ve Canlı Sohbet panellerine erişin

### Test Sayfası
Sistem sağlığını kontrol edin: `http://localhost:5000/test_sayfa.html`

## Otomatik Görevler

### Gece Eğitimi (Her Gece 02:00)

Konuşmaları NLU formatına çevirir ve modeli eğitir:

```bash
python automated_training.py
```

### Haftalık Yedekleme (Her Pazar 03:00)

Veritabanını JSON formatında yedekler:

```bash
python database_backup.py
```

### Crontab Kurulumu

```bash
# Crontab dosyasını düzenle
crontab -e

# Örnek crontab dosyasını kopyala
cat crontab.example >> /var/spool/cron/crontabs/$(whoami)
```

## Dizin Yapısı

```
rasa-projem/
├── config.yml              # Rasa konfigürasyonu (TR, %80 confidence)
├── domain.yml              # Domain tanımları (slots, intents, responses)
├── endpoints.yml           # Action server ve channel endpoints
├── data/
│   └── nlu.yml            # NLU eğitim verisi (otomatik doldurulur)
├── actions/
│   ├── actions.py         # Custom action'lar
│   ├── database/
│   │   └── mongoclient.py # MongoDB istemcisi
│   ├── telegram_notifier.py
│   ├── sentiment_analyzer.py
│   └── gpt4_fallback.py
├── webchat/
│   ├── index.html         # Chat widget
│   ├── style.css
│   └── chat.js
├── admin_panel/
│   ├── dashboard.html     # İstatistikler
│   ├── egitim.html        # Eğitim yönetimi
│   ├── canli.html         # Canlı sohbet takibi
│   ├── admin-style.css
│   ├── dashboard.js
│   ├── egitim.js
│   └── canli.js
├── models/                # Eğitilmiş modeller
├── backups/               # Veritabanı yedekleri
├── veri_deposu.json       # Admin veri deposu
├── app.py                 # Flask API server
├── automated_training.py  # Otomatik eğitim scripti
└── database_backup.py     # Yedekleme scripti
```

## API Endpoints

### Sağlık Kontrolleri
- `GET /api/health/mongo` - MongoDB bağlantı durumu
- `GET /api/health/telegram` - Telegram konfigürasyon durumu

### İstatistikler
- `GET /api/statistics?period=daily|weekly|monthly|yearly|total`

### Eğitim Verisi
- `GET /api/training-data` - Tüm eğitim verisini getir
- `POST /api/training-data` - Yeni eğitim verisi ekle
- `DELETE /api/training-data/:id` - Eğitim verisini sil

### Canlı Konuşmalar
- `GET /api/live-conversations` - Aktif konuşmaları listele
- `GET /api/conversation/:user_id` - Belirli kullanıcının konuşma geçmişi
- `POST /api/intervention` - Admin müdahalesi

### Model Eğitimi
- `POST /api/train-model` - Model eğitimini başlat

### Admin Doğrulama
- `POST /api/admin/request-code` - 6 haneli kod talep et
- `POST /api/admin/verify-code` - Kodu doğrula

## Güvenlik

### HTTPS Konfigürasyonu

Üretim ortamında HTTPS kullanın. Nginx örneği:

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /webhooks/ {
        proxy_pass http://localhost:5005;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Şifreleme

Hassas veriler MongoDB'de otomatik şifrelenir. `.env` dosyasını güvenli tutun.

## Sorun Giderme

### Rasa başlamıyor
```bash
# Port kullanımda olabilir
lsof -i :5005
kill -9 <PID>
```

### MongoDB bağlantı hatası
```bash
# MongoDB servisini kontrol et
sudo systemctl status mongodb

# Logları kontrol et
tail -f /var/log/mongodb/mongod.log
```

### Action server hatası
```bash
# Actions klasöründe requirements.txt var mı kontrol et
pip install -r requirements.txt
```

## Geliştirme

### Yeni Intent Ekleme

1. `domain.yml` dosyasına intent ekleyin
2. `data/nlu.yml` dosyasına örnekler ekleyin
3. `actions/actions.py` dosyasına custom action ekleyin (gerekirse)
4. Modeli yeniden eğitin: `rasa train`

### Yeni Admin Panel Sayfası

1. `admin_panel/` klasörüne HTML dosyası ekleyin
2. JavaScript dosyası oluşturun
3. `admin-style.css` kullanın veya özelleştirin
4. Sidebar menüsüne link ekleyin

## Lisans

MIT License

## Destek

Sorularınız için: support@example.com
