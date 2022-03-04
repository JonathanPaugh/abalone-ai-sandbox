class Move:
    def __init__(self, selection, direction):
        self.selection = selection
        self.direction = direction

    def __str__(self):
        string = F"{self.direction}, {self.selection}"
        return string
