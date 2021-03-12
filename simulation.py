# Authors: Rick van Bellen, Tim Debets, Pierre Onghena
import random

import pygame
from pygame.locals import *

from Beacon import Beacon
from Robot import Robot
import settings
import math

from utility import calc_distance


def manual_play():
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

    # Create robot object and walls
    all_sprites = pygame.sprite.Group()
    robot = Robot(20)
    all_sprites.add(robot)

    # Variable to keep the main loop running
    running = True

    # Setup the clock to fix framerate
    clock = pygame.time.Clock()

    # For printing numbers:
    font = pygame.font.SysFont("Courier New", 14)

    history_x = []
    history_y = []

    beacons = []
    for i in range(20):
        beacons.append(Beacon(random.uniform(0, settings.SCREEN_WIDTH), random.uniform(0, settings.SCREEN_HEIGHT), i))

    # Main game loop
    while running:
        history_x.append(robot.x)
        history_y.append(robot.y)
        # Look at every event in the queue
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                # If the user hit escape, stop the program
                if event.key == K_ESCAPE:
                    running = False

            # If the user closed the window, stop the program
            elif event.type == QUIT:
                running = False

        # Get the set of keys pressed and check for user input, update accordingly
        pressed_keys = pygame.key.get_pressed()
        robot.update(pressed_keys)

        # Fill the screen with white
        screen.fill((255, 255, 255))

        # Get everything ready to draw the text on the screen
        # Wheel speed
        text_areas = []
        text_rects = []

        left_wheel_text = font.render("Speed of robot:  " + (str(round(robot.v, 2))), True, (0, 0, 0))
        text_areas.append(left_wheel_text)
        text_rect_left = left_wheel_text.get_rect()
        text_rect_left.left = 10
        text_rect_left.centery = 30
        text_rects.append(text_rect_left)
        orientation_text = font.render("Orientation of robot: " + (str(round(robot.theta, 2))), True, (0, 0, 0))
        text_areas.append(orientation_text)
        orient_rect = orientation_text.get_rect()
        orient_rect.left = 10
        orient_rect.centery = 50
        text_rects.append(orient_rect)

        # # Fill covered area
        for i in range(len(history_x) - 1):
            pygame.draw.line(screen, (0, 0, 0), (history_x[i], history_y[i]), (history_x[i + 1], history_y[i + 1]), 3)

        # Write the needed text on the screen
        for i in range(len(text_areas)):
            screen.blit(text_areas[i], text_rects[i])

        for beacon in beacons:
            distance = calc_distance((robot.x, robot.y), (beacon.x, beacon.y))
            if distance <= settings.MAX_SENSOR_DIST:
                beacon.distance = distance
                # It draws now from center of circles
                pygame.draw.line(screen, (28, 144, 70), (robot.x, robot.y), (beacon.x, beacon.y), 2)
            pygame.draw.circle(screen, (0, 0, 0), (beacon.x, beacon.y), 10)


        # Draw all entities
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Update the screen
        pygame.display.flip()

        # Maintain 30 fps
        clock.tick(settings.fps)


if __name__ == "__main__":
    manual_play()
