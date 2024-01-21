import sys
import random
import pygame
import copy


SCREEN_SIZE = 600
black = (0, 0, 0)


class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.color = color
        self.size = 1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.size)

    @staticmethod
    def randomxy():
        return int(random.random() * SCREEN_SIZE)

    @staticmethod
    def create(number, color):
        group = []
        for i in range(number):
            p = Particle(Particle.randomxy(), Particle.randomxy(), color)
            group.append(p)

        return group


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

    particles = []
    particles += Particle.create(2, "red")

    done = False
    while not done:
        screen.fill(black)
        for p in particles:
            p.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pygame.display.flip()
        # pygame.display.update()
        # pygame.time.Clock.tick(30)

    pygame.quit()
    sys.exit()
