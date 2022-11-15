import curses
from dataclasses import replace

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)
        self.game = life

    def draw_borders(self, screen) -> None:
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        for i in range(0, len(self.game.curr_generation)):
            screen.addstr(
                i + 1,
                1,
                "".join(map(str, self.game.curr_generation[i])).replace("0", " ").replace("1", "*"),
            )
        screen.refresh()
        screen.getch()
        self.game.step()

    def run(self) -> None:
        screen = curses.initscr()
        self.draw_borders(screen)
        self.game.create_grid(randomize=True)
        while True:
            self.draw_grid(screen)


life = GameOfLife((80, 30), max_generations=1000)
ui = Console(life)
ui.run()