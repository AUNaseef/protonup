"""ProtonUp CLI"""
import sys
import argparse
from .api import install_directory, installed_versions
from .api import get_proton, remove_proton
from .utilities import folder_size
from .constants import TEMP_DIR, MIB


def parse_arguments():
    """Parse commandline arguments"""
    parser = argparse.ArgumentParser(usage="%(prog)s", description="Manage Proton-GE Installations",
                                     epilog="GPLv3 - Repo : https://github.com/AUNaseef/protonup")
    parser.add_argument('-t', '--tag', type=str, default=None, help='install a specific version')
    parser.add_argument('-l', '--list', action='store_true', help='list installed versions')
    parser.add_argument('-r', '--rem', type=str, default=None, metavar='TAG',
                        help='remove existing installations')
    parser.add_argument('-o', '--output', type=str, default=None, metavar='DIR',
                        help='set download directory')
    parser.add_argument('-d', '--dir', type=str, default=None, help='set installation directory')
    parser.add_argument('-y', '--yes', action='store_true', help='disable prompts and logs')
    parser.add_argument('--download', action='store_true', help='download only')
    return parser.parse_args()


def main():
    """Start here"""
    args = parse_arguments()
    if args.dir:
        print(f"Install directory set to '{install_directory(args.dir)}'")
    if args.tag or not (args.rem or args.list or args.dir):
        get_proton(version=args.tag, yes=args.yes, dl_only=args.download,
                   output=args.output)
    if args.rem:
        if not remove_proton(version=args.rem, yes=args.yes):
            print(f'Proton-{args.rem} not installed')
    if args.list:
        for item in installed_versions():
            print(f"{item} - {round(folder_size(install_directory() + item)/MIB, 2)} MiB")
