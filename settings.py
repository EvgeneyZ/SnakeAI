class Settings:
    def __init__(self):
        self.screen_width = 32
        self.screen_height = 18
        self.cell_size = 40

        self.bg_color = (20, 0, 50)
        self.line_color = (200, 200, 220)
        self.snake_color = (255, 255, 255)
        self.apple_color = (255, 0, 0)
        self.head_color = (124, 252, 0)
        self.tail_color = (135, 206, 250)

        self.FPS = 30

    def get_neighbors(self, cell):
        x = cell[0]
        y = cell[1]

        answers = []

        if x > 0:
            answers.append((x - 1, y))
        if x < self.screen_width - 1:
            answers.append((x + 1, y))
        if y > 0:
            answers.append((x, y - 1))
        if y < self.screen_height - 1:
            answers.append((x, y + 1))

        return answers

    def find_distance(self, cell1, cell2):
        return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])
