@echo off
title PhaseShift: Thermodynamic Duo
cd /d "C:\PhaseShift"
python main.py
if errorlevel 1 (
    echo.
    echo Ada error saat menjalankan game. Tekan sembarang tombol untuk keluar.
    pause > nul
)
