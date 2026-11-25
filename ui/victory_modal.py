"""
Modal / Kartu Layar Kemenangan (Level Completed Overlay).
"""
import pygame

class VictoryModal:
    def __init__(self, font_banner, font_sub, font_main, font_hud):
        self.font_banner = font_banner
        self.font_sub = font_sub
        self.font_main = font_main
        self.font_hud = font_hud

    def draw(self, screen, screen_width, screen_height, elapsed_time, death_count):
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((10, 12, 18, 220))
        screen.blit(overlay, (0, 0))

        card_w, card_h = 580, 290
        cx = screen_width // 2 - card_w // 2
        cy = screen_height // 2 - card_h // 2
        card_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        card_surf.fill((22, 26, 38, 245))
        pygame.draw.rect(card_surf, (100, 220, 255), card_surf.get_rect(), width=3, border_radius=12)
        screen.blit(card_surf, (cx, cy))

        win_title = self.font_banner.render("LEVEL 1 BERHASIL DITAMATKAN!", True, (255, 215, 80))
        win_sub = self.font_sub.render("Fisika Termodinamika & Kerja Sama Elemen Berjalan Sempurna!", True, (220, 230, 245))
        stat_1 = self.font_main.render(f"Waktu Penyelesaian: {int(elapsed_time)} Detik", True, (150, 220, 255))
        death_color = (255, 120, 120) if death_count > 0 else (120, 255, 140)
        stat_2 = self.font_main.render(f"Jumlah Kematian: {death_count} Kali", True, death_color)
        restart_hint = self.font_hud.render("Tekan [ R ] untuk Mengulang Level 1 | [ ESC ] Keluar", True, (255, 240, 160))

        screen.blit(win_title, (screen_width // 2 - win_title.get_width() // 2, cy + 30))
        screen.blit(win_sub, (screen_width // 2 - win_sub.get_width() // 2, cy + 85))
        screen.blit(stat_1, (screen_width // 2 - stat_1.get_width() // 2, cy + 135))
        screen.blit(stat_2, (screen_width // 2 - stat_2.get_width() // 2, cy + 170))
        screen.blit(restart_hint, (screen_width // 2 - restart_hint.get_width() // 2, cy + 235))
