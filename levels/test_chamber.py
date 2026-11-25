"""
Peta ruang uji coba (Test Chamber) untuk menguji pergerakan, lompatan,
dan interaksi permukaan lantai es vs batu normal.
"""
import pygame
from settings import (
    TILE_SIZE, COLOR_SOLID, COLOR_ICE, COLOR_WATER, 
    COLOR_LAVA, COLOR_TEXT
)

TEST_MAP = [
    "################################",
    "#                              #",
    "#                              #",
    "#                              #",
    "#       #####                  #",
    "#                              #",
    "#                *****         #",
    "#               *******        #",
    "#    1    2                    #",
    "#   ########                   #",
    "#              ###             #",
    "#                              #",
    "#                     ####     #",
    "#                              #",
    "#         ~~~~~~               #",
    "#         ~~~~~~         P     #",
    "################################",
    "################################",
]

class TestChamber:
    def __init__(self):
        self.solid_tiles = []
        self.ice_tiles = []
        self.water_tiles = []
        self.spawn_ignis = (120, 280)
        self.spawn_cryo = (180, 280)
        self.goal_rect = None
        
        self.load_map(TEST_MAP)

    def load_map(self, map_data):
        self.solid_tiles.clear()
        self.ice_tiles.clear()
        self.water_tiles.clear()

        for row_idx, row in enumerate(map_data):
            for col_idx, char in enumerate(row):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE
                rect = pygame.FRect(x, y, TILE_SIZE, TILE_SIZE)

                if char == '#':
                    self.solid_tiles.append(rect)
                elif char == '*':
                    self.ice_tiles.append(rect)
                    self.solid_tiles.append(rect)  # Es juga padat
                elif char == '~':
                    self.water_tiles.append(rect)
                elif char == '1':
                    self.spawn_ignis = (x, y)
                elif char == '2':
                    self.spawn_cryo = (x, y)
                elif char == 'P':
                    self.goal_rect = pygame.FRect(x + 5, y - 10, TILE_SIZE - 10, TILE_SIZE + 10)

    def draw(self, surface, camera_offset=(0, 0)):
        ox, oy = camera_offset

        # 1. Gambar Balok Batu Padat (#)
        for tile in self.solid_tiles:
            if tile in self.ice_tiles:
                continue  # Digambar terpisah di bawah
            draw_rect = pygame.Rect(tile.x - ox, tile.y - oy, tile.width, tile.height)
            pygame.draw.rect(surface, COLOR_SOLID, draw_rect)
            # Detail border batu
            pygame.draw.rect(surface, (75, 82, 100), draw_rect, width=2)
            pygame.draw.line(surface, (95, 105, 130), (draw_rect.left + 2, draw_rect.top + 2), (draw_rect.right - 2, draw_rect.top + 2), 2)

        # 2. Gambar Balok Es Kristal (*)
        for tile in self.ice_tiles:
            draw_rect = pygame.Rect(tile.x - ox, tile.y - oy, tile.width, tile.height)
            # Surface es dengan transparansi
            ice_surf = pygame.Surface((tile.width, tile.height), pygame.SRCALPHA)
            pygame.draw.rect(ice_surf, COLOR_ICE, ice_surf.get_rect(), border_radius=3)
            # Kilau es diagonal
            pygame.draw.line(ice_surf, (255, 255, 255, 200), (5, 5), (15, 15), 2)
            pygame.draw.line(ice_surf, (255, 255, 255, 180), (tile.width - 15, 5), (tile.width - 5, 15), 2)
            surface.blit(ice_surf, draw_rect)

        # 3. Gambar Kolam Air (~)
        for tile in self.water_tiles:
            draw_rect = pygame.Rect(tile.x - ox, tile.y - oy, tile.width, tile.height)
            water_surf = pygame.Surface((tile.width, tile.height), pygame.SRCALPHA)
            pygame.draw.rect(water_surf, COLOR_WATER, water_surf.get_rect())
            # Riak air di atas
            pygame.draw.line(water_surf, (100, 180, 255, 220), (0, 2), (tile.width, 2), 2)
            surface.blit(water_surf, draw_rect)

        # 4. Gambar Goal Portal (P)
        if self.goal_rect:
            p_rect = pygame.Rect(self.goal_rect.x - ox, self.goal_rect.y - oy, self.goal_rect.width, self.goal_rect.height)
            portal_surf = pygame.Surface((p_rect.width, p_rect.height), pygame.SRCALPHA)
            pygame.draw.ellipse(portal_surf, (180, 100, 255, 220), portal_surf.get_rect())
            pygame.draw.ellipse(portal_surf, (240, 200, 255, 255), portal_surf.get_rect(), width=2)
            surface.blit(portal_surf, p_rect)
