class Room:
    def __init__(self, name, description, exits, items=None, log=None, glitch=False):
        self.name = name
        self.description = description
        self.exits = exits  # dict: {'norte': 'Sala 2'}
        self.items = items if items else []
        self.log = log
        self.glitch = glitch
