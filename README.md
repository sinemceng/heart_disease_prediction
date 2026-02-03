# Yapay Zeka Destekli Kalp Hastalığı Risk Analiz Paneli ❤️

#### Bu proje, UCI Heart Disease veri seti kullanılarak geliştirilmiş, uçtan uca bir makine öğrenmesi uygulamasıdır. Kullanıcıların demografik ve klinik sağlık verilerini analiz ederek kalp hastalığı riskini tahmin eder.

## 📊 Proje Mutfak: Ar-Ge Süreci (.ipynb)

Projenin temelini oluşturan heart_disease_prediction.ipynb dosyasında şu aşamalar gerçekleştirilmiştir:

* Veri Ön İşleme: Eksik veriler (missing values) sayısal sütunlar için median, kategorik sütunlar için mode stratejisi ile doldurulmuştur.

* Özellik Mühendisliği: id, dataset gibi tahmine etkisi olmayan sütunlar elenmiş, hedef değişken (num) "Risk Var/Yok" şeklinde ikili sınıflandırmaya (binary classification) dönüştürülmüştür.

* Encoding: Kategorik veriler One-Hot Encoding yöntemiyle modele uygun hale getirilmiştir.

* Model Seçimi: Random Forest algoritması kullanılmış ve doğruluk oranları karşılaştırılmıştır.

### 🎯 Model Performansı

- Algoritma: Random Forest Classifier

- Doğruluk (Accuracy): %83.70

- Metrikler: Precision, Recall ve F1-Score değerleri dengeli bir performans sergilemektedir (Notebook içerisinde detaylı rapor mevcuttur).

## ✨ Uygulama Özellikleri

- Dinamik Risk Derecelendirmesi: Modelin olasılık çıktılarına göre Düşük, Orta ve Yüksek risk seviyeleri belirlenir.

- Feature Importance: Tahmini en çok etkileyen 5 faktör (örn: yaş, göğüs ağrısı tipi, ST depresyonu) grafiksel olarak sunulur.

- Veri Dışa Aktarma: Yapılan tüm analizler tarih ve saat damgasıyla birlikte Excel (.xlsx) raporu olarak indirilebilir.

- Kullanıcı Dostu Arayüz: Streamlit tabanlı, mor/lila temalı profesyonel dashboard tasarımı.

## Kurulum ve Çalıştırma

Projeyi yerelinizde çalıştırmak için:

1. Depoyu klonlayın: git clone https://github.com/sinemceng/heart_disease_prediction.git

2. Gerekli kütüphaneleri yükleyin: pip install -r requirements.txt

3. Uygulamayı başlatın: streamlit run main.py

## Geliştirici
**Sinem Özdemir**

Bilgisayar Mühendisliği Öğrencisi

[Linkedin Profilim](www.linkedin.com/in/sinemozdemir1) | [E-posta Adresim](sinozdemir04@gmail.com)
