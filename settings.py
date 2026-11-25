"""
Konfigurasi dan konstanta global untuk game PhaseShift.
"""

# =========================
# PENGATURAN DISPLAY & WINDOW
# =========================
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Thermodynamic Duo"

# Ukuran Tile Grid
TILE_SIZE = 40

# =========================
# PALET WARNA (RGB)
# =========================
COLOR_BG = (18, 20, 28)
COLOR_TEXT = (240, 240, 245)

# Ignis (Panas)
COLOR_IGNIS_BODY = (255, 90, 30)
COLOR_IGNIS_GLOW = (255, 160, 40)
COLOR_IGNIS_CORE = (255, 230, 150)

# Cryo (Dingin)
COLOR_CRYO_BODY = (40, 170, 255)
COLOR_CRYO_GLOW = (100, 220, 255)
COLOR_CRYO_CORE = (220, 250, 255)

# Material Lingkungan
COLOR_SOLID = (60, 65, 80)
COLOR_WATER = (30, 100, 220, 180)
COLOR_ICE = (180, 230, 255, 230)
COLOR_STEAM = (220, 230, 240, 120)
COLOR_LAVA = (230, 50, 10)
COLOR_OBSIDIAN = (35, 30, 45)
COLOR_VINES = (50, 140, 60)

# =========================
# FISIKA KINEMATIK
# =========================
GRAVITY = 1300.0            # Piksel per detik kuadrat
TERMINAL_VELOCITY = 850.0

# Kecepatan Karakter (Piksel per detik)
MOVE_SPEED = 290.0
ACCELERATION = 1500.0
FRICTION_NORMAL = 1600.0
FRICTION_ICE = 250.0        # Licin di atas es

# Karakteristik Lompat
JUMP_FORCE = -570.0         # Daya lompat responsif (mampu melompati hingga 3 tile tinggi)
COYOTE_TIME = 0.12          # Toleransi melompat setelah lepas tebing (detik)
JUMP_BUFFER_TIME = 0.10     # Toleransi menekan lompat sebelum mendarat (detik)

# =========================
# MEKANIK TERMODINAMIKA
# =========================
TEMP_IGNIS = 100.0          # °C
TEMP_CRYO = -100.0          # °C
TEMP_AMBIENT = 20.0         # °C

# Ambang Batas Fase Air
TEMP_FREEZE = 0.0           # Air -> Es
TEMP_BOIL = 100.0           # Air -> Uap
TEMP_MELT_OBSIDIAN = 200.0  # Lava membeku di bawah suhu ini

# =========================
# NETWORK MULTIPLAYER
# =========================
DEFAULT_PORT = 7777
MAX_PACKET_SIZE = 1024
