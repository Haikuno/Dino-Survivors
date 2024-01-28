class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, "rt") as f:
            for line in f:
                self.data.append(line)
