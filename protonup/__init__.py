"""ProtonUp - Manage Proton-GE Installations"""
def main():
    from .cli import main
    return main()

from .api import install_directory, installed_versions
from .api import fetch_data, fetch_releases
from .api import get_proton, remove_proton
