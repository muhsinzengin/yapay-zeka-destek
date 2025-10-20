# Sistem Kurulum ve Kullanım Rehberi

## 📋 İçindekiler
1. [Ön Gereksinimler](#ön-gereksinimler)
2. [Kurulum Adımları](#kurulum-adımları)
3. [Konfigürasyon](#konfigürasyon)
4. [İlk Çalıştırma](#ilk-çalıştırma)
5. [Kullanım](#kullanım)
6. [Sorun Giderme](#sorun-giderme)

## Ön Gereksinimler

### 1. Python 3.10 Kurulumu
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip

# Kontrol
python3.10 --version
```

### 2. MongoDB Kurulumu
```bash
# Ubuntu/Debian
sudo apt install -y mongodb

# MongoDB'yi başlat
sudo systemctl start mongodb
sudo systemctl enable mongodb

# Kontrol
mongo --version
```

### 3. Git Kurulumu
```bash
sudo apt install git
```

## Kurulum Adımları

### Adım 1: Projeyi İndirin
```bash
git clone https://github.com/muhsinzengin/yapay-zeka-destek.git
cd yapay-zeka-destek
```

### Adım 2: Sanal Ortam Oluşturun (Önerilen)
```bash
python3.10 -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

### Adım 3: Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

Bu işlem 5-10 dakika sürebilir. İndirilen paketler:
- Rasa 3.6 ve bağımlılıkları
- Flask ve Flask-CORS
- PyMongo (MongoDB client)
- python-telegram-bot
- Ve diğerleri...

## Konfigürasyon

### Adım 1: Ortam Değişkenlerini Ayarlayın

```bash
cd rasa-projem
cp .env.example .env
nano .env  # veya tercih ettiğiniz editör
```

### Adım 2: .env Dosyasını Düzenleyin

#### MongoDB Ayarları
```env
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=rasa_chatbot
```
> Yerel MongoDB kullanıyorsanız varsayılan değerleri değiştirmeyin.

#### Telegram Bot Kurulumu

1. **Telegram'da @BotFather'ı bulun ve konuşmayı başlatın**
2. `/newbot` komutunu gönderin
3. Bot için bir isim ve kullanıcı adı seçin
4. Size verilen token'ı kopyalayın

```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

5. **Admin Chat ID'nizi öğrenin:**
   - @userinfobot ile konuşmaya başlayın
   - Size gönderilen ID'yi kopyalayın

```env
TELEGRAM_ADMIN_CHAT_ID=123456789
```

#### OpenAI API Anahtarı (GPT-4 için)

1. https://platform.openai.com/api-keys adresine gidin
2. Yeni bir API anahtarı oluşturun
3. Anahtarı kopyalayın

```env
OPENAI_API_KEY=sk-...
```

> **Not:** GPT-4 kullanımı ücretlidir. Maliyetleri kontrol altında tutmak için dashboard'dan harcamalarınızı takip edin.

#### Flask Ayarları
```env
FLASK_ENV=production
PORT=5000
SECRET_KEY=rastgele_güçlü_bir_anahtar_oluşturun
```

Secret key oluşturmak için:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### Adım 3: İlk Model Eğitimi

```bash
cd rasa-projem
rasa train
```

Bu işlem ilk kez 10-15 dakika sürebilir. Sonraki eğitimler daha hızlı olacaktır.

## İlk Çalıştırma

### Yöntem 1: Otomatik Başlatma (Önerilen)

```bash
cd rasa-projem
./start.sh
```

Script otomatik olarak:
- Gerekli klasörleri oluşturur
- Servisleri başlatır
- Log dosyalarını izler

### Yöntem 2: Manuel Başlatma

Üç ayrı terminal açın:

**Terminal 1 - Rasa Server:**
```bash
cd rasa-projem
rasa run --enable-api --cors "*"
```

**Terminal 2 - Action Server:**
```bash
cd rasa-projem
rasa run actions
```

**Terminal 3 - Flask API:**
```bash
cd rasa-projem
python app.py
```

## Kullanım

### 1. Webchat Testi

Tarayıcınızda açın: http://localhost:5000/webchat/index.html

**İlk Mesajınızı Gönderin:**
- "Merhaba" yazın
- Bot'un yanıt verdiğini görmelisiniz

### 2. Sistem Sağlık Kontrolü

http://localhost:5000/test_sayfa.html adresine gidin

Tüm servisler yeşil ✅ olmalı:
- Rasa Sunucusu
- MongoDB
- Action Sunucusu
- Telegram Bot (yapılandırıldıysa)

### 3. Admin Paneline Giriş

1. http://localhost:5000/admin/dashboard.html adresine gidin
2. "Kod İste" butonuna tıklayın
3. Telegram'ınızı kontrol edin
4. 6 haneli kodu girin

**Admin Panel Özellikleri:**

#### Dashboard (Gösterge Paneli)
- Bugünkü, haftalık, aylık ve yıllık istatistikler
- Toplam konuşma sayısı
- Benzersiz kullanıcı sayısı
- GPT-4 kullanım maliyeti

#### Eğitim Paneli
- Yeni soru-cevap çiftleri ekleyin
- Mevcut eğitim verilerini görüntüleyin
- Eğitim verilerini silin
- Modeli manuel olarak eğitin

**Eğitim Verisi Ekleme:**
1. "Sorular" alanına virgülle ayrılmış sorular yazın
   - Örnek: "Merhaba, Nasılsın, İyi günler"
2. "Cevap" alanına bot'un vereceği yanıtı yazın
   - Örnek: "Merhaba! Size nasıl yardımcı olabilirim?"
3. İsteğe bağlı "Intent" adı verin
4. "Kaydet" butonuna tıklayın

#### Canlı Sohbet Paneli
- Aktif konuşmaları gerçek zamanlı görün
- Kullanıcı mesajlarını okuyun
- Gerektiğinde müdahale edin (bot otomatik durur)

### 4. Otomatik Görevleri Ayarlama

#### Gece Eğitimi (Her gece 02:00)

```bash
crontab -e
```

Aşağıdaki satırı ekleyin:
```
0 2 * * * cd /tam/yol/rasa-projem && /usr/bin/python3 automated_training.py >> /var/log/rasa_training.log 2>&1
```

#### Haftalık Yedekleme (Her Pazar 03:00)

```
0 3 * * 0 cd /tam/yol/rasa-projem && /usr/bin/python3 database_backup.py >> /var/log/rasa_backup.log 2>&1
```

## Sorun Giderme

### Problem: Rasa başlamıyor

**Çözüm 1:** Port kullanımda olabilir
```bash
lsof -i :5005
kill -9 <PID>
```

**Çözüm 2:** Model eksik
```bash
cd rasa-projem
rasa train
```

### Problem: MongoDB bağlantı hatası

**Kontrol 1:** MongoDB çalışıyor mu?
```bash
sudo systemctl status mongodb
```

**Kontrol 2:** MongoDB başlat
```bash
sudo systemctl start mongodb
```

**Kontrol 3:** Bağlantı ayarlarını kontrol et
```bash
mongo
# MongoDB shell açılmalı
```

### Problem: Action server hatası

**Çözüm:** Bağımlılıkları yeniden yükle
```bash
pip install -r requirements.txt
```

### Problem: Telegram bildirimleri çalışmıyor

**Kontrol 1:** .env dosyasında token doğru mu?
```bash
cat .env | grep TELEGRAM
```

**Kontrol 2:** Bot'u test et
```bash
curl https://api.telegram.org/bot<TOKEN>/getMe
```

### Problem: GPT-4 yanıt vermiyor

**Kontrol 1:** API anahtarı doğru mu?
**Kontrol 2:** OpenAI hesabınızda kredi var mı?
**Kontrol 3:** Logları kontrol edin:
```bash
tail -f logs/actions.log
```

### Problem: Admin paneli açılmıyor

**Kontrol:** Flask API çalışıyor mu?
```bash
curl http://localhost:5000/api/health/mongo
```

## İleri Düzey Ayarlar

### HTTPS Kurulumu (Üretim için Zorunlu)

#### Nginx ile:
```bash
sudo apt install nginx certbot python3-certbot-nginx

# SSL sertifikası al
sudo certbot --nginx -d yourdomain.com
```

#### Nginx konfigürasyonu:
```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /webhooks/ {
        proxy_pass http://localhost:5005;
    }
}
```

### MongoDB Güvenlik

```bash
# MongoDB'de admin kullanıcısı oluştur
mongo
> use admin
> db.createUser({
    user: "admin",
    pwd: "güçlü_şifre",
    roles: ["root"]
})

# .env dosyasını güncelle
MONGODB_URI=mongodb://admin:güçlü_şifre@localhost:27017/
```

### Performans Optimizasyonu

**Rasa için:**
```bash
# config.yml'de epochs sayısını artırın (daha iyi doğruluk)
# Ancak eğitim süresi uzar
```

**MongoDB için:**
```bash
# Indexleri kontrol et
mongo
> use rasa_chatbot
> db.conversations.getIndexes()
```

## Yardım ve Destek

- GitHub Issues: https://github.com/muhsinzengin/yapay-zeka-destek/issues
- Rasa Dokümantasyonu: https://rasa.com/docs/
- MongoDB Dokümantasyonu: https://docs.mongodb.com/

## Sistem Gereksinimleri (Üretim)

- **CPU:** 2+ cores
- **RAM:** 4GB+ (8GB önerilen)
- **Disk:** 10GB+ boş alan
- **Ağ:** Stabil internet bağlantısı
- **OS:** Ubuntu 20.04+ veya benzeri Linux dağıtımı

## Yedekleme Stratejisi

1. **Veritabanı:** Haftalık otomatik (database_backup.py)
2. **Modeller:** models/ klasörünü manuel yedekleyin
3. **Konfigürasyon:** .env ve config dosyalarını güvenli tutun
4. **Kod:** Git repository'de saklayın

## Güvenlik Kontrol Listesi

- [ ] .env dosyası .gitignore'da
- [ ] MongoDB güvenlik duvarı kuralları aktif
- [ ] HTTPS sertifikası yüklü
- [ ] Güçlü şifreler kullanıldı
- [ ] Telegram bot token'ları güvenli
- [ ] OpenAI API anahtarı korumalı
- [ ] Düzenli yedekleme yapılıyor
- [ ] Log dosyaları izleniyor

## Sonraki Adımlar

1. ✅ Sistemi test edin
2. ✅ Eğitim verisi ekleyin
3. ✅ Modeli yeniden eğitin
4. ✅ Üretim ortamına deploy edin
5. ✅ Performansı izleyin
6. ✅ Kullanıcı geri bildirimlerini toplayın
7. ✅ Düzenli güncellemeler yapın

---

**Tebrikler! 🎉** Sistem başarıyla kuruldu ve çalışıyor.
