import os
import sys

import PyInstaller.__main__

print("Building FavoritesToPlaylist.exe...")

try:
    # Redirect stdout and stderr to os.devnull to hide debug prints
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')
    
    PyInstaller.__main__.run([
        'FavoritesToPlaylist.py',
        '--onefile',
        '--windowed'
    ])
except Exception as e:
    print(f"Failed to build FavoritesToPlaylist.exe: {str(e)}")
finally:
    # Restore stdout and stderr
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    print("FavoritesToPlaylist.exe built successfully.")