import pygame
from snake import Snake
from ai_opponent import AiOpponent
from obstacles import Obstacle
from power_ups import PowerUp
from leaderboards import Leaderboard
from unlockables import Unlockable
from achievements import Achievement
from daily_challenges import DailyChallenge

class SnakeGame:
    def __init__(self):
        self.snake = Snake()
        self.ai_opponent = AiOpponent()
        self.obstacles = Obstacle()
        self.power_ups = PowerUp()
        self.leaderboards = Leaderboard()
        self.unlockables = Unlockable()
        self.achievements = Achievement()
        self.daily_challenges = DailyChallenge()
        self.score = 0

    def play(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()