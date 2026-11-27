"""
Level 1: "The Awakening" (Edisi Termodinamika & Fisika Terukur)
Fitur:
1. Akses Altar Tanpa Hambatan:
   - Lantai dari pintu keluar terowongan sampai ke Altar R & B datar penuh!
   - Pemain cukup BERJALAN langsung menuju Altar R & B tanpa perlu melompat tebing!
2. Pijakan Batu Aman (Safe Shore) antara Danau dan Tembok Sulur:
   - Ignis berdiri kokoh di atas batu padat saat mencairkan tembok, tidak tercebur ke danau!
3. Siklus Fisika 2 Arah:
   - Cryo membekukan air dengan Frost Cast, Ignis mencairkannya kembali dengan Heat Stance.
4. Tangga One-Way (Jump-Through Platforms '='):
   - Bisa dilompati tembus dari bawah tanpa membentur kepala!
   - Jarak tinggi antar tangga dihitung tepat hanya 2 tile (80px), jauh di bawah daya lompat (125px).
"""
import pygame
import math
from settings import (
    TILE_SIZE, COLOR_SOLID, COLOR_IGNIS_GLOW, COLOR_CRYO_GLOW
)
from levels.thermal_system import WaterTile, FrozenBarrier, ThermalCrucible

# Peta Level 1 (32 x 18):
# ~ : Air (Danau 4 tile: cols 3-6)
# % : Tembok Sulur Beku (col 8, di bawah atap batu cols 4-8)
# R, B : Altar Termal (cols 22, 27) -> LANTAI DATAR TERBUKA!
# = : Platform One-Way (Bisa ditembus dari bawah, mendarat di atasnya)
# P : Portal Keluar
LEVEL_1_MAP = [
    "################################", # 0
    "#                              #", # 1
    "#                              #", # 2
    "#                        P     #", # 3
    "#                      =====   #", # 4 (Portal Platform)
    "#                              #", # 5
    "#                =====         #", # 6 (Step 3)
    "#                              #", # 7
    "#          =====               #", # 8 (Step 2)
    "#                              #", # 9
    "#   #####        =====         #", # 10 (Roof col 4-8; Step 1 col 17-21)
    "#   #####                      #", # 11
    "#12     %                 ==== #", # 12 (Spawn aman cols 1-2; Barrier %, Step 0 col 26-29)
    "#       %             R    B   #", # 13 (LANTAI DATAR! Jalan langsung ke R & B!)
    "###~~~~####################### #", # 14 (Floor Y=560)
    "###~~~~#                     # #", # 15
    "################################", # 16
    "################################", # 17
]

class Level1:
    def __init__(self):
        self.solid_tiles = []
        self.one_way_platforms = []
        self.spike_tiles = []
        self.water_tiles = []
        self.barriers = []
        
        self.crucible_ignis = None
        self.crucible_cryo = None
        self.portal_rect = None
        
        self.spawn_ignis = (60, 440)
        self.spawn_cryo = (100, 440)
        
        self.puzzle_solved = False
        self.level_completed = False
        self.anim_time = 0.0

        self.load_level(LEVEL_1_MAP)

    def load_level(self, map_data):
        self.solid_tiles.clear()
        self.one_way_platforms.clear()
        self.spike_tiles.clear()
        self.water_tiles.clear()
        self.barriers.clear()

        for row_idx, row in enumerate(map_data):
            for col_idx, char in enumerate(row):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE
                rect = pygame.FRect(x, y, TILE_SIZE, TILE_SIZE)

                if char == '#':
                    self.solid_tiles.append(rect)
                elif char == '=':
                    # Platform one-way tipis di bagian atas tile
                    one_way_rect = pygame.FRect(x, y, TILE_SIZE, 12)
                    self.one_way_platforms.append(one_way_rect)
                elif char == '^':
                    spike_rect = pygame.FRect(x + 4, y + 16, TILE_SIZE - 8, TILE_SIZE - 16)
                    self.spike_tiles.append(spike_rect)
                elif char == '~':
                    self.water_tiles.append(WaterTile(x, y))
                elif char == '%':
                    self.barriers.append(FrozenBarrier(x, y))
                elif char == '1':
                    self.spawn_ignis = (x, y)
                elif char == '2':
                    self.spawn_cryo = (x, y)
                elif char == 'R':
                    self.crucible_ignis = ThermalCrucible(x, y, "ignis")
                elif char == 'B':
                    self.crucible_cryo = ThermalCrucible(x, y, "cryo")
                elif char == 'P':
                    self.portal_rect = pygame.FRect(x + 4, y - 10, TILE_SIZE - 8, TILE_SIZE + 10)

    def update(self, dt, ignis, cryo):
        self.anim_time += dt

        for water in self.water_tiles:
            water.update(dt)

        # -----------------------------------------------------------------
        # 1. PEMBEKUAN AIR OLEH CRYO (Frost Cast / Dash)
        # -----------------------------------------------------------------
        if cryo.is_acting:
            for water in self.water_tiles:
                water.freeze()
        elif cryo.dash_timer > 0.0:
            dash_zone = pygame.FRect(
                cryo.physics.rect.x - 30, cryo.physics.rect.y - 10,
                cryo.physics.rect.width + 60, cryo.physics.rect.height + 30
            )
            for water in self.water_tiles:
                if dash_zone.colliderect(water.rect):
                    water.freeze()

        # -----------------------------------------------------------------
        # 2. PANAS TERARAH IGNIS (Directional Heat Stance & Dash)
        # -----------------------------------------------------------------
        ignis_is_heating = (ignis.is_acting or ignis.dash_timer > 0.0)
        
        if ignis_is_heating:
            if ignis.physics.facing_right:
                ignis_heat_zone = pygame.FRect(
                    ignis.physics.rect.x - 8, ignis.physics.rect.y - 10,
                    ignis.physics.rect.width + 55, ignis.physics.rect.height + 25
                )
            else:
                ignis_heat_zone = pygame.FRect(
                    ignis.physics.rect.x - 55, ignis.physics.rect.y - 10,
                    ignis.physics.rect.width + 55, ignis.physics.rect.height + 25
                )

            # A. Mencairkan Es jika sengaja diarahkan ke danau
            for water in self.water_tiles:
                if water.is_frozen and ignis_heat_zone.colliderect(water.rect):
                    water.melt()

            # B. Melelehkan Tembok Sulur Beku
            for barrier in self.barriers:
                if not barrier.is_destroyed:
                    if ignis_heat_zone.colliderect(barrier.rect):
                        melt_speed = 190.0 if ignis.is_acting else 300.0
                        barrier.apply_heat(melt_speed * dt)

        # -----------------------------------------------------------------
        # 3. REAKTOR TERMAL GANDA (Altar Charging)
        # -----------------------------------------------------------------
        ignis_channeling = False
        if self.crucible_ignis:
            if ignis.physics.rect.colliderect(self.crucible_ignis.rect) and ignis.is_acting:
                ignis_channeling = True
            self.crucible_ignis.update(dt, ignis_channeling)

        cryo_channeling = False
        if self.crucible_cryo:
            if cryo.physics.rect.colliderect(self.crucible_cryo.rect) and cryo.is_acting:
                cryo_channeling = True
            self.crucible_cryo.update(dt, cryo_channeling)

        if not self.puzzle_solved and self.crucible_ignis and self.crucible_cryo:
            if self.crucible_ignis.is_fully_charged and self.crucible_cryo.is_fully_charged:
                self.puzzle_solved = True

        # -----------------------------------------------------------------
        # 4. KEMENANGAN (Keduanya masuk ke Portal)
        # -----------------------------------------------------------------
        if self.puzzle_solved and self.portal_rect:
            ignis_in = ignis.physics.rect.colliderect(self.portal_rect)
            cryo_in = cryo.physics.rect.colliderect(self.portal_rect)
            if ignis_in and cryo_in:
                self.level_completed = True

    def get_solid_tiles(self):
        solids = list(self.solid_tiles)
        for water in self.water_tiles:
            if water.is_frozen:
                solids.append(water.rect)
        for barrier in self.barriers:
            if not barrier.is_destroyed:
                solids.append(barrier.rect)
        return solids

    def get_ice_tiles(self):
        return [w.rect for w in self.water_tiles if w.is_frozen]

    def get_one_way_platforms(self):
        return self.one_way_platforms

    def draw(self, surface, camera_offset=(0, 0)):
        ox, oy = camera_offset

        # 1. Batu Padat (#)
        for tile in self.solid_tiles:
            draw_rect = pygame.Rect(tile.x - ox, tile.y - oy, tile.width, tile.height)
            pygame.draw.rect(surface, COLOR_SOLID, draw_rect)
            pygame.draw.rect(surface, (75, 82, 100), draw_rect, width=2)
            pygame.draw.line(surface, (95, 105, 130), (draw_rect.left + 2, draw_rect.top + 2), (draw_rect.right - 2, draw_rect.top + 2), 2)

        # 2. Platform One-Way Jump-Through (=)
        for plat in self.one_way_platforms:
            px = plat.x - ox
            py = plat.y - oy
            p_rect = pygame.Rect(px, py, plat.width, plat.height)
            pygame.draw.rect(surface, (80, 85, 105), p_rect, border_radius=2)
            pygame.draw.line(surface, (140, 200, 255), (p_rect.left + 1, p_rect.top + 1), (p_rect.right - 1, p_rect.top + 1), 2)

        # 3. Duri Tajam (^)
        for spike in self.spike_tiles:
            sx = spike.x - ox
            sy = spike.y - oy
            w, h = spike.width, spike.height
            for i in range(2):
                p1 = (sx + i * (w/2), sy + h)
                p2 = (sx + (i + 0.5) * (w/2), sy - 3)
                p3 = (sx + (i + 1) * (w/2), sy + h)
                pygame.draw.polygon(surface, (210, 50, 50), [p1, p2, p3])
                pygame.draw.polygon(surface, (255, 120, 120), [p1, p2, p3], width=1)

        # 4. Air / Es Dinamis (~)
        for water in self.water_tiles:
            water.draw(surface, camera_offset, self.anim_time)

        # 4. Tembok Sulur Beku (%)
        for barrier in self.barriers:
            barrier.draw(surface, camera_offset, self.anim_time)

        # 5. Altar Reaktor Termal (R & B)
        if self.crucible_ignis:
            self.crucible_ignis.draw(surface, camera_offset, self.anim_time)
        if self.crucible_cryo:
            self.crucible_cryo.draw(surface, camera_offset, self.anim_time)

        # 6. Portal Keluar (P)
        if self.portal_rect:
            px = self.portal_rect.x - ox
            py = self.portal_rect.y - oy
            pw, ph = self.portal_rect.width, self.portal_rect.height
            portal_surf = pygame.Surface((pw + 24, ph + 24), pygame.SRCALPHA)
            
            if self.puzzle_solved:
                spin = self.anim_time * 4.0
                pygame.draw.ellipse(portal_surf, (180, 80, 255, 180), (4, 4, pw + 16, ph + 16))
                rx = math.cos(spin) * 8
                pygame.draw.ellipse(portal_surf, (255, 230, 100, 240), (12 + rx, 8, pw, ph), width=3)
                pygame.draw.circle(portal_surf, (255, 255, 255), (portal_surf.get_width() // 2, portal_surf.get_height() // 2), 8)
            else:
                pygame.draw.ellipse(portal_surf, (60, 50, 80, 120), (4, 4, pw + 16, ph + 16))
                pygame.draw.ellipse(portal_surf, (100, 90, 120, 160), (12, 8, pw, ph), width=2)
                
            surface.blit(portal_surf, (px - 12, py - 12))
