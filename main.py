#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pygame
import pygame_menu

from menu import Menu

from constants import *
from objects import *
from population import Population


pygame.init()



def run_simulation():
    print("run simulation !!!!!!")

RESET_GAME = True
POPULATION = 1000
STEPS = 400
MUTATION_RATE = 0.01

def reset():
    print("Reset !!")
    global RESET_GAME
    RESET_GAME = True

def set_population(value):
    global POPULATION
    POPULATION = value

def set_steps(value):
    global STEPS
    STEPS = value

def set_mutation_rate(value):
    global MUTATION_RATE
    MUTATION_RATE = value

clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE)
menu = Menu(
    run_simulation, 
    reset, 
    set_population,
    set_steps,
    set_mutation_rate
).get_menu()

pygame.display.flip()

population = None
goal = None

while True:

    if RESET_GAME:
        RESET_GAME = False
        population = Population(POPULATION, STEPS)
        goal = Goal(RED, (SCENE_WIDTH/2, 20))

    screen.fill(WHITE)

    events = pygame.event.get()
    menu.update(events)
    menu.draw(screen)

    if pygame_menu.events.MENU_LAST_WIDGET_DISABLE_ACTIVE_STATE in menu.get_last_update_mode()[0]:
        events = []

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    goal.draw(screen)

    population.update(goal)
    population.draw(screen)
    if population.all_agents_are_dead():
        print("all agents are dead")
        population.calculate_fitness(goal)
        population.get_survivors()
        population.natural_selection()
        population.mutate_babies(MUTATION_RATE)


    pygame.display.update()
    clock.tick(30)


