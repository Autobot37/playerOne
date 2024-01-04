import pygame
import math
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
        offset = (round((self.x - img.get_rect().center[0])),
                  round((self.y - img.get_rect().center[1])))
        poi = mask_background.overlap(mask_img, offset)
        return poi is not None

    def collision_point(self,img,x=0,y=0):
        mask_background = pygame.mask.from_surface(self.game.track_border)
        if mask_background.get_at((x,y)):
            return True
        return False

    def update(self):
        keys = pygame.key.get_pressed()

        self.angle %= 360
        if keys[pygame.K_LEFT]:
            self.angle += 5
        if keys[pygame.K_RIGHT]:
            self.angle -= 5

        angle = math.radians(self.angle)

        old_x = self.x
        old_y = self.y

        if keys[pygame.K_DOWN]:
            self.x -= self.speed * math.cos(angle)
            self.y += self.speed * math.sin(angle)
        if keys[pygame.K_UP]:
            self.x += self.speed * math.cos(angle)
            self.y -= self.speed * math.sin(angle)

        self.car_rect.center = (round(self.x), round(self.y))

        if self.is_collision(self.car_image, self.game.track_border):
            self.x, self.y = old_x, old_y
            self.car_rect.center = (round(old_x), round(old_y))

        #self.cast_rays(4,50)

    def cast_rays(self, num_rays, ray_length):
        ray_angles = [math.radians(self.angle - 90 + i * (180 / (num_rays - 1))) for i in range(num_rays)]
        ray_lines_surface = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)

        for angle in ray_angles:
            ray_dx = math.cos(angle)
            ray_dy = math.sin(angle)

            ray_x = self.x
            ray_y = self.y

            for _ in range(ray_length):
                ray_x += ray_dx
                ray_y += ray_dy

                if self.collision_point(self.game.track_border, x=round(ray_x), y=round(ray_y)):
                    pygame.draw.aaline(ray_lines_surface, (255, 255, 0, 50), (self.x, self.y),
                                       (round(ray_x), round(ray_y)))
                    print(ray_x,ray_y)
                    break

        self.surface.blit(ray_lines_surface, (0, 0))
        pygame.display.flip()