import random
from settings import Settings

s = Settings()

class AI:

    def __init__(self):
        self.width = s.screen_width
        self.height = s.screen_height
        self.path = []
        self.mode = "Apple"
        self.counter = 0
        self.max_counter = 10

    def pass_through(self, blocks, apple):
        
        head = blocks[0]
        snake_len = len(blocks)

        if len(self.path) < 2 or self.mode == "Tail":
            neighbors = s.get_neighbors(head)
            for neighbor in neighbors[:]:
                if neighbor in blocks[:-1]:
                    neighbors.remove(neighbor)
            if len(neighbors) == 1:
                self.path = [head, neighbors[0]]
                return
        if len(self.path) < 2 or self.mode == "Tail":
            self.path = self.get_shortest_path(head, apple, blocks, snake_len, tail=False, longest=False)
        if len(self.path) < 2:
            self.path = self.get_shortest_path(head, blocks[-1], blocks, snake_len, tail=True, longest=True)
            self.mode = "Tail"
        else:
            self.mode = "Apple"

        if len(self.path) < 2:
            self.path = self.get_safe_direction(blocks[:])

    def get_safe_direction(self, blocks):
        head = blocks[0]
        tail = blocks[-1]
        blocks = blocks[:len(blocks) - 1]

        neighbors = s.get_neighbors(head)
        for neighbor in neighbors[:]:
            if neighbor in blocks:
                neighbors.remove(neighbor)

        if len(neighbors) > 0:
            return [head, random.choice(neighbors)]

        return []

    def get_direction_from_points(self, cell1, cell2):
        return (cell2[0] - cell1[0], cell2[1] - cell1[1])


    def get_shortest_path(self, start, target, blocks, snake_len, tail=False, longest=False):
        path = []
        to_observe = [start]
        exhausted = []
        walls = blocks[:]
        if not tail:
            walls.pop(-1)
        walls = walls[::-1]
        offset = 0

        while to_observe:
            cur = to_observe.pop(-1)

            if path:
                while path[-1] not in s.get_neighbors(cur):
                    path.pop(-1)
                    walls.pop(-1)
                    offset -= 1

            path.append(cur)

            if cur == target:
                walls.append(cur)

                if tail or len(self.get_shortest_path(cur, walls[offset - 1], walls[::-1], snake_len, tail=True, longest=False)) >= 2:
                    return path
                else:
                    return []

            neighbors = s.get_neighbors(cur)

            for neighbor in neighbors[:]:
                if neighbor in exhausted or neighbor in walls[offset:]:
                    neighbors.remove(neighbor)

            if len(neighbors) != 0:
                _reversed = True
                if longest:
                    _reversed = False

                prev_path = None
                if len(path) >= 2:
                    prev_path = [path[-2], path[-1]]
                neighbors = sorted(neighbors, 
                        key=lambda x : self.sort_key(x, target, walls[offset:], _reversed, tail, snake_len, prev_path), 
                        reverse=_reversed)
                for neighbor in neighbors:
                    if neighbor in to_observe:
                        to_observe.remove(neighbor)
                    to_observe.append(neighbor)
            offset += 1
            exhausted.append(cur)
            walls.append(cur)

        return []

    def sort_key(self, x, target, blocks, reverse, tail, snake_len, prev=None):

        if not tail and snake_len < s.screen_width * s.screen_height / 3:
            return s.find_distance(x, target)

        neighbors = s.get_neighbors(x)
        for n in neighbors[:]:
            if n not in blocks:
                neighbors.remove(n)

        number = len(neighbors)

        if x[0] == 0 or x[0] == s.screen_width - 1:
            number += 1
        if x[1] == 0 or x[1] == s.screen_height - 1:
            number += 1
            
        mult = 1
        if prev != None:
            if x[0] - prev[1][0] == prev[1][0] - prev[0][0] and x[1] - prev[1][1] == prev[1][1] - prev[0][1]:
                mult = 2
        
        if snake_len > s.screen_width * s.screen_height * 7/10:
            mult = 1

        if reverse:
            return s.find_distance(x, target) / (mult * (1 + number))
        else:
            return s.find_distance(x, target) * (mult * (1 + number))
            

    def output(self):
        if len(self.path) >= 2:
            direction =  self.get_direction_from_points(self.path[0], self.path[1])
            self.path.pop(0)
            return direction
        return self.random_output()

    def random_output(self):
        return random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

