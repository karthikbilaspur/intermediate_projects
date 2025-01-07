import pygame

class Achievement:
    def __init__(self, font_size=24, font_color=(255, 255, 255)):
        """
        Initialize Achievement object.

        Args:
        font_size (int): Font size for achievement text.
        font_color (tuple): Font color (RGB).
        """
        self.font_size = font_size
        self.font_color = font_color
        self.achievements = {
            "Novice": {"score": 50, "unlocked": False},
            "Intermediate": {"score": 200, "unlocked": False},
            "Expert": {"score": 500, "unlocked": False}
        }
        self.font = pygame.font.SysFont("Arial", self.font_size)

    def update(self, score):
        """
        Update achievements based on score.

        Args:
        score (int): Current score.
        """
        for achievement, values in self.achievements.items():
            if score >= values["score"] and not values["unlocked"]:
                values["unlocked"] = True
                print(f"Achievement unlocked: {achievement}")

    def draw(self, window):
        """
        Draw achievements on window.

        Args:
        window: Pygame window object.
        """
        y = 10
        for achievement, values in self.achievements.items():
            text = f"{achievement}: {values['score']} ({'Unlocked' if values['unlocked'] else 'Locked'})"
            text_surface = self.font.render(text, True, self.font_color)
            window.blit(text_surface, (10, y))
            y += self.font_size + 5