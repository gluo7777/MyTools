# MyTools Local Automation

A command line utility that accomplishes various things

[repo](https://github.com/gluo7777/mytools)

## Current Functionalities

- GitHub `mytool github`
    1. create, delete, and list repositories for authenticated user
- Diagnostics `mytool info`
    1. print information about system such as OS

## Development

### Upgrade python

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.9
sudo apt install python3.9-distutils
python3.9 -m pip install --upgrade pip
sudo apt-get install python3.9-venv
python3.9 -m pip --version
python3.9 -m venv -h
```

### Set up venv

```bash
python3.9 -m venv .venv
source .venv/bin/activate
## python automatically points to python3.9 now
python --version
which python
```

### Install dev dependencies

```bash
python -m pip install -r requirements.txt
```

### Running as script

```bash
python -m cli.scripts.main
# Do not run python cli/scripts/main.py as python's module resolution will not work
```

### Testing

```bash
python -m unittest
```

### Linting

```bash
> pylint --disable=all --enable=F,unreachable,duplicate-key,unnecessary-semicolon,global-variable-not-assigned,unused-variable,unused-wildcard-import,binary-op-exception,bad-format-string,anomalous-backslash-in-string,bad-open-mode,E0001,E0011,E0012,E0100,E0101,E0102,E0103,E0104,E0105,E0107,E0108,E0110,E0111,E0112,E0113,E0114,E0115,E0116,E0117,E0118,E0202,E0203,E0211,E0213,E0236,E0237,E0238,E0239,E0240,E0241,E0301,E0302,E0303,E0401,E0402,E0601,E0602,E0603,E0604,E0611,E0632,E0633,E0701,E0702,E0703,E0704,E0710,E0711,E0712,E1003,E1101,E1102,E1111,E1120,E1121,E1123,E1124,E1125,E1126,E1127,E1128,E1129,E1130,E1131,E1132,E1133,E1134,E1135,E1136,E1137,E1138,E1139,E1200,E1201,E1205,E1206,E1300,E1301,E1302,E1303,E1304,E1305,E1306,E1310,E1700,E1701 --msg-template='{line},{column},{category},{symbol}:{msg}' --reports=n --output-format=text cli

```

### Building sdist and wheel

```bash
python -m pip install --upgrade build
python -m build
```

### Distribution

### Installation

```bash
# Install wheel file directly
python -m pip install path/to/file.whl
```

## Files

- `requirements.txt`: required (concrete) dependencies for development or installation from source
- `setup.cfg`: project metadata
    - `install_requires`: required (abstract) dependencies for usage as a python module
- `constraints.txt`: similar to requirements.txt but only specifies constraints (typically for transitive dependencies)
- `pyproject.toml`: specifies dependencies that are used during the building of the source code but not required afterwards