import pygame

class Snake:
    def __init__(self, window_width=720, window_height=480, snake_color=(0, 255, 0), snake_size=20):
        """
        Initialize Snake object.

        Args:
        window_width (int): Window width.
        window_height (int): Window height.
        snake_color (tuple): Snake color (RGB).
        snake_size (int): Snake segment size.
        """
        self.window_width = window_width
        self.window_height = window_height
        self.snake_color = snake_color
        self.snake_size = snake_size
        self.position = [100, 50]
        self.body = [[100, 50], [90, 50], [80, 50]]
        self.direction = "RIGHT"

    def move(self):
        """
        Update snake position based on direction.
        """
        head = self.body[-1]
        if self.direction == "RIGHT":
            new_head = [head[0] + self.snake_size, head[1]]
        elif self.direction == "LEFT":
            new_head = [head[0] - self.snake_size, head[1]]
        elif self.direction == "UP":
            new_head = [head[0], head[1] - self.snake_size]
        elif self.direction == "DOWN":
            new_head = [head[0], head[1] + self.snake_size]

        self.body.append(new_head)
        self.body.pop(0)

    def draw(self, window):
        """
        Draw snake on window.

        Args:
        window: Pygame window object.
        """
        for pos in self.body:
            pygame.draw.rect(window, self.snake_color, pygame.Rect(pos[0], pos[1], self.snake_size, self.snake_size))