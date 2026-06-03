# 📦 Endüstriyel Barkod ve Seri No Okuma Sistemi

Bu proje, endüstriyel üretim bantlarında ve lojistik süreçlerinde karşılaşılan düşük kaliteli, kavisli ve zorlu ışık koşullarına sahip etiketlerdeki seri numaralarını tespit etmek için geliştirilmiş yapay zeka destekli bir okuma sistemidir.

## 🚀 Kullanılan Teknolojiler
* **Arayüz:** Streamlit
* **Nesne Tespiti (Object Detection):** YOLO (Özel eğitilmiş model)
* **Görüntü İşleme:** OpenCV (Adaptif Binarizasyon, Kontur Analizi)
* **Optik Karakter Tanıma (OCR):** EasyOCR

## 💡 Geliştirilen Mühendislik Çözümleri
* **Kontur Analizi ile Guard Bars Temizliği:** Barkodların aşağı sarkan koruyucu çizgileri, matematiksel şekil analiziyle tespit edilip silinmiştir.
* **ROI (İlgi Alanı) Çıkarımı:** Yapay zekanın halüsinasyon görmesini engellemek için yalnızca rakamların bulunduğu şerit izole edilmiştir.
* **Adaptif Thresholding:** Silindirik ve gölgeli yüzeylerde rakamların içinin boşalmasını önleyerek matbaa baskısı netliği elde edilmiştir.

## 🛠️ Nasıl Çalıştırılır?
1. Gerekli kütüphaneleri yükleyin: `pip install -r requirements.txt` (Gereksinimler dosyanız varsa)
2. Modeli çalıştırın: `streamlit run app.py`
