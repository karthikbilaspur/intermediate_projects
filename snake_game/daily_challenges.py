import pygame

class DailyChallenge:
    def __init__(self, font_size=24, font_color=(255, 255, 255)):
        """
        Initialize DailyChallenge object.

        Args:
        font_size (int): Font size for challenge text.
        font_color (tuple): Font color (RGB).
        """
        self.font_size = font_size
        self.font_color = font_color
        self.challenges = {
            "Score": {"target": 100, "progress": 0},
            "Length": {"target": 10, "progress": 0},
            "Time": {"target": 60, "progress": 0}  # seconds
        }
        self.font = pygame.font.SysFont("Arial", self.font_size)

    def update(self, score, length, time):
        """
        Update daily challenges.

        Args:
        score (int): Current score.
        length (int): Current length.
        time (int): Elapsed time (seconds).
        """
        self.challenges["Score"]["progress"] = score
        self.challenges["Length"]["progress"] = length
        self.challenges["Time"]["progress"] = time

    def draw(self, window):
        """
        Draw daily challenges on window.

        Args:
        window: Pygame window object.
        """
        y = 10
        for challenge, values in self.challenges.items():
            text = f"{challenge}: {values['progress']}/{values['target']}"
            text_surface = self.font.render(text, True, self.font_color)
            window.blit(text_surface, (10, y))
            y += self.font_size + 5