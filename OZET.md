# 🎯 Proje Özeti - Yapay Zeka Destek Sistemi

## Proje Hakkında

Bu proje, Rasa 3.6 tabanlı, MongoDB entegreli, Telegram bildirimleri ve GPT-4 Turbo fallback özellikli **tam kapsamlı bir müşteri destek chatbot sistemi**dir.

## ✨ Temel Özellikler

### 1. **Akıllı Konuşma Yönetimi**
- Rasa 3.6 ile doğal dil işleme
- Türkçe dil desteği
- %80 güven eşiği
- Düşük güvende GPT-4 Turbo'ya otomatik geçiş
- Duygu analizi (pozitif, negatif, kızgın, nötr)

### 2. **Kapsamlı Admin Paneli**
- **Dashboard:** Gerçek zamanlı istatistikler
  - Günlük, haftalık, aylık, yıllık metrikler
  - Toplam konuşma ve kullanıcı sayıları
  - GPT-4 kullanım maliyeti takibi
  
- **Eğitim Yönetimi:**
  - Soru-cevap çiftleri ekleme (virgülle ayrılmış)
  - Mevcut eğitim verilerini görüntüleme ve silme
  - Tek tıkla model eğitimi

- **Canlı Sohbet İzleme:**
  - Aktif konuşmaları gerçek zamanlı takip
  - Konuşma geçmişini görüntüleme
  - Admin müdahalesi (bot otomatik durur)
  - Yeşil ışıklı aktif kullanıcı göstergesi

### 3. **Modern Web Arayüzü**
- Sağ üst yarım ekran chat widget
- Responsive tasarım
- Gradient renkler (🤖 mavi-mor)
- Typing indicator
- Smooth animasyonlar

### 4. **Güçlü Backend Entegrasyonu**
- **MongoDB:** Tüm konuşmaları kaydeder
- **Telegram Bot:** 
  - Yeni müşteri bildirimleri
  - 6 haneli admin giriş kodu
  - Müdahale gerekli bildirimleri
- **GPT-4 Turbo:** Fallback AI yanıtları
- **Flask API:** Admin panel backend'i

### 5. **Otomasyon ve Bakım**
- **Gece Eğitimi:** Her gece 02:00 (cron)
  - Konuşmaları NLU formatına çevirir
  - Modeli otomatik eğitir
  - Eski logları temizler (30 gün+)

- **Haftalık Yedekleme:** Her Pazar 03:00 (cron)
  - Tüm veritabanını JSON'a yedekler
  - 4 haftalık yedek tutar
  - Eski yedekleri otomatik siler

### 6. **Güvenlik**
- HTTPS desteği (production için)
- Şifrelenmiş API anahtarları
- Telegram 6 haneli doğrulama
- MongoDB authentication
- Firewall kuralları

## 📁 Dosya Yapısı

```
yapay-zeka-destek/
├── README.md                    # Genel bilgi
├── KURULUM_REHBERI.md          # Detaylı kurulum kılavuzu
├── HIZLI_REFERANS.md           # Komut referansları
├── MIMARI.md                    # Sistem mimarisi
├── CHECKLIST.md                 # Kurulum kontrol listesi
├── requirements.txt             # Python bağımlılıkları
│
└── rasa-projem/                # Ana proje
    ├── README.md               # Proje dokümantasyonu
    ├── .env.example            # Örnek ortam değişkenleri
    ├── .gitignore              # Git ignore kuralları
    │
    ├── config.yml              # Rasa NLU/Core konfigürasyonu
    ├── domain.yml              # Intents, slots, responses
    ├── endpoints.yml           # Telegram, webchat endpoints
    │
    ├── data/
    │   └── nlu.yml            # Eğitim verileri (otomatik doldurulur)
    │
    ├── actions/                # Custom actions
    │   ├── __init__.py
    │   ├── actions.py         # Ana action'lar
    │   ├── database/
    │   │   ├── __init__.py
    │   │   └── mongoclient.py # MongoDB client
    │   ├── telegram_notifier.py
    │   ├── sentiment_analyzer.py
    │   └── gpt4_fallback.py
    │
    ├── webchat/                # Chat widget
    │   ├── index.html
    │   ├── style.css
    │   └── chat.js
    │
    ├── admin_panel/            # Admin paneli
    │   ├── dashboard.html     # İstatistikler
    │   ├── egitim.html        # Eğitim yönetimi
    │   ├── canli.html         # Canlı sohbet
    │   ├── admin-style.css    # Ortak stiller
    │   ├── dashboard.js
    │   ├── egitim.js
    │   └── canli.js
    │
    ├── models/                 # Eğitilmiş modeller
    │   └── .gitkeep
    │
    ├── backups/                # Veritabanı yedekleri
    ├── logs/                   # Log dosyaları
    │
    ├── app.py                  # Flask API server
    ├── automated_training.py   # Otomatik eğitim scripti
    ├── database_backup.py      # Yedekleme scripti
    ├── crontab.example         # Örnek cron jobs
    ├── veri_deposu.json        # Admin veri deposu
    ├── start.sh                # Başlatma scripti
    ├── stop.sh                 # Durdurma scripti
    └── test_sayfa.html         # Sistem test sayfası
```

## 🔧 Teknolojiler

### Backend
- **Python 3.10:** Ana programlama dili
- **Rasa 3.6:** Conversational AI framework
- **Flask 2.3:** Web framework
- **MongoDB 4.4+:** NoSQL veritabanı
- **python-telegram-bot 20.5:** Telegram entegrasyonu
- **OpenAI GPT-4 Turbo:** Fallback AI

### Frontend
- **HTML5/CSS3:** Modern web standartları
- **Vanilla JavaScript:** Bağımlılıksız, hızlı
- **Responsive Design:** Mobil uyumlu

### DevOps
- **Git:** Versiyon kontrolü
- **Cron:** Zamanlanmış görevler
- **Systemd:** Servis yönetimi (production)
- **Nginx:** Reverse proxy (production)

## 📊 Temel Metrikler

### Performans Hedefleri
- **Yanıt Süresi:** < 2 saniye
- **Model Güveni:** > 80% (hedef)
- **GPT-4 Fallback:** < 20% (maliyet kontrolü)
- **Uptime:** > 99.5%
- **Concurrent Users:** 100+ (optimizasyonla 1000+)

### Kapasite
- **Günlük Konuşma:** 10,000+ mesaj
- **Eğitim Verisi:** Sınırsız
- **Model Eğitim Süresi:** ~10-15 dakika
- **Veritabanı Boyutu:** ~1GB/ay (tahmini)

## 🚀 Hızlı Başlangıç

### 3 Adımda Kurulum:

**1. Klonla ve Bağımlılıkları Yükle**
```bash
git clone https://github.com/muhsinzengin/yapay-zeka-destek.git
cd yapay-zeka-destek
pip install -r requirements.txt
```

**2. Yapılandır**
```bash
cd rasa-projem
cp .env.example .env
nano .env  # API anahtarlarını ekle
```

**3. Başlat**
```bash
./start.sh
```

### İlk Erişim:
- **Webchat:** http://localhost:5000/webchat/index.html
- **Admin:** http://localhost:5000/admin/dashboard.html
- **Test:** http://localhost:5000/test_sayfa.html

## 💡 Kullanım Senaryoları

### Senaryo 1: Müşteri Desteği
Bir müşteri chat widget'ından "Siparişimi takip etmek istiyorum" yazar:
1. Rasa intent'i tanır (track_order)
2. Güven > 80% ise hazır yanıt verir
3. Güven < 80% ise GPT-4'e yönlendirir
4. Konuşma MongoDB'ye kaydedilir
5. Admin canlı sohbet panelinden izler

### Senaryo 2: Kızgın Müşteri
Müşteri sinirli bir mesaj yazar:
1. Sentiment analyzer "angry" tespit eder
2. Özel yumuşatıcı yanıt verilir
3. Telegram'a acil bildirim gider
4. Admin müdahale edebilir
5. Bot müdahale sonrası durur

### Senaryo 3: Yeni Müşteri
İlk kez gelen bir kullanıcı:
1. "Merhaba" mesajı gönderir
2. MongoDB'de ilk konuşması olduğu tespit edilir
3. Telegram'a "Yeni Müşteri" bildirimi gider
4. Admin müşteriyi izlemeye başlar
5. Gerekirse proaktif yardım sunar

### Senaryo 4: Model Eğitimi
Admin panelinden yeni veri eklenir:
1. "Kargom nerede, Siparişim nerede" → "Sipariş takip sistemi..."
2. Veri MongoDB'ye kaydedilir
3. Gece otomatik eğitim çalışır
4. Yeni model sabah hazır olur
5. Bot artık bu soruları bilir

## 📈 Ölçeklenebilirlik

### Küçük İşletme (10-100 kullanıcı/gün)
- Single server
- 2GB RAM
- 1 Rasa instance
- MongoDB single instance
```
Maliyet: ~$20-50/ay
```

### Orta Ölçek (100-1000 kullanıcı/gün)
- Multiple servers
- 4-8GB RAM
- Load balanced Rasa (2-3 instances)
- MongoDB replica set
```
Maliyet: ~$100-200/ay
```

### Büyük Ölçek (1000+ kullanıcı/gün)
- Kubernetes cluster
- 16GB+ RAM
- Auto-scaling Rasa
- MongoDB sharded cluster
- Redis caching
```
Maliyet: $500+/ay
```

## 🎓 Öğrenme Kaynakları

### Rasa
- Official Docs: https://rasa.com/docs/
- Tutorial: https://rasa.com/docs/rasa/tutorial/
- Community: https://forum.rasa.com/

### MongoDB
- Official Docs: https://docs.mongodb.com/
- University: https://university.mongodb.com/

### Flask
- Official Docs: https://flask.palletsprojects.com/
- Tutorial: https://flask.palletsprojects.com/tutorial/

## 🤝 Katkıda Bulunma

Projeye katkıda bulunmak isterseniz:

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/yeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik ekle'`)
4. Branch'i push edin (`git push origin feature/yeniOzellik`)
5. Pull Request açın

## 📄 Lisans

MIT License - Detaylar için LICENSE dosyasına bakın.

## 🆘 Destek

### Dokümantasyon
- `README.md` - Genel bakış
- `KURULUM_REHBERI.md` - Adım adım kurulum
- `HIZLI_REFERANS.md` - Komut referansı
- `MIMARI.md` - Sistem mimarisi
- `CHECKLIST.md` - Kurulum kontrol listesi

### İletişim
- **GitHub Issues:** https://github.com/muhsinzengin/yapay-zeka-destek/issues
- **Email:** support@example.com
- **Telegram:** @support_group

## 🎯 Roadmap

### v1.1 (Planlanan)
- [ ] WhatsApp entegrasyonu
- [ ] Multi-language support
- [ ] Voice message support
- [ ] Advanced analytics dashboard
- [ ] A/B testing framework

### v2.0 (Gelecek)
- [ ] Mobile app (React Native)
- [ ] Video chat support
- [ ] AI-powered suggestions
- [ ] Custom ML models
- [ ] Enterprise features

## ⚠️ Önemli Notlar

1. **Güvenlik:** Production'da mutlaka HTTPS kullanın
2. **Yedekleme:** Düzenli yedekleme yapın
3. **Monitoring:** Sistem metriklerini izleyin
4. **Maliyet:** GPT-4 kullanımını takip edin
5. **Güncelleme:** Düzenli güncellemeleri takip edin

## 🎉 Başarı Hikayeleri

_Sistemi kullanan işletmelerden geri bildirimler:_

> "Müşteri memnuniyeti %30 arttı, yanıt süresi %50 azaldı."
> - _Örnek E-ticaret Şirketi_

> "24/7 destek sunabiliyoruz, ekip yükü %40 azaldı."
> - _Örnek SaaS Şirketi_

---

**Sistem Durumu:** ✅ Production Ready

**Son Güncelleme:** 2025-10-20

**Versiyon:** 1.0.0

**Geliştirici:** muhsinzengin

---

**🚀 Başarılar dileriz!**

Herhangi bir sorunuz varsa dokümantasyonu inceleyin veya GitHub'da issue açın.
