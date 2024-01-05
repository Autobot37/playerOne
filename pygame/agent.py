import pygame
import sys
import math
from car import Car
import os
import pickle
if not os.path.exists("weights.pkl"):
    from model import train
    train()

class Game:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width,self.height))
        icon = pygame.image.load('icon.jpg')
        pygame.display.set_icon(icon)
        self.running = True
        self._background_img = pygame.image.load("background.png")
        self.background_img = pygame.transform.scale(self._background_img,(self.width,self.height))

        self._track_border = pygame.image.load("track-border.png")
        self.track_border = pygame.transform.scale(self._track_border, (self.width, self.height))

        self.data = []
        self.keys = []
        self.car = Car(self.width//2,3*self.height//4 - 24,self)

        with open('weights.pkl', 'rb') as file:
            self.weights = pickle.load(file)
        self.clock = pygame.time.Clock()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.car.update_auto()
    def draw(self):
        pygame.display.set_caption(f"Autopilot - {self.clock.get_fps():.2f}")
        self.screen.fill((255,255,255))
        self.screen.blit(self.background_img, (0, 0))
        self.car.draw()
        pygame.display.flip()

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()
        return self.data, self.keys
        sys.exit()


if __name__ == "__main__":
    game = Game()
    data, keys = game.run()
    print(data, keys)