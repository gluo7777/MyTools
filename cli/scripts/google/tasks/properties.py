from cli.scripts.google.properties import GoogleProperties

class TaskProperties(GoogleProperties):
    PREFIX = "tasks"
    def __init__(self):
        super().__init__()