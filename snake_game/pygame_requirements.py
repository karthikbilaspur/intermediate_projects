import pygame
import sys

def init_pygame(window_width=720, window_height=480, title="Pygame Window"):
    """
    Initialize Pygame.

    Args:
    window_width (int): Window width.
    window_height (int): Window height.
    title (str): Window title.
    """
    pygame.init()
    pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption(title)

def quit_pygame():
    """
    Quit Pygame.
    """
    pygame.quit()
    sys.exit()