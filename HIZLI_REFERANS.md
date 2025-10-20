# Hızlı Referans Kılavuzu

## 🚀 Başlatma ve Durdurma

### Tüm Servisleri Başlat
```bash
cd rasa-projem
./start.sh
```

### Tüm Servisleri Durdur
```bash
./stop.sh
```

### Sadece Rasa'yı Yeniden Başlat
```bash
pkill -f "rasa run"
rasa run --enable-api --cors "*" &
```

## 📝 Eğitim İşlemleri

### Modeli Eğit
```bash
cd rasa-projem
rasa train
```

### Sadece NLU Eğit
```bash
rasa train nlu
```

### Modeli Test Et
```bash
rasa test
```

### Interactive Training
```bash
rasa interactive
```

## 💾 Veritabanı İşlemleri

### MongoDB'ye Bağlan
```bash
mongo
use rasa_chatbot
```

### Tüm Konuşmaları Gör
```javascript
db.conversations.find().pretty()
```

### Bugünkü Konuşmaları Say
```javascript
var today = new Date();
today.setHours(0,0,0,0);
db.conversations.count({timestamp: {$gte: today}})
```

### Kullanıcıya Göre Konuşmaları Bul
```javascript
db.conversations.find({user_id: "user_123"}).pretty()
```

### Eski Logları Temizle (30 günden eski)
```javascript
var cutoff = new Date();
cutoff.setDate(cutoff.getDate() - 30);
db.conversations.deleteMany({timestamp: {$lt: cutoff}})
```

### Manuel Yedek Al
```bash
python database_backup.py
```

## 📊 İstatistik ve Analiz

### API ile İstatistik Al
```bash
# Bugünkü istatistikler
curl http://localhost:5000/api/statistics?period=daily

# Haftalık
curl http://localhost:5000/api/statistics?period=weekly

# Aylık
curl http://localhost:5000/api/statistics?period=monthly
```

### Canlı Konuşmaları Listele
```bash
curl http://localhost:5000/api/live-conversations
```

## 🔍 Log İnceleme

### Rasa Logları
```bash
tail -f logs/rasa.log
```

### Action Server Logları
```bash
tail -f logs/actions.log
```

### Flask API Logları
```bash
tail -f logs/flask.log
```

### Tüm Logları Birlikte İzle
```bash
tail -f logs/*.log
```

## 🧪 Test İşlemleri

### Tek Mesaj Test
```bash
curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{"sender":"test","message":"Merhaba"}'
```

### Sağlık Kontrolü
```bash
# Rasa
curl http://localhost:5005/

# MongoDB
curl http://localhost:5000/api/health/mongo

# Telegram
curl http://localhost:5000/api/health/telegram
```

### Action Server Test
```bash
curl http://localhost:5055/health
```

## 📱 Telegram İşlemleri

### Bot Bilgilerini Görüntüle
```bash
curl https://api.telegram.org/bot<TOKEN>/getMe
```

### Webhook Ayarla
```bash
curl https://api.telegram.org/bot<TOKEN>/setWebhook \
  -d "url=https://yourdomain.com/webhooks/telegram/webhook"
```

### Webhook'u Kaldır
```bash
curl https://api.telegram.org/bot<TOKEN>/deleteWebhook
```

### Webhook Bilgisini Görüntüle
```bash
curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo
```

## 🔧 Sorun Giderme Komutları

### Port Kullanımını Kontrol Et
```bash
# Rasa port (5005)
lsof -i :5005

# Action server port (5055)
lsof -i :5055

# Flask port (5000)
lsof -i :5000
```

### Process'leri Öldür
```bash
pkill -f "rasa run"
pkill -f "python app.py"
```

### Python Bağımlılıklarını Yenile
```bash
pip install --upgrade -r requirements.txt
```

### Disk Kullanımını Kontrol Et
```bash
du -sh rasa-projem/*
```

### Log Dosyalarını Temizle
```bash
rm logs/*.log
```

## 📤 Deployment İşlemleri

### Production Modunda Başlat
```bash
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Systemd Service Oluştur

**rasa.service:**
```ini
[Unit]
Description=Rasa Server
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/path/to/rasa-projem
ExecStart=/usr/local/bin/rasa run --enable-api --cors "*"
Restart=always

[Install]
WantedBy=multi-user.target
```

**Servisi Başlat:**
```bash
sudo systemctl start rasa
sudo systemctl enable rasa
```

## 🔐 Güvenlik İşlemleri

### .env Dosyası Şifrele
```bash
# gpg ile şifrele
gpg -c .env

# Şifreyi çöz
gpg .env.gpg
```

### Yeni Secret Key Oluştur
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### SSL Sertifikası Yenile
```bash
sudo certbot renew
```

## 📈 Performans Optimizasyonu

### MongoDB İndeks Oluştur
```javascript
db.conversations.createIndex({user_id: 1, timestamp: -1})
db.conversations.createIndex({timestamp: -1})
```

### Rasa Model Boyutunu Küçült
```bash
# config.yml'de:
# epochs sayısını azalt
# component'leri optimize et
```

### Eski Modelleri Temizle
```bash
cd models
ls -lt | tail -n +6 | awk '{print $9}' | xargs rm
# Son 5 modeli tutar, eskilerini siler
```

## 🔄 Güncelleme İşlemleri

### Git'ten Güncellemeleri Çek
```bash
git pull origin main
```

### Rasa'yı Güncelle
```bash
pip install --upgrade rasa
```

### Bağımlılıkları Güncelle
```bash
pip install --upgrade -r requirements.txt
```

## 📊 Monitoring Komutları

### Sistem Kaynaklarını İzle
```bash
# CPU ve RAM kullanımı
htop

# Sadece Python process'leri
ps aux | grep python
```

### MongoDB Performansı
```javascript
db.serverStatus()
db.stats()
```

### Bağlantı Sayıları
```bash
netstat -an | grep 5005 | wc -l  # Rasa
netstat -an | grep 5000 | wc -l  # Flask
```

## 🎯 Hızlı Komutlar (Alias)

**~/.bashrc veya ~/.zshrc'ye ekleyin:**

```bash
# Rasa kısayolları
alias rasa-start='cd ~/rasa-projem && ./start.sh'
alias rasa-stop='cd ~/rasa-projem && ./stop.sh'
alias rasa-train='cd ~/rasa-projem && rasa train'
alias rasa-logs='cd ~/rasa-projem && tail -f logs/*.log'
alias rasa-backup='cd ~/rasa-projem && python database_backup.py'

# Reload
source ~/.bashrc  # veya source ~/.zshrc
```

## 📞 API Endpoint'leri

### Temel Endpoint'ler
```bash
# Rasa webhook
POST http://localhost:5005/webhooks/rest/webhook

# İstatistikler
GET http://localhost:5000/api/statistics?period=daily

# Eğitim verisi
GET http://localhost:5000/api/training-data
POST http://localhost:5000/api/training-data
DELETE http://localhost:5000/api/training-data/:id

# Canlı konuşmalar
GET http://localhost:5000/api/live-conversations
GET http://localhost:5000/api/conversation/:user_id

# Model eğitimi
POST http://localhost:5000/api/train-model

# Admin
POST http://localhost:5000/api/admin/request-code
POST http://localhost:5000/api/admin/verify-code
```

## 🆘 Acil Durum Komutları

### Tüm Servisleri Zorla Durdur
```bash
pkill -9 -f rasa
pkill -9 -f python
```

### MongoDB'yi Zorla Durdur
```bash
sudo systemctl stop mongodb
```

### Tüm Portları Temizle
```bash
sudo fuser -k 5005/tcp
sudo fuser -k 5055/tcp
sudo fuser -k 5000/tcp
```

### Son Çare: Sistemi Yeniden Başlat
```bash
sudo reboot
```

## 💡 İpuçları

1. **Log dosyalarını düzenli kontrol edin**
2. **Yedekleri farklı bir konumda saklayın**
3. **Test ortamında deneyip production'a alın**
4. **Cron job'ların çalıştığını doğrulayın**
5. **Disk alanını düzenli kontrol edin**
6. **MongoDB indekslerini optimize edin**
7. **SSL sertifikalarının geçerliliğini kontrol edin**

---

**Not:** Bu komutları kullanmadan önce ne yaptığınızdan emin olun. Özellikle production ortamında dikkatli olun.
