from src.engine.game import Game
from src.screens.menu import Menu

import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
menu = Menu(screen)
menu.run()

#game = Game()
#game.run()
