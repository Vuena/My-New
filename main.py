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

    while True:
        try:
            # 1. Adım: Görüntü Al ve Analiz Et
            decision = brain.analyze_screen()

            if not decision:
                print("[DÖNGÜ] Karar alınamadı, tekrar deneniyor...")
                time.sleep(2)
                continue

            # 2. Adım: Kararı Değerlendir
            if decision.get("found"):
                # Qwen VL genellikle [0-1000] aralığında koordinat verir.
                # Eğer model pixel veriyorsa bu adım atlanabilir, ancak genelde normalize değer verir.
                # Biz her ihtimale karşı modelden pixel istediğimizi varsaysak da,
                # güvenli taraf için modelin döndürdüğü değerleri kontrol etmeliyiz.
                # Ancak kullanıcı promptunda "koordinatları ver" dedi, modelin pixel mi normalize mi döndüreceği
                # kullanılan modele göre değişir. Qwen VL 2.5/MAX genelde normalize (1000x1000) çalışır.

                raw_x = decision["coordinates"]["x"]
                raw_y = decision["coordinates"]["y"]

                # Basit bir kontrol: Eğer koordinatlar 1000'den küçük ve ekran 1920 ise muhtemelen normalize'dir.
                # Ancak Dofus penceresi küçük de olabilir.
                # Burada varsayım: Model 1000x1000 grid kullanıyor.
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
                    # 4. Adım: Eylemi Gerçekleştir
                    print(f"[EYLEM] Gidiliyor... Sebep: {reason}")

                    mouse.click(target_x, target_y)

                    # 5. Adım: Başarı Kontrolü (Görsel Zeka ile)
                    # Modelden eylemin başarılı olup olmadığını kontrol etmesini iste
                    # Karakter hedefe doğru koşuyor mu veya savaş başladı mı?
                    print("[KONTROL] Eylem sonucu analiz ediliyor...")
                    # Hareket için biraz zaman tanı (örn. 3-4 saniye)
                    time.sleep(4)

                    result = brain.verify_action_success(decision['target_type'])

                    if result and not result.get("success", True):
                        print(f"[HATA] Eylem başarısız oldu! Sebep: {result.get('reason')}")
                        print(f"[ÖĞRENME] Koordinat ({target_x}, {target_y}) yasaklı listeye ekleniyor.")
                        memory.add_forbidden_zone(target_x, target_y, reason=result.get('reason', 'Eylem başarısız'))
                    else:
                        print(f"[BAŞARI] Eylem başarılı görünüyor: {result.get('reason', 'Bilinmiyor')}")
                        mouse.random_sleep(1, 2) # İşlem sonrası dinlenme

                else:
                    print("[İPTAL] Bu koordinat daha önce hatalı olarak işaretlenmiş. Atlanıyor.")
            else:
                print("[DÖNGÜ] Hedef bulunamadı. Bekleniyor...")

            # Döngü arası bekleme
            mouse.random_sleep(2, 4)

        except KeyboardInterrupt:
            print("\n[SİSTEM] Kullanıcı tarafından durduruldu.")
            sys.exit()
        except Exception as e:
            print(f"\n[HATA] Döngü hatası: {e}")
            print("Sistem 5 saniye içinde tekrar deneyecek...")
            time.sleep(5)

if __name__ == "__main__":
    main()
