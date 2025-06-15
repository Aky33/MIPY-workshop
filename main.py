from src.engine.game import Game
from src.screens.menu import Menu
from src.screens.intro import Intro

import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))

intro = Intro(screen)
intro.run()

menu = Menu(screen)
menu.run()

#game = Game()
#game.run()
