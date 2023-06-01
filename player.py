class Player:
    def __init__(self):
        self.name = ''
        self.score = 0

    def return_data(self):
        return tuple([self.name, self.score])
