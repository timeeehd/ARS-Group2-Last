# Main author: Rick van Bellen
# Co author: Pierre Onghena, Tim Debets

import math
import pygame
from pygame.locals import *
import settings
import numpy as np


# class that defines the robot
class Robot(pygame.sprite.Sprite):
    def __init__(self, radius, nr_sensors):
        super(Robot, self).__init__()
        self.id = 'robot'
        self.surf = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        self.surf.fill((255, 255, 255, 0))
        self.rect = self.surf.get_rect()
        # self.rect.move_ip((settings.SCREEN_WIDTH // 2 - radius, settings.SCREEN_HEIGHT // 2 - radius))
        self.rect.move_ip(200, 200)
        self.Vl = 10  # 1000000
        self.Vr = 10  # 1000000
        self.radius = radius
        self.l = 2 * radius
        self.x = self.rect.centerx
        self.y = self.rect.centery
        self.theta = 0

    # Define the robot movement
    def update(self, pressed_keys, ):
        # Handle user input
        if pressed_keys[K_w]:
            self.Vl += settings.V_step
            self.Vr += settings.V_step
        if pressed_keys[K_s]:
            self.Vl -= settings.V_step
            self.Vr -= settings.V_step
        if pressed_keys[K_a]:
            self.theta -= settings.theta_step
            if self.theta <= 0:
                self.theta += 2 * math.pi
        if pressed_keys[K_d]:
            self.theta += settings.theta_step
            if self.theta >= 2 * math.pi:
                self.theta -= 2 * math.pi

        # Move the robot, and register positions
        # If the wheels move at the same velocity, move forward
        self.x = self.x + self.Vl * math.cos(self.theta) * settings.dt
        self.y = self.y + self.Vl * math.sin(self.theta) * settings.dt

        self.rect.centerx = self.x
        self.rect.centery = self.y

        # Redraw the line indicating the direction the robot is facing
        radius = self.radius
        self.surf.fill((255, 255, 255, 0))
        pygame.draw.circle(self.surf, (100, 100, 200, 255), (radius, radius), radius)
        pygame.draw.line(self.surf, (0, 0, 0), (radius, radius),
                         (radius + math.cos(self.theta) * radius, radius + math.sin(self.theta) * radius), 5)

        # Keep robot on the screen
        if self.rect.left < 0:
            self.rect.left = 0
            self.x = self.rect.centerx
        if self.rect.right > settings.SCREEN_WIDTH:
            self.rect.right = settings.SCREEN_WIDTH
            self.x = self.rect.centerx
        if self.rect.top <= 0:
            self.rect.top = 0
            self.y = self.rect.centery
        if self.rect.bottom >= settings.SCREEN_HEIGHT:
            self.rect.bottom = settings.SCREEN_HEIGHT
            self.y = self.rect.centery
