import settings


class Beacon:
    def __init__(self, x, y, id):
        super(Beacon, self).__init__()
        self.x = x
        self.y = y
        self.id = id
        self.distance = 100000