import math
from random import random, uniform

from objects import Agent
from constants import *


class Population:
    def __init__(self, size, steps):
        self.agents = []

        self._dead_agents = set()
        self._reached_goal_agents = set()

        self.fitness_sum = 0

        self.generation = 1
        self.best_parent =  0
        self.min_steps = steps

        for i in range(size):
            self.agents.append(
                Agent(BLACK, (SCENE_WIDTH/2, SCENE_HEIGHT-10), agent_id=i, steps=steps)
            )

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
                print(f"agent {a.name} survived")
                
        print(f"survivors of gen {self.generation} = {survivors}, min step: {self.min_steps}")
        print(f"rate: {survivors/len(self.agents)*100}%")

    def natural_selection(self):
        new_agents = []

        self.set_best_agent()
        self.fitness_sum = self.calculate_fitness_sum()

        print(self.best_parent)
        print(len(self.agents))

        new_agents.append(self.agents[self.best_parent].give_birth(0))
        new_agents[0].is_best = True

        for i in range(1, len(self.agents)):
            parent = self.select_parent()
            new_agents.append(parent.give_birth(i))

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


    def mutate_babies(self, mutation_rate):
        for i, a in enumerate(self.agents):
            if i == 0:
                continue
            a.brain.mutate(mutation_rate)

    def set_best_agent(self):
        _max = 0
        max_index = 0
        for i, a in enumerate(self.agents):
            if a.fitness > _max:
                #print(f"new best fitness ({a.name}): {a.fitness}, won: {a.goal_reached}")
                _max = a.fitness
                max_index = i
        self.best_parent = max_index
        if self.agents[self.best_parent].goal_reached:
            self.min_steps = self.agents[self.best_parent].brain.step
            print(f"min step: {self.min_steps}")


