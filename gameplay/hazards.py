"""
Sistem Bahaya Lingkungan (Hazards):
- Air cair memadamkan Ignis seketika (harus dibekukan dulu oleh Cryo).
- Duri tajam mengeliminasi karakter apapun yang menyentuhnya.
"""
from settings import COLOR_IGNIS_GLOW, COLOR_CRYO_GLOW

class HazardSystem:
    @staticmethod
    def check_hazards(level, ignis, cryo, on_death_callback):
        """
        Memeriksa kontak pemain dengan bahaya lingkungan.
        on_death_callback(character, color, reason_text)
        """
        # 1. Cek apakah Ignis tercebur ke air cair (belum membeku)
        for water in level.water_tiles:
            if not water.is_frozen:
                if ignis.physics.rect.colliderect(water.rect):
                    on_death_callback(
                        ignis,
                        COLOR_IGNIS_GLOW,
                        "IGNIS PADAM! AIR HARUS DIBEKUKAN CRYO DULU!"
                    )
                    break

        # 2. Cek tabrakan duri tajam
        for spike in level.spike_tiles:
            if ignis.physics.rect.colliderect(spike):
                on_death_callback(
                    ignis,
                    COLOR_IGNIS_GLOW,
                    "IGNIS TERKENA DURI!"
                )
                break
            if cryo.physics.rect.colliderect(spike):
                on_death_callback(
                    cryo,
                    COLOR_CRYO_GLOW,
                    "CRYO TERKENA DURI!"
                )
                break
