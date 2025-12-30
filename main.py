import time
import sys
import pyautogui
from memory import DynamicMemory
from human_mouse import HumanMouse
from vision_brain import VisionBrain

def main():
    print("=== Dofus AI Ajanı Başlatılıyor ===")
    print("Çıkış için Ctrl+C basınız.")

    # Modülleri başlat
    memory = DynamicMemory()
    mouse = HumanMouse()
    brain = VisionBrain(api_url="http://localhost:1234/v1/chat/completions", model_id="local-model")

    # Ekran boyutlarını al (Koordinat ölçekleme için)
    screen_w, screen_h = pyautogui.size()

    # Yasaklı bölgeye kaç kez denk gelindiğini sayar
    forbidden_streak = 0

    while True:
        try:
            # 1. Adım: Görüntü Al ve Analiz Et
            decision = brain.analyze_screen()

            if not decision:
                print("[DÖNGÜ] Karar alınamadı, tekrar deneniyor...")
                time.sleep(1) # Beklemeyi azalttık
                continue

            # 2. Adım: Kararı Değerlendir
            if decision.get("found"):
                # Koordinat hesaplama...
                raw_x = decision["coordinates"]["x"]
                raw_y = decision["coordinates"]["y"]

                if raw_x <= 1000 and raw_y <= 1000 and screen_w > 1000:
                    target_x = int((raw_x / 1000) * screen_w)
                    target_y = int((raw_y / 1000) * screen_h)
                    print(f"[KOORDİNAT] Normalize ({raw_x}, {raw_y}) -> Ekran ({target_x}, {target_y})")
                else:
                    target_x = raw_x
                    target_y = raw_y

                reason = decision.get("reason", "Belirtilmemiş")

                print(f"[KARAR] Hedef bulundu: {decision['target_type']} @ ({target_x}, {target_y})")

                # 3. Adım: Hafıza Kontrolü (Neden-Sonuç)
                if memory.is_action_safe(target_x, target_y):
                    # Yasaklı olmayan güvenli bir hedef bulundu, sayacı sıfırla
                    forbidden_streak = 0

                    # 4. Adım: Eylemi Gerçekleştir
                    print(f"[EYLEM] Gidiliyor... Sebep: {reason}")

                    mouse.click(target_x, target_y)

                    # 5. Adım: Başarı Kontrolü
                    print("[KONTROL] Eylem sonucu analiz ediliyor...")
                    time.sleep(3) # Beklemeyi azalttık (Daha hızlı tepki)

                    result = brain.verify_action_success(decision['target_type'])

                    if result and not result.get("success", True):
                        print(f"[HATA] Eylem başarısız oldu! Sebep: {result.get('reason')}")
                        print(f"[ÖĞRENME] Koordinat ({target_x}, {target_y}) yasaklı listeye ekleniyor.")
                        memory.add_forbidden_zone(target_x, target_y, reason=result.get('reason', 'Eylem başarısız'))
                    else:
                        print(f"[BAŞARI] Eylem başarılı görünüyor: {result.get('reason', 'Bilinmiyor')}")
                        mouse.random_sleep(0.5, 1.5) # İşlem sonrası dinlenme (Azaltıldı)

                else:
                    print("[İPTAL] Bu koordinat daha önce hatalı olarak işaretlenmiş. Atlanıyor.")
                    forbidden_streak += 1

                    # Eğer sürekli yasaklı bölgeye denk geliyorsak (Döngüye girdiyse)
                    if forbidden_streak >= 3:
                        print("[DÖNGÜ KIRICI] Sürekli yasaklı hedef bulunuyor. Rastgele hareket yapılıyor...")
                        # Ekranın ortasına yakın rastgele bir yere tıkla veya mouse'u oynat
                        rand_x = screen_w // 2 + random.randint(-200, 200)
                        rand_y = screen_h // 2 + random.randint(-200, 200)
                        mouse.move_to(rand_x, rand_y, duration=0.2)
                        forbidden_streak = 0 # Sayacı sıfırla
                        time.sleep(1)

            else:
                print("[DÖNGÜ] Hedef bulunamadı. Bekleniyor...")

            # Döngü arası bekleme
            mouse.random_sleep(1, 2) # Genel döngü hızını artırdık (Azaltıldı)

        except KeyboardInterrupt:
            print("\n[SİSTEM] Kullanıcı tarafından durduruldu.")
            sys.exit()
        except Exception as e:
            print(f"\n[HATA] Döngü hatası: {e}")
            print("Sistem 5 saniye içinde tekrar deneyecek...")
            time.sleep(5)

if __name__ == "__main__":
    main()
