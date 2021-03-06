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