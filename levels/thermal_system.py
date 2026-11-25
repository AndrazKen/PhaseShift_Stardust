"""
Sistem Interaksi Fisika Termal Real-Time untuk Level 1:
1. Air (Water) <-> Es (Ice): Siklus 2 Arah (Cryo membekukan air, Ignis Heat Stance/Rage mencairkannya kembali!).
2. Tembok Sulur Beku (Frozen Barrier): Menutup lorong penuh dari lantai sampai atap.
3. Reaktor Termal Ganda (Thermal Crucible): Mengisi daya altar dengan menahan Heat Stance dan Frost Cast.
"""
import pygame
import math
from settings import (
    TILE_SIZE, COLOR_WATER, COLOR_ICE, 
    COLOR_IGNIS_GLOW, COLOR_CRYO_GLOW, COLOR_SOLID
)

class WaterTile:
    def __init__(self, x, y):
        self.rect = pygame.FRect(x, y, TILE_SIZE, TILE_SIZE)
        self.is_frozen = False
        self.anim_offset = (x // TILE_SIZE) * 0.8
        self.steam_timer = 0.0

    def freeze(self):
        self.is_frozen = True

    def melt(self):
        if self.is_frozen:
            self.is_frozen = False
            self.steam_timer = 0.8  # Efek kepulan uap mendesis

    def update(self, dt):
        if self.steam_timer > 0.0:
            self.steam_timer = max(0.0, self.steam_timer - dt)

    def draw(self, surface, camera_offset, anim_time):
        ox, oy = camera_offset
        draw_rect = pygame.Rect(self.rect.x - ox, self.rect.y - oy, self.rect.width, self.rect.height)

        if self.is_frozen:
            # Balok Es Kristal Padat
            ice_surf = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(ice_surf, (160, 225, 255, 230), ice_surf.get_rect(), border_radius=3)
            # Pola kristal es menyilang berkilau
            pygame.draw.line(ice_surf, (255, 255, 255, 220), (4, 4), (16, 16), 2)
            pygame.draw.line(ice_surf, (255, 255, 255, 180), (draw_rect.width - 16, 4), (draw_rect.width - 4, 16), 2)
            pygame.draw.rect(ice_surf, (210, 245, 255), ice_surf.get_rect(), width=2, border_radius=3)
            surface.blit(ice_surf, draw_rect)
        else:
            # Cairan Air Beriak Dinamis (Mematikan untuk Ignis!)
            water_surf = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(water_surf, (30, 110, 230, 190), water_surf.get_rect())
            
            # Gelombang air bergerak
            wave_y = int(math.sin(anim_time * 6.0 + self.anim_offset) * 3.0) + 3
            pygame.draw.line(water_surf, (140, 200, 255, 240), (0, wave_y), (draw_rect.width, wave_y), 2)
            surface.blit(water_surf, draw_rect)

            # Efek uap saat baru saja mencair
            if self.steam_timer > 0.0:
                steam_alpha = int((self.steam_timer / 0.8) * 160)
                steam_surf = pygame.Surface((draw_rect.width, 16), pygame.SRCALPHA)
                pygame.draw.ellipse(steam_surf, (240, 240, 255, steam_alpha), steam_surf.get_rect())
                surface.blit(steam_surf, (draw_rect.x, draw_rect.top - 8))

class FrozenBarrier:
    """Tembok Es / Sulur Beku yang menutup penuh lorong (tinggi 2 tile) dari lantai hingga atap."""
    def __init__(self, x, y):
        # Menutup 2 tile tinggi penuh (80px)
        self.rect = pygame.FRect(x, y, TILE_SIZE, TILE_SIZE * 2)
        self.hp = 100.0
        self.is_destroyed = False

    def apply_heat(self, amount):
        if not self.is_destroyed:
            self.hp = max(0.0, self.hp - amount)
            if self.hp <= 0.0:
                self.is_destroyed = True
                return True
        return False

    def draw(self, surface, camera_offset, anim_time):
        if self.is_destroyed:
            return
        ox, oy = camera_offset
        draw_rect = pygame.Rect(self.rect.x - ox, self.rect.y - oy, self.rect.width, self.rect.height)

        barrier_surf = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
        ratio = self.hp / 100.0
        barrier_surf.fill((60, 160, 180, int(230 * ratio)))
        pygame.draw.rect(barrier_surf, (190, 245, 255), barrier_surf.get_rect(), width=2, border_radius=4)
        
        # Garis pola akar sulur es membeku
        pygame.draw.line(barrier_surf, (40, 90, 80), (6, 12), (26, draw_rect.height - 18), 3)
        pygame.draw.line(barrier_surf, (40, 90, 80), (24, 24), (8, draw_rect.height - 28), 3)
        
        # Retakan saat dipanaskan Ignis
        if ratio < 0.85:
            pygame.draw.line(barrier_surf, (255, 255, 255), (10, 20), (22, 38), 2)
            pygame.draw.line(barrier_surf, (255, 200, 120), (14, 50), (24, 65), 2)
            
        surface.blit(barrier_surf, draw_rect)

class ThermalCrucible:
    """Altar Reaktor Termal: Ignis menahan Heat Stance, Cryo menahan Frost Cast."""
    def __init__(self, x, y, crucible_type):
        self.rect = pygame.FRect(x + 2, y + 16, TILE_SIZE - 4, TILE_SIZE - 16)
        self.type = crucible_type  # "ignis" atau "cryo"
        self.charge = 0.0
        self.is_fully_charged = False
        self.is_channeling = False

    def update(self, dt, player_channeling):
        self.is_channeling = player_channeling
        if player_channeling:
            self.charge = min(100.0, self.charge + 55.0 * dt)
        else:
            if not self.is_fully_charged:
                self.charge = max(0.0, self.charge - 25.0 * dt)

        if self.charge >= 100.0:
            self.is_fully_charged = True

    def draw(self, surface, camera_offset, anim_time):
        ox, oy = camera_offset
        draw_rect = pygame.Rect(self.rect.x - ox, self.rect.y - oy, self.rect.width, self.rect.height)

        color = COLOR_IGNIS_GLOW if self.type == "ignis" else COLOR_CRYO_GLOW
        base_color = (45, 25, 20) if self.type == "ignis" else (20, 35, 50)

        pygame.draw.rect(surface, base_color, draw_rect, border_radius=3)
        pygame.draw.rect(surface, (70, 75, 90), draw_rect, width=2, border_radius=3)

        # Progress bar di bawah altar
        bar_w = draw_rect.width - 6
        fill_w = int(bar_w * (self.charge / 100.0))
        bar_rect = pygame.Rect(draw_rect.x + 3, draw_rect.bottom - 6, bar_w, 4)
        pygame.draw.rect(surface, (15, 18, 25), bar_rect)
        if fill_w > 0:
            pygame.draw.rect(surface, color, (bar_rect.x, bar_rect.y, fill_w, 4))

        # Kristal pilar melayang
        ratio = self.charge / 100.0
        crystal_y = draw_rect.top - 18 + int(math.sin(anim_time * 5.0) * 3.0)
        crystal_rect = pygame.Rect(draw_rect.centerx - 8, crystal_y, 16, 18)

        glow_alpha = int(80 + 175 * ratio)
        glow_surf = pygame.Surface((36, 36), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*color, glow_alpha), (18, 18), int(12 + 6 * ratio))
        surface.blit(glow_surf, (crystal_rect.centerx - 18, crystal_rect.centery - 18))

        pygame.draw.polygon(surface, color, [
            (crystal_rect.centerx, crystal_rect.top),
            (crystal_rect.right, crystal_rect.centery),
            (crystal_rect.centerx, crystal_rect.bottom),
            (crystal_rect.left, crystal_rect.centery),
        ])
        if self.is_fully_charged:
            pygame.draw.polygon(surface, (255, 255, 255), [
                (crystal_rect.centerx, crystal_rect.top + 3),
                (crystal_rect.right - 3, crystal_rect.centery),
                (crystal_rect.centerx, crystal_rect.bottom - 3),
                (crystal_rect.left + 3, crystal_rect.centery),
            ])
