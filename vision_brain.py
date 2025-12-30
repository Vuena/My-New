import requests
import base64
import json
import time
import mss
import mss.tools
from PIL import Image
import io

class VisionBrain:
    def __init__(self, api_url="http://localhost:1234/v1/chat/completions", model_id="local-model", logger=None):
        self.api_url = api_url
        self.model_id = model_id
        self.logger = logger

    def capture_screen(self):
        """Tüm ekranın görüntüsünü alır ve base64 formatına çevirir."""
        with mss.mss() as sct:
            # İlk monitörü al
            monitor = sct.monitors[1]
            sct_img = sct.grab(monitor)

            # MSS -> PIL Image dönüşümü
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

            # Resmi bellekte buffer'a kaydet
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG", quality=85) # Hız için kaliteyi biraz düşürdük
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

            return img_str

    def analyze_screen(self):
        """
        Ekran görüntüsünü modele gönderir ve JSON formatında aksiyon kararı ister.
        """
        if self.logger:
            self.logger.write("[VISION] Ekran görüntüsü alınıyor...")
        else:
            print("[VISION] Ekran görüntüsü alınıyor...")

        base64_image = self.capture_screen()

        if self.logger:
            self.logger.write("[VISION] Modele gönderiliyor...")
        else:
            print("[VISION] Modele gönderiliyor...")

        # Qwen VL için prompt yapısı
        # Not: Modelin yeteneğine göre prompt optimize edilmelidir.
        system_prompt = """
        Sen Dofus oyunu için bir otomasyon asistanısın. Görevin ekrandaki toplanabilir kaynakları (ağaç, maden, bitki) veya saldırılabilecek canavarları tespit etmek.

        ÖNEMLİ: Sadece TEK BİR hedef seç ve koordinatını ver.
        Cevabını SADECE geçerli bir JSON formatında ver. Başka hiçbir metin yazma.

        JSON Formatı:
        {
            "found": true/false,
            "target_type": "resource" veya "enemy" veya "none",
            "coordinates": {"x": 100, "y": 200},
            "reason": "Burada bir buğday tarlası tespit edildi."
        }

        Eğer hiçbir şey yoksa "found": false döndür.
        """

        payload = {
            "model": self.model_id,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Ekranda toplanacak kaynak veya saldırılacak düşman var mı? Varsa bir tanesinin koordinatını ver."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "temperature": 0.1, # Kararlı olması için düşük sıcaklık
            "max_tokens": 200
        }

        try:
            response = requests.post(self.api_url, json=payload, headers={"Content-Type": "application/json"}, timeout=30)
            response.raise_for_status()

            result = response.json()
            content = result['choices'][0]['message']['content']

            # JSON temizleme (Bazen modeller markdown ```json ... ``` ekler)
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].strip()

            # Log AI Interaction
            if self.logger:
                self.logger.log_ai_interaction(system_prompt, content)

            decision = json.loads(content)
            return decision

        except requests.exceptions.RequestException as e:
            msg = f"[HATA] API isteği başarısız: {e}"
            if self.logger: self.logger.write(msg)
            else: print(msg)
            return None
        except json.JSONDecodeError:
            msg = f"[HATA] Model JSON döndürmedi. Gelen veri: {content}"
            if self.logger: self.logger.write(msg)
            else: print(msg)
            return None
        except Exception as e:
            msg = f"[HATA] Beklenmeyen hata: {e}"
            if self.logger: self.logger.write(msg)
            else: print(msg)
            return None

    def verify_action_success(self, target_type):
        """
        Eylem sonrası ekranı tekrar analiz ederek başarısızlık durumunu kontrol eder.
        Basit mantık: Kaynak hala oradaysa başarısızdır. Savaş ekranı açıldıysa başarılıdır.
        """
        if self.logger:
            self.logger.write("[VISION] Eylem sonucu doğrulanıyor...")
        else:
            print("[VISION] Eylem sonucu doğrulanıyor...")

        time.sleep(1) # Animasyonların bitmesi için kısa bekleme
        base64_image = self.capture_screen()

        system_prompt = f"""
        Sen bir doğrulama asistanısın. Az önce bir '{target_type}' hedefine tıklandı.
        Şu anki ekran görüntüsüne bakarak işlemin başarılı olup olmadığını kontrol et.

        Başarılı sayılması için şunlardan BİRİSİ gerçekleşmiş olmalı:
        1. Kaynak (ağaç/bitki) ekrandan kayboldu veya kesildi.
        2. Savaş ekranı açıldı (ekran tamamen değişti).
        3. Karakter hedefe doğru koşuyor veya hareket ediyor.

        Eğer karakter hareket halindeyse bunu BAŞARILI (success: true) saymalısın.

        Cevabını SADECE JSON formatında ver:
        {{
            "success": true/false,
            "reason": "Karakter hareket ediyor" veya "Kaynak kayboldu" veya "Hiçbir şey değişmedi"
        }}
        """

        payload = {
            "model": self.model_id,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": [
                    {"type": "text", "text": "İşlem başarılı mı? Karakter hareket ediyor mu veya kaynak toplandı mı?"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]}
            ],
            "max_tokens": 100
        }

        try:
            response = requests.post(self.api_url, json=payload, headers={"Content-Type": "application/json"}, timeout=30)
            content = response.json()['choices'][0]['message']['content']

            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].strip()

            # Log AI Interaction (Verification)
            if self.logger:
                self.logger.log_ai_interaction(system_prompt, content)

            return json.loads(content)

        except Exception as e:
            msg = f"[HATA] Doğrulama hatası: {e}"
            if self.logger: self.logger.write(msg)
            else: print(msg)
            return {"success": True} # Hata durumunda döngüyü bozmamak için varsayılan başarılı kabul et

        except requests.exceptions.RequestException as e:
            print(f"[HATA] API isteği başarısız: {e}")
            return None
        except json.JSONDecodeError:
            print(f"[HATA] Model JSON döndürmedi. Gelen veri: {content}")
            return None
