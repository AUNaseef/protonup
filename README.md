## Introduction
ProtonUp-ng: CLI program and API to automate the installation and update of [GloriousEggroll](https://github.com/GloriousEggroll/)'s [Proton-GE](https://github.com/GloriousEggroll/proton-ge-custom)

Note: This is a fork of AUNaseef's awesome ProtonUp. I will maintain this fork until he pulls all needed changes for the new versioning scheme of GE-Proton into his codebase.

[![Downloads](https://pepy.tech/badge/protonup-ng)](https://pepy.tech/project/protonup-ng)

## Installation
Install from Python Package Index
```
pip3 install protonup-ng
```
Install from source
```
git clone https://github.com/cloudishBenne/protonup-ng && cd protonup-ng
python3 setup.py install --user
```
Install a snapshot of the repo
```
pip3 install https://github.com/cloudishBenne/protonup-ng/archive/main.zip
# or any other branch, tag, commit
# pip3 install https://github.com/cloudishBenne/protonup-ng/archive/[branch, tag, commit-hash].zip
```
If you get a `command not found` error, add the following to your `~/.profile` (if it's not already present) and run `source ~/.profile`
```
if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
fi
```

## Usage
### Note: The package itself is now called protonup-ng, but usage on the terminal is still protonup to not breaking scripts.
Set your installation directory before running the program with `-d "your/compatibilitytools.d/directory"`

Example:
```
protonup -d "~/.steam/root/compatibilitytools.d/"
```
---
To update to the latest version, just run `protonup` from a command line

Example:
```
protonup
```
---
List available versions with `--releases`

Example:
```
protonup --releases
```
---
Install a specific version with `-t "version tag"`

Example:
```
protonup -t 6.5-GE-2
```
or with the new naming scheme:
```
protonup -t GE-Proton7-10
```
---
By default the downloads are stored in a temporary folder. Change it with `-o "custom/download/directory"`

Example:
```
protonup -o ~/Downloads
```
---
List existing installations with `-l`

Example:
```
protonup -l
```
---
Remove existing installations with `-r "version tag`

Example:
```
protonup -r 6.5-GE-2
```
or with the new naming scheme:
```
protonup -r GE-Proton7-10
```
---
Use `--download` to download  Proton-GE to the current working directory without installing it, you can override destination with `-o`

Example:
```
protonup --download
```
---
Use `-y` toggle to carry out actions without any logging or interaction

Example:
```
protonup --download -o ~/Downloads -y
```
---
### Restart Steam after making changes
