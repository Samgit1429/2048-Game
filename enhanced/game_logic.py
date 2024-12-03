import random
from tile import Tile
from grid import draw
from constants import ROWS, COLS, MOVE_VEL, RECT_WIDTH, RECT_HEIGHT, FPS


def get_random_pos(tiles):
    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLS)
        if f"{row}{col}" not in tiles:
            return row, col


def generate_tiles():
    tiles = {}
    for _ in range(2):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)
    return tiles


def update_tiles(tiles, sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile


def move_tiles(window, tiles, clock, direction):
    updated = True
    blocks = set()  # Tracks merged tiles

    # Define direction-specific behaviors
    if direction == "left":
        sort_func = lambda x: x.col
        reverse = False
        delta = (-MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL
        )
        ceil = True
    elif direction == "right":
        sort_func = lambda x: x.col
        reverse = True
        delta = (MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == COLS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x
        )
        ceil = False
    elif direction == "up":
        sort_func = lambda x: x.row
        reverse = False
        delta = (0, -MOVE_VEL)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL
        )
        ceil = True
    elif direction == "down":
        sort_func = lambda x: x.row
        reverse = True
        delta = (0, MOVE_VEL)
        boundary_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VEL < next_tile.y
        )
        ceil = False

    # Movement loop
    while updated:
        clock.tick(FPS)
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

        for i, tile in enumerate(sorted_tiles):
            if boundary_check(tile):  # Skip if at boundary
                continue

            next_tile = get_next_tile(tile)
            if not next_tile:  # If no tile, move freely
                tile.move(delta)
            elif (
                tile.value == next_tile.value
                and tile not in blocks
                and next_tile not in blocks
            ):  # If tiles can merge
                if merge_check(tile, next_tile):
                    tile.move(delta)
                else:
                    next_tile.value *= 2
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
            elif move_check(tile, next_tile):  # If can move closer
                tile.move(delta)
            else:
                continue

            tile.set_pos(ceil)  # Update tile's position
            updated = True

        update_tiles(tiles, sorted_tiles)  # Update tile positions on the board
        draw(window, tiles)  # Re-draw board after every move

    # Check if a new tile can be added
    return end_move(tiles)

def end_move(tiles):
    from game_logic import get_random_pos  # Avoid circular import
    if len(tiles) == ROWS * COLS:  # If board is full, check game over
        return "lost"

    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    return "continue"
