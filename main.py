#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pygame
import pygame_menu

from constants import *
from objects import *
from population import Population



pygame.init()
   

population = Population(1000)
goal = Goal(RED, (WIDTH/2, 20))

clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE)

pygame.display.flip()

while True:

    for event in pygame.event.get():
       
        if event.type == pygame.QUIT:
            pygame.quit()
            break

    screen.fill(WHITE)

    goal.draw(screen)

    population.update(goal)
    population.draw(screen)
    if population.all_agents_are_dead():
        print("all agents are dead")
        population.calculate_fitness(goal)
        population.get_survivors()
        population.natural_selection()
        population.mutate_babies()


    pygame.display.update()
    clock.tick(30)


