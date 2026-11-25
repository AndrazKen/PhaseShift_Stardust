# ❄️🔥 PhaseShift (Thermodynamic Duo Platformer)

Game platformer berbasis fisika termal dinamis (*Thermodynamic Flux*) yang dibuat **100% menggunakan Python murni** tanpa game engine.

---

## 🎮 Kontrol Game (Local Co-op / Single Player)

* **Player 1 (Ignis - Panas / Api)**:
  * `A` / `D` : Bergerak Kiri / Kanan
  * `W` / `Space` : Melompat
  * `Left Shift` : Heat Dash (Mencairkan es, memanaskan air jadi geyser)

* **Player 2 (Cryo - Dingin / Es)**:
  * `Panah Kiri` / `Panah Kanan` : Bergerak Kiri / Kanan
  * `Panah Atas` : Melompat
  * `Right Control` : Frost Glaze (Membekukan air jadi es, mendinginkan lava)

* **Sinergi Spesial**:
  * **Thermal Shockwave**: Dash ke arah satu sama lain di udara untuk memicu ledakan termal pemecah rintangan!

---

## 📁 Struktur Direktori
* `core/`: Siklus hidup game loop (`Game`), input controller (`InputHandler`), dan state management.
* `engine/`: Sistem fisika kustom (AABB kinematics, coyote time), dynamic camera, dan particle manager.
* `entities/`: Controller karakter (Ignis & Cryo).
* `gameplay/`: Deteksi bahaya lingkungan (*hazards*) dan sinergi elemen (*thermal shockwave*).
* `levels/`: Peta level berbasis matriks ASCII & sistem termodinamika (Water, Ice, Crucible).
* `ui/`: Tampilan HUD, popup toast notification, panduan dinamis, dan victory modal.
* `assets/`: Sound synthesizer & aset visual sprites pixel-art.
