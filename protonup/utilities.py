"""Utilities"""
import os
import sys
import hashlib
import requests
from .constants import BUFFER_SIZE


def readable_size(num, suffix='B'):
    """ Convert bytes to readable values """
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)


def download(url, destination, show_progress=False):
    """Download files"""
    try:
        file = requests.get(url, stream=True)
    except OSError:
        return False  # Network error

    if show_progress:
        f_size = int(file.headers.get('content-length'))
        f_size_r = readable_size(f_size)
        c_count = int(f_size / BUFFER_SIZE)
        c_current = 1
    destination = os.path.expanduser(destination)
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, 'wb') as dest:
        for chunk in file.iter_content(chunk_size=BUFFER_SIZE):
            if chunk:
                dest.write(chunk)
                dest.flush()
            if show_progress:
                progress = min((c_current / c_count) * 100, 100.00)
                downloaded = readable_size(c_current * BUFFER_SIZE)
                sys.stdout.write(f'\rDownloaded {progress:.2f}% - {downloaded} / {f_size_r}   ')
                c_current += 1
        if show_progress:
            sys.stdout.write('\n')
    return True


def sha512sum(filename):
    """
    Get SHA512 checksum of a file
    Return Type: str
    """
    sha512sum = hashlib.sha512()
    with open(filename, 'rb') as file:
        while True:
            data = file.read(BUFFER_SIZE)
            if not data:
                break
            sha512sum.update(data)
    return sha512sum.hexdigest()


def folder_size(folder):
    """
    Calculate the size of a folder in bytes
    Return Type: int
    """
    size = 0
    for root, dirs, files in os.walk(folder, onerror=None):
        for file in files:
            size += os.path.getsize(os.path.join(root, file))
    return size
