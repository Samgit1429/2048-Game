import pygame

from constants import (
    WIDTH,
    HEIGHT,
    ROWS,
    COLS,
    RECT_HEIGHT,
    RECT_WIDTH,
    OUTLINE_COLOR,
    OUTLINE_THICKNESS,
    BACKGROUND_COLOR,
    FONT,
    FONT_COLOR,
    SCORE,
)


def draw_grid(window):
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    for col in range(1, COLS):
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)

    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)


def draw(window, tiles):
    window.fill(BACKGROUND_COLOR)  # Clear the window before drawing

    for tile in tiles.values():
        tile.draw(window)

    draw_grid(window)

    # Display the score
    score_text = FONT.render(f"Score: {SCORE}", 1, FONT_COLOR)
    window.blit(score_text, (10, 10))  # Adjust position as needed

    pygame.display.flip()  # Update the entire display
