# Main author: Rick van Bellen
# Co author: Pierre Onghena, Tim Debets

import math
import pygame
from pygame.locals import *
import settings
import numpy as np
from utility import *


def predict_position(beacon_features):
    # If there is one beacon or less, we can't predict the position
    if len(beacon_features) <= 2:
        return None
    # If there are 2, we can predict the pose with 2 beacons
    # elif len(beacon_features) == 2:
    #     # Calculate position
    #     x0, y0, r0 = beacon_features[0][0].x, beacon_features[0][0].y, beacon_features[0][0].distance
    #     x1, y1, r1 = beacon_features[1][0].x, beacon_features[1][0].y, beacon_features[1][0].distance
    #     intersection1, intersection2 = intersection_points(x0, y0, r0, x1, y1, r1)
    #
    #     # Choose just one intersection to be the right one
    #     intersection = intersection1
    #
    #     # Calculate orientation
    #     angle_intersection_to_circle_center = math.atan(abs(intersection[1] - y0) / abs(intersection[0] - x0))
    #     orientation = (angle_intersection_to_circle_center + beacon_features[0][1]) % (2 * math.pi)
    #     return np.array([intersection[0], intersection[1], orientation])
    # If there are 3 or more, take 3 and predict the pose
    else:
        x0, y0, r0 = beacon_features[0][0].x, beacon_features[0][0].y, beacon_features[0][0].distance
        x1, y1, r1 = beacon_features[1][0].x, beacon_features[1][0].y, beacon_features[1][0].distance
        x2, y2, r2 = beacon_features[2][0].x, beacon_features[2][0].y, beacon_features[2][0].distance

        # Intersections of circle 1 and 2
        intersection1, intersection2 = intersection_points(x0, y0, r0, x1, y1, r1)

        # Intersections of circle 1 and 3
        intersection3, intersection4 = intersection_points(x0, y0, r0, x2, y2, r2)
        # Get the final verdict
        if calc_distance(intersection1, intersection3) < 0.01 or calc_distance(intersection1, intersection4) < 0.01:
            x, y = intersection1
        else:
            x, y = intersection2

        # I still don't know which is correct without using theta so I'll just return x3 and y3
        angle_intersection_to_circle_center = math.atan(abs(y - y0) / abs(x - x0))
        orientation = (angle_intersection_to_circle_center + beacon_features[0][1]) % (2 * math.pi)
        return np.array([x, y, orientation])


# Method for Kalman filter
def kalman_filter(previous_state, previous_covariance, action, beacon_features, B, R, Q):
    A = np.eye(3)
    C = np.eye(3)
    # Calculate the observation from the beacon features
    z = predict_position(beacon_features)
    if z is None:
        z = previous_state
    # Sensor noise
    noise_x, noise_y, noise_t = np.random.normal(0, 0.3), np.random.normal(0, 0.3), \
                                np.random.normal(0, 0.1)
    noise = [noise_x, noise_y, noise_t]
    z = np.add(z, noise)

    # Prediction
    pred_state = A.dot(previous_state) + B.dot(action)
    pred_covariance = A.dot(previous_covariance).dot(A.T) + R

    # Correction
    if z is not None:
        K = pred_covariance.dot(C.T).dot(np.linalg.inv(C.dot(pred_covariance).dot(C.T) + Q))
        state = pred_state + K.dot(z - C.dot(pred_state))
        covariance = (np.eye(3) - K.dot(C)).dot(pred_covariance)
    else:
        state = pred_state
        covariance = pred_covariance
    return state, covariance


# class that defines the robot
class Robot(pygame.sprite.Sprite):
    def __init__(self, radius):
        super(Robot, self).__init__()
        self.id = 'robot'
        self.surf = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        self.surf.fill((255, 255, 255, 0))
        self.rect = self.surf.get_rect()
        self.rect.move_ip(200, 200)
        self.v = 0
        self.radius = radius
        self.l = 2 * radius
        self.x = self.rect.centerx
        self.y = self.rect.centery
        self.theta = 0
        self.state = np.array([self.x, self.y, self.theta])
        self.covariance = np.diag([0, 0, 0])

    # Define the robot movement
    def update(self, pressed_keys, beacons):
        omega = 0
        # Handle user input
        if pressed_keys[K_w]:
            self.v += settings.V_step
        if pressed_keys[K_s]:
            self.v -= settings.V_step
        if pressed_keys[K_a]:
            omega = settings.theta_step
            self.theta -= omega
            if self.theta <= 0:
                self.theta += 2 * math.pi
        if pressed_keys[K_d]:
            omega = settings.theta_step
            self.theta += omega
            if self.theta >= 2 * math.pi:
                self.theta -= 2 * math.pi
        if pressed_keys[K_x]:
            self.v = 0

        # Move the robot, and register positions
        # If the wheels move at the same velocity, move forward
        self.x = self.x + self.v * math.cos(self.theta) * settings.dt
        self.y = self.y + self.v * math.sin(self.theta) * settings.dt

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

        # Update the prediction of the robot location
        action = np.array([self.v, omega])
        dt = settings.dt
        B = np.array([[dt * math.cos(self.theta), 0],
                      [dt * math.sin(self.theta), 0],
                      [0, dt]])
        # TODO: update R and Q
        R = np.diag([0.6, 0.6, 0.4])
        Q = np.diag([0.1, 0.1, 0.05])
        beacon_features = []
        for beacon in beacons:
            phi = self.theta - beacon.angle
            if phi < 0:
                phi = 2 * math.pi + phi
            beacon_features.append(np.array([beacon, phi]))
        self.state, self.covariance = kalman_filter(self.state, self.covariance, action, beacon_features, B, R, Q)
