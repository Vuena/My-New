import json
import os
import math

class DynamicMemory:
    def __init__(self, filepath="beyin.json"):
        self.filepath = filepath
        self.memory = {
            "forbidden_zones": [],
            "successful_actions": []
        }
        self.load_memory()

    def load_memory(self):
        """Diskten hafıza dosyasını yükler."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    self.memory = json.load(f)
                print(f"[HAFIZA] {self.filepath} başarıyla yüklendi.")
            except json.JSONDecodeError:
                print("[HAFIZA] JSON dosyası bozuk, yeni hafıza başlatılıyor.")
        else:
            print("[HAFIZA] Yeni hafıza dosyası oluşturuluyor.")
            self.save_memory()

    def save_memory(self):
        """Hafızayı diske kaydeder."""
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, indent=4, ensure_ascii=False)

    def add_forbidden_zone(self, x, y, reason="Unknown"):
        """Başarısız bir eylemi yasaklı bölge olarak ekler."""
        entry = {
            "x": x,
            "y": y,
            "reason": reason,
            "timestamp": "TODO: Add timestamp"  # Basit tutmak için timestamp şimdilik string
        }
        self.memory["forbidden_zones"].append(entry)
        self.save_memory()
        print(f"[HAFIZA] Yasaklı bölge eklendi: ({x}, {y}) - Sebep: {reason}")

    def is_action_safe(self, x, y, radius=20):
        """
        Verilen koordinatın yasaklı bir bölgeye yakın olup olmadığını kontrol eder.
        radius: Yasaklı noktaya ne kadar yakınsa 'tehlikeli' sayılacağı (piksel cinsinden).
        """
        for zone in self.memory["forbidden_zones"]:
            dist = math.sqrt((x - zone["x"])**2 + (y - zone["y"])**2)
            if dist < radius:
                print(f"[HAFIZA] Eylem REDDEDİLDİ! ({x}, {y}) noktası yasaklı bölgeye çok yakın ({dist:.2f}px). Sebep: {zone['reason']}")
                return False
        return True
