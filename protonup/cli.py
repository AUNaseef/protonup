"""ProtonUp CLI"""
import argparse
from .api import install_directory, installed_versions
from .api import get_proton, remove_proton, fetch_releases
from .utilities import folder_size, readable_size


def parse_arguments():
    """Parse commandline arguments"""
    parser = argparse.ArgumentParser(usage="%(prog)s", description="Manage Proton-GE Installations",
                                     epilog="GPLv3 - Repo : https://github.com/AUNaseef/protonup")
    parser.add_argument('-t', '--tag', type=str, default=None, help='install a specific version')
    parser.add_argument('-l', '--list', action='store_true', help='list installed versions')
    parser.add_argument('-r', '--remove', type=str, default=None, metavar='TAG',
                        help='remove existing installations')
    parser.add_argument('-o', '--output', type=str, default=None, metavar='DIR',
                        help='set download directory')
    parser.add_argument('-d', '--dir', type=str, default=None, help='set installation directory')
    parser.add_argument('-y', '--yes', action='store_true', help='disable prompts and logs')
    parser.add_argument('--download', action='store_true', help='download only')
    parser.add_argument('--releases', action='store_true', help='list available versions')
    return parser.parse_args()


def main():
    """Start here"""
    args = parse_arguments()

    if args.dir:
        print(f"Install directory set to '{install_directory(args.dir)}'")

    if args.tag or not (args.remove or args.list or args.dir or args.releases):
        get_proton(version=args.tag, yes=args.yes, dl_only=args.download,
                   output=args.output)
    if args.remove:
        if args.yes or input(f"Confirm remove {args.remove}? (Y/n): ") not in ['y', 'Y', '']:
            return
        if not remove_proton(version=args.remove):
            print(f'Proton-{args.remove} not installed')

    if args.list:
        _install_directory = install_directory()
        for item in installed_versions():
            print(f"{item} - {readable_size(folder_size(_install_directory + item))}")

    if args.releases:
        for tag in fetch_releases():
            print(tag)
