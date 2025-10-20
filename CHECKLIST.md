# Kurulum ve Yapılandırma Kontrol Listesi

Sistemi kurmadan önce bu listeyi takip edin. Her adımı tamamladıktan sonra işaretleyin.

## ✅ Ön Hazırlık

### Sistem Gereksinimleri
- [ ] Python 3.10 kurulu
- [ ] MongoDB 4.4+ kurulu ve çalışıyor
- [ ] Git kurulu
- [ ] En az 4GB RAM mevcut
- [ ] En az 10GB disk alanı mevcut
- [ ] İnternet bağlantısı aktif

### Hesaplar ve Anahtarlar
- [ ] Telegram hesabı mevcut
- [ ] OpenAI hesabı oluşturuldu (GPT-4 için)
- [ ] GitHub hesabı mevcut (isteğe bağlı)

## 📥 Kurulum

### Repository ve Bağımlılıklar
- [ ] Repository klonlandı
- [ ] Sanal ortam oluşturuldu (önerilen)
- [ ] requirements.txt yüklendi
- [ ] Tüm bağımlılıklar başarıyla kuruldu

### Dizin Yapısı
- [ ] rasa-projem klasörü mevcut
- [ ] models/ klasörü oluşturuldu
- [ ] backups/ klasörü oluşturuldu
- [ ] logs/ klasörü oluşturuldu

## 🔧 Yapılandırma

### Ortam Değişkenleri (.env)
- [ ] .env.example .env olarak kopyalandı
- [ ] MONGODB_URI ayarlandı
- [ ] MONGODB_DATABASE ayarlandı
- [ ] TELEGRAM_BOT_TOKEN ayarlandı
- [ ] TELEGRAM_ADMIN_CHAT_ID ayarlandı
- [ ] OPENAI_API_KEY ayarlandı
- [ ] SECRET_KEY oluşturuldu
- [ ] .env dosyası .gitignore'a eklendi

### Telegram Bot Kurulumu
- [ ] @BotFather ile yeni bot oluşturuldu
- [ ] Bot token'ı alındı ve .env'ye eklendi
- [ ] Admin chat ID öğrenildi (@userinfobot)
- [ ] Admin chat ID .env'ye eklendi
- [ ] Bot ile test mesajı gönderildi

### MongoDB Kurulumu
- [ ] MongoDB servisi çalışıyor
- [ ] mongo komutunu ile bağlantı test edildi
- [ ] rasa_chatbot veritabanı oluşturuldu
- [ ] Admin kullanıcısı oluşturuldu (üretim için)
- [ ] Bağlantı .env'de doğru yapılandırıldı

### OpenAI API Kurulumu
- [ ] OpenAI hesabı oluşturuldu
- [ ] API anahtarı oluşturuldu
- [ ] API anahtarı .env'ye eklendi
- [ ] Kredi bakiyesi kontrol edildi
- [ ] Usage limits ayarlandı (maliyet kontrolü)

## 🎓 İlk Eğitim

### Model Hazırlığı
- [ ] config.yml kontrol edildi
- [ ] domain.yml kontrol edildi
- [ ] data/nlu.yml oluşturuldu
- [ ] rasa train komutu çalıştırıldı
- [ ] Model başarıyla eğitildi
- [ ] models/ klasöründe .tar.gz dosyası oluştu

## 🚀 Servis Başlatma

### Manuel Test
- [ ] Rasa server başlatıldı (port 5005)
- [ ] Action server başlatıldı (port 5055)
- [ ] Flask API başlatıldı (port 5000)
- [ ] Tüm servisler hatasız çalışıyor

### Otomatik Başlatma
- [ ] start.sh script'i test edildi
- [ ] Tüm servisler otomatik başladı
- [ ] Log dosyaları oluşturuldu
- [ ] PID dosyaları oluşturuldu

## 🧪 Test ve Doğrulama

### Webchat Testi
- [ ] http://localhost:5000/webchat/index.html açıldı
- [ ] Chat widget görünüyor
- [ ] "Merhaba" mesajı gönderildi
- [ ] Bot yanıt verdi
- [ ] Konuşma MongoDB'ye kaydedildi

### Admin Panel Testi
- [ ] http://localhost:5000/admin/dashboard.html açıldı
- [ ] Telegram'a kod gönderildi
- [ ] Kod ile giriş yapıldı
- [ ] Dashboard istatistikleri görüntülendi

### Test Sayfası Kontrolü
- [ ] http://localhost:5000/test_sayfa.html açıldı
- [ ] Rasa sunucusu yeşil ✅
- [ ] MongoDB yeşil ✅
- [ ] Action server yeşil ✅
- [ ] Telegram bot yapılandırıldı ✅
- [ ] Test cümlesi denenmiş
- [ ] Yanıt süresi makul (< 3 saniye)

### API Endpoint Testleri
- [ ] GET /api/statistics test edildi
- [ ] GET /api/training-data test edildi
- [ ] POST /api/training-data test edildi
- [ ] GET /api/live-conversations test edildi
- [ ] POST /api/train-model test edildi

### Telegram Entegrasyonu
- [ ] Yeni konuşma başlatıldı
- [ ] Telegram'a bildirim geldi
- [ ] Bildirimde kullanıcı ID doğru
- [ ] Bildirimde mesaj doğru

### GPT-4 Fallback Testi
- [ ] Düşük güvenli mesaj gönderildi
- [ ] GPT-4 yanıt verdi
- [ ] Maliyet MongoDB'ye kaydedildi
- [ ] Dashboard'da maliyet gösterildi

## 📊 İstatistik ve Monitoring

### Dashboard Verileri
- [ ] Bugünkü konuşmalar sayılıyor
- [ ] Haftalık istatistikler doğru
- [ ] Aylık istatistikler doğru
- [ ] GPT-4 maliyeti hesaplanıyor
- [ ] Son aktiviteler listeleniyor

### Eğitim Paneli
- [ ] Yeni eğitim verisi eklendi
- [ ] Virgülle ayrılmış sorular çalışıyor
- [ ] Veriler MongoDB'de görünüyor
- [ ] Arama fonksiyonu çalışıyor
- [ ] Silme işlemi çalışıyor
- [ ] Model eğitimi tetiklendi

### Canlı Sohbet Paneli
- [ ] Aktif konuşmalar listeleniyor
- [ ] Konuşma geçmişi görüntüleniyor
- [ ] Müdahale mesajı gönderildi
- [ ] Bot müdahale sonrası durdu
- [ ] Otomatik yenileme çalışıyor

## 🔄 Otomasyonlar

### Cron Job Kurulumu
- [ ] crontab.example incelendi
- [ ] crontab -e ile düzenleme açıldı
- [ ] Gece eğitimi (02:00) eklendi
- [ ] Haftalık yedek (Pazar 03:00) eklendi
- [ ] Dosya yolları doğru ayarlandı
- [ ] Cron servisi aktif

### Otomatik Eğitim Testi
- [ ] automated_training.py manuel çalıştırıldı
- [ ] Konuşmalar NLU'ya aktarıldı
- [ ] Model yeniden eğitildi
- [ ] Eski loglar temizlendi
- [ ] Script hatasız tamamlandı

### Otomatik Yedekleme Testi
- [ ] database_backup.py manuel çalıştırıldı
- [ ] backups/ klasöründe yedek oluştu
- [ ] JSON formatı geçerli
- [ ] Tüm collection'lar yedeklendi
- [ ] Eski yedekler temizlendi (4 hafta+)

## 🔐 Güvenlik

### Temel Güvenlik
- [ ] .env dosyası git'e eklenmiş
- [ ] .gitignore doğru yapılandırılmış
- [ ] API anahtarları şifreli saklanıyor
- [ ] Güçlü şifreler kullanılıyor

### Network Güvenliği
- [ ] Firewall kuralları ayarlandı
- [ ] Sadece gerekli portlar açık
- [ ] MongoDB dış erişime kapalı
- [ ] CORS doğru yapılandırılmış

### Üretim Güvenliği (Production)
- [ ] HTTPS sertifikası kuruldu (Let's Encrypt)
- [ ] Nginx veya Apache yapılandırıldı
- [ ] SSL/TLS zorunlu kılındı
- [ ] MongoDB authentication aktif
- [ ] Strong password policy uygulandı

## 📈 Performans Optimizasyonu

### MongoDB Optimizasyonu
- [ ] İndeksler oluşturuldu
- [ ] Slow query log aktif
- [ ] Connection pooling ayarlandı
- [ ] Disk alanı izleniyor

### Rasa Optimizasyonu
- [ ] Model boyutu optimize edildi
- [ ] Pipeline ayarları yapıldı
- [ ] Cache ayarları yapıldı
- [ ] Memory limitleri ayarlandı

### Flask Optimizasyonu
- [ ] Gunicorn multi-worker kullanılıyor
- [ ] Static dosyalar cache'leniyor
- [ ] Database connection pool ayarlandı

## 📝 Dokümantasyon

### Dokümantasyon Kontrolü
- [ ] README.md okundu
- [ ] KURULUM_REHBERI.md takip edildi
- [ ] HIZLI_REFERANS.md yer işaretlendi
- [ ] MIMARI.md incelendi
- [ ] Bu checklist tamamlandı

### Ekip Eğitimi
- [ ] Sistem mimarisi anlatıldı
- [ ] Admin panel kullanımı gösterildi
- [ ] Sorun giderme adımları paylaşıldı
- [ ] Acil durum prosedürleri belgelendi

## 🚨 Acil Durum Hazırlığı

### Yedekleme Stratejisi
- [ ] Yedekleme planı oluşturuldu
- [ ] Farklı konumda yedek tutuluyor
- [ ] Restore prosedürü test edildi
- [ ] Yedekleme logları izleniyor

### Monitoring ve Alerting
- [ ] Uptime monitoring ayarlandı
- [ ] Error alerting yapılandırıldı
- [ ] Disk alanı monitoring aktif
- [ ] Response time tracking çalışıyor

### Disaster Recovery
- [ ] Sistem yedekleri alındı
- [ ] Restore planı oluşturuldu
- [ ] Failover stratejisi belirlendi
- [ ] İletişim planı hazırlandı

## 📞 Destek ve Bakım

### Düzenli Bakım
- [ ] Haftalık log kontrolü planlandı
- [ ] Aylık performans analizi planlandı
- [ ] Çeyreklik güvenlik güncellemesi planlandı
- [ ] Yıllık sistem yenileme planlandı

### İletişim Kanalları
- [ ] GitHub Issues etkin
- [ ] Destek email adresi belirlendi
- [ ] Telegram grup oluşturuldu (opsiyonel)
- [ ] Dokümantasyon wiki kuruldu (opsiyonel)

## 🎉 Final Kontrol

### Sistem Sağlığı
- [ ] Tüm servisler çalışıyor
- [ ] Tüm testler geçti
- [ ] Log dosyaları temiz (kritik hata yok)
- [ ] Performans hedefleri karşılanıyor
- [ ] Güvenlik kontrolleri geçti

### Kullanıma Hazırlık
- [ ] Kullanıcı dokümantasyonu hazır
- [ ] Admin eğitimi tamamlandı
- [ ] Destek kanalları aktif
- [ ] Monitoring kuruldu
- [ ] Yedekleme çalışıyor

### Production'a Alma
- [ ] Staging ortamda test edildi
- [ ] Load test yapıldı
- [ ] Security audit tamamlandı
- [ ] Rollback planı hazır
- [ ] Production deploy tamamlandı

---

## 📊 Skor

**Toplam işaretlenen görevler:** ___ / 200+

- **0-50:** Kurulum başlangıç aşamasında
- **51-100:** Temel kurulum tamamlandı
- **101-150:** İleri düzey yapılandırma yapıldı
- **151-200:** Production'a hazır
- **200+:** Tam optimizasyonlu enterprise kurulum ✨

---

**Not:** Bu checklist'i yazdırıp fiziksel olarak da takip edebilirsiniz. Her sprint'te ilerlemenizi gözden geçirin.

**İyi çalışmalar! 🚀**
