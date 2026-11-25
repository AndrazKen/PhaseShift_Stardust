"""
Sistem fisika kustom (kinematika platformer modern, AABB collision, & One-Way Jump-Through Platforms).
"""
import pygame
from settings import (
    GRAVITY, TERMINAL_VELOCITY, ACCELERATION, 
    FRICTION_NORMAL, FRICTION_ICE, MOVE_SPEED,
    JUMP_FORCE, COYOTE_TIME, JUMP_BUFFER_TIME
)

class PhysicsBody:
    def __init__(self, x, y, width, height):
        self.rect = pygame.FRect(x, y, width, height)
        self.vx = 0.0
        self.vy = 0.0
        
        # State tabrakan
        self.on_ground = False
        self.on_ice = False
        self.hit_ceiling = False
        self.hit_wall = False
        
        # Game Feel
        self.coyote_timer = 0.0
        self.jump_buffer_timer = 0.0
        self.facing_right = True

    def update_horizontal(self, dt, move_input, is_dashing=False):
        if is_dashing:
            return

        friction = FRICTION_ICE if self.on_ice else FRICTION_NORMAL

        if move_input != 0:
            self.facing_right = (move_input > 0)
            target_speed = move_input * MOVE_SPEED
            if (self.vx < target_speed and move_input > 0) or (self.vx > target_speed and move_input < 0):
                self.vx += move_input * ACCELERATION * dt
                if move_input > 0 and self.vx > target_speed:
                    self.vx = target_speed
                elif move_input < 0 and self.vx < target_speed:
                    self.vx = target_speed
            else:
                self.vx = target_speed
        else:
            if self.vx > 0:
                self.vx = max(0.0, self.vx - friction * dt)
            elif self.vx < 0:
                self.vx = min(0.0, self.vx + friction * dt)

    def apply_gravity(self, dt, is_dashing=False):
        if not is_dashing:
            self.vy = min(TERMINAL_VELOCITY, self.vy + GRAVITY * dt)

    def update_timers(self, dt):
        if self.on_ground:
            self.coyote_timer = COYOTE_TIME
        else:
            self.coyote_timer = max(0.0, self.coyote_timer - dt)

        if self.jump_buffer_timer > 0:
            self.jump_buffer_timer = max(0.0, self.jump_buffer_timer - dt)

    def queue_jump(self):
        self.jump_buffer_timer = JUMP_BUFFER_TIME

    def try_jump(self):
        can_jump = (self.coyote_timer > 0.0 or self.on_ground)
        wants_jump = (self.jump_buffer_timer > 0.0)

        if can_jump and wants_jump:
            self.vy = JUMP_FORCE
            self.coyote_timer = 0.0
            self.jump_buffer_timer = 0.0
            self.on_ground = False
            return True
        return False

    def cut_jump(self):
        if self.vy < -100.0:
            self.vy *= 0.45

    def resolve_collisions(self, dt, solid_tiles, ice_tiles=None, one_way_platforms=None):
        """
        Resolusi tabrakan AABB sumbu terpisah.
        Mendukung One-Way Platforms: bisa dilompati tembus dari bawah, mendarat kokoh di atasnya.
        """
        ice_tiles = ice_tiles or []
        one_way_platforms = one_way_platforms or []

        # 1. Gerak & Tabrakan Sumbu X (Hanya dengan solid tiles, tidak terhalang oleh one-way)
        self.rect.x += self.vx * dt
        self.hit_wall = False
        for tile in solid_tiles:
            if self.rect.colliderect(tile):
                if self.vx > 0:
                    self.rect.right = tile.left
                    self.hit_wall = True
                elif self.vx < 0:
                    self.rect.left = tile.right
                    self.hit_wall = True
                self.vx = 0.0

        # 2. Gerak & Tabrakan Sumbu Y
        prev_bottom = self.rect.bottom
        self.rect.y += self.vy * dt
        self.on_ground = False
        self.hit_ceiling = False
        self.on_ice = False

        # Tabrakan dengan Solid Tiles (Lantai, Tembok, Atap)
        for tile in solid_tiles:
            if self.rect.colliderect(tile):
                if self.vy > 0:
                    self.rect.bottom = tile.top
                    self.vy = 0.0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = tile.bottom
                    self.vy = 0.0
                    self.hit_ceiling = True

        # Tabrakan dengan One-Way Platforms (Hanya saat jatuh ke bawah vy >= 0)
        if self.vy >= 0:
            for plat in one_way_platforms:
                if self.rect.right > plat.left and self.rect.left < plat.right:
                    # Jika posisi kaki sebelumnya berada di atas atau sejajar permukaan platform
                    if prev_bottom <= plat.top + 14 and self.rect.bottom >= plat.top:
                        self.rect.bottom = plat.top
                        self.vy = 0.0
                        self.on_ground = True

        # Periksa pijakan es
        if self.on_ground:
            feet_sensor = pygame.FRect(self.rect.x, self.rect.bottom, self.rect.width, 4)
            for ice in ice_tiles:
                if feet_sensor.colliderect(ice):
                    self.on_ice = True
                    break
