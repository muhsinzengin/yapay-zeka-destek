# Sistem Mimarisi

## 📐 Genel Mimari

```
┌─────────────────────────────────────────────────────────────────┐
│                         Kullanıcılar                              │
│                  (Web, Telegram, Mobile)                          │
└────────────────────┬────────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌──────────────┐         ┌──────────────┐
│  Webchat UI  │         │   Telegram   │
│  (Port 5000) │         │   Webhook    │
└──────┬───────┘         └──────┬───────┘
       │                        │
       └────────────┬───────────┘
                    │
                    ▼
         ┌─────────────────┐
         │   Flask API     │
         │   (Port 5000)   │
         │   - Statistics  │
         │   - Training    │
         │   - Admin Auth  │
         └────────┬────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
┌──────────────┐    ┌──────────────┐
│ Rasa Server  │    │   MongoDB    │
│ (Port 5005)  │───▶│   Database   │
│   - NLU      │    │   - Logs     │
│   - Core     │    │   - Training │
│   - Policies│    │   - Stats    │
└──────┬───────┘    └──────────────┘
       │
       ▼
┌──────────────┐
│Action Server │
│ (Port 5055)  │
│  - MongoDB   │
│  - Telegram  │
│  - GPT-4     │
│  - Sentiment │
└──────────────┘
       │
       ├──────────────────┐
       │                  │
       ▼                  ▼
┌──────────────┐   ┌──────────────┐
│  Telegram    │   │   OpenAI     │
│    API       │   │   GPT-4 API  │
└──────────────┘   └──────────────┘
```

## 🔧 Bileşenler

### 1. Rasa Server (Port 5005)
**Görev:** Doğal dil işleme ve konuşma yönetimi

**Modüller:**
- **NLU (Natural Language Understanding):**
  - WhitespaceTokenizer: Metni kelimelerine ayırır
  - RegexFeaturizer: Düzenli ifade özellikleri çıkarır
  - LexicalSyntacticFeaturizer: Kelime özellikleri
  - CountVectorsFeaturizer: Kelime sayımı ve n-gram özellikleri
  - DIETClassifier: Intent ve entity tanıma
  - EntitySynonymMapper: Entity eşleştirme
  - ResponseSelector: Yanıt seçimi
  - FallbackClassifier: Düşük güven durumlarını yönetir

- **Policies (Dialog Yönetimi):**
  - MemoizationPolicy: Ezberlenen konuşmaları hatırlar
  - RulePolicy: Kural tabanlı yanıtlar
  - TEDPolicy: Makine öğrenmesi tabanlı dialog yönetimi

**Güven Eşiği:** 80% (0.8)
- > 80%: Rasa yanıt verir
- < 80%: GPT-4'e yönlendirilir

### 2. Action Server (Port 5055)
**Görev:** Custom action'ları çalıştırır

**Action'lar:**
1. **action_log_conversation**
   - Her konuşmayı MongoDB'ye kaydeder
   - Tarih, saat, user_id, mesaj, intent, güven skoru

2. **action_analyze_sentiment**
   - Mesajın duygusunu analiz eder
   - Pozitif, negatif, nötr, kızgın
   - Türkçe anahtar kelimeler kullanır

3. **action_notify_telegram**
   - Yeni müşteri geldiğinde bildirim gönderir
   - Admin'e Telegram üzerinden mesaj atar

4. **action_fallback_gpt4**
   - Düşük güven durumlarında GPT-4'ü çağırır
   - Maliyeti MongoDB'ye kaydeder
   - Türkçe yanıt üretir

5. **action_admin_authenticate**
   - 6 haneli kod üretir
   - Telegram'a gönderir
   - 5 dakika geçerli

6. **action_save_training_data**
   - Admin panelinden gelen verileri kaydeder
   - NLU formatına çevirir

### 3. Flask API Server (Port 5000)
**Görev:** Admin panel backend'i ve dosya sunumu

**Endpoint'ler:**

**Sağlık Kontrolleri:**
- `GET /api/health/mongo` - MongoDB durumu
- `GET /api/health/telegram` - Telegram konfigürasyonu

**İstatistikler:**
- `GET /api/statistics?period=daily|weekly|monthly|yearly|total`
  - Konuşma sayısı
  - Benzersiz kullanıcı sayısı
  - GPT-4 kullanımı
  - Maliyet hesaplaması

**Eğitim Verisi:**
- `GET /api/training-data` - Listele
- `POST /api/training-data` - Ekle
- `DELETE /api/training-data/:id` - Sil

**Canlı Konuşmalar:**
- `GET /api/live-conversations` - Aktif konuşmalar
- `GET /api/conversation/:user_id` - Kullanıcı geçmişi
- `POST /api/intervention` - Admin müdahalesi

**Model Eğitimi:**
- `POST /api/train-model` - Eğitimi başlat

**Admin:**
- `POST /api/admin/request-code` - Kod talep et
- `POST /api/admin/verify-code` - Kodu doğrula

### 4. MongoDB Database
**Görev:** Veri saklama ve analitik

**Collections:**

**conversations:**
```javascript
{
  user_id: String,
  message: String,
  intent: String,
  confidence: Number,
  timestamp: Date,
  sender: String  // 'user' veya 'bot' veya 'admin'
}
```

**training_data:**
```javascript
{
  intent: String,
  questions: [String],
  answer: String,
  created_at: Date
}
```

**admin_codes:**
```javascript
{
  code: String,
  created_at: Date,
  expires_at: Date,
  used: Boolean
}
```

**gpt4_usage:**
```javascript
{
  user_id: String,
  message: String,
  response: String,
  timestamp: Date,
  estimated_tokens: Number
}
```

**İndeksler:**
- conversations: (timestamp DESC), (user_id)
- training_data: (intent)
- admin_codes: (expires_at) TTL
- gpt4_usage: (timestamp DESC)

### 5. Telegram Bot Integration
**Görev:** Bildirimler ve admin auth

**Özellikler:**
- Yeni müşteri bildirimi
- Admin giriş kodu gönderimi
- Müdahale gerekli bildirimi

**Mesaj Formatı:**
```
🆕 Yeni Müşteri!
👤 Kullanıcı: user_123
💬 İlk Mesaj: Merhaba...

🔐 Admin Giriş Kodu
Kodunuz: 123456
⏱ Bu kod 5 dakika geçerlidir.
```

### 6. GPT-4 Turbo Integration
**Görev:** Fallback AI yanıtları

**Konfigürasyon:**
- Model: gpt-4-turbo-preview
- Temperature: 0.7
- Max Tokens: 500
- System Prompt: Türkçe müşteri destek asistanı

**Maliyet Takibi:**
- Her kullanım MongoDB'ye kaydedilir
- Token tahmini yapılır
- Dashboard'da gösterilir

### 7. Web Interfaces

**Webchat (Sağ Yarım Ekran):**
- Modern gradient tasarım
- Gerçek zamanlı mesajlaşma
- Typing indicator
- Responsive design

**Admin Panel:**

**Dashboard:**
- Günlük/haftalık/aylık/yıllık stats
- GPT-4 maliyet analizi
- Son aktiviteler

**Eğitim:**
- Soru-cevap ekleme (virgülle ayrılmış)
- Mevcut verileri listeleme
- Silme işlemi
- Model eğitimi tetikleme

**Canlı Sohbet:**
- Aktif konuşmaları listeleme
- Mesaj geçmişini görüntüleme
- Admin müdahalesi (bot otomatik durur)
- Gerçek zamanlı güncelleme

**Test Sayfası:**
- Sistem sağlık kontrolleri
- Cümle testi
- Yanıt süresi ölçümü
- Güven skoru gösterimi

## 🔄 Veri Akışı

### Kullanıcı Mesajı Akışı:
```
1. Kullanıcı mesaj yazar (Webchat veya Telegram)
   ↓
2. Mesaj Rasa Server'a gönderilir
   ↓
3. NLU modülü intent ve entity'leri tespit eder
   ↓
4. Policy güven skorunu değerlendirir
   ↓
5a. Güven > 80%:
    → Rasa yanıt verir
    → action_log_conversation çalışır
    → MongoDB'ye kaydedilir
   
5b. Güven < 80%:
    → action_fallback_gpt4 çalışır
    → GPT-4'ten yanıt alınır
    → Maliyet kaydedilir
   ↓
6. Yanıt kullanıcıya iletilir
```

### Yeni Müşteri Bildirimi Akışı:
```
1. Kullanıcı ilk mesajını gönderir
   ↓
2. action_notify_telegram çalışır
   ↓
3. MongoDB'de kullanıcı konuşma sayısı kontrol edilir
   ↓
4. İlk konuşma ise Telegram'a bildirim gönderilir
   ↓
5. Admin Telegram'dan bildirim alır
```

### Admin Giriş Akışı:
```
1. Admin panel açılır
   ↓
2. "Kod İste" butonuna tıklanır
   ↓
3. Flask API /api/admin/request-code endpoint'ini çağırır
   ↓
4. 6 haneli kod üretilir
   ↓
5. MongoDB'ye kaydedilir (5 dk TTL)
   ↓
6. Telegram'a gönderilir
   ↓
7. Admin kodu girer
   ↓
8. /api/admin/verify-code ile doğrulama yapılır
   ↓
9. Başarılı ise session token döner
   ↓
10. Admin panel erişimi sağlanır
```

### Otomatik Eğitim Akışı:
```
1. Cron job tetiklenir (Her gece 02:00)
   ↓
2. automated_training.py çalışır
   ↓
3. MongoDB'den konuşmalar çekilir
   ↓
4. NLU formatına dönüştürülür
   ↓
5. data/nlu.yml güncellenir
   ↓
6. rasa train komutu çalıştırılır
   ↓
7. Yeni model models/ klasörüne kaydedilir
   ↓
8. Eski loglar temizlenir (30 gün+)
```

## 🔐 Güvenlik Katmanları

### 1. Network Security
- HTTPS/TLS şifreleme
- CORS yapılandırması
- Firewall kuralları

### 2. Authentication
- Telegram 6 haneli kod doğrulama
- Session token yönetimi
- 5 dakikalık kod süresi

### 3. Data Security
- MongoDB authentication
- .env dosyası şifreleme
- API key koruması

### 4. Application Security
- Input validation
- SQL injection koruması (NoSQL)
- Rate limiting

## 📊 Performans Optimizasyonları

### MongoDB
- İndeksler (timestamp, user_id)
- Aggregation pipeline'ları
- TTL indeksleri (auto cleanup)

### Rasa
- Model caching
- Batch processing
- Optimized pipeline

### Flask
- Gunicorn multi-worker
- Static file caching
- Database connection pooling

## 🔄 Yedekleme Stratejisi

### Otomatik Yedekler
- **Veritabanı:** Haftalık (Pazar 03:00)
- **Format:** JSON (BSON compatible)
- **Saklama:** 4 hafta
- **Konum:** backups/ klasörü

### Manuel Yedekler
- **Modeller:** models/ klasörü
- **Konfigürasyon:** .env, config.yml
- **Kod:** Git repository

## 📈 Ölçeklenebilirlik

### Horizontal Scaling
- Multiple Rasa instances (load balancer)
- MongoDB replica set
- Redis for session storage

### Vertical Scaling
- Daha fazla RAM (model için)
- Daha fazla CPU (training için)
- SSD storage (hız için)

## 🎯 Monitoring Points

### Metrikler
- Response time (< 2 saniye hedef)
- Confidence scores (> 80% hedef)
- GPT-4 fallback oranı (< 20% hedef)
- Conversation count
- User retention

### Loglar
- Application logs (logs/*.log)
- MongoDB logs (/var/log/mongodb/)
- Nginx logs (/var/log/nginx/)
- System logs (journalctl)

## 🚨 Hata Yönetimi

### Error Handling
- Try-catch blokları
- Fallback yanıtları
- Graceful degradation
- Error logging

### Recovery
- Automatic restart (systemd)
- Database backup restore
- Model rollback

---

**Not:** Bu mimari üretim ortamına hazırdır ancak trafiğe göre optimize edilmelidir.
