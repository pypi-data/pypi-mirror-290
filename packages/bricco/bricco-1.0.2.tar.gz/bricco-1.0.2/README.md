# python3-bricco

## Description

Bricco is a simple Tor bridges testing tool.
It can find Tor bridges in some text data (for now **obfs4** and **vanilla**) and perform fast port scanning to check bridge availability.

## Installation

The script is pure Python and a part of [PyPI](https://pypi.org/project/bricco), so can be installed via *pip*:

```bash
python3 -m pip install bricco
```

## Usage

Bridges test:

```bash
bricco test -i ${untested_bridges_txt} -o ${available_bridges_txt}
```

Set smaller socket timeout to make things faster:

```bash
# 2 sec instead of 5
bricco test -i ${untested_bridges_txt} -o ${available_bridges_txt} -t 2
```

Also, it is possible to use external [Nmap](https://nmap.org/) executable.
Presumably, it is more accurate than using native Python3 `socket` module:

```bash
# Debian: sudo apt install nmap
bricco test -i ${untested_bridges_txt} -o ${available_bridges_txt} -n /usr/bin/nmap
# Windows:
bricco test -i ${untested_bridges_txt} -o ${available_bridges_txt} -n C:/downloads/nmap.exe
```

## Bugs

If you want to report a bug or propose a feature, feel free to [open an issue](https://codeberg.org/screwery/bricco/issues).
