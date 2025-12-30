import time
import sys
import pyautogui
import random
import datetime
import os
from memory import DynamicMemory
from human_mouse import HumanMouse
from vision_brain import VisionBrain
from logger import Logger

def main():
    # Logger'ı başlat
    log = Logger()
    log.write("=== Dofus AI Ajanı Başlatılıyor ===")
    log.write("Çıkış için Ctrl+C basınız.")

    # Modülleri başlat
    memory = DynamicMemory()
    mouse = HumanMouse()
    # Logger'ı vision_brain'e ilet (AI logları için)
    brain = VisionBrain(api_url="http://localhost:1234/v1/chat/completions", model_id="local-model", logger=log)

    # Ekran boyutlarını al (Koordinat ölçekleme için)
    screen_w, screen_h = pyautogui.size()

    # Yasaklı bölgeye kaç kez denk gelindiğini sayar
    forbidden_streak = 0

    while True:
        try:
            # 1. Adım: Görüntü Al ve Analiz Et
            decision = brain.analyze_screen()

            if not decision:
                log.write("[DÖNGÜ] Karar alınamadı, tekrar deneniyor...")
                time.sleep(1)
                continue

            # 2. Adım: Kararı Değerlendir
            if decision.get("found"):
                raw_x = decision["coordinates"]["x"]
                raw_y = decision["coordinates"]["y"]

                if raw_x <= 1000 and raw_y <= 1000 and screen_w > 1000:
                    target_x = int((raw_x / 1000) * screen_w)
                    target_y = int((raw_y / 1000) * screen_h)
                    log.write(f"[KOORDİNAT] Normalize ({raw_x}, {raw_y}) -> Ekran ({target_x}, {target_y})")
                else:
                    target_x = raw_x
                    target_y = raw_y

                reason = decision.get("reason", "Belirtilmemiş")

                log.write(f"[KARAR] Hedef bulundu: {decision['target_type']} @ ({target_x}, {target_y})")

                # 3. Adım: Hafıza Kontrolü (Neden-Sonuç)
                if memory.is_action_safe(target_x, target_y):
                    # Yasaklı olmayan güvenli bir hedef bulundu, sayacı sıfırla
                    forbidden_streak = 0

                    # 4. Adım: Eylemi Gerçekleştir
                    log.write(f"[EYLEM] Gidiliyor... Sebep: {reason}")

                    mouse.click(target_x, target_y)

                    # 5. Adım: Başarı Kontrolü
                    log.write("[KONTROL] Eylem sonucu analiz ediliyor...")
                    time.sleep(3)

                    result = brain.verify_action_success(decision['target_type'])

                    if result and not result.get("success", True):
                        log.write(f"[HATA] Eylem başarısız oldu! Sebep: {result.get('reason')}")
                        log.write(f"[ÖĞRENME] Koordinat ({target_x}, {target_y}) yasaklı listeye ekleniyor.")
                        memory.add_forbidden_zone(target_x, target_y, reason=result.get('reason', 'Eylem başarısız'))
                    else:
                        log.write(f"[BAŞARI] Eylem başarılı görünüyor: {result.get('reason', 'Bilinmiyor')}")
                        mouse.random_sleep(0.5, 1.5)

                else:
                    log.write("[İPTAL] Bu koordinat daha önce hatalı olarak işaretlenmiş. Atlanıyor.")
                    forbidden_streak += 1

                    # Eğer sürekli yasaklı bölgeye denk geliyorsak
                    if forbidden_streak >= 2: # Eşiği düşürdük, daha hızlı tepki versin
                        log.write(f"[DÖNGÜ KIRICI] {forbidden_streak} kez üst üste yasaklı hedef. Rastgele hareket yapılıyor...")

                        # Eğer haritanın ortasındaysa kenara, kenardaysa ortaya gitmeyi dene
                        # Amaç kamerayı (haritayı) değiştirmek veya karakteri "unstick" yapmak

                        # Tamamen rastgele bir noktaya tıkla (Karakteri yürütmek için)
                        rand_x = random.randint(100, screen_w - 100)
                        rand_y = random.randint(100, screen_h - 100)

                        log.write(f"[UNSTICK] Rastgele noktaya tıklanıyor: ({rand_x}, {rand_y})")
                        mouse.click(rand_x, rand_y)

                        forbidden_streak = 0 # Sayacı sıfırla
                        time.sleep(4) # Yürümesi için zaman tanı

            else:
                log.write("[DÖNGÜ] Hedef bulunamadı. Bekleniyor...")

            # Döngü arası bekleme
            mouse.random_sleep(1, 2)

        except KeyboardInterrupt:
            log.write("\n[SİSTEM] Kullanıcı tarafından durduruldu.")
            sys.exit()
        except Exception as e:
            log.write(f"\n[HATA] Döngü hatası: {e}")
            log.write("Sistem 5 saniye içinde tekrar deneyecek...")
            time.sleep(5)

        except KeyboardInterrupt:
            print("\n[SİSTEM] Kullanıcı tarafından durduruldu.")
            sys.exit()
        except Exception as e:
            print(f"\n[HATA] Döngü hatası: {e}")
            print("Sistem 5 saniye içinde tekrar deneyecek...")
            time.sleep(5)

if __name__ == "__main__":
    main()
