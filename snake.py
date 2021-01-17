from settings import Settings


s = Settings()

class Snake:

    def __init__(self):
        self.body = [(0, 0)]
        self.direction = (1, 0)
        self.dead = False

    def move(self):
        self.body.insert(0, (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1]))
        head = self.body[0]
        if head == self.apple.position:
            self.apple.randomize()
        else:
            self.body.pop(-1)

        if head in self.body[1:]:
            self.dead = True
        elif head[0] < 0 or head[0] >= s.screen_width or head[1] < 0 or head[1] >= s.screen_height:
            self.dead = True

    def __bool__(self):
        if self.dead:
            return False
        return True

    def __len__(self):
        return len(self.body) 

