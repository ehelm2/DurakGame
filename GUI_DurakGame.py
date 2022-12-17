# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 15:50:28 2022

@author: emily
"""
import pygame

# icon_filepath = 

pygame.init()

screen = pygame.display.set_mode((1200,800))

# title and icon
pygame.display.set_caption('Durak')
icon = pygame.image.load('poker.png')
pygame.display.set_icon(icon)


#Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False