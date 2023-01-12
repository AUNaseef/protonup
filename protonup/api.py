"""ProtonUp API"""
import os
import shutil
from configparser import ConfigParser
import tarfile
import requests
from .utilities import download, sha512sum, readable_size
from .constants import CONFIG_FILE, PROTONGE_URL
from .constants import TEMP_DIR, DEFAULT_INSTALL_DIR


def fetch_data(tag) -> dict:
    """
    Fetch ProtonGE release information from github
    Return Type: dict {str, str}
    Content(s):
        'version', date', 'download', 'size', 'checksum'
    """
    url = PROTONGE_URL + (f'/tags/{tag}' if tag else '/latest')
    data = requests.get(url).json()
    if 'tag_name' not in data:
        return {}  # invalid tag

    values = {'version': data['tag_name'], 'date': data['published_at'].split('T')[0]}
    for asset in data['assets']:
        if asset['name'].endswith('sha512sum'):
            values['checksum'] = asset['browser_download_url']
        elif asset['name'].endswith('tar.gz'):
            values['download'] = asset['browser_download_url']
            values['size'] = asset['size']
    return values


def fetch_releases(count=100) -> list:
    """
    List ProtonGE releases on Github
    Return Type: list[str]
    """
    tags = []
    for release in requests.get(PROTONGE_URL + "?per_page=" + str(count)).json():
        tags.append(release['tag_name'])
    tags.reverse()
    return tags


def install_directory(target=None) -> str:
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


def installed_versions() -> list:
    """
    List of proton installations
    Return Type: list[str]
    """
    installdir = install_directory()
    versions_found = []

    if os.path.exists(installdir):
        folders = os.listdir(installdir)
        # Find names of directories with proton
        versions_found = [folder for folder in folders if os.path.exists(installdir + '/' + folder + "/proton")]

    return versions_found


def get_proton(version=None, yes=True, dl_only=False, output=None) -> bool:
    """Download and (optionally) install Proton"""
    installdir = install_directory()
    data = fetch_data(tag=version)

    if not data or 'download' not in data:
        if not yes:
            print('[ERROR] invalid tag / binary not found')
        return False

    protondir = installdir + data['version']
    checksum_dir = protondir + '/sha512sum'
    source_checksum = requests.get(data['checksum']).text if 'checksum' in data else None
    local_checksum = open(checksum_dir).read() if os.path.exists(checksum_dir) else None

    # Check if it already exist
    if os.path.exists(protondir) and not dl_only:
        if local_checksum and source_checksum:
            if local_checksum in source_checksum:
                if not yes:
                    print(f"[INFO] {data['version']} already installed")
                    print("[INFO] No hotfix found")
                return False
            elif not yes:
                print("[INFO] Hotfix available")
        else:
            if not yes:
                print(f"[INFO] {data['version']} already installed")
            return False

    # Confirmation
    if not yes:
        print(f"Ready to download {data['version']}",
              f"\nSize      : {readable_size(data['size'])}",
              f"\nPublished : {data['date']}")
        if input("Continue? (Y/n): ") not in ['y', 'Y', '']:
            return False

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
        return True

    download_checksum = sha512sum(destination)
    if source_checksum and (download_checksum not in source_checksum):
        if not yes:
            print("[ERROR] Checksum verification failed")
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
        return True

    # Installation
    if not dl_only:
        if os.path.exists(protondir):
            shutil.rmtree(protondir)
        tarfile.open(destination, "r:gz").extractall(install_directory())
        if not yes:
            print('[INFO] Installed in: ' + protondir)
        open(checksum_dir, 'w').write(download_checksum)
    elif not yes:
        print('[INFO] Downloaded to: ' + destination)

    # Clean up
    shutil.rmtree(TEMP_DIR, ignore_errors=True)

    return True


def remove_proton(version=None) -> bool:
    """Uninstall existing proton installation"""
    target = install_directory() + str(version)
    if os.path.exists(target):
        shutil.rmtree(target)
        return True
    return False
