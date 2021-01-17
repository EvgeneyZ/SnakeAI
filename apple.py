from random import randint
from settings import Settings

s = Settings()

class Apple:

    def __init__(self, snake):
        self.snake = snake
        self.position = (0, 0)
        self.randomize()

    def randomize(self):

        if len(self.snake.body) == s.screen_width * s.screen_height:
            self.position = (-1, -1)
            return

        while self.position in self.snake.body:
            self.position = (randint(0, s.screen_width - 1), randint(0, s.screen_height - 1))
