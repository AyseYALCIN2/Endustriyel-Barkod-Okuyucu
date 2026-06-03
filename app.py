import streamlit as st
import easyocr
from ultralytics import YOLO
from PIL import Image
from image_processing import prepare_image, enhance_barcode_for_ocr

st.set_page_config(page_title="Endüstriyel Barkod Okuyucu", layout="centered")

@st.cache_resource
def load_models():
    yolo_model = YOLO('models/best.pt') 
    ocr_reader = easyocr.Reader(['en'])
    return yolo_model, ocr_reader

st.title("Endüstriyel Barkod & Seri No Okuyucu 📦")
st.write("Sistemin okumasını istediğiniz etiketi yüklemek veya kamerayla çekmek için aşağıdaki butona tıklayın.")

try:
    model, reader = load_models()
except Exception as e:
    st.error("Model dosyası (best.pt) bulunamadı! 'models' klasörünü kontrol edin.")
    st.stop()

def process_and_display(image):
    with st.spinner("Yapay zeka görseli işliyor..."):
        results = model(image)
        
        if len(results[0].boxes) == 0:
            st.warning("Görselde barkod/etiket tespit edilemedi. Lütfen daha net bir açıdan deneyin.")
            return

        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Görüntüyü temizle, üstteki çizgileri at ve sadece rakamları al
                processed_image = enhance_barcode_for_ocr(image, box)
                
                # Sadece OCR'ın okuduğu o incecik temiz şeridi ekrana bas
                st.image(processed_image, caption="Yapay Zekanın Baktığı Odak Noktası", width=400)
                
                # EasyOCR Ayarları: paragraph=True ile uzaktaki 4'ü de aynı kelime bloğuna dahil ediyoruz
                ocr_result = reader.readtext(processed_image, allowlist='0123456789', paragraph=True)
                
                if ocr_result:
                    raw_text = "".join([res[1] for res in ocr_result])
                    cleaned_text = raw_text.replace(" ", "")
                    st.success(f"Sistem Çıktısı (Okunan Metin): **{cleaned_text}**")
                else:
                    st.error("Etiket tespit edildi ancak metin okunamadı.")

# --- ARAYÜZ ---
uploaded_file = st.file_uploader("Fotoğraf Çek veya Galeriden Seç", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = prepare_image(uploaded_file)
    st.image(image, caption='Sisteme Gelen Orijinal Fotoğraf', width=400)
    process_and_display(image)

st.markdown("---")
st.caption("Bilişim Sistemleri ve Teknolojileri | Dönem Projesi")