# BAGUS TERLAMBAT 4 HARI

# PhaseShift (Thermodynamic Duo Platformer)

Game platformer berbasis fisika termal dinamis (*Thermodynamic Flux*) yang dibuat menggunakan Python dan Pygame tanpa game engine.

## Kelompok Stardust
Project Kelompok Stardust, dengan anggota:
   1.Muhammad Andraz Kenang Romero (2632070)
   2.Ica Puspita
   3.Hit Samuel Manurung (2632015)
   4.Arga (2632010)
   5.Riko (2632058)

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

Game ini mendukung mode local co-op dan solo swap.

Player 1 (Ignis, elemen api):
* `A` / `D`: Bergerak ke kiri atau kanan
* `W` / `Space`: Melompat
* `Left Shift`: Dash
* `S`: Heat Stance (mencairkan es, melelehkan tembok penghalang, dan mengisi altar merah saat berada di darat)

Player 2 (Cryo, elemen es):
* `Panah Kiri` / `Panah Kanan`: Bergerak ke kiri atau kanan
* `Panah Atas`: Melompat
* `Right Control` / `Right Shift`: Dash
* `Panah Bawah`: Frost Cast (membekukan air menjadi es dan mengisi altar biru saat berada di darat)

Kontrol umum dan mode solo:
* `M`: Beralih antara mode Co-op Lokal dan Solo Swap
* `Tab`: Berganti karakter aktif saat berada di mode Solo Swap (tombol gerak, lompat, dash, dan skill mengendalikan karakter yang sedang aktif)
* `R`: Reset level
* `Esc`: Keluar dari game

Sinergi spesial (Thermal Shockwave):
* Lakukan dash dengan Ignis dan Cryo ke arah satu sama lain hingga bertabrakan untuk memicu pantulan termal.

## Struktur direktori

* `core/`: Siklus hidup game loop (`Game`), input controller (`InputHandler`), dan manajemen state.
* `engine/`: Sistem fisika kustom (AABB kinematics, coyote time), kamera dinamis, dan particle manager.
* `entities/`: Controller karakter untuk Ignis dan Cryo.
* `gameplay/`: Deteksi bahaya lingkungan (*hazards*) dan sinergi elemen (*thermal shockwave*).
* `levels/`: Peta level berbasis matriks ASCII dan sistem termodinamika (Water, Ice, Crucible).
* `ui/`: Tampilan HUD, notifikasi toast, panduan dinamis, dan layar kemenangan (*victory modal*).
* `assets/`: Sound synthesizer dan aset sprite pixel-art.
