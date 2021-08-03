## Introduction
CLI program and API to automate the installation and update of [GloriousEggroll](https://github.com/GloriousEggroll/)'s [Proton-GE](https://github.com/GloriousEggroll/proton-ge-custom)

[![Downloads](https://pepy.tech/badge/protonup)](https://pepy.tech/project/protonup)

## Installation
Install from Python Package Index
```
pip3 install protonup
```
Install from source
```
git clone https://github.com/AUNaseef/protonup && cd protonup
python3 setup.py install --user
```
If you get a `command not found` error, add the following to your `~/.profile` (if it's not already present) and run `source ~/.profile`
```
if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
fi
```

## Usage
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
