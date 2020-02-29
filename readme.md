# MyTools Local Automation

A command line utility that accomplishes various things

[repo](https://github.com/gluo7777/mytools)

## Current Functionalities

- GitHub `mytool github`
    1. create, delete, and list repositories for authenticated user
- Diagnostics `mytool info`
    1. print information about system such as OS

## Development

1. Version > Python 3.8.1
2. Create setup.py if missing
3. Initialize virtualenv
    > virtualenv env
    > ./venv/Scripts/activate
4. Create script executables
    > pip install --editable .