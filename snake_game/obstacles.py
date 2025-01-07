import pygame
import random

class Obstacle:
    def __init__(self, window_width=720, window_height=480, obstacle_color=(128, 128, 128), obstacle_size=20):
        """
        Initialize Obstacle object.

        Args:
        window_width (int): Window width.
        window_height (int): Window height.
        obstacle_color (tuple): Obstacle color (RGB).
        obstacle_size (int): Obstacle size.
        """
        self.window_width = window_width
        self.window_height = window_height
        self.obstacle_color = obstacle_color
        self.obstacle_size = obstacle_size
        self.positions = self.generate_positions()

    def generate_positions(self):
        """
        Generate random obstacle positions.

        Returns:
        list: List of obstacle positions.
        """
        positions = []
        for _ in range(5):
            x = random.randint(0, self.window_width - self.obstacle_size) // self.obstacle_size * self.obstacle_size
            y = random.randint(0, self.window_height - self.obstacle_size) // self.obstacle_size * self.obstacle_size
            positions.append([x, y])
        return positions

    def draw(self, window):
        """
        Draw obstacles on window.

        Args:
        window: Pygame window object.
        """
        for position in self.positions:
            pygame.draw.rect(window, self.obstacle_color, pygame.Rect(position[0], position[1], self.obstacle_size, self.obstacle_size))