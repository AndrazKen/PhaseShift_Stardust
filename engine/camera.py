"""
Sistem kamera cerdas: Smooth Lerp Tracking yang otomatis mengikuti
titik tengah antara Ignis dan Cryo di dalam viewport.
"""
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class DynamicCamera:
    def __init__(self, world_width=1280, world_height=720):
        self.x = 0.0
        self.y = 0.0
        self.target_x = 0.0
        self.target_y = 0.0
        self.world_width = world_width
        self.world_height = world_height
        self.lerp_speed = 7.0  # Kecepatan transisi kamera halus

    def update(self, dt, target_rects):
        """Menghitung titik tengah semua target yang aktif dan smooth lerp."""
        if not target_rects:
            return

        # Hitung center of mass antara target
        min_x = min(r.x for r in target_rects)
        max_x = max(r.right for r in target_rects)
        min_y = min(r.y for r in target_rects)
        max_y = max(r.bottom for r in target_rects)

        mid_x = (min_x + max_x) * 0.5
        mid_y = (min_y + max_y) * 0.5

        self.target_x = mid_x - SCREEN_WIDTH * 0.5
        self.target_y = mid_y - SCREEN_HEIGHT * 0.5

        # Clamp ke batas dunia jika dunia lebih besar dari layar
        max_scroll_x = max(0, self.world_width - SCREEN_WIDTH)
        max_scroll_y = max(0, self.world_height - SCREEN_HEIGHT)

        self.target_x = max(0.0, min(self.target_x, max_scroll_x))
        self.target_y = max(0.0, min(self.target_y, max_scroll_y))

        # Smooth Lerp
        self.x += (self.target_x - self.x) * min(1.0, self.lerp_speed * dt)
        self.y += (self.target_y - self.y) * min(1.0, self.lerp_speed * dt)

    @property
    def offset(self):
        return (int(self.x), int(self.y))
