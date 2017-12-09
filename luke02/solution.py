#!/usr/bin/env python3
import curses
from enum import Flag, auto
from time import sleep

class CellState(Flag):
    OPEN = auto()
    REACHABLE = auto()
    VISITED = auto()

def calc_cell_is_open(x, y):
    result = (x**3) + (12*x*y) + (5*x*(y**2))
    antall_enere = bin(result).count('1')
    return antall_enere % 2 == 0

def generate_grid(rows, columns):
    grid = []
    for row in range(rows):
        grid.append([CellState.OPEN if calc_cell_is_open(column+1, row+1) else CellState(0) for column in range(columns)])
    return grid

def draw_grid(grid, pad):
    pad.clear()
    unreached = 0
    for row_idx, row in enumerate(grid):
        for column_idx, cell in enumerate(row):
            if CellState.OPEN in cell:
                char = '_'
                attr = 0
                if CellState.VISITED in cell:
                    attr = curses.color_pair(2)
                elif CellState.REACHABLE in cell:
                    attr = curses.color_pair(1)
                else:
                    unreached += 1
            else:
                char = '#'
                attr = 0
            pad.addstr(row_idx+2, column_idx, char, attr)
    pad.addstr(0,2,str(unreached))
    pad.refresh(0,0, 0,0, curses.LINES-4, curses.COLS-4)

def get_reachable_neighbours(grid, cell):
    (y, x) = cell
    neighbour_directions = [(1,0),(0,1),(-1,0),(0,-1)]
    possible_neighbours = [tuple(map(sum, zip(cell,x))) for x in neighbour_directions]
    reachable_neighbours = []
    for (y, x) in possible_neighbours:
        if y < 0 or x < 0: continue
        try:
            if CellState.OPEN in grid[y][x] and CellState.VISITED not in grid[y][x]:
                reachable_neighbours.append((y, x))
        except Exception as e:
            # Out of bounds
            continue
    return reachable_neighbours

def navigate(grid, stack):
    current_cell = stack.pop()
    (y, x) = current_cell
    grid[y][x] |= CellState.VISITED
    reachable_cells = get_reachable_neighbours(grid, current_cell)
    stack.update(reachable_cells)
    for (y, x) in reachable_cells:
        grid[y][x] |= CellState.REACHABLE

def main(stdscr, rows, columns):
    grid = generate_grid(rows, columns)
    stack = set()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_CYAN)
    assert curses.can_change_color(), 'No colors'
    pad = curses.newpad(rows+2, columns+2)
    pad.nodelay(True)
    draw_grid(grid, pad)
    # Set starting point
    grid[0][0] |= CellState.REACHABLE
    stack.add((0, 0))
    while len(stack):
        c = pad.getch()
        if c == ord('q'):
            break
        navigate(grid, stack)
        draw_grid(grid, pad)
        sleep(0.1)
    pad.nodelay(False)
    pad.getch()

curses.wrapper(main, 20, 20)

