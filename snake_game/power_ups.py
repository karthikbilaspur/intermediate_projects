import pygame
import random

class PowerUp:
    def __init__(self, window_width=720, window_height=480, power_up_color=(255, 255, 0), power_up_size=20):
        """
        Initialize PowerUp object.

        Args:
        window_width (int): Window width.
        window_height (int): Window height.
        power_up_color (tuple): Power-up color (RGB).
        power_up_size (int): Power-up size.
        """
        self.window_width = window_width
        self.window_height = window_height
        self.power_up_color = power_up_color
        self.power_up_size = power_up_size
        self.positions = self.generate_positions()

    def generate_positions(self):
        """
        Generate random power-up positions.

        Returns:
        list: List of power-up positions.
        """
        positions = []
        for _ in range(3):
            x = random.randint(0, self.window_width - self.power_up_size) // self.power_up_size * self.power_up_size
            y = random.randint(0, self.window_height - self.power_up_size) // self.power_up_size * self.power_up_size
            positions.append([x, y])
        return positions

    def draw(self, window):
        """
        Draw power-ups on window.

        Args:
        window: Pygame window object.
        """
        for position in self.positions:
            pygame.draw.rect(window, self.power_up_color, pygame.Rect(position[0], position[1], self.power_up_size, self.power_up_size))