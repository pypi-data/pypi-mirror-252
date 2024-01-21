from .functions import Functions
from .user import User

class Typergame:

    def __init__(self, projectname: str, commands: list, defaultdelay: int = 0.02, defaultnewline: bool = True):
        """Initialization of module, set as variable game https://typergame.replit.app/docs?typergame.Typergame()"""
        self.functions = Functions(defaultdelay, defaultnewline)
        self.user = User(projectname, commands, defaultdelay, defaultnewline)

