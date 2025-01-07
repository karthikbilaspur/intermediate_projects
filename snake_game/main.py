import pygame
import sys
from game import SnakeGame

def main():
    pygame.init()
    game = SnakeGame()
    game.play()

if __name__ == "__main__":
    main()