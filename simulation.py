# Authors: Rick van Bellen, Tim Debets, Pierre Onghena
import pygame
from pygame.locals import *
from Robot import Robot
import settings
import math


def manual_play():
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

    # Create robot object and walls
    all_sprites = pygame.sprite.Group()
    robot = Robot(20, 12)
    all_sprites.add(robot)


    # Variable to keep the main loop running
    running = True

    # Setup the clock to fix framerate
    clock = pygame.time.Clock()

    # For printing numbers:
    font = pygame.font.SysFont("Courier New", 14)

    history_x = []
    history_y = []

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

        left_wheel = robot.Vl
        right_wheel = robot.Vr
        left_wheel_text = font.render("Speed left wheel:  " + (str(round(left_wheel, 2))), True, (0, 0, 0))
        text_areas.append(left_wheel_text)
        text_rect_left = left_wheel_text.get_rect()
        text_rect_left.left = 10
        text_rect_left.centery = 10
        text_rects.append(text_rect_left)
        right_wheel_text = font.render("Speed right wheel: " + (str(round(right_wheel, 2))), True, (0, 0, 0))
        text_areas.append(right_wheel_text)
        text_rect_right = right_wheel_text.get_rect()
        text_rect_right.left = 10
        text_rect_right.centery = 30
        text_rects.append(text_rect_right)
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

        # Draw all entities
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)


        # Update the screen
        pygame.display.flip()

        # Maintain 30 fps
        clock.tick(settings.fps)


if __name__ == "__main__":
    manual_play()
