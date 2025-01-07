import pygame

class Leaderboard:
    def __init__(self, font_size=24, font_color=(255, 255, 255), max_scores=10):
        """
        Initialize Leaderboard object.

        Args:
        font_size (int): Font size for leaderboard text.
        font_color (tuple): Font color (RGB).
        max_scores (int): Maximum scores to display.
        """
        self.font_size = font_size
        self.font_color = font_color
        self.max_scores = max_scores
        self.scores = []
        self.font = pygame.font.SysFont("Arial", self.font_size)

    def update(self, score):
        """
        Update leaderboard scores.

        Args:
        score (int): New score.
        """
        self.scores.append(score)
        self.scores.sort(reverse=True)
        self.scores = self.scores[:self.max_scores]

    def draw(self, window):
        """
        Draw leaderboard on window.

        Args:
        window: Pygame window object.
        """
        y = 10
        text_surface = self.font.render("Leaderboard:", True, self.font_color)
        window.blit(text_surface, (10, y))
        y += self.font_size + 10

        for i, score in enumerate(self.scores):
            text = f"{i+1}. {score}"
            text_surface = self.font.render(text, True, self.font_color)
            window.blit(text_surface, (10, y))
            y += self.font_size + 5