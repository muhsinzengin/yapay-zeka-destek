# Yapay Zeka Destek Sistemi

Modern, ölçeklenebilir ve kapsamlı bir müşteri destek chatbot sistemi.

## 🎯 Özellikler

- **Rasa 3.6** ile güçlendirilmiş doğal dil işleme
- **Türkçe dil desteği** ve %80 güven eşiği
- **MongoDB** ile konuşma kayıtları ve analitik
- **Telegram bildirimleri** (yeni müşteri, admin girişi)
- **GPT-4 Turbo fallback** düşük güven durumlarında
- **Gelişmiş admin paneli** (Dashboard, Eğitim, Canlı Sohbet)
- **Yarım ekran sağ üst chat penceresi**
- **6 haneli Telegram doğrulama**
- **Duygu analizi**
- **Otomatik gece eğitimi**
- **Yapay zeka maliyet takibi**
- **30 günlük log otomatik temizleme**
- **Haftalık otomatik yedekleme**

## 🚀 Hızlı Başlangıç

```bash
# Repository'yi klonlayın
git clone https://github.com/muhsinzengin/yapay-zeka-destek.git
cd yapay-zeka-destek/rasa-projem

# Bağımlılıkları yükleyin
pip install -r ../requirements.txt

# Ortam değişkenlerini yapılandırın
cp .env.example .env
# .env dosyasını düzenleyin

# MongoDB'yi başlatın
sudo systemctl start mongodb

# Tüm servisleri başlatın
./start.sh
```

## 📁 Proje Yapısı

```
yapay-zeka-destek/
├── README.md                    # Ana README dosyası
├── requirements.txt             # Python bağımlılıkları
└── rasa-projem/                # Ana proje klasörü
    ├── README.md               # Detaylı dokümantasyon
    ├── config.yml              # Rasa konfigürasyonu
    ├── domain.yml              # Domain tanımları
    ├── endpoints.yml           # Endpoint yapılandırması
    ├── data/                   # Eğitim verileri
    ├── actions/                # Custom actions
    ├── webchat/                # Chat widget
    ├── admin_panel/            # Admin paneli
    ├── models/                 # Eğitilmiş modeller
    ├── backups/                # Veritabanı yedekleri
    ├── app.py                  # Flask API server
    ├── start.sh                # Başlatma scripti
    └── stop.sh                 # Durdurma scripti
```

## 📚 Dokümantasyon

Detaylı dokümantasyon için: [rasa-projem/README.md](rasa-projem/README.md)

## 🔧 Gereksinimler

- Python 3.10+
- MongoDB 4.4+
- Rasa 3.6
- 2GB+ RAM
- Internet bağlantısı (GPT-4 ve Telegram için)

## 🌐 Erişim URL'leri

- **Webchat**: http://localhost:5000/webchat/index.html
- **Admin Panel**: http://localhost:5000/admin/dashboard.html
- **Test Sayfası**: http://localhost:5000/test_sayfa.html
- **Rasa API**: http://localhost:5005
- **Flask API**: http://localhost:5000/api

## 🔐 Güvenlik

- HTTPS kullanımı önerilir (üretim ortamında)
- `.env` dosyasını asla paylaşmayın
- Telegram bot token'larını güvenli tutun
- MongoDB'yi güvenli ağda çalıştırın

## 📝 Lisans

MIT License

## 🤝 Katkıda Bulunma

Pull request'ler memnuniyetle karşılanır. Büyük değişiklikler için lütfen önce bir issue açın.

## 📧 İletişim

Sorularınız için issue açabilir veya e-posta gönderebilirsiniz.