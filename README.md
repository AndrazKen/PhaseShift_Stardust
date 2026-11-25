# PhaseShift (Thermodynamic Duo Platformer)

Game platformer berbasis fisika termal dinamis (*Thermodynamic Flux*) yang dibuat menggunakan Python dan Pygame tanpa game engine.

## Cara menjalankan

1. Clone repository ini lalu masuk ke folder project:
   ```bash
   git clone https://github.com/AndrazKen/PhaseShift_Stardust.git
   cd PhaseShift_Stardust
   ```
2. Pasang dependency yang dibutuhkan:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan game melalui terminal:
   ```bash
   python main.py
   ```
   Jika menggunakan Windows, Anda juga bisa langsung menjalankan `run_game.bat`.

## Kontrol game

Game ini mendukung mode local co-op maupun single player.

Player 1 (Ignis, elemen api):
* `A` / `D`: Bergerak ke kiri atau kanan
* `W` / `Space`: Melompat
* `Left Shift`: Heat Dash untuk mencairkan es dan memanaskan air menjadi geyser

Player 2 (Cryo, elemen es):
* `Panah Kiri` / `Panah Kanan`: Bergerak ke kiri atau kanan
* `Panah Atas`: Melompat
* `Right Control`: Frost Glaze untuk membekukan air menjadi es dan mendinginkan lava

Sinergi spesial (Thermal Shockwave):
* Lakukan dash ke arah satu sama lain saat berada di udara untuk memicu ledakan termal yang bisa memecahkan rintangan.

## Struktur direktori

* `core/`: Siklus hidup game loop (`Game`), input controller (`InputHandler`), dan manajemen state.
* `engine/`: Sistem fisika kustom (AABB kinematics, coyote time), kamera dinamis, dan particle manager.
* `entities/`: Controller karakter untuk Ignis dan Cryo.
* `gameplay/`: Deteksi bahaya lingkungan (*hazards*) dan sinergi elemen (*thermal shockwave*).
* `levels/`: Peta level berbasis matriks ASCII dan sistem termodinamika (Water, Ice, Crucible).
* `ui/`: Tampilan HUD, notifikasi toast, panduan dinamis, dan layar kemenangan (*victory modal*).
* `assets/`: Sound synthesizer dan aset sprite pixel-art.
