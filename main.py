#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pygame
from pygame.math import Vector2
import math
from random import random, uniform


size = w, h = 687, 419

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()


class Brain:
    def __init__(self, size):
        self.directions = [Vector2(0, 0)] * size
        self.step = 0
        self.randomize()

    def randomize(self):
        for i, v in enumerate(self.directions):
            random_angle = uniform(0.0, 2*math.pi)
            self.directions[i] = Vector2(math.cos(random_angle), math.sin(random_angle))

    def clone(self):
        clone_brain = Brain(len(self.directions))
        for i, di in enumerate(self.directions):
            clone_brain.directions[i] = Vector2(di.x, di.y)
        return clone_brain

    def mutate(self):
        mutation_rate = 0.01

        for i, v in enumerate(self.directions):
            if i == 0:
                continue
            rand = random() 
            if rand < mutation_rate:
                random_angle = uniform(0.0, 2*math.pi)
                self.directions[i] = Vector2(math.cos(random_angle), math.sin(random_angle))



class Dot:
    __SIZE__ = (5, 5)
    def __init__(self, color, initial_position):
        self.pos = Vector2(initial_position)
        self.vel = Vector2(0,0)
        self.acc = Vector2(0,0)
        self.color = color
        self.rect = pygame.Rect(self.pos, self.__SIZE__)

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)



class Agent(Dot):
    def __init__(self, color, initial_position, agent_id):
        super().__init__(color, initial_position)
        self.brain = Brain(400)
        self.dead = False
        self.name = f"{agent_id}"

        self.fitness = 0
        self.goal_reached = False

        self.fitness_over_time = []
        self.is_best = False

    def draw(self, screen):
        if self.is_best:
            self.color = GREEN
        pygame.draw.ellipse(screen, self.color, self.rect)


    def move(self):
        if len(self.brain.directions) > self.brain.step:
            self.acc = self.brain.directions[self.brain.step]
            self.brain.step += 1
        else:
            #print(f"Agent #{self.name} is out of breath, can't move anymore")
            self.dead = True

        self.vel += self.acc

        if self.vel.length_squared() > 25:
            self.vel.normalize_ip()
            self.vel *= 5
        self.pos += self.vel
        self.rect.update(self.pos, self.rect.size)


    def update(self, goal):
        if not self.dead and not self.goal_reached:
            self.move()

            if self.pos.x < 2 or self.pos.y < 2 or self.pos.x > w-2 or self.pos.y > h-2:
                #print(f"Agent #{self.name} is beyong the universe, dead")
                self.dead = True
            elif Vector2(self.rect.center).distance_to(Vector2(goal.rect.center)) < 5:
                print(f"Agent {self.name} reached the goal ! {self.fitness}, steps {self.brain.step}")
                self.goal_reached = True


    def calculate_fitness(self, goal):
        if self.goal_reached:
            self.fitness = 1.0/16.0 + (10000.0 / float(self.brain.step ** 2))
        else:
            distance_to_goal = Vector2(self.rect.center).distance_to(Vector2(goal.rect.center))
            #print(f"distance of #{self.name} from goal {distance_to_goal}")

            # the bigger the distance, the less fit is the agent
            if distance_to_goal == 0:
                distance_to_goal = 0.001

            self.fitness = 1.0 / (distance_to_goal ** 2)

    def give_birth(self):
        agent = Agent(BLACK, (w/2, h-10), agent_id=f"{self.name}X")
        agent.brain = self.brain.clone()
        return agent

class Population:
    def __init__(self, size):
        self.agents = []

        self._dead_agents = set()
        self._reached_goal_agents = set()

        self.fitness_sum = 0

        self.generation = 1
        self.best_parent =  0
        self.min_steps = 400

        for i in range(size):
            self.agents.append(Agent(BLACK, (w/2, h-10), agent_id=i))

    def draw(self, screen):
        for i,dot in enumerate(self.agents):
            if i == 0:
                continue
            dot.draw(screen)
        self.agents[0].draw(screen) 


    def update(self, goal):

        for dot in self.agents:
            if dot.brain.step > self.min_steps:
                dot.dead = True
            else:
                dot.update(goal)


    def calculate_fitness(self, goal):
        for a in self.agents:
            a.calculate_fitness(goal)

    def all_agents_are_dead(self):
        for a in self.agents:
            if not (a.dead or a.goal_reached):
                return False
        return True


    def get_survivors(self):
        survivors = 0
        for a in self.agents:
            if a.goal_reached:
                survivors += 1
                
        print(f"survivors of gen {self.generation} = {survivors}, min step: {self.min_steps}")
        print(f"rate: {survivors/len(self.agents)*100}%")

    def natural_selection(self):
        new_agents = []

        self.set_best_agent()
        self.fitness_sum = self.calculate_fitness_sum()

        print(self.best_parent)
        print(len(self.agents))

        new_agents.append(self.agents[self.best_parent].give_birth())
        new_agents[0].is_best = True

        for _ in range(1, len(self.agents)):
            parent = self.select_parent()
            new_agents.append(parent.give_birth())

        self.agents = new_agents.copy()

        self.generation += 1

        self._reached_goal_agents = set()
        self._dead_agents = set()


    def calculate_fitness_sum(self):
        fsum = 0
        for a in self.agents:
            fsum += a.fitness

        return fsum

    def select_parent(self):
        rand = uniform(0, self.fitness_sum)
        running_sum = 0
        for d in self.agents:
            running_sum += d.fitness
            if running_sum > rand:
                return d


    def mutate_babies(self):
        for i, a in enumerate(self.agents):
            if i == 0:
                continue
            a.brain.mutate()

    def set_best_agent(self):
        _max = 0
        max_index = 0
        for i, a in enumerate(self.agents):
            if a.fitness > _max:
                print(f"new best fitness ({a.name}): {a.fitness}, won: {a.goal_reached}")
                _max = a.fitness
                max_index = i
        self.best_parent = max_index
        if self.agents[self.best_parent].goal_reached:
            self.min_steps = self.agents[self.best_parent].brain.step
            print(f"min step: {self.min_steps}")




class Goal(Dot):
    __SIZE__ = (10, 10)
    

population = Population(1000)
goal = Goal(RED, (w/2, 20))

clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)

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


