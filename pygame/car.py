import pygame
import math
import numpy as np
def softmax(x):
  exp = np.exp(x- np.max(x,axis=1,keepdims=True))
  return exp/np.sum(exp,axis=1,keepdims=True)

def predict(w, x):
  logits = np.dot(x,w)
  softmaxed = softmax(logits)
  return softmaxed


class Car:
    def __init__(self,x,y,game):
        self.x = x
        self.y = y
        self.speed = 3
        self.angle = 0
        self.game = game
        self.surface = game.screen
        self.scale_factor = 0.1
        self._car_image = pygame.image.load("car.png")
        self.car_image = pygame.transform.scale(self._car_image,
                                                (int(self._car_image.get_width() * self.scale_factor),
                                                 int(self._car_image.get_height() * self.scale_factor)))
        self.car_image.set_colorkey((255,255,255))
        self.car_rect = self.car_image.get_rect()
        self.car_rect.center = (self.x, self.y)

    def draw(self):
        rotated_car = pygame.transform.rotate(self.car_image, (self.angle+3*90))
        rotated_rect = rotated_car.get_rect(center=self.car_rect.center)
        self.surface.blit(rotated_car, rotated_rect.topleft)

    def is_collision(self, img, img2,x= 0,y = 0):
        mask_img = pygame.mask.from_surface(img)
        mask_background = pygame.mask.from_surface(img2)
        offset = (((self.x - img.get_rect().center[0])),
                  ((self.y - img.get_rect().center[1])))
        poi = mask_background.overlap(mask_img, offset)
        print(poi)
        return poi

    def collision_point(self,x=0,y=0):
        color = self.game.background_img.get_at((x,y))
        if color==((255,255,255)) or color==((0,0,0)) or color==((255,0,0)):
            return True
        return False

    def boundary(self,x,y):
        return 0<=round(x)<self.game.width and 0<=round(y)<self.game.height

    def update(self):
        keys = pygame.key.get_pressed()
        pressed = str("None")

        self.angle %= 360
        if keys[pygame.K_LEFT]:
            pressed = str("LEFT")
            self.angle += 5
        if keys[pygame.K_RIGHT]:
            pressed = str("RIGHT")
            self.angle -= 5

        angle = math.radians(self.angle)

        old_x = self.x
        old_y = self.y

        # if keys[pygame.K_DOWN]:
        #     self.x -= self.speed * math.cos(angle)
        #     self.y += self.speed * math.sin(angle)
        if True:
            self.x += self.speed * math.cos(angle)
            self.y -= self.speed * math.sin(angle)

        self.car_rect.center = (round(self.x), round(self.y))

        if self.is_collision(self.car_image, self.game.track_border):
            self.x, self.y = old_x, old_y
            self.car_rect.center = (round(old_x), round(old_y))

        # if self.collision_point(round(self.x), round(self.y)):
        #     self.x, self.y = old_x, old_y
        #     self.car_rect.center = (round(old_x), round(old_y))

        readings = self.cast_rays(6,100)
        self.game.keys.append(pressed)
        self.game.data.append(readings)

    def update_auto(self):
        readings = self.cast_rays(6, 100)
        pressed = "None"
        key_logit = predict(self.game.weights, np.array(readings).reshape(1,-1))
        key = np.argmax(key_logit)
        if key == 0:
            pressed = "LEFT"
        if key == 1:
            pressed = "RIGHT"

        self.angle %= 360
        if pressed == "LEFT":
            self.angle += 5
        if pressed == "RIGHT":
            self.angle -= 5

        angle = math.radians(self.angle)

        old_x = self.x
        old_y = self.y

        if True:
            self.x += self.speed * math.cos(angle)
            self.y -= self.speed * math.sin(angle)

        self.car_rect.center = (round(self.x), round(self.y))

        if self.is_collision(self.car_image, self.game.track_border):
            self.x, self.y = old_x, old_y
            self.car_rect.center = (round(old_x), round(old_y))

        print(f"I pressed {pressed}")

    def cast_rays(self, num_rays, ray_length):
        ray_angles = [math.radians(-self.angle - 90 + i * (180 / (num_rays - 1))) for i in range(num_rays)]
        readings = []
        for angle in ray_angles:
            ray_dx = math.cos(angle)/2
            ray_dy = math.sin(angle)/2

            ray_x = self.x
            ray_y = self.y

            for l in range(ray_length):
                ray_x += ray_dx
                ray_y += ray_dy
                pygame.draw.aaline(self.surface, (255, 255, 0, 50), (self.x, self.y), (round(ray_x), round(ray_y)))

                if self.boundary(ray_x,ray_y) and self.collision_point(x=round(ray_x), y=round(ray_y)):
                    #print(ray_x,ray_y)
                    readings.append(math.sqrt((self.x-ray_x)**2+(self.y-ray_y)**2))
                    break

                if l == ray_length-1:
                    readings.append(math.sqrt((self.x - ray_x) ** 2 + (self.y - ray_y) ** 2))

        pygame.display.flip()
        return readings