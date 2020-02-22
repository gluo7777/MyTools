from configparser import ConfigParser, ExtendedInterpolation
import os
import click
from pathlib import Path

# init parser settings
file_parser = ConfigParser(allow_no_value=True,
    comment_prefixes='#',
    strict=True,
    empty_lines_in_values=False,
    interpolation=ExtendedInterpolation())

# create new file
# add sections
# create file
config_file = os.getcwd() + '/config.ini'
if not os.path.exists(config_file):
    click.echo(f"Creating configuration file at {config_file}")
    # os.makedirs(config_file, exist_ok=True)
    open(config_file, 'a').close()
    click.echo("Run mytool setup afterwards to manually enter values")
    file_parser.add_section("GitHub")
    file_parser.set("GitHub","accesstoken","abcd")
    file_parser.add_section("Diagnostics")
    file_parser.set("Diagnostics","verbose","false")
    file_parser.write(open(config_file, mode='w'))

file_parser.read(config_file)
for section in file_parser.sections():
    for item in file_parser.items(section):
        print(f'{item[0]}={item[1]}')