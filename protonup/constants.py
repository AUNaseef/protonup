"""Constant Values"""
import os
CONFIG_FILE = os.path.expanduser('~/.config/protonup/config.ini')
DEFAULT_INSTALL_DIR = os.path.expanduser('~/.steam/root/compatibilitytools.d/')
TEMP_DIR = '/tmp/protonup/'
PROTONGE_URL = 'https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases/'
MIB = 1048576  # One mebibyte in bytes
BUFFER_SIZE = 65536  # Work with 64 kb chunks
