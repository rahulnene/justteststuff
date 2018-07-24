import math
import random
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D

class point:
    def __init__(self, xCoord, yCoord, zCoord):
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.zCoord - zCoord


# #ax + by = c
# class Line:
#     def __init__(self, a, b, c):
#         self.slope = -a/b
#         self.intercept = c/a

class body:
    def __init__(self, location, mass, velocity, name=""):
        self.location = location
        self.mass = mass
        self.velocity = velocity
        self.name = name


def calculate_single_body_acceleration(bodies, body_index):
    G_const = 6.67408e-11  # m3 kg-1 s-2
    acceleration = point(0, 0, 0)
    target_body = bodies[body_index]
    for index, external_body in enumerate(bodies):
        if index != body_index:
            r = (target_body.location.x - external_body.location.x) ** 2 + (
                        target_body.location.y - external_body.location.y) ** 2 + (
                            target_body.location.z - external_body.location.z) ** 2
            r = math.sqrt(r)
            tmp = G_const * external_body.mass / r ** 3
            acceleration.x += tmp * (external_body.location.x - target_body.location.x)
            acceleration.y += tmp * (external_body.location.y - target_body.location.y)
            acceleration.z += tmp * (external_body.location.z - target_body.location.z)
    return acceleration
