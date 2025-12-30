import pyautogui
import time
import random
import numpy as np
import math

# Güvenlik önlemi: Mouse ekranın köşesine giderse işlemi durdurur
pyautogui.FAILSAFE = True
# Daha akıcı hareket için pause süresini düşür
pyautogui.PAUSE = 0.01

class HumanMouse:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()

    def _bezier_curve(self, start, end, control1, control2, num_points=25):
        """İki nokta arasında 3. dereceden Bezier eğrisi noktaları oluşturur."""
        points = []
        for t in np.linspace(0, 1, num_points):
            x = (1 - t)**3 * start[0] + \
                3 * (1 - t)**2 * t * control1[0] + \
                3 * (1 - t) * t**2 * control2[0] + \
                t**3 * end[0]
            y = (1 - t)**3 * start[1] + \
                3 * (1 - t)**2 * t * control1[1] + \
                3 * (1 - t) * t**2 * control2[1] + \
                t**3 * end[1]
            points.append((x, y))
        return points

    def move_to(self, target_x, target_y, duration=0.5):
        """
        Hedef noktaya insansı, kavisli bir hareketle gider.
        Hedefe varmadan önce +/- 5 piksel sapma ve rastgele hız değişimleri uygular.
        """
        start_x, start_y = pyautogui.position()

        # Rastgele kontrol noktaları oluştur (Kavis vermek için)
        # Kontrol noktaları başlangıç ve bitiş noktalarının arasında bir yerlerde olmalı ama sapmalı
        dist = math.hypot(target_x - start_x, target_y - start_y)

        # Eğer mesafe çok kısaysa direkt git (aşırı hesaplamaya gerek yok)
        if dist < 50:
            pyautogui.moveTo(target_x, target_y, duration=duration * 0.5, tween=pyautogui.easeOutQuad)
            return

        # Kontrol noktalarını rastgele seç
        control1 = (
            start_x + (target_x - start_x) * 0.3 + random.uniform(-100, 100),
            start_y + (target_y - start_y) * 0.3 + random.uniform(-100, 100)
        )
        control2 = (
            start_x + (target_x - start_x) * 0.7 + random.uniform(-100, 100),
            start_y + (target_y - start_y) * 0.7 + random.uniform(-100, 100)
        )

        # Bezier yolunu hesapla
        path_points = self._bezier_curve((start_x, start_y), (target_x, target_y), control1, control2)

        # Yol boyunca hareket et
        # Hareketi daha doğal yapmak için her adımda bekleme süresini biraz değiştirmiyoruz çünkü
        # pyautogui zaten yavaşlatıyor, ama adımları manuel atacağız.

        # PyAutoGUI'nin kendi tween özelliği yerine manuel nokta takibi yapıyoruz
        # çünkü tam kavis istiyoruz.

        for x, y in path_points:
            # Her adımda çok küçük mikro sapmalar eklemiyoruz, kavis zaten yeterli.
            # Sadece çok hızlı hareket et.
            pyautogui.moveTo(x, y, duration=0.01) # Çok kısa süre, akıcı görünmesi için

        # Son düzeltme: Hedef noktaya tam varış (veya +/- sapma ile)
        jitter_x = random.randint(-5, 5)
        jitter_y = random.randint(-5, 5)
        final_x = target_x + jitter_x
        final_y = target_y + jitter_y

        pyautogui.moveTo(final_x, final_y, duration=0.1, tween=pyautogui.easeOutQuad)

    def click(self, x, y):
        """Belirtilen koordinata gider ve tıklar."""
        self.move_to(x, y)
        time.sleep(random.uniform(0.1, 0.3)) # Tıklamadan önce milisaniyelik insan beklemesi
        pyautogui.click()
        print(f"[MOUSE] Tıklandı: {x}, {y}")

    def random_sleep(self, min_seconds=1.0, max_seconds=3.0):
        """İşlemler arasında rastgele bekler."""
        sleep_time = random.uniform(min_seconds, max_seconds)
        print(f"[BEKLEME] {sleep_time:.2f} saniye bekleniyor...")
        time.sleep(sleep_time)
