"""
Sistem Mekanik Sinergi Elemen:
- Thermal Shockwave (High-Five Dash): Ketika kedua karakter saling dash dan bertabrakan di udara.
"""
from entities.player import PlayerState

class SynergySystem:
    @staticmethod
    def check_thermal_shockwave(ignis, cryo):
        """
        Mengecek benturan dash ganda antara Ignis dan Cryo.
        Mengembalikan True jika shockwave terjadi, memantulkan kecepatan kedua pemain.
        """
        if ignis.state == PlayerState.DASH and cryo.state == PlayerState.DASH:
            if ignis.physics.rect.colliderect(cryo.physics.rect):
                ignis.physics.vx = -ignis.dash_dir * 450.0
                cryo.physics.vx = -cryo.dash_dir * 450.0
                ignis.physics.vy = -350.0
                cryo.physics.vy = -350.0
                ignis.dash_timer = 0.0
                cryo.dash_timer = 0.0
                return True
        return False
