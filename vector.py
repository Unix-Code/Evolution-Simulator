from math import atan2, degrees

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

    def heading(self, in_degrees=False):
        angle = atan2(self.y, self.x)
        return degrees(angle) if in_degrees else angle

    def coords(self):
        return self.x, self.y

    def polar_coords(self):
        """
        Cartesion -> Polar
        :return: polar coordinates in format (r, theta)
        """
        return self.mag, self.heading()

    @classmethod
    def steer_force(cls, target, location, velocity, max_force, max_speed=MAX_SPEED):
        return target.sub(location).set_mag(max_speed).sub(velocity).limit(max_force)

    @classmethod
    def steer_forces(cls, targets, location, velocity, max_force, max_speed=MAX_SPEED):
        target_vels = [target.sub(location) for target in targets]
        weighted_target_vels = [t.mult(euclid_distance(Vector.null().coords(), t.coords()) ** 2) for t in target_vels]
        return Vector.average_many(weighted_target_vels).set_mag(max_speed).sub(velocity).limit(max_force)

    @classmethod
    def null(cls):
        return Vector(0, 0)

    @classmethod
    def average_many(cls, vectors):
        sum_x = 0
        sum_y = 0
        for vector in vectors:
            sum_x += vector.x
            sum_y += vector.y
        avg_x = sum_x / len(vectors)
        avg_y = sum_y / len(vectors)
        return Vector(avg_x, avg_y)
