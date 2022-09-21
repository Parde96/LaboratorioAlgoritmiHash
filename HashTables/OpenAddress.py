class OpenAddress:

    def __init__(self, num_cells):
        self.collision = 0
        self.num_cells = num_cells
        self.cells = []
        for i in range(num_cells):
            self.cells.append(None)

    def hash(self, index, key):
        return ((key % self.num_cells) + index) % self.num_cells

    def insert(self, key):
        i = 0
        while True:
            j = self.hash(i, key)
            if self.cells[j] is None or self.cells[j] == "DEL":
                self.cells[j] = key
                return j
            else:
                i += 1
                self.collision += 1
            if i == self.num_cells:
                break
        return "Error"

    def search(self, key):
        i = 0
        while True:
            j = self.hash(i, key)
            if self.cells[j] == key:
                return j
            i += 1
            if i == self.num_cells or self.cells[j] is None:
                break
        return None

    def delete(self, key):
        index = self.search(key)
        if index is not None:
            self.cells[index] = "DEL"

    def print(self):
        for i in self.cells:
            if i is not None:
                print(i)
