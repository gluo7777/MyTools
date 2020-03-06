import cli.scripts.google.commands as parent
import cli.scripts.google.tasks.commands as tasks

parent.commands.add_command(tasks.commands)