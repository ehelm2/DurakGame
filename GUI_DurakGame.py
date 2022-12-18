# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 15:50:28 2022

@author: emily
"""
import pygame
from DurakGame import *
from card_dictionary import card_files

# def render_interface(window):
#     window.fill((25, 130, 56))
#     font = pygame.font.SysFont('imprintshadow', 60, True)
#     # Draw pile stays constant
#     window.blit(cardBack, (300, 100))

#     text = font.render('players hand:', True, (255, 255, 255))
#     window.blit(text,(100, 500))

pygame.init()
# bounds = (1000, 600)
# window = pygame.display.set_mode(bounds)
# pygame.display.set_caption('Durak')
# icon = pygame.image.load('icons/poker.png')
# pygame.display.set_icon(icon)

# cardBack = pygame.image.load('icons/design1.png')

#Game Loop
running = True
while running:
    key = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            key = event.key

    IntObj = pyGame()
    gamelogic = DurakGame(IntObj)
    gamelogic.play(IntObj, key)

    # render_interface(window)


    pygame.display.update()
