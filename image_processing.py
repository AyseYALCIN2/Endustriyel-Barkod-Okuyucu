import cv2
import numpy as np
from PIL import Image

def prepare_image(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")
    return image

def enhance_barcode_for_ocr(image, box):
    img_array = np.array(image)
    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    x1, y1, x2, y2 = map(int, box.xyxy[0])
    h_orig, w_orig, _ = img_cv.shape
    
    # Sağdan ve soldan %5 pay
    x1 = max(0, int(x1 - (x2-x1)*0.05))
    x2 = min(w_orig, int(x2 + (x2-x1)*0.05))
    y2 = min(h_orig, int(y2 + (y2-y1)*0.05))
    
    # Rakamların olduğu alt %40'lık kısmı alıyoruz
    y1_new = y1 + int((y2 - y1) * 0.60) 
    cropped_region = img_cv[y1_new:y2, x1:x2]
    
    # 1. Griye çevir ve 3 kat büyüt
    gray = cv2.cvtColor(cropped_region, cv2.COLOR_BGR2GRAY)
    large = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    
    # 2. Siyah-Beyaz Binarizasyon
    blur = cv2.GaussianBlur(large, (5, 5), 0)
    _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # --- YENİ VE KUSURSUZ ÇİZGİ TEMİZLEYİCİ ---
    binary_inv = cv2.bitwise_not(binary)
    contours, _ = cv2.findContours(binary_inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    img_h = binary_inv.shape[0]
    
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        
        # YENİ ŞART: 
        # 1. Eğer şekil tavan sınırına (en üste) çok yakınsa (y < img_h * 0.20)
        # 2. Ve eni boyundan darsa (yani ince uzunsa)
        if y < (img_h * 0.20) and w < (h * 0.80):
            # O sarkan barkod çizgisini beyaz (255) renge boyayarak yok et!
            cv2.drawContours(binary, [cnt], -1, 255, -1)
            
    return binary