import pygame

from constants import WINDOW, FPS, SCORE
from game_logic import generate_tiles, move_tiles
from grid import draw


def main(window):
    clock = pygame.time.Clock()
    run = True
    tiles = generate_tiles()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if move_tiles(window, tiles, clock, "left") == "lost":
                        print("Game Over!")
                        run = False
                if event.key == pygame.K_RIGHT:
                    if move_tiles(window, tiles, clock, "right") == "lost":
                        print("Game Over!")
                        run = False
                if event.key == pygame.K_UP:
                    if move_tiles(window, tiles, clock, "up") == "lost":
                        print("Game Over!")
                        run = False
                if event.key == pygame.K_DOWN:
                    if move_tiles(window, tiles, clock, "down") == "lost":
                        print("Game Over!")
                        run = False

        draw(window, tiles)

    pygame.quit()


if __name__ == "__main__":
    main(WINDOW)
