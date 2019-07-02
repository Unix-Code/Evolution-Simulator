from math import atan2

from utils import euclid_distance


class Vector:
    MAX_SPEED = 10

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mag = euclid_distance((0, 0), (x, y))

    def normalize(self):
        return Vector(0, 0) if self.mag == 0 else self.div(self.mag);

    def add(self, other_vector):
        new_x = self.x + other_vector.x
        new_y = self.y + other_vector.y
        return Vector(new_x, new_y)

    def sub(self, other_vector):
        new_x = self.x - other_vector.x
        new_y = self.y - other_vector.y
        return Vector(new_x, new_y)

    def mult(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def mult_complex(self, scalarx, scalary):
        return Vector(self.x * scalarx, self.y * scalary)

    def div(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)

    def invert(self):
        return Vector(self.x * -1, self.y * -1)

    def invert_x(self):
        return Vector(self.x * -1, self.y)

    def invert_y(self):
        return Vector(self.x, self.y * -1)

    def set_mag(self, new_mag):
        return self.normalize().mult(new_mag)

    def limit(self, limit=MAX_SPEED):
        return self.normalize().mult(limit) if self.mag > limit else self

    def coords(self):
        return self.x, self.y

    def polar_coords(self):
        """
        Cartesion -> Polar
        :return: polar coordinates in format (r, theta)
        """
        return self.mag, atan2(self.y, self.x)

    @classmethod
    def steer_force(cls, target, location, velocity, max_force, max_speed=MAX_SPEED):
        return target.sub(location).set_mag(max_speed).sub(velocity).limit(max_force)

    @classmethod
    def null(cls):
        return Vector(0, 0)
