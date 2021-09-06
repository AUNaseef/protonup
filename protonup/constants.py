"""Constant Values"""
import os
CONFIG_FILE = os.path.expanduser('~/.config/protonup/config.ini')
DEFAULT_INSTALL_DIR = os.path.expanduser('~/.steam/root/compatibilitytools.d/')
POSSIBLE_INSTALL_LOCATIONS = [
    {'install_dir': '~/.steam/root/compatibilitytools.d/', 'display_name': 'Steam'},
    {'install_dir': '~/.var/app/com.valvesoftware.Steam/data/Steam/compatibilitytools.d/', 'display_name': 'Steam (Flatpak)'}
]
TEMP_DIR = '/tmp/protonup/'
PROTONGE_URL = 'https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases'
BUFFER_SIZE = 65536  # Work with 64 kb chunks
