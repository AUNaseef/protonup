"""ProtonUp API"""
import os
import shutil
from configparser import ConfigParser
import tarfile
import requests
from .utilities import download, sha512sum
from .constants import CONFIG_FILE, PROTONGE_URL, MIB
from .constants import TEMP_DIR, DEFAULT_INSTALL_DIR


def fetch_data(tag):
    """
    Fetch ProtonGE release information from github
    Return Type: dict
    Content(s):
        'version', date', 'download', 'size', 'checksum'
    """
    url = PROTONGE_URL + (f'tags/{tag}' if tag and tag == 'latest' else 'latest')
    data = requests.get(url).json()
    if 'tag_name' not in data:
        return None  # invalid tag

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
        return False

    protondir = installdir + 'Proton-' + data['version']
    checksum_dir = protondir + '/sha512sum'
    source_checksum = requests.get(data['checksum']).text
    local_checksum = open(checksum_dir).read() if os.path.exists(checksum_dir) else None

    # Check if it already exist
    if os.path.exists(protondir) and not dl_only:
        if local_checksum and source_checksum:
            if local_checksum in source_checksum:
                if not yes:
                    print(f"[INFO] Proton-{data['version']} already installed")
                    print("[INFO] No hotfix found")
                return
            elif not yes:
                print("[INFO] Hotfix available")
        else:
            if not yes:
                print(f"[INFO] Proton-{data['version']} already installed")
            return

    # Confirmation
    if not yes:
        print(f"Ready to download Proton-{data['version']}",
              f"\nSize      : {round(data['size']/MIB, 2)} MiB",
              f"\nPublished : {data['date']}")
        if not input("Continue? (Y/N): ") in ['y', 'Y']:
            return

    # Prepare Destination
    destination = output if output else (os.getcwd() if dl_only else TEMP_DIR)
    if not destination.endswith('/'):
        destination += '/'
    destination += data['download'].split('/')[-1]
    destination = os.path.expanduser(destination)

    # Download
    if not download(url=data['download'], destination=destination, show_progress=not yes):
        if not yes:
            print("[ERROR] Download failed")
        return

    download_checksum = sha512sum(destination)
    if source_checksum and (download_checksum not in source_checksum):
        if not yes:
            print("[ERROR] Checksum verification failed")
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
        return

    # Installation
    if not dl_only:
        if os.path.exists(protondir):
            shutil.rmtree(protondir)
        tarfile.open(destination, "r:gz").extractall(install_directory())
        if not yes:
            print('[INFO] Installed in: ' + protondir)
        open(checksum_dir, 'w').write(download_checksum)
    elif not yes:
        print('[INFO] Dowloaded to: ' + destination)

    # Clean up
    shutil.rmtree(TEMP_DIR, ignore_errors=True)


def remove_proton(version=None, yes=True):
    """Uninstall existing proton installation"""
    target = install_directory() + "Proton-" + version
    if os.path.exists(target):
        if yes or input(f'Are you sure? (Y/N) ') in ['y', 'Y']:
            shutil.rmtree(install_directory() + 'Proton-' + version)
        return True
    return False
