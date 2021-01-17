class Settings:
    def __init__(self):

        #You can modify these values!
        self.screen_width = 16      #width of the board
        self.screen_height = 9      #height of the board
        self.cell_size = 80         #size if a single square
        self.FPS = 30               #speed of the game

        #Colors
        self.bg_color = (20, 0, 50)
        self.line_color = (200, 200, 255)
        self.snake_color = (255, 255, 255)
        self.apple_color = (255, 0, 0)
        self.head_color = (124, 252, 0)
        self.tail_color = (135, 206, 250)


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
