import sys
import pygame

from settings import Settings
from snake import Snake
from apple import Apple

from ai import AI

s = Settings()


def draw_board(screen, snake, apple, path, myfont):

    #draw snake
    pygame.draw.rect(screen, s.head_color, (snake.body[0][0] * s.cell_size, snake.body[0][1] * s.cell_size, s.cell_size, s.cell_size))

    for block in snake.body[1:-1]:
        pygame.draw.rect(screen, s.snake_color, (block[0] * s.cell_size, block[1] * s.cell_size, s.cell_size, s.cell_size))

    if len(snake.body) > 1:
        pygame.draw.rect(screen, s.tail_color, 
                (snake.body[-1][0] * s.cell_size, snake.body[-1][1] * s.cell_size, s.cell_size, s.cell_size))
  
    #draw apple
    pygame.draw.rect(screen, s.apple_color, (apple.position[0] * s.cell_size, apple.position[1] * s.cell_size, s.cell_size, s.cell_size))


    #draw snake's path (debug only)
    for i in range(1, len(path)):
        xpr = path[i - 1][0]
        ypr = path[i - 1][1]
        x = path[i][0]
        y = path[i][1]

        xpr *= s.cell_size
        xpr += s.cell_size / 2

        ypr *= s.cell_size
        ypr += s.cell_size / 2

        x *= s.cell_size
        x += s.cell_size / 2

        y *= s.cell_size
        y += s.cell_size / 2
        #pygame.draw.line(screen, (255, 142, 32), (xpr, ypr), (x, y))

    #draw grid
    for x in range(0, s.screen_width + 1):
        pygame.draw.line(screen, s.line_color, (x * s.cell_size,0), (x * s.cell_size,s.screen_height * s.cell_size))
    for y in range(0, s.screen_height + 1):
        pygame.draw.line(screen, s.line_color, (0, y * s.cell_size), (s.screen_width * s.cell_size, y * s.cell_size))
  
    #draw score
    text_surface = myfont.render(str(len(snake.body) - 1) + "/" + str(s.screen_width * s.screen_height - 1), False, (100, 255, 0))
    screen.blit(text_surface, (0, 0))

    return screen

def pause():
    flag = True
    while (flag):
        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    flag = False


def run_game():
    pygame.init()
    pygame.font.init()
    w = s.screen_width * s.cell_size + 1
    h = s.screen_height * s.cell_size + 1
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Snake")

    myfont = pygame.font.SysFont('Arial', 40)

    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple(snake)
    snake.apple = apple
    ai = AI()


    while (True):

        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    snake.direction = (1, 0)
                elif event.key == pygame.K_UP:
                    snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN:
                    snake.direction = (0, 1)
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    pause()

        if not snake.dead:
            ai.pass_through(snake.body[:], apple.position[:])
            snake.direction = ai.output()
            snake.move()
        screen.fill(s.bg_color)
        screen = draw_board(screen, snake, apple, ai.path, myfont)
        pygame.display.flip()

        if (snake.dead):
            print("Snake lost, size: ", len(snake))
            apple.randomize()
            snake = Snake()
            apple.snake = snake
            snake.apple = apple
            ai = AI()
        elif len(snake.body) == s.screen_width * s.screen_height:
            print("Snake won! Size: ", len(snake))
            return

        fps = s.FPS
        if ai.mode == "Tail":
            fps *= 2
        clock.tick(fps)

while True:
    run_game()
