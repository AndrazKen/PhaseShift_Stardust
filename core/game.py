"""
Game Engine Utama PhaseShift:
Mengatur siklus hidup aplikasi, inisialisasi subsistem, update game loop, dan rendering.
"""
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
    COLOR_BG
)
from engine.camera import DynamicCamera
from engine.particles import ParticleManager
from entities.player import Player, CharacterType
from levels.level1 import Level1
from core.state import GameMode, GameStats
from core.input_handler import InputHandler
from gameplay.hazards import HazardSystem
from gameplay.mechanics import SynergySystem
from ui.hud import HUD
from ui.toast import ToastManager
from ui.victory_modal import VictoryModal

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = False

        # Inisialisasi Font
        self.font_main = pygame.font.SysFont("Segoe UI, Arial", 18, bold=True)
        self.font_title = pygame.font.SysFont("Segoe UI, Arial", 22, bold=True)
        self.font_hud = pygame.font.SysFont("Consolas, Courier", 14)
        self.font_banner = pygame.font.SysFont("Segoe UI, Arial", 32, bold=True)
        self.font_sub = pygame.font.SysFont("Segoe UI, Arial", 18)

        # Inisialisasi Level & Entitas
        self.level = Level1()
        self.ignis = Player(self.level.spawn_ignis[0], self.level.spawn_ignis[1], CharacterType.IGNIS)
        self.cryo = Player(self.level.spawn_cryo[0], self.level.spawn_cryo[1], CharacterType.CRYO)
        self.camera = DynamicCamera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Subsistem & Manajer
        self.particle_manager = ParticleManager()
        self.input_handler = InputHandler()
        self.stats = GameStats()
        self.hud = HUD(self.font_main, self.font_title, self.font_hud)
        self.toast = ToastManager(self.font_main)
        self.victory_modal = VictoryModal(self.font_banner, self.font_sub, self.font_main, self.font_hud)

        # Status Gameplay
        self.current_mode = GameMode.COOP_LOCAL
        self.active_solo_char = CharacterType.IGNIS
        self.shockwave_flash = 0.0

    def trigger_death(self, character, particles_color, reason_text):
        """Menangani eliminasi karakter dan respawn."""
        self.stats.record_death()
        self.toast.show(reason_text, 3.0)

        self.particle_manager.spawn_death_burst(
            character.physics.rect.centerx,
            character.physics.rect.centery,
            particles_color,
            count=25
        )

        if character.char_type == CharacterType.IGNIS:
            character.physics.rect.x, character.physics.rect.y = self.level.spawn_ignis
        else:
            character.physics.rect.x, character.physics.rect.y = self.level.spawn_cryo

        character.physics.vx, character.physics.vy = 0.0, 0.0

    def reset_level(self):
        """Mereset level 1 dan mengembalikan posisi pemain ke spawn."""
        self.level = Level1()
        self.ignis.physics.rect.x, self.ignis.physics.rect.y = self.level.spawn_ignis
        self.ignis.physics.vx, self.ignis.physics.vy = 0.0, 0.0

        self.cryo.physics.rect.x, self.cryo.physics.rect.y = self.level.spawn_cryo
        self.cryo.physics.vx, self.cryo.physics.vy = 0.0, 0.0

        self.stats.elapsed_time = 0.0

    def update(self, dt, ignis_cmd, cryo_cmd):
        """Memperbarui fisika, level, interaksi bahaya, dan kamera."""
        self.stats.update_time(dt)

        solid_tiles = self.level.get_solid_tiles()
        ice_tiles = self.level.get_ice_tiles()
        one_way = self.level.get_one_way_platforms()

        # Update Karakter
        self.ignis.update(
            dt,
            ignis_cmd.move,
            ignis_cmd.jump_pressed,
            ignis_cmd.jump_released,
            ignis_cmd.dash_pressed,
            ignis_cmd.action_pressed,
            solid_tiles,
            ice_tiles,
            one_way
        )

        self.cryo.update(
            dt,
            cryo_cmd.move,
            cryo_cmd.jump_pressed,
            cryo_cmd.jump_released,
            cryo_cmd.dash_pressed,
            cryo_cmd.action_pressed,
            solid_tiles,
            ice_tiles,
            one_way
        )

        # Update Level Termodinamika
        old_solved = self.level.puzzle_solved
        self.level.update(dt, self.ignis, self.cryo)
        if not old_solved and self.level.puzzle_solved:
            self.toast.show("KEDUA ALTAR TERISI PENUH! PORTAL KELUAR AKTIF!", 4.0)

        # Cek Bahaya Lingkungan (Air cair & Duri)
        HazardSystem.check_hazards(self.level, self.ignis, self.cryo, self.trigger_death)

        # Sinergi Karakter (Thermal Shockwave High-Five)
        if SynergySystem.check_thermal_shockwave(self.ignis, self.cryo):
            self.shockwave_flash = 0.25

        if self.shockwave_flash > 0.0:
            self.shockwave_flash = max(0.0, self.shockwave_flash - dt)

        # Update Partikel & UI Toast
        self.particle_manager.update(dt)
        self.toast.update(dt)

        # Update Kamera
        self.camera.update(dt, [self.ignis.physics.rect, self.cryo.physics.rect])

    def render(self):
        """Menggambar seluruh komponen game ke layar."""
        self.screen.fill(COLOR_BG)

        # Gambar Grid Halus
        cam_ox, cam_oy = self.camera.offset
        grid_size = 40
        for gx in range(0, SCREEN_WIDTH + grid_size, grid_size):
            offset_x = (gx - (cam_ox % grid_size))
            pygame.draw.line(self.screen, (25, 28, 40), (offset_x, 0), (offset_x, SCREEN_HEIGHT), 1)
        for gy in range(0, SCREEN_HEIGHT + grid_size, grid_size):
            offset_y = (gy - (cam_oy % grid_size))
            pygame.draw.line(self.screen, (25, 28, 40), (0, offset_y), (SCREEN_WIDTH, offset_y), 1)

        # Gambar Level & Karakter
        self.level.draw(self.screen, self.camera.offset)
        self.ignis.draw(self.screen, self.camera.offset)
        self.cryo.draw(self.screen, self.camera.offset)

        # Gambar Partikel
        self.particle_manager.draw(self.screen, self.camera.offset)

        # Efek Kilatan Shockwave
        if self.shockwave_flash > 0.0:
            flash_alpha = int((self.shockwave_flash / 0.25) * 140)
            flash_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            flash_surf.fill((255, 255, 255, flash_alpha))
            self.screen.blit(flash_surf, (0, 0))

        # Gambar HUD & Toast
        self.hud.draw(
            self.screen,
            self.current_mode,
            self.active_solo_char,
            self.stats.elapsed_time,
            self.stats.death_count,
            self.clock.get_fps(),
            self.level
        )
        self.toast.draw(self.screen, SCREEN_WIDTH)

        # Layar Kemenangan (Overlay)
        if self.level.level_completed:
            self.victory_modal.draw(
                self.screen,
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
                self.stats.elapsed_time,
                self.stats.death_count
            )

        pygame.display.flip()

    def run(self):
        """Game loop utama."""
        self.running = True
        while self.running:
            dt = min(0.05, self.clock.tick(FPS) / 1000.0)

            ignis_cmd, cryo_cmd = self.input_handler.process_inputs(
                self.current_mode,
                self.active_solo_char
            )

            if self.input_handler.should_quit:
                self.running = False
                break

            if self.input_handler.should_reset:
                self.reset_level()

            if self.input_handler.mode_toggled:
                self.current_mode = (
                    GameMode.SOLO_SWAP
                    if self.current_mode == GameMode.COOP_LOCAL
                    else GameMode.COOP_LOCAL
                )

            if self.input_handler.solo_char_swapped:
                self.active_solo_char = (
                    CharacterType.CRYO
                    if self.active_solo_char == CharacterType.IGNIS
                    else CharacterType.IGNIS
                )

            if not self.level.level_completed:
                self.update(dt, ignis_cmd, cryo_cmd)
            self.render()

        pygame.quit()