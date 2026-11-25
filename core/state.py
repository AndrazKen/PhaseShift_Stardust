"""
Manajemen mode dan status permainan PhaseShift.
"""
from entities.player import CharacterType

class GameMode:
    COOP_LOCAL = "2-Player Co-op"
    SOLO_SWAP = "1-Player (Solo Swap)"

class GameStats:
    def __init__(self):
        self.death_count = 0
        self.elapsed_time = 0.0

    def record_death(self):
        self.death_count += 1

    def update_time(self, dt):
        self.elapsed_time += dt

    def reset(self):
        self.death_count = 0
        self.elapsed_time = 0.0
