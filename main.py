"""
====================================================================
PHASESHIFT: THERMODYNAMIC DUO
Level 1: "The Awakening" (Fisika Termodinamika Penuh: Air, Es, & Altar Reaktor)
====================================================================
Titik masuk utama (Entry Point) game PhaseShift.
"""
import sys
from core.game import Game

def main():
    game = Game()
    game.run()
    sys.exit()

if __name__ == "__main__":
    main()
