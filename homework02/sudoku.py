import pathlib
import random
import time
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    a = []
    for i in range(n):
        a.append(values[:n])
        values = values[n:]
    return a


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    a = []
    for i in grid:
        a.append(i[pos[1]])
    return a


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    x0 = (pos[0] // 3) * 3
    x1 = x0 + 3
    y0 = (pos[1] // 3) * 3
    y1 = y0 + 3
    a = []
    for i in grid[x0:x1]:
        a += i[y0:y1]
    return a


def find_empty_positions(
    grid: tp.List[tp.List[str]],
) -> tp.Optional[tp.Tuple[int, int]]:
    for index, row in enumerate(grid):
        if "." in row:
            return index, row.index(".")
    return None


all_values = {str(x) for x in range(1, 10)}


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    row = get_row(grid, pos)
    col = get_col(grid, pos)
    block_values = set(get_block(grid, pos))

    free_values = all_values - block_values
    possible_values = set()

    for value in free_values:
        if value in row or value in col:
            continue
        possible_values.add(value)

    return possible_values


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    def get_solution(
        inGrid: tp.List[tp.List[str]],
    ) -> tp.Optional[tp.List[tp.List[str]]]:
        empty_pos = find_empty_positions(inGrid)
        if empty_pos is None:
            return inGrid

        possible_values = find_possible_values(inGrid, empty_pos)
        if not possible_values:
            return None

        row_empty_pos, col_empty_pos = empty_pos
        for value in possible_values:
            inGrid[row_empty_pos][col_empty_pos] = value
            if get_solution(inGrid) is not None:
                return inGrid

            inGrid[row_empty_pos][col_empty_pos] = "."
        return None

    return get_solution(grid)


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """Если решение solution верно, то вернуть True, в противном случае False"""
    for row_index in range(9):
        for col_index in range(9):
            row_values = get_row(solution, (row_index, col_index))
            col_values = get_col(solution, (row_index, col_index))
            block_values = get_block(solution, (row_index, col_index))

            all_sets = set(row_values) and set(col_values) and set(block_values)

            is_solution = (
                len(row_values) == len(set(row_values)),
                len(col_values) == len(set(col_values)),
                len(block_values) == len(set(block_values)),
                not (all_sets - all_values),
            )

            if not all(is_solution):
                return False
    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов"""
    empty_sudoku = [["." for _ in range(9)] for _ in range(9)]
    if N == 0:
        return empty_sudoku

    sudoku = solve(grid=empty_sudoku)
    if sudoku is None:
        return empty_sudoku

    field_square_size = 9 * 9
    if N > field_square_size:
        return sudoku

    free_position_count = field_square_size - N
    while free_position_count != 0:
        row_index_position, col_index_position = (
            random.randint(0, 8),
            random.randint(0, 8),
        )

        if sudoku[row_index_position][col_index_position] == ".":
            continue

        sudoku[row_index_position][col_index_position] = "."
        free_position_count -= 1

    return sudoku


def run_solve(puzzle: tp.List[tp.List[str]]) -> None:
    start = time.time()
    solution = solve(puzzle)
    end = time.time()
    if solution is not None:
        print(f"{end-start}")
        display(solution)
    else:
        print(f"Puzzle {puzzle} can't be solved")


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
