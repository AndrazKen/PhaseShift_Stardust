"""
Kelas entitas karakter Ignis & Cryo.
Mengelola state machine animasi, loading sprite pixel art, dan skill termal.
"""
import pygame
import os
import math
from engine.physics import PhysicsBody
from settings import (
    COLOR_IGNIS_GLOW, COLOR_CRYO_GLOW,
    COLOR_IGNIS_BODY, COLOR_CRYO_BODY
)

class CharacterType:
    IGNIS = "ignis"
    CRYO = "cryo"

class PlayerState:
    IDLE = "idle"
    WALK = "walk"
    JUMP = "jump"
    FALL = "fall"
    DASH = "dash"
    ACTION = "action"

class Player:
    def __init__(self, x, y, char_type=CharacterType.IGNIS):
        self.char_type = char_type
        
        # Hitbox fisik (lebar 32px, tinggi 52px)
        self.physics = PhysicsBody(x, y, 32, 52)
        
        # State animasi
        self.state = PlayerState.IDLE
        self.anim_time = 0.0
        
        # Kemampuan Dash
        self.dash_timer = 0.0
        self.dash_duration = 0.22
        self.dash_cooldown_timer = 0.0
        self.dash_cooldown = 0.55
        self.dash_speed = 680.0
        self.dash_dir = 1
        self.dash_ghosts = []  # Efek bayangan jejak dash (motion blur)
        
        # Kemampuan Khusus (Heat Stance / Frost Cast)
        self.is_acting = False
        self.action_timer = 0.0
        self.action_duration = 0.40
        
        # Efek visual
        self.glow_color = COLOR_IGNIS_GLOW if char_type == CharacterType.IGNIS else COLOR_CRYO_GLOW
        self.body_color = COLOR_IGNIS_BODY if char_type == CharacterType.IGNIS else COLOR_CRYO_BODY
        
        # Memuat sprites
        self.sprites = {}
        self.load_sprites()

    def load_sprites(self):
        """Memuat sprite pixel-art transparan dan mengubah ukurannya sesuai proporsi."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        base_dir = os.path.join(project_root, "assets", "sprites", self.char_type)
        action_name = "heat_stance" if self.char_type == CharacterType.IGNIS else "frost_cast"
        
        sprite_files = {
            PlayerState.IDLE: "idle.png",
            PlayerState.WALK: "walk.png",
            PlayerState.JUMP: "jump.png",
            PlayerState.FALL: "fall.png",
            PlayerState.DASH: "dash.png",
            PlayerState.ACTION: f"{action_name}.png",
        }
        
        target_height = 54  # Proporsional dengan tile 40px
        
        for state, filename in sprite_files.items():
            path = os.path.join(base_dir, filename)
            if os.path.exists(path):
                raw_img = pygame.image.load(path)
                if pygame.display.get_surface() is not None:
                    img = raw_img.convert_alpha()
                else:
                    img = raw_img
                w, h = img.get_size()
                scale_ratio = target_height / max(1, h)
                target_w = max(1, int(w * scale_ratio))
                scaled = pygame.transform.smoothscale(img, (target_w, target_height))
                self.sprites[state] = scaled
            else:
                self.sprites[state] = None

    def trigger_dash(self):
        """Memicu gerakan dash cepat ke arah karakter menghadap."""
        if self.dash_cooldown_timer <= 0.0 and self.dash_timer <= 0.0:
            self.dash_timer = self.dash_duration
            self.dash_cooldown_timer = self.dash_cooldown
            self.dash_dir = 1 if self.physics.facing_right else -1
            self.physics.vx = self.dash_dir * self.dash_speed
            self.physics.vy = 0.0
            return True
        return False

    def trigger_action(self):
        """Memicu Heat Stance (Ignis) atau Frost Cast (Cryo)."""
        if not self.is_acting and self.physics.on_ground:
            self.is_acting = True
            self.action_timer = self.action_duration
            self.physics.vx = 0.0
            return True
        return False

    def update(self, dt, move_input, jump_pressed, jump_released, dash_pressed, action_pressed, solid_tiles, ice_tiles, one_way_platforms=None):
        self.anim_time += dt
        
        # 1. Update cooldown dash & action
        if self.dash_cooldown_timer > 0.0:
            self.dash_cooldown_timer = max(0.0, self.dash_cooldown_timer - dt)
            
        if self.action_timer > 0.0:
            self.action_timer = max(0.0, self.action_timer - dt)
            if self.action_timer == 0.0:
                self.is_acting = False

        # 2. Proses Input Aksi
        if dash_pressed:
            self.trigger_dash()
            
        if action_pressed:
            self.trigger_action()

        is_dashing = (self.dash_timer > 0.0)
        if is_dashing:
            self.dash_timer = max(0.0, self.dash_timer - dt)
            self.physics.vx = self.dash_dir * self.dash_speed
            self.physics.vy = 0.0  # Melayang di udara saat dash
            # Tambahkan jejak bayangan dash
            self.dash_ghosts.append({
                "x": self.physics.rect.x,
                "y": self.physics.rect.y,
                "alpha": 180,
                "facing_right": self.physics.facing_right,
                "state": PlayerState.DASH
            })
        else:
            # Kontrol pergerakan normal jika tidak sedang Heat Stance / Frost Cast
            if self.is_acting:
                self.physics.vx = 0.0
            else:
                self.physics.update_horizontal(dt, move_input, is_dashing=False)

        # 3. Proses Lompat
        self.physics.update_timers(dt)
        if jump_pressed and not self.is_acting:
            self.physics.queue_jump()
        self.physics.try_jump()
        
        if jump_released:
            self.physics.cut_jump()

        # 4. Terapkan Gravitasi & Tabrakan
        self.physics.apply_gravity(dt, is_dashing=is_dashing)
        self.physics.resolve_collisions(dt, solid_tiles, ice_tiles, one_way_platforms)

        # 5. Tentukan State Animasi
        if is_dashing:
            self.state = PlayerState.DASH
        elif self.is_acting:
            self.state = PlayerState.ACTION
        elif not self.physics.on_ground:
            if self.physics.vy < 0:
                self.state = PlayerState.JUMP
            else:
                self.state = PlayerState.FALL
        elif abs(self.physics.vx) > 20:
            self.state = PlayerState.WALK
        else:
            self.state = PlayerState.IDLE

        # 6. Update bayangan jejak dash
        for ghost in self.dash_ghosts[:]:
            ghost["alpha"] -= 600 * dt
            if ghost["alpha"] <= 0:
                self.dash_ghosts.remove(ghost)

    def draw(self, surface, camera_offset=(0, 0)):
        ox, oy = camera_offset
        draw_x = self.physics.rect.x - ox
        draw_y = self.physics.rect.y - oy

        # 1. Gambar jejak bayangan dash (ghosting effect)
        for ghost in self.dash_ghosts:
            sprite = self.sprites.get(ghost["state"])
            if sprite:
                g_img = sprite.copy()
                g_img.set_alpha(int(ghost["alpha"]))
                if not ghost["facing_right"]:
                    g_img = pygame.transform.flip(g_img, True, False)
                gx = ghost["x"] - ox
                gy = ghost["y"] - oy
                # Center sprite di atas hitbox
                diff_w = (g_img.get_width() - self.physics.rect.width) // 2
                diff_h = g_img.get_height() - self.physics.rect.height
                surface.blit(g_img, (gx - diff_w, gy - diff_h))

        # 2. Gambar Karakter Utama
        sprite = self.sprites.get(self.state) or self.sprites.get(PlayerState.IDLE)
        if sprite:
            img = sprite
            # Efek 'breathing/bobbing' lembut saat Idle atau Walk
            bob_y = 0
            if self.state == PlayerState.IDLE:
                bob_y = math.sin(self.anim_time * 5.0) * 2.0
            elif self.state == PlayerState.WALK:
                bob_y = abs(math.sin(self.anim_time * 12.0)) * 3.0

            if not self.physics.facing_right:
                img = pygame.transform.flip(img, True, False)

            # Posisi sprite: diletakkan pas menempel ke dasar hitbox kaki
            diff_w = (img.get_width() - self.physics.rect.width) // 2
            diff_h = img.get_height() - self.physics.rect.height
            surface.blit(img, (draw_x - diff_w, draw_y - diff_h + bob_y))
        else:
            # Fallback jika sprite tidak ditemukan: kotak warna berpendar
            pygame.draw.rect(surface, self.body_color, (draw_x, draw_y, self.physics.rect.width, self.physics.rect.height), border_radius=4)

        # 3. Gambar Aura Partikel Kecil
        glow_alpha = int(120 + 40 * math.sin(self.anim_time * 6.0))
        glow_surf = pygame.Surface((self.physics.rect.width + 16, 8), pygame.SRCALPHA)
        pygame.draw.ellipse(glow_surf, (*self.glow_color, glow_alpha), glow_surf.get_rect())
        surface.blit(glow_surf, (draw_x - 8, draw_y + self.physics.rect.height - 4))
