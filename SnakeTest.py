import unittest
import pygame as pg
from snake_game import SnakeGame

class TestSnakeGame(unittest.TestCase):
    def test_snake_movement(self):

        game = SnakeGame(5, 100)
        initial_position = game.snake.center
        game.handle_event(pg.K_w)  # Move snake up
        self.assertEqual(game.snake.center, (initial_position[0], initial_position[1] - 100))
        game.handle_event(pg.K_s)  # Move snake down
        self.assertEqual(game.snake.center, initial_position)

    def test_food_generation(self):
        game = SnakeGame(5, 100)
        food_positions = set()
        for _ in range(100):
            game.generate_food()
            food_positions.add(game.food.center)
        self.assertTrue(len(food_positions) > 1)

    def test_game_over(self):

        game = SnakeGame(5, 100)
        game.snake.center = (0, 0)
        game.handle_event(pg.K_d)
        game.update_game()
        self.assertTrue(game.game_over)

        game.reset_game()
        game.snake.center = (250, 250)
        game.handle_event(pg.K_a)
        game.update_game()
        self.assertFalse(game.game_over)

if __name__ == '__main__':
    unittest.main()