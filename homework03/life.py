import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        return [
            [random.randint(0, 1) if randomize else 0 for _ in range(self.rows)]
            for _ in range(self.cols)
        ]

    def get_neighbours(self, cell: Cell) -> Cells:
        m = []
        for i, j in (
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ):
            if cell[0] + i >= 0 and cell[1] + j >= 0:
                try:
                    m.append(self.curr_generation[cell[0] + i][cell[1] + j])
                except IndexError:
                    pass
        return m

    def get_next_generation(self) -> Grid:
        grid = [[0] * len(self.curr_generation[0]) for _ in range(len(self.curr_generation))]
        for i in range(len(self.curr_generation)):
            for j in range(len(self.curr_generation[0])):
                n = self.get_neighbours((i, j)).count(1)
                if self.curr_generation[i][j] and n == 2 or n == 3:
                    grid[i][j] = 1
        return grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is None:
            return False
        return int(self.generations) <= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path):
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename) as f:
            return [[int(j) for j in i] for i in f]

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as f:
            for i in self.curr_generation:
                print(i, sep="", file=f)