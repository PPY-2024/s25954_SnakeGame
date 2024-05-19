import pygame as pg
import unittest
from unittest.mock import patch

import pytest
import io
import sys

from snake_game.SnakeGame import *
class TestSnakeGame(unittest.TestCase):

    def test_get_random_position(self):
        # Check if the random position generated is within the valid range
        for _ in range(10):
            pos = get_random_position()
            self.assertTrue(RANGE[0] <= pos[0] <= RANGE[1])
            self.assertTrue(RANGE[0] <= pos[1] <= RANGE[1])

    def test_snake_collision_with_wall(self):
        # Test if snake collides with the wall
        snake.center = [0, WINDOW // 2]  # Place snake at left wall
        snake_dir = (-TILE_SIZE, 0)  # Move snake left
        game_over = False
        while not game_over:
            snake.move_ip(snake_dir)
            if (snake.left < 0 or snake.right > WINDOW or
                    snake.top < 0 or snake.bottom > WINDOW):
                game_over = True
        self.assertTrue(game_over)

    def test_snake_collision_with_self(self):
        # Test if snake collides with itself
        segments.clear()
        segments.append(pg.rect.Rect([TILE_SIZE * 3, TILE_SIZE * 3, TILE_SIZE - 2, TILE_SIZE - 2]))
        segments.append(pg.rect.Rect([TILE_SIZE * 2, TILE_SIZE * 3, TILE_SIZE - 2, TILE_SIZE - 2]))
        segments.append(pg.rect.Rect([TILE_SIZE, TILE_SIZE * 3, TILE_SIZE - 2, TILE_SIZE - 2]))
        snake.center = [TILE_SIZE, TILE_SIZE * 3]  # Place snake head next to its body
        snake_dir = (TILE_SIZE, 0)  # Move snake right
        game_over = False
        while not game_over:
            snake.move_ip(snake_dir)
            if snake.collidelist(segments[:-1]) != -1:
                game_over = True
        self.assertTrue(game_over)

    @patch('pygame.event.get')
    def test_game_quit(self, mock_event_get):
        # Test if the game quits when the quit event is triggered
        mock_event_get.return_value = [pg.event.Event(pg.QUIT)]
        with self.assertRaises(SystemExit):
            game("Test User")

if __name__ == '__main__':
    unittest.main()