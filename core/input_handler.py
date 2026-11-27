"""
Input Handler untuk PhaseShift:
Mengelola event input diskrit dan continuous mapping untuk Co-op dan Solo Swap.
"""
import pygame
from core.state import GameMode
from entities.player import CharacterType

class ActionState:
    """Menyimpan status aksi sesaat untuk satu karakter."""
    def __init__(self):
        self.move = 0.0
        self.jump_pressed = False
        self.jump_released = False
        self.dash_pressed = False
        self.action_pressed = False

class InputHandler:
    def __init__(self):
        self.should_quit = False
        self.should_reset = False
        self.mode_toggled = False
        self.solo_char_swapped = False

    def process_inputs(self, current_mode, active_solo_char):
        """
        Memproses event queue dan continuous key press.
        Mengembalikan tuple (ignis_actions, cryo_actions).
        """
        self.should_quit = False
        self.should_reset = False
        self.mode_toggled = False
        self.solo_char_swapped = False

        ignis = ActionState()
        cryo = ActionState()

        # 1. Event Polling (Diskrit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.should_quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.should_quit = True
                elif event.key == pygame.K_r:
                    self.should_reset = True
                elif event.key == pygame.K_m:
                    self.mode_toggled = True
                elif event.key == pygame.K_TAB:
                    if current_mode == GameMode.SOLO_SWAP:
                        self.solo_char_swapped = True

                # Tombol Ignis
                if event.key in (pygame.K_w, pygame.K_SPACE):
                    ignis.jump_pressed = True
                if event.key == pygame.K_LSHIFT:
                    ignis.dash_pressed = True
                if event.key == pygame.K_s:
                    ignis.action_pressed = True

                # Tombol Cryo
                if event.key == pygame.K_UP:
                    cryo.jump_pressed = True
                if event.key in (pygame.K_RCTRL, pygame.K_RSHIFT):
                    cryo.dash_pressed = True
                if event.key == pygame.K_DOWN:
                    cryo.action_pressed = True

            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_w, pygame.K_SPACE):
                    ignis.jump_released = True
                if event.key == pygame.K_UP:
                    cryo.jump_released = True

        # 2. Continuous Input Processing
        keys = pygame.key.get_pressed()

        if current_mode == GameMode.COOP_LOCAL:
            if keys[pygame.K_a]: ignis.move -= 1.0
            if keys[pygame.K_d]: ignis.move += 1.0
            if keys[pygame.K_s]: ignis.action_pressed = True

            if keys[pygame.K_LEFT]: cryo.move -= 1.0
            if keys[pygame.K_RIGHT]: cryo.move += 1.0
            if keys[pygame.K_DOWN]: cryo.action_pressed = True
            return ignis, cryo

        # Mode Solo Swap: arahkan semua kontrol hanya ke karakter aktif
        active = ActionState()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: active.move -= 1.0
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: active.move += 1.0
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: active.action_pressed = True

        active.jump_pressed = ignis.jump_pressed or cryo.jump_pressed
        active.jump_released = ignis.jump_released or cryo.jump_released
        active.dash_pressed = ignis.dash_pressed or cryo.dash_pressed
        active.action_pressed = active.action_pressed or ignis.action_pressed or cryo.action_pressed

        if active_solo_char == CharacterType.IGNIS:
            return active, ActionState()
        return ActionState(), active
