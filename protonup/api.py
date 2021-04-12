"""ProtonUp API"""
import os
import shutil
from configparser import ConfigParser
import tarfile
import requests
from .utilities import download
from .constants import CONFIG_FILE, PROTONGE_URL, MIB
from .constants import TEMP_DIR, DEFAULT_INSTALL_DIR


def fetch_data(tag):
    """
    Fetch ProtonGE release information from github
    Return Type: dict
    Content(s):
        'version', date', 'download', 'size', 'checksum'
    """
    url = PROTONGE_URL + (f'tags/{tag}' if tag and tag is not 'latest' else 'latest')
    data = requests.get(url).json()
    if 'tag_name' not in data:
        return  # invalid tag

    values = {'version': data['tag_name'], 'date': data['published_at'].split('T')[0]}
    for asset in data['assets']:
        if asset['name'].endswith('sha512sum'):
            values['checksum'] = asset['browser_download_url']
        elif asset['name'].endswith('tar.gz'):
            values['download'] = asset['browser_download_url']
            values['size'] = asset['size']
    return values


def install_directory(target=None):
    """
    Custom install directory
    Return Type: str
    """
    config = ConfigParser()
    if target and target.lower() != 'get':
        if target.lower() == 'default':
            target = DEFAULT_INSTALL_DIR
        if not target.endswith('/'):
            target += '/'
        if not config.has_section('protonup'):
            config.add_section('protonup')
        config['protonup']['installdir'] = target
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, 'w') as file:
            config.write(file)
        return target
    elif os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        if config.has_option('protonup', 'installdir'):
            return os.path.expanduser(config['protonup']['installdir'])
    else:
        return DEFAULT_INSTALL_DIR


def installed_versions():
    """
    List of proton installations
    Return Type: str[]
    """
    installdir = install_directory()
    versions_found = []

    if os.path.exists(installdir):
        folders = os.listdir(installdir)
        # Find names of directories with proton
        for folder in folders:
            if os.path.exists(f'{installdir}/{folder}/proton'):
                versions_found.append(folder)

    return versions_found


def get_proton(version=None, yes=True, dl_only=False, output=None):
    """Download and (optionally) install Proton"""
    installdir = install_directory()
    data = fetch_data(tag=version)

    if not data or 'download' not in data:
        if not yes:
            print('[ERROR] invalid tag / binary not found')
        return False  # invalid tag or no download link

    protondir = installdir + 'Proton-' + data['version']

    if os.path.exists(protondir) and not dl_only:
        # TODO: Check if data['hash'] matches installation
        if not yes:
            print(f"[INFO] Proton-{data['version']} already installed")
        return False

    if not yes:
        print(f"Ready to download Proton-{data['version']}",
              f"\nSize      : {round(data['size']/MIB, 2)} MiB",
              f"\nPublished : {data['date']}")
        if not input("Continue? (Y/N): ") in ['y', 'Y']:
            return

    # Prepare destination
    destination = output if output else (os.getcwd() if dl_only else TEMP_DIR)
    if not destination.endswith('/'):
        destination += '/'
    destination += data['download'].split('/')[-1]
    destination = os.path.expanduser(destination)

    download(url=data['download'], destination=destination, show_progress=not yes)
    # TODO: Check if data['hash'] matches the downloaded file

    # Installation
    if not dl_only:
        if os.path.exists(protondir):
            shutil.rmtree(protondir)
        tarfile.open(destination, "r:gz").extractall(install_directory())
        if not yes:
            print('[INFO] Installed in: ' + protondir)
    elif not yes:
        print('[INFO] Dowloaded to: ' + destination)

    shutil.rmtree(TEMP_DIR, ignore_errors=True)


def remove_proton(version=None, yes=True):
    """Uninstall existing proton installation"""
    target = install_directory() + "Proton-" + version
    if os.path.exists(target):
        if yes or input(f'Do you want to remove {version}? (y/n) : ') in ['y', 'Y']:
            shutil.rmtree(install_directory() + 'Proton-' + version)
    else:
        return False
    return True
