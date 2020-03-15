# MyTools Local Automation

A command line utility that accomplishes various things

[repo](https://github.com/gluo7777/mytools)

## Current Functionalities

- GitHub `mytool github`
    1. create, delete, and list repositories for authenticated user
- Diagnostics `mytool info`
    1. print information about system such as OS

## Upgrade Python

### Windows 10

https://stackoverflow.com/questions/45137395/how-do-i-upgrade-the-python-installation-in-windows-10

```powershell
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
refreshenv
choco upgrade python -y
py -m pip install --upgrade pip
alias pip="py -m pip"
```

## Development

1. Version > Python 3.8.1
2. Create setup.py if missing
3. Initialize virtualenv
    > virtualenv venv
    > ./venv/Scripts/activate
4. Create script executables
    > pip install --editable .

## Packaging

1. (If venv is activated) `deactivate`
1. `python -m pip install --upgrade pip`
1. `python -m pip install --user --upgrade setuptools wheel`
1. (If generated python packages and wheel) `python setup.py sdist bdist_wheel`
1. (If uploaded to pypi) Create account at `https://test.pypi.org/` and generate API master token
1. Install twine for uploading to PYPI `python3 -m pip install --user --upgrade twine`
1. Set up `$HOME/.pypirc`
1. Upload with twine `python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*`

## Built Distribution

[Official Documentation](https://docs.python.org/3/distutils/builtdist.html)

1. (Local) `python setup.py install`

1. Generate built distributions for tar,zip,msi extensions which should cover all 3 major platforms
> python setup.py bdist --format=zip,gztar,wininst