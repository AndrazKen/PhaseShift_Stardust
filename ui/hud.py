"""
Heads-Up Display (HUD):
- Header Bar (Judul, Mode, Statistik waktu, Kematian, FPS)
- Footer Bar (Petunjuk kontrol dinamis Co-op / Solo)
- Dynamic In-Game Puzzle Hint (Panduan langkah puzzle saat ini)
"""
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_IGNIS_GLOW, COLOR_CRYO_GLOW
)
from core.state import GameMode
from entities.player import CharacterType

class HUD:
    def __init__(self, font_main, font_title, font_hud):
        self.font_main = font_main
        self.font_title = font_title
        self.font_hud = font_hud

        self.header_surf = pygame.Surface((SCREEN_WIDTH, 48), pygame.SRCALPHA)
        self.header_surf.fill((12, 14, 20, 220))

        self.footer_surf = pygame.Surface((SCREEN_WIDTH, 42), pygame.SRCALPHA)
        self.footer_surf.fill((12, 14, 20, 220))

    def draw(self, screen, current_mode, active_solo_char, elapsed_time, death_count, fps, level):
        self._draw_header(screen, current_mode, elapsed_time, death_count, fps)
        self._draw_footer(screen, current_mode, active_solo_char)
        self._draw_puzzle_hint(screen, level)

    def _draw_header(self, screen, current_mode, elapsed_time, death_count, fps):
        screen.blit(self.header_surf, (0, 0))

        title_lbl = self.font_title.render("PHASESHIFT - LEVEL 1: THERMAL GENESIS", True, (255, 210, 100))
        mode_lbl = self.font_main.render(f"Mode: {current_mode} [M]", True, (100, 220, 255))
        stats_lbl = self.font_hud.render(
            f"Waktu: {int(elapsed_time)}s | Kematian: {death_count} | FPS: {int(fps)}",
            True,
            (200, 210, 230)
        )

        screen.blit(title_lbl, (20, 10))
        screen.blit(mode_lbl, (SCREEN_WIDTH // 2 - mode_lbl.get_width() // 2, 12))
        screen.blit(stats_lbl, (SCREEN_WIDTH - stats_lbl.get_width() - 20, 16))

    def _draw_footer(self, screen, current_mode, active_solo_char):
        screen.blit(self.footer_surf, (0, SCREEN_HEIGHT - 42))

        if current_mode == GameMode.COOP_LOCAL:
            p1_info = self.font_hud.render(
                "IGNIS: A/D=Jalan | W/Spasi=Lompat | L-Shift=Dash | S=Heat Stance (Bakar)",
                True,
                COLOR_IGNIS_GLOW
            )
            p2_info = self.font_hud.render(
                "CRYO: Panah=Jalan/Lompat | R-Ctrl=Dash | Bawah=Frost Cast (Bekukan)",
                True,
                COLOR_CRYO_GLOW
            )
            screen.blit(p1_info, (20, SCREEN_HEIGHT - 30))
            screen.blit(p2_info, (SCREEN_WIDTH - p2_info.get_width() - 20, SCREEN_HEIGHT - 30))
        else:
            active_name = "IGNIS" if active_solo_char == CharacterType.IGNIS else "CRYO"
            color = COLOR_IGNIS_GLOW if active_solo_char == CharacterType.IGNIS else COLOR_CRYO_GLOW
            solo_info = self.font_hud.render(
                f"SOLO: Mengontrol {active_name} | Tekan [TAB] Ganti Karakter | [R] Reset",
                True,
                color
            )
            screen.blit(solo_info, (20, SCREEN_HEIGHT - 30))

    def _draw_puzzle_hint(self, screen, level):
        all_frozen = all(w.is_frozen for w in level.water_tiles)
        any_barrier = any(not b.is_destroyed for b in level.barriers)

        if not all_frozen:
            hint_txt = self.font_hud.render(
                "LANGKAH 1: Cryo tekan [Bawah] (Frost Cast) Bekukan Air! (Ignis [S] bisa mencairkannya lagi!)",
                True,
                (130, 220, 255)
            )
        elif any_barrier:
            hint_txt = self.font_hud.render(
                "LANGKAH 2: Ignis masuk ke lorong & tahan [S] (Heat Stance) untuk Melelehkan Tembok Sulur!",
                True,
                (255, 170, 90)
            )
        elif not level.puzzle_solved:
            hint_txt = self.font_hud.render(
                "LANGKAH 3: Di Altar: Ignis tahan [S] di Altar Merah & Cryo tahan [Bawah] di Altar Biru!",
                True,
                (255, 230, 140)
            )
        else:
            hint_txt = self.font_hud.render(
                "LANGKAH 4: Portal Aktif! Naiki anak tangga di sebelah kanan dan masuk ke Portal bersama!",
                True,
                (120, 255, 150)
            )

        screen.blit(hint_txt, (SCREEN_WIDTH // 2 - hint_txt.get_width() // 2, SCREEN_HEIGHT - 70))
