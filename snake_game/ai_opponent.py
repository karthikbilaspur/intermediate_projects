import pygame
import random

class AiOpponent:
    def __init__(self, window_width=720, window_height=480, opponent_color=(0, 0, 255), opponent_size=20):
        """
        Initialize AiOpponent object.

        Args:
        window_width (int): Window width.
        window_height (int): Window height.
        opponent_color (tuple): Opponent color (RGB).
        opponent_size (int): Opponent segment size.
        """
        self.window_width = window_width
        self.window_height = window_height
        self.opponent_color = opponent_color
        self.opponent_size = opponent_size
        self.position = [random.randint(0, window_width - opponent_size) // opponent_size * opponent_size,
                         random.randint(0, window_height - opponent_size) // opponent_size * opponent_size]
        self.body = [self.position]
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

    def move(self):
        """
        Update AI opponent position based on direction.
        """
        head = self.body[-1]
        if self.direction == "RIGHT":
            new_head = [head[0] + self.opponent_size, head[1]]
        elif self.direction == "LEFT":
            new_head = [head[0] - self.opponent_size, head[1]]
        elif self.direction == "UP":
            new_head = [head[0], head[1] - self.opponent_size]
        elif self.direction == "DOWN":
            new_head = [head[0], head[1] + self.opponent_size]

        self.body.append(new_head)
        self.body.pop(0)

        # Random direction change
        if random.random() < 0.1:
            self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

    def draw(self, window):
        """
        Draw AI opponent on window.

        Args:
        window: Pygame window object.
        """
        for pos in self.body:
            pygame.draw.rect(window, self.opponent_color, pygame.Rect(pos[0], pos[1], self.opponent_size, self.opponent_size))