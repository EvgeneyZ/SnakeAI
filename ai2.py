class AI:

    def __init__(self, board_width, board_height):
        self.board_width = board_width
        self.board_height = board_height
        self.path = []

        self.direction = (1, 0)
        self.mode = 'None'

    def input(self, blocks : list[tuple[int]], apple : list[tuple[int]]):
        

        if self.mode == 'apple' and len(self.path) > 0:
            self.direction = (self.path[-1][0] - blocks[0][0], self.path[-1][1] - blocks[0][1])
            self.path.pop(-1)
            return

        self.path = []
        if self.find_shortest_path(blocks[:-1], blocks[0], blocks[-1], apple, []):
            self.direction = (self.path[-1][0] - blocks[0][0], self.path[-1][1] - blocks[0][1])
            self.mode = 'apple'
            self.path.pop(-1)
        else:
            self.path = []
            if self.find_shortest_path(blocks[:-1], blocks[0], blocks[-1], blocks[-1], [], to_tail=True):
                self.direction = (self.path[-1][0] - blocks[0][0], self.path[-1][1] - blocks[0][1])

    def output(self):
        return self.direction

    def find_shortest_path(self, blocks, start, tail, target, exhausted = [], to_tail=False):
        neighbors = self.get_neighbors(start)
        for neighbor in neighbors[:]:
            if neighbor in blocks or neighbor in exhausted:
                neighbors.remove(neighbor)

        if len(neighbors) == 0:
            return False

        if target in neighbors:
            tmp_blocks = blocks[:]
            tmp_blocks.insert(0, target)
            if len(blocks) <= 6 or to_tail or self.check_space(tmp_blocks, target, [tail], []):
                self.path.insert(0, target)
                return True

        neighbors = sorted(neighbors, key=lambda x: AI.get_distance(x, target, 'manhatten'), reverse=to_tail)

        for neighbor in neighbors:
            exhausted.append(neighbor)
            tmp_blocks = blocks[:-1]
            tmp_blocks.insert(0, neighbor)
            
            if len(blocks) >= 6 and not to_tail and not self.check_space(tmp_blocks, neighbor, [blocks[-1]], []):
                exhausted.remove(neighbor)
                continue

            new_tail = neighbor
            if len(blocks) > 0:
                new_tail = blocks[-1]
            if self.find_shortest_path(tmp_blocks, neighbor, new_tail, target, exhausted, to_tail=to_tail):
                self.path.append(neighbor)
                return True

        return False

    def check_space(self, blocks, start, targets, exhausted = []):
        neighbors = self.get_neighbors(start)

        for neighbor in neighbors[:]:
            if neighbor in blocks or neighbor in exhausted:
                neighbors.remove(neighbor)

        if len(neighbors) == 0:
            return False

        for target in targets:
            if target in neighbors:
                return True

        neighbors = sorted(neighbors, key=lambda x: AI.get_distance(x, targets[-1], 'manhatten'), reverse=True)


        for neighbor in neighbors:
            exhausted.append(neighbor)
            tmp_blocks = blocks[:-1]
            tmp_blocks.insert(0, neighbor)
            tmp_targets = targets[:]
            tmp_targets.append(tmp_blocks[-1])
            if self.check_space(tmp_blocks, neighbor, tmp_targets, exhausted):
                return True

        return False


    def get_neighbors(self, cell):
        neighbors = []

        if cell[0] > 0:
            neighbors.append((cell[0] - 1, cell[1]))

        if cell[1] > 0:
            neighbors.append((cell[0], cell[1] - 1))

        if cell[0] < self.board_width - 1:
            neighbors.append((cell[0] + 1, cell[1]))

        if cell[1] < self.board_height - 1:
            neighbors.append((cell[0], cell[1] + 1))

        return neighbors


    @staticmethod
    def get_distance(cell1, cell2, mode='real'):
        if mode == 'real':
            return (cell1[0] - cell2[0]) ** 2 + (cell1[1] - cell2[1]) ** 2
        else:
            return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])
