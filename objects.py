import pygame
from pygame.math import Vector2
from brain import Brain
from constants import *

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
    def __init__(self, color, initial_position, agent_id, steps):
        super().__init__(color, initial_position)
        self.steps = steps
        self.brain = Brain(self.steps)
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

            if self.pos.x < 2 or self.pos.y < 2 or self.pos.x > SCENE_WIDTH-2 or self.pos.y > SCENE_HEIGHT-2:
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

    def give_birth(self, birth_id):
        agent = Agent(BLACK, (SCENE_WIDTH/2, SCENE_HEIGHT-10), 
                      agent_id=f"{self.name}:{birth_id}", steps=self.steps)
        agent.brain = self.brain.clone()
        return agent



class Goal(Dot):
    __SIZE__ = (10, 10)
 
