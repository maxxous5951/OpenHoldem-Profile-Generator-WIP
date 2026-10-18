"""Double-clic : lance l'interface sans console (Windows)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ohpg.gui.app import run

sys.exit(run())
