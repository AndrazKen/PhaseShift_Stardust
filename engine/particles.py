"""
Sistem Pengelolaan Partikel untuk PhaseShift.
Mendukung partikel kematian, percikan elemen, dan efek visual lainnya.
"""
import pygame
import random

class ParticleManager:
    def __init__(self):
        self.particles = []

    def spawn_death_burst(self, center_x, center_y, color, count=25):
        """Memicu ledakan partikel saat karakter tereliminasi."""
        ticks = pygame.time.get_ticks()
        for i in range(count):
            self.particles.append({
                "x": float(center_x),
                "y": float(center_y),
                "vx": ((ticks + i * 17) % 100 - 50) * 8.0,
                "vy": -abs((ticks + i * 13) % 80) * 6.0,
                "color": color,
                "life": 0.6,
                "radius": 4
            })

    def update(self, dt):
        """Memperbarui posisi partikel dan menerapkan gravitasi."""
        for p in self.particles[:]:
            p["x"] += p["vx"] * dt
            p["y"] += p["vy"] * dt
            p["vy"] += 800.0 * dt
            p["life"] -= dt
            if p["life"] <= 0:
                self.particles.remove(p)

    def draw(self, surface, camera_offset):
        """Menggambar seluruh partikel aktif dengan pergeseran kamera."""
        ox, oy = camera_offset
        for p in self.particles:
            px = int(p["x"] - ox)
            py = int(p["y"] - oy)
            pygame.draw.circle(surface, p["color"], (px, py), p.get("radius", 4))

    def clear(self):
        """Membersihkan semua partikel."""
        self.particles.clear()
