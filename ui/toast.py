"""
Pengelola Notifikasi Toast: Menampilkan banner pesan popup beranimasi waktu singkat.
"""
import pygame

class ToastManager:
    def __init__(self, font):
        self.font = font
        self.message = ""
        self.timer = 0.0

    def show(self, message, duration=3.0):
        self.message = message
        self.timer = duration

    def update(self, dt):
        if self.timer > 0.0:
            self.timer = max(0.0, self.timer - dt)

    def draw(self, screen, screen_width):
        if self.timer <= 0.0 or not self.message:
            return

        toast_surf = self.font.render(self.message, True, (255, 255, 255))
        tw, th = toast_surf.get_width() + 30, toast_surf.get_height() + 16
        tx = screen_width // 2 - tw // 2
        ty = 60

        box = pygame.Surface((tw, th), pygame.SRCALPHA)
        box.fill((30, 35, 50, 235))
        pygame.draw.rect(box, (255, 210, 100), box.get_rect(), width=2, border_radius=6)
        screen.blit(box, (tx, ty))
        screen.blit(toast_surf, (tx + 15, ty + 8))
