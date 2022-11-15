import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.speed = speed
        self.width = life.rows * cell_size
        self.height = life.cols * cell_size
        self.cell_size = cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw_lines(self) -> None:
        # Copy from previous assignment
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        # Copy from previous assignment
        for x in range(self.life.rows):
            for y in range(self.life.cols):
                pygame.draw.rect(
                    self.screen,
                    pygame.Color("green")
                    if self.life.curr_generation[x][y] == 1
                    else pygame.Color("white"),
                    (
                        y * self.cell_size,
                        x * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    ),
                )

    def cell_edit(self, x, y) -> None:
        row = y // self.cell_size
        col = x // self.cell_size
        if self.life.curr_generation[row][col]:
            self.life.curr_generation[row][col] = 0
        else:
            1

    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pause = not pause
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    self.cell_edit(x, y)
                    self.draw_grid()
                    self.draw_lines()
                    pygame.display.flip()

            if not pause:
                self.life.step()
                self.draw_grid()
                self.draw_lines()
                pygame.display.flip()
            clock.tick(self.speed)


if __name__ == "__main__":
    game = GameOfLife(size=(20, 20), randomize=True)
    gui = GUI(life=game, cell_size=20)
    gui.run()