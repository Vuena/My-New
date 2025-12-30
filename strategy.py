class GeneralStrategy:
    def __init__(self, logger=None):
        self.logger = logger
        # Basit seviye rehberi (Örnek)
        self.level_guide = {
            (1, 10): "Incarnam - Gobball",
            (11, 20): "Astrub - Piwis",
            (21, 40): "Astrub - Forest",
            (41, 60): "Amakna - Cracklers"
        }
        self.current_objective = "Grind"

    def determine_objective(self, current_level, current_map_zone):
        """
        Mevcut seviyeye ve konuma göre üst düzey hedef belirler.
        """
        recommended_zone = "Unknown"
        for levels, zone in self.level_guide.items():
            if levels[0] <= current_level <= levels[1]:
                recommended_zone = zone
                break

        msg = f"[STRATEJİ] Seviye: {current_level} | Mevcut Bölge: {current_map_zone} | Hedef Bölge: {recommended_zone}"
        if self.logger:
            self.logger.write(msg)
        else:
            print(msg)

        return recommended_zone

    def get_tactical_advice(self, combat_screen=False):
        """
        Duruma göre taktik verir.
        Eğer savaş ekranı tespit edilirse savaş moduna geçer.
        """
        if combat_screen:
            return "COMBAT_MODE"
        return "EXPLORE_MODE"
