#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame.math import Vector2

import math
from random import uniform, random

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

    def mutate(self, mutation_rate=0.01):

        for i, v in enumerate(self.directions):
            if i == 0:
                continue
            rand = random() 
            if rand < mutation_rate:
                random_angle = uniform(0.0, 2*math.pi)
                self.directions[i] = Vector2(math.cos(random_angle), math.sin(random_angle))


